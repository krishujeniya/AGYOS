//! AGYOS Operator Control & Human Pilot Engine (Step 14).
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

use serde::{Deserialize, Serialize};

/// Cohort assignment for counterbalanced human pilot.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PilotCohort {
    /// Cohort A: English locale, keyboard-only and assistive-tech operators.
    EnglishAssistive,
    /// Cohort B: Second locale (Gujarati gu-IN), multilingual comprehension.
    GujaratiStandard,
}

impl PilotCohort {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::EnglishAssistive => "en-US-assistive",
            Self::GujaratiStandard => "gu-IN-standard",
        }
    }

    pub fn locale(&self) -> &'static str {
        match self {
            Self::EnglishAssistive => "en-US",
            Self::GujaratiStandard => "gu-IN",
        }
    }
}

/// Profile of a human pilot participant.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PilotOperator {
    pub id: String,
    pub name: String,
    pub cohort: PilotCohort,
    pub is_assistive_tech_user: bool,
    pub is_first_time_user: bool,
    pub identified_external_authorizer: Option<String>,
}

/// Interactive focusable UI element for keyboard navigation (WCAG 2.1 AA).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum FocusableElement {
    SummaryView,
    ProposalBody,
    WorkHoursCapInput,
    DeclineButton,
    ConfirmButton,
}

impl FocusableElement {
    pub const ALL: [Self; 5] = [
        Self::SummaryView,
        Self::ProposalBody,
        Self::WorkHoursCapInput,
        Self::DeclineButton,
        Self::ConfirmButton,
    ];

    pub fn next(&self) -> Self {
        match self {
            Self::SummaryView => Self::ProposalBody,
            Self::ProposalBody => Self::WorkHoursCapInput,
            Self::WorkHoursCapInput => Self::DeclineButton,
            Self::DeclineButton => Self::ConfirmButton,
            Self::ConfirmButton => Self::SummaryView,
        }
    }

    pub fn prev(&self) -> Self {
        match self {
            Self::SummaryView => Self::ConfirmButton,
            Self::ProposalBody => Self::SummaryView,
            Self::WorkHoursCapInput => Self::ProposalBody,
            Self::DeclineButton => Self::WorkHoursCapInput,
            Self::ConfirmButton => Self::DeclineButton,
        }
    }

    pub fn screen_reader_label(&self, locale: &str) -> &'static str {
        match (self, locale) {
            (Self::SummaryView, "gu-IN") => "કાર્ય સારાંશ દર્શક (વાંચન માટે)",
            (Self::SummaryView, _) => "Task Summary View (read-only)",
            (Self::ProposalBody, "gu-IN") => "દરખાસ્ત વિગતો (વાંચન માટે)",
            (Self::ProposalBody, _) => "Proposal Details Body (read-only)",
            (Self::WorkHoursCapInput, "gu-IN") => "કાર્ય કલાક મર્યાદા ઇનપુટ ફીલ્ડ",
            (Self::WorkHoursCapInput, _) => "Work Hours Cap Input Field (editable)",
            (Self::DeclineButton, "gu-IN") => "અસ્વીકાર કરો બટન",
            (Self::DeclineButton, _) => "Decline and Cancel Button",
            (Self::ConfirmButton, "gu-IN") => "મંજૂર કરો અને આગળ વધો બટન",
            (Self::ConfirmButton, _) => "Confirm and Proceed Button",
        }
    }
}

/// Keyboard action for keyboard-only accessibility.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KeyboardAction {
    Tab,
    ShiftTab,
    Enter,
    Escape,
    InputText(String),
}

/// Monotonic, append-only linear transcript entry.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TranscriptEntry {
    pub sequence: u64,
    pub timestamp_epoch_s: u64,
    pub actor: String,
    pub action_type: String,
    pub content: String,
    pub screen_reader_announcement: String,
}

/// Linear transcript maintaining strict chronological ordering.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct LinearTranscript {
    entries: Vec<TranscriptEntry>,
}

impl LinearTranscript {
    pub fn new() -> Self {
        Self { entries: Vec::new() }
    }

    pub fn append(
        &mut self,
        timestamp_s: u64,
        actor: impl Into<String>,
        action_type: impl Into<String>,
        content: impl Into<String>,
        announcement: impl Into<String>,
    ) {
        let seq = (self.entries.len() + 1) as u64;
        self.entries.push(TranscriptEntry {
            sequence: seq,
            timestamp_epoch_s: timestamp_s,
            actor: actor.into(),
            action_type: action_type.into(),
            content: content.into(),
            screen_reader_announcement: announcement.into(),
        });
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn entries(&self) -> &[TranscriptEntry] {
        &self.entries
    }

    pub fn render_plain_text(&self) -> String {
        let mut out = String::new();
        for entry in &self.entries {
            out.push_str(&format!(
                "[{}] ({}) {}: {}\n",
                entry.sequence, entry.actor, entry.action_type, entry.content
            ));
        }
        out
    }

    pub fn render_screen_reader_feed(&self) -> String {
        let mut out = String::new();
        for entry in &self.entries {
            out.push_str(&format!(
                "Event {}: {}\n",
                entry.sequence, entry.screen_reader_announcement
            ));
        }
        out
    }
}

/// State of an active operator session.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OperatorSessionState {
    pub operator_id: String,
    pub cohort: PilotCohort,
    pub locale: String,
    pub focused_element: FocusableElement,
    pub hours_cap: u32,
    pub is_cancelled: bool,
    pub is_confirmed: bool,
    pub consent_withdrawn: bool,
    pub transcript: LinearTranscript,
    pub last_checkpoint_step: u32,
    pub review_duration_ms: u64,
}

