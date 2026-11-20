//! Scoped Billing and Payment Disbursal Adapter.
//!
//! Complies with Principle P04, P05, P09, P10, and P11 (Idempotent Semantics).
//!
//! Invariants:
//! - Financial disbursements are strictly R3 external irreversible actions.
//! - A changed amount with the same idempotency key produces ZERO external effect
//!   and returns a hard ChangedAmount conflict error.
//! - Ambiguous receipts stop automatic execution until operator reconciliation.

use std::collections::HashMap;
use domain::{ActorId, FixedMoney, RiskTier, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct BillingAdapter {
    idempotency_ledger: HashMap<String, (FixedMoney, String, AdapterReceipt)>,
}

impl BillingAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn process_disbursement(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        is_gateway_ambiguous: bool,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Billing disbursement cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Billing disburse capability revoked".to_string(),
            ));
        }
        if invocation.risk_tier != RiskTier::R3 {
            return Err(AdapterReconciliationError::UnauthorizedRiskEscalation(
                "Billing disbursement requires R3 external irreversible authorization".to_string(),
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
        if !invocation.recipient.starts_with("stripe:acct_") && !invocation.recipient.starts_with("bank:iban_") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "stripe:acct_<id> or bank:iban_<id>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        let amount = invocation.amount.unwrap_or(FixedMoney::ZERO);

        // Strict idempotency verification
        if let Some((cached_amount, cached_recipient, cached_receipt)) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            if *cached_amount != amount {
                // Changed amount conflict: create ZERO further effect!
                return Err(AdapterReconciliationError::ChangedAmount {
                    expected: *cached_amount,
                    actual: amount,
                });
            }
            if cached_recipient != &invocation.recipient {
                return Err(AdapterReconciliationError::WrongRecipient {
                    expected: cached_recipient.clone(),
                    actual: invocation.recipient.clone(),
                });
            }
            return Ok(cached_receipt.clone());
        }

        // Gateway ambiguity check
        if is_gateway_ambiguous {
            return Err(AdapterReconciliationError::AmbiguousReceipt(format!(
                "Payment gateway returned unconfirmed receipt for key '{}'; zero side effects until reconciled",
                invocation.idempotency_key
            )));
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-bill-{}", invocation.operation_id),
            "task-billing-disburse",
            expected_tenant,
            expected_caller,
            "billing:disburse",
            &invocation.idempotency_key,
            &format!("stripe-tx-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:funds-transferred",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(
            invocation.idempotency_key.clone(),
            (amount, invocation.recipient.clone(), receipt.clone()),
        );

        Ok(receipt)
    }
}
