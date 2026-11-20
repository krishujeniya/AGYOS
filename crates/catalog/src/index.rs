//! Fast In-Memory Reconciled Catalog Index.

use std::collections::HashMap;
use crate::ledger::MigrationLedger;
use crate::reconcile::CatalogReconciler;
use crate::role::{GoverningPod, RoleDefinition, RoleRegistry};
use crate::skill::{SkillDefinition, SkillDisposition};

pub struct ReconciledCatalogIndex {
    roles: HashMap<String, RoleDefinition>,
    skills: HashMap<String, SkillDefinition>,
    aliases: HashMap<String, String>,
}

impl ReconciledCatalogIndex {
    pub fn load_default() -> Self {
        let role_list = RoleRegistry::load_roles();
        let ledger = MigrationLedger::build_reconciled_ledger();

        let mut roles = HashMap::with_capacity(role_list.len());
        for r in role_list {
            roles.insert(r.role_id.clone(), r);
        }

        let mut skills = HashMap::with_capacity(ledger.sources.len());
        for (_path, rec) in &ledger.sources {
            skills.insert(
                rec.old_id.clone(),
                SkillDefinition::new(
                    rec.old_id.clone(),
                    "legacy",
                    rec.owner_role.clone(),
                    Vec::new(),
                    rec.disposition,
                ),
            );
        }

        // Inject the 2 resolved conflict records
        let conflicts = CatalogReconciler::resolve_ownership_conflicts();
        for c in conflicts {
            skills.insert(
                c.skill_id.clone(),
                SkillDefinition::new(
                    c.skill_id,
                    "voice-infra",
                    c.resolved_primary,
                    vec![c.resolved_secondary],
                    SkillDisposition::Active,
                ),
            );
        }

        Self {
            roles,
            skills,
            aliases: ledger.aliases,
        }
    }

    pub fn role_count(&self) -> usize {
        self.roles.len()
    }

    pub fn skill_count(&self) -> usize {
        self.skills.len()
    }

    pub fn alias_count(&self) -> usize {
        self.aliases.len()
    }

    pub fn get_role(&self, role_id: &str) -> Option<&RoleDefinition> {
        self.roles.get(role_id)
    }

    pub fn get_skill(&self, skill_id: &str) -> Option<&SkillDefinition> {
        self.skills.get(skill_id)
    }

    pub fn resolve_alias(&self, alias: &str) -> Option<&String> {
        self.aliases.get(alias)
    }

    pub fn is_selectable(&self, skill_id: &str) -> bool {
        self.skills.get(skill_id).map(|s| s.is_selectable).unwrap_or(false)
    }

    pub fn roles_by_pod(&self, pod: GoverningPod) -> Vec<&RoleDefinition> {
        self.roles.values().filter(|r| r.governing_pod == pod).collect()
    }
}

impl Default for ReconciledCatalogIndex {
    fn default() -> Self {
        Self::load_default()
    }
}
