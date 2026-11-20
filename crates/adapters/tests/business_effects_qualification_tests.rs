//! Integration Test Suite for Scoped Business Effects and Adapter Qualification (Step 13).
//!
//! Complies with Step 13 finish test and Principles:
//! - P04 (Behavioral Contracts)
//! - P05 (Least Privilege & Complete Mediation)
//! - P06 (Traceable Provenance & W3C PROV Receipts)
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P11 (Idempotent Semantics - RFC 9110)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)
//! - P30 (Human Consent Authority)
//! - P32 (Operator-Owned Budgets)

use adapters::{
    AdapterInvocation, AdapterReconciliationError, BillingAdapter, CrmAdapter,
    GitAdapter, HelpdeskAdapter, HiringAdapter, LegalAdapter, ModelAdapter, WebAdapter,
};
use domain::{ActorId, FixedMoney, RiskTier, WorkspaceId};

fn create_test_invocation(
    op_id: &str,
    idempotency_key: &str,
    tenant: &WorkspaceId,
    caller: &ActorId,
    recipient: &str,
    amount: Option<FixedMoney>,
    risk: RiskTier,
    deadline_offset_s: u64,
) -> AdapterInvocation {
    AdapterInvocation {
        operation_id: op_id.to_string(),
        idempotency_key: idempotency_key.to_string(),
        tenant_id: tenant.clone(),
        caller_id: caller.clone(),
        recipient: recipient.to_string(),
        deadline_epoch_s: 1_000_000 + deadline_offset_s,
        amount,
        payload_digest: format!("sha256:payload-{}", op_id),
        risk_tier: risk,
        is_cancelled: false,
        is_revoked: false,
    }
}

#[test]
fn test_crm_adapter_qualification() {
    let mut adapter = CrmAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-account-executive");

    let invocation = create_test_invocation(
        "crm-01",
        "idem-crm-01",
        &tenant,
        &caller,
        "crm-account:org-acme-123",
        Some(FixedMoney::from_dollars(5_000)),
        RiskTier::R1,
        300,
    );

    // 1. Valid execution in sandbox
    let receipt = adapter.sync_opportunity(&invocation, &tenant, &caller, 1_000_010)
        .expect("Valid CRM sync should succeed");
    assert_eq!(receipt.status, "CONFIRMED");
    assert_eq!(receipt.idempotency_key, "idem-crm-01");
    assert!(receipt.receipt.verified);

    // 2. Idempotent replay with identical key returns cached receipt
    let replay = adapter.sync_opportunity(&invocation, &tenant, &caller, 1_000_020)
        .expect("Replay should succeed idempotently");
    assert_eq!(replay, receipt);

    // 3. Changed amount on same idempotency key fails with ChangedAmount
    let mut changed_amount = invocation.clone();
    changed_amount.amount = Some(FixedMoney::from_dollars(6_000));
    let err_amount = adapter.sync_opportunity(&changed_amount, &tenant, &caller, 1_000_030);
    assert!(matches!(err_amount, Err(AdapterReconciliationError::ChangedAmount { .. })));

    // 4. Cross-tenant rejection
    let foreign_tenant = WorkspaceId::new("workspace-tenant-b");
    let err_tenant = adapter.sync_opportunity(&invocation, &foreign_tenant, &caller, 1_000_010);
    assert!(matches!(err_tenant, Err(AdapterReconciliationError::TenantMismatch { .. })));

    // 5. Wrong recipient rejection
    let mut wrong_recip = invocation.clone();
    wrong_recip.idempotency_key = "idem-crm-02".to_string();
    wrong_recip.recipient = "unverified-email@evil.com".to_string();
    let err_recip = adapter.sync_opportunity(&wrong_recip, &tenant, &caller, 1_000_010);
    assert!(matches!(err_recip, Err(AdapterReconciliationError::WrongRecipient { .. })));

    // 6. Monotonic deadline expiration
    let err_deadline = adapter.sync_opportunity(&invocation, &tenant, &caller, 1_000_500);
    assert!(matches!(err_deadline, Err(AdapterReconciliationError::DeadlineExpired { .. })));

    // 7. Cancellation and revocation
    let mut cancelled = invocation.clone();
    cancelled.idempotency_key = "idem-crm-03".to_string();
    cancelled.is_cancelled = true;
    assert!(matches!(adapter.sync_opportunity(&cancelled, &tenant, &caller, 1_000_010), Err(AdapterReconciliationError::OperationCancelled(_))));

    let mut revoked = invocation.clone();
    revoked.idempotency_key = "idem-crm-04".to_string();
    revoked.is_revoked = true;
    assert!(matches!(adapter.sync_opportunity(&revoked, &tenant, &caller, 1_000_010), Err(AdapterReconciliationError::CapabilityRevoked(_))));
}

