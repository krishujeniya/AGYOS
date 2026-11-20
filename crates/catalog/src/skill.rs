//! AGYOS Skill Definitions and Dispositions.
//!
//! Complies with Principle P04 (Behavioral Contracts) and P29 (Progressive Disclosure).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum SkillDisposition {
    Active,
    Merged,
    ReferenceOnly,
    Unavailable,
    Restricted,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SkillDefinition {
    pub id: String,
    pub home: String,
    pub primary_role: String,
    pub secondary_roles: Vec<String>,
    pub disposition: SkillDisposition,
    pub is_selectable: bool,
}

impl SkillDefinition {
    pub fn new(
        id: impl Into<String>,
        home: impl Into<String>,
        primary_role: impl Into<String>,
        secondary_roles: Vec<String>,
        disposition: SkillDisposition,
    ) -> Self {
        let is_selectable = matches!(disposition, SkillDisposition::Active | SkillDisposition::Merged);
        Self {
            id: id.into(),
            home: home.into(),
            primary_role: primary_role.into(),
            secondary_roles,
            disposition,
            is_selectable,
        }
    }
}
