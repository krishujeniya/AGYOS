//! Outbox Record and Operational Lifecycle.
//!
//! Complies with Principle P10 (Atomic Durability and Sagas).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum OutboxStatus {
    Pending,
    Dispatched,
    Confirmed,
    ExplicitUnknown,
    Failed,
    Compensated,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OutboxRecord {
    pub effect_id: String,
    pub operation_key: String,
    pub effect_type: String,
    pub payload_json: String,
    pub status: OutboxStatus,
    pub retry_count: u32,
    pub updated_at_epoch_s: u64,
}
