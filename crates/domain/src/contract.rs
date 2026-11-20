//! TaskContract Implementation and Boundary Invariants.
//!
//! Complies with:
//! - Depth <= 2 (L0 Coordinator -> L1 Pod -> L2 Worker)
//! - 5 Governing Pods
//! - Risk Tiers (R0 - R3)
//! - Principle P04 (Behavioral Contracts) and P09 (Explicit State)

use serde::{Deserialize, Serialize};
use crate::budget::BudgetLedger;
use crate::error::DomainError;
use crate::gate::Gate;
use crate::id::{ActorId, RoleId, TaskId, WorkspaceId};
use crate::risk::RiskTier;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DataClass {
    Class0Public,
    Class1Internal,
    Class2PrivateClient,
    Class3RestrictedSecret,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TaskContract {
    pub id: TaskId,
    pub workspace_id: WorkspaceId,
    pub revision: u64,
    pub actor_id: ActorId,
    pub role_id: RoleId,
    pub delegation_depth: usize,
    pub risk_tier: RiskTier,
    pub data_class: DataClass,
    pub current_gate: Gate,
    pub budget: BudgetLedger,
    pub prompt: String,
}

impl TaskContract {
    pub fn new(
        id: TaskId,
        workspace_id: WorkspaceId,
        actor_id: ActorId,
        role_id: RoleId,
        delegation_depth: usize,
        risk_tier: RiskTier,
        data_class: DataClass,
        budget: BudgetLedger,
        prompt: impl Into<String>,
    ) -> Result<Self, DomainError> {
        // Enforce Depth <= 2
        if delegation_depth > 2 {
            return Err(DomainError::DelegationDepthExceeded {
                limit: 2,
                actual: delegation_depth,
            });
        }

        Ok(Self {
            id,
            workspace_id,
            revision: 1,
            actor_id,
            role_id,
            delegation_depth,
            risk_tier,
            data_class,
            current_gate: Gate::Idle,
            budget,
            prompt: prompt.into(),
        })
    }
}
