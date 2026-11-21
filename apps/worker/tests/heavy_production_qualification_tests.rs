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
    let in_price = FixedMoney::from_micros(150_000); // $0.15 per million ($0.00000015/tok)
    let out_price = FixedMoney::from_micros(600_000); // $0.60 per million ($0.00000060/tok)

    let mut controller = SpendingLimitController::new(max_spend, in_price, out_price);

    // Hourly cost formula check: 540 * in + 108 * out
    let hourly = controller.calculate_hourly_cost_at_50_jobs_per_sec();
    assert_eq!(
        hourly,
        FixedMoney::from_micros(540 * 150_000 + 108 * 600_000)
    );

    // Normal reservation: 1,500 input + 300 output tokens must equal exactly 405 microdollars
    let cost = controller
        .reserve_call(1_500, 300)
        .expect("1500 in + 300 out call reservation must succeed");
    assert_eq!(
        cost,
        FixedMoney::from_micros(405),
        "1,500 in ($0.15/M) + 300 out ($0.60/M) must equal exactly 405 microdollars"
    );

    // Exceed spending limit
    let mut small_controller =
        SpendingLimitController::new(FixedMoney::from_micros(10), in_price, out_price);
    let err_budget = small_controller.reserve_call(100_000, 50_000);
    assert!(err_budget.is_err());
    assert!(err_budget.unwrap_err().contains("Spending limit reached"));
}

#[test]
fn test_worker_leases_double_lease_rejection_and_fence_validated_release() {
    let mut lease_mgr = WorkerPoolLeaseManager::new();

    // 1. Initial lease acquisition succeeds
    let lease = lease_mgr
        .acquire_lease("task-unique-01", 1_000_000)
        .expect("Initial lease acquisition must succeed");
    assert_eq!(lease_mgr.active_lease_count(), 1);

    // 2. Double lease for the same task fails cleanly
    let err_double = lease_mgr.acquire_lease("task-unique-01", 1_000_001);
    assert!(err_double.is_err(), "Double lease for same task must fail cleanly");
    assert_eq!(lease_mgr.active_lease_count(), 1, "Slot count must not leak on double lease");

    // 3. Release with wrong fence token is rejected
    let wrong_fence = FenceToken::new(999);
    let err_wrong_fence = lease_mgr.release_lease_with_fence("task-unique-01", wrong_fence);
    assert!(err_wrong_fence.is_err(), "Release with wrong fence must fail");
    assert_eq!(lease_mgr.active_lease_count(), 1, "Lease must remain active after failed release");

    // 4. Release with correct fence token succeeds
    let ok_release = lease_mgr
        .release_lease_with_fence("task-unique-01", lease.fence_token)
        .expect("Release with matching fence must succeed");
    assert!(ok_release);
    assert_eq!(lease_mgr.active_lease_count(), 0);
}

