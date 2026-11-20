//! Cutover Guard & In-Flight Recheck Engine (Step 18).
//!
//! Complies with Step 18 finish criteria:
//! "Recheck the fence, cursor and in-flight ledger at the actual switch.
//! Decline, failed CI, stale evidence and changed artifact all block."
//!
//! Principles:
//! - P05 (Complete Mediation)
//! - P09 (Explicit State & Invariants)
//! - P10 (Leases with Fencing & Atomic Sagas)
//! - P17 (Progressive Delivery & Canary Gates)

use crate::gates::{ReleaseCandidate, ReleaseGateEngine, ReleaseGateFailure};
use migration::{CutoverCoordinator, MigrationCursor, WriterRole};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use store::{FenceToken, OutboxRecord, OutboxStatus};

/// Verified certificate emitted when live release cutover succeeds.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct VerifiedReleaseExecutionReceipt {
    pub release_tag: String,
    pub commit_sha: String,
    pub active_writer: WriterRole,
    pub final_fence: FenceToken,
    pub cursor_id: String,
    pub verified_at_epoch_s: u64,
    pub receipt_signature: String,
}

pub struct LiveCutoverGuard;

impl LiveCutoverGuard {
    /// Executes the final verification and live cutover transition.
    /// Rechecks all release candidate gates, current fence, verified cursor, and in-flight outbox queue.
    pub fn execute_cutover(
        candidate: &ReleaseCandidate,
        coordinator: &mut CutoverCoordinator,
        cursor: &MigrationCursor,
        in_flight_outbox: &[OutboxRecord],
        current_epoch_s: u64,
        max_evidence_age_s: u64,
    ) -> Result<VerifiedReleaseExecutionReceipt, Vec<ReleaseGateFailure>> {
        let mut failures = Vec::new();

        // 1. Evaluate release candidate gates (SHA, CI status, evidence freshness, digests, separate approvals)
        if let Err(gate_errs) = ReleaseGateEngine::evaluate_candidate(candidate, current_epoch_s, max_evidence_age_s) {
            failures.extend(gate_errs);
        }

        // 2. Recheck fence token at the actual switch
        if coordinator.current_fence().epoch() != cursor.fence_token.epoch() {
            failures.push(ReleaseGateFailure::StaleFenceOrCursor {
                details: format!(
                    "Coordinator fence epoch {} differs from migration cursor fence {}",
                    coordinator.current_fence().epoch(),
                    cursor.fence_token.epoch()
                ),
            });
        }

        // 3. Recheck in-flight ledger: must have 0 uncommitted/pending operations
        let pending_count = in_flight_outbox
            .iter()
            .filter(|o| o.status == OutboxStatus::Pending || o.status == OutboxStatus::Dispatched)
            .count();
        if pending_count > 0 {
            failures.push(ReleaseGateFailure::UncommittedInFlightWorkRemaining {
                count: pending_count,
            });
        }

        if !failures.is_empty() {
            return Err(failures);
        }

        // 4. Perform atomic writer ownership transfer
        let transfer_res = coordinator.transfer_writer_ownership(cursor, current_epoch_s);
        if let Err(e) = transfer_res {
            failures.push(ReleaseGateFailure::StaleFenceOrCursor {
                details: format!("Ownership transfer failed: {:?}", e),
            });
            return Err(failures);
        }

        // 5. Generate signed execution receipt
        let mut hasher = Sha256::new();
        hasher.update(candidate.release_tag.as_bytes());
        hasher.update(candidate.target_commit_sha.as_bytes());
        hasher.update(cursor.cursor_id.as_bytes());
        hasher.update(coordinator.current_fence().epoch().to_be_bytes());
        hasher.update(current_epoch_s.to_be_bytes());
        hasher.update(b"VERIFIED_LIVE_RELEASE_CUTOVER");
        let receipt_signature = format!("SIG-LIVE-RELEASE:{}", hex::encode(hasher.finalize()));

        Ok(VerifiedReleaseExecutionReceipt {
            release_tag: candidate.release_tag.clone(),
            commit_sha: candidate.target_commit_sha.clone(),
            active_writer: coordinator.active_role(),
            final_fence: coordinator.current_fence(),
            cursor_id: cursor.cursor_id.clone(),
            verified_at_epoch_s: current_epoch_s,
            receipt_signature,
        })
    }
}
