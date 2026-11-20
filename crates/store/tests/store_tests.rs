//! Embedded Transactional Store Persistence and Invariant Tests.
//! Principles: P09, P10, P11, P21

use domain::WorkspaceId;
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

        assert_eq!(store.workspace_id(), &ws_id);

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

#[test]
fn test_snapshot_and_wal_persistence() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_snap_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_snap_test");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    for i in 1..=5 {
        let ev = EventRecord {
            revision: i,
            timestamp_epoch_s: 1700000000 + i,
            event_type: format!("EVENT_{}", i),
            payload_json: "{}".to_string(),
        };
        store.commit_transaction(FenceToken::new(1), ev, None).expect("Commit");
    }

    assert_eq!(store.events().len(), 5);
    store.take_snapshot().expect("Snapshot should succeed");

    let reopened = TransactionalStore::open(&temp_dir, ws_id).expect("Reopen");
    assert_eq!(reopened.events().len(), 5);

    let _ = std::fs::remove_dir_all(&temp_dir);
}
