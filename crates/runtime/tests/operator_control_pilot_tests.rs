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
    FocusableElement, KeyboardAction, LinearTranscript, OperatorSessionState, PilotCohort,
    PilotEngine, PilotOperator, ProviderSimulator,
};

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
