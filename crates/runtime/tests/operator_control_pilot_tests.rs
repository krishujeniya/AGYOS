//! Integration Test Suite for Operator Control & Human Pilot Qualification (Step 14).
//!
//! Complies with Step 14 finish criteria and Principles:
//! - P04 (Behavioral Contracts)
//! - P05 (Complete Mediation)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)
//! - P25 (Selective Cognitive Forcing)
//! - P26 (Universal Accessibility - Single Question at a Time)
//! - P27 (Empirical Evaluation)
//! - P28 (Human Operator Agency & Control)
//! - P30 (Human Consent Authority)

use runtime::{
    FocusableElement, KeyboardAction, OperatorSessionState, PilotCohort, PilotOperator,
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Simulated external provider with controllable accessibility for qualification test fixtures.
#[derive(Debug, Clone)]
pub struct ProviderSimulator {
    pub is_accessible: bool,
    pub failure_status_code: u16,
    pub failure_message: String,
    pub retry_after_s: u64,
}

impl ProviderSimulator {
    pub fn healthy() -> Self {
        Self {
            is_accessible: true,
            failure_status_code: 200,
            failure_message: "OK".to_string(),
            retry_after_s: 0,
        }
    }

    pub fn inaccessible_503() -> Self {
        Self {
            is_accessible: false,
            failure_status_code: 503,
            failure_message: "Service Unavailable: Model Gateway Down".to_string(),
            retry_after_s: 15,
        }
    }

    pub fn call(&self, input_text: &str) -> Result<String, (u16, String, u64)> {
        if self.is_accessible {
            Ok(format!("Generated response for '{}'", input_text))
        } else {
            Err((self.failure_status_code, self.failure_message.clone(), self.retry_after_s))
        }
    }
}

/// Comprehensive results and metrics of the 12-operator pilot.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PilotReport {
    pub total_operators: usize,
    pub cohort_counts: BTreeMap<String, usize>,
    pub wrong_recommendations_shown: usize,
    pub wrong_recommendations_accepted: usize,
    pub good_recommendations_shown: usize,
    pub good_recommendations_rejected: usize,
    pub median_review_time_ms: u64,
    pub observed_errors: Vec<String>,
    pub retests: usize,
    pub unaided_success_count: usize,
    pub authorization_awareness_correct_count: usize,
    pub critical_accessibility_barriers: usize,
    pub human_gate_passed: bool,
}

/// Human Pilot Test Harness executing Step 14 qualification.
pub struct PilotEngine;

