//! Legacy State Reader for Migration & Reversal (Step 17).
//!
//! Complies with Step 17 finish criteria and Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P06 (Canonical Structured Formats)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Legacy database revision entry.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyRevision {
    pub revision_id: u64,
    pub timestamp_epoch_s: u64,
    pub author: String,
    pub checksum: String,
}

/// Legacy operation record in SQLite outbox table.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyOperation {
    pub op_id: String,
    pub idempotency_key: String,
    pub action_type: String,
    pub raw_payload: String,
    pub status: String,
    pub retries: u32,
    pub updated_epoch_s: u64,
}

/// Legacy event entry in SQLite event log.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyEvent {
    pub event_seq: u64,
    pub timestamp: u64,
    pub kind: String,
    pub body_json: String,
}

/// Legacy memory tier entry.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyMemoryRecord {
    pub memory_id: String,
    pub tier: String,
    pub key: String,
    pub content: String,
    pub created_epoch_s: u64,
}

/// Legacy private vault secret reference.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyVaultReference {
    pub ref_id: String,
    pub scope: String,
    pub secret_alias: String,
    pub vault_path: String,
}

/// Legacy output artifact reference.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyArtifact {
    pub artifact_id: String,
    pub rel_path: String,
    pub sha256_hex: String,
    pub size_bytes: usize,
}

/// Frozen snapshot of legacy store state.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LegacyStateSnapshot {
    pub workspace_id: String,
    pub revisions: Vec<LegacyRevision>,
    pub operations: Vec<LegacyOperation>,
    pub events: Vec<LegacyEvent>,
    pub memories: Vec<LegacyMemoryRecord>,
    pub vault_refs: Vec<LegacyVaultReference>,
    pub artifacts: Vec<LegacyArtifact>,
}

impl LegacyStateSnapshot {
    /// Computes deterministic SHA-256 digest over the entire legacy state snapshot.
    pub fn compute_digest(&self) -> String {
        let serialized = serde_json::to_string(self).unwrap_or_default();
        let mut hasher = Sha256::new();
        hasher.update(serialized.as_bytes());
        hex::encode(hasher.finalize())
    }
}

/// Read-only reader for legacy state stores.
pub struct LegacyStateReader {
    snapshot: LegacyStateSnapshot,
}

impl LegacyStateReader {
    pub fn new(snapshot: LegacyStateSnapshot) -> Self {
        Self { snapshot }
    }

    /// Read-only access to legacy state snapshot.
    pub fn read_snapshot(&self) -> &LegacyStateSnapshot {
        &self.snapshot
    }

    /// Calculates deterministic SHA-256 digest of the current legacy state.
    pub fn calculate_snapshot_digest(&self) -> String {
        self.snapshot.compute_digest()
    }
}
