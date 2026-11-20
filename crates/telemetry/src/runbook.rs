//! On-Call Operations & Incident Response Engine (Step 15).
//!
//! Complies with Step 15 finish criteria and Google SRE Principles:
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection)

use serde::{Deserialize, Serialize};

/// Production incident severity classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum IncidentSeverity {
    /// SEV-1: Critical failure: durable data loss, state corruption, or writer partition.
    Sev1Critical,
    /// SEV-2: Major failure: external provider degradation, circuit breaker tripped, or runaway token burn.
    Sev2Major,
    /// SEV-3: Minor issue: cache cold-start latency spike, non-blocking telemetry warning.
    Sev3Minor,
}

impl IncidentSeverity {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Sev1Critical => "SEV-1",
            Self::Sev2Major => "SEV-2",
            Self::Sev3Minor => "SEV-3",
        }
    }
}

/// Structured response guidance from the on-call runbook.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct IncidentResponsePlan {
    pub severity: IncidentSeverity,
    pub title: String,
    pub immediate_actions: Vec<String>,
    pub recovery_procedure: String,
    pub verification_command: String,
}

pub struct OnCallRunbook;

impl OnCallRunbook {
    /// Classifies an operational symptom and generates a typed incident response plan.
    pub fn triage_symptom(symptom: &str) -> IncidentResponsePlan {
        let lower = symptom.to_lowercase();

        if lower.contains("corruption") || lower.contains("data loss") || lower.contains("split-brain") {
            IncidentResponsePlan {
                severity: IncidentSeverity::Sev1Critical,
                title: "Durable Store Integrity or Split-Brain Incident".to_string(),
                immediate_actions: vec![
                    "Pause incoming durable writes immediately".to_string(),
                    "Inspect WAL events.log for corruption markers".to_string(),
                    "Verify active leader fence token epoch".to_string(),
                ],
                recovery_procedure: "Restore from latest verified backup archive using LocalBackupEngine::restore_backup".to_string(),
                verification_command: "bin/agyos workspace restore <milestone_id>".to_string(),
            }
        } else if lower.contains("circuit breaker") || lower.contains("503") || lower.contains("runaway") || lower.contains("provider down") {
            IncidentResponsePlan {
                severity: IncidentSeverity::Sev2Major,
                title: "Provider Degraded or Circuit Breaker Tripped".to_string(),
                immediate_actions: vec![
                    "Verify circuit breaker has tripped closed to prevent request flooding".to_string(),
                    "Activate local offline fallback templates".to_string(),
                    "Verify pending outbox records are held safely in Pending status".to_string(),
                ],
                recovery_procedure: "Wait for provider health probe or switch to backup approved provider".to_string(),
                verification_command: "bin/agyos state && bin/agyos diagnostics --preview".to_string(),
            }
        } else {
            IncidentResponsePlan {
                severity: IncidentSeverity::Sev3Minor,
                title: "Operational Threshold Warning or Cold Start Spike".to_string(),
                immediate_actions: vec![
                    "Check cold cache initialization latency".to_string(),
                    "Monitor steady RSS memory footprint against 256 MiB ceiling".to_string(),
                ],
                recovery_procedure: "Warm catalog caches and compact state if context > 65%".to_string(),
                verification_command: "bin/agyos compact".to_string(),
            }
        }
    }
}
