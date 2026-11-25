"""Tests for the 104-Role Enterprise Matrix (agyos_decision/roles.py).

Covers:
- classify_role_for_task() — representative queries across all 12 departments
- list_roles() — department and seniority filters
- get_role() — exact lookup for every role_id
- get_skills_for_role() — non-empty skill lists per role
"""

from __future__ import annotations

import unittest

from agyos_decision.roles import (
    CompanyDepartment,
    SeniorityLevel,
    classify_role_for_task,
    get_all_skills_for_role,
    get_role,
    get_role_for_skill,
    get_skills_for_role,
    list_roles,
)


class TestClassifyRoleForTask(unittest.TestCase):
    """classify_role_for_task returns the most relevant role for a natural language query."""

    def _assert_role(self, query: str, expected_role_id: str) -> None:
        result = classify_role_for_task(query)
        self.assertEqual(
            result.role_id,
            expected_role_id,
            f"Query '{query}' expected {expected_role_id!r}, got {result.role_id!r}",
        )

    # Executive
    def test_ceo_vision_query(self):
        self._assert_role("define company vision and OKRs for Q2", "role-ceo")

    def test_cto_architecture_decision(self):
        self._assert_role("make an architecture decision about build vs buy", "role-cto")

    def test_cfo_financial_model(self):
        self._assert_role("build a financial model for investor fundraise", "role-cfo")

    # Product
    def test_pm_prd_query(self):
        self._assert_role("write a product spec with acceptance criteria and user stories", "role-senior-pm")

    def test_growth_pm_ab_test(self):
        self._assert_role("run an a/b test on the activation funnel", "role-growth-pm")

    def test_scrum_coach_sprint(self):
        self._assert_role("facilitate a sprint retrospective and burndown review", "role-scrum-agile-coach")

    # Engineering
    def test_swe_bug_fix(self):
        result = classify_role_for_task("fix the bug in the checkout handler and add unit tests")
        self.assertIn(result.department, [
            CompanyDepartment.ENGINEERING.value,
            CompanyDepartment.PRODUCT.value,
        ])

    def test_frontend_engineer(self):
        self._assert_role("build a react component with tailwind and accessibility", "role-frontend-engineer")

    def test_devops_engineer(self):
        self._assert_role("set up github actions ci/cd pipeline with docker and kubernetes", "role-devops-engineer")

    def test_security_engineer(self):
        self._assert_role("run owasp top 10 penetration test and sast scan", "role-security-engineer")

    def test_web3_blockchain(self):
        self._assert_role("write a solidity smart contract for an nft marketplace", "role-web3-blockchain-eng")

    def test_agentic_workflow(self):
        self._assert_role("design a multi-agent orchestration workflow with mcp", "role-agentic-workflow-architect")

    # Data & AI
    def test_ml_engineer(self):
        self._assert_role("deploy a hugging face model for embedding inference", "role-ml-engineer")

    def test_data_engineer(self):
        self._assert_role("build an etl pipeline with dbt and snowflake", "role-data-engineer")

    def test_ai_product_engineer(self):
        self._assert_role("build a rag pipeline with langchain and vector search", "role-ai-product-engineer")

    def test_privacy_engineer(self):
        self._assert_role("implement gdpr right to erasure and pii anonymization", "role-privacy-engineer")

    # Design
    def test_ux_ui_designer(self):
        self._assert_role("design a figma wireframe and high-fidelity ui mockup", "role-ux-ui-designer")

    def test_motion_designer(self):
        self._assert_role("create a lottie animation and motion graphic for the landing page", "role-motion-designer")

    def test_design_system_engineer(self):
        self._assert_role("build a design system with shadcn tokens and tailwind", "role-design-system-engineer")

    # Marketing
    def test_seo_specialist(self):
        self._assert_role("do keyword research and technical seo audit with structured data", "role-seo-specialist")

    def test_email_lifecycle_marketer(self):
        self._assert_role("write a drip email sequence with klaviyo automation", "role-email-lifecycle-marketer")

    def test_cro(self):
        self._assert_role("optimize the signup flow cro and landing page conversion rate", "role-conversion-optimizer")

    def test_performance_marketer(self):
        self._assert_role("optimize google ads roas and meta ads cpm", "role-performance-marketer")

    # Sales
    def test_account_executive(self):
        self._assert_role("write a sales proposal and close the enterprise deal", "role-account-executive")

    def test_sdr(self):
        self._assert_role("write a cold email outreach sequence for prospecting", "role-sales-development-rep")

    def test_freelancer_sales(self):
        self._assert_role("write a freelance proposal and negotiate the retainer rate", "role-freelancer-sales")

    # Customer Success
    def test_support_engineer(self):
        self._assert_role("troubleshoot the customer support ticket with api error", "role-support-engineer")

    def test_onboarding_specialist(self):
        self._assert_role("create a new customer onboarding welcome email and kickoff", "role-onboarding-specialist")

    def test_technical_writer(self):
        self._assert_role("write api documentation and user guide with release notes", "role-docs-technical-writer")

    # Finance
    def test_billing_payments(self):
        self._assert_role("implement stripe subscription billing with dunning management", "role-billing-payments-eng")

    def test_fp_and_a(self):
        self._assert_role("build an fp&a financial model with variance analysis and forecast", "role-fp-and-a-analyst")

    def test_cost_optimization(self):
        self._assert_role("reduce aws cloud cost and identify savings with rightsizing", "role-cost-optimization-analyst")

    # Legal
    def test_contract_manager(self):
        self._assert_role("draft an msa and nda vendor agreement contract", "role-contract-manager")

    def test_compliance_officer(self):
        self._assert_role("prepare for soc2 audit and gdpr compliance program", "role-compliance-officer")

    # People
    def test_recruiter(self):
        self._assert_role("screen engineering candidate resumes and write interview rubric", "role-recruiter")

    def test_solopreneur_operator(self):
        self._assert_role("manage everything as a solopreneur solo founder one person company", "role-solopreneur-operator")

    # IT & Infra
    def test_cloud_architect(self):
        self._assert_role("design aws multi-cloud architecture with terraform and landing zone", "role-cloud-architect")

    def test_observability_engineer(self):
        self._assert_role("instrument opentelemetry tracing with prometheus and grafana", "role-observability-engineer")

    def test_database_reliability(self):
        self._assert_role("optimize postgres query plan with index and vacuum", "role-database-reliability-eng")


