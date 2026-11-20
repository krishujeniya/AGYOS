//! AGYOS Maintenance, Canary Observation, Retirement, and Research Refresh Engine (Steps 19 & 20).
//!
//! Complies with Step 19 & 20 finish criteria and Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P04 (Behavioral Contracts & Compatibility)
//! - P06 (Canonical Structured Formats & TOON Invariants)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Clean Room Reproducibility)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)
//! - P20 (Bounded Autonomous Loops)
//! - P25 (Deliberation Councils)
//! - P26 (Howard 1966 EVPI)
//! - P27 (Empirical 4-Arm Benchmark)

pub mod canary;
pub mod export_restore;
pub mod research_decision;
pub mod risks_metrics;

pub use canary::{CanaryObservation, CanaryRetirementEngine, RetirementReceipt};
pub use export_restore::{PortableToonArchive, RestoredWorkspaceState, VendorIndependentEngine};
pub use research_decision::{
    DecisionDisposition, RdrValidationReceipt, ResearchDecisionEntry, ResearchDecisionRecord,
    SourceCategory,
};
pub use risks_metrics::{BaselineMetricItem, MaintenanceRiskLedger, OpenRisk};
