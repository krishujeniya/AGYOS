//! Gate Lifecycle Definitions and Strict Transition Rules.
//!
//! Complies with Principle P09 (Explicit State and Invariants).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Gate {
    Idle,
    Understand,
    Analyze,
    Plan,
    Implement,
    Verify,
    Ship,
    Reflect,
}

impl Gate {
    /// Returns true if transitioning from `self` to `target` follows the strictly valid progression.
    /// Any skipped gate (e.g. Understand -> Implement) is rejected!
    pub fn can_transition_to(&self, target: Gate) -> bool {
        match (*self, target) {
            (Gate::Idle, Gate::Understand) => true,
            (Gate::Understand, Gate::Analyze) => true,
            (Gate::Analyze, Gate::Plan) => true,
            (Gate::Plan, Gate::Implement) => true,
            (Gate::Implement, Gate::Verify) => true,
            (Gate::Verify, Gate::Ship) => true,
            (Gate::Ship, Gate::Reflect) => true,
            (Gate::Reflect, Gate::Idle) => true,
            // Re-evaluations and backward loops (Review failure / rework)
            (Gate::Verify, Gate::Implement) => true,
            (Gate::Implement, Gate::Plan) => true,
            (Gate::Plan, Gate::Analyze) => true,
            // Self-transitions are no-ops
            (a, b) if a == b => true,
            _ => false,
        }
    }
}
