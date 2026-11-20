//! Integration Test Suite for Migration and Reversal Qualification (Step 17).
//!
//! Complies with Step 17 finish criteria:
//! - "Two imports produce the same records"
//! - "both readers reconcile with a signed difference ledger"
//! - "Roll forward, inject a failure, and roll back including operations accepted after the snapshot"
//! - "Zero lost accepted work, duplicated effects or dual writers"
//!
//! Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P06 (Canonical Structured Formats)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics)
//! - P12 (Statistical Proof & Regression Bounds)

use migration::{
    CutoverCoordinator, FencingCutoverError, LegacyArtifact, LegacyEvent, LegacyMemoryRecord,
    LegacyOperation, LegacyRevision, LegacyStateReader, LegacyStateSnapshot, LegacyVaultReference,
    ReversalDrillHarness, ShadowReaderReconciler, StateMapper, WriterRole,
};
use store::{FenceToken, OutboxRecord, OutboxStatus};

fn create_fixture_legacy_snapshot() -> LegacyStateSnapshot {
    LegacyStateSnapshot {
        workspace_id: "ws-legacy-fixture-01".to_string(),
        revisions: vec![
            LegacyRevision {
                revision_id: 1,
                timestamp_epoch_s: 1_000_000,
                author: "Krish Ujeniya".to_string(),
                checksum: "sha256-rev-1".to_string(),
            },
            LegacyRevision {
                revision_id: 2,
                timestamp_epoch_s: 1_000_050,
                author: "Krish Ujeniya".to_string(),
                checksum: "sha256-rev-2".to_string(),
            },
        ],
        operations: vec![
            LegacyOperation {
                op_id: "op-001".to_string(),
                idempotency_key: "idem-key-001".to_string(),
                action_type: "billing_charge".to_string(),
                raw_payload: "{\"amount_micros\": 1000}".to_string(),
                status: "confirmed".to_string(),
                retries: 0,
                updated_epoch_s: 1_000_010,
            },
            LegacyOperation {
                op_id: "op-002".to_string(),
                idempotency_key: "idem-key-002".to_string(),
                action_type: "crm_sync".to_string(),
                raw_payload: "{\"account\": \"acme\"}".to_string(),
                status: "confirmed".to_string(),
                retries: 1,
                updated_epoch_s: 1_000_060,
            },
        ],
        events: vec![
            LegacyEvent {
                event_seq: 1,
                timestamp: 1_000_000,
                kind: "workspace_created".to_string(),
                body_json: "{\"name\": \"main\"}".to_string(),
            },
            LegacyEvent {
                event_seq: 2,
                timestamp: 1_000_050,
                kind: "policy_applied".to_string(),
                body_json: "{\"mode\": \"strict\"}".to_string(),
            },
        ],
        memories: vec![
            LegacyMemoryRecord {
                memory_id: "mem-01".to_string(),
                tier: "recall".to_string(),
                key: "client_preference".to_string(),
                content: "Keep budget under 12 hours".to_string(),
                created_epoch_s: 1_000_020,
            },
        ],
        vault_refs: vec![
            LegacyVaultReference {
                ref_id: "vault-01".to_string(),
                scope: "crm".to_string(),
                secret_alias: "crm_api_token".to_string(),
                vault_path: "secrets/crm".to_string(),
            },
        ],
        artifacts: vec![
            LegacyArtifact {
                artifact_id: "art-01".to_string(),
                rel_path: "proposals/onboarding.toon".to_string(),
                sha256_hex: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855".to_string(),
                size_bytes: 2048,
            },
        ],
    }
}

#[test]
fn test_two_independent_imports_produce_identical_canonical_records() {
    let legacy = create_fixture_legacy_snapshot();
    let reader = LegacyStateReader::new(legacy.clone());
    let source_digest = reader.calculate_snapshot_digest();

    // 1. First import
    let import1 = StateMapper::map_snapshot(reader.read_snapshot())
        .expect("First import must succeed");

    // 2. Second independent import
    let import2 = StateMapper::map_snapshot(reader.read_snapshot())
        .expect("Second import must succeed");

    // 3. Verify determinism receipt
    let receipt = StateMapper::verify_deterministic_import(&import1, &import2, &source_digest);
    assert!(
        receipt.is_identical_match,
        "Two independent imports must produce identical canonical records"
    );
    assert_eq!(receipt.mapped_events_count, 2);
    assert_eq!(receipt.mapped_outbox_count, 2);
    assert_eq!(receipt.mapped_memory_count, 1);
    assert_eq!(receipt.mapped_artifacts_count, 1);
    assert_eq!(import1.canonical_digest, import2.canonical_digest);
}

