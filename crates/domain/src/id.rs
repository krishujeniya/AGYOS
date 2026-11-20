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
define_id!(WorkspaceId, "ws_");
define_id!(ActorId, "actor_");
define_id!(RoleId, "role_");
define_id!(ReceiptId, "rec_");
define_id!(ApprovalId, "appr_");
