//! Local Backup, Restore, and Outstanding Effect Recovery Engine (Step 15).
//!
//! Complies with Step 15 finish criteria:
//! "An operator can recover with a clean installation and verified backup and locate every outstanding effect."
//!
//! Principles:
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics)
//! - P20 (End-to-End Observability)

use domain::WorkspaceId;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use store::{OutboxRecord, OutboxStatus, TransactionalStore};

/// Verified backup archive manifest containing SHA-256 integrity digests.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BackupManifest {
    pub workspace_id: String,
    pub created_epoch_s: u64,
    pub events_count: usize,
    pub outbox_count: usize,
    pub pending_effects_count: usize,
    pub events_digest: String,
    pub outbox_digest: String,
    pub dedup_digest: String,
    pub manifest_digest: String,
}

/// Local backup and disaster recovery coordinator.
pub struct LocalBackupEngine;

impl LocalBackupEngine {
    /// Creates a verified, self-contained backup archive from an active workspace store.
    pub fn create_backup(
        base_dir: &Path,
        workspace_id: &WorkspaceId,
        backup_archive_path: &Path,
        timestamp_s: u64,
    ) -> Result<BackupManifest, String> {
        let ws_dir = base_dir.join(workspace_id.as_str());
        if !ws_dir.exists() {
            return Err(format!("Workspace directory {:?} does not exist", ws_dir));
        }

        let events_path = ws_dir.join("events.log");
        let events_raw = if events_path.exists() {
            fs::read_to_string(&events_path).map_err(|e| e.to_string())?
        } else {
            String::new()
        };
        let events_count = events_raw.lines().filter(|l| !l.trim().is_empty()).count();
        let events_digest = crate::metrics::RedactedMetricsCollector::compute_sha256_digest(&events_raw);

        let outbox_path = ws_dir.join("outbox.json");
        let outbox_raw = if outbox_path.exists() {
            fs::read_to_string(&outbox_path).map_err(|e| e.to_string())?
        } else {
            "[]".to_string()
        };
        let outbox_records: Vec<OutboxRecord> = if outbox_path.exists() {
            serde_json::from_str(&outbox_raw)
                .map_err(|e| format!("Corrupted outbox.json in workspace: {}", e))?
        } else {
            Vec::new()
        };
        let outbox_count = outbox_records.len();
        let pending_effects_count = outbox_records
            .iter()
            .filter(|r| r.status == OutboxStatus::Pending || r.status == OutboxStatus::ExplicitUnknown)
            .count();
        let outbox_digest = crate::metrics::RedactedMetricsCollector::compute_sha256_digest(&outbox_raw);

        let dedup_path = ws_dir.join("dedup.json");
        let dedup_raw = if dedup_path.exists() {
            let content = fs::read_to_string(&dedup_path).map_err(|e| e.to_string())?;
            // Validate dedup JSON integrity
            let _: serde_json::Value = serde_json::from_str(&content)
                .map_err(|e| format!("Corrupted dedup.json in workspace: {}", e))?;
            content
        } else {
            "{}".to_string()
        };
        let dedup_digest = crate::metrics::RedactedMetricsCollector::compute_sha256_digest(&dedup_raw);

        let fence_path = ws_dir.join("fence.json");
        let fence_raw = if fence_path.exists() {
            fs::read_to_string(&fence_path).map_err(|e| e.to_string())?
        } else {
            "{\"epoch\":1}".to_string()
        };

        let manifest_content = format!(
            "{}:{}:{}:{}:{}",
            workspace_id.as_str(),
            events_digest,
            outbox_digest,
            dedup_digest,
            timestamp_s
        );
        let manifest_digest =
            crate::metrics::RedactedMetricsCollector::compute_sha256_digest(&manifest_content);

        let manifest = BackupManifest {
            workspace_id: workspace_id.as_str().to_string(),
            created_epoch_s: timestamp_s,
            events_count,
            outbox_count,
            pending_effects_count,
            events_digest,
            outbox_digest,
            dedup_digest,
            manifest_digest,
        };

        // Serialize backup archive package
        let package = serde_json::json!({
            "manifest": manifest,
            "events_raw": events_raw,
            "outbox_raw": outbox_raw,
            "dedup_raw": dedup_raw,
            "fence_raw": fence_raw,
        });

        if let Some(parent) = backup_archive_path.parent() {
            fs::create_dir_all(parent).map_err(|e| e.to_string())?;
        }
        let json = serde_json::to_string_pretty(&package).map_err(|e| e.to_string())?;
        fs::write(backup_archive_path, json).map_err(|e| e.to_string())?;

        Ok(manifest)
    }

