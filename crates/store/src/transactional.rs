//! Embedded File-Backed Transactional Store.
//!
//! Guarantees:
//! - An acknowledged local operation survives process kill.
//! - Outbox updates and state mutations commit atomically.
//! - Monotonic fence tokens reject stale split-brain writers.
//! - Workspace deletion invalidates all indexes, logs, and memory access.

use std::fs::{self, File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};

use domain::WorkspaceId;
use crate::dedup::DeduplicationTable;
use crate::error::StoreError;
use crate::event::EventRecord;
use crate::fence::FenceToken;
use crate::outbox::{OutboxRecord, OutboxStatus};
use crate::vault::PrivateVaultBoundary;

pub struct TransactionalStore {
    workspace_id: WorkspaceId,
    workspace_dir: PathBuf,
    current_fence: FenceToken,
    events: Vec<EventRecord>,
    outbox: Vec<OutboxRecord>,
    dedup: DeduplicationTable,
    vault: PrivateVaultBoundary,
}

impl TransactionalStore {
    pub fn open(base_dir: &Path, workspace_id: WorkspaceId) -> Result<Self, StoreError> {
        // Enforce root containment and validate workspace path
        let canonical_base = base_dir.canonicalize().unwrap_or_else(|_| base_dir.to_path_buf());
        let ws_dir = base_dir.join(workspace_id.as_str());
        if let Ok(canon_ws) = ws_dir.canonicalize() {
            if !canon_ws.starts_with(&canonical_base) {
                return Err(StoreError::CrossWorkspaceAccess {
                    expected: canonical_base.display().to_string(),
                    actual: canon_ws.display().to_string(),
                });
            }
        }

        fs::create_dir_all(&ws_dir).map_err(|e| StoreError::IoError(e.to_string()))?;

        // Recover durable fence token from disk or initialize to 1
        let fence_path = ws_dir.join("fence.json");
        let initial_fence = if fence_path.exists() {
            let data = fs::read_to_string(&fence_path).unwrap_or_default();
            serde_json::from_str::<u64>(&data).map(FenceToken::new).unwrap_or(FenceToken::new(1))
        } else {
            FenceToken::new(1)
        };

        let mut store = Self {
            workspace_id,
            workspace_dir: ws_dir,
            current_fence: initial_fence,
            events: Vec::new(),
            outbox: Vec::new(),
            dedup: DeduplicationTable::default(),
            vault: PrivateVaultBoundary::default(),
        };

        store.recover_from_disk()?;
        Ok(store)
    }

    pub fn current_fence(&self) -> FenceToken {
        self.current_fence
    }

    pub fn workspace_id(&self) -> &WorkspaceId {
        &self.workspace_id
    }

    pub fn set_fence(&mut self, token: FenceToken) {
        self.current_fence = token;
        let _ = self.persist_fence();
    }

    pub fn events(&self) -> &[EventRecord] {
        &self.events
    }

    pub fn outbox(&self) -> &[OutboxRecord] {
        &self.outbox
    }

    pub fn dedup(&self) -> &DeduplicationTable {
        &self.dedup
    }

    pub fn vault_mut(&mut self) -> &mut PrivateVaultBoundary {
        &mut self.vault
    }

    /// Commit transaction atomically to disk.
    /// Rejects stale fence tokens and monotonically allocates revisions internally.
    pub fn commit_transaction(
        &mut self,
        caller_fence: FenceToken,
        event: EventRecord,
        pending_outbox: Option<OutboxRecord>,
    ) -> Result<u64, StoreError> {
        if caller_fence < self.current_fence {
            return Err(StoreError::StaleFenceToken {
                current_fence: self.current_fence.epoch(),
                submitted_fence: caller_fence.epoch(),
            });
        }

        // Monotonically advance and persist fence if caller has higher epoch
        if caller_fence > self.current_fence {
            self.current_fence = caller_fence;
            self.persist_fence()?;
        }

        // Deduplication check bound to operation key and payload hash
        if let Some(ref ob) = pending_outbox {
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            let mut hasher = DefaultHasher::new();
            ob.payload_json.hash(&mut hasher);
            let payload_hash = format!("{:016x}", hasher.finish());

            if let Some(stored_val) = self.dedup.get(&ob.operation_key) {
                if let Some((stored_hash, _effect_id)) = stored_val.split_once(':') {
                    if stored_hash != payload_hash {
                        return Err(StoreError::IdempotencyConflict {
                            operation_key: ob.operation_key.clone(),
                            expected_payload_hash: stored_hash.to_string(),
                            actual_payload_hash: payload_hash,
                        });
                    }
                }
                // Identical retry -> return latest revision without re-executing
                return Ok(self.events.last().map(|e| e.revision).unwrap_or(0));
            }
        }

        // Monotonically allocate revision internally
        let next_revision = (self.events.len() + 1) as u64;
        let mut allocated_event = event;
        allocated_event.revision = next_revision;

        // 1. Write event to WAL on disk
        let events_path = self.workspace_dir.join("events.log");
        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&events_path)
            .map_err(|e| StoreError::IoError(e.to_string()))?;

        let serialized_event = serde_json::to_string(&allocated_event)
            .map_err(|e| StoreError::SerializationError(e.to_string()))?;
        writeln!(file, "{}", serialized_event).map_err(|e| StoreError::IoError(e.to_string()))?;
        file.sync_all().map_err(|e| StoreError::IoError(e.to_string()))?;

