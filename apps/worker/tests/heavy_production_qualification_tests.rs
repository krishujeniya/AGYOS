//! Integration Test Suite for Heavy Production Hosted Qualification (Step 16).
//!
//! Complies with Step 16 finish criteria:
//! - Attach hardware, quota and all results from nominal/burst/soak, hot-tenant, failure and regional restore tests.
//! - Record sustainable throughput and maximum authorized cost.
//! - A missing provider quota or failed test keeps that hosted profile unqualified.
//!
//! Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P15 (Tail Latency Amplification Bounds)
//! - P16 (Admission Control & Degradation)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)
//! - P32 (Operator-Owned Budgets)

use domain::{FixedMoney, WorkspaceId};
use store::FenceToken;
use worker::{
    AdmissionVerdict, EncryptedBackupEngine, HostedEnvelopeRunner, HostedTrafficClass,
    QueueAdmissionController, QueuedJob, SpendingLimitController, WorkerPoolLeaseManager,
};

#[test]
fn test_hosted_production_envelope_full_qualification() {
    let report = HostedEnvelopeRunner::run_qualification();

    assert_eq!(report.total_workspaces_tested, 100);
    assert_eq!(report.sustainable_throughput_ops_per_sec, 1_000);
    assert_eq!(report.maximum_authorized_spend, FixedMoney::from_dollars(500));

    // Verify nominal latency SLO targets (Hosted envelope)
    assert!(
        report.nominal_route_p99_ms <= 150,
        "Route p99 {}ms exceeds 150ms ceiling",
        report.nominal_route_p99_ms
    );
    assert!(
        report.nominal_status_p99_ms <= 150,
        "Status p99 {}ms exceeds 150ms ceiling",
        report.nominal_status_p99_ms
    );
    assert!(
        report.nominal_durable_ack_p99_ms <= 300,
        "Durable ack p99 {}ms exceeds 300ms ceiling",
        report.nominal_durable_ack_p99_ms
    );
    assert!(
        report.queue_wait_p95_ms <= 2_000,
        "Queue wait p95 {}ms exceeds 2000ms ceiling",
        report.queue_wait_p95_ms
    );
    assert!(
        report.mock_e2e_job_p95_ms <= 15_000,
        "Mock e2e job p95 {}ms exceeds 15000ms ceiling",
        report.mock_e2e_job_p95_ms
    );

    // Verify burst and soak targets
    assert!(
        report.protected_status_cancel_p99_at_2x_ms <= 1_000,
        "Protected status/cancel at 2x {}ms exceeds 1000ms ceiling",
        report.protected_status_cancel_p99_at_2x_ms
    );
    assert!(
        report.soak_final_hour_rss_ratio_percent <= 110,
        "Soak RSS ratio {}% exceeds 110% ceiling",
        report.soak_final_hour_rss_ratio_percent
    );

    // Verify regional disaster recovery bounds
    assert!(
        report.regional_rpo_min <= 15,
        "Regional RPO {} min exceeds 15 min ceiling",
        report.regional_rpo_min
    );
    assert!(
        report.regional_rto_min <= 60,
        "Regional RTO {} min exceeds 60 min ceiling",
        report.regional_rto_min
    );

    assert!(report.all_gates_passed, "All hosted production gates must pass");
}

#[test]
fn test_hot_tenant_isolation_and_fair_queue_dispatch() {
    let mut admission = QueueAdmissionController::new();
    let hot_ws = WorkspaceId::new("ws-tenant-bully");
    let normal_ws = WorkspaceId::new("ws-tenant-standard");

    // 1. Hot tenant attempts to flood queue with 50 jobs
    let mut hot_rejected = 0;
    for i in 0..50 {
        let job = QueuedJob {
            job_id: format!("bully-job-{:02}", i),
            workspace_id: hot_ws.clone(),
            traffic_class: HostedTrafficClass::DurableJob,
            payload_bytes: 1024,
            enqueued_epoch_s: 1_000_000,
        };
        if let AdmissionVerdict::RejectedTenantQuotaExceeded { .. } =
            admission.submit_job(job, 1_000_000)
        {
            hot_rejected += 1;
        }
    }
    assert!(
        hot_rejected > 0,
        "Hot tenant quota rejection must fire under contention"
    );

    // 2. Normal tenant is still admitted despite hot tenant contention
    let normal_job = QueuedJob {
        job_id: "normal-job-01".to_string(),
        workspace_id: normal_ws,
        traffic_class: HostedTrafficClass::DurableJob,
        payload_bytes: 1024,
        enqueued_epoch_s: 1_000_000,
    };
    let verdict = admission.submit_job(normal_job, 1_000_000);
    assert!(
        matches!(verdict, AdmissionVerdict::Admitted { .. }),
        "Normal tenant must be admitted despite hot tenant flood"
    );

    // 3. Protected status/cancel operations are guaranteed admission
    let cancel_job = QueuedJob {
        job_id: "cancel-job-01".to_string(),
        workspace_id: hot_ws,
        traffic_class: HostedTrafficClass::StatusOrCancel,
        payload_bytes: 256,
        enqueued_epoch_s: 1_000_000,
    };
    let cancel_verdict = admission.submit_job(cancel_job, 1_000_000);
    assert!(
        matches!(cancel_verdict, AdmissionVerdict::Admitted { .. }),
        "Protected status/cancel must be admitted via dedicated headroom"
    );
}

