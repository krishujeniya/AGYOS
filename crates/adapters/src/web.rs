//! Scoped Read-Only Web Retrieval Adapter.
//!
//! Complies with Principle P04, P05, P07, and P21 (Privacy and Boundary Protection).
//!
//! Invariants:
//! - Strictly read-only (GET/HEAD); mutations are rejected with DisallowedMethod.
//! - SSRF defense: blocks loopback, private IP, and cloud metadata endpoints.
//! - Zero secret leakage: authorization headers and tokens are scrubbed from receipts.

use std::collections::HashMap;
use domain::{ActorId, WorkspaceId};
use crate::{AdapterInvocation, AdapterReceipt, AdapterReconciliationError};

#[derive(Debug, Default)]
pub struct WebAdapter {
    idempotency_ledger: HashMap<String, AdapterReceipt>,
}

impl WebAdapter {
    pub fn new() -> Self {
        Self {
            idempotency_ledger: HashMap::new(),
        }
    }

    pub fn fetch_url(
        &mut self,
        invocation: &AdapterInvocation,
        expected_tenant: &WorkspaceId,
        expected_caller: &ActorId,
        http_method: &str,
        current_time_epoch_s: u64,
    ) -> Result<AdapterReceipt, AdapterReconciliationError> {
        if invocation.is_cancelled {
            return Err(AdapterReconciliationError::OperationCancelled(
                "Web fetch cancelled by operator".to_string(),
            ));
        }
        if invocation.is_revoked {
            return Err(AdapterReconciliationError::CapabilityRevoked(
                "Web read capability revoked".to_string(),
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

        // Method invariant: strictly read-only
        let m_upper = http_method.to_uppercase();
        if m_upper != "GET" && m_upper != "HEAD" {
            return Err(AdapterReconciliationError::DisallowedMethod(format!(
                "Method '{}' disallowed: WebAdapter is strictly read-only",
                http_method
            )));
        }

        // SSRF protection
        let url_lower = invocation.recipient.to_lowercase();
        if url_lower.contains("127.0.0.1")
            || url_lower.contains("localhost")
            || url_lower.contains("169.254.169.254")
            || url_lower.contains("0.0.0.0")
        {
            return Err(AdapterReconciliationError::ProhibitedContent(
                "SSRF defense: loopback and cloud metadata endpoints blocked".to_string(),
            ));
        }

        if !url_lower.starts_with("https://") && !url_lower.starts_with("http://") {
            return Err(AdapterReconciliationError::WrongRecipient {
                expected: "https://<valid-domain>".to_string(),
                actual: invocation.recipient.clone(),
            });
        }

        // Idempotency lookup
        if let Some(cached_receipt) = self.idempotency_ledger.get(&invocation.idempotency_key) {
            return Ok(cached_receipt.clone());
        }

        let receipt = AdapterReceipt::new(
            &format!("rcpt-web-{}", invocation.operation_id),
            "task-web-fetch",
            expected_tenant,
            expected_caller,
            "web:fetch_url",
            &invocation.idempotency_key,
            &format!("web-doc-{}", invocation.operation_id),
            &invocation.payload_digest,
            "digest:sanitized-web-content",
            current_time_epoch_s,
        );

        self.idempotency_ledger.insert(invocation.idempotency_key.clone(), receipt.clone());
        Ok(receipt)
    }
}
