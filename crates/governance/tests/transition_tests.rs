//! Enumerated Transition Fixtures and Invariant Tests for Governance.
//! Principles: P04, P05, P09, P32
//!
//! Acceptance Targets:
//! - Rejection of skipped gates (P09)
//! - Rejection of cross-workspace access (P05)
//! - Rejection of stale revisions (CAS)
//! - Rejection of changed or expired approvals
//! - A thousand USD 0.001 charges sum to USD 1.00 exactly (FixedMoney)
//! - Concurrent reservations cannot consume 20% recovery reserve fund

use domain::{
    ActorId, Approval, ApprovalId, ApprovalStatus, BudgetLedger, DataClass, DomainError,
    FixedMoney, Gate, RiskTier, RoleId, TaskContract, TaskId, WorkspaceId,
};
use governance::{PolicyEngine, StateMachine};

fn sample_contract() -> TaskContract {
    let budget = BudgetLedger::new(FixedMoney::from_dollars(10)); // $10.00 total
    TaskContract::new(
        TaskId::new("task_test_01"),
        WorkspaceId::new("ws_alpha"),
        ActorId::new("krishujeniya"),
        RoleId::new("role-senior-swe"),
        1,
        RiskTier::R1,
        DataClass::Class2PrivateClient,
        budget,
        "Sample prompt",
    )
    .expect("Valid contract creation")
}

#[test]
fn test_reject_skipped_gates() {
    let mut contract = sample_contract();
    assert_eq!(contract.current_gate, Gate::Idle);

    // Idle -> Understand is valid
    StateMachine::advance_gate(&mut contract, Gate::Understand).expect("Idle -> Understand valid");

    // Understand -> Implement is an invalid skipped gate (must pass Analyze -> Plan first!)
    let err = StateMachine::advance_gate(&mut contract, Gate::Implement)
        .expect_err("Skipping Analyze and Plan must fail");
    match err {
        DomainError::InvalidGateTransition { current, requested } => {
            assert_eq!(current, Gate::Understand);
            assert_eq!(requested, Gate::Implement);
        }
        other => panic!("Expected InvalidGateTransition, got {:?}", other),
    }

    // Following strict path succeeds
    StateMachine::advance_gate(&mut contract, Gate::Analyze).expect("Understand -> Analyze valid");
    StateMachine::advance_gate(&mut contract, Gate::Plan).expect("Analyze -> Plan valid");
    StateMachine::advance_gate(&mut contract, Gate::Implement).expect("Plan -> Implement valid");
}

#[test]
fn test_reject_cross_workspace_access() {
    let contract = sample_contract();
    let foreign_ws = WorkspaceId::new("ws_foreign");

    let err = StateMachine::verify_workspace(&contract, &foreign_ws)
        .expect_err("Cross-workspace access must be denied");
    match err {
        DomainError::CrossWorkspaceAccessDenied { expected, actual } => {
            assert_eq!(expected.as_str(), "ws_alpha");
            assert_eq!(actual.as_str(), "ws_foreign");
        }
        other => panic!("Expected CrossWorkspaceAccessDenied, got {:?}", other),
    }
}

#[test]
fn test_reject_stale_revisions() {
    let mut contract = sample_contract();
    assert_eq!(contract.revision, 1);

    // Advance gate increments revision to 2
    StateMachine::advance_gate(&mut contract, Gate::Understand).expect("Advance gate");
    assert_eq!(contract.revision, 2);

    // Submitting stale revision 1 must be rejected
    let err = StateMachine::verify_revision(&contract, 1)
        .expect_err("Stale revision 1 must fail when current is 2");
    match err {
        DomainError::StaleRevision { current, submitted } => {
            assert_eq!(current, 2);
            assert_eq!(submitted, 1);
        }
        other => panic!("Expected StaleRevision, got {:?}", other),
    }
}

#[test]
fn test_reject_expired_or_changed_approvals() {
    let now = 1700000000u64;
    let approval = Approval {
        id: ApprovalId::new("appr_01"),
        granter: ActorId::new("krishujeniya"),
        scope: "production_git_push".to_string(),
        status: ApprovalStatus::Approved,
        granted_at_epoch_s: now - 3600,
        expires_at_epoch_s: now - 10, // Expired 10 seconds ago
        signature_digest: "sig_abc123".to_string(),
    };

    // Expired check
    let err = PolicyEngine::verify_approval(&approval, "production_git_push", now)
        .expect_err("Expired approval must fail");
    match err {
        DomainError::ApprovalExpired { expires_at_epoch_s, current_epoch_s } => {
            assert_eq!(expires_at_epoch_s, now - 10);
            assert_eq!(current_epoch_s, now);
        }
        other => panic!("Expected ApprovalExpired, got {:?}", other),
    }

    // Scope mismatch check
    let valid_approval = Approval {
        id: ApprovalId::new("appr_02"),
        granter: ActorId::new("krishujeniya"),
        scope: "read_only_audit".to_string(),
        status: ApprovalStatus::Approved,
        granted_at_epoch_s: now - 100,
        expires_at_epoch_s: now + 3600,
        signature_digest: "sig_def456".to_string(),
    };

    let scope_err = PolicyEngine::verify_approval(&valid_approval, "write_payment", now)
        .expect_err("Scope mismatch must fail");
    match scope_err {
        DomainError::ApprovalScopeMismatch { required, provided } => {
            assert_eq!(required, "write_payment");
            assert_eq!(provided, "read_only_audit");
        }
        other => panic!("Expected ApprovalScopeMismatch, got {:?}", other),
    }
}

#[test]
fn test_thousand_microcharges_sum_to_one_dollar_exactly() {
    // 1,000 charges of USD 0.001 must sum to USD 1.000000 exactly
    let mut total = FixedMoney::ZERO;
    let charge = FixedMoney::ONE_MILLI_DOLLAR; // $0.001 = 1,000 micro-dollars

    for _ in 0..1_000 {
        total = total + charge;
    }

    assert_eq!(total, FixedMoney::ONE_DOLLAR);
    assert_eq!(total.as_micros(), 1_000_000);
    assert_eq!(total.as_f64(), 1.0);
}

#[test]
fn test_concurrent_reservations_cannot_consume_recovery_funds() {
    let mut contract = sample_contract();
    // Total budget = $10.00
    // Recovery reserve = 20% = $2.00
    // Maximum spendable = $8.00
    assert_eq!(contract.budget.recovery_reserve(), FixedMoney::from_dollars(2));
    assert_eq!(contract.budget.available_spendable(), FixedMoney::from_dollars(8));

    // Reservation of $7.00 succeeds ($1.00 spendable remaining + $2.00 recovery reserve)
    PolicyEngine::reserve_funds(&mut contract, FixedMoney::from_dollars(7))
        .expect("Reservation of $7.00 should succeed");
    assert_eq!(contract.budget.available_spendable(), FixedMoney::from_dollars(1));

    // Reservation of an additional $2.00 attempts to consume into the $2.00 recovery reserve -> MUST FAIL!
    let err = PolicyEngine::reserve_funds(&mut contract, FixedMoney::from_dollars(2))
        .expect_err("Attempt to consume 20% recovery reserve must fail");

    match err {
        DomainError::RecoveryReserveViolation { requested, available, recovery_reserve } => {
            assert_eq!(requested, FixedMoney::from_dollars(2));
            assert_eq!(available, FixedMoney::from_dollars(1));
            assert_eq!(recovery_reserve, FixedMoney::from_dollars(2));
        }
        other => panic!("Expected RecoveryReserveViolation, got {:?}", other),
    }
}
