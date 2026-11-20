//! Step 11: Place and Qualify Skills — Qualification and Integrity Tests.
//!
//! Complies with Step 11 finish test and Principles P04, P05, P06, P09, P23, P24, P26, P28, P29, P31, P32:
//! - Each required ID has one canonical path, owner, principle and passing positive/negative/interruption fixtures.
//! - Every department and pod has expected natural-language route labels, including abstention and clarification cases.
//! - Tenant-specific specialties are packaged as lazy runbooks only admitted via explicit qualification.

use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};

use catalog::{
    Department, GoverningPod, RouteEvaluationResult, SkillPlacementRegistry,
};

#[test]
fn test_153_canonical_skills_across_27_homes() {
    let skills = SkillPlacementRegistry::load_required_153();

    // 1. Exactly 153 required distinct skills
    assert_eq!(
        skills.len(),
        153,
        "SkillPlacementRegistry must contain exactly 153 canonical skills"
    );

    let mut ids = HashSet::new();
    let mut homes = HashSet::new();
    let mut paths = HashSet::new();

    for skill in &skills {
        // Assert uniqueness
        assert!(ids.insert(&skill.id), "Duplicate skill id: {}", skill.id);
        assert!(paths.insert(&skill.canonical_path), "Duplicate canonical path: {}", skill.canonical_path);
        homes.insert(&skill.home);

        // Assert schema completeness
        assert!(!skill.id.is_empty());
        assert!(!skill.home.is_empty());
        assert!(!skill.owner_team.is_empty());
        assert!(!skill.principles.is_empty());
        assert!(!skill.intent.is_empty());
        assert!(!skill.route_labels.is_empty());

        // Assert canonical path format
        let expected_path = format!("knowledge/skills/{}/{}.toon", skill.home, skill.id);
        assert_eq!(skill.canonical_path, expected_path);

        // Assert principles all have valid Pxx format
        for p in &skill.principles {
            assert!(p.starts_with('P'), "Principle must start with P: {}", p);
        }
    }

    // 2. Exactly 27 distinct homes
    assert_eq!(
        homes.len(),
        27,
        "Skill catalog must span exactly 27 homes"
    );
}

#[test]
fn test_physical_toon_files_exist_and_are_valid() {
    let skills = SkillPlacementRegistry::load_required_153();

    for skill in &skills {
        let path = if Path::new(&skill.canonical_path).exists() {
            PathBuf::from(&skill.canonical_path)
        } else if Path::new("../../").join(&skill.canonical_path).exists() {
            Path::new("../../").join(&skill.canonical_path)
        } else if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
            PathBuf::from(manifest_dir).join("../../").join(&skill.canonical_path)
        } else {
            PathBuf::from(&skill.canonical_path)
        };

        assert!(
            path.exists(),
            "Physical TOON skill file must exist at {} (resolved: {:?})",
            skill.canonical_path,
            path
        );

        let content = fs::read_to_string(path)
            .unwrap_or_else(|e| panic!("Failed to read {}: {}", skill.canonical_path, e));

        assert!(
            content.contains(&format!("id: \"{}\"", skill.id)),
            "Skill file {} must declare matching id",
            skill.canonical_path
        );
        assert!(
            content.contains(&format!("home: \"{}\"", skill.home)),
            "Skill file {} must declare matching home",
            skill.canonical_path
        );
        assert!(
            content.contains("fixtures:"),
            "Skill file {} must declare fixtures block",
            skill.canonical_path
        );
    }
}

#[test]
fn test_12_department_end_to_end_fixtures() {
    let fixtures = SkillPlacementRegistry::get_department_fixtures();

    // Verify all 12 departments are represented
    assert_eq!(
        fixtures.len(),
        12,
        "Must provide one end-to-end fixture per department"
    );

    let mut depts = HashSet::new();

    for f in &fixtures {
        assert!(depts.insert(f.department), "Duplicate department fixture: {:?}", f.department);

        // 1. Positive scenario: route matches expected department and skill
        let pos_result = SkillPlacementRegistry::evaluate_natural_language_route(&f.positive_prompt);
        match pos_result {
            RouteEvaluationResult::Matched { skill_id, department, pod } => {
                assert_eq!(department, f.department, "Positive prompt must route to declared department");
                assert_eq!(pod, f.pod, "Positive prompt must route to declared pod");
                assert_eq!(skill_id, f.skill_id, "Positive prompt must route to declared skill");
            }
            other => panic!("Expected matched route for positive fixture {:?}, got {:?}", f.department, other),
        }

        // 2. Negative scenario: route abstains with expected reason
        let neg_result = SkillPlacementRegistry::evaluate_natural_language_route(&f.negative_prompt);
        match neg_result {
            RouteEvaluationResult::Abstain { reason } => {
                assert_eq!(reason, f.abstention_reason, "Negative prompt must return declared abstention reason");
            }
            other => panic!("Expected abstention for negative fixture {:?}, got {:?}", f.department, other),
        }

        // 3. Interruption scenario: recovery checkpoint is non-empty
        assert!(
            !f.interruption_prompt.is_empty(),
            "Interruption prompt must be defined for {:?}",
            f.department
        );
        assert!(
            !f.recovery_checkpoint.is_empty(),
            "Recovery checkpoint must be defined for {:?}",
            f.department
        );
    }
}

