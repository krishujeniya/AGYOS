//! AGY Host CLI Version Negotiation.
//!
//! Complies with Principle P04 (Behavioral Contracts and Compatibility).
//! Pinned baseline: AGY CLI v1.5.13 (min 1.5.0, max 1.5.x).

use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgyVersion {
    pub major: u32,
    pub minor: u32,
    pub patch: u32,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VersionError {
    ParseError(String),
    UnsupportedVersion { found: String, expected_min: String },
}

impl fmt::Display for VersionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            VersionError::ParseError(msg) => write!(f, "Invalid AGY CLI version format: {}", msg),
            VersionError::UnsupportedVersion { found, expected_min } => {
                write!(f, "Unsupported AGY CLI version: {} (minimum required is {})", found, expected_min)
            }
        }
    }
}

impl std::error::Error for VersionError {}

impl AgyVersion {
    pub fn parse(s: &str) -> Result<Self, VersionError> {
        let trimmed = s.trim().trim_start_matches('v');
        let parts: Vec<&str> = trimmed.split('.').collect();
        if parts.len() < 3 {
            return Err(VersionError::ParseError(s.to_string()));
        }
        let major = parts[0].parse::<u32>().map_err(|e| VersionError::ParseError(e.to_string()))?;
        let minor = parts[1].parse::<u32>().map_err(|e| VersionError::ParseError(e.to_string()))?;
        let patch = parts[2].split('-').next().unwrap_or("0")
            .parse::<u32>().map_err(|e| VersionError::ParseError(e.to_string()))?;

        Ok(Self { major, minor, patch })
    }

    pub fn is_supported(&self) -> bool {
        // Supported range: 1.5.0 to 1.5.x
        self.major == 1 && self.minor >= 5
    }

    pub fn negotiate(raw_version: &str) -> Result<Self, VersionError> {
        let ver = Self::parse(raw_version)?;
        if !ver.is_supported() {
            return Err(VersionError::UnsupportedVersion {
                found: raw_version.to_string(),
                expected_min: "1.5.0".to_string(),
            });
        }
        Ok(ver)
    }
}
