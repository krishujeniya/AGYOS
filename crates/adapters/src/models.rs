//! Scoped Model Provider Adapter.
//!
//! Complies with Principle P04, P05, P15 (Tail Latency), and P32 (Operator Budgets).

use std::collections::HashMap;
use domain::{ActorId, FixedMoney, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct ModelAdapter {
    idempotency_ledger: HashMap<String, (FixedMoney, AdapterReceipt)>,
}

impl ModelAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn invoke_model(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Model invocation cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Model invocation capability revoked".to_string(),
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
        if !invocation.recipient.starts_with("model:") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "model:<provider>/<model_id>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        let token_cost = invocation.amount.unwrap_or(FixedMoney::ZERO);

        // Idempotency lookup
        if let Some((cached_cost, cached_receipt)) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            if *cached_cost != token_cost {
                return Err(AdapterReconciliationError::ChangedAmount {
                    expected: *cached_cost,
                    actual: token_cost,
                });
            }
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-model-{}", invocation.operation_id),
            "task-model-inference",
            expected_tenant,
            expected_caller,
            "model:invoke",
            &invocation.idempotency_key,
            &format!("completion-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:model-completion",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), (token_cost, receipt.clone()));
        Ok(receipt)
    }
}
