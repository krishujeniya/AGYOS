//! Broker Confinement and Process Isolation for AGY Host.
//!
//! Complies with Principle P05 (Complete Mediation, Least Privilege) and
//! P07 (Secure Development & Recurrence Prevention).

use std::fmt;
use domain::RiskLevel;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ConfinementError {
    OmittedHooks(String),
    UnbrokeredCommandDenied(String),
    UnauthorizedPrivilegeEscalation { requested: RiskLevel, max_permitted: RiskLevel },
    PrivateVaultAccessViolation(String),
}

impl fmt::Display for ConfinementError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfinementError::OmittedHooks(msg) => write!(f, "Omitted hooks violation: {}", msg),
            ConfinementError::UnbrokeredCommandDenied(cmd) => {
                write!(f, "Unbrokered shell execution blocked: command '{}' cannot exercise privileged effects", cmd)
            }
            ConfinementError::UnauthorizedPrivilegeEscalation { requested, max_permitted } => {
                write!(f, "Privilege escalation denied: requested {:?}, maximum allowed is {:?}", requested, max_permitted)
            }
            ConfinementError::PrivateVaultAccessViolation(key) => {
                write!(f, "Private vault boundary violation: unbrokered shell cannot read secret '{}'", key)
            }
        }
    }
}

impl std::error::Error for ConfinementError {}

pub struct ConfinementGuard {
    hooks_installed: bool,
    broker_token_active: bool,
    max_permitted_risk: RiskLevel,
}

impl ConfinementGuard {
    pub fn new(hooks_installed: bool, broker_token_active: bool, max_permitted_risk: RiskLevel) -> Self {
        Self {
            hooks_installed,
            broker_token_active,
            max_permitted_risk,
        }
    }

    /// Check whether a command is permitted to execute.
    pub fn verify_command_execution(&self, command: &str, risk: RiskLevel) -> Result<(), ConfinementError> {
        // 1. Mandatory hook enforcement
        if !self.hooks_installed {
            return Err(ConfinementError::OmittedHooks(
                "Execution hooks (.agents/hooks.json) missing or inactive".to_string(),
            ));
        }

        // 2. Privilege ceiling check
        if risk > self.max_permitted_risk {
            return Err(ConfinementError::UnauthorizedPrivilegeEscalation {
                requested: risk,
                max_permitted: self.max_permitted_risk,
            });
        }

        // 3. For R1..R3 effects, unbrokered shell execution is forbidden
        if risk != RiskLevel::R0 && !self.broker_token_active {
            return Err(ConfinementError::UnbrokeredCommandDenied(command.to_string()));
        }

        Ok(())
    }

    /// Ensure private vault secrets are strictly isolated from shell inspection.
    pub fn verify_vault_isolation(&self, secret_key: &str) -> Result<(), ConfinementError> {
        if !self.broker_token_active {
            return Err(ConfinementError::PrivateVaultAccessViolation(secret_key.to_string()));
        }
        Ok(())
    }
}
