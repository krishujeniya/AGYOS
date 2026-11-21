//! Integration Test Suite for Release Certification Qualification (Step 18).
//!
//! Complies with Step 18 finish criteria:
//! - "Only authorized commit/push can trigger publication"
//! - "Only exact-SHA passing CI plus separate approval can deploy the digest and execute the live cutover for that profile"
//! - "Recheck the fence, cursor and in-flight ledger at the actual switch"
//! - "Decline, failed CI, stale evidence and changed artifact all block"
//! - "Rollback and signed human handover succeed on a clean machine"
//!
//! Principles:
//! - P01 (Grounded Intent & Explicit Contracts)
//! - P05 (Least Privilege & Complete Mediation)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Build Provenance & Supply Chain Integrity)
//! - P09 (Explicit State & Invariants)
//! - P10 (Leases with Fencing & Atomic Sagas)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)

use migration::{CutoverCoordinator, WriterRole};
use release::{
    CleanMachineVerifier, ClientDiscoveryProject, LiveCutoverGuard, OperatorApprovalToken,
    ReleaseCandidate, ReleaseGateEngine, ReleaseGateFailure,
};
use store::{FenceToken, OutboxRecord, OutboxStatus};

fn create_valid_release_candidate(commit_sha: &str, current_epoch: u64) -> ReleaseCandidate {
    let digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855".to_string();

    let git_pub = OperatorApprovalToken {
        decision_id: "dec-git-01".to_string(),
        approver_name: "Krish Ujeniya".to_string(),
        approved_revision: commit_sha.to_string(),
        action_type: "git_publication".to_string(),
        approved: true,
        timestamp_epoch_s: current_epoch,
    };

    let prod_rel = OperatorApprovalToken {
        decision_id: "dec-prod-01".to_string(),
        approver_name: "Krish Ujeniya".to_string(),
        approved_revision: commit_sha.to_string(),
        action_type: "production_release".to_string(),
        approved: true,
        timestamp_epoch_s: current_epoch,
    };

    ReleaseCandidate {
        release_tag: "v1.0.0-rc1".to_string(),
        target_commit_sha: commit_sha.to_string(),
        ci_run_sha: commit_sha.to_string(),
        ci_status: "success".to_string(),
        evidence_timestamp_epoch_s: current_epoch - 60, // 60s ago
        artifact_digest: digest.clone(),
        provenance_digest: digest,
        rights_cleared: true,
        zero_secrets_leaked: true,
        ast_checks_passed: true,
        measured_route_p99_ms: 35,
        measured_status_p99_ms: 22,
        measured_durable_ack_p99_ms: 110,
        git_publication_approval: Some(git_pub),
        production_release_approval: Some(prod_rel),
    }
}

#[test]
fn test_complete_client_discovery_to_handover_project_lifecycle() {
    let mut project = ClientDiscoveryProject::new_fixture("proj-onboard-01", "Acme Holdings");

    // Initial state: work cap 20 hours
    assert_eq!(project.initial_work_cap_hours, 20);

    // Operator corrects work cap from 20 hours to 12 hours
    project.apply_operator_correction(12);
    assert_eq!(project.corrected_work_cap_hours, 12);

    // Generate proposal artifact
    project.generate_proposal_artifact();
    assert!(!project.artifact_sha256.is_empty());
    assert!(project.artifact_body.contains("two_week_cap_hours: 12"));

    // Verify zero outbound delivery in sandbox
    let zero_outbound = project.sandbox_verify_zero_outbound_delivery();
    assert!(zero_outbound, "Sandbox must block all outbound deliveries");
    assert_eq!(project.outbound_deliveries_executed, 0);

    // Operator signs handover certificate
    let cert = project.sign_handover("Krish Ujeniya", 1_000_100);
    assert_eq!(cert.authorizing_operator, "Krish Ujeniya");
    assert_eq!(cert.agreed_cap_hours, 12);
    assert!(cert.outbound_external_deliveries_blocked);
    assert_eq!(cert.handover_status, "DELIVERED_VERIFIED");
    assert!(cert.certificate_signature.starts_with("SIG-HANDOVER:"));
}

