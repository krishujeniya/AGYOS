//! AGYOS Scoped Business Effects and Adapter Qualification Engine.
//!
//! Complies with Step 13: Qualify business effects, and Principles:
//! - P04 (Behavioral Contracts & Versioned Semantics)
//! - P05 (Least Privilege, Complete Mediation & Fail-Safe Defaults)
//! - P06 (Traceable Provenance & W3C PROV Receipts)
//! - P09 (Explicit State & Invariant Checks)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics - RFC 9110)
//! - P20 (End-to-End Observability)
//! - P21 (Purpose Limitation & Privacy Boundaries)
//! - P30 (Human Consent & Revocation)
//! - P32 (Operator-Owned Budgets)

pub mod billing;
pub mod crm;
pub mod git;
pub mod helpdesk;
pub mod hiring;
pub mod legal;
pub mod models;
pub mod web;

use domain::{ActorId, FixedMoney, Receipt, ReceiptId, RiskTier, TaskId, WorkspaceId};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AdapterCapability {
    CrmManage,
    HelpdeskTriage,
    BillingDisburse,
    LegalReview,
    HiringScreen,
    GitPublish,
    ModelInvoke,
    WebRead,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdapterInvocation {
    pub operation_id: String,
    pub idempotency_key: String,
    pub tenant_id: WorkspaceId,
    pub caller_id: ActorId,
    pub recipient: String,
    pub deadline_epoch_s: u64,
    pub amount: Option<FixedMoney>,
    pub payload_digest: String,
    pub risk_tier: RiskTier,
    pub is_cancelled: bool,
    pub is_revoked: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AdapterReconciliationError {
    IdentityMismatch { expected: ActorId, actual: ActorId },
    TenantMismatch { expected: WorkspaceId, actual: WorkspaceId },
    WrongRecipient { expected: String, actual: String },
    DeadlineExpired { deadline: u64, current: u64 },
    ChangedAmount { expected: FixedMoney, actual: FixedMoney },
    RepeatedPublicationAttempt(String),
    AmbiguousReceipt(String),
    CapabilityRevoked(String),
    OperationCancelled(String),
    UnauthorizedRiskEscalation(String),
    DisallowedMethod(String),
    ProhibitedContent(String),
}

impl std::fmt::Display for AdapterReconciliationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::IdentityMismatch { expected, actual } => {
                write!(f, "Caller identity mismatch: expected {}, got {}", expected, actual)
            }
            Self::TenantMismatch { expected, actual } => {
                write!(f, "Tenant boundary mismatch: expected {}, got {}", expected, actual)
            }
            Self::WrongRecipient { expected, actual } => {
                write!(f, "Wrong recipient: expected '{}', got '{}'", expected, actual)
            }
            Self::DeadlineExpired { deadline, current } => {
                write!(f, "Operation deadline expired: deadline {}s, current {}s", deadline, current)
            }
            Self::ChangedAmount { expected, actual } => {
                write!(f, "Idempotency conflict on changed amount: expected ${:.4}, got ${:.4}", expected.as_f64(), actual.as_f64())
            }
            Self::RepeatedPublicationAttempt(msg) => write!(f, "Repeated publication attempt: {}", msg),
            Self::AmbiguousReceipt(msg) => write!(f, "Ambiguous receipt requires reconciliation: {}", msg),
            Self::CapabilityRevoked(msg) => write!(f, "Capability revoked: {}", msg),
            Self::OperationCancelled(msg) => write!(f, "Operation cancelled before execution: {}", msg),
            Self::UnauthorizedRiskEscalation(msg) => write!(f, "Unauthorized risk tier: {}", msg),
            Self::DisallowedMethod(msg) => write!(f, "Disallowed method: {}", msg),
            Self::ProhibitedContent(msg) => write!(f, "Prohibited content detected: {}", msg),
        }
    }
}

impl std::error::Error for AdapterReconciliationError {}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AdapterReceipt {
    pub receipt: Receipt,
    pub idempotency_key: String,
    pub external_reference: String,
    pub status: String,
}

impl AdapterReceipt {
    pub fn new(
        receipt_id: &str,
        task_id: &str,
        tenant_id: &WorkspaceId,
        caller_id: &ActorId,
        action: &str,
        idempotency_key: &str,
        external_ref: &str,
        input_digest: &str,
        output_digest: &str,
        timestamp: u64,
    ) -> Self {
        Self {
            receipt: Receipt {
                id: ReceiptId::new(receipt_id),
                task_id: TaskId::new(task_id),
                workspace_id: tenant_id.clone(),
                actor_id: caller_id.clone(),
                action: action.to_string(),
                input_digest: input_digest.to_string(),
                output_digest: output_digest.to_string(),
                timestamp_epoch_s: timestamp,
                verified: true,
            },
            idempotency_key: idempotency_key.to_string(),
            external_reference: external_ref.to_string(),
            status: "CONFIRMED".to_string(),
        }
    }
}

pub use billing::BillingAdapter;
pub use crm::CrmAdapter;
pub use git::GitAdapter;
pub use helpdesk::HelpdeskAdapter;
pub use hiring::HiringAdapter;
pub use legal::LegalAdapter;
pub use models::ModelAdapter;
pub use web::WebAdapter;
