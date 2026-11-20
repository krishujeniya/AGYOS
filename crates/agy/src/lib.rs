//! AGYOS AGY Host Bridge, Projection Engine, and Broker Confinement.
//!
//! Complies with Step 08 acceptance criteria and Principles P04, P05, P09, P11, P13, P29.

pub mod bridge;
pub mod confinement;
pub mod projection;
pub mod version;

pub use bridge::{AgyBridge, BridgeError, ExecutionReceipt};
pub use confinement::{ConfinementError, ConfinementGuard};
pub use projection::{ProjectionEngine, ProjectionError};
pub use version::{AgyVersion, VersionError};
