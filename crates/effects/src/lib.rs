//! AGYOS Privileged Effect Broker and Saga Compensator.
//!
//! Complies with Principle P05 (Complete Mediation), P10 (Atomic Durability and Sagas),
//! and P11 (Idempotent Semantics).

pub mod broker;
pub mod provider;
pub mod saga;

pub use broker::EffectBroker;
pub use provider::{EffectOutcome, EffectProvider, MockFixtureProvider};
pub use saga::SagaCoordinator;
