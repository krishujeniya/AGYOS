//! Integration Test Suite for EVPI Decision Making and Context Budgets (Step 12).
//!
//! Complies with Principle P28 (Howard 1966 EVPI), P24 (Calibrated Reliance),
//! P26 (One Question at a Time), and P32 (Operator-Owned Budgets).

use domain::{FixedMoney, RiskTier};
use runtime::{ActionDecision, ContextBudget, EvpiEngine, EvpiParameters, TokenSavingsEvaluator};

#[test]
fn test_evpi_calculation_and_clarification_decision() {
    // Case 1: High uncertainty (60.00% = 6,000 pts), Error cost = $10.00 (10,000,000 micros).
    // Interruption cost = $1.00 (1,000,000 micros).
    // EVPI = $10.00 * 0.60 = $6.00.
    // Since EVPI ($6.00) > Interruption ($1.00), engine MUST clarify (Principle P28).
    let params = EvpiParameters::new(
        6_000,
        FixedMoney::from_dollars(10),
        FixedMoney::from_dollars(1),
    );
    assert_eq!(params.calculate_evpi(), FixedMoney::from_dollars(6));

    let decision = EvpiEngine::evaluate(
        RiskTier::R1,
        false,
        Some("Which database column should be indexed?"),
        "Assume default primary key indexing",
        &params,
    );

    match decision {
        ActionDecision::Clarify { question, evpi, cost_of_clarification } => {
            assert_eq!(question, "Which database column should be indexed?");
            assert_eq!(evpi, FixedMoney::from_dollars(6));
            assert_eq!(cost_of_clarification, FixedMoney::from_dollars(1));
        }
        other => panic!("Expected Clarify decision, got {:?}", other),
    }

    // Case 2: Low uncertainty (5.00% = 500 pts), Error cost = $2.00 (2,000,000 micros).
    // Interruption cost = $1.00 (1,000,000 micros).
    // EVPI = $2.00 * 0.05 = $0.10.
    // Since EVPI ($0.10) <= Interruption ($1.00), engine proceeds with default assumption.
    let low_params = EvpiParameters::new(
        500,
        FixedMoney::from_dollars(2),
        FixedMoney::from_dollars(1),
    );
    assert_eq!(low_params.calculate_evpi(), FixedMoney::from_micros(100_000)); // $0.10

    let decision_low = EvpiEngine::evaluate(
        RiskTier::R1,
        false,
        Some("Which cache ttl to use?"),
        "Adopt standard 300s TTL cache assumption",
        &low_params,
    );

    match decision_low {
        ActionDecision::ProceedWithAssumption { assumption, evpi, .. } => {
            assert_eq!(assumption, "Adopt standard 300s TTL cache assumption");
            assert_eq!(evpi, FixedMoney::from_micros(100_000));
        }
        other => panic!("Expected ProceedWithAssumption, got {:?}", other),
    }
}

#[test]
fn test_evpi_consent_never_inferred_for_r3_or_privacy() {
    // Invariant: For R3 external irreversible effects or privacy actions, consent CANNOT be assumed
    // even if uncertainty is 0!
    let zero_uncertainty_params = EvpiParameters::new(
        0,
        FixedMoney::from_dollars(100),
        FixedMoney::from_dollars(10),
    );

    let decision_r3 = EvpiEngine::evaluate(
        RiskTier::R3,
        false,
        None,
        "Attempt to assume wire transfer approval",
        &zero_uncertainty_params,
    );

    match decision_r3 {
        ActionDecision::RequestExplicitConsent { reason, risk_tier } => {
            assert_eq!(risk_tier, RiskTier::R3);
            assert!(reason.contains("Irreversible action"));
        }
        other => panic!("R3 must require explicit consent, got {:?}", other),
    }

    // Sensitive privacy data processing
    let decision_privacy = EvpiEngine::evaluate(
        RiskTier::R1,
        true, // is_privacy_sensitive
        None,
        "Attempt to assume PII processing consent",
        &zero_uncertainty_params,
    );

    match decision_privacy {
        ActionDecision::RequestExplicitConsent { reason, .. } => {
            assert!(reason.contains("personal data processing"));
        }
        other => panic!("Privacy action must require explicit consent, got {:?}", other),
    }
}

#[test]
fn test_context_budget_ceiling_and_20_percent_reserve_invariants() {
    let mut budget = ContextBudget::default_contract_ceiling();

    assert_eq!(budget.max_tokens, 30_000);
    assert_eq!(budget.token_recovery_reserve(), 6_000); // 20%
    assert_eq!(budget.spendable_token_limit(), 24_000); // 80%
    assert_eq!(budget.available_tokens(), 24_000);

    // Allocate valid tokens
    assert!(budget.allocate_tokens(10_000).is_ok());
    assert_eq!(budget.available_tokens(), 14_000);

    // Attempting to consume recovery reserve must fail immediately!
    assert!(budget.allocate_tokens(15_000).is_err());

    // Allocate remaining spendable exactly
    assert!(budget.allocate_tokens(14_000).is_ok());
    assert_eq!(budget.available_tokens(), 0);

    // Any further allocation rejected
    assert!(budget.allocate_tokens(1).is_err());

    // Financial recovery reserve
    assert_eq!(budget.max_money, FixedMoney::from_micros(1_500_000)); // $1.50
    assert_eq!(budget.money_recovery_reserve(), FixedMoney::from_micros(300_000)); // $0.30 (20%)
    assert_eq!(budget.spendable_money_limit(), FixedMoney::from_micros(1_200_000)); // $1.20

    // Tool call ceiling & reserve (40 max, 8 reserved, 32 spendable)
    assert_eq!(budget.spendable_tool_call_limit(), 32);
    for _ in 0..32 {
        assert!(budget.record_tool_call().is_ok());
    }
    // 33rd tool call breaches recovery reserve!
    assert!(budget.record_tool_call().is_err());
}

#[test]
fn test_p22_measured_token_savings_threshold() {
    // Progressive TOON retrieval (shortlist + single runbook) vs monolithic raw context
    let raw_monolithic_tokens = 5_000;
    let toon_progressive_tokens = 1_250;

    let savings = TokenSavingsEvaluator::calculate_savings_percentage(raw_monolithic_tokens, toon_progressive_tokens);
    assert_eq!(savings, 75.0, "Progressive TOON retrieval achieves 75% token reduction");
    assert!(TokenSavingsEvaluator::satisfies_p22_threshold(raw_monolithic_tokens, toon_progressive_tokens));

    // Verify 20% threshold edge
    assert!(TokenSavingsEvaluator::satisfies_p22_threshold(1_000, 800)); // exactly 20%
    assert!(!TokenSavingsEvaluator::satisfies_p22_threshold(1_000, 850)); // 15% < 20%
}
