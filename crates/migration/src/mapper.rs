//! State Mapper: Legacy SQLite/JSON to Canonical Rust/TOON Models (Step 17).
//!
//! Complies with Principle P06 (Canonical Structured Formats) and P09 (Explicit State & Invariants).
//! Invariant: Mapping is 100% deterministic. Two independent runs produce identical records.

use crate::legacy_reader::LegacyStateSnapshot;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use store::{EventRecord, OutboxRecord, OutboxStatus};

/// Canonical memory item representation.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CanonicalMemoryItem {
    pub memory_id: String,
    pub tier: String,
    pub key: String,
    pub content_digest: String,
    pub content: String,
    pub created_epoch_s: u64,
}

/// Canonical vault reference with strict scoped permission.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CanonicalVaultRef {
    pub ref_id: String,
    pub scope: String,
    pub secret_alias: String,
    pub vault_path: String,
}

/// Canonical artifact record with verified integrity digest.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CanonicalArtifactRecord {
    pub artifact_id: String,
    pub rel_path: String,
    pub sha256_hex: String,
    pub size_bytes: usize,
}

/// Fully mapped canonical state resulting from legacy import.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MappedCanonicalState {
    pub workspace_id: String,
    pub latest_revision: u64,
    pub events: Vec<EventRecord>,
    pub outbox: Vec<OutboxRecord>,
    pub memory_records: Vec<CanonicalMemoryItem>,
    pub vault_references: Vec<CanonicalVaultRef>,
    pub artifacts: Vec<CanonicalArtifactRecord>,
    pub canonical_digest: String,
}

/// Deterministic receipt proving identical imports.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DeterministicImportReceipt {
    pub source_sha256: String,
    pub target_sha256: String,
    pub mapped_events_count: usize,
    pub mapped_outbox_count: usize,
    pub mapped_memory_count: usize,
    pub mapped_artifacts_count: usize,
    pub is_identical_match: bool,
}

pub struct StateMapper;

impl StateMapper {
    /// Maps a legacy snapshot into canonical Rust/TOON domain structures deterministically.
    pub fn map_snapshot(legacy: &LegacyStateSnapshot) -> Result<MappedCanonicalState, String> {
        let latest_revision = legacy
            .revisions
            .iter()
            .map(|r| r.revision_id)
            .max()
            .unwrap_or(0);

        // 1. Map events
        let mut events = Vec::with_capacity(legacy.events.len());
        for ev in &legacy.events {
            events.push(EventRecord {
                revision: ev.event_seq,
                timestamp_epoch_s: ev.timestamp,
                event_type: ev.kind.clone(),
                payload_json: ev.body_json.clone(),
            });
        }
        events.sort_by_key(|e| e.revision);

        // 2. Map outbox records
        let mut outbox = Vec::with_capacity(legacy.operations.len());
        for op in &legacy.operations {
            let status = match op.status.to_lowercase().as_str() {
                "confirmed" => OutboxStatus::Confirmed,
                "dispatched" => OutboxStatus::Dispatched,
                "explicit_unknown" => OutboxStatus::ExplicitUnknown,
                "failed" => OutboxStatus::Failed,
                "compensated" => OutboxStatus::Compensated,
                _ => OutboxStatus::Pending,
            };

            outbox.push(OutboxRecord {
                effect_id: op.op_id.clone(),
                operation_key: op.idempotency_key.clone(),
                effect_type: op.action_type.clone(),
                payload_json: op.raw_payload.clone(),
                status,
                retry_count: op.retries,
                updated_at_epoch_s: op.updated_epoch_s,
            });
        }
        outbox.sort_by(|a, b| a.effect_id.cmp(&b.effect_id));

        // 3. Map memory items
        let mut memory_records = Vec::with_capacity(legacy.memories.len());
        for mem in &legacy.memories {
            let mut hasher = Sha256::new();
            hasher.update(mem.content.as_bytes());
            let content_digest = hex::encode(hasher.finalize());

            memory_records.push(CanonicalMemoryItem {
                memory_id: mem.memory_id.clone(),
                tier: mem.tier.clone(),
                key: mem.key.clone(),
                content_digest,
                content: mem.content.clone(),
                created_epoch_s: mem.created_epoch_s,
            });
        }
        memory_records.sort_by(|a, b| a.memory_id.cmp(&b.memory_id));

        // 4. Map vault references
        let mut vault_references = Vec::with_capacity(legacy.vault_refs.len());
        for v in &legacy.vault_refs {
            vault_references.push(CanonicalVaultRef {
                ref_id: v.ref_id.clone(),
                scope: v.scope.clone(),
                secret_alias: v.secret_alias.clone(),
                vault_path: v.vault_path.clone(),
            });
        }
        vault_references.sort_by(|a, b| a.ref_id.cmp(&b.ref_id));

        // 5. Map artifacts
        let mut artifacts = Vec::with_capacity(legacy.artifacts.len());
        for art in &legacy.artifacts {
            artifacts.push(CanonicalArtifactRecord {
                artifact_id: art.artifact_id.clone(),
                rel_path: art.rel_path.clone(),
                sha256_hex: art.sha256_hex.clone(),
                size_bytes: art.size_bytes,
            });
        }
        artifacts.sort_by(|a, b| a.artifact_id.cmp(&b.artifact_id));

        // 6. Compute canonical state digest
        let mut hasher = Sha256::new();
        hasher.update(legacy.workspace_id.as_bytes());
        hasher.update(latest_revision.to_be_bytes());
        for ev in &events {
            hasher.update(ev.revision.to_be_bytes());
            hasher.update(ev.event_type.as_bytes());
            hasher.update(ev.payload_json.as_bytes());
        }
        for ob in &outbox {
            hasher.update(ob.effect_id.as_bytes());
            hasher.update(ob.operation_key.as_bytes());
            hasher.update(ob.payload_json.as_bytes());
        }
        for mem in &memory_records {
            hasher.update(mem.content_digest.as_bytes());
        }
        for art in &artifacts {
            hasher.update(art.sha256_hex.as_bytes());
        }
        let canonical_digest = hex::encode(hasher.finalize());

        Ok(MappedCanonicalState {
            workspace_id: legacy.workspace_id.clone(),
            latest_revision,
            events,
            outbox,
            memory_records,
            vault_references,
            artifacts,
            canonical_digest,
        })
    }

    /// Verifies that two independent import executions produce identical mapped records.
    pub fn verify_deterministic_import(
        import1: &MappedCanonicalState,
        import2: &MappedCanonicalState,
        source_digest: &str,
    ) -> DeterministicImportReceipt {
        let is_identical = import1 == import2 && import1.canonical_digest == import2.canonical_digest;

        DeterministicImportReceipt {
            source_sha256: source_digest.to_string(),
            target_sha256: import1.canonical_digest.clone(),
            mapped_events_count: import1.events.len(),
            mapped_outbox_count: import1.outbox.len(),
            mapped_memory_count: import1.memory_records.len(),
            mapped_artifacts_count: import1.artifacts.len(),
            is_identical_match: is_identical,
        }
    }
}
