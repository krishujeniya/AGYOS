//! Scoped CRM Adapter.
//!
//! Complies with Principle P04, P05, P06, and P11 (Idempotent Semantics).

use std::collections::HashMap;
use domain::{ActorId, FixedMoney, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct CrmAdapter {
    idempotency_ledger: HashMap<String, (FixedMoney, AdapterReceipt)>,
}

impl CrmAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn sync_opportunity(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "CRM opportunity sync cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "CRM management capability revoked".to_string(),
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
        if invocation.recipient.trim().is_empty() || !invocation.recipient.contains("crm-account") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "crm-account:<id>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        let amount = invocation.amount.unwrap_or(FixedMoney::ZERO);

        // Idempotency lookup
        if let Some((cached_amount, cached_receipt)) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            if *cached_amount != amount {
                return Err(AdapterReconciliationError::ChangedAmount {
                    expected: *cached_amount,
                    actual: amount,
                });
            }
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-crm-{}", invocation.operation_id),
            "task-crm-sync",
            expected_tenant,
            expected_caller,
            "crm:sync_opportunity",
            &invocation.idempotency_key,
            &format!("ext-opp-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:crm-synced",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), (amount, receipt.clone()));
        Ok(receipt)
    }
}
