//! Immutable Receipts and Evidence Verification.
//!
//! Complies with Principle P06 (Traceable Provenance) and P08 (Build Provenance).

use serde::{Deserialize, Serialize};
use crate::id::{ActorId, ReceiptId, TaskId, WorkspaceId};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Receipt {
    pub id: ReceiptId,
    pub task_id: TaskId,
    pub workspace_id: WorkspaceId,
    pub actor_id: ActorId,
    pub action: String,
    pub input_digest: String,
    pub output_digest: String,
    pub timestamp_epoch_s: u64,
    pub verified: bool,
}