impl OperatorSessionState {
    pub fn new(operator: &PilotOperator) -> Self {
        let mut transcript = LinearTranscript::new();
        let welcome = match operator.cohort.locale() {
            "gu-IN" => "નવી ઑપરેટર સત્ર શરૂ થઈ. પ્રાથમિક ધ્યાન સારાંશ દર્શક પર છે.",
            _ => "New operator session initialized. Initial focus on Summary View.",
        };
        transcript.append(
            1_000_000,
            "system",
            "INITIALIZE",
            format!("Session started for {}", operator.name),
            welcome,
        );

        Self {
            operator_id: operator.id.clone(),
            cohort: operator.cohort,
            locale: operator.cohort.locale().to_string(),
            focused_element: FocusableElement::SummaryView,
            hours_cap: 20, // Initial default proposal cap
            is_cancelled: false,
            is_confirmed: false,
            consent_withdrawn: false,
            transcript,
            last_checkpoint_step: 1,
            review_duration_ms: 0,
        }
    }

    /// Process keyboard input in strict keyboard-only mode.
    pub fn handle_keyboard_action(&mut self, action: KeyboardAction, timestamp_s: u64) {
        match action {
            KeyboardAction::Tab => {
                self.focused_element = self.focused_element.next();
                let announcement = self.focused_element.screen_reader_label(&self.locale);
                self.transcript.append(
                    timestamp_s,
                    "operator",
                    "KEYBOARD_NAV",
                    format!("Focused {:?}", self.focused_element),
                    format!("Focus moved to {}", announcement),
                );
            }
            KeyboardAction::ShiftTab => {
                self.focused_element = self.focused_element.prev();
                let announcement = self.focused_element.screen_reader_label(&self.locale);
                self.transcript.append(
                    timestamp_s,
                    "operator",
                    "KEYBOARD_NAV",
                    format!("Focused {:?}", self.focused_element),
                    format!("Focus moved back to {}", announcement),
                );
            }
            KeyboardAction::InputText(text) => {
                if self.focused_element == FocusableElement::WorkHoursCapInput {
                    if let Ok(parsed_hours) = text.trim().parse::<u32>() {
                        let old_hours = self.hours_cap;
                        self.hours_cap = parsed_hours;
                        self.is_confirmed = false; // Modification invalidates any stale prior confirmation
                        let msg = match self.locale.as_str() {
                            "gu-IN" => format!("કલાક મર્યાદા {} થી બદલીને {} કલાક કરવામાં આવી.", old_hours, parsed_hours),
                            _ => format!("Work hours cap modified from {}h to {}h.", old_hours, parsed_hours),
                        };
                        self.transcript.append(
                            timestamp_s,
                            "operator",
                            "CORRECTION",
                            format!("Cap changed to {}h", parsed_hours),
                            msg,
                        );
                    }
                }
            }
            KeyboardAction::Enter => match self.focused_element {
                FocusableElement::ConfirmButton => {
                    self.is_confirmed = true;
                    let msg = match self.locale.as_str() {
                        "gu-IN" => "ઓપરેટરે દરખાસ્ત મંજૂર કરી.",
                        _ => "Operator confirmed and accepted proposal.",
                    };
                    self.transcript.append(
                        timestamp_s,
                        "operator",
                        "CONFIRM",
                        "Confirmed proposal with current constraints",
                        msg,
                    );
                }
                FocusableElement::DeclineButton => {
                    self.is_cancelled = true;
                    self.is_confirmed = false;
                    let msg = match self.locale.as_str() {
                        "gu-IN" => "ઓપરેટરે દરખાસ્ત અસ્વીકાર કરી.",
                        _ => "Operator declined proposal.",
                    };
                    self.transcript.append(
                        timestamp_s,
                        "operator",
                        "DECLINE",
                        "Declined proposal",
                        msg,
                    );
                }
                _ => {}
            },
            KeyboardAction::Escape => {
                self.is_cancelled = true;
                self.consent_withdrawn = true;
                self.is_confirmed = false;
                let msg = match self.locale.as_str() {
                    "gu-IN" => "ઓપરેટરે મંજૂરી પાછી ખેંચી અને સત્ર રદ કર્યું.",
                    _ => "Operator withdrew consent via Escape key. Operation halted.",
                };
                self.transcript.append(
                    timestamp_s,
                    "operator",
                    "REVOKE_CONSENT",
                    "Consent withdrawn via Escape",
                    msg,
                );
            }
        }
    }

    /// Simulate process crash and subsequent rehydration from checkpoint.
    pub fn simulate_crash_and_recover(&self) -> Self {
        // Rehydrates cleanly from snapshot without in-memory reference sharing
        let json = serde_json::to_string(self).unwrap_or_default();
        let mut recovered: Self = serde_json::from_str(&json).unwrap_or_else(|_| self.clone());
        let timestamp = 1_000_100;
        let announcement = match recovered.locale.as_str() {
            "gu-IN" => "સિસ્ટમ ક્રેશ પછી સ્થિતિ પુનઃસ્થાપિત થઈ. તમામ ફેરફારો સુરક્ષિત છે.",
            _ => "State rehydrated after simulated crash. All constraints preserved.",
        };
        recovered.transcript.append(
            timestamp,
            "system",
            "CRASH_RECOVERY",
            format!("Restored checkpoint at step {}", recovered.last_checkpoint_step),
            announcement,
        );
        recovered
    }
}
