//! Scoped Git Publication and Provenance Adapter.
//!
//! Complies with Principle P04, P05, P06, and P08 (Build Provenance).
//!
//! Invariants:
//! - Single main branch exclusive! Pushes to feature branches or divergent remotes are rejected.
//! - Identity lock: author must match Krish Ujeniya.
//! - Repeated publication with conflicting commit tree fails with RepeatedPublicationAttempt.

use std::collections::HashMap;
use domain::{ActorId, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct GitAdapter {
    publication_ledger: HashMap<String, (String, AdapterReceipt)>, // tag -> (commit_sha, receipt)
}

impl GitAdapter {
    pub fn new() -> Self {
        Self {
            publication_ledger: HashMap::new(),
        }
    }

    pub fn publish_release_tag(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        target_branch: &str,
        commit_sha: &str,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Git publication cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Git publication capability revoked".to_string(),
            ));
        }
        if current_time_epoch_s > invocation.deadline_epoch_s {
            return Err(AdapterReconciliationError::DeadlineExpired {
                deadline: invocation.deadline_epoch_s,
                current: current_time_epoch_s,
            });
        }
        if &invocation.tenant_id != expected_tenant {
            return Err(AdapterReconciliationError::TenantMismatch {
                expected: expected_tenant.clone(),
                actual: invocation.tenant_id.clone(),
            });
        }
        if &invocation.caller_id != expected_caller {
            return Err(AdapterReconciliationError::IdentityMismatch {
                expected: expected_caller.clone(),
                actual: invocation.caller_id.clone(),
            });
        }

        // Single main branch invariant
        if target_branch != "main" && target_branch != "refs/heads/main" {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "main".to_string(),
                actual: target_branch.to_string(),
            });
        }

        let release_tag = &invocation.recipient;
        if !release_tag.starts_with("refs/tags/") && !release_tag.starts_with("v") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "refs/tags/<version> or v<semver>".to_string(),
                actual: release_tag.clone(),
            });
        }

        // Repeated publication check
        if let Some((existing_sha, cached_receipt)) = self.publication_ledger.get(release_tag) {
            if existing_sha != commit_sha {
                return Err(AdapterReconciliationError::RepeatedPublicationAttempt(format!(
                    "Conflicting commit SHA for tag '{}': existing {}, attempted {}",
                    release_tag, existing_sha, commit_sha
                )));
            }
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-git-{}", invocation.operation_id),
            "task-git-publish",
            expected_tenant,
            expected_caller,
            "git:publish_tag",
            &invocation.idempotency_key,
            &format!("git-tag-{}", release_tag),
            &invocation.payload_digest,
            commit_sha,
            current_time_epoch_s,
        );

        self.publication_ledger.insert(release_tag.clone(), (commit_sha.to_string(), receipt.clone()));
        Ok(receipt)
    }
}
