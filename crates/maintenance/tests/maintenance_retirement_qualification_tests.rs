//! Integration Test Suite for Maintenance & Retirement Qualification (Step 19).
//!
//! Complies with Step 19 finish criteria:
//! - "After ≥14 days of qualified canary/production observation, zero unresolved migration discrepancies and documented reversal authority, retire old writes only for the qualified profile. Preserve the legacy snapshot and provider for any unmigrated profile."
//! - "Operator can export and restore without the original vendor."
//! - "Baseline metrics and open risks have owners and dates."
//!
//! Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P06 (Canonical Structured Formats & TOON Invariants)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Clean Room Reproducibility)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)

use maintenance::{
    CanaryObservation, CanaryRetirementEngine, MaintenanceRiskLedger, OpenRisk,
    VendorIndependentEngine,
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
        ..valid_canary
    };
    let err_dirty = CanaryRetirementEngine::evaluate_retirement(&dirty_canary, now);
    assert!(err_dirty.is_err());
    assert!(err_dirty.unwrap_err().contains("must be 0"));
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
