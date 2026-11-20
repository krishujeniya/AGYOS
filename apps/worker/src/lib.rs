//! AGYOS Hosted Worker & Heavy Production Engine.
//!
//! Complies with Step 16: Qualify heavy production, and Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P15 (Tail Latency Amplification Bounds)
//! - P16 (Admission Control & Degradation)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)
//! - P32 (Operator-Owned Budgets)

pub mod admission;
pub mod budget_limits;
pub mod encrypted_backup;
pub mod envelope;
pub mod leases;

pub use admission::{AdmissionVerdict, HostedTrafficClass, QueueAdmissionController, QueuedJob};
pub use budget_limits::SpendingLimitController;
pub use encrypted_backup::{EncryptedBackupEngine, EncryptedBackupEnvelope};
pub use envelope::{HostedEnvelopeRunner, HostedQualificationReport};
pub use leases::{WorkerId, WorkerLease, WorkerPoolLeaseManager};
