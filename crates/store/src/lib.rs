//! AGYOS Embedded Transactional Store and Outbox.
//!
//! Complies with Principle P09 (Explicit State and Invariants), P10 (Atomic Durability and Sagas),
//! P11 (Idempotent Semantics), and P21 (Purpose Limitation & Privacy Risk).

pub mod dedup;
pub mod error;
pub mod event;
pub mod fence;
pub mod outbox;
pub mod transactional;
pub mod vault;

pub use dedup::DeduplicationTable;
pub use error::StoreError;
pub use event::EventRecord;
pub use fence::FenceToken;
pub use outbox::{OutboxRecord, OutboxStatus};
pub use transactional::TransactionalStore;
pub use vault::PrivateVaultBoundary;
