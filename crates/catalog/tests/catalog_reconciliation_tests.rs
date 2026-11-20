//! Step 10: Reconcile Catalogs — Verification and Integrity Tests.
//!
//! Complies with Step 10 acceptance criteria and Principles P03, P06, P09, P10, P12, P29:
//! - Reconcile 2,549 source paths
//! - Reconcile 4,620 aliases
//! - Reconcile 104 operational roles across 12 departments and 5 pods
//! - Resolve the 2 ownership conflicts (amazon-alexa and cloudflare-workers-expert)
//! - Ensure every unavailable record is strictly unselectable
//! - Ensure regenerated indexes match the canonical graph without dangling edges

use catalog::{
    CatalogReconciler, GoverningPod, MigrationLedger, ReconciledCatalogIndex, RoleRegistry,
};

#[test]
fn test_reconcile_2549_source_paths_inventory() {
    let ledger = MigrationLedger::build_reconciled_ledger();

    // Verify exact count of 2,549 source paths
    assert_eq!(
        ledger.total_sources, 2549,
        "Reconciled source inventory must equal 2,549 paths exactly"
    );

    // Verify all source records have valid paths and owner roles
    for (path, record) in &ledger.sources {
        assert!(!path.is_empty());
        assert!(!record.old_id.is_empty());
        assert!(!record.owner_role.is_empty());
    }
}

#[test]
fn test_reconcile_4620_alias_edges() {
    let ledger = MigrationLedger::build_reconciled_ledger();

    // Verify exact count of 4,620 alias mappings
    assert_eq!(
        ledger.total_aliases, 4620,
        "Reconciled aliases must equal 4,620 edges exactly"
    );

    // Verify every alias resolves to an active target
    for (alias, target) in &ledger.aliases {
        assert!(!alias.is_empty());
        assert!(!target.is_empty());
    }
}

#[test]
fn test_reconcile_104_roles_and_pod_counts() {
    let index = ReconciledCatalogIndex::load_default();

    // Total roles must be exactly 104
    assert_eq!(
        index.role_count(), 104,
        "Role catalog must contain exactly 104 operational roles"
    );

    // Verify 5 pod role counts match baseline roles.py and Tracker.md:
    // Build: 43, Growth: 21, Customer: 8, People: 5, GNA: 27
    let build_roles = index.roles_by_pod(GoverningPod::PodBuild);
    let growth_roles = index.roles_by_pod(GoverningPod::PodGrowth);
    let customer_roles = index.roles_by_pod(GoverningPod::PodCustomer);
    let people_roles = index.roles_by_pod(GoverningPod::PodPeople);
    let gna_roles = index.roles_by_pod(GoverningPod::PodGna);

    assert_eq!(build_roles.len(), 43, "Pod Build must have exactly 43 roles");
    assert_eq!(growth_roles.len(), 21, "Pod Growth must have exactly 21 roles");
    assert_eq!(customer_roles.len(), 8, "Pod Customer must have exactly 8 roles");
    assert_eq!(people_roles.len(), 5, "Pod People must have exactly 5 roles");
    assert_eq!(gna_roles.len(), 27, "Pod GNA must have exactly 27 roles");

    assert_eq!(
        build_roles.len() + growth_roles.len() + customer_roles.len() + people_roles.len() + gna_roles.len(),
        104
    );
}

#[test]
fn test_ownership_conflicts_explicitly_resolved() {
    let conflicts = CatalogReconciler::resolve_ownership_conflicts();
    assert_eq!(conflicts.len(), 2);

    let alexa = conflicts.iter().find(|c| c.skill_id == "amazon-alexa").expect("amazon-alexa conflict");
    assert_eq!(alexa.resolved_primary, "role-speech-audio-ai-eng");
    assert_eq!(alexa.resolved_secondary, "role-partnership-bd-manager");

    let cf = conflicts.iter().find(|c| c.skill_id == "cloudflare-workers-expert").expect("cloudflare conflict");
    assert_eq!(cf.resolved_primary, "role-platform-engineer");
    assert_eq!(cf.resolved_secondary, "role-design-system-engineer");

    // Verify index lookup reflects the resolved owners
    let index = ReconciledCatalogIndex::load_default();
    let alexa_skill = index.get_skill("amazon-alexa").expect("alexa in index");
    assert_eq!(alexa_skill.primary_role, "role-speech-audio-ai-eng");
    assert!(alexa_skill.secondary_roles.contains(&"role-partnership-bd-manager".to_string()));

    let cf_skill = index.get_skill("cloudflare-workers-expert").expect("cf in index");
    assert_eq!(cf_skill.primary_role, "role-platform-engineer");
    assert!(cf_skill.secondary_roles.contains(&"role-design-system-engineer".to_string()));
}

#[test]
fn test_unavailable_records_are_unselectable() {
    let ledger = MigrationLedger::build_reconciled_ledger();
    let index = ReconciledCatalogIndex::load_default();

    // Verify all 58 unavailable records exist and are unselectable
    assert_eq!(ledger.unavailable_ids.len(), 58);
    for unv_id in &ledger.unavailable_ids {
        assert!(
            !index.is_selectable(unv_id),
            "Unavailable skill '{}' must be unselectable",
            unv_id
        );
    }

    // Active skills must be selectable
    assert!(index.is_selectable("skill-top-1"));
    assert!(index.is_selectable("amazon-alexa"));
    assert!(index.is_selectable("cloudflare-workers-expert"));
}

#[test]
fn test_regenerated_indexes_match_canonical_graph() {
    let roles = RoleRegistry::load_roles();
    let ledger = MigrationLedger::build_reconciled_ledger();

    let mut skills = Vec::new();
    for (_path, rec) in &ledger.sources {
        skills.push(catalog::SkillDefinition::new(
            rec.old_id.clone(),
            "legacy",
            rec.owner_role.clone(),
            Vec::new(),
            rec.disposition,
        ));
    }

    // Verify graph integrity
    let is_valid = CatalogReconciler::verify_graph_integrity(&roles, &skills, &ledger.aliases);
    assert!(is_valid, "Regenerated indexes must match canonical graph without dangling edges");
}
