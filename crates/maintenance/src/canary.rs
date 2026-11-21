//! Canary Observation & Legacy Write Retirement Engine (Step 19).
//!
//! Complies with Step 19 finish criteria:
//! "After ≥14 days of qualified canary/production observation, zero unresolved migration discrepancies
//! and documented reversal authority, retire old writes only for the qualified profile.
//! Preserve the legacy snapshot and provider for any unmigrated profile."
//!
//! Principles:
//! - P03 (Bounded Memory & Working Sets)
//! - P07 (Secure Development Lifecycle / SSDF)
//! - P09 (Explicit State & Invariants)
//! - P17 (Progressive Delivery & Canary Gates)

use serde::{Deserialize, Serialize};

/// Canary observation record tracking live deployment stability.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CanaryObservation {
    pub profile_name: String,
    pub observation_start_epoch_s: u64,
    pub observation_end_epoch_s: u64,
    pub total_operations_observed: usize,
    pub unresolved_migration_discrepancies: usize,
    pub documented_reversal_authority: String,
    pub legacy_snapshot_sha: String,
    pub legacy_provider_retained: bool,
}

/// Official retirement receipt certifying safe legacy write retirement.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RetirementReceipt {
    pub profile_name: String,
    pub observation_days: u32,
    pub legacy_writes_retired: bool,
    pub legacy_snapshot_preserved: bool,
    pub preserved_legacy_sha: String,
    pub reversal_authority_verified: bool,
    pub retired_at_epoch_s: u64,
}

pub struct CanaryRetirementEngine;

impl CanaryRetirementEngine {
    /// Minimum observation requirement: 14 days (1,209,600 seconds).
    pub const MIN_OBSERVATION_SECONDS: u64 = 14 * 86_400;

    /// Evaluates whether a canary profile meets all Step 19 criteria for legacy write retirement.
    pub fn evaluate_retirement(
        canary: &CanaryObservation,
        current_epoch_s: u64,
    ) -> Result<RetirementReceipt, String> {
        let elapsed = canary.observation_end_epoch_s.saturating_sub(canary.observation_start_epoch_s);
        let observation_days = (elapsed / 86_400) as u32;

        if elapsed < Self::MIN_OBSERVATION_SECONDS {
            return Err(format!(
                "Insufficient canary observation: {} days (requires >= 14 days)",
                observation_days
            ));
        }

        if canary.total_operations_observed == 0 {
            return Err("Zero operations observed during canary observation window".to_string());
        }

        if !canary.legacy_provider_retained {
            return Err("Legacy provider must be retained as fallback for unmigrated profiles".to_string());
        }

        if canary.unresolved_migration_discrepancies > 0 {
            return Err(format!(
                "Unresolved migration discrepancies present: {} (must be 0)",
                canary.unresolved_migration_discrepancies
            ));
        }

        if canary.documented_reversal_authority.trim().is_empty() {
            return Err("Missing documented reversal authority".to_string());
        }

        if canary.legacy_snapshot_sha.trim().is_empty() {
            return Err("Missing preserved legacy snapshot SHA".to_string());
        }

        Ok(RetirementReceipt {
            profile_name: canary.profile_name.clone(),
            observation_days,
            legacy_writes_retired: true,
            legacy_snapshot_preserved: true,
            preserved_legacy_sha: canary.legacy_snapshot_sha.clone(),
            reversal_authority_verified: true,
            retired_at_epoch_s: current_epoch_s,
        })
    }
}
