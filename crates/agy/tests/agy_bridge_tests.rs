//! AGY CLI Integration and Verification Tests.
//! Principles: P04, P05, P09, P11, P13, P29
//!
//! Acceptance Targets:
//! - An authenticated natural-language request finds the fixture skill, reads the correct item and returns a receipt.
//! - A denied harmless read records blocked even if the CLI exits zero.
//! - Unsupported AGY version is rejected.
//! - Omitted hooks prevent privileged effect dispatch.
//! - Unbrokered commands cannot exercise privileged effects.
//! - Flat collision detection on skill slugs.

use agy::{
    AgyBridge, ConfinementError, ConfinementGuard, ProjectionEngine,
};
use domain::{GateState, RiskLevel, TaskId, WorkspaceId};
use governance::GatePolicy;
use store::TransactionalStore;

#[test]
fn test_deterministic_one_skill_lookup_and_receipt() {
    let temp_dir = std::env::temp_dir().join(format!("agy_lookup_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_lookup");
    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");

    let guard = ConfinementGuard::new(true, true, RiskLevel::R3);
    let policy = GatePolicy::default();
    let task_id = TaskId::new("task_01");

    // Authenticated natural language request for fixture skill
    let receipt = AgyBridge::execute_skill_request(
        &mut store,
        "1.5.13",
        &guard,
        &policy,
        task_id.clone(),
        "operator/capture-goal",
        true, // actor permitted
        0,    // CLI exit code 0
    ).expect("Execute skill request should succeed");

    assert_eq!(receipt.gate_state, GateState::Confirmed);
    assert_eq!(receipt.skill_id, "operator/capture-goal");
    assert_eq!(receipt.task_id, task_id);
    assert_eq!(receipt.exit_code, 0);
    assert!(receipt.reason.contains("Authorized R0"));

    // Verify receipt was committed to store events
    assert_eq!(store.events().len(), 1);
    assert_eq!(store.events()[0].event_type, "EXECUTION_RECEIPT_ISSUED");

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_denied_harmless_read_records_blocked_receipt_even_if_exit_zero() {
    let temp_dir = std::env::temp_dir().join(format!("agy_denied_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_denied");
    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");

    let guard = ConfinementGuard::new(true, true, RiskLevel::R3);
    let policy = GatePolicy::default();
    let task_id = TaskId::new("task_denied");

    // Host CLI simulator returned 0, but actor is unpermitted
    let receipt = AgyBridge::execute_skill_request(
        &mut store,
        "1.5.13",
        &guard,
        &policy,
        task_id.clone(),
        "operator/capture-goal",
        false, // actor is NOT permitted!
        0,     // CLI exits zero!
    ).expect("Bridge should generate audit receipt");

    // Must record Blocked despite CLI exit 0!
    assert_eq!(receipt.gate_state, GateState::Blocked);
    assert_eq!(receipt.exit_code, 0);
    assert!(receipt.reason.contains("Policy violation"));

    // Durable store event proves it was blocked
    assert_eq!(store.events().len(), 1);
    assert!(store.events()[0].payload_json.contains("Blocked"));

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_unsupported_agy_version_rejected() {
    let temp_dir = std::env::temp_dir().join(format!("agy_ver_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_ver");
    let mut store = TransactionalStore::open(&temp_dir, ws_id).expect("Store open");

    let guard = ConfinementGuard::new(true, true, RiskLevel::R3);
    let policy = GatePolicy::default();
    let task_id = TaskId::new("task_ver");

    // Version 1.4.0 is below supported range (1.5.0+)
    let err = AgyBridge::execute_skill_request(
        &mut store,
        "1.4.0",
        &guard,
        &policy,
        task_id,
        "operator/capture-goal",
        true,
        0,
    ).expect_err("Unsupported version must fail");

    assert!(err.to_string().contains("Unsupported AGY CLI version"));

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_omitted_hooks_prevent_privileged_effect_dispatch() {
    // Hooks NOT installed
    let guard = ConfinementGuard::new(false, true, RiskLevel::R3);
    let err = guard.verify_command_execution("billing/charge", RiskLevel::R3)
        .expect_err("Missing hooks must be rejected");

    match err {
        ConfinementError::OmittedHooks(msg) => assert!(msg.contains("missing or inactive")),
        other => panic!("Expected OmittedHooks, got {:?}", other),
    }
}

#[test]
fn test_unbrokered_command_cannot_exercise_privileged_effects() {
    // Hooks installed, but broker token NOT active (unbrokered shell)
    let guard = ConfinementGuard::new(true, false, RiskLevel::R3);

    // 1. Privileged R2/R3 command denied
    let err = guard.verify_command_execution("billing/charge", RiskLevel::R3)
        .expect_err("Unbrokered command must be denied");

    match err {
        ConfinementError::UnbrokeredCommandDenied(cmd) => assert_eq!(cmd, "billing/charge"),
        other => panic!("Expected UnbrokeredCommandDenied, got {:?}", other),
    }

    // 2. Private vault access denied to unbrokered shell
    let vault_err = guard.verify_vault_isolation("STRIPE_SECRET_KEY")
        .expect_err("Vault access from unbrokered shell must be denied");

    match vault_err {
        ConfinementError::PrivateVaultAccessViolation(key) => assert_eq!(key, "STRIPE_SECRET_KEY"),
        other => panic!("Expected PrivateVaultAccessViolation, got {:?}", other),
    }
}

#[test]
fn test_projection_flat_slug_collision_detection() {
    let mut engine = ProjectionEngine::new();

    let toon1 = "id: \"capture-goal\"\nintent: \"First intent\"\n";
    let (slug1, _) = engine.project_skill_markdown(toon1).expect("First project");
    assert_eq!(slug1, "capture-goal");

    // Second skill with identical slug -> MUST COLLIDE
    let toon2 = "id: \"capture-goal\"\nintent: \"Second intent\"\n";
    let err = engine.project_skill_markdown(toon2)
        .expect_err("Duplicate slug must trigger collision");

    assert!(err.to_string().contains("Flat slug collision detected"));
}

#[test]
fn test_project_hooks_and_mcp_json() {
    let engine = ProjectionEngine::new();

    let hooks_toon = "hooks:\n  - name: \"pre-command\"\n    type: \"PreToolUse\"\n";
    let hooks_json = engine.project_hooks_json(hooks_toon).expect("Project hooks");
    assert!(hooks_json.contains("pre-command"));
    assert!(hooks_json.contains("PreToolUse"));

    let mcp_toon = "servers:\n  - name: \"agyos-kernel\"\n";
    let mcp_json = engine.project_mcp_json(mcp_toon).expect("Project mcp");
    assert!(mcp_json.contains("agyos-kernel"));
    assert!(mcp_json.contains("AGYOS_CONFINED"));
}
