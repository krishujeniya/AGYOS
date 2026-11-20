//! Effect Broker, Idempotency, and Crash Recovery Tests.
//! Principles: P05, P10, P11, P12

use domain::WorkspaceId;
use effects::{EffectBroker, MockFailureMode, MockFixtureProvider, SagaCoordinator};
use store::{
    EventRecord, FenceToken, OutboxRecord, OutboxStatus, TransactionalStore,
};

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
fn test_saga_compensation_on_cancelled_effect() {
    let temp_dir = std::env::temp_dir().join(format!("agyos_saga_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_saga_test");

    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");
    let mut provider = MockFixtureProvider::new(MockFailureMode::NormalSuccess);

    let event = EventRecord {
        revision: 1,
        timestamp_epoch_s: 1700000030,
        event_type: "STAGE_PROPOSAL".to_string(),
        payload_json: "{}".to_string(),
    };
    let outbox = OutboxRecord {
        effect_id: "eff_compensate".to_string(),
        operation_key: "op_comp".to_string(),
        effect_type: "PAYMENT".to_string(),
        payload_json: "{}".to_string(),
        status: OutboxStatus::Pending,
        retry_count: 0,
        updated_at_epoch_s: 1700000030,
    };

    store.commit_transaction(FenceToken::new(1), event, Some(outbox)).expect("Commit");
    EffectBroker::process_outbox(&mut store, &mut provider).expect("Process");

    assert_eq!(store.outbox()[0].status, OutboxStatus::Confirmed);

    // Operator cancels / rolls back -> trigger saga compensation
    let compensated = SagaCoordinator::compensate_effect(&mut store, &mut provider, "eff_compensate")
        .expect("Compensate should succeed");

    assert!(compensated);
    assert_eq!(store.outbox()[0].status, OutboxStatus::Compensated);
    assert_eq!(provider.compensate_count, 1);

    let _ = std::fs::remove_dir_all(&temp_dir);
}
