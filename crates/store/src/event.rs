//! Append-Only Event Records and Monotonic Revisions.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EventRecord {
    pub revision: u64,
    pub timestamp_epoch_s: u64,
    pub event_type: String,
    pub payload_json: String,
}