#[test]
fn test_declined_or_unconfirmed_external_action_issues_no_delivery_receipt() {
    let mut project = ClientDiscoveryProject::new_fixture("proj-declined-01", "Gamma Corp");
    project.apply_operator_correction(12);
    project.generate_proposal_artifact();
    project.sandbox_verify_zero_outbound_delivery();

    // 1. Explicitly declined external action -> NO delivery receipt
    project.decline_external_action();
    let cert_declined = project.sign_handover("Krish Ujeniya", 1_000_100);
    assert_eq!(
        cert_declined.handover_status,
        "NO_DELIVERY_RECEIPT_DECLINED_OR_UNCONFIRMED"
    );
    assert_eq!(
        cert_declined.certificate_signature,
        "NO_RECEIPT_DECLINED_OR_UNCONFIRMED"
    );

    // 2. Unconfirmed external action -> NO delivery receipt
    project.external_action_declined = false;
    project.external_action_confirmed = false;
    let cert_unconfirmed = project.sign_handover("Krish Ujeniya", 1_000_100);
    assert_eq!(
        cert_unconfirmed.handover_status,
        "NO_DELIVERY_RECEIPT_DECLINED_OR_UNCONFIRMED"
    );
    assert_eq!(
        cert_unconfirmed.certificate_signature,
        "NO_RECEIPT_DECLINED_OR_UNCONFIRMED"
    );
}

#[test]
fn test_blocking_on_declined_or_missing_operator_approval() {
    let sha = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678";
    let now = 1_000_000;
    let mut candidate = create_valid_release_candidate(sha, now);

    // 1. Missing Git publication approval -> BLOCK
    candidate.git_publication_approval = None;
    let res1 = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res1, Err(ref errs) if errs.contains(&ReleaseGateFailure::GitPublicationDeclinedOrMissing)),
        "Missing Git publication approval must block release"
    );

    // 2. Declined Git publication approval -> BLOCK
    candidate.git_publication_approval = Some(OperatorApprovalToken {
        decision_id: "dec-git-01".to_string(),
        approver_name: "Krish Ujeniya".to_string(),
        approved_revision: sha.to_string(),
        action_type: "git_publication".to_string(),
        approved: false, // Operator declined
        timestamp_epoch_s: now,
    });
    let res2 = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res2, Err(ref errs) if errs.contains(&ReleaseGateFailure::GitPublicationDeclinedOrMissing)),
        "Declined Git publication approval must block release"
    );

    // 3. Declined Production release approval -> BLOCK
    candidate.git_publication_approval = Some(OperatorApprovalToken {
        decision_id: "dec-git-01".to_string(),
        approver_name: "Krish Ujeniya".to_string(),
        approved_revision: sha.to_string(),
        action_type: "git_publication".to_string(),
        approved: true,
        timestamp_epoch_s: now,
    });
    candidate.production_release_approval = Some(OperatorApprovalToken {
        decision_id: "dec-prod-01".to_string(),
        approver_name: "Krish Ujeniya".to_string(),
        approved_revision: sha.to_string(),
        action_type: "production_release".to_string(),
        approved: false, // Operator declined
        timestamp_epoch_s: now,
    });
    let res3 = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res3, Err(ref errs) if errs.contains(&ReleaseGateFailure::ProductionReleaseDeclinedOrMissing)),
        "Declined production release approval must block release"
    );
}

#[test]
fn test_blocking_on_failed_ci_or_sha_mismatch() {
    let sha = "11223344556677889900aabbccddeeff11223344";
    let now = 1_000_000;
    let mut candidate = create_valid_release_candidate(sha, now);

    // 1. Exact-SHA mismatch -> BLOCK
    candidate.ci_run_sha = "99887766554433221100ffeeddccbbaa99887766".to_string();
    let res_sha = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_sha, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::ShaMismatch { .. }))),
        "SHA mismatch between target and CI must block release"
    );

    // 2. Failed CI build status -> BLOCK
    candidate.ci_run_sha = sha.to_string();
    candidate.ci_status = "failure".to_string();
    let res_ci = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_ci, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::CiBuildFailed { .. }))),
        "Failed CI run must block release"
    );
}

