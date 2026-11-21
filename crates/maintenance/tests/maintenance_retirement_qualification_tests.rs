//! Integration Test Suite for Maintenance, Retirement, and 2027 Evidence Refresh (Steps 19 & 20).
//!
//! Complies with Step 19 & 20 finish criteria:
//! - "After ≥14 days of qualified canary/production observation, zero unresolved migration discrepancies and documented reversal authority, retire old writes only for the qualified profile. Preserve the legacy snapshot and provider for any unmigrated profile."
//! - "Operator can export and restore without the original vendor."
//! - "Baseline metrics and open risks have owners and dates."
//! - "At the first 2027 release review, examine new final standards, peer-reviewed results and provider docs scoped to this plan. Compare each proposal against frozen fixtures before changing policy. A dated research decision record lists source status, impacted principle/skill, result and adopt/defer/reject decision. If still in 2026 record this as future work; it does not block a qualified 2026 release."
//!
//! Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P04 (Behavioral Contracts & Compatibility)
//! - P06 (Canonical Structured Formats & TOON Invariants)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Clean Room Reproducibility)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)
//! - P20 (Bounded Autonomous Loops)
//! - P25 (Deliberation Councils)
//! - P26 (Howard 1966 EVPI)
//! - P27 (Empirical 4-Arm Benchmark)

use maintenance::{
    CanaryObservation, CanaryRetirementEngine, MaintenanceRiskLedger,
    OpenRisk, ResearchDecisionRecord, VendorIndependentEngine,
};
use store::{EventRecord, OutboxRecord, OutboxStatus};

#[test]
fn test_canary_observation_and_legacy_write_retirement() {
    let now = 2_000_000;
    let fourteen_days_s = 14 * 86_400;

    let valid_canary = CanaryObservation {
        profile_name: "local-production".to_string(),
        observation_start_epoch_s: now - fourteen_days_s,
        observation_end_epoch_s: now,
        total_operations_observed: 50_000,
        unresolved_migration_discrepancies: 0,
        documented_reversal_authority: "Krish Ujeniya, Operations Lead".to_string(),
        legacy_snapshot_sha: "009074d934289553a61763d70c50ee5160e60110".to_string(),
        legacy_provider_retained: true,
    };

    // 1. Valid retirement evaluation
    let receipt = CanaryRetirementEngine::evaluate_retirement(&valid_canary, now)
        .expect("Valid 14-day canary observation must qualify for legacy write retirement");

    assert!(receipt.legacy_writes_retired);
    assert!(receipt.legacy_snapshot_preserved);
    assert_eq!(receipt.preserved_legacy_sha, "009074d934289553a61763d70c50ee5160e60110");
    assert!(receipt.reversal_authority_verified);
    assert_eq!(receipt.observation_days, 14);

    // 2. Reject insufficient observation window (<14 days)
    let short_canary = CanaryObservation {
        observation_start_epoch_s: now - (10 * 86_400), // only 10 days
        ..valid_canary.clone()
    };
    let err_short = CanaryRetirementEngine::evaluate_retirement(&short_canary, now);
    assert!(err_short.is_err());
    assert!(err_short.unwrap_err().contains("requires >= 14 days"));

    // 3. Reject if unresolved discrepancies exist
    let dirty_canary = CanaryObservation {
        unresolved_migration_discrepancies: 2,
        ..valid_canary.clone()
    };
    let err_dirty = CanaryRetirementEngine::evaluate_retirement(&dirty_canary, now);
    assert!(err_dirty.is_err());
    assert!(err_dirty.unwrap_err().contains("must be 0"));

    // 4. Reject if legacy provider is not retained as fallback
    let no_fallback_canary = CanaryObservation {
        legacy_provider_retained: false,
        ..valid_canary.clone()
    };
    let err_no_fallback = CanaryRetirementEngine::evaluate_retirement(&no_fallback_canary, now);
    assert!(err_no_fallback.is_err());
    assert!(err_no_fallback.unwrap_err().contains("Legacy provider must be retained"));

    // 5. Reject if zero operations were observed
    let zero_ops_canary = CanaryObservation {
        total_operations_observed: 0,
        ..valid_canary
    };
    let err_zero_ops = CanaryRetirementEngine::evaluate_retirement(&zero_ops_canary, now);
    assert!(err_zero_ops.is_err());
    assert!(err_zero_ops.unwrap_err().contains("Zero operations observed"));
}

