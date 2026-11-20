//! AGYOS Maintenance, Canary Observation, and Retirement Engine (Step 19).
//!
//! Complies with Step 19 finish criteria and Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P06 (Canonical Structured Formats & TOON Invariants)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Clean Room Reproducibility)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)

pub mod canary;
pub mod export_restore;
pub mod risks_metrics;

pub use canary::{CanaryObservation, CanaryRetirementEngine, RetirementReceipt};
pub use export_restore::{PortableToonArchive, RestoredWorkspaceState, VendorIndependentEngine};
pub use risks_metrics::{BaselineMetricItem, MaintenanceRiskLedger, OpenRisk};
