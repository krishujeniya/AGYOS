//! Integration Test Suite for Local Production Qualification (Step 15).
//!
//! Complies with Step 15 finish criteria:
//! - Local nominal and recovery gates pass.
//! - No live-provider throughput is inferred.
//! - An operator can recover with a clean installation and verified backup and locate every outstanding effect.
//! - Regional/standby tests apply to hosted only.
//!
//! Principles:
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics)
//! - P15 (Tail Latency Amplification Bounds)
//! - P16 (Admission Control & Degradation)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)

use domain::{ActorId, EventId, WorkspaceId};
use std::fs;
use std::path::PathBuf;
use store::{EventRecord, FenceToken, OutboxRecord, OutboxStatus, TransactionalStore};
use telemetry::{
    BackupManifest, IncidentSeverity, LocalBackupEngine, LocalFaultProfile, LocalLoadProfile,
    LocalOfflineProfile, MetricClass, OnCallRunbook, RedactedMetricsCollector,
};

fn create_temp_dir(prefix: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("agyos-test-{}-{}", prefix, std::process::id()));
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();
    dir
}

#[test]
fn test_local_nominal_load_profile_and_slo_targets() {
    let mut profile = LocalLoadProfile::new();

    // 100 seconds simulation of 20 ops/s = 2,000 operations
    profile.run_nominal_simulation(100);
    let collector = profile.collector();

    assert_eq!(collector.total_samples(), 2_000);
    assert_eq!(collector.count_by_class(MetricClass::Route), 1_600); // 80%
    assert_eq!(collector.count_by_class(MetricClass::Status), 300); // 15%
    assert_eq!(collector.count_by_class(MetricClass::DurableSubmit), 100); // 5%

    // Verify nominal latency SLO targets
    assert!(
        collector.warm_p99_ms(MetricClass::Route) <= 100,
        "Warm route p99 was {}ms, expected <= 100ms",
        collector.warm_p99_ms(MetricClass::Route)
    );
    assert!(
        collector.warm_p99_ms(MetricClass::Status) <= 100,
        "Warm status p99 was {}ms, expected <= 100ms",
        collector.warm_p99_ms(MetricClass::Status)
    );
    assert!(
        collector.warm_p99_ms(MetricClass::DurableSubmit) <= 250,
        "Durable submit p99 was {}ms, expected <= 250ms",
        collector.warm_p99_ms(MetricClass::DurableSubmit)
    );
    assert!(
        collector.cold_first_route_ms() <= 2000,
        "Cold route latency was {}ms, expected <= 2000ms",
        collector.cold_first_route_ms()
    );
    assert!(
        collector.steady_rss_mib() <= 256,
        "Steady RSS was {} MiB, expected <= 256 MiB",
        collector.steady_rss_mib()
    );

    assert!(collector.verify_local_nominal_slo().is_ok());
}

#[test]
fn test_redacted_metrics_zero_leakage() {
    let mut collector = RedactedMetricsCollector::new();

    let secret_tag = "tag:deploy-with-ghp_1234567890abcdef1234567890abcdef12 and AKIAIOSFODNN7EXAMPLE";
    let sensitive_payload = "sk-ant-api03-abcdef123456 Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 for user.confidential@enterprise-client.com";

    collector.record(
        MetricClass::Route,
        15,
        secret_tag,
        sensitive_payload,
        1_000_000,
    );

    let json_export = collector.export_redacted_json();
    let toon_export = collector.export_redacted_toon();

    // Verify zero plaintext secrets appear anywhere in exported telemetry
    assert!(!json_export.contains("ghp_1234567890abcdef"));
    assert!(!json_export.contains("AKIAIOSFODNN7EXAMPLE"));
    assert!(!json_export.contains("sk-ant-api03"));
    assert!(!json_export.contains("eyJhbGciOiJIUzI1Ni"));
    assert!(!json_export.contains("user.confidential@enterprise-client.com"));

    assert!(!toon_export.contains("ghp_1234567890abcdef"));
    assert!(!toon_export.contains("AKIAIOSFODNN7EXAMPLE"));
    assert!(!toon_export.contains("sk-ant-api03"));

    // Verify redacted markers and hashes are present
    assert!(json_export.contains("[REDACTED-TOKEN]"));
    assert!(json_export.contains("sha256:"));
}