#[test]
fn test_fair_queue_round_robin_dispatch_without_starvation() {
    let mut admission = QueueAdmissionController::new();
    let ws_a = WorkspaceId::new("ws-tenant-alpha");
    let ws_b = WorkspaceId::new("ws-tenant-beta");
    let ws_c = WorkspaceId::new("ws-tenant-gamma");

    // Submit 2 jobs from tenant A, 2 from B, 2 from C
    for i in 0..2 {
        admission.submit_job(
            QueuedJob {
                job_id: format!("job-a-{}", i),
                workspace_id: ws_a.clone(),
                traffic_class: HostedTrafficClass::DurableJob,
                payload_bytes: 100,
                enqueued_epoch_s: 1_000_000,
            },
            1_000_000,
        );
        admission.submit_job(
            QueuedJob {
                job_id: format!("job-b-{}", i),
                workspace_id: ws_b.clone(),
                traffic_class: HostedTrafficClass::DurableJob,
                payload_bytes: 100,
                enqueued_epoch_s: 1_000_000,
            },
            1_000_000,
        );
        admission.submit_job(
            QueuedJob {
                job_id: format!("job-c-{}", i),
                workspace_id: ws_c.clone(),
                traffic_class: HostedTrafficClass::DurableJob,
                payload_bytes: 100,
                enqueued_epoch_s: 1_000_000,
            },
            1_000_000,
        );
    }

    assert_eq!(admission.total_entries(), 6);

    // Round-robin dispatch order must interleave across tenants: A, B, C, A, B, C
    let j1 = admission.dispatch_next().expect("Dispatch 1");
    let j2 = admission.dispatch_next().expect("Dispatch 2");
    let j3 = admission.dispatch_next().expect("Dispatch 3");
    let j4 = admission.dispatch_next().expect("Dispatch 4");
    let j5 = admission.dispatch_next().expect("Dispatch 5");
    let j6 = admission.dispatch_next().expect("Dispatch 6");

    assert_eq!(j1.workspace_id, ws_a);
    assert_eq!(j2.workspace_id, ws_b);
    assert_eq!(j3.workspace_id, ws_c);
    assert_eq!(j4.workspace_id, ws_a);
    assert_eq!(j5.workspace_id, ws_b);
    assert_eq!(j6.workspace_id, ws_c);
    assert_eq!(admission.total_entries(), 0);
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
    assert!(!envelope.nonce_hex.is_empty());
    assert!(envelope.payload_digest.starts_with("sha256:"));
    assert!(!EncryptedBackupEngine::is_legacy(&envelope));

    // 2. Decrypt backup
    let decrypted = EncryptedBackupEngine::decrypt_backup(&envelope, secret_k1)
        .expect("Decryption must succeed with valid key");
    assert_eq!(decrypted, plaintext);

    // 3. Decrypt with wrong key fails
    let err_decrypt = EncryptedBackupEngine::decrypt_backup(&envelope, "wrong-key-32-bytes-invalid-here");
    assert!(err_decrypt.is_err());

    // 4. Tampered ciphertext fails authentication tag verification
    let mut tampered_ct = envelope.clone();
    tampered_ct.ciphertext_hex = format!("ff{}", &tampered_ct.ciphertext_hex[2..]);
    let err_tamper_ct = EncryptedBackupEngine::decrypt_backup(&tampered_ct, secret_k1);
    assert!(err_tamper_ct.is_err());
    assert!(err_tamper_ct.unwrap_err().contains("authentication tag verification failed"));

    // 5. Tampered metadata fails authentication tag verification
    let mut tampered_version = envelope.clone();
    tampered_version.key_version = 99;
    assert!(EncryptedBackupEngine::decrypt_backup(&tampered_version, secret_k1).is_err());

    let mut tampered_ts = envelope.clone();
    tampered_ts.timestamp_epoch_s = 2_000_000;
    assert!(EncryptedBackupEngine::decrypt_backup(&tampered_ts, secret_k1).is_err());

    let mut tampered_digest = envelope.clone();
    tampered_digest.payload_digest = "sha256:0000000000000000000000000000000000000000000000000000000000000000".to_string();
    assert!(EncryptedBackupEngine::decrypt_backup(&tampered_digest, secret_k1).is_err());

    // 6. Key rotation to key version 2
    let rotated = EncryptedBackupEngine::rotate_key(&envelope, secret_k1, 2, secret_k2)
        .expect("Key rotation must succeed");
    assert_eq!(rotated.key_version, 2);

    let decrypted_v2 = EncryptedBackupEngine::decrypt_backup(&rotated, secret_k2)
        .expect("Decryption must succeed with rotated key v2");
    assert_eq!(decrypted_v2, plaintext);
}

#[test]
fn test_legacy_backup_envelope_detection_and_migration() {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};

    let plaintext = "{\"legacy_workspace\": \"ws-legacy-999\", \"records\": 42}";
    let legacy_secret = "legacy-secret-key-32-characters!";
    let new_secret = "modern-aes-key-v2-secret-32-chars";

    // Fabricate a legacy envelope without nonce_hex and using DefaultHasher
    let key_bytes = legacy_secret.as_bytes();
    let mut encrypted_bytes = Vec::new();
    for (i, b) in plaintext.bytes().enumerate() {
        encrypted_bytes.push(b ^ key_bytes[i % key_bytes.len()]);
    }
    let ciphertext_hex = encrypted_bytes.iter().map(|b| format!("{:02x}", b)).collect::<String>();

    let mut tag_hasher = DefaultHasher::new();
    ciphertext_hex.hash(&mut tag_hasher);
    (1u32).hash(&mut tag_hasher);
    legacy_secret.hash(&mut tag_hasher);
    let auth_tag_hex = format!("{:016x}", tag_hasher.finish());

    let legacy_envelope = worker::EncryptedBackupEnvelope {
        key_version: 1,
        ciphertext_hex,
        auth_tag_hex,
        payload_digest: "sha256:legacy_fake_hash".to_string(),
        timestamp_epoch_s: 1_600_000_000,
        nonce_hex: String::new(),
    };

    assert!(EncryptedBackupEngine::is_legacy(&legacy_envelope));

    // Migrate legacy envelope to modern authenticated envelope
    let migrated = EncryptedBackupEngine::migrate_legacy(
        &legacy_envelope,
        legacy_secret,
        2,
        new_secret,
        1_700_000_000,
    )
    .expect("Migration of legacy backup envelope must succeed");

    assert!(!EncryptedBackupEngine::is_legacy(&migrated));
    assert_eq!(migrated.key_version, 2);
    assert!(!migrated.nonce_hex.is_empty());
    assert!(migrated.payload_digest.starts_with("sha256:"));

    // Decrypt migrated envelope with new secret
    let decrypted = EncryptedBackupEngine::decrypt_backup(&migrated, new_secret)
        .expect("Decryption of migrated envelope must succeed");
    assert_eq!(decrypted, plaintext);
}