#[test]
fn test_helpdesk_adapter_qualification() {
    let mut adapter = HelpdeskAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-support-engineer");

    let invocation = create_test_invocation(
        "hd-01",
        "idem-hd-01",
        &tenant,
        &caller,
        "ticket:inc-8842",
        None,
        RiskTier::R1,
        300,
    );

    // 1. Valid triage execution
    let receipt = adapter.triage_ticket(&invocation, &tenant, &caller, 1_000_010)
        .expect("Valid ticket triage should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 2. Idempotent replay
    let replay = adapter.triage_ticket(&invocation, &tenant, &caller, 1_000_020)
        .expect("Idempotent replay should succeed");
    assert_eq!(replay, receipt);

    // 3. Recipient verification
    let mut wrong_recip = invocation.clone();
    wrong_recip.idempotency_key = "idem-hd-02".to_string();
    wrong_recip.recipient = "random-chat-room".to_string();
    assert!(matches!(adapter.triage_ticket(&wrong_recip, &tenant, &caller, 1_000_010), Err(AdapterReconciliationError::WrongRecipient { .. })));

    // 4. Cancellation & revocation
    let mut cancelled = invocation.clone();
    cancelled.idempotency_key = "idem-hd-03".to_string();
    cancelled.is_cancelled = true;
    assert!(matches!(adapter.triage_ticket(&cancelled, &tenant, &caller, 1_000_010), Err(AdapterReconciliationError::OperationCancelled(_))));
}

#[test]
fn test_billing_adapter_qualification() {
    let mut adapter = BillingAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-corporate-controller");

    let invocation = create_test_invocation(
        "bill-01",
        "idem-bill-01",
        &tenant,
        &caller,
        "stripe:acct_1M2N3P4Q",
        Some(FixedMoney::from_dollars(1_250)),
        RiskTier::R3, // Strict R3
        300,
    );

    // 1. Unauthorized risk tier (R1 attempted for billing disburse) must be rejected
    let mut low_risk = invocation.clone();
    low_risk.risk_tier = RiskTier::R1;
    let err_risk = adapter.process_disbursement(&low_risk, &tenant, &caller, false, 1_000_010);
    assert!(matches!(err_risk, Err(AdapterReconciliationError::UnauthorizedRiskEscalation(_))));

    // 2. Valid R3 execution
    let receipt = adapter.process_disbursement(&invocation, &tenant, &caller, false, 1_000_010)
        .expect("Valid billing disbursement should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 3. Changed amount on same idempotency key fails with ChangedAmount and produces ZERO further effect
    let mut changed_amount = invocation.clone();
    changed_amount.amount = Some(FixedMoney::from_dollars(1_500));
    let err_amount = adapter.process_disbursement(&changed_amount, &tenant, &caller, false, 1_000_020);
    assert!(matches!(err_amount, Err(AdapterReconciliationError::ChangedAmount { .. })));

    // 4. Wrong recipient account
    let mut wrong_recip = invocation.clone();
    wrong_recip.idempotency_key = "idem-bill-02".to_string();
    wrong_recip.recipient = "paypal:unverified_account".to_string();
    let err_recip = adapter.process_disbursement(&wrong_recip, &tenant, &caller, false, 1_000_010);
    assert!(matches!(err_recip, Err(AdapterReconciliationError::WrongRecipient { .. })));

    // 5. Ambiguous gateway receipt stops execution until reconciled
    let mut ambiguous_call = invocation.clone();
    ambiguous_call.idempotency_key = "idem-bill-03".to_string();
    let err_ambig = adapter.process_disbursement(&ambiguous_call, &tenant, &caller, true, 1_000_010);
    assert!(matches!(err_ambig, Err(AdapterReconciliationError::AmbiguousReceipt(_))));
}

#[test]
fn test_legal_adapter_qualification() {
    let mut adapter = LegalAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-general-counsel");

    let invocation = create_test_invocation(
        "legal-01",
        "idem-legal-01",
        &tenant,
        &caller,
        "jurisdiction:US-CA",
        None,
        RiskTier::R2,
        300,
    );

    // 1. Valid contract review
    let receipt = adapter.review_contract(
        &invocation,
        &tenant,
        &caller,
        "Standard mutual NDA with 2-year confidentiality term and Delaware choice of law",
        1_000_010,
    ).expect("Valid contract review should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 2. Unlimited liability indemnity clause strictly blocked
    let mut bad_clause_call = invocation.clone();
    bad_clause_call.idempotency_key = "idem-legal-02".to_string();
    let err_clause = adapter.review_contract(
        &bad_clause_call,
        &tenant,
        &caller,
        "Vendor shall provide unlimited liability indemnity for all consequential losses",
        1_000_010,
    );
    assert!(matches!(err_clause, Err(AdapterReconciliationError::ProhibitedContent(_))));

    // 3. Invalid jurisdiction recipient
    let mut bad_jur = invocation.clone();
    bad_jur.idempotency_key = "idem-legal-03".to_string();
    bad_jur.recipient = "offshore-unregulated-zone".to_string();
    assert!(matches!(
        adapter.review_contract(&bad_jur, &tenant, &caller, "Standard terms", 1_000_010),
        Err(AdapterReconciliationError::WrongRecipient { .. })
    ));
}

#[test]
fn test_hiring_adapter_qualification() {
    let mut adapter = HiringAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-hr-business-partner");

    let invocation = create_test_invocation(
        "hire-01",
        "idem-hire-01",
        &tenant,
        &caller,
        "candidate:cand-9912",
        None,
        RiskTier::R1,
        300,
    );

    // 1. Valid hiring candidate evaluation
    let receipt = adapter.evaluate_candidate(
        &invocation,
        &tenant,
        &caller,
        "Technical systems architecture rubric: concurrency, API design, testing discipline",
        1_000_010,
    ).expect("Valid hiring evaluation should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 2. Protected demographic traits inquiry strictly prohibited (P21)
    let mut bad_rubric_call = invocation.clone();
    bad_rubric_call.idempotency_key = "idem-hire-02".to_string();
    let err_demo = adapter.evaluate_candidate(
        &bad_rubric_call,
        &tenant,
        &caller,
        "Inquire regarding protected demographic traits and family plans",
        1_000_010,
    );
    assert!(matches!(err_demo, Err(AdapterReconciliationError::ProhibitedContent(_))));
}

#[test]
fn test_git_adapter_qualification() {
    let mut adapter = GitAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-staff-engineer");

    let invocation = create_test_invocation(
        "git-01",
        "idem-git-01",
        &tenant,
        &caller,
        "refs/tags/v1.0.0",
        None,
        RiskTier::R3,
        300,
    );

    // 1. Single main branch invariant: feature branches rejected!
    let err_branch = adapter.publish_release_tag(
        &invocation,
        &tenant,
        &caller,
        "feature/cool-idea",
        "commit-sha-abc-123",
        1_000_010,
    );
    assert!(matches!(err_branch, Err(AdapterReconciliationError::WrongRecipient { .. })));

    // 2. Valid publication to main branch
    let receipt = adapter.publish_release_tag(
        &invocation,
        &tenant,
        &caller,
        "main",
        "commit-sha-abc-123",
        1_000_010,
    ).expect("Valid release tagging on main should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 3. Repeated publication on same tag with identical commit returns cached receipt idempotently
    let replay = adapter.publish_release_tag(
        &invocation,
        &tenant,
        &caller,
        "main",
        "commit-sha-abc-123",
        1_000_020,
    ).expect("Identical re-publication should succeed idempotently");
    assert_eq!(replay, receipt);

    // 4. Repeated publication with conflicting commit SHA fails with RepeatedPublicationAttempt!
    let mut conflict_call = invocation.clone();
    conflict_call.idempotency_key = "idem-git-02".to_string();
    let err_conflict = adapter.publish_release_tag(
        &conflict_call,
        &tenant,
        &caller,
        "main",
        "commit-sha-def-999", // conflicting commit on same tag v1.0.0!
        1_000_030,
    );
    assert!(matches!(err_conflict, Err(AdapterReconciliationError::RepeatedPublicationAttempt(_))));
}

#[test]
fn test_model_adapter_qualification() {
    let mut adapter = ModelAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-ai-product-engineer");

    let invocation = create_test_invocation(
        "model-01",
        "idem-model-01",
        &tenant,
        &caller,
        "model:google/gemini-2.0-flash",
        Some(FixedMoney::from_micros(1_200)),
        RiskTier::R0,
        300,
    );

    // 1. Valid model inference
    let receipt = adapter.invoke_model(&invocation, &tenant, &caller, 1_000_010)
        .expect("Valid model invocation should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 2. Deadline expiration
    let err_timeout = adapter.invoke_model(&invocation, &tenant, &caller, 1_000_400);
    assert!(matches!(err_timeout, Err(AdapterReconciliationError::DeadlineExpired { .. })));

    // 3. Idempotent replay
    let replay = adapter.invoke_model(&invocation, &tenant, &caller, 1_000_020)
        .expect("Idempotent replay should succeed");
    assert_eq!(replay, receipt);
}

#[test]
fn test_web_adapter_qualification() {
    let mut adapter = WebAdapter::new();
    let tenant = WorkspaceId::new("workspace-tenant-a");
    let caller = ActorId::new("role-market-researcher");

    let invocation = create_test_invocation(
        "web-01",
        "idem-web-01",
        &tenant,
        &caller,
        "https://api.github.com/repos/krishujeniya/AGYOS",
        None,
        RiskTier::R0,
        300,
    );

    // 1. Valid read-only GET fetch
    let receipt = adapter.fetch_url(&invocation, &tenant, &caller, "GET", 1_000_010)
        .expect("Valid GET fetch should succeed");
    assert_eq!(receipt.status, "CONFIRMED");

    // 2. Disallowed mutation methods (POST, PUT, DELETE)
    let err_post = adapter.fetch_url(&invocation, &tenant, &caller, "POST", 1_000_010);
    assert!(matches!(err_post, Err(AdapterReconciliationError::DisallowedMethod(_))));

    // 3. SSRF Protection: loopback and metadata IPs blocked
    let ssrf_targets = [
        "https://127.0.0.1:8080/admin",
        "http://localhost:3000/internal",
        "http://169.254.169.254/latest/meta-data/",
        "http://0.0.0.0:8000/keys",
    ];

    for ssrf_url in &ssrf_targets {
        let mut ssrf_invocation = invocation.clone();
        ssrf_invocation.idempotency_key = format!("idem-ssrf-{}", ssrf_url);
        ssrf_invocation.recipient = ssrf_url.to_string();
        let err_ssrf = adapter.fetch_url(&ssrf_invocation, &tenant, &caller, "GET", 1_000_010);
        assert!(matches!(err_ssrf, Err(AdapterReconciliationError::ProhibitedContent(_))), "SSRF target {} must be blocked", ssrf_url);
    }
}
