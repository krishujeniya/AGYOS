//! AGYOS Local Production Qualification, Redacted Metrics, and Telemetry Engine.
//!
//! Complies with Step 15 finish criteria and Principles:
//! - P15 (Tail Latency Amplification Bounds)
//! - P16 (Admission Control & Degradation)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)

pub mod backup;
pub mod metrics;
pub mod profiles;
pub mod runbook;

pub use backup::{BackupManifest, LocalBackupEngine};
pub use metrics::{MetricClass, OperationSample, RedactedMetricsCollector};
pub use profiles::{LocalFaultProfile, LocalLoadProfile, LocalOfflineProfile};
pub use runbook::{IncidentResponsePlan, IncidentSeverity, OnCallRunbook};
