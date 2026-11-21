//! Isolated Private Vault Boundary for Secrets.
//!
//! Complies with Principle P21 (Purpose Limitation & Privacy Risk) and
//! Production Invariant 5 (Zero Secrets in Plaintext/Logs).

use serde::{Deserialize, Serialize, Serializer};
use std::collections::HashMap;
use std::fmt;

#[derive(Clone, PartialEq, Eq, Default)]
pub struct PrivateVaultBoundary {
    entries: HashMap<String, String>, // key -> secret_value
}

impl fmt::Debug for PrivateVaultBoundary {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("PrivateVaultBoundary")
            .field("keys_count", &self.entries.len())
            .field("keys", &self.entries.keys().collect::<Vec<_>>())
            .field("secrets", &"[REDACTED]")
            .finish()
    }
}

impl Serialize for PrivateVaultBoundary {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        use serde::ser::SerializeMap;
        let mut map = serializer.serialize_map(Some(self.entries.len()))?;
        for k in self.entries.keys() {
            map.serialize_entry(k, "[REDACTED-SECRET]")?;
        }
        map.end()
    }
}

impl<'de> Deserialize<'de> for PrivateVaultBoundary {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let entries = HashMap::<String, String>::deserialize(deserializer)?;
        Ok(Self { entries })
    }
}

impl PrivateVaultBoundary {
    pub fn set_secret(&mut self, key: impl Into<String>, secret: impl Into<String>) {
        self.entries.insert(key.into(), secret.into());
    }

    pub fn get_secret(&self, key: &str) -> Option<&str> {
        self.entries.get(key).map(|s| s.as_str())
    }

    pub fn contains_key(&self, key: &str) -> bool {
        self.entries.contains_key(key)
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }
}