#[test]
fn test_shadow_read_and_signed_difference_ledger_reconciliation() {
    let legacy = create_fixture_legacy_snapshot();
    let canonical = StateMapper::map_snapshot(&legacy)
        .expect("Mapping must succeed");

    // 1. Reconcile clean matching stores
    let ledger = ShadowReaderReconciler::reconcile(&legacy, &canonical, 1_000_100);
    assert!(
        ledger.is_reconciled,
        "Clean shadow read must produce reconciled state"
    );
    assert_eq!(ledger.discrepancies.len(), 0);
    assert!(ledger.matched_entities_count >= 5);
    assert!(ledger.signed_attestation.starts_with("SIG-RECON-SHA256:"));

    // 2. Inject deliberate divergence in canonical and verify detection
    let mut modified_canonical = canonical.clone();
    modified_canonical.events.pop(); // Remove an event

    let divergent_ledger = ShadowReaderReconciler::reconcile(&legacy, &modified_canonical, 1_000_100);
    assert!(
        !divergent_ledger.is_reconciled,
        "Divergent shadow read must detect discrepancies"
    );
    assert!(!divergent_ledger.discrepancies.is_empty());
}

#[test]
fn test_writer_fencing_and_split_brain_protection() {
    let mut fence = FenceToken::new(5);
    let mut coordinator = CutoverCoordinator::new(fence);

    assert_eq!(coordinator.active_role(), WriterRole::LegacyPrimary);

    // 1. Authorize legacy write before fencing
    assert!(coordinator.authorize_write(WriterRole::LegacyPrimary, fence).is_ok());

    // 2. Reject stale fence token
    let stale_fence = FenceToken::new(3);
    assert!(coordinator.fence_writes(stale_fence).is_err());

    // 3. Advance fence and fence writes
    fence = fence.next();
    assert_eq!(coordinator.fence_writes(fence).unwrap(), fence);
    assert_eq!(coordinator.active_role(), WriterRole::FencedDraining);

    // 4. Writes are blocked during draining
    assert_eq!(
        coordinator.authorize_write(WriterRole::LegacyPrimary, fence),
        Err(FencingCutoverError::WritesFencedDuringDraining)
    );

    // 5. Drain in-flight operations
    let mut in_flight = vec![OutboxRecord {
        effect_id: "eff-drain-01".to_string(),
        operation_key: "key-drain-01".to_string(),
        effect_type: "billing".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1_000_000,
    }];
    let drained = coordinator.drain_in_flight(&mut in_flight, 1_000_100).unwrap();
    assert_eq!(drained, 1);
    assert_eq!(in_flight[0].status, OutboxStatus::Confirmed);

    // 6. Transfer ownership to Canonical Authoritative writer
    let cursor = coordinator.save_migration_cursor("cursor-01", 2, "hash123", 1_000_100);
    let receipt = coordinator.transfer_writer_ownership(&cursor, 1_000_100).unwrap();
    assert_eq!(receipt.to_role, WriterRole::CanonicalAuthoritative);
    assert!(receipt.is_legacy_sealed);

    // 7. Verify legacy writer is now permanently sealed (split-brain protection)
    let legacy_write_attempt = coordinator.authorize_write(WriterRole::LegacyPrimary, fence);
    assert_eq!(legacy_write_attempt, Err(FencingCutoverError::LegacyWriterSealed));
    assert_eq!(coordinator.dual_writer_attempts(), 1);
}

#[test]
fn test_reversal_drill_roll_forward_failure_injection_and_rollback() {
    let base_snapshot = create_fixture_legacy_snapshot();

    // Operations accepted after the snapshot (W_post) during cutover window
    let post_snapshot_ops = vec![
        OutboxRecord {
            effect_id: "op-post-001".to_string(),
            operation_key: "idem-key-post-001".to_string(),
            effect_type: "crm_update".to_string(),
            payload_json: "{\"stage\": \"proposal_sent\"}".to_string(),
            status: OutboxStatus::Pending,
            retry_count: 0,
            updated_at_epoch_s: 1_000_110,
        },
        OutboxRecord {
            effect_id: "op-post-002".to_string(),
            operation_key: "idem-key-post-002".to_string(),
            effect_type: "billing_reservation".to_string(),
            payload_json: "{\"reserve_micros\": 500000}".to_string(),
            status: OutboxStatus::Pending,
            retry_count: 0,
            updated_at_epoch_s: 1_000_120,
        },
    ];

    let result = ReversalDrillHarness::run_drill(&base_snapshot, post_snapshot_ops);

    // Assert Step 17 finish test requirements:
    // - Zero lost accepted work (post-snapshot operations preserved)
    // - Zero duplicated effects
    // - Zero dual writers
    assert!(result.drill_passed, "Cutover reversal drill must pass");
    assert_eq!(result.pre_snapshot_operations_count, 2);
    assert_eq!(result.post_snapshot_accepted_count, 2);
    assert_eq!(result.recovered_total_work_count, 4);
    assert_eq!(result.lost_accepted_work_count, 0, "Zero lost accepted work");
    assert_eq!(result.duplicated_effects_detected, 0, "Zero duplicated effects");
    assert_eq!(result.dual_writer_violations_detected, 0, "Zero dual writers");
}
