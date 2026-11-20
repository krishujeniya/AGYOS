//! AGYOS Release Certification & Cutover Qualification Engine (Step 18).
//!
//! Complies with Step 18 finish criteria and Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Build Provenance & Supply Chain Integrity)
//! - P09 (Explicit State & Invariants)
//! - P10 (Leases with Fencing & Atomic Sagas)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)

pub mod clean_machine_verifier;
pub mod cutover_guard;
pub mod discovery_handover;
pub mod gates;

pub use clean_machine_verifier::{CleanMachineReport, CleanMachineVerifier};
pub use cutover_guard::{LiveCutoverGuard, VerifiedReleaseExecutionReceipt};
pub use discovery_handover::{ClientDiscoveryProject, SignedHandoverCertificate};
pub use gates::{
    OperatorApprovalToken, ReleaseCandidate, ReleaseGateEngine, ReleaseGateFailure,
};
