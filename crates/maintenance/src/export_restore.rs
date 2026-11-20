//! Vendor-Independent Export and Restoration Engine (Step 19).
//!
//! Complies with Step 19 finish criteria:
//! "Operator can export and restore without the original vendor."
//!
//! Principles:
//! - P06 (Canonical Structured Formats & TOON Invariants)
//! - P08 (Clean Room Reproducibility)
//! - P09 (Explicit State & Invariants)
//! - P21 (Privacy & Boundary Protection)

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use store::{EventRecord, OutboxRecord};

/// Portable vendor-agnostic TOON archive of workspace state.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PortableToonArchive {
    pub workspace_id: String,
    pub exported_at_epoch_s: u64,
    pub events_count: usize,
    pub outbox_count: usize,
    pub raw_toon_payload: String,
    pub archive_sha256: String,
}

/// Restored workspace state recovered without external vendor dependence.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RestoredWorkspaceState {
    pub workspace_id: String,
    pub events: Vec<EventRecord>,
    pub outbox: Vec<OutboxRecord>,
    pub restored_at_epoch_s: u64,
    pub is_verified: bool,
}

pub struct VendorIndependentEngine;

impl VendorIndependentEngine {
    /// Exports complete workspace events and outbox into a self-describing, vendor-agnostic TOON archive.
    pub fn export_archive(
        workspace_id: &str,
        events: &[EventRecord],
        outbox: &[OutboxRecord],
        current_epoch_s: u64,
    ) -> PortableToonArchive {
        let events_json = serde_json::to_string(events).unwrap_or_default();
        let outbox_json = serde_json::to_string(outbox).unwrap_or_default();

        let raw_toon = format!(
            "archive:\n  workspace: \"{}\"\n  exported_at: {}\n  events: {}\n  outbox: {}\n",
            workspace_id, current_epoch_s, events_json, outbox_json
        );

        let mut hasher = Sha256::new();
        hasher.update(raw_toon.as_bytes());
        let archive_sha256 = hex::encode(hasher.finalize());

        PortableToonArchive {
            workspace_id: workspace_id.to_string(),
            exported_at_epoch_s: current_epoch_s,
            events_count: events.len(),
            outbox_count: outbox.len(),
            raw_toon_payload: raw_toon,
            archive_sha256,
        }
    }

    /// Restores workspace state completely from a portable TOON archive without external vendor or cloud APIs.
    pub fn restore_archive(
        archive: &PortableToonArchive,
        current_epoch_s: u64,
    ) -> Result<RestoredWorkspaceState, String> {
        // 1. Verify archive integrity digest
        let mut hasher = Sha256::new();
        hasher.update(archive.raw_toon_payload.as_bytes());
        let computed_digest = hex::encode(hasher.finalize());

        if computed_digest != archive.archive_sha256 {
            return Err("Archive integrity verification failed: SHA-256 digest mismatch".to_string());
        }

        // 2. Parse events from portable payload
        let events_marker = "  events: ";
        let outbox_marker = "  outbox: ";

        let events_start = archive
            .raw_toon_payload
            .find(events_marker)
            .ok_or("Missing events section in portable archive")?
            + events_marker.len();
        let events_end = archive
            .raw_toon_payload[events_start..]
            .find('\n')
            .map(|idx| events_start + idx)
            .unwrap_or(archive.raw_toon_payload.len());
        let events_str = &archive.raw_toon_payload[events_start..events_end];
        let events: Vec<EventRecord> = serde_json::from_str(events_str)
            .map_err(|e| format!("Failed to parse events: {}", e))?;

        // 3. Parse outbox from portable payload
        let outbox_start = archive
            .raw_toon_payload
            .find(outbox_marker)
            .ok_or("Missing outbox section in portable archive")?
            + outbox_marker.len();
        let outbox_end = archive
            .raw_toon_payload[outbox_start..]
            .find('\n')
            .map(|idx| outbox_start + idx)
            .unwrap_or(archive.raw_toon_payload.len());
        let outbox_str = &archive.raw_toon_payload[outbox_start..outbox_end];
        let outbox: Vec<OutboxRecord> = serde_json::from_str(outbox_str)
            .map_err(|e| format!("Failed to parse outbox: {}", e))?;

        if events.len() != archive.events_count || outbox.len() != archive.outbox_count {
            return Err("Restored entity count does not match archive manifest".to_string());
        }

        Ok(RestoredWorkspaceState {
            workspace_id: archive.workspace_id.clone(),
            events,
            outbox,
            restored_at_epoch_s: current_epoch_s,
            is_verified: true,
        })
    }
}
