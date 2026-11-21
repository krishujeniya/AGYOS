//! AGYOS External Effect Execution, Compensating Sagas, and Outbox Broker.
//!
//! Complies with Step 13: Implement business and external effects, and Principles:
//! - P05 (Complete Mediation)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Explicit Compensation & Audit Trails)
//! - P17 (Effect Confinement)

pub mod broker;
pub mod provider;
pub mod saga;

pub use broker::EffectBroker;
pub use provider::{EffectOutcome, EffectProvider};
pub use saga::SagaCoordinator;
