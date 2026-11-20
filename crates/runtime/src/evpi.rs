//! Expected Value of Perfect Information (EVPI) and Socratic Intent Synthesis.
//!
//! Complies with Principle P28 (Decision Value Under Uncertainty - Howard, 1966),
//! P24 (Calibrated Reliance), P26 (One Question at a Time), and P30 (Human Consent Authority).
//!
//! Mathematical Formulation:
//! - Prior Uncertainty: U in [0.0, 1.0]
//! - Cost of Reversible Error: C_err (FixedMoney)
//! - Cost of Operator Interruption: C_clarify (FixedMoney)
//! - EVPI = U * C_err
//!
//! Decision Rules:
//! 1. Non-inferable Consent: R3 irreversible external effects or P21 privacy actions
//!    CANNOT be assumed by any EVPI calculation. Explicit consent is mandatory.
//! 2. If EVPI > C_clarify: Ask exactly ONE material question (P26) to resolve ambiguity.
//! 3. If EVPI <= C_clarify: Proceed with explicit, documented, reversible assumption.

use domain::{FixedMoney, RiskTier};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EvpiParameters {
    pub prior_uncertainty_pts: u32, // 0 to 10,000 basis points (0.00% to 100.00%)
    pub cost_of_error: FixedMoney,
    pub cost_of_clarification: FixedMoney,
}

impl EvpiParameters {
    pub fn new(uncertainty_pts: u32, cost_of_error: FixedMoney, cost_of_clarification: FixedMoney) -> Self {
        Self {
            prior_uncertainty_pts: uncertainty_pts.min(10_000),
            cost_of_error,
            cost_of_clarification,
        }
    }

    /// Calculate EVPI in FixedMoney micro-dollars.
    pub fn calculate_evpi(&self) -> FixedMoney {
        let err_micros = self.cost_of_error.as_micros();
        let evpi_micros = (err_micros * self.prior_uncertainty_pts as i64) / 10_000;
        FixedMoney::from_micros(evpi_micros)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ActionDecision {
    /// Clarification question required before proceeding.
    Clarify {
        question: String,
        evpi: FixedMoney,
        cost_of_clarification: FixedMoney,
    },
    /// Reversible assumption adopted; operator notified for optional correction.
    ProceedWithAssumption {
        assumption: String,
        evpi: FixedMoney,
        cost_of_clarification: FixedMoney,
    },
    /// Consequential irreversible action requiring explicit human consent (P30).
    RequestExplicitConsent {
        reason: String,
        risk_tier: RiskTier,
    },
}

pub struct EvpiEngine;

impl EvpiEngine {
    /// Evaluate task intent under uncertainty according to Howard (1966) EVPI.
    pub fn evaluate(
        risk: RiskTier,
        is_privacy_sensitive: bool,
        clarification_question: Option<&str>,
        default_assumption: &str,
        params: &EvpiParameters,
    ) -> ActionDecision {
        // Invariant 1: Consent can NEVER be inferred from an EVPI heuristic for R3 or sensitive operations
        if risk == RiskTier::R3 || is_privacy_sensitive {
            return ActionDecision::RequestExplicitConsent {
                reason: "Irreversible action or personal data processing requires explicit operator approval"
                    .to_string(),
                risk_tier: risk,
            };
        }

        let evpi = params.calculate_evpi();

        // Invariant 2: If expected value of information exceeds interruption cost, clarify!
        if evpi > params.cost_of_clarification {
            let question = clarification_question
                .unwrap_or("Could you clarify the specific constraints and acceptance criteria?")
                .to_string();
            ActionDecision::Clarify {
                question,
                evpi,
                cost_of_clarification: params.cost_of_clarification,
            }
        } else {
            // Invariant 3: Otherwise adopt safe reversible assumption and proceed
            ActionDecision::ProceedWithAssumption {
                assumption: default_assumption.to_string(),
                evpi,
                cost_of_clarification: params.cost_of_clarification,
            }
        }
    }
}
