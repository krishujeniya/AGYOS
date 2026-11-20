//! Integration Test Suite for Deliberation Councils, P27 Benchmark, and Model Policy (Step 12).
//!
//! Complies with Principle P25 (Selective Cognitive Forcing), P27 (Empirically Justified Councils),
//! P15 (Tail Amplification), P16 (Admission Control), and P32 (Operator-Owned Budgets).

use domain::{ActorId, FixedMoney, RiskTier};
use runtime::{
    AdmissionController, BlindReviewCriterion, CouncilEngine, ExecutionMode,
    ModelPolicyRouter, ModelTier, P27Arm, P27BenchmarkRunner,
};

#[test]
fn test_selective_cognitive_forcing_and_dissent_recording() {
    let reviewer_1 = ActorId::new("role-staff-engineer");
    let reviewer_2 = ActorId::new("role-security-engineer");
    let reviewer_3 = ActorId::new("role-database-reliability-eng");

    // Reviewers record prior criterion and preliminary verdict in private (Principle P25)
    let reviews = vec![
        BlindReviewCriterion {
            reviewer: reviewer_1,
            prior_criterion: "Must pass deterministic state machine and CAS checks".to_string(),
            verdict: "Approve".to_string(),
            confidence: 0.95,
            rationale: "CAS check passes monotonically".to_string(),
        },
        BlindReviewCriterion {
            reviewer: reviewer_2,
            prior_criterion: "Must not expose environment credentials or unvalidated parameters".to_string(),
            verdict: "Approve".to_string(),
            confidence: 0.98,
            rationale: "Zero leaked credentials verified".to_string(),
        },
        BlindReviewCriterion {
            reviewer: reviewer_3,
            prior_criterion: "Must include index on foreign key column to prevent table lock".to_string(),
            verdict: "Dissent: Missing index on tenant_id".to_string(),
            confidence: 0.90,
            rationale: "Migration lacks index on tenant_id creating potential lock risk".to_string(),
        },
    ];

    let base_risk = RiskTier::R2;
    let base_budget = FixedMoney::from_dollars(1);

    let outcome = CouncilEngine::conduct_blind_review(
        "Review database schema migration for multi-tenant billing",
        reviews,
        base_risk,
        base_budget,
    ).expect("Council deliberation should complete");

    assert_eq!(outcome.dissents.len(), 1, "Expected 1 recorded dissent");
    assert_eq!(outcome.dissents[0].member.as_str(), "role-database-reliability-eng");
    assert!(outcome.dissents[0].dissenting_verdict.contains("Missing index"));
    assert!(outcome.dissents[0].rationale.contains("lacks index"));
    assert_eq!(outcome.effective_risk_tier, RiskTier::R2);
    assert_eq!(outcome.authorized_spend, FixedMoney::from_dollars(1));
}

#[test]
fn test_council_cannot_increase_authority_or_budget() {
    // Invariant: A council CANNOT elevate RiskTier authority above base contract!
    let base_risk = RiskTier::R1;
    let attempted_elevation = RiskTier::R3;
    let result = CouncilEngine::enforce_authority_cap(base_risk, attempted_elevation);
    assert!(result.is_err(), "Council authority escalation from R1 to R3 must be rejected");

    let valid_authority = CouncilEngine::enforce_authority_cap(RiskTier::R2, RiskTier::R1);
    assert!(valid_authority.is_ok());

    // Invariant: A council CANNOT increase budget above base allocation!
    let base_budget = FixedMoney::from_dollars(1);
    let attempted_budget = FixedMoney::from_dollars(2);
    let budget_result = CouncilEngine::enforce_budget_cap(base_budget, attempted_budget);
    assert!(budget_result.is_err(), "Council budget escalation must be rejected");

    let valid_budget = CouncilEngine::enforce_budget_cap(base_budget, FixedMoney::from_micros(500_000));
    assert!(valid_budget.is_ok());
}

