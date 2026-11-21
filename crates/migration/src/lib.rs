//! AGYOS State Migration & Reversal Engine (Step 17).
//!
//! Complies with Step 17 finish criteria and Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P06 (Canonical Structured Formats)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics)
//! - P12 (Statistical Proof & Regression Bounds)

pub mod fencing_cutover;
pub mod legacy_reader;
pub mod mapper;
pub mod reconciler;
pub mod reversal_drill;

pub use fencing_cutover::{
    CutoverCoordinator, FencingCutoverError, MigrationCursor, WriterOwnershipReceipt, WriterRole,
};
pub use legacy_reader::{
    LegacyArtifact, LegacyEvent, LegacyMemoryRecord, LegacyOperation, LegacyRevision,
    LegacyStateReader, LegacyStateSnapshot, LegacyVaultReference,
};
pub use mapper::{
    CanonicalArtifactRecord, CanonicalMemoryItem, CanonicalVaultRef, DeterministicImportReceipt,
    MappedCanonicalState, StateMapper,
};
pub use reconciler::{ShadowReaderReconciler, SignedDifferenceLedger, StateDiscrepancy};
pub use reversal_drill::{ReversalDrillHarness, ReversalDrillResult};
