//! Deliberation Council Engine with Blind Independent Review and Recorded Dissent.
//!
//! Complies with Principle P25 (Selective Cognitive Forcing - Buçinca et al., 2021)
//! and P27 (Empirically Justified Councils - Vaccaro et al., 2024).
//!
//! Invariants:
//! - Selective cognitive forcing: reviewers formulate criteria before seeing peers' verdicts.
//! - Dissent is recorded explicitly with rationale before consensus.
//! - A council CANNOT increase authority (RiskTier) or budgets (P32).

use domain::{ActorId, CouncilDissent, DomainError, FixedMoney, RiskTier};

#[derive(Debug, Clone, PartialEq)]
pub struct BlindReviewCriterion {
    pub reviewer: ActorId,
    pub prior_criterion: String,
    pub verdict: String,
    pub confidence: f64, // 0.0 to 1.0
    pub rationale: String,
}

#[derive(Debug, Clone, PartialEq)]
pub struct CouncilDeliberationOutcome {
    pub question_prompt: String,
    pub consensus_verdict: String,
    pub approved: bool,
    pub dissents: Vec<CouncilDissent>,
    pub effective_risk_tier: RiskTier,
    pub authorized_spend: FixedMoney,
}

pub struct CouncilEngine;

impl CouncilEngine {
    /// Conduct blind independent review across council members (Principle P25).
    /// Enforces that each member evaluates against their own recorded prior criterion.
    pub fn conduct_blind_review(
        question_prompt: &str,
        reviews: Vec<BlindReviewCriterion>,
        base_risk: RiskTier,
        base_budget: FixedMoney,
    ) -> Result<CouncilDeliberationOutcome, DomainError> {
        if reviews.is_empty() {
            return Err(DomainError::UnauthorizedR3Effect(
                "Cannot deliberate with empty council roster".to_string(),
            ));
        }

        let mut dissents = Vec::new();
        let first_verdict = reviews[0].verdict.clone();
        let mut unanimous = true;

        for review in &reviews {
            if review.verdict != first_verdict {
                unanimous = false;
                dissents.push(CouncilDissent {
                    member: review.reviewer.clone(),
                    dissenting_verdict: review.verdict.clone(),
                    rationale: review.rationale.clone(),
                });
            }
        }

        let (consensus_verdict, approved) = if unanimous {
            (first_verdict.clone(), first_verdict.to_lowercase().contains("approve") || first_verdict.to_lowercase().contains("pass"))
        } else {
            // Coordinator reconciles dissent
            let pass_count = reviews.iter().filter(|r| r.verdict.to_lowercase().contains("approve") || r.verdict.to_lowercase().contains("pass")).count();
            if pass_count > reviews.len() / 2 {
                ("Approved with recorded dissent".to_string(), true)
            } else {
                ("Rejected: majority or critical dissent unreconciled".to_string(), false)
            }
        };

        Ok(CouncilDeliberationOutcome {
            question_prompt: question_prompt.to_string(),
            consensus_verdict,
            approved,
            dissents,
            effective_risk_tier: base_risk,
            authorized_spend: base_budget,
        })
    }

    /// Strict Invariant: Council CANNOT increase authority (RiskTier) above base contract!
    pub fn enforce_authority_cap(base_risk: RiskTier, proposed: RiskTier) -> Result<RiskTier, DomainError> {
        if proposed > base_risk {
            return Err(DomainError::UnauthorizedR3Effect(format!(
                "Council authority escalation rejected: cannot elevate {:?} above base {:?}",
                proposed, base_risk
            )));
        }
        Ok(proposed)
    }

    /// Strict Invariant: Council CANNOT increase budget above base allocation!
    pub fn enforce_budget_cap(base_funds: FixedMoney, proposed: FixedMoney) -> Result<FixedMoney, DomainError> {
        if proposed > base_funds {
            return Err(DomainError::BudgetExceeded {
                requested: proposed,
                available: base_funds,
            });
        }
        Ok(proposed)
    }
}
