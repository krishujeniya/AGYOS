//! Risk-Tiered Model Routing and Admission Control.
//!
//! Complies with Principle P15 (Tail Amplification), P16 (Admission Control),
//! and P32 (Operator-Owned Budgets).
//!
//! Policy Invariants:
//! - High-risk work (R2/R3) mandates independent verification and deliberation tier.
//! - Low-risk work (R0/R1) selects cheaper fast-path single agent.
//! - 10% control capacity reserved strictly for status and cancellation (P16).

use domain::{RiskTier, TaskContract};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ModelTier {
    FastTier,
    DeliberationTier,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExecutionMode {
    FastPathSingleAgent,
    CouncilWithIndependentChecker,
}

pub struct ModelPolicyRouter;

impl ModelPolicyRouter {
    /// Select optimal execution mode and model tier based on risk and contract boundaries.
    pub fn select_execution_mode(risk: RiskTier) -> (ExecutionMode, ModelTier) {
        match risk {
            RiskTier::R0 | RiskTier::R1 => (
                ExecutionMode::FastPathSingleAgent,
                ModelTier::FastTier,
            ),
            RiskTier::R2 | RiskTier::R3 => (
                ExecutionMode::CouncilWithIndependentChecker,
                ModelTier::DeliberationTier,
            ),
        }
    }

    /// Check whether a contract requires mandatory independent checker review.
    pub fn requires_independent_checker(contract: &TaskContract) -> bool {
        contract.risk_tier >= RiskTier::R2
    }
}

pub struct AdmissionController {
    pub max_queue_slots: usize,
    pub active_jobs: usize,
    pub queued_jobs: usize,
    pub reserved_control_slots: usize, // 10% strictly reserved for status / cancel
}

impl AdmissionController {
    pub fn new(max_slots: usize) -> Self {
        let control_slots = (max_slots * 10) / 100;
        Self {
            max_queue_slots: max_slots,
            active_jobs: 0,
            queued_jobs: 0,
            reserved_control_slots: control_slots.max(1),
        }
    }

    pub fn available_standard_slots(&self) -> usize {
        let total_in_flight = self.active_jobs + self.queued_jobs;
        let spendable = self.max_queue_slots.saturating_sub(self.reserved_control_slots);
        spendable.saturating_sub(total_in_flight)
    }

    /// Try to admit standard workload job. Fails if entering reserved control capacity.
    pub fn admit_standard_job(&mut self) -> Result<(), &'static str> {
        if self.available_standard_slots() == 0 {
            return Err("Admission rejected: capacity exhausted, reserved 10% control headroom protected");
        }
        self.queued_jobs += 1;
        Ok(())
    }

    /// Admit status or cancellation operation into the protected 10% reserve.
    pub fn admit_control_operation(&mut self) -> Result<(), &'static str> {
        let total = self.active_jobs + self.queued_jobs;
        if total >= self.max_queue_slots {
            return Err("Critical overload: even control capacity saturated");
        }
        self.active_jobs += 1;
        Ok(())
    }
}