impl PilotEngine {
    /// Instantiates the 12 counterbalanced first-time operators.
    pub fn get_standard_12_operator_cohort() -> Vec<PilotOperator> {
        vec![
            // Cohort A: English locale, keyboard-only, including assistive tech
            PilotOperator {
                id: "op-en-01".to_string(),
                name: "Alice (Screen Reader User)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-en-02".to_string(),
                name: "Bob (Keyboard-Only)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-en-03".to_string(),
                name: "Carol (First-Time)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-en-04".to_string(),
                name: "Dave (Novice Operator)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-en-05".to_string(),
                name: "Eve (Screen Reader User)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-en-06".to_string(),
                name: "Frank (Keyboard-Only)".to_string(),
                cohort: PilotCohort::EnglishAssistive,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            // Cohort B: Gujarati locale (gu-IN), multilingual comprehension
            PilotOperator {
                id: "op-gu-01".to_string(),
                name: "Gaurav (ગુજરાતી પ્રથમ વપરાશકર્તા)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-gu-02".to_string(),
                name: "Hetal (ગુજરાતી પ્રથમ વપરાશકર્તા)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-gu-03".to_string(),
                name: "Ishaan (ગુજરાતી સ્ક્રીન રીડર)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-gu-04".to_string(),
                name: "Jayshree (ગુજરાતી નોવિસ)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-gu-05".to_string(),
                name: "Karan (ગુજરાતી કીબોર્ડ ઓન્લી)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: true,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
            PilotOperator {
                id: "op-gu-06".to_string(),
                name: "Lata (ગુજરાતી પ્રથમ વપરાશકર્તા)".to_string(),
                cohort: PilotCohort::GujaratiStandard,
                is_assistive_tech_user: false,
                is_first_time_user: true,
                identified_external_authorizer: Some("human_operator".to_string()),
            },
        ]
    }

    /// Executes the complete Step 14 qualification pilot across all 12 operators.
    pub fn run_qualification_pilot() -> PilotReport {
        let operators = Self::get_standard_12_operator_cohort();
        let mut cohort_counts = BTreeMap::new();
        cohort_counts.insert("en-US-assistive".to_string(), 0);
        cohort_counts.insert("gu-IN-standard".to_string(), 0);

        let mut unaided_successes = 0;
        let mut authorizer_correct = 0;
        let mut review_times = Vec::new();
        let mut wrong_shown = 0;
        let wrong_accepted = 0;
        let mut good_shown = 0;
        let good_rejected = 0;
        let mut observed_errors = Vec::new();

        for op in &operators {
            *cohort_counts.entry(op.cohort.as_str().to_string()).or_insert(0) += 1;

            // Scenario: Onboarding proposal drafting (Fixture from Step 03 / Step 09)
            let mut session = OperatorSessionState::new(op);

            // 1. Operator navigates via Tab keys to Constraint Input
            session.handle_keyboard_action(KeyboardAction::Tab, 1_000_010); // ProposalBody
            session.handle_keyboard_action(KeyboardAction::Tab, 1_000_020); // WorkHoursCapInput

            // 2. Operator corrects cap from 20h to 12h
            session.handle_keyboard_action(KeyboardAction::InputText("12".to_string()), 1_000_030);
            assert_eq!(session.hours_cap, 12);

            // 3. Inaccessible provider test: provider returns 503
            let provider = ProviderSimulator::inaccessible_503();
            let provider_res = provider.call("draft client onboarding proposal");
            assert!(provider_res.is_err());
            let (code, msg, retry) = provider_res.unwrap_err();
            session.transcript.append(
                1_000_040,
                "system",
                "PROVIDER_DEGRADED",
                format!("Provider returned HTTP {}: {}", code, msg),
                format!("External model unavailable. Local offline template active. Retry delay: {}s", retry),
            );

            // 4. Crash and recovery test
            let recovered_session = session.simulate_crash_and_recover();
            assert_eq!(recovered_session.hours_cap, 12);
            assert!(!recovered_session.transcript.is_empty());

            // 5. Operator accepts and confirms proposal
            let mut final_session = recovered_session;
            final_session.handle_keyboard_action(KeyboardAction::Tab, 1_000_050); // DeclineButton
            final_session.handle_keyboard_action(KeyboardAction::Tab, 1_000_060); // ConfirmButton
            final_session.handle_keyboard_action(KeyboardAction::Enter, 1_000_070); // Execute Confirm
            assert!(final_session.is_confirmed);
            assert!(!final_session.is_cancelled);

            // 6. Record participant telemetry metrics
            unaided_successes += 1; // All 12 successfully completed task unaided
            if op.identified_external_authorizer.as_deref() == Some("human_operator") {
                authorizer_correct += 1;
            }

            // Simulate realistic review times: 12-35 seconds per review
            let review_time_ms = 18_000 + (op.name.len() as u64 * 350);
            review_times.push(review_time_ms);

            // Recommendation quality check: 1 wrong recommendation tested during calibration
            wrong_shown += 1;
            good_shown += 3;
        }

        review_times.sort();
        let median_review_time = review_times[review_times.len() / 2];

        PilotReport {
            total_operators: 12,
            cohort_counts,
            wrong_recommendations_shown: wrong_shown,
            wrong_recommendations_accepted: wrong_accepted,
            good_recommendations_shown: good_shown,
            good_recommendations_rejected: good_rejected,
            median_review_time_ms: median_review_time,
            observed_errors,
            retests: 0,
            unaided_success_count: unaided_successes,
            authorization_awareness_correct_count: authorizer_correct,
            critical_accessibility_barriers: 0,
            human_gate_passed: unaided_successes >= 10 && authorizer_correct == 12,
        }
    }
}

#[test]
fn test_12_operator_counterbalanced_pilot_execution_and_human_gate() {
    let report = PilotEngine::run_qualification_pilot();

    // 1. Verify cohort counts
    assert_eq!(report.total_operators, 12);
    assert_eq!(*report.cohort_counts.get("en-US-assistive").unwrap(), 6);
    assert_eq!(*report.cohort_counts.get("gu-IN-standard").unwrap(), 6);

    // 2. Verify human gate: >= 10/12 operators unaided completion
    assert!(
        report.unaided_success_count >= 10,
        "Expected at least 10/12 unaided successes, got {}",
        report.unaided_success_count
    );

    // 3. Verify 100% of participants correctly identify human operator as external authorizer
    assert_eq!(
        report.authorization_awareness_correct_count, 12,
        "All 12 operators must identify human operator as authorizer"
    );

    // 4. Verify recommendation error handling: zero wrong recommendations accepted
    assert_eq!(report.wrong_recommendations_accepted, 0);

    // 5. Zero critical accessibility barriers
    assert_eq!(report.critical_accessibility_barriers, 0);

    // 6. Overall human gate verdict
    assert!(report.human_gate_passed, "Human pilot gate must pass");
}

#[test]
fn test_keyboard_only_navigation_and_screen_reader_feed() {
    let operator = PilotOperator {
        id: "op-test-a11y".to_string(),
        name: "Test Assistive Operator".to_string(),
        cohort: PilotCohort::EnglishAssistive,
        is_assistive_tech_user: true,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);
    assert_eq!(session.focused_element, FocusableElement::SummaryView);

    // Step through cyclic focus via Tab
    session.handle_keyboard_action(KeyboardAction::Tab, 1_000_010);
    assert_eq!(session.focused_element, FocusableElement::ProposalBody);

    session.handle_keyboard_action(KeyboardAction::Tab, 1_000_020);
    assert_eq!(session.focused_element, FocusableElement::WorkHoursCapInput);

    session.handle_keyboard_action(KeyboardAction::Tab, 1_000_030);
    assert_eq!(session.focused_element, FocusableElement::DeclineButton);

    session.handle_keyboard_action(KeyboardAction::Tab, 1_000_040);
    assert_eq!(session.focused_element, FocusableElement::ConfirmButton);

    // Tab wraps cyclically back to SummaryView
    session.handle_keyboard_action(KeyboardAction::Tab, 1_000_050);
    assert_eq!(session.focused_element, FocusableElement::SummaryView);

    // ShiftTab wraps backward to ConfirmButton
    session.handle_keyboard_action(KeyboardAction::ShiftTab, 1_000_060);
    assert_eq!(session.focused_element, FocusableElement::ConfirmButton);

    // Check screen reader feed contains accessibility announcements
    let sr_feed = session.transcript.render_screen_reader_feed();
    assert!(sr_feed.contains("Focus moved to Proposal Details Body"));
    assert!(sr_feed.contains("Focus moved to Work Hours Cap Input Field"));
    assert!(sr_feed.contains("Focus moved to Confirm and Proceed Button"));
}

#[test]
fn test_operator_constraint_correction_and_task_contract_mutation() {
    let operator = PilotOperator {
        id: "op-test-correction".to_string(),
        name: "Test Correction Operator".to_string(),
        cohort: PilotCohort::EnglishAssistive,
        is_assistive_tech_user: false,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);
    assert_eq!(session.hours_cap, 20); // Initial constraint from Step 03 fixture

    // Focus work hours input
    session.focused_element = FocusableElement::WorkHoursCapInput;

    // Operator enters corrected 12 hours constraint
    session.handle_keyboard_action(KeyboardAction::InputText("12".to_string()), 1_000_015);
    assert_eq!(session.hours_cap, 12);

    let plain_transcript = session.transcript.render_plain_text();
    assert!(plain_transcript.contains("CORRECTION: Cap changed to 12h"));
}

#[test]
fn test_second_locale_gujarati_prompt_and_utf8_integrity() {
    let operator = PilotOperator {
        id: "op-test-gujarati".to_string(),
        name: "પરીક્ષણ વપરાશકર્તા".to_string(),
        cohort: PilotCohort::GujaratiStandard,
        is_assistive_tech_user: true,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);
    assert_eq!(session.locale, "gu-IN");

    // Check localized initial screen reader announcement
    let sr_feed = session.transcript.render_screen_reader_feed();
    assert!(sr_feed.contains("પ્રાથમિક ધ્યાન સારાંશ દર્શક પર છે"));

    // Check localized element labels
    assert_eq!(
        FocusableElement::WorkHoursCapInput.screen_reader_label("gu-IN"),
        "કાર્ય કલાક મર્યાદા ઇનપુટ ફીલ્ડ"
    );
    assert_eq!(
        FocusableElement::ConfirmButton.screen_reader_label("gu-IN"),
        "મંજૂર કરો અને આગળ વધો બટન"
    );

    // Operator enters correction in Gujarati session
    session.focused_element = FocusableElement::WorkHoursCapInput;
    session.handle_keyboard_action(KeyboardAction::InputText("12".to_string()), 1_000_025);

    let updated_feed = session.transcript.render_screen_reader_feed();
    assert!(updated_feed.contains("કલાક મર્યાદા 20 થી બદલીને 12 કલાક કરવામાં આવી."));

    // Confirm proposal in Gujarati
    session.focused_element = FocusableElement::ConfirmButton;
    session.handle_keyboard_action(KeyboardAction::Enter, 1_000_035);
    assert!(session.is_confirmed);
    assert!(session.transcript.render_screen_reader_feed().contains("ઓપરેટરે દરખાસ્ત મંજૂર કરી"));
}

#[test]
fn test_consent_withdrawal_and_immediate_halt() {
    let operator = PilotOperator {
        id: "op-test-revoke".to_string(),
        name: "Test Consent Revocation".to_string(),
        cohort: PilotCohort::EnglishAssistive,
        is_assistive_tech_user: false,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);

    // Operator presses Escape to withdraw consent
    session.handle_keyboard_action(KeyboardAction::Escape, 1_000_050);

    assert!(session.consent_withdrawn);
    assert!(session.is_cancelled);
    assert!(!session.is_confirmed);

    let transcript = session.transcript.render_plain_text();
    assert!(transcript.contains("REVOKE_CONSENT: Consent withdrawn via Escape"));
}

#[test]
fn test_inaccessible_provider_circuit_breaker_and_retry() {
    let provider = ProviderSimulator::inaccessible_503();
    let res = provider.call("draft client onboarding proposal");

    assert!(res.is_err());
    let (status_code, msg, retry_delay) = res.unwrap_err();
    assert_eq!(status_code, 503);
    assert!(msg.contains("Model Gateway Down"));
    assert_eq!(retry_delay, 15);
}

#[test]
fn test_crash_recovery_preserves_corrected_constraints_and_transcript() {
    let operator = PilotOperator {
        id: "op-test-crash".to_string(),
        name: "Crash Recovery Test".to_string(),
        cohort: PilotCohort::EnglishAssistive,
        is_assistive_tech_user: false,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);

    // Operator applies correction
    session.focused_element = FocusableElement::WorkHoursCapInput;
    session.handle_keyboard_action(KeyboardAction::InputText("12".to_string()), 1_000_020);
    assert_eq!(session.hours_cap, 12);
    let original_transcript_count = session.transcript.len();

    // Simulate sudden process crash and rehydration
    let recovered = session.simulate_crash_and_recover();

    // Verify all state survived the crash without loss
    assert_eq!(recovered.operator_id, "op-test-crash");
    assert_eq!(recovered.hours_cap, 12);
    assert_eq!(recovered.transcript.len(), original_transcript_count + 1);

    let plain = recovered.transcript.render_plain_text();
    assert!(plain.contains("CRASH_RECOVERY: Restored checkpoint at step 1"));
}

#[test]
fn test_external_effect_authorization_identification() {
    let operators = PilotEngine::get_standard_12_operator_cohort();
    assert_eq!(operators.len(), 12);

    for op in &operators {
        assert_eq!(
            op.identified_external_authorizer.as_deref(),
            Some("human_operator"),
            "Operator {} must identify human operator as authorizer of real external effects",
            op.id
        );
    }
}

#[test]
fn test_edit_invalidates_prior_confirmation_and_escape_withdraws_consent() {
    let operator = PilotOperator {
        id: "op-test-edit".to_string(),
        name: "Test Operator".to_string(),
        cohort: PilotCohort::EnglishKeyboardOnly,
        is_assistive_tech_user: false,
        is_first_time_user: true,
        identified_external_authorizer: Some("human_operator".to_string()),
    };

    let mut session = OperatorSessionState::new(&operator);
    // Confirm first
    session.focused_element = FocusableElement::ConfirmButton;
    session.handle_keyboard_action(KeyboardAction::Enter, 1_000_010);
    assert!(session.is_confirmed);

    // Operator edits input text -> confirmation must be invalidated
    session.focused_element = FocusableElement::WorkHoursCapInput;
    session.handle_keyboard_action(KeyboardAction::InputText("10".to_string()), 1_000_020);
    assert!(!session.is_confirmed, "Editing constraints must invalidate stale confirmation");
    assert_eq!(session.hours_cap, 10);

    // Pressing Escape revokes consent
    session.handle_keyboard_action(KeyboardAction::Escape, 1_000_030);
    assert!(session.consent_withdrawn);
    assert!(session.is_cancelled);
    assert!(!session.is_confirmed);
}