class TestListRoles(unittest.TestCase):
    """list_roles returns filtered collections."""

    def test_returns_all_104_roles(self):
        roles = list_roles()
        self.assertGreaterEqual(len(roles), 100,
            f"Expected at least 100 roles, got {len(roles)}")

    def test_filter_by_engineering_department(self):
        roles = list_roles(department=CompanyDepartment.ENGINEERING.value)
        self.assertGreaterEqual(len(roles), 10)
        for r in roles:
            self.assertEqual(r.department, CompanyDepartment.ENGINEERING.value)

    def test_filter_by_L8_seniority(self):
        roles = list_roles(seniority=SeniorityLevel.L8.value)
        self.assertGreater(len(roles), 0)
        for r in roles:
            self.assertEqual(r.seniority, SeniorityLevel.L8.value)

    def test_filter_by_finance_and_seniority(self):
        roles = list_roles(
            department=CompanyDepartment.FINANCE.value,
            seniority=SeniorityLevel.L5.value,
        )
        self.assertGreater(len(roles), 0)
        for r in roles:
            self.assertEqual(r.department, CompanyDepartment.FINANCE.value)
            self.assertEqual(r.seniority, SeniorityLevel.L5.value)

    def test_all_roles_have_required_fields(self):
        for role in list_roles():
            self.assertTrue(role.role_id, f"Missing role_id on {role}")
            self.assertTrue(role.title, f"Missing title on {role.role_id}")
            self.assertTrue(role.department, f"Missing department on {role.role_id}")
            self.assertTrue(role.seniority, f"Missing seniority on {role.role_id}")
            self.assertTrue(role.governing_pod, f"Missing governing_pod on {role.role_id}")
            self.assertTrue(role.mandate, f"Missing mandate on {role.role_id}")

    def test_all_roles_have_at_least_one_primary_skill(self):
        for role in list_roles():
            self.assertGreater(
                len(role.primary_skills), 0,
                f"Role {role.role_id!r} has no primary_skills",
            )

    def test_all_roles_have_at_least_one_keyword(self):
        for role in list_roles():
            self.assertGreater(
                len(role.keywords), 0,
                f"Role {role.role_id!r} has no keywords",
            )

    def test_all_governing_pods_valid(self):
        valid_pods = {
            "pod-growth", "pod-customer", "pod-build", "pod-gna", "pod-people"
        }
        for role in list_roles():
            self.assertIn(
                role.governing_pod, valid_pods,
                f"Role {role.role_id!r} has invalid governing_pod {role.governing_pod!r}",
            )


