//! Scoped Hiring and People Operations Adapter.
//!
//! Complies with Principle P04, P05, P21, and P25 (Selective Cognitive Forcing).

use std::collections::HashMap;
use domain::{ActorId, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct HiringAdapter {
    idempotency_ledger: HashMap<String, AdapterReceipt>,
}

impl HiringAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn evaluate_candidate(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        rubric_criteria: &str,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Candidate evaluation cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Hiring screening capability revoked".to_string(),
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
        if !invocation.recipient.starts_with("candidate:") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "candidate:<id>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        // Prohibited content check: inquiring into protected demographic characteristics
        let rubric_lower = rubric_criteria.to_lowercase();
        if rubric_lower.contains("protected demographic") || rubric_lower.contains("marital status") {
            return Err(AdapterReconciliationError::ProhibitedContent(
                "Inquiry into protected demographic characteristics strictly prohibited by employment policy".to_string(),
            ));
        }

        // Idempotency lookup
        if let Some(cached_receipt) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-hire-{}", invocation.operation_id),
            "task-hiring-eval",
            expected_tenant,
            expected_caller,
            "hiring:evaluate_candidate",
            &invocation.idempotency_key,
            &format!("eval-scorecard-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:scorecard-verified",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), receipt.clone());
        Ok(receipt)
    }
}
