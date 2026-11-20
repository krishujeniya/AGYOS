//! AGYOS Pure Domain Models.
//!
//! Complies with Principle P02 (Information Hiding), P04 (Behavioral Contracts),
//! P05 (Least Privilege), and P09 (Explicit State and Invariants).
//!
//! Invariant: Zero host, network, or database dependencies.

pub mod approval;
pub mod budget;
pub mod contract;
pub mod council;
pub mod error;
pub mod gate;
pub mod id;
pub mod receipt;
pub mod risk;

pub use approval::{Approval, ApprovalStatus};
pub use budget::{BudgetLedger, FixedMoney};
pub use contract::{DataClass, TaskContract};
pub use council::{Council, CouncilDissent, CouncilQuestion};
pub use error::DomainError;
pub use gate::Gate;
pub use id::{ActorId, ApprovalId, ReceiptId, RoleId, TaskId, WorkspaceId};
pub use receipt::Receipt;
pub use risk::RiskTier;