#[test]
fn test_blocking_on_stale_evidence_or_changed_artifact_digest() {
    let sha = "aabbccddeeff00112233445566778899aabbccdd";
    let now = 1_000_000;
    let mut candidate = create_valid_release_candidate(sha, now);

    // 1. Stale evidence (older than 3600s window) -> BLOCK
    candidate.evidence_timestamp_epoch_s = now - 7200; // 2 hours old
    let res_stale = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_stale, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::StaleEvidence { .. }))),
        "Stale verification evidence must block release"
    );

    // 2. Changed artifact digest (tampering or mismatch) -> BLOCK
    candidate.evidence_timestamp_epoch_s = now - 60;
    candidate.artifact_digest = "modified_tampered_digest_hex_0123456789".to_string();
    let res_digest = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_digest, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::ChangedArtifactDigest { .. }))),
        "Modified artifact digest must block release"
    );

    // 3. Future evidence timestamp -> BLOCK
    candidate.artifact_digest = candidate.provenance_digest.clone();
    candidate.evidence_timestamp_epoch_s = now + 600; // In the future!
    let res_future = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_future, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::StaleEvidence { .. }))),
        "Future evidence timestamp must block release"
    );

    // 4. Swapped or replayed approval token -> BLOCK
    candidate.evidence_timestamp_epoch_s = now - 60;
    // Put git_publication approval in production_release slot
    candidate.production_release_approval = candidate.git_publication_approval.clone();
    let res_swapped = ReleaseGateEngine::evaluate_candidate(&candidate, now, 3600);
    assert!(
        matches!(res_swapped, Err(ref errs) if errs.contains(&ReleaseGateFailure::ProductionReleaseDeclinedOrMissing)),
        "Swapped approval token with wrong action_type must block release"
    );
}

#[test]
fn test_fence_cursor_inflight_recheck_at_actual_cutover() {
    let sha = "5566778899aabbccddeeff001122334455667788";
    let now = 1_000_000;
    let candidate = create_valid_release_candidate(sha, now);

    let fence = FenceToken::new(20);
    let mut coordinator = CutoverCoordinator::new(fence);

    // Fence writes
    let next_fence = fence.next();
    coordinator.fence_writes(next_fence).unwrap();
    assert_eq!(coordinator.active_role(), WriterRole::FencedDraining);

    let cursor = coordinator.save_migration_cursor("cursor-step-18", 5, "snapshot-digest", now);

    // 1. In-flight operations remaining -> BLOCK
    let uncommitted_outbox = vec![OutboxRecord {
        effect_id: "eff-pending-01".to_string(),
        operation_key: "key-pending-01".to_string(),
        effect_type: "billing".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Pending, // Uncommitted!
        retry_count: 0,
        updated_at_epoch_s: now,
    }];

    let cutover_res1 = LiveCutoverGuard::execute_cutover(
        &candidate,
        &mut coordinator,
        &cursor,
        &uncommitted_outbox,
        now,
        3600,
    );
    assert!(
        matches!(cutover_res1, Err(ref errs) if errs.iter().any(|e| matches!(e, ReleaseGateFailure::UncommittedInFlightWorkRemaining { count: 1 }))),
        "In-flight uncommitted ledger items must block live cutover"
    );

    // 2. Clean in-flight ledger (all committed) -> SUCCESS
    let clean_outbox = vec![OutboxRecord {
        effect_id: "eff-pending-01".to_string(),
        operation_key: "key-pending-01".to_string(),
        effect_type: "billing".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Confirmed,
        retry_count: 0,
        updated_at_epoch_s: now,
    }];

    let cutover_res2 = LiveCutoverGuard::execute_cutover(
        &candidate,
        &mut coordinator,
        &cursor,
        &clean_outbox,
        now,
        3600,
    );
    assert!(cutover_res2.is_ok(), "Cutover must succeed when all checks pass");
    let receipt = cutover_res2.unwrap();
    assert_eq!(receipt.active_writer, WriterRole::CanonicalAuthoritative);
    assert!(coordinator.is_legacy_sealed());
    assert!(receipt.receipt_signature.starts_with("SIG-LIVE-RELEASE:"));
}

#[test]
fn test_clean_machine_restoration_and_signed_handover_and_rollback() {
    let mut project = ClientDiscoveryProject::new_fixture("proj-clean-01", "Beta Global");
    project.apply_operator_correction(12);
    project.generate_proposal_artifact();
    project.sandbox_verify_zero_outbound_delivery();
    let cert = project.sign_handover("Krish Ujeniya", 1_000_100);

    // Run clean machine drill
    let report = CleanMachineVerifier::run_clean_machine_drill(&cert);

    assert!(report.is_clean_environment);
    assert!(report.handover_certificate_verified, "Signed handover must verify on clean machine");
    assert!(report.rollback_rehearsal_succeeded, "Rollback rehearsal must succeed on clean machine");
    assert!(report.zero_unauthorized_external_state);
}