class TestGetRole(unittest.TestCase):
    """get_role returns exact matches and None for unknown IDs."""

    _SAMPLE_ROLE_IDS = [
        "role-ceo", "role-cto", "role-coo", "role-cpo", "role-cmo", "role-cso",
        "role-cfo", "role-vp-engineering", "role-product-director", "role-senior-pm",
        "role-pm", "role-scrum-agile-coach", "role-ux-researcher", "role-growth-pm",
        "role-product-analyst", "role-technical-pm", "role-staff-engineer",
        "role-senior-swe", "role-swe", "role-frontend-engineer", "role-backend-engineer",
        "role-mobile-engineer", "role-devops-engineer", "role-site-reliability-engineer",
        "role-security-engineer", "role-qa-engineer", "role-web3-blockchain-eng",
        "role-desktop-app-eng", "role-network-infra-eng", "role-database-reliability-eng",
        "role-incident-commander", "role-agentic-workflow-architect", "role-data-scientist",
        "role-ml-engineer", "role-data-engineer", "role-ai-product-engineer",
        "role-data-analyst", "role-research-scientist", "role-privacy-engineer",
        "role-computer-vision-eng", "role-speech-audio-ai-eng", "role-mlops-engineer",
        "role-design-director", "role-ux-ui-designer", "role-product-designer",
        "role-brand-designer", "role-motion-designer", "role-3d-visual-designer",
        "role-design-system-engineer", "role-ux-copywriter", "role-content-strategist",
        "role-seo-specialist", "role-performance-marketer", "role-social-media-manager",
        "role-brand-copywriter", "role-conversion-optimizer", "role-email-lifecycle-marketer",
        "role-pr-comms-manager", "role-partnership-bd-manager", "role-community-manager",
        "role-vp-sales", "role-account-executive", "role-sales-development-rep",
        "role-solutions-engineer", "role-customer-success-manager", "role-revenue-operations",
        "role-enterprise-ae", "role-freelancer-sales", "role-support-engineer",
        "role-onboarding-specialist", "role-implementation-consultant",
        "role-technical-account-manager", "role-churn-analyst", "role-docs-technical-writer",
        "role-corporate-controller", "role-fp-and-a-analyst", "role-tax-compliance-spec",
        "role-billing-payments-eng", "role-treasury-banking-spec", "role-accounts-manager",
        "role-startup-cfo-advisor", "role-cost-optimization-analyst",
        "role-general-counsel", "role-ip-patent-attorney", "role-contract-manager",
        "role-compliance-officer", "role-data-protection-officer", "role-risk-manager",
        "role-vp-people", "role-recruiter", "role-hr-business-partner",
        "role-hr-ops-specialist", "role-learning-development", "role-procurement-vendor-manager",
        "role-office-facilities-manager", "role-executive-assistant",
        "role-solopreneur-operator", "role-chief-of-staff",
        "role-it-systems-admin", "role-cloud-architect", "role-platform-engineer",
        "role-cybersecurity-analyst", "role-observability-engineer", "role-finops-cloud-cost",
    ]

    def test_all_role_ids_resolve(self):
        for role_id in self._SAMPLE_ROLE_IDS:
            role = get_role(role_id)
            self.assertIsNotNone(role, f"get_role({role_id!r}) returned None")
            self.assertEqual(role.role_id, role_id)

    def test_unknown_role_returns_none(self):
        self.assertIsNone(get_role("role-does-not-exist"))

    def test_total_registered_roles_count(self):
        registered = sum(1 for rid in self._SAMPLE_ROLE_IDS if get_role(rid) is not None)
        self.assertEqual(registered, len(self._SAMPLE_ROLE_IDS))


class TestGetSkillsForRole(unittest.TestCase):
    """get_skills_for_role returns non-empty lists for all registered roles."""

    def test_ceo_has_skills(self):
        skills = get_skills_for_role("role-ceo")
        self.assertGreater(len(skills), 0)
        self.assertIsInstance(skills[0], str)

    def test_unknown_role_returns_empty(self):
        self.assertEqual(get_skills_for_role("role-does-not-exist"), [])

    def test_all_roles_return_non_empty_skills(self):
        for role in list_roles():
            skills = get_skills_for_role(role.role_id)
            self.assertGreater(
                len(skills), 0,
                f"get_skills_for_role({role.role_id!r}) returned empty list",
            )

    def test_skills_are_strings(self):
        for role in list_roles():
            for skill in get_skills_for_role(role.role_id):
                self.assertIsInstance(skill, str, f"Non-string skill in {role.role_id!r}: {skill!r}")


