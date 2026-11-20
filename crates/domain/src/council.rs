//! Bounded Multi-Model Deliberation Council.
//!
//! Complies with Principle P25 (Selective Cognitive Forcing) and P27 (Empirically Justified Councils).

use serde::{Deserialize, Serialize};
use crate::id::ActorId;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CouncilQuestion {
    pub prompt: String,
    pub constraints: Vec<String>,
    pub required_evidence: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CouncilDissent {
    pub member: ActorId,
    pub dissenting_verdict: String,
    pub rationale: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Council {
    pub name: String,
    pub members: Vec<ActorId>,
    pub active_question: Option<CouncilQuestion>,
    pub dissents: Vec<CouncilDissent>,
}

impl Council {
    pub fn new(name: impl Into<String>, members: Vec<ActorId>) -> Self {
        Self {
            name: name.into(),
            members,
            active_question: None,
            dissents: Vec::new(),
        }
    }

    pub fn record_dissent(&mut self, dissent: CouncilDissent) {
        self.dissents.push(dissent);
    }
}