#[test]
fn test_model_policy_risk_tier_routing() {
    // R0 / R1 -> FastPathSingleAgent on FastTier
    let (mode_r0, tier_r0) = ModelPolicyRouter::select_execution_mode(RiskTier::R0);
    assert_eq!(mode_r0, ExecutionMode::FastPathSingleAgent);
    assert_eq!(tier_r0, ModelTier::FastTier);

    let (mode_r1, tier_r1) = ModelPolicyRouter::select_execution_mode(RiskTier::R1);
    assert_eq!(mode_r1, ExecutionMode::FastPathSingleAgent);
    assert_eq!(tier_r1, ModelTier::FastTier);

    // R2 / R3 -> CouncilWithIndependentChecker on DeliberationTier
    let (mode_r2, tier_r2) = ModelPolicyRouter::select_execution_mode(RiskTier::R2);
    assert_eq!(mode_r2, ExecutionMode::CouncilWithIndependentChecker);
    assert_eq!(tier_r2, ModelTier::DeliberationTier);

    let (mode_r3, tier_r3) = ModelPolicyRouter::select_execution_mode(RiskTier::R3);
    assert_eq!(mode_r3, ExecutionMode::CouncilWithIndependentChecker);
    assert_eq!(tier_r3, ModelTier::DeliberationTier);
}

#[test]
fn test_admission_control_with_10_percent_protected_headroom() {
    // Capacity 10 slots -> 1 slot strictly reserved for status / cancellation
    let mut admission = AdmissionController::new(10);
    assert_eq!(admission.reserved_control_slots, 1);
    assert_eq!(admission.available_standard_slots(), 9);

    // Fill up 9 standard slots
    for _ in 0..9 {
        assert!(admission.admit_standard_job().is_ok());
    }
    assert_eq!(admission.available_standard_slots(), 0);

    // 10th standard job must be rejected to protect control headroom (Principle P16)
    assert!(admission.admit_standard_job().is_err());

    // However, status / cancellation control operation CAN be admitted into protected slot!
    assert!(admission.admit_control_operation().is_ok());

    // Total saturation now blocks all further operations
    assert!(admission.admit_control_operation().is_err());
}

#[test]
fn test_the_four_p27_arms_comparative_benchmark_and_200_task_cohort() {
    // 1. High-risk task evaluation: Council delivers 98% defect catch rate vs 65% for Single Agent
    let hr_comp = P27BenchmarkRunner::evaluate_high_risk_task("task-sec-audit");
    assert_eq!(hr_comp.arm_results.len(), 4);
    let single_agent = &hr_comp.arm_results[1];
    let council = &hr_comp.arm_results[3];
    assert_eq!(single_agent.arm, P27Arm::SingleAgent);
    assert_eq!(council.arm, P27Arm::HumanPlusCouncil);
    assert!(council.defect_catch_rate > single_agent.defect_catch_rate, "Council must achieve superior defect detection on high-risk task");
    assert!(council.uncertainty < single_agent.uncertainty, "Council must yield lower residual uncertainty");

    // 2. Low-risk task evaluation: Single agent delivers high quality at 650ms vs 12,000ms for Council
    let lr_comp = P27BenchmarkRunner::evaluate_low_risk_task("task-doc-typo");
    let lr_single = &lr_comp.arm_results[1];
    let lr_council = &lr_comp.arm_results[3];
    assert!(lr_single.duration_ms < lr_council.duration_ms / 10, "Single agent must be >10x faster for low-risk task");
    assert!(lr_single.tokens_used < lr_council.tokens_used / 3, "Single agent must consume <1/3 tokens for low-risk task");
    assert!(lr_single.quality_score >= 0.90, "Single agent quality remains excellent for low-risk task");

    // 3. Paired cohort simulation of 200 tasks (Production Envelope requirement)
    let (mean_savings, mean_council_defect_rate, mean_single_agent_quality) = P27BenchmarkRunner::simulate_cohort(200);
    assert!(mean_savings >= 20.0, "Mean token savings across 200 paired tasks must be >= 20% (achieved {:.2}%)", mean_savings);
    assert!(mean_council_defect_rate >= 0.95, "Council defect detection rate on high-risk tasks must be >= 95%");
    assert!(mean_single_agent_quality >= 0.90, "Single agent quality on low-risk tasks must be >= 90%");
}