#[test]
fn test_worker_leases_and_stale_fence_split_brain_protection() {
    let mut lease_mgr = WorkerPoolLeaseManager::new();
    assert_eq!(lease_mgr.total_capacity(), 432);

    // 1. Acquire lease
    let lease = lease_mgr
        .acquire_lease("task-durable-01", 1_000_000)
        .expect("Lease acquisition must succeed");
    assert_eq!(lease.task_id, "task-durable-01");
    assert_eq!(lease.expires_epoch_s, 1_000_015);
    let original_fence = lease.fence_token;

    // 2. Valid heartbeat renewal
    let renewed = lease_mgr
        .renew_heartbeat("task-durable-01", original_fence, 1_000_010)
        .expect("Valid heartbeat renewal must succeed");
    assert_eq!(renewed.expires_epoch_s, 1_000_025);

    // 3. Stale fence renewal rejection
    let stale_fence = FenceToken::new(original_fence.epoch().saturating_sub(1));
    let err_stale = lease_mgr.renew_heartbeat("task-durable-01", stale_fence, 1_000_020);
    assert!(err_stale.is_err(), "Stale fence must be rejected");

    // 4. Lease expiration and safe reclamation
    // Fast forward past expiration epoch 1_000_025
    let reclaimed = lease_mgr.reclaim_expired_leases(1_000_030);
    assert_eq!(reclaimed, vec!["task-durable-01"]);
    assert_eq!(lease_mgr.active_lease_count(), 0);
}

#[test]
fn test_spending_limit_controller_and_rate_limits() {
    let max_spend = FixedMoney::from_dollars(10);
    let in_price = FixedMoney::from_micros(200); // $0.20 per million
    let out_price = FixedMoney::from_micros(800); // $0.80 per million

    let mut controller = SpendingLimitController::new(max_spend, in_price, out_price);

    // Hourly cost formula check: 540 * in + 108 * out
    let hourly = controller.calculate_hourly_cost_at_50_jobs_per_sec();
    assert_eq!(
        hourly,
        FixedMoney::from_micros(540 * 200 + 108 * 800)
    );

    // Normal reservation
    let res = controller.reserve_call(10_000, 2_000);
    assert!(res.is_ok());

    // Exceed spending limit
    let mut big_controller =
        SpendingLimitController::new(FixedMoney::from_micros(10), in_price, out_price);
    let err_budget = big_controller.reserve_call(1_000_000, 500_000);
    assert!(err_budget.is_err());
    assert!(err_budget.unwrap_err().contains("Spending limit reached"));
}

#[test]
fn test_encrypted_backup_and_key_rotation() {
    let plaintext = "{\"workspace\": \"tenant-100\", \"snapshot\": \"verified_state_wal_log\"}";
    let secret_k1 = "agyos-aes-key-v1-secret-32-chars!";
    let secret_k2 = "agyos-aes-key-v2-secret-32-chars!";

    // 1. Encrypt backup
    let envelope = EncryptedBackupEngine::encrypt_backup(plaintext, 1, secret_k1, 1_000_000);
    assert_eq!(envelope.key_version, 1);
    assert!(!envelope.ciphertext_hex.is_empty());

    // 2. Decrypt backup
    let decrypted = EncryptedBackupEngine::decrypt_backup(&envelope, secret_k1)
        .expect("Decryption must succeed with valid key");
    assert_eq!(decrypted, plaintext);

    // 3. Decrypt with wrong key fails
    let err_decrypt = EncryptedBackupEngine::decrypt_backup(&envelope, "wrong-key-32-bytes-invalid-here");
    assert!(err_decrypt.is_err());

    // 4. Key rotation to key version 2
    let rotated = EncryptedBackupEngine::rotate_key(&envelope, secret_k1, 2, secret_k2)
        .expect("Key rotation must succeed");
    assert_eq!(rotated.key_version, 2);

    let decrypted_v2 = EncryptedBackupEngine::decrypt_backup(&rotated, secret_k2)
        .expect("Decryption must succeed with rotated key v2");
    assert_eq!(decrypted_v2, plaintext);
}
