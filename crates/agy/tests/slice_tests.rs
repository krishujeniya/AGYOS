//! First Internal Slice Verification and Interruption Recovery Tests.
//! Principles: P01, P04, P05, P06, P09, P10, P23, P24, P30, P31
//!
//! Acceptance Targets:
//! - Proposal totals <= 12 hours over two weeks.
//! - Cites corrected constraint.
//! - Survives restart/interruption and resumes at same decision via Ariadne breadcrumb.
//! - Produces zero outbound deliveries (complete mediation).
//! - False evidence fails Review; failed Test cannot enter Ship.
//! - Novice operator can explain what happened from receipt.

use agy::{
    OnboardingProposalSession, SliceError,
};
use domain::{Gate, TaskId, WorkspaceId};
use store::TransactionalStore;

#[test]
fn test_slice_nominal_and_interruption_recovery() {
    let temp_dir = std::env::temp_dir().join(format!("agy_slice_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_slice_client");
    let task_id = TaskId::new("task_onboarding_001");

    // Phase 1: In initial session, operator describes need with 20h cap, then corrects to 12h
    {
        let mut store = TransactionalStore::open(&temp_dir, ws_id.clone())
            .expect("Store open should succeed");

        let mut session = OnboardingProposalSession::initialize(&mut store, ws_id.clone(), task_id.clone())
            .expect("Session init should succeed");

        // Operator applies natural-language correction: change cap to 12h
        session.apply_operator_correction(&mut store, 12)
            .expect("Correction to 12h should succeed");

        // Independent review of evidence on corrected proposal
        session.review_evidence(&mut store, true).expect("Review should pass with valid evidence");

        // Process dropped here simulating unexpected crash / operator closing AGY CLI!
    }

    // Phase 2: Fresh process start — resume session from Ariadne breadcrumb
    {
        let mut store = TransactionalStore::open(&temp_dir, ws_id.clone())
            .expect("Store reopen should succeed");

        // Retrieve breadcrumb from durable store
        let crumb = OnboardingProposalSession::resume_from_store(&store, &ws_id, &task_id)
            .expect("Ariadne breadcrumb recovery should succeed");

        assert_eq!(crumb.task_id, task_id);
        assert_eq!(crumb.active_hours_cap, 12, "Corrected constraint must survive interruption");
        assert_eq!(crumb.last_confirmed_gate, Gate::Plan);
        assert_eq!(crumb.pending_gate, Gate::Implement);
        assert!(crumb.review_passed, "Review verdict on corrected proposal preserved");

        // Resume active session and proceed to Ship
        let mut session = OnboardingProposalSession::initialize(&mut store, ws_id.clone(), task_id.clone())
            .expect("Session re-init");
        session.apply_operator_correction(&mut store, crumb.active_hours_cap)
            .expect("Apply recovered cap");
        session.review_evidence(&mut store, true)
            .expect("Review confirmed on active session");

        let receipt = session.finalize_ship(&mut store).expect("Ship should succeed");

        // Verify acceptance criteria
        assert_eq!(receipt.final_hours_cap, 12);
        assert_eq!(receipt.timeline_weeks, 2);
        assert_eq!(receipt.outbound_effects_count, 0, "Outbound deliveries must remain strictly 0");
        assert!(receipt.review_passed);
        assert!(receipt.human_explanation.contains("12-hour cap"));
    }

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_slice_false_evidence_fails_review_and_blocks_ship() {
    let temp_dir = std::env::temp_dir().join(format!("agy_false_ev_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_false_ev");
    let task_id = TaskId::new("task_false_002");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    let mut session = OnboardingProposalSession::initialize(&mut store, ws_id, task_id)
        .expect("Init");

    // Reviewer identifies falsified or unverified evidence
    let err = session.review_evidence(&mut store, false).expect_err("False evidence must fail Review");
    match err {
        SliceError::ReviewFailed(msg) => assert!(msg.contains("Falsified or unverified evidence")),
        other => panic!("Expected ReviewFailed, got {:?}", other),
    }

    // Attempting to ship after failed review must block
    session.apply_operator_correction(&mut store, 10).expect("Correction");
    let ship_err = session.finalize_ship(&mut store).expect_err("Failed review must block Ship");
    assert!(ship_err.to_string().contains("review verdict"));

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_slice_uncorrected_proposal_exceeding_12h_blocks_ship() {
    let temp_dir = std::env::temp_dir().join(format!("agy_uncorrected_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_uncorrected");
    let task_id = TaskId::new("task_20h_003");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    let mut session = OnboardingProposalSession::initialize(&mut store, ws_id, task_id)
        .expect("Init");

    // Proposal remains at 20h without correction -> Attempt to ship must fail
    let err = session.finalize_ship(&mut store).expect_err("Gate not implement should fail");
    assert!(err.to_string().contains("Gate progression blocked"));

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_slice_zero_outbound_egress_enforced() {
    let temp_dir = std::env::temp_dir().join(format!("agy_egress_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_egress");
    let task_id = TaskId::new("task_egress_004");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    let mut session = OnboardingProposalSession::initialize(&mut store, ws_id, task_id)
        .expect("Init");

    session.apply_operator_correction(&mut store, 10).expect("Correction");
    session.review_evidence(&mut store, true).expect("Review");
    let receipt = session.finalize_ship(&mut store).expect("Ship");

    assert_eq!(receipt.outbound_effects_count, 0);
    assert_eq!(store.outbox().len(), 0);

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_slice_stale_review_after_operator_correction_blocks_ship() {
    let temp_dir = std::env::temp_dir().join(format!("agy_stale_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_stale");
    let task_id = TaskId::new("task_stale_005");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    let mut session = OnboardingProposalSession::initialize(&mut store, ws_id, task_id)
        .expect("Init");

    // Review passes for initial 20h draft
    session.review_evidence(&mut store, true).expect("Review passes initially");

    // Operator applies correction modifying constraint to 10h
    session.apply_operator_correction(&mut store, 10).expect("Correction to 10h");

    // Attempting to finalize ship without re-reviewing the corrected proposal MUST fail as stale
    let err = session.finalize_ship(&mut store).expect_err("Stale review must block Ship");
    assert!(
        err.to_string().contains("stale"),
        "Error message must explicitly cite stale review verdict, got: {}",
        err
    );

    let _ = std::fs::remove_dir_all(&temp_dir);
}

#[test]
fn test_slice_missing_review_verdict_blocks_ship() {
    let temp_dir = std::env::temp_dir().join(format!("agy_missing_rev_{}", std::process::id()));
    let ws_id = WorkspaceId::new("ws_missing_rev");
    let task_id = TaskId::new("task_missing_006");

    let mut store = TransactionalStore::open(&temp_dir, ws_id.clone()).expect("Store open");
    let mut session = OnboardingProposalSession::initialize(&mut store, ws_id, task_id)
        .expect("Init");

    // Operator applies correction without any review ever happening
    session.apply_operator_correction(&mut store, 10).expect("Correction to 10h");

    let err = session.finalize_ship(&mut store).expect_err("Missing review must block Ship");
    assert!(
        err.to_string().contains("Missing stored review verdict"),
        "Error message must cite missing review verdict, got: {}",
        err
    );

    let _ = std::fs::remove_dir_all(&temp_dir);
}
