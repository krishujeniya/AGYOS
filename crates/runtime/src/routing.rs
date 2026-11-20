//! Progressive Context Retrieval and Multi-Department Intent Routing.
//!
//! Complies with Principle P22 (Measured Context Retrieval - Liu et al., TACL 2024),
//! P24 (Calibrated Reliance), P26 (Universal Accessibility), and P29 (Progressive Disclosure).
//!
//! Invariants:
//! - Progressive disclosure: shortlists candidate metadata before loading runbooks.
//! - Deterministic abstention on prohibited, malicious, or ambiguous negatives.
//! - Natural language routing covers all 12 departments and 5 pods.

use catalog::{
    CanonicalSkill, Department, GoverningPod, RouteEvaluationResult, SkillPlacementRegistry,
};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, PartialEq)]
pub struct CandidateSkillMatch {
    pub skill_id: String,
    pub home: String,
    pub department: Department,
    pub pod: GoverningPod,
    pub relevance_score: f64,
    pub matching_label: String,
}

#[derive(Debug, Clone, PartialEq)]
pub enum RetrievalResult {
    Shortlist {
        candidates: Vec<CandidateSkillMatch>,
        total_tokens_shortlist: usize,
    },
    ClarificationRequired {
        prompt: String,
        question: String,
    },
    Abstain {
        reason: String,
    },
}

pub struct ProgressiveRetriever {
    skills: Vec<CanonicalSkill>,
}

impl ProgressiveRetriever {
    pub fn new() -> Self {
        Self {
            skills: SkillPlacementRegistry::load_required_153(),
        }
    }

    /// Retrieve candidate shortlist using progressive disclosure (Principle P29).
    /// Does not load the full runbook bodies; only returns ranked candidate cards.
    pub fn retrieve_shortlist(&self, prompt: &str, limit: usize) -> RetrievalResult {
        // First check abstention and clarification gates
        match SkillPlacementRegistry::evaluate_natural_language_route(prompt) {
            RouteEvaluationResult::Abstain { reason } => {
                return RetrievalResult::Abstain { reason };
            }
            RouteEvaluationResult::ClarificationRequired { prompt, question } => {
                return RetrievalResult::ClarificationRequired { prompt, question };
            }
            RouteEvaluationResult::Matched { .. } => {
                // Proceed to score and rank candidates
            }
        }

        let p_lower = prompt.to_lowercase();
        let prompt_tokens: Vec<&str> = p_lower
            .split(|c: char| !c.is_alphanumeric() && c != '-')
            .filter(|s| !s.is_empty())
            .collect();

        let mut scored: Vec<CandidateSkillMatch> = Vec::new();

        for skill in &self.skills {
            let mut highest_score = 0.0;
            let mut best_label = String::new();

            for label in &skill.route_labels {
                let l_lower = label.to_lowercase();
                let score = Self::calculate_match_score(&p_lower, &prompt_tokens, &l_lower);
                if score > highest_score {
                    highest_score = score;
                    best_label = label.clone();
                }
            }

            if highest_score > 0.15 {
                scored.push(CandidateSkillMatch {
                    skill_id: skill.id.clone(),
                    home: skill.home.clone(),
                    department: skill.department,
                    pod: skill.pod,
                    relevance_score: highest_score,
                    matching_label: best_label,
                });
            }
        }

        // Sort descending by score
        scored.sort_by(|a, b| b.relevance_score.partial_cmp(&a.relevance_score).unwrap_or(std::cmp::Ordering::Equal));

        let top_candidates: Vec<CandidateSkillMatch> = scored.into_iter().take(limit.max(1)).collect();

        // Estimated tokens for shortlist metadata (~60 tokens per candidate card vs ~1,200 per full runbook)
        let total_tokens_shortlist = top_candidates.len() * 60;

        RetrievalResult::Shortlist {
            candidates: top_candidates,
            total_tokens_shortlist,
        }
    }

    /// On-demand loading of single runbook body after progressive shortlist acceptance (Principle P22).
    pub fn load_selected_runbook(&self, skill_id: &str) -> Option<String> {
        let skill = self.skills.iter().find(|s| s.id == skill_id)?;
        let path = Path::new(&skill.canonical_path);
        if path.exists() {
            fs::read_to_string(path).ok()
        } else {
            // Synthesize minimal TOON runbook representation if file not on local disk
            Some(format!(
                "skill:\n  id: \"{}\"\n  home: \"{}\"\n  department: \"{:?}\"\n  pod: \"{:?}\"\n",
                skill.id, skill.home, skill.department, skill.pod
            ))
        }
    }

    fn calculate_match_score(prompt: &str, prompt_tokens: &[&str], label: &str) -> f64 {
        if prompt.contains(label) {
            return 1.0 + (label.len() as f64 / 100.0);
        }

        let label_tokens: Vec<&str> = label.split_whitespace().collect();
        if label_tokens.is_empty() {
            return 0.0;
        }

        let mut matches = 0;
        for lt in &label_tokens {
            if prompt_tokens.iter().any(|pt| pt.contains(lt) || lt.contains(pt)) {
                matches += 1;
            }
        }

        (matches as f64) / (label_tokens.len() as f64)
    }
}

impl Default for ProgressiveRetriever {
    fn default() -> Self {
        Self::new()
    }
}
