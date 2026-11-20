//! Domain Error Types and Invariant Diagnostics.

use std::fmt;
use crate::budget::FixedMoney;
use crate::gate::Gate;
use crate::id::WorkspaceId;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DomainError {
    DelegationDepthExceeded { limit: usize, actual: usize },
    InvalidGateTransition { current: Gate, requested: Gate },
    CrossWorkspaceAccessDenied { expected: WorkspaceId, actual: WorkspaceId },
    StaleRevision { current: u64, submitted: u64 },
    ApprovalExpired { expires_at_epoch_s: u64, current_epoch_s: u64 },
    ApprovalScopeMismatch { required: String, provided: String },
    RecoveryReserveViolation { requested: FixedMoney, available: FixedMoney, recovery_reserve: FixedMoney },
    BudgetExceeded { requested: FixedMoney, available: FixedMoney },
    UnauthorizedR3Effect(String),
}

impl fmt::Display for DomainError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DomainError::DelegationDepthExceeded { limit, actual } => {
                write!(f, "Delegation depth ceiling exceeded: limit {}, actual {}", limit, actual)
            }
            DomainError::InvalidGateTransition { current, requested } => {
                write!(f, "Invalid gate transition: cannot skip or jump from {:?} to {:?}", current, requested)
            }
            DomainError::CrossWorkspaceAccessDenied { expected, actual } => {
                write!(f, "Cross-workspace access denied: contract belongs to {}, caller is {}", expected, actual)
            }
            DomainError::StaleRevision { current, submitted } => {
                write!(f, "Stale revision rejected: current revision is {}, submitted is {}", current, submitted)
            }
            DomainError::ApprovalExpired { expires_at_epoch_s, current_epoch_s } => {
                write!(f, "Approval expired at epoch {}s, current time is {}s", expires_at_epoch_s, current_epoch_s)
            }
            DomainError::ApprovalScopeMismatch { required, provided } => {
                write!(f, "Approval scope mismatch: required '{}', provided '{}'", required, provided)
            }
            DomainError::RecoveryReserveViolation { requested, available, recovery_reserve } => {
                write!(
                    f,
                    "Reservation of ${:.4} exceeds spendable balance ${:.4}; cannot consume ${:.4} recovery reserve",
                    requested.as_f64(),
                    available.as_f64(),
                    recovery_reserve.as_f64()
                )
            }
            DomainError::BudgetExceeded { requested, available } => {
                write!(f, "Budget exceeded: requested ${:.4}, available ${:.4}", requested.as_f64(), available.as_f64())
            }
            DomainError::UnauthorizedR3Effect(msg) => write!(f, "Unauthorized R3 external effect: {}", msg),
        }
    }
}

impl std::error::Error for DomainError {}
