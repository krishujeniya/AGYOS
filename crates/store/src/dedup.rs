//! Deduplication Table for Idempotent Execution.
//!
//! Complies with Principle P11 (Idempotent Semantics).

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Default)]
pub struct DeduplicationTable {
    pub entries: HashMap<String, String>, // operation_key -> result_receipt_json
}

impl DeduplicationTable {
    pub fn contains(&self, operation_key: &str) -> bool {
        self.entries.contains_key(operation_key)
    }

    pub fn get(&self, operation_key: &str) -> Option<&String> {
        self.entries.get(operation_key)
    }

    pub fn insert(&mut self, operation_key: String, result_receipt_json: String) {
        self.entries.insert(operation_key, result_receipt_json);
    }
}