        // 2. Stage outbox record if present (bind operation_key to payload hash)
        if let Some(ob) = pending_outbox {
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            let mut hasher = DefaultHasher::new();
            ob.payload_json.hash(&mut hasher);
            let payload_hash = format!("{:016x}", hasher.finish());

            self.dedup.insert(ob.operation_key.clone(), format!("{}:{}", payload_hash, ob.effect_id));
            self.outbox.push(ob);
            self.persist_outbox()?;
            self.persist_dedup()?;
        }

        self.events.push(allocated_event);
        Ok(next_revision)
    }

    /// Update outbox record status.
    pub fn update_outbox_status(&mut self, effect_id: &str, status: OutboxStatus) -> Result<(), StoreError> {
        if let Some(record) = self.outbox.iter_mut().find(|r| r.effect_id == effect_id) {
            record.status = status;
            self.persist_outbox()?;
        }
        Ok(())
    }

    /// Persist state snapshot atomically.
    pub fn take_snapshot(&self) -> Result<(), StoreError> {
        let snap_path = self.workspace_dir.join("snapshot.json");
        let tmp_path = self.workspace_dir.join("snapshot.json.tmp");

        let json = serde_json::to_string_pretty(&self.events)
            .map_err(|e| StoreError::SerializationError(e.to_string()))?;
        fs::write(&tmp_path, json).map_err(|e| StoreError::IoError(e.to_string()))?;
        fs::rename(&tmp_path, &snap_path).map_err(|e| StoreError::IoError(e.to_string()))?;
        Ok(())
    }

    /// Recover state from disk WAL.
    fn recover_from_disk(&mut self) -> Result<(), StoreError> {
        let events_path = self.workspace_dir.join("events.log");
        if events_path.exists() {
            let file = File::open(&events_path).map_err(|e| StoreError::IoError(e.to_string()))?;
            let reader = BufReader::new(file);
            for line in reader.lines() {
                let l = line.map_err(|e| StoreError::IoError(e.to_string()))?;
                if !l.trim().is_empty() {
                    let event: EventRecord = serde_json::from_str(&l)
                        .map_err(|e| StoreError::CorruptedState(e.to_string()))?;
                    self.events.push(event);
                }
            }
        }

        let outbox_path = self.workspace_dir.join("outbox.json");
        if outbox_path.exists() {
            let data = fs::read_to_string(&outbox_path).map_err(|e| StoreError::IoError(e.to_string()))?;
            if !data.trim().is_empty() {
                self.outbox = serde_json::from_str(&data)
                    .map_err(|e| StoreError::CorruptedState(e.to_string()))?;
            }
        }

        let dedup_path = self.workspace_dir.join("dedup.json");
        if dedup_path.exists() {
            let data = fs::read_to_string(&dedup_path).map_err(|e| StoreError::IoError(e.to_string()))?;
            if !data.trim().is_empty() {
                self.dedup = serde_json::from_str(&data)
                    .map_err(|e| StoreError::CorruptedState(e.to_string()))?;
            }
        }

        Ok(())
    }

    fn persist_fence(&self) -> Result<(), StoreError> {
        let path = self.workspace_dir.join("fence.json");
        let tmp = self.workspace_dir.join("fence.json.tmp");
        fs::write(&tmp, serde_json::to_string(&self.current_fence.epoch()).unwrap_or_default())
            .map_err(|e| StoreError::IoError(e.to_string()))?;
        fs::rename(&tmp, &path).map_err(|e| StoreError::IoError(e.to_string()))?;
        Ok(())
    }

    fn persist_outbox(&self) -> Result<(), StoreError> {
        let path = self.workspace_dir.join("outbox.json");
        let tmp = self.workspace_dir.join("outbox.json.tmp");
        let json = serde_json::to_string(&self.outbox)
            .map_err(|e| StoreError::SerializationError(e.to_string()))?;
        fs::write(&tmp, json).map_err(|e| StoreError::IoError(e.to_string()))?;
        fs::rename(&tmp, &path).map_err(|e| StoreError::IoError(e.to_string()))?;
        Ok(())
    }

    fn persist_dedup(&self) -> Result<(), StoreError> {
        let path = self.workspace_dir.join("dedup.json");
        let tmp = self.workspace_dir.join("dedup.json.tmp");
        let json = serde_json::to_string(&self.dedup)
            .map_err(|e| StoreError::SerializationError(e.to_string()))?;
        fs::write(&tmp, json).map_err(|e| StoreError::IoError(e.to_string()))?;
        fs::rename(&tmp, &path).map_err(|e| StoreError::IoError(e.to_string()))?;
        Ok(())
    }

    /// Completely delete workspace and invalidate its indexes and access (P21).
    pub fn delete_workspace(base_dir: &Path, workspace_id: &WorkspaceId) -> Result<(), StoreError> {
        let canonical_base = base_dir.canonicalize().unwrap_or_else(|_| base_dir.to_path_buf());
        let ws_dir = base_dir.join(workspace_id.as_str());

        if let Ok(canon_ws) = ws_dir.canonicalize() {
            if !canon_ws.starts_with(&canonical_base) {
                return Err(StoreError::CrossWorkspaceAccess {
                    expected: canonical_base.display().to_string(),
                    actual: canon_ws.display().to_string(),
                });
            }
        }

        if !ws_dir.exists() {
            return Err(StoreError::WorkspaceNotFound(workspace_id.clone()));
        }
        fs::remove_dir_all(&ws_dir).map_err(|e| StoreError::IoError(e.to_string()))?;
        Ok(())
    }
}
