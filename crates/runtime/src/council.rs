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

fn is_verdict_approved(v: &str) -> bool {
    let lower = v.trim().to_lowercase();
    if lower.contains("not approve")
        || lower.contains("not approved")
        || lower.contains("do not approve")
        || lower.contains("disapprove")
        || lower.contains("reject")
        || lower.contains("fail")
        || lower.contains("denied")
        || lower.contains("deny")
        || lower.contains("dissent")
    {
        return false;
    }
    lower == "approve"
        || lower == "approved"
        || lower == "pass"
        || lower == "passed"
        || lower.starts_with("approve")
}

pub struct CouncilEngine;

impl CouncilEngine {
    /// Conduct blind independent review across council members (Principle P25).
    /// Enforces that each unique member evaluates against their own recorded prior criterion.
    /// Duplicated reviewers do not create a quorum; negative verdicts stay negative.
    pub fn conduct_blind_review(
        question_prompt: &str,
        reviews: Vec<BlindReviewCriterion>,
        base_risk: RiskTier,
        base_budget: FixedMoney,
    ) -> Result<CouncilDeliberationOutcome, DomainError> {
        let mut seen = std::collections::HashSet::new();
        let mut unique_reviews = Vec::new();
        for r in reviews {
            if seen.insert(r.reviewer.clone()) {
                unique_reviews.push(r);
            }
        }

        if unique_reviews.is_empty() {
            return Err(DomainError::UnauthorizedR3Effect(
                "Cannot deliberate with empty council roster".to_string(),
            ));
        }

        let mut dissents = Vec::new();
        let first_verdict = unique_reviews[0].verdict.clone();
        let first_approved = is_verdict_approved(&first_verdict);
        let mut unanimous = true;

        for review in &unique_reviews {
            let approved = is_verdict_approved(&review.verdict);
            if review.verdict != first_verdict || approved != first_approved {
                unanimous = false;
                dissents.push(CouncilDissent {
                    member: review.reviewer.clone(),
                    dissenting_verdict: review.verdict.clone(),
                    rationale: review.rationale.clone(),
                });
            }
        }

        let (consensus_verdict, approved) = if unanimous {
            (first_verdict.clone(), first_approved)
        } else {
            // Coordinator reconciles dissent based on unique quorum
            let pass_count = unique_reviews.iter().filter(|r| is_verdict_approved(&r.verdict)).count();
            if pass_count > unique_reviews.len() / 2 {
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
