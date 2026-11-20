//! Pure State Machine Transition Rules.
//!
//! Enforces:
//! - Rejection of skipped gates (P09)
//! - Rejection of cross-workspace access (P05)
//! - Rejection of stale revisions (CAS check)

use domain::{DomainError, Gate, TaskContract, WorkspaceId};

pub struct StateMachine;

impl StateMachine {
    /// Advance gate with strict ordering checks. Rejects skipped gates!
    pub fn advance_gate(contract: &mut TaskContract, target: Gate) -> Result<(), DomainError> {
        if !contract.current_gate.can_transition_to(target) {
            return Err(DomainError::InvalidGateTransition {
                current: contract.current_gate,
                requested: target,
            });
        }
        contract.current_gate = target;
        contract.revision += 1;
        Ok(())
    }

    /// Enforce workspace isolation. Rejects cross-workspace access!
    pub fn verify_workspace(contract: &TaskContract, caller_ws: &WorkspaceId) -> Result<(), DomainError> {
        if &contract.workspace_id != caller_ws {
            return Err(DomainError::CrossWorkspaceAccessDenied {
                expected: contract.workspace_id.clone(),
                actual: caller_ws.clone(),
            });
        }
        Ok(())
    }

    /// Check revision match (CAS check). Rejects stale revisions!
    pub fn verify_revision(contract: &TaskContract, submitted_rev: u64) -> Result<(), DomainError> {
        if contract.revision != submitted_rev {
            return Err(DomainError::StaleRevision {
                current: contract.revision,
                submitted: submitted_rev,
            });
        }
        Ok(())
    }
}
