//! Risk Tiers (R0 - R3) for Operational Mediation.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum RiskTier {
    /// R0: Read-only, zero side effects or persistent state mutations.
    R0,
    /// R1: Local reversible, isolated repository or workspace file modifications.
    R1,
    /// R2: Shared internal, internal database, multi-tenant state changes.
    R2,
    /// R3: External irreversible, financial disbursement, public git push, customer messaging.
    R3,
}

impl RiskTier {
    pub fn is_external_effect(&self) -> bool {
        matches!(self, RiskTier::R3)
    }

    pub fn requires_human_approval(&self) -> bool {
        matches!(self, RiskTier::R3)
    }
}
