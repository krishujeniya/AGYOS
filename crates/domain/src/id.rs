//! Strongly-typed Domain Identifiers.

use serde::{Deserialize, Serialize};
use std::fmt;

macro_rules! define_id {
    ($name:ident, $prefix:expr) => {
        #[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
        pub struct $name(String);

        impl $name {
            pub fn new(val: impl Into<String>) -> Self {
                Self(val.into())
            }

            pub fn as_str(&self) -> &str {
                &self.0
            }
        }

        impl fmt::Display for $name {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(f, "{}", self.0)
            }
        }
    };
}

define_id!(TaskId, "task_");
define_id!(ActorId, "actor_");
define_id!(RoleId, "role_");
define_id!(ReceiptId, "rec_");
define_id!(ApprovalId, "appr_");

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct WorkspaceId(String);

impl WorkspaceId {
    pub fn new(val: impl Into<String>) -> Self {
        let s = val.into();
        Self::validate(&s).expect("Invalid workspace id");
        Self(s)
    }

    pub fn try_new(val: impl Into<String>) -> Result<Self, String> {
        let s = val.into();
        Self::validate(&s)?;
        Ok(Self(s))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    pub fn validate(val: &str) -> Result<(), String> {
        if val.is_empty() || val.len() > 128 {
            return Err("Workspace ID length must be between 1 and 128 characters".to_string());
        }
        if val.contains("..") || val.contains('/') || val.contains('\\') || val.contains('\0') {
            return Err("Workspace ID contains forbidden path traversal or separator characters".to_string());
        }
        if !val.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_' || c == '.') {
            return Err("Workspace ID contains invalid characters (allowed: alphanumeric, '-', '_', '.')".to_string());
        }
        Ok(())
    }
}

impl fmt::Display for WorkspaceId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}
