"""Offline capability cases and catalog integrity checks for skill selection."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

from agyos_decision import skills_router as router
from agyos_decision.catalog import canonical_entry

ROOT = Path(__file__).resolve().parents[2]


class RoutingTests(unittest.TestCase):
    CASES = {
        "fix python crash": "diagnosing-bugs",
        "debug a React regression": "diagnosing-bugs",
        "animate modal transition": "motion-patterns",
        "compare Postgres vs SQLite tradeoffs": "council",
        "free tier infrastructure": "agyos-free-infra-catalog",
        "write literature review": "agyos-academic-research",
        "update rules and skills and decision routing": "agyos-decision",
        "design responsive interface": "frontend-design-direction",
        "optimize slow Python code latency": "benchmark-optimization-loop",
        "audit JWT security": "security-review",
        "design database schema migration": "database-design",
        "hello": "agyos-decision",
        "pineapple": "agyos-decision",
        "use agyos-founder-guide": "agyos-founder-guide",
        "transcribe audio recording": "audio-transcriber",
        "set up OpenWhispr voice dictation and connect its MCP server": "openwhispr",
        "check android screen visually": "android_ui_verification",
        "edit a local talking-head recording, remove pauses and approved retakes, add captions": "ai-video-editor",
        "Check every skill, improve the descriptions, organize the catalog, fix broken links, and rename only when justified": "agyos-self-improvement",
        "Audit and clean up the AGYOS skills catalog": "agyos-self-improvement",
        "Optimize every skill and make AGYOS skill discovery clearer": "agyos-self-improvement",
        "Create a 30 week DevOps career learning plan": "devops-career-roadmap",
        "Help us find the first 500 paying users through creator comments": "first-500-paying-users",
        "Make an AI accounts to follow watchlist": "ai-industry-watchlist",
        "How do I set up the Harvey free AI sales agent safely?": "harvey-sales-agent-guide",
        "Import all skill repositories into AGYOS": "agyos-self-improvement",
    }

    def test_frozen_task_cases(self):
        for query, expected in self.CASES.items():
            with self.subTest(query=query):
                result = router.decide_skill(query)
                self.assertEqual(result["primary_skill"], expected)
                self.assertTrue((ROOT / result["runbook_path"]).is_file())
                self.assertEqual(result["confidence_kind"], "heuristic_not_probability")
                self.assertEqual(result["execution_status"], "pending_runbook_read")

    def test_keywords_use_word_boundaries_and_phrases(self):
        self.assertEqual(router.classify_domain("pineapple")[0], "general")
        self.assertEqual(router.classify_domain("free tier")[0], "free_infrastructure")
        self.assertEqual(router.classify_domain("literature review")[0], "academic_research")
        self.assertEqual(router.classify_domain("organize every skill in the catalog")[0], "skill_catalog_maintenance")

    def test_complexity_respects_high_risk_even_in_short_prompts(self):
        for query in ("schema migration", "update all rules and skills", "add auth", "payment typo",
                      "delete production database", "drop table users", "wire money", "deploy to production"):
            with self.subTest(query=query):
                self.assertGreaterEqual(router.assess_complexity(query)[0], 3)
        self.assertEqual(router.assess_complexity("fix README typo")[0], 1)
        self.assertEqual(router.assess_complexity("adjust one file")[0], 2)
        self.assertGreaterEqual(router.assess_complexity("build something new")[0], 3)

    def test_no_catalog_does_not_invent_a_runbook(self):
        with patch.object(router, "load_catalog", return_value=[]):
            with self.assertRaisesRegex(ValueError, "catalog"):
                router.decide_skill("fix crash")

    def test_rejects_empty_tasks(self):
        for query in ("", "   "):
            with self.assertRaises(ValueError):
                router.decide_skill(query)

    def test_no_matches_or_zero_limit_return_no_candidates(self):
        self.assertEqual(router.select_best_skills("zzzxxyy", [], limit=5), [])
        self.assertEqual(router.select_best_skills("python", limit=0), [])
        self.assertEqual(router.select_best_skills("python", limit=-1), [])

    def test_load_catalog_survives_missing_and_corrupt_indexes(self):
        router.load_catalog.cache_clear()
        self.addCleanup(router.load_catalog.cache_clear)
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.json"
            bad = Path(temp) / "bad.json"
            bad.write_text("{broken")
            with patch.object(router, "MANIFEST_DATA", bad), patch.object(router, "DOCS_DATA", missing), \
                    patch.object(router, "physical_catalog", wraps=router.physical_catalog) as fallback:
                catalog = router.load_catalog()
                fallback.assert_called_once()
            self.assertEqual(len(catalog), len(list((ROOT / ".agents/skills").glob("*/SKILL.md"))))

    def test_complete_manifest_does_not_reparse_all_runbooks(self):
        router.load_catalog.cache_clear()
        self.addCleanup(router.load_catalog.cache_clear)
        with patch.object(router, "physical_catalog", side_effect=AssertionError("unneeded fallback")):
            catalog = router.load_catalog()
        self.assertIn("android_ui_verification", {s["name"] for s in catalog})

    def test_catalog_filters_traversal_missing_and_forged_paths(self):
        router.load_catalog.cache_clear()
        self.addCleanup(router.load_catalog.cache_clear)
        entries = [
            {"name": "../README", "path": ".agents/skills/../README"},
            {"name": "missing-skill", "path": ".agents/skills/missing-skill"},
            {"name": "diagnosing-bugs", "path": "/tmp/forged"},
        ]
        with tempfile.TemporaryDirectory() as temp:
            index = Path(temp) / "manifest.json"
            index.write_text(json.dumps({"skills": entries}))
            with patch.object(router, "MANIFEST_DATA", index):
                catalog = router.load_catalog()
        self.assertFalse(any(s["name"] in ("../README", "missing-skill") for s in catalog))
        match = next(s for s in catalog if s["name"] == "diagnosing-bugs")
        self.assertEqual(match["path"], ".agents/skills/diagnosing-bugs")

    def test_catalog_rejects_invalid_field_types(self):
        for invalid in ({"category": 123}, {"description": []}, {"description": ""}):
            with self.subTest(invalid=invalid):
                self.assertIsNone(canonical_entry({"name": "diagnosing-bugs", "description": "Debug failures", **invalid}))


class CatalogTests(unittest.TestCase):
    def test_every_rule_has_supported_metadata_and_size(self):
        for path in (ROOT / ".agents/rules").glob("*.md"):
            with self.subTest(rule=path.name):
                text = path.read_text()
                self.assertLess(path.stat().st_size, 24000)
                self.assertTrue(text.startswith("---\n"))
                metadata = yaml.load(text.split("\n---\n", 1)[0][4:], Loader=YAML_LOADER)
                self.assertIn(metadata["trigger"], ("always_on", "model_decision", "glob", "manual"))

    def test_every_skill_has_valid_discovery_metadata(self):
        for path in (ROOT / ".agents/skills").glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                text = path.read_text()
                self.assertTrue(text.startswith("---\n"))
                metadata = yaml.load(text.split("\n---\n", 1)[0][4:], Loader=YAML_LOADER)
                self.assertEqual(metadata["name"], path.parent.name)
                self.assertIsInstance(metadata["description"], str)
                self.assertTrue(metadata["description"].strip())

    def test_all_indexes_cover_the_physical_catalog(self):
        physical = {p.parent.name for p in (ROOT / ".agents/skills").glob("*/SKILL.md")}
        manifest = json.loads((ROOT / ".agents/skills-manifest.json").read_text())
        docs = json.loads((ROOT / "docs/skills-data.json").read_text())
        self.assertEqual({s["name"] for s in manifest["skills"]}, physical)
        self.assertEqual({s["id"] for s in docs}, physical)
        self.assertEqual(len(manifest["skills"]), len(physical))
        self.assertEqual(manifest["total_skills"], len(physical))
        for entry in manifest["skills"]:
            self.assertNotEqual(entry["description"], f"{entry['name']} skill")

    def test_all_curated_references_exist(self):
        names = set(router.LANGUAGE_FRAMEWORK_MAP.values())
        for domain in router.DOMAIN_TAXONOMY.values():
            names.update([domain["primary"], *domain["alternatives"]])
        for name in names:
            self.assertTrue((ROOT / ".agents/skills" / name / "SKILL.md").is_file(), name)


class EntryPointTests(unittest.TestCase):
    def test_cli_json_and_runbook_output(self):
        result = subprocess.run(
            [str(ROOT / "bin/agyos"), "decide", "fix python crash", "--json", "--runbook"],
            text=True, capture_output=True, cwd="/tmp",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["primary_skill"], "diagnosing-bugs")
        self.assertEqual(payload["runbook"], (ROOT / payload["runbook_path"]).read_text())
        self.assertEqual(payload["execution_status"], "runbook_returned")

    def test_cli_empty_task_returns_error_without_traceback(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/agyos-decision.py"), "  ", "--json"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_mcp_uses_same_router(self):
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "agyos_decision", "arguments": {"task": "fix python crash", "include_runbook": True},
        }}
        result = subprocess.run(
            ["node", str(ROOT / "mcp/state-server.cjs")], input=json.dumps(request) + "\n",
            text=True, capture_output=True, check=True,
        )
        payload = json.loads(json.loads(result.stdout)["result"]["content"][0]["text"])
        self.assertEqual(payload["primary_skill"], "diagnosing-bugs")
        self.assertIn("runbook", payload)


if __name__ == "__main__":
    unittest.main()