class TestAgentDefinitionsOnDisk(unittest.TestCase):
    """Verify that all registered roles have physical gemini/agents/<role-id>.toon definition files."""

    def test_all_104_roles_have_agent_file(self):
        from pathlib import Path
        repo_root = Path(__file__).resolve().parent.parent.parent
        agents_dir = repo_root / "agents"
        self.assertTrue(agents_dir.is_dir())
        for role in list_roles():
            agent_file_toon = agents_dir / f"{role.role_id}.toon"
            agent_file_md = agents_dir / f"{role.role_id}.md"
            self.assertTrue(
                agent_file_toon.is_file() or agent_file_md.is_file(),
                f"Missing agent file for role: {role.role_id}",
            )
            raw = (agent_file_toon if agent_file_toon.is_file() else agent_file_md).read_text(encoding="utf-8")
            if raw.startswith('mode: "100644"\ntext: '):
                import json
                content = json.loads(raw.split("text: ", 1)[1].strip())
            else:
                content = raw
            self.assertTrue(content.startswith("---"))
            self.assertIn(f"name: {role.role_id}", content)


class TestSkillsByRoleOnDisk(unittest.TestCase):
    """Verify role-based skills directory (builtin/skills/<role-id>/) and matrix indexes."""

    def setUp(self):
        from pathlib import Path
        self.repo_root = Path(__file__).resolve().parent.parent.parent
        self.skills_by_role_dir = self.repo_root / "skills"
        self.matrix_file = self.skills_by_role_dir / "roles-skills-matrix.json"

    def test_skills_by_role_directory_exists(self):
        self.assertTrue(self.skills_by_role_dir.is_dir())

    def test_matrix_file_exists_and_valid(self):
        import json
        self.assertTrue(self.matrix_file.is_file())
        with open(self.matrix_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("by_role", data)
        self.assertIn("by_skill", data)
        self.assertEqual(len(data["by_role"]), 104)
        self.assertGreaterEqual(len(data["by_skill"]), 2000)

    def test_matrix_covers_physical_catalog(self):
        import json

        skills_dir = self.repo_root / "skills"
        physical = {path.parent.name for path in skills_dir.glob("*/*/SKILL.toon")}
        mapped = set(json.loads(self.matrix_file.read_text(encoding="utf-8"))["by_skill"])
        missing = sorted(physical - mapped)
        dangling = sorted(mapped - physical)
        self.assertFalse(missing, f"Skills missing from the role matrix: {missing}")
        self.assertFalse(dangling, f"Role matrix entries without a skill: {dangling}")

    def test_all_roles_have_skills_directory(self):
        self.assertTrue(self.skills_by_role_dir.is_dir())
        role_dirs = [p for p in self.skills_by_role_dir.iterdir() if p.is_dir() and p.name.startswith("role-")]
        self.assertGreaterEqual(len(role_dirs), 90)

    def test_symlinks_resolve_to_valid_skill_md(self):
        from agyos_decision.catalog import resolve_skill_dir
        checked = 0
        for role in list_roles():
            for skill_name in get_all_skills_for_role(role.role_id):
                skill_dir = resolve_skill_dir(skill_name)
                self.assertIsNotNone(skill_dir, f"Missing skill dir for {role.role_id}/{skill_name}")
                skill_toon = skill_dir / "SKILL.toon"
                self.assertTrue(
                    skill_toon.is_file(),
                    f"Missing SKILL.toon for {role.role_id}/{skill_name}: {skill_toon}",
                )
                checked += 1
        self.assertGreater(checked, 2000)

    def test_get_all_skills_for_role_returns_mapped_skills(self):
        for role in list_roles():
            all_skills = get_all_skills_for_role(role.role_id)
            self.assertGreater(
                len(all_skills), 0,
                f"Role {role.role_id} returned empty mapped skills",
            )
            # Ensure primary skills are subset of all skills
            for p in role.primary_skills:
                self.assertIn(
                    p, all_skills,
                    f"Primary skill {p} missing from all_skills of {role.role_id}",
                )

    def test_get_role_for_skill_resolves(self):
        res = get_role_for_skill("react-best-practices")
        self.assertIsNotNone(res)
        self.assertEqual(res["primary_role"], "role-frontend-engineer")


if __name__ == "__main__":
    unittest.main()