#[test]
fn test_local_fault_profile_durability_and_split_brain_fence() {
    let temp_dir = create_temp_dir("fault-fence");
    let ws_id = WorkspaceId::new("ws-fault-test");

    let res = LocalFaultProfile::test_fence_split_brain(&temp_dir, &ws_id);
    assert!(res.is_ok(), "Fence split brain test failed: {:?}", res);

    let _ = fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_clean_install_and_backup_recovery_locates_outstanding_effects() {
    let source_dir = create_temp_dir("backup-src");
    let target_dir = create_temp_dir("backup-dst");
    let archive_path = source_dir.join("backup-archive.json");

    let ws_id = WorkspaceId::new("ws-production-local");
    let mut store = TransactionalStore::open(&source_dir, ws_id.clone()).unwrap();

    // 1. Commit 10 durable events and 4 outbox records (2 delivered, 2 pending)
    for i in 1..=10 {
        let event = EventRecord {
            event_id: EventId::new(format!("evt-{:03}", i)),
            workspace_id: ws_id.clone(),
            revision: i as u64,
            actor_id: ActorId::new("operator-admin"),
            event_type: "proposal_step_committed".to_string(),
            payload_json: format!("{{\"step\": {}}}", i),
            timestamp_epoch_s: 1_000_000 + i as u64,
        };

        let outbox = if i == 3 {
            Some(OutboxRecord {
                effect_id: "eff-01".to_string(),
                operation_key: "op-key-01".to_string(),
                tenant_id: ws_id.clone(),
                caller_id: ActorId::new("operator-admin"),
                recipient: "crm-account:acme".to_string(),
                deadline_epoch_s: 1_005_000,
                status: OutboxStatus::Delivered,
                attempt_count: 1,
                last_error: None,
            })
        } else if i == 7 {
            Some(OutboxRecord {
                effect_id: "eff-02-pending".to_string(),
                operation_key: "op-key-02-pending".to_string(),
                tenant_id: ws_id.clone(),
                caller_id: ActorId::new("operator-admin"),
                recipient: "ticket:inc-404".to_string(),
                deadline_epoch_s: 1_005_000,
                status: OutboxStatus::Pending, // Outstanding effect 1
                attempt_count: 0,
                last_error: None,
            })
        } else if i == 9 {
            Some(OutboxRecord {
                effect_id: "eff-03-pending".to_string(),
                operation_key: "op-key-03-pending".to_string(),
                tenant_id: ws_id.clone(),
                caller_id: ActorId::new("operator-admin"),
                recipient: "stripe:acct_99".to_string(),
                deadline_epoch_s: 1_005_000,
                status: OutboxStatus::Pending, // Outstanding effect 2
                attempt_count: 0,
                last_error: None,
            })
        } else {
            None
        };

        store.commit_transaction(FenceToken::new(1), event, outbox).unwrap();
    }

    assert_eq!(store.events().len(), 10);
    assert_eq!(store.outbox().len(), 3);

    // 2. Create verified signed backup
    let manifest = LocalBackupEngine::create_backup(
        &source_dir,
        &ws_id,
        &archive_path,
        1_000_100,
    ).expect("Backup creation must succeed");

    assert_eq!(manifest.events_count, 10);
    assert_eq!(manifest.pending_effects_count, 2);
    assert!(archive_path.exists());

    // 3. Simulate clean installation recovery: restore into empty target_dir
    let restored_manifest = LocalBackupEngine::restore_backup(
        &archive_path,
        &target_dir,
    ).expect("Backup restoration must succeed");

    assert_eq!(restored_manifest, manifest);

    // 4. Locate every outstanding effect in the restored outbox
    let outstanding = LocalBackupEngine::locate_outstanding_effects(&target_dir, &ws_id)
        .expect("Locate outstanding effects must succeed");

    assert_eq!(outstanding.len(), 2, "Expected exactly 2 outstanding pending effects");
    let effect_ids: Vec<String> = outstanding.iter().map(|e| e.effect_id.clone()).collect();
    assert!(effect_ids.contains(&"eff-02-pending".to_string()));
    assert!(effect_ids.contains(&"eff-03-pending".to_string()));

    // 5. Verify RPO = 0: all 10 historical events rehydrated
    let restored_store = TransactionalStore::open(&target_dir, ws_id.clone()).unwrap();
    assert_eq!(restored_store.events().len(), 10);

    let _ = fs::remove_dir_all(&source_dir);
    let _ = fs::remove_dir_all(&target_dir);
}

#[test]
fn test_local_offline_profile_zero_network_egress() {
    let offline_ok = LocalOfflineProfile::verify_offline_independence();
    assert_eq!(offline_ok, Ok(true));
}

#[test]
fn test_oncall_runbook_triage() {
    let sev1_plan = OnCallRunbook::triage_symptom("Detected store corruption and split-brain writer");
    assert_eq!(sev1_plan.severity, IncidentSeverity::Sev1Critical);
    assert!(sev1_plan.immediate_actions[0].contains("Pause incoming durable writes"));

    let sev2_plan = OnCallRunbook::triage_symptom("External model returned HTTP 503 circuit breaker tripped");
    assert_eq!(sev2_plan.severity, IncidentSeverity::Sev2Major);
    assert!(sev2_plan.immediate_actions[1].contains("local offline fallback"));

    let sev3_plan = OnCallRunbook::triage_symptom("Cold start latency exceeded 1500ms warning");
    assert_eq!(sev3_plan.severity, IncidentSeverity::Sev3Minor);
    assert!(sev3_plan.verification_command.contains("bin/agyos compact"));
}