    /// Restores a verified backup into a clean installation target directory.
    pub fn restore_backup(
        backup_archive_path: &Path,
        target_base_dir: &Path,
    ) -> Result<BackupManifest, String> {
        let package_raw = fs::read_to_string(backup_archive_path).map_err(|e| e.to_string())?;
        let package: serde_json::Value =
            serde_json::from_str(&package_raw).map_err(|e| e.to_string())?;

        let manifest: BackupManifest = serde_json::from_value(package["manifest"].clone())
            .map_err(|e| format!("Invalid backup manifest: {}", e))?;

        let events_raw = package["events_raw"].as_str().unwrap_or_default();
        let outbox_raw = package["outbox_raw"].as_str().unwrap_or("[]");
        let dedup_raw = package["dedup_raw"].as_str().unwrap_or("{}");

        // Verify digests before restoring (P09, P20)
        let calc_events_digest =
            crate::metrics::RedactedMetricsCollector::compute_sha256_digest(events_raw);
        if calc_events_digest != manifest.events_digest {
            return Err("Corrupted backup: events digest mismatch".to_string());
        }

        let calc_outbox_digest =
            crate::metrics::RedactedMetricsCollector::compute_sha256_digest(outbox_raw);
        if calc_outbox_digest != manifest.outbox_digest {
            return Err("Corrupted backup: outbox digest mismatch".to_string());
        }

        let calc_dedup_digest =
            crate::metrics::RedactedMetricsCollector::compute_sha256_digest(dedup_raw);
        if calc_dedup_digest != manifest.dedup_digest {
            return Err("Corrupted backup: dedup digest mismatch".to_string());
        }

        // Validate payload deserializability before writing any files to target destination
        if !outbox_raw.trim().is_empty() {
            let _: Vec<OutboxRecord> = serde_json::from_str(outbox_raw)
                .map_err(|e| format!("Corrupted outbox records in archive: {}", e))?;
        }
        if !dedup_raw.trim().is_empty() {
            let _: serde_json::Value = serde_json::from_str(dedup_raw)
                .map_err(|e| format!("Corrupted dedup table in archive: {}", e))?;
        }

        // Write restored state into temporary staging directory first for atomic activation (P10)
        let staging_dir = target_base_dir.join(format!(".restore_tmp_{}", manifest.workspace_id));
        if staging_dir.exists() {
            let _ = fs::remove_dir_all(&staging_dir);
        }
        if let Err(e) = fs::create_dir_all(&staging_dir) {
            return Err(format!("Failed to create staging directory: {}", e));
        }

        let write_res = (|| -> Result<(), std::io::Error> {
            fs::write(staging_dir.join("events.log"), events_raw)?;
            fs::write(staging_dir.join("outbox.json"), outbox_raw)?;
            fs::write(staging_dir.join("dedup.json"), dedup_raw)?;
            if let Some(fence_raw) = package.get("fence_raw").and_then(|v| v.as_str()) {
                fs::write(staging_dir.join("fence.json"), fence_raw)?;
            }
            Ok(())
        })();

        if let Err(e) = write_res {
            let _ = fs::remove_dir_all(&staging_dir);
            return Err(format!("Failed to write staged restore files: {}", e));
        }

        // Atomically activate restored directory
        let ws_dir = target_base_dir.join(&manifest.workspace_id);
        if ws_dir.exists() {
            let _ = fs::remove_dir_all(&ws_dir);
        }
        if let Err(e) = fs::rename(&staging_dir, &ws_dir) {
            let _ = fs::remove_dir_all(&staging_dir);
            return Err(format!("Failed to activate restored workspace directory: {}", e));
        }

        Ok(manifest)
    }

    /// Locates every outstanding effect in the restored outbox (Pending or ExplicitUnknown).
    pub fn locate_outstanding_effects(
        target_base_dir: &Path,
        workspace_id: &WorkspaceId,
    ) -> Result<Vec<OutboxRecord>, String> {
        let store = TransactionalStore::open(target_base_dir, workspace_id.clone())
            .map_err(|e| format!("Failed to open restored store: {:?}", e))?;

        // Outstanding effects are those requiring reconciliation (Pending or ExplicitUnknown)
        let pending = store
            .outbox()
            .iter()
            .filter(|rec| rec.status == OutboxStatus::Pending || rec.status == OutboxStatus::ExplicitUnknown)
            .cloned()
            .collect();

        Ok(pending)
    }
}