#[test]
fn test_vendor_independent_export_and_restore() {
    let ws_id = "ws-vendor-free-01";
    let now = 1_500_000;

    let events = vec![
        EventRecord {
            revision: 1,
            timestamp_epoch_s: now - 100,
            event_type: "proposal_drafted".to_string(),
            payload_json: "{\"cap_hours\": 12}".to_string(),
        },
        EventRecord {
            revision: 2,
            timestamp_epoch_s: now - 50,
            event_type: "handover_signed".to_string(),
            payload_json: "{\"status\": \"DELIVERED_VERIFIED\"}".to_string(),
        },
    ];

    let outbox = vec![
        OutboxRecord {
            effect_id: "eff-001".to_string(),
            operation_key: "idem-001".to_string(),
            effect_type: "billing".to_string(),
            payload_json: "{\"micros\": 500}".to_string(),
            status: OutboxStatus::Confirmed,
            retry_count: 0,
            updated_at_epoch_s: now - 50,
        },
    ];

    // 1. Export to portable TOON archive
    let archive = VendorIndependentEngine::export_archive(ws_id, &events, &outbox, now);
    assert_eq!(archive.workspace_id, ws_id);
    assert_eq!(archive.events_count, 2);
    assert_eq!(archive.outbox_count, 1);
    assert!(!archive.archive_sha256.is_empty());

    // 2. Restore completely without external vendor
    let restored = VendorIndependentEngine::restore_archive(&archive, now + 10)
        .expect("Vendor-independent restoration must succeed");

    assert_eq!(restored.workspace_id, ws_id);
    assert_eq!(restored.events, events);
    assert_eq!(restored.outbox, outbox);
    assert!(restored.is_verified);
}

#[test]
fn test_risk_register_and_baseline_metrics_have_owners_and_dates() {
    let ledger = MaintenanceRiskLedger::default_ledger();

    // 1. Validate that all default risks and baseline metrics have owners and dates
    assert!(ledger.validate_owners_and_dates().is_ok());
    assert!(!ledger.open_risks.is_empty());
    assert!(!ledger.baseline_metrics.is_empty());

    for risk in &ledger.open_risks {
        assert_eq!(risk.owner, "Krish Ujeniya");
        assert!(!risk.target_resolution_date.is_empty());
        assert!(!risk.mitigation_plan.is_empty());
    }

    for metric in &ledger.baseline_metrics {
        assert_eq!(metric.owner, "Krish Ujeniya");
        assert!(!metric.review_date.is_empty());
        assert_eq!(metric.status, "WITHIN_SLO");
    }

    // 2. Reject risk with missing owner
    let mut invalid_ledger = ledger.clone();
    invalid_ledger.open_risks.push(OpenRisk {
        risk_id: "RISK-INVALID".to_string(),
        title: "No Owner Risk".to_string(),
        owner: "".to_string(), // Missing owner!
        target_resolution_date: "2026-12-31".to_string(),
        severity: "SEV-3".to_string(),
        mitigation_plan: "None".to_string(),
    });
    assert!(invalid_ledger.validate_owners_and_dates().is_err());
}

#[test]
fn test_step_20_research_decision_record_2027_evidence_refresh() {
    let rdr = ResearchDecisionRecord::default_2027_record();

    // 1. Validate in 2026 context: must be future work and must NOT block 2026 release
    let receipt = rdr.validate(2026).expect("2026 RDR validation must succeed");
    assert_eq!(receipt.rdr_id, "RDR-2027-01");
    assert_eq!(receipt.total_sources_evaluated, 5);
    assert_eq!(receipt.adopted_count, 1); // NIST SSDF
    assert_eq!(receipt.deferred_count, 3); // MCP, EVPI dynamic, weighted council
    assert_eq!(receipt.rejected_count, 1); // Unbrokered GUI browser
    assert!(receipt.is_future_work);
    assert!(!receipt.blocks_2026_release);
    assert!(receipt.frozen_fixtures_verified);

    // 2. Verify all evaluated entries contain source status, principle, proposed change, and fixture comparison
    for entry in &rdr.entries {
        assert!(!entry.source_status.is_empty());
        assert!(!entry.impacted_principle.is_empty());
        assert!(!entry.proposed_change.is_empty());
        assert!(!entry.rationale.is_empty());
        assert!(entry.frozen_fixtures_compared);
    }

    // 3. Reject if 2026 execution incorrectly attempts to block 2026 release
    let mut blocking_rdr = rdr.clone();
    blocking_rdr.blocks_2026_release = true;
    let err_blocking = blocking_rdr.validate(2026);
    assert!(err_blocking.is_err());
    assert!(err_blocking.unwrap_err().contains("must not block a qualified 2026 release"));

    // 4. Reject if not marked as future work when executed in 2026
    let mut non_future_rdr = rdr.clone();
    non_future_rdr.is_future_work = false;
    let err_future = non_future_rdr.validate(2026);
    assert!(err_future.is_err());
    assert!(err_future.unwrap_err().contains("must be recorded as future work"));

    // 5. Reject entry without frozen fixture comparison
    let mut unverified_fixture_rdr = rdr.clone();
    unverified_fixture_rdr.entries[0].frozen_fixtures_compared = false;
    let err_fixture = unverified_fixture_rdr.validate(2026);
    assert!(err_fixture.is_err());
    assert!(err_fixture.unwrap_err().contains("must be compared against frozen fixtures"));
}
