//! Approval, Consent, and Revocation Models.
//!
//! Complies with Principle P05 (Least Privilege) and P30 (Authority as Human Choice).

use serde::{Deserialize, Serialize};
use crate::id::{ActorId, ApprovalId};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ApprovalStatus {
    Pending,
    Approved,
    Declined,
    Expired,
    Revoked,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Approval {
    pub id: ApprovalId,
    pub granter: ActorId,
    pub scope: String,
    pub status: ApprovalStatus,
    pub granted_at_epoch_s: u64,
    pub expires_at_epoch_s: u64,
    pub signature_digest: String,
}

impl Approval {
    pub fn is_valid_at(&self, scope_req: &str, current_time_epoch_s: u64) -> bool {
        if self.status != ApprovalStatus::Approved {
            return false;
        }
        if self.scope != scope_req {
            return false;
        }
        if current_time_epoch_s > self.expires_at_epoch_s {
            return false;
        }
        true
    }

    pub fn revoke(&mut self) {
        self.status = ApprovalStatus::Revoked;
    }
}
