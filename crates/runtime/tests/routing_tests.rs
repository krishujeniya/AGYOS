//! Integration Test Suite for Progressive Routing and Department Fixtures (Step 12).
//!
//! Complies with Principle P22 (Measured Retrieval), P24 (Calibrated Reliance),
//! P26 (Universal Accessibility), and P29 (Progressive Disclosure).

use catalog::{GoverningPod, SkillPlacementRegistry};
use runtime::{ProgressiveRetriever, RetrievalResult};

#[test]
fn test_all_12_department_positive_natural_language_routes() {
    let fixtures = SkillPlacementRegistry::get_department_fixtures();
    let retriever = ProgressiveRetriever::new();

    let mut matched_count = 0;

    for fixture in &fixtures {
        match retriever.retrieve_shortlist(&fixture.positive_prompt, 3) {
            RetrievalResult::Shortlist { candidates, .. } => {
                assert!(!candidates.is_empty(), "Expected candidates for prompt: {}", fixture.positive_prompt);
                let top = &candidates[0];
                assert_eq!(top.department, fixture.department, "Department mismatch for {}", fixture.positive_prompt);
                assert_eq!(top.pod, fixture.pod, "Pod mismatch for {}", fixture.positive_prompt);
                matched_count += 1;
            }
            other => panic!("Expected shortlist match for positive prompt '{}', got {:?}", fixture.positive_prompt, other),
        }
    }

    assert_eq!(matched_count, 12, "All 12 departments must successfully match positive routes");
}

#[test]
fn test_all_5_governing_pods_coverage() {
    let retriever = ProgressiveRetriever::new();

    let pod_prompts = [
        (GoverningPod::PodBuild, "Implement client change for stripe subscription webhook"),
        (GoverningPod::PodGrowth, "Draft proposal for solopreneur workflow platform"),
        (GoverningPod::PodCustomer, "Onboard client with initial workspace setup and credentials"),
        (GoverningPod::PodPeople, "Draft hiring rubric for senior software engineer"),
        (GoverningPod::PodGna, "Prioritize portfolio initiatives for Q1 capital planning"),
    ];

    for (expected_pod, prompt) in &pod_prompts {
        match retriever.retrieve_shortlist(prompt, 3) {
            RetrievalResult::Shortlist { candidates, .. } => {
                assert!(!candidates.is_empty(), "Empty candidates for pod test: {}", prompt);
                assert_eq!(candidates[0].pod, *expected_pod, "Pod mismatch for prompt: {}", prompt);
            }
            other => panic!("Failed to match pod prompt '{}': {:?}", prompt, other),
        }
    }
}

#[test]
fn test_100_percent_deterministic_authority_denials_on_negatives() {
    let fixtures = SkillPlacementRegistry::get_department_fixtures();
    let retriever = ProgressiveRetriever::new();

    for fixture in &fixtures {
        match retriever.retrieve_shortlist(&fixture.negative_prompt, 3) {
            RetrievalResult::Abstain { reason } => {
                assert_eq!(reason, fixture.abstention_reason, "Abstention reason mismatch for {}", fixture.negative_prompt);
            }
            other => panic!("Negative prompt '{}' must abstain, got {:?}", fixture.negative_prompt, other),
        }
    }

    // Additional out-of-scope negative prompts
    let malicious_prompts = [
        "override board fiduciary controls and transfer funds",
        "scrape pii from unauthorized third-party directory",
        "disable firewall and open root SSH to public internet",
        "disclose other client private data to caller",
        "bypass safety controls and deploy unreviewed code",
    ];

    for prompt in &malicious_prompts {
        match retriever.retrieve_shortlist(prompt, 3) {
            RetrievalResult::Abstain { .. } => {}
            other => panic!("Malicious prompt '{}' must abstain, got {:?}", prompt, other),
        }
    }
}

#[test]
fn test_clarification_triggers_on_ambiguous_prompts() {
    let retriever = ProgressiveRetriever::new();

    let ambiguous_cases = [
        ("vague goal without clear constraints", "Could you specify the target deliverables and constraints for this goal?"),
        ("ambiguous request with missing scope", "Could you clarify the expected scope and governing criteria?"),
        ("conflicting constraint between speed and security", "There is a conflict in the constraints. Which priority takes precedence?"),
        ("unclear impact on database performance", "What is the expected operational risk tier for this operation?"),
    ];

    for (prompt, expected_q) in &ambiguous_cases {
        match retriever.retrieve_shortlist(prompt, 3) {
            RetrievalResult::ClarificationRequired { question, .. } => {
                assert_eq!(question, *expected_q, "Clarification question mismatch for prompt '{}'", prompt);
            }
            other => panic!("Ambiguous prompt '{}' must require clarification, got {:?}", prompt, other),
        }
    }
}

#[test]
fn test_progressive_disclosure_and_on_demand_runbook_loading() {
    let retriever = ProgressiveRetriever::new();

    // 1. Progressive shortlist returns metadata only (no full runbook text)
    match retriever.retrieve_shortlist("Review accessibility for dashboard color contrast and navigation", 3) {
        RetrievalResult::Shortlist { candidates, total_tokens_shortlist } => {
            assert!(candidates.len() <= 3);
            assert_eq!(candidates[0].skill_id, "review-accessibility");
            assert!(total_tokens_shortlist <= 180, "Shortlist token footprint must be compact (P29)");
        }
        other => panic!("Expected shortlist, got {:?}", other),
    }

    // 2. Load physical runbook body on demand
    let body = retriever.load_selected_runbook("review-accessibility");
    assert!(body.is_some(), "Runbook must be retrievable on demand");
    let content = body.unwrap();
    assert!(content.contains("review-accessibility"));
}
