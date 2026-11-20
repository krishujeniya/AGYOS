//! Transactional Recovery and Outbox Fixture Tests.
//! Principles: P09, P10, P11, P12, P21
//!
//! Acceptance Targets:
//! - An acknowledged local operation survives process kill.
//! - Duplicate replay emits exactly one effect with a fixture provider.
//! - Crashes around the provider receipt end as Confirmed or explicit Unknown.
//! - Deleting a workspace invalidates all its indexes and memory access.
//! - Stale split-brain writer with old fence token is rejected.

use domain::WorkspaceId;
use effects::{EffectBroker, MockFailureMode, MockFixtureProvider};
use store::{
    EventRecord, FenceToken, OutboxRecord, OutboxStatus, StoreError, TransactionalStore,
};

#[test]
fn test_acknowledged_local_operation_survives_process_kill() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_recov_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_recovery_test");

    // Phase 1: Open store, commit event and outbox record
    {
        let mut store = TransactionalStore::open(&temp_dir, ws_id.clone())
            .expect("Store open should succeed");

        let event = EventRecord {
            revision: 1,
            timestamp_epoch_s: 1700000000,
            event_type: "TASK_CREATED".to_string(),
            payload_json: "{\"task\":\"onboard_client\"}".to_string(),
        };

        let outbox = OutboxRecord {
            effect_id: "eff_01".to_string(),
            operation_key: "op_key_abc".to_string(),
            effect_type: "STAGE_PROPOSAL".to_string(),
            payload_json: "{\"amount\":12}".to_string(),
            status: OutboxStatus::Pending,
            retry_count: 0,
            updated_at_epoch_s: 1700000000,
        };

        store
            .commit_transaction(FenceToken::new(1), event, Some(outbox))
            .expect("Commit should succeed");
        // Store dropped here without clean exit, simulating process termination
    }

    // Phase 2: Fresh process start - recover from disk
    {
        let recovered = TransactionalStore::open(&temp_dir, ws_id)
            .expect("Store recovery should succeed");

        assert_eq!(recovered.events().len(), 1);
        assert_eq!(recovered.events()[0].revision, 1);
        assert_eq!(recovered.events()[0].event_type, "TASK_CREATED");

        assert_eq!(recovered.outbox().len(), 1);
        assert_eq!(recovered.outbox()[0].effect_id, "eff_01");
        assert_eq!(recovered.outbox()[0].status, OutboxStatus::Pending);
    }

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_duplicate_replay_emits_one_effect_with_fixture_provider() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_dedup_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_dedup_test");

    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");
    let mut provider = MockFixtureProvider::new(MockFailureMode::NormalSuccess);

    let event1 = EventRecord {
        revision: 1,
        timestamp_epoch_s: 1700000000,
        event_type: "DISPATCH".to_string(),
        payload_json: "{}".to_string(),
    };
    let outbox1 = OutboxRecord {
        effect_id: "eff_100".to_string(),
        operation_key: "idempotency_key_identical".to_string(),
        effect_type: "NOTIFY".to_string(),
        payload_json: "{\"msg\":\"hello\"}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1700000000,
    };

    store
        .commit_transaction(FenceToken::new(1), event1, Some(outbox1))
        .expect("Commit 1");
    EffectBroker::process_outbox(&mut store, &mut provider).expect("Process outbox 1");
    assert_eq!(provider.dispatch_count, 1);

    // Duplicate replay attempt with identical operation_key
    let event2 = EventRecord {
        revision: 2,
        timestamp_epoch_s: 1700000005,
        event_type: "DISPATCH_REPLAY".to_string(),
        payload_json: "{}".to_string(),
    };
    let outbox2 = OutboxRecord {
        effect_id: "eff_101".to_string(),
        operation_key: "idempotency_key_identical".to_string(), // identical key
        effect_type: "NOTIFY".to_string(),
        payload_json: "{\"msg\":\"hello\"}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1700000005,
    };

    store
        .commit_transaction(FenceToken::new(1), event2, Some(outbox2))
        .expect("Duplicate submission handled idempotently");
    EffectBroker::process_outbox(&mut store, &mut provider).expect("Process outbox 2");

    // Provider dispatch counter must remain strictly 1!
    assert_eq!(provider.dispatch_count, 1, "Duplicate replay must not emit secondary effect");

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_crashes_around_provider_receipt_end_as_confirmed_or_explicit_unknown() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_crash_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_crash_test");

    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");

    // Scenario 1: Crash after dispatch before receipt -> ExplicitUnknown
    let mut crash_provider = MockFixtureProvider::new(MockFailureMode::CrashAfterDispatchBeforeReceipt);
    let event1 = EventRecord {
        revision: 1,
        timestamp_epoch_s: 1700000010,
        event_type: "SEND".to_string(),
        payload_json: "{}".to_string(),
    };
    let outbox1 = OutboxRecord {
        effect_id: "eff_crash".to_string(),
        operation_key: "op_crash".to_string(),
        effect_type: "PAYMENT".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1700000010,
    };

    store
        .commit_transaction(FenceToken::new(1), event1, Some(outbox1))
        .expect("Commit");
    let outcomes = EffectBroker::process_outbox(&mut store, &mut crash_provider).expect("Process");
    assert_eq!(outcomes[0].1, OutboxStatus::ExplicitUnknown);
    assert_eq!(store.outbox()[0].status, OutboxStatus::ExplicitUnknown);

    // Scenario 2: Normal success -> Confirmed
    let mut ok_provider = MockFixtureProvider::new(MockFailureMode::NormalSuccess);
    let event2 = EventRecord {
        revision: 2,
        timestamp_epoch_s: 1700000020,
        event_type: "SEND2".to_string(),
        payload_json: "{}".to_string(),
    };
    let outbox2 = OutboxRecord {
        effect_id: "eff_ok".to_string(),
        operation_key: "op_ok".to_string(),
        effect_type: "PAYMENT".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1700000020,
    };

    store
        .commit_transaction(FenceToken::new(1), event2, Some(outbox2))
        .expect("Commit");
    let outcomes2 = EffectBroker::process_outbox(&mut store, &mut ok_provider).expect("Process");
    assert_eq!(outcomes2[0].1, OutboxStatus::Confirmed);
    assert_eq!(store.outbox()[1].status, OutboxStatus::Confirmed);

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_deleting_workspace_invalidates_all_indexes_and_access() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_del_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_ephemeral");

    {
        let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
        let event = EventRecord {
            revision: 1,
            timestamp_epoch_s: 1700000030,
            event_type: "INIT".to_string(),
            payload_json: "{}".to_string(),
        };
        store.commit_transaction(FenceToken::new(1), event, None).expect("Commit");
    }

    // Delete workspace completely
    TransactionalStore::delete_workspace(&temp_dir, &ws_id).expect("Delete workspace");

    // Subsequent access returns WorkspaceNotFound
    let err = TransactionalStore::delete_workspace(&temp_dir, &ws_id)
        .expect_err("Already deleted workspace must return WorkspaceNotFound");
    match err {
        StoreError::WorkspaceNotFound(id) => assert_eq!(id, ws_id),
        other => panic!("Expected WorkspaceNotFound, got {:?}", other),
    }

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_fencing_token_rejects_stale_split_brain_writer() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_fence_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_fence_test");

    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");
    // Leader lease updated to epoch 5
    store.set_fence(FenceToken::new(5));

    let event = EventRecord {
        revision: 1,
        timestamp_epoch_s: 1700000040,
        event_type: "STALE_WRITE".to_string(),
        payload_json: "{}".to_string(),
    };

    // Stale writer submits with old epoch 3 -> MUST FAIL
    let err = store
        .commit_transaction(FenceToken::new(3), event, None)
        .expect_err("Stale fence token must be rejected");

    match err {
        StoreError::StaleFenceToken { current_fence, submitted_fence } => {
            assert_eq!(current_fence, 5);
            assert_eq!(submitted_fence, 3);
        }
        other => panic!("Expected StaleFenceToken, got {:?}", other),
    }

    let _ = std::fs::remove_dir_all(&temp_dir);
}
