"""Offline security and routing cases for eight pinned integration sources."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import subprocess
import tempfile

from agyos_decision.integrations.source_registry import ROOT, load_registry, match_sources
from agyos_decision.integrations.agent_reach_adapter import invoke_read_only


class SourceRegistryTests(unittest.TestCase):
    def test_eight_pinned_sources_and_native_targets(self):
        sources = load_registry()
        self.assertEqual(len(sources), 8)
        self.assertEqual(len({s["repo"] for s in sources}), 8)
        self.assertTrue(all((ROOT / ".agents/skills" / s["primary_skill"] / "SKILL.md").is_file() for s in sources))

    def test_representative_intents_have_single_source(self):
        cases = {
            "Research competing agent architectures and compare execution strategy": "agent-architecture-intelligence",
            "Choose the best available skills for this task": "agentic-awesome-skills",
            "Validate my startup idea": "founders-kit",
            "Create a personalized AI engineering career roadmap": "ai-career-planner",
            "Build a production-ready machine learning pipeline": "ai-engineering-os",
            "Review the code and find problems before release": "gstack",
            "Research customer discussions online across supported platforms": "agent-reach",
            "Design an edge AI deployment architecture": "microsoft-edge-ai",
        }
        for request, expected in cases.items():
            with self.subTest(request=request):
                matches = match_sources(request)
                self.assertTrue(matches, request)
                self.assertEqual(matches[0]["source_id"], expected)

    def test_no_bad_matches_for_unrelated_or_partial_terms(self):
        for request in ("", "review a recipe", "I love my career", "random text", "deploy production now"):
            self.assertEqual(match_sources(request), [])

    def test_forged_destination_is_rejected(self):
        src = json.loads((ROOT / "integrations/registry/sources.json").read_text())
        src["sources"][0]["primary_skill"] = "../README"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.json"
            p.write_text(json.dumps(src))
            with self.assertRaises(ValueError):
                load_registry(p)

    def test_duplicate_source_is_rejected(self):
        src = json.loads((ROOT / "integrations/registry/sources.json").read_text())
        src["sources"][1]["id"] = src["sources"][0]["id"]
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.json"
            p.write_text(json.dumps(src))
            with self.assertRaises(ValueError):
                load_registry(p)


class AgentReachAdapterTests(unittest.TestCase):
    @patch("agyos_decision.integrations.agent_reach_adapter.shutil.which", return_value=None)
    def test_missing_dependency_fails_closed(self, _which):
        self.assertEqual(invoke_read_only("github", "agents")["error"], "NOT_INSTALLED")

    @patch("agyos_decision.integrations.agent_reach_adapter.shutil.which", return_value="/usr/bin/agent-reach")
    @patch("agyos_decision.integrations.agent_reach_adapter.subprocess.run")
    def test_public_search_uses_argument_vector_only(self, run, _which):
        run.return_value = subprocess.CompletedProcess([], 0, '{"ok": true, "result": {"items": []}}', "")
        result = invoke_read_only("youtube", "edge AI; echo BAD")
        self.assertTrue(result["ok"])
        self.assertEqual(run.call_args.args[0], ["/usr/bin/agent-reach", "youtube", "search", "edge AI; echo BAD"])
        self.assertFalse(run.call_args.kwargs["check"])

    @patch("agyos_decision.integrations.agent_reach_adapter.shutil.which", return_value="/usr/bin/agent-reach")
    @patch("agyos_decision.integrations.agent_reach_adapter.subprocess.run")
    def test_no_mutating_or_authenticated_channel(self, run, _which):
        for operation in ("setup", "add", "login", "reddit", "twitter", "read", "update"):
            self.assertEqual(invoke_read_only(operation, "hello")["error"], "UNAUTHORIZED_OPERATION")
        run.assert_not_called()

    @patch("agyos_decision.integrations.agent_reach_adapter.shutil.which", return_value="/usr/bin/agent-reach")
    @patch("agyos_decision.integrations.agent_reach_adapter.subprocess.run")
    def test_reject_malformed_json_and_nonzero_exit(self, run, _which):
        run.return_value = subprocess.CompletedProcess([], 0, "untrusted garbage", "")
        self.assertEqual(invoke_read_only("channels")["error"], "INVALID_RESPONSE")
        run.return_value = subprocess.CompletedProcess([], 1, '{"ok": false, "error": {"hint": "secret"}}', "")
        self.assertEqual(invoke_read_only("channels")["error"], "UPSTREAM_ERROR")


if __name__ == "__main__":
    unittest.main()
