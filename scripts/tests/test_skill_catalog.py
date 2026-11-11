"""Regression tests for the read-only skill catalog quality audit."""

import tempfile
import unittest
from pathlib import Path

from scripts.audit_skill_catalog import SKILLS_DIR, audit_catalog


class SkillCatalogAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_skill(self, name, description, body):
        skill_dir = self.skills_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n{body}",
            encoding="utf-8",
        )
        return skill_file

    def codes(self, report):
        return {finding["code"] for finding in report["findings"]}

    def review_codes(self, report):
        return {finding["code"] for finding in report["review_candidates"]}

    def test_clean_skill_and_valid_local_reference_have_no_findings(self):
        skill_file = self.write_skill(
            "alpha-skill",
            "Use Alpha for reviewing Python API compatibility and migration steps.",
            "Read the [migration guide](references/migration.md) before changing APIs.\n",
        )
        reference = skill_file.parent / "references" / "migration.md"
        reference.parent.mkdir()
        reference.write_text("# Migration\n", encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["skill_count"], 1)
        self.assertEqual(report["findings"], [])

    def test_reports_noncanonical_id_placeholder_long_file_and_broken_link(self):
        body = "[missing guide](references/missing.md)\n" + "detail\n" * 296
        self.write_skill(
            "weak_skill",
            "One sentence - what this skill does and when to invoke it",
            body,
        )

        report = audit_catalog(self.skills_dir)

        self.assertTrue(
            {
                "placeholder-description",
                "runbook-too-long",
                "broken-local-link",
            }.issubset(self.codes(report))
        )
        self.assertIn("noncanonical-id", self.review_codes(report))

    def test_reports_malformed_frontmatter_without_aborting_catalog_scan(self):
        skill_dir = self.skills_dir / "broken-header"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: [invalid\ndescription: broken\n---\nBody\n",
            encoding="utf-8",
        )
        self.write_skill(
            "valid-skill",
            "Use this skill to check valid frontmatter handling in a catalog.",
            "Body\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["skill_count"], 2)
        self.assertIn("invalid-frontmatter", self.codes(report))

    def test_json_fragment_description_is_rejected(self):
        skill_dir = self.skills_dir / "phone-tool"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: phone-tool\ndescription: 'api_base\": \"https://api.example.com/v1\"'\n---\nBody\n",
            encoding="utf-8",
        )

        report = audit_catalog(self.skills_dir)

        self.assertIn("placeholder-description", self.codes(report))

    def test_long_description_is_reported_as_a_review_candidate(self):
        self.write_skill(
            "verbose-skill",
            "Use this skill to verify an intentionally verbose discovery description.",
            "Detailed body.\n",
        )
        skill_file = self.skills_dir / "verbose-skill" / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        original = "Use this skill to verify an intentionally verbose discovery description."
        skill_file.write_text(text.replace(original, "Useful discovery detail. " * 16), encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        self.assertIn("long-description", self.review_codes(report))

    def test_duplicate_bodies_are_reported_as_review_groups_not_errors(self):
        body = "# Shared procedure\n\nCheck the supplied file and report findings.\n"
        self.write_skill("first-skill", "Use for first domain-specific review tasks.", body)
        self.write_skill("second-skill", "Use for second domain-specific review tasks.", body)

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["findings"], [])
        self.assertEqual(report["duplicate_body_groups"], [["first-skill", "second-skill"]])

    def test_duplicate_detection_uses_preserved_full_runbook_reference(self):
        for name in ("first-skill", "second-skill"):
            skill_file = self.write_skill(
                name,
                f"Use this skill to review the {name} implementation details.",
                "# Short entrypoint\nRead the full guide.\n",
            )
            reference = skill_file.parent / "references" / "FULL_RUNBOOK.md"
            reference.parent.mkdir()
            reference.write_text("# Shared detailed procedure\n\nSame source body.\n", encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["duplicate_body_groups"], [["first-skill", "second-skill"]])

    def test_duplicate_detection_does_not_group_shared_wrappers_with_distinct_references(self):
        for name, details in (("first-skill", "First domain procedure."), ("second-skill", "Second domain procedure.")):
            skill_file = self.write_skill(
                name,
                f"Use this skill to review the {name} implementation details.",
                "# Short entrypoint\nRead the full guide.\n",
            )
            reference = skill_file.parent / "references" / "FULL_RUNBOOK.md"
            reference.parent.mkdir()
            reference.write_text(f"# Detailed procedure\n\n{details}\n", encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["duplicate_body_groups"], [])

    def test_external_and_anchor_links_are_not_treated_as_missing_files(self):
        self.write_skill(
            "linked-skill",
            "Use this skill to verify local links and external references.",
            "[site](https://example.com) [section](#details)\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["findings"], [])

    def test_cross_skill_relative_link_is_resolved_within_repository_boundary(self):
        self.write_skill(
            "first-skill",
            "Use this skill to check cross-skill links in a catalog.",
            "See [second skill](../second-skill/SKILL.md).\n",
        )
        self.write_skill(
            "second-skill",
            "Use this skill to validate a cross-skill relative link.",
            "Body\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["findings"], [])

    def test_yaml_example_in_code_fence_is_not_duplicate_frontmatter(self):
        self.write_skill(
            "template-skill",
            "Use this skill to create reusable skill metadata templates.",
            "```yaml\n---\nname: example\ndescription: Example only.\n---\n```\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertNotIn("duplicate-frontmatter", self.codes(report))

    def test_deprecation_notice_is_not_a_placeholder_description(self):
        self.write_skill(
            "legacy-skill",
            "[Deprecated: use replacement-skill] Legacy workflow. Route new requests to replacement-skill.",
            "Body\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertNotIn("placeholder-description", self.codes(report))

    def test_skill_local_reference_links_are_checked(self):
        skill_file = self.write_skill(
            "reference-skill",
            "Use this skill to validate linked reference material in the catalog.",
            "Read [details](references/details.md).\n",
        )
        reference = skill_file.parent / "references" / "details.md"
        reference.parent.mkdir()
        reference.write_text("See [missing](not-present.md).\n", encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        broken = [item for item in report["findings"] if item["code"] == "broken-local-link"]
        self.assertEqual(len(broken), 1)
        self.assertTrue(broken[0]["path"].endswith("references/details.md"))

    def test_root_relative_web_path_is_a_review_candidate_not_a_missing_file(self):
        self.write_skill(
            "web-doc-skill",
            "Use this skill to cite external vendor documentation accurately.",
            "See [vendor docs](/en/docs/agents-and-tools/agent-skills/overview).\n",
        )

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["findings"], [])
        self.assertIn("root-relative-link", self.review_codes(report))

    def test_dependency_markdown_is_outside_the_skill_audit_boundary(self):
        skill_file = self.write_skill(
            "vendored-skill",
            "Use this skill to inspect a vendored tool integration.",
            "Read the vendored package docs.\n",
        )
        dependency_doc = skill_file.parent / "scripts" / "node_modules" / "pkg" / "README.md"
        dependency_doc.parent.mkdir(parents=True)
        dependency_doc.write_text("[missing](not-shipped.md)\n", encoding="utf-8")

        report = audit_catalog(self.skills_dir)

        self.assertEqual(report["findings"], [])

    def test_keyvault_key_and_secret_skills_use_their_own_clients(self):
        keys = (SKILLS_DIR / "azure-keyvault-keys-ts" / "SKILL.md").read_text()
        secrets = (SKILLS_DIR / "azure-keyvault-secrets-ts" / "SKILL.md").read_text()

        self.assertIn("new KeyClient", keys)
        self.assertNotIn("new SecretClient", keys)
        self.assertIn("new SecretClient", secrets)
        self.assertNotIn("new KeyClient", secrets)

    def test_audio_transcriber_does_not_call_an_undefined_model_helper(self):
        skill_dir = SKILLS_DIR / "audio-transcriber"
        skill = (skill_dir / "references" / "FULL_RUNBOOK.md").read_text()

        self.assertNotIn("call_ai_model(", skill)
        self.assertIn("summarizer", skill)

    def test_python_architect_frontmatter_is_not_led_by_node_backend_guidance(self):
        skill = (SKILLS_DIR / "elite-python-architect" / "SKILL.md").read_text()
        full_guide = (SKILLS_DIR / "elite-python-architect" / "references" / "FULL_RUNBOOK.md").read_text()

        self.assertNotIn("(Node.js · Express · TypeScript · Microservices)", skill[:2500])
        self.assertIn("nodejs-backend-patterns", skill[:2500])
        self.assertIn("legacy-node-backend-guide.md", full_guide)

    def test_production_audit_is_scoped_read_only_and_evidence_based_by_default(self):
        runbook = (
            SKILLS_DIR
            / "production-code-audit"
            / "references"
            / "FULL_RUNBOOK.md"
        ).read_text(encoding="utf-8")

        self.assertIn("The default audit is read-only.", runbook)
        self.assertIn("change only the authorized files", runbook)
        self.assertIn("state the evidence and coverage limits", runbook)
        self.assertIn("do not state an improvement percentage", runbook)
        self.assertNotIn("Fix everything automatically", runbook)
        self.assertNotIn("Do all of this without asking the user", runbook)

    def test_imported_scaffold_skills_have_domain_specific_steps(self):
        expected_markers = {
            "scientific-research": "research question",
            "secure-env-secrets-manager": "never print secret values",
            "skill-seekers": "skill-seekers create",
            "speed-reader": "macOS",
            "superpowers-lab": "experimental skills",
            "twitter-article-publisher": "Premium Plus",
            "ui-design-guidelines": "design-engineering guide",
            "vector-semantic-file-search": "embedding provider",
            "web-fuzzing-ffuf": "written scope",
            "win11-system-manager": "archived and read-only",
        }

        for name, marker in expected_markers.items():
            with self.subTest(skill=name):
                content = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(marker.casefold(), content.casefold())
                self.assertNotIn(
                    "This skill provides guidance and patterns for",
                    content,
                )
                if name == "scientific-research":
                    self.assertIn(
                        "source: \"https://github.com/K-Dense-AI/scientific-agent-skills\"",
                        content,
                    )
                if name == "win11-system-manager":
                    for prerequisite in ("Windows 11", "PowerShell 7+", "Claude Code", "Internet access"):
                        self.assertIn(prerequisite.casefold(), content.casefold())

    def test_duplicate_pairs_have_distinct_supported_scopes(self):
        expected_markers = {
            "agents-v2-py": "compatibility pointer",
            "hosted-agents-v2-py": "HostedAgentDefinition",
            "context-restore": "first unfinished authorized step",
            "refactor-context-restore": "approved refactoring plan",
            "error-multi-review": "reproduce the error",
            "perf-test-review": "comparable baseline measurements",
        }

        for name, marker in expected_markers.items():
            with self.subTest(skill=name):
                root = SKILLS_DIR / name
                text = (root / "SKILL.md").read_text(encoding="utf-8")
                reference = root / "references" / "FULL_RUNBOOK.md"
                if reference.exists():
                    text += "\n" + reference.read_text(encoding="utf-8")
                self.assertIn(marker.casefold(), text.casefold())
                self.assertNotIn("resources/implementation-playbook.md", text)

        context = (SKILLS_DIR / "context-restore" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("context-restore --", context)

    def test_legacy_duplicate_ids_point_to_canonical_runbooks_and_keep_assets(self):
        aliases = {
            "brand-guidelines-community": "brand-design-system",
            "brand-guidelines": "brand-design-system",
            "error-analysis": "diagnostics-analysis",
            "documentation-generation-doc-generate": "doc-generator",
            "internal-comms-community": "internal-team-communications",
            "tech-debt-cleanup": "codebase-tech-debt",
            "fp-react": "fp-ts-react",
            "fp-pragmatic": "fp-ts-pragmatic",
            "fp-errors": "fp-ts-errors",
            "remotion-best-practices": "remotion-video-creation",
        }
        for alias, canonical in aliases.items():
            with self.subTest(alias=alias):
                text = (SKILLS_DIR / alias / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"../{canonical}/SKILL.md", text)
                self.assertTrue((SKILLS_DIR / canonical / "SKILL.md").is_file())

        resource_aliases = {
            "error-analysis/resources/implementation-playbook.md":
                "../../diagnostics-analysis/resources/implementation-playbook.md",
            "documentation-generation-doc-generate/resources/implementation-playbook.md":
                "../../doc-generator/resources/implementation-playbook.md",
            "tech-debt-cleanup/references/FULL_RUNBOOK.md":
                "../../codebase-tech-debt/references/FULL_RUNBOOK.md",
            "fp-react/references/FULL_RUNBOOK.md": "../../fp-ts-react/references/FULL_RUNBOOK.md",
            "fp-pragmatic/references/FULL_RUNBOOK.md": "../../fp-ts-pragmatic/references/FULL_RUNBOOK.md",
            "fp-errors/references/FULL_RUNBOOK.md": "../../fp-ts-errors/references/FULL_RUNBOOK.md",
        }
        for relative_path, target in resource_aliases.items():
            with self.subTest(path=relative_path):
                path = SKILLS_DIR / relative_path
                contents = path.read_text(encoding="utf-8")
                self.assertIn(target, contents)
                self.assertTrue((path.parent / target).resolve().is_file())
                if relative_path == "tech-debt-cleanup/references/FULL_RUNBOOK.md":
                    self.assertEqual(
                        contents,
                        "# Compatibility reference pointer\n\n"
                        "Use the canonical [codebase-tech-debt full runbook]"
                        "(../../codebase-tech-debt/references/FULL_RUNBOOK.md). "
                        "This path remains for compatibility with existing links.\n",
                    )

        examples = (
            "3p-updates.md",
            "company-newsletter.md",
            "faq-answers.md",
            "general-comms.md",
        )
        for example in examples:
            self.assertTrue((SKILLS_DIR / "internal-team-communications/examples" / example).is_file())

    def test_openwhispr_skill_documents_setup_privacy_and_mcp_boundaries(self):
        path = SKILLS_DIR / "openwhispr" / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        import yaml

        metadata = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(metadata["metadata"]["version"], "1.0.2")
        for marker in (
            "https://github.com/OpenWhispr/openwhispr",
            "https://docs.openwhispr.com/help/privacy/where-your-data-goes",
            "https://docs.openwhispr.com/integrations/mcp",
            "System Audio",
            "The separate **Screen Recording** permission is for optional voice-agent screen context",
            "Claude Connectors requests all documented scopes",
            "a read-only smoke test does not limit the granted permissions",
            "For API-key clients, verify the configured scope set",
            "For those clients, grant only the scopes needed",
            "Dictation**, **Note Recording**, and **Audio Upload**",
            "do not commit it",
            "explicit user authorization",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker.casefold(), text.casefold())

    def test_remotion_legacy_rule_paths_point_to_canonical_rules(self):
        legacy = SKILLS_DIR / "remotion-best-practices" / "rules"
        canonical = SKILLS_DIR / "remotion-video-creation" / "rules"
        legacy_rules = tuple(legacy.rglob("*.md"))
        self.assertEqual(len(legacy_rules), 28)
        for path in legacy_rules:
            with self.subTest(rule=path.relative_to(legacy)):
                relative = path.relative_to(legacy).as_posix()
                target = f"../../remotion-video-creation/rules/{relative}"
                self.assertEqual(
                    path.read_text(encoding="utf-8"),
                    "# Compatibility reference pointer\n\n"
                    f"Use the canonical [Remotion rule]({target}). "
                    "This legacy path remains for compatibility with existing links.\n",
                )
                self.assertTrue((path.parent / target).resolve().is_file())

        for asset in (
            "assets/charts-bar-chart.tsx",
            "assets/text-animations-typewriter.tsx",
            "assets/text-animations-word-highlight.tsx",
        ):
            with self.subTest(asset=asset):
                old_asset = legacy / asset
                canonical_asset = canonical / asset
                self.assertTrue(old_asset.is_file())
                self.assertEqual(old_asset.read_bytes(), canonical_asset.read_bytes())


if __name__ == "__main__":
    unittest.main()
