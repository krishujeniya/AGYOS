//! Scoped Helpdesk Adapter.
//!
//! Complies with Principle P04, P05, P11, and P23 (Human-Centered Delivery).

use std::collections::HashMap;
use domain::{ActorId, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct HelpdeskAdapter {
    idempotency_ledger: HashMap<String, AdapterReceipt>,
}

impl HelpdeskAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn triage_ticket(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Ticket triage cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Helpdesk triage capability revoked".to_string(),
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
        if !invocation.recipient.starts_with("ticket:") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "ticket:<id>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        // Idempotency lookup
        if let Some(cached_receipt) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-helpdesk-{}", invocation.operation_id),
            "task-helpdesk-triage",
            expected_tenant,
            expected_caller,
            "helpdesk:triage_ticket",
            &invocation.idempotency_key,
            &format!("ext-ticket-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:ticket-triaged",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), receipt.clone());
        Ok(receipt)
    }
}