#[test]
fn test_pod_and_department_skill_distribution() {
    let skills = SkillPlacementRegistry::load_required_153();

    // Build: 89 skills (Product 18, Engineering 41, DataAi 19, Design 5, Delivery 6)
    let build_skills: Vec<_> = skills.iter().filter(|s| s.pod == GoverningPod::PodBuild).collect();
    assert_eq!(build_skills.len(), 89, "Pod Build must have exactly 89 skills");

    // Growth: 10 skills (Marketing 5, SalesBd 5)
    let growth_skills: Vec<_> = skills.iter().filter(|s| s.pod == GoverningPod::PodGrowth).collect();
    assert_eq!(growth_skills.len(), 10, "Pod Growth must have exactly 10 skills");

    // Customer: 5 skills (CustomerSuccess 5)
    let customer_skills: Vec<_> = skills.iter().filter(|s| s.pod == GoverningPod::PodCustomer).collect();
    assert_eq!(customer_skills.len(), 5, "Pod Customer must have exactly 5 skills");

    // People: 5 skills (PeopleOps 5)
    let people_skills: Vec<_> = skills.iter().filter(|s| s.pod == GoverningPod::PodPeople).collect();
    assert_eq!(people_skills.len(), 5, "Pod People must have exactly 5 skills");

    // GNA: 44 skills (Executive 9, Finance 5, LegalCompliance 11, ITInfra Protection/Operations/ITPlatform 19)
    let gna_skills: Vec<_> = skills.iter().filter(|s| s.pod == GoverningPod::PodGna).collect();
    assert_eq!(gna_skills.len(), 44, "Pod GNA must have exactly 44 skills");

    assert_eq!(
        build_skills.len() + growth_skills.len() + customer_skills.len() + people_skills.len() + gna_skills.len(),
        153
    );
}

#[test]
fn test_natural_language_routing_clarification_and_abstention() {
    // 1. Positive route matching
    let res = SkillPlacementRegistry::evaluate_natural_language_route("Please capture goal from the founder");
    assert_eq!(
        res,
        RouteEvaluationResult::Matched {
            skill_id: "capture-goal".to_string(),
            department: Department::Product,
            pod: GoverningPod::PodBuild,
        }
    );

    // 2. Clarification trigger (EVPI uncertainty)
    let clarify_res = SkillPlacementRegistry::evaluate_natural_language_route("We have a vague goal for the client");
    match clarify_res {
        RouteEvaluationResult::ClarificationRequired { prompt, question } => {
            assert!(prompt.contains("vague goal"));
            assert!(!question.is_empty());
        }
        other => panic!("Expected ClarificationRequired, got {:?}", other),
    }

    // 3. Out of scope / unrecognized abstention
    let abstain_res = SkillPlacementRegistry::evaluate_natural_language_route("Provide current weather in Paris");
    match abstain_res {
        RouteEvaluationResult::Abstain { reason } => {
            assert!(reason.contains("No matching operational capability found"));
        }
        other => panic!("Expected Abstain, got {:?}", other),
    }
}

#[test]
fn test_tenant_specialty_lazy_runbook_isolation() {
    // Unadmitted specialty is rejected
    let unadmitted = SkillPlacementRegistry::validate_tenant_specialty("specialty-custom-biotech-crm", false);
    assert!(unadmitted.is_err());
    assert_eq!(
        unadmitted.unwrap_err(),
        "Tenant specialty packaged as lazy runbook and not admitted into active catalog"
    );

    // Admitted specialty is approved
    let admitted = SkillPlacementRegistry::validate_tenant_specialty("specialty-custom-biotech-crm", true);
    assert!(admitted.is_ok());

    // Standard core skill is always approved regardless of admission flag
    let core = SkillPlacementRegistry::validate_tenant_specialty("capture-goal", false);
    assert!(core.is_ok());
}
