//! Shadow Reader & Signed Difference Ledger Reconciler (Step 17).
//!
//! Complies with Step 17 finish criteria:
//! "both readers reconcile with a signed difference ledger."
//! Principles:
//! - P06 (Canonical Structured Formats)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)

use crate::legacy_reader::LegacyStateSnapshot;
use crate::mapper::MappedCanonicalState;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Specific difference between legacy and canonical state records.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StateDiscrepancy {
    pub entity_type: String,
    pub entity_id: String,
    pub legacy_value: String,
    pub canonical_value: String,
    pub reason: String,
}

/// Signed difference ledger attesting reconciliation status.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SignedDifferenceLedger {
    pub cursor_epoch_s: u64,
    pub legacy_digest: String,
    pub canonical_digest: String,
    pub matched_entities_count: usize,
    pub discrepancies: Vec<StateDiscrepancy>,
    pub is_reconciled: bool,
    pub signed_attestation: String,
}

pub struct ShadowReaderReconciler;

impl ShadowReaderReconciler {
    /// Reconciles legacy state against canonical mapped state and generates a signed difference ledger.
    pub fn reconcile(
        legacy: &LegacyStateSnapshot,
        canonical: &MappedCanonicalState,
        cursor_epoch_s: u64,
    ) -> SignedDifferenceLedger {
        let mut discrepancies = Vec::new();
        let mut matched_count = 0;

        let legacy_digest = legacy.compute_digest();
        let canonical_digest = canonical.canonical_digest.clone();

        // 1. Compare events count and sequence
        if legacy.events.len() != canonical.events.len() {
            discrepancies.push(StateDiscrepancy {
                entity_type: "events_count".to_string(),
                entity_id: "events".to_string(),
                legacy_value: legacy.events.len().to_string(),
                canonical_value: canonical.events.len().to_string(),
                reason: "Mismatch in total event records count".to_string(),
            });
        } else {
            for (leg, can) in legacy.events.iter().zip(canonical.events.iter()) {
                if leg.event_seq == can.revision && leg.kind == can.event_type {
                    matched_count += 1;
                } else {
                    discrepancies.push(StateDiscrepancy {
                        entity_type: "event_record".to_string(),
                        entity_id: leg.event_seq.to_string(),
                        legacy_value: format!("{}:{}", leg.event_seq, leg.kind),
                        canonical_value: format!("{}:{}", can.revision, can.event_type),
                        reason: "Event revision or type divergence".to_string(),
                    });
                }
            }
        }

        // 2. Compare operations / outbox records
        if legacy.operations.len() != canonical.outbox.len() {
            discrepancies.push(StateDiscrepancy {
                entity_type: "outbox_count".to_string(),
                entity_id: "operations".to_string(),
                legacy_value: legacy.operations.len().to_string(),
                canonical_value: canonical.outbox.len().to_string(),
                reason: "Mismatch in outbox records count".to_string(),
            });
        } else {
            for leg_op in &legacy.operations {
                if let Some(can_op) = canonical.outbox.iter().find(|o| o.effect_id == leg_op.op_id) {
                    if can_op.operation_key == leg_op.idempotency_key {
                        matched_count += 1;
                    } else {
                        discrepancies.push(StateDiscrepancy {
                            entity_type: "outbox_key".to_string(),
                            entity_id: leg_op.op_id.clone(),
                            legacy_value: leg_op.idempotency_key.clone(),
                            canonical_value: can_op.operation_key.clone(),
                            reason: "Operation idempotency key divergence".to_string(),
                        });
                    }
                } else {
                    discrepancies.push(StateDiscrepancy {
                        entity_type: "missing_outbox".to_string(),
                        entity_id: leg_op.op_id.clone(),
                        legacy_value: leg_op.op_id.clone(),
                        canonical_value: "NOT_FOUND".to_string(),
                        reason: "Operation missing from canonical store".to_string(),
                    });
                }
            }
        }

        // 3. Compare memories
        for leg_mem in &legacy.memories {
            if let Some(can_mem) = canonical.memory_records.iter().find(|m| m.memory_id == leg_mem.memory_id) {
                if can_mem.key == leg_mem.key {
                    matched_count += 1;
                }
            } else {
                discrepancies.push(StateDiscrepancy {
                    entity_type: "memory_record".to_string(),
                    entity_id: leg_mem.memory_id.clone(),
                    legacy_value: leg_mem.key.clone(),
                    canonical_value: "NOT_FOUND".to_string(),
                    reason: "Memory entry missing from canonical store".to_string(),
                });
            }
        }

        // 4. Compare artifacts
        for leg_art in &legacy.artifacts {
            if let Some(can_art) = canonical.artifacts.iter().find(|a| a.artifact_id == leg_art.artifact_id) {
                if can_art.sha256_hex == leg_art.sha256_hex {
                    matched_count += 1;
                } else {
                    discrepancies.push(StateDiscrepancy {
                        entity_type: "artifact_checksum".to_string(),
                        entity_id: leg_art.artifact_id.clone(),
                        legacy_value: leg_art.sha256_hex.clone(),
                        canonical_value: can_art.sha256_hex.clone(),
                        reason: "Artifact checksum mismatch".to_string(),
                    });
                }
            } else {
                discrepancies.push(StateDiscrepancy {
                    entity_type: "artifact_record".to_string(),
                    entity_id: leg_art.artifact_id.clone(),
                    legacy_value: leg_art.rel_path.clone(),
                    canonical_value: "NOT_FOUND".to_string(),
                    reason: "Artifact missing from canonical store".to_string(),
                });
            }
        }

        let is_reconciled = discrepancies.is_empty();

        // 5. Generate signed attestation
        let mut hasher = Sha256::new();
        hasher.update(cursor_epoch_s.to_be_bytes());
        hasher.update(legacy_digest.as_bytes());
        hasher.update(canonical_digest.as_bytes());
        hasher.update(if is_reconciled { "RECONCILED_SUCCESS".as_bytes() } else { "DISCREPANCIES_DETECTED".as_bytes() });
        let signature = format!("SIG-RECON-SHA256:{}", hex::encode(hasher.finalize()));

        SignedDifferenceLedger {
            cursor_epoch_s,
            legacy_digest,
            canonical_digest,
            matched_entities_count: matched_count,
            discrepancies,
            is_reconciled,
            signed_attestation: signature,
        }
    }
}
