//! Policy Engine for Budget and Approval Verification.
//!
//! Enforces:
//! - 20% untouchable recovery reserve fund (P32)
//! - Expiration and scope checks on human approvals (P05, P30)

use domain::{Approval, DomainError, FixedMoney, TaskContract};

pub struct PolicyEngine;

impl PolicyEngine {
    /// Verify human approval validity against requested scope and current timestamp.
    pub fn verify_approval(
        approval: &Approval,
        required_scope: &str,
        current_time_epoch_s: u64,
    ) -> Result<(), DomainError> {
        if current_time_epoch_s > approval.expires_at_epoch_s {
            return Err(DomainError::ApprovalExpired {
                expires_at_epoch_s: approval.expires_at_epoch_s,
                current_epoch_s: current_time_epoch_s,
            });
        }
        if approval.scope != required_scope {
            return Err(DomainError::ApprovalScopeMismatch {
                required: required_scope.to_string(),
                provided: approval.scope.clone(),
            });
        }
        Ok(())
    }

    /// Attempt to reserve funds for task operations.
    /// Strictly guarantees that the 20% recovery reserve fund remains untouchable!
    pub fn reserve_funds(contract: &mut TaskContract, amount: FixedMoney) -> Result<(), DomainError> {
        contract.budget.reserve(amount)
    }
}
