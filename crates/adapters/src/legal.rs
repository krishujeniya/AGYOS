//! Scoped Legal and Compliance Adapter.
//!
//! Complies with Principle P04, P05, P06, and P21 (Privacy and Regulatory Boundaries).

use std::collections::HashMap;
use domain::{ActorId, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct LegalAdapter {
    idempotency_ledger: HashMap<String, AdapterReceipt>,
}

impl LegalAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn review_contract(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        clause_text: &str,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Legal contract review cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Legal review capability revoked".to_string(),
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
        if !invocation.recipient.starts_with("jurisdiction:") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "jurisdiction:<iso-code>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        // Prohibited terms check: unlimited liability
        if clause_text.to_lowercase().contains("unlimited liability") {
            return Err(AdapterReconciliationError::ProhibitedContent(
                "Unlimited liability indemnity clause prohibited; requires General Counsel sign-off".to_string(),
            ));
        }

        // Idempotency lookup
        if let Some(cached_receipt) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-legal-{}", invocation.operation_id),
            "task-legal-review",
            expected_tenant,
            expected_caller,
            "legal:review_contract",
            &invocation.idempotency_key,
            &format!("legal-doc-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:contract-approved",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), receipt.clone());
        Ok(receipt)
    }
}
