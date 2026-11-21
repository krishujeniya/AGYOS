//! Release Certification Gates & Verification Constraints (Step 18).
//!
//! Complies with Step 18 finish criteria and Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P08 (Build Provenance & Supply Chain Integrity)
//! - P09 (Explicit State & Invariants)
//! - P12 (Statistical Proof & Regression Bounds)
//! - P17 (Progressive Delivery & Canary Gates)

use serde::{Deserialize, Serialize};

/// Operator approval token recording human decision for a scoped action.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperatorApprovalToken {
    pub decision_id: String,
    pub approver_name: String,
    pub approved_revision: String,
    pub action_type: String, // "git_publication" or "production_release"
    pub approved: bool,
    pub timestamp_epoch_s: u64,
}

/// Explicit verification failures blocking release.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ReleaseGateFailure {
    ShaMismatch { target_sha: String, ci_sha: String },
    CiBuildFailed { status: String },
    StaleEvidence { evidence_age_s: u64, max_allowed_s: u64 },
    ChangedArtifactDigest { expected_digest: String, actual_digest: String },
    RightsViolation { details: String },
    DefensiveChecksFailed { details: String },
    SloViolation { metric: String, observed_ms: u64, ceiling_ms: u64 },
    GitPublicationDeclinedOrMissing,
    ProductionReleaseDeclinedOrMissing,
    UncommittedInFlightWorkRemaining { count: usize },
    StaleFenceOrCursor { details: String },
}

/// Release candidate package subject to gating.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReleaseCandidate {
    pub release_tag: String,
    pub target_commit_sha: String,
    pub ci_run_sha: String,
    pub ci_status: String,
    pub evidence_timestamp_epoch_s: u64,
    pub artifact_digest: String,
    pub provenance_digest: String,
    pub rights_cleared: bool,
    pub zero_secrets_leaked: bool,
    pub ast_checks_passed: bool,
    pub measured_route_p99_ms: u64,
    pub measured_status_p99_ms: u64,
    pub measured_durable_ack_p99_ms: u64,
    pub git_publication_approval: Option<OperatorApprovalToken>,
    pub production_release_approval: Option<OperatorApprovalToken>,
}

pub struct ReleaseGateEngine;

impl ReleaseGateEngine {
    /// Evaluates all release gates strictly. Returns Ok(()) only when all conditions pass.
    pub fn evaluate_candidate(
        candidate: &ReleaseCandidate,
        current_epoch_s: u64,
        max_evidence_age_s: u64,
    ) -> Result<(), Vec<ReleaseGateFailure>> {
        let mut failures = Vec::new();

        // 1. Exact-SHA Verification Gate
        if candidate.target_commit_sha != candidate.ci_run_sha {
            failures.push(ReleaseGateFailure::ShaMismatch {
                target_sha: candidate.target_commit_sha.clone(),
                ci_sha: candidate.ci_run_sha.clone(),
            });
        }

        // 2. Passing CI Gate
        if candidate.ci_status.to_lowercase() != "success" {
            failures.push(ReleaseGateFailure::CiBuildFailed {
                status: candidate.ci_status.clone(),
            });
        }

        // 3. Evidence Freshness Gate (Reject stale and future timestamps)
        if candidate.evidence_timestamp_epoch_s > current_epoch_s {
            failures.push(ReleaseGateFailure::StaleEvidence {
                evidence_age_s: candidate.evidence_timestamp_epoch_s - current_epoch_s,
                max_allowed_s: max_evidence_age_s,
            });
        } else {
            let evidence_age = current_epoch_s - candidate.evidence_timestamp_epoch_s;
            if evidence_age > max_evidence_age_s {
                failures.push(ReleaseGateFailure::StaleEvidence {
                    evidence_age_s: evidence_age,
                    max_allowed_s: max_evidence_age_s,
                });
            }
        }

        // 4. Artifact Integrity / Provenance Digest Gate
        if candidate.artifact_digest != candidate.provenance_digest {
            failures.push(ReleaseGateFailure::ChangedArtifactDigest {
                expected_digest: candidate.provenance_digest.clone(),
                actual_digest: candidate.artifact_digest.clone(),
            });
        }

        // 5. Rights & License Clearance Gate
        if !candidate.rights_cleared {
            failures.push(ReleaseGateFailure::RightsViolation {
                details: "Unverified rights or restricted software license detected".to_string(),
            });
        }

        // 6. Defensive Checks Gate
        if !candidate.zero_secrets_leaked || !candidate.ast_checks_passed {
            failures.push(ReleaseGateFailure::DefensiveChecksFailed {
                details: "Defensive scan failure: potential secret leakage or AST syntax issue".to_string(),
            });
        }

        // 7. SLO Verification Gate (Hosted / Local Ceilings)
        if candidate.measured_route_p99_ms > 150 {
            failures.push(ReleaseGateFailure::SloViolation {
                metric: "nominal_route_p99_ms".to_string(),
                observed_ms: candidate.measured_route_p99_ms,
                ceiling_ms: 150,
            });
        }
        if candidate.measured_status_p99_ms > 150 {
            failures.push(ReleaseGateFailure::SloViolation {
                metric: "nominal_status_p99_ms".to_string(),
                observed_ms: candidate.measured_status_p99_ms,
                ceiling_ms: 150,
            });
        }
        if candidate.measured_durable_ack_p99_ms > 300 {
            failures.push(ReleaseGateFailure::SloViolation {
                metric: "nominal_durable_ack_p99_ms".to_string(),
                observed_ms: candidate.measured_durable_ack_p99_ms,
                ceiling_ms: 300,
            });
        }

        // 8. Separate Operator Decisions Gate
        // Decision A: Git publication
        match &candidate.git_publication_approval {
            Some(token) if token.approved
                && token.approved_revision == candidate.target_commit_sha
                && token.action_type == "git_publication"
                && token.timestamp_epoch_s <= current_epoch_s => {}
            _ => failures.push(ReleaseGateFailure::GitPublicationDeclinedOrMissing),
        }

        // Decision B: Production release cutover
        match &candidate.production_release_approval {
            Some(token) if token.approved
                && token.approved_revision == candidate.target_commit_sha
                && token.action_type == "production_release"
                && token.timestamp_epoch_s <= current_epoch_s => {}
            _ => failures.push(ReleaseGateFailure::ProductionReleaseDeclinedOrMissing),
        }

        if failures.is_empty() {
            Ok(())
        } else {
            Err(failures)
        }
    }
}
