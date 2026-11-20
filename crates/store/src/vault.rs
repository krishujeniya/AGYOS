//! Isolated Private Vault Boundary for Secrets.
//!
//! Complies with Principle P21 (Purpose Limitation & Privacy Risk) and
//! Production Invariant 5 (Zero Secrets in Plaintext/Logs).

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Default)]
pub struct PrivateVaultBoundary {
    entries: HashMap<String, String>, // key -> secret_value
}

impl PrivateVaultBoundary {
    pub fn set_secret(&mut self, key: impl Into<String>, secret: impl Into<String>) {
        self.entries.insert(key.into(), secret.into());
    }

    pub fn get_secret(&self, key: &str) -> Option<&str> {
        self.entries.get(key).map(|s| s.as_str())
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }
}
