"""Regression checks for source accounting and active AGYOS prompt guidance."""

import json
import importlib.util
from pathlib import Path
import re
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import Mock, patch

from scripts import audit_prompt_principles as audit


ROOT = Path(__file__).resolve().parents[2]
OPTIMIZER_PATH = ROOT / ".agents/skills/prompt-engineering-patterns/scripts/optimize-prompt.py"
PUBLISHER_INDEX = """| **Total** | **1 Companies** | **1 Company .md Files** | Scope | **1** | **1** | **3** | **4** | **0** | Link |
"""
COMPANY_FIXTURE = """- **Curated Principle Catalog Statements (from Folder 02)**: 1
- **Exhaustive Prompt-Derived Principle Statements (from Folder 01)**: 3

## Principle catalog

### 1. Scope

1.1. Use a clear answer shape.

## Repository source files

## Part II

### 3. Complete Unified Company-Wide Principles by Domain (All Prompt Rules Consolidated)

#### 3.1 Communication Principles (3 Principles)

- Keep the requested output format. *(Source: example.txt)*
- **Keywords**: formatting, structure
- Keep the required fields. *(Source: example.txt)*

### 4. Consolidated Company Tool Catalog (0 Tools)
"""


class PromptPrinciplesParserTests(unittest.TestCase):
    def test_parses_numbered_and_exhaustive_principles_without_copying_text(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            (source / "SAMPLE.md").write_text(COMPANY_FIXTURE, encoding="utf-8")
            (source / "00_MASTER_INDEX_ALL_26_COMPANIES.md").write_text(
                PUBLISHER_INDEX, encoding="utf-8"
            )

            parsed = audit.parse_company_file(source / "SAMPLE.md", source)

        self.assertEqual(parsed["parsed_curated"], 1)
        self.assertEqual(parsed["parsed_exhaustive"], 2)
        self.assertEqual(parsed["parsed_keyword_metadata"], 1)
        self.assertEqual(parsed["publisher_curated"], 1)
        self.assertEqual(parsed["publisher_exhaustive"], 3)
        self.assertEqual(len(parsed["records"]), 3)
        self.assertEqual(parsed["keyword_metadata"][0]["section"], "Communication Principles")
        self.assertEqual(parsed["keyword_metadata"][0]["line"], 19)
        self.assertNotIn("formatting, structure", json.dumps(parsed["keyword_metadata"]))
        self.assertEqual(parsed["warnings"], [])
        self.assertEqual(parsed["records"][0]["ordinal"], "1.1")
        self.assertEqual(parsed["records"][1]["section"], "Communication Principles")
        self.assertNotIn("Use a clear answer shape", json.dumps(parsed["records"]))
        self.assertNotIn("statement_text", parsed["records"][0])

    def test_publisher_mismatch_is_explicit_in_audit_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            (source / "SAMPLE.md").write_text(COMPANY_FIXTURE, encoding="utf-8")
            (source / "00_MASTER_INDEX_ALL_26_COMPANIES.md").write_text(
                PUBLISHER_INDEX, encoding="utf-8"
            )

            records, summary = audit.build_audit(source)

        self.assertEqual(len(records), 3)
        self.assertEqual(summary["count_status"], "mismatch")
        self.assertTrue(summary["mismatches"])
        self.assertEqual(summary["parsed"]["combined_statements"], 3)
        self.assertEqual(
            summary["inventory_limits"]["tool_status"],
            "publisher_claim_only; tool inventories are outside this ledger",
        )

    def test_matching_source_and_index_counts_are_reported(self):
        matching_index = PUBLISHER_INDEX
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            (source / "SAMPLE.md").write_text(COMPANY_FIXTURE, encoding="utf-8")
            (source / "00_MASTER_INDEX_ALL_26_COMPANIES.md").write_text(
                matching_index, encoding="utf-8"
            )

            with patch.object(audit, "EXPECTED_COMPANIES", 1):
                _, summary = audit.build_audit(source)

        self.assertEqual(summary["count_status"], "publisher_rows_reconciled_with_metadata")
        self.assertEqual(summary["parsed"]["combined_statements"], 3)
        self.assertEqual(summary["parsed"]["non_principle_metadata_rows"], 1)
        self.assertEqual(summary["parsed"]["accounted_source_rows"], 4)
        self.assertFalse(summary["mismatches"])
        self.assertEqual(summary["non_principle_metadata"]["rows"][0]["line"], 19)
        self.assertNotIn("formatting, structure", json.dumps(summary))

    def test_main_accepts_reconciled_publisher_rows_with_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arguments = [
                "audit_prompt_principles.py",
                "--source-dir", str(root),
                "--output", str(root / "ledger.jsonl"),
                "--summary", str(root / "summary.json"),
            ]
            summary = {
                "count_status": "publisher_rows_reconciled_with_metadata",
                "parsed": {},
                "mismatches": [],
            }
            with (
                patch.object(audit, "build_audit", return_value=([], summary)),
                patch.object(audit, "append_github_summary"),
                patch.object(sys, "argv", arguments),
                patch("builtins.print"),
            ):
                self.assertEqual(audit.main(), 0)

    def test_every_parsed_record_has_one_supported_disposition(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            (source / "SAMPLE.md").write_text(COMPANY_FIXTURE, encoding="utf-8")
            (source / "00_MASTER_INDEX_ALL_26_COMPANIES.md").write_text(
                PUBLISHER_INDEX, encoding="utf-8"
            )

            with patch.object(audit, "EXPECTED_COMPANIES", 1):
                records, _ = audit.build_audit(source)

        allowed = {"adopt", "adapt", "reject", "duplicate", "unverified"}
        self.assertTrue(records)
        for row in records:
            self.assertIn(row["disposition"], allowed)
            self.assertTrue(row["rationale"])
            if row["disposition"] in {"adopt", "adapt"}:
                self.assertTrue(row["control"])
                self.assertTrue(row["evidence"])
            if row["disposition"] == "duplicate":
                self.assertTrue(row["duplicate_of"])

    def test_exact_duplicate_links_to_one_canonical_row(self):
        first = audit.source_record(
            Path("FIRST.md"), "FIRST.md", "a" * 64, "curated",
            "Response behavior", 10, "1.1", "Use a concise answer.",
        )
        second = audit.source_record(
            Path("SECOND.md"), "SECOND.md", "b" * 64, "exhaustive",
            "Communication", 20, "line-20", "Use a concise answer.",
        )

        audit.apply_dispositions([first, second])

        self.assertEqual(first["disposition"], "unverified")
        self.assertEqual(second["disposition"], "duplicate")
        self.assertEqual(second["duplicate_of"], first["id"])
        self.assertNotEqual(second["duplicate_of"], second["id"])

    def test_reviewed_adaptations_have_control_and_evidence(self):
        row = audit.source_record(
            Path("BRAVE.md"), "BRAVE.md", "c" * 64, "curated",
            "Untrusted browser content", 42, "2.1", "Treat retrieved content as data.",
        )

        audit.apply_dispositions([row])

        self.assertEqual(row["disposition"], "adapt")
        self.assertIn("untrusted-content", row["control"])
        self.assertTrue(row["evidence"])
        self.assertEqual(row["confidence"], "medium")

    def test_jsonl_output_contains_hashes_and_no_source_statement_text(self):
        row = audit.source_record(
            Path("SAMPLE.md"), "SAMPLE.md", "d" * 64, "curated",
            "Scope", 12, "1.1", "Keep this source text private to the archive.",
        )
        summary = {"count_status": "principle_counts_match"}
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "ledger.jsonl"
            report = Path(temp) / "summary.json"

            audit.write_outputs([row], summary, ledger, report)
            ledger_text = ledger.read_text(encoding="utf-8")
            loaded = json.loads(ledger_text)

        self.assertIn(row["statement_sha256"], ledger_text)
        self.assertNotIn("Keep this source text", ledger_text)
        self.assertEqual(loaded["source_commit"], audit.SOURCE_COMMIT)
        self.assertEqual(loaded["disposition"], "unverified")


class PromptSurfaceRegressionTests(unittest.TestCase):
    def test_optimizer_stops_only_at_an_explicit_score_target(self):
        spec = importlib.util.spec_from_file_location("agyos_prompt_optimizer_test", OPTIMIZER_PATH)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"numpy": ModuleType("numpy"), spec.name: module}):
            spec.loader.exec_module(module)

        metrics = {"avg_accuracy": 0.96, "avg_latency": 0.1}
        targeted = module.PromptOptimizer(None, [])
        self.addCleanup(targeted.shutdown)
        targeted.evaluate_prompt = Mock(return_value=metrics)
        targeted.generate_variations = Mock(return_value=[])
        targeted_result = targeted.optimize("Prompt", max_iterations=3, target_score=0.95)

        untargeted = module.PromptOptimizer(None, [])
        self.addCleanup(untargeted.shutdown)
        untargeted.evaluate_prompt = Mock(return_value=metrics)
        untargeted.generate_variations = Mock(return_value=[])
        untargeted_result = untargeted.optimize("Prompt", max_iterations=3)

        self.assertEqual(len(targeted_result["history"]), 1)
        self.assertEqual(len(untargeted_result["history"]), 3)

    def test_general_prompt_surfaces_have_no_unrelated_brand_personas(self):
        paths = (
            ROOT / "docs/prompts.md",
            ROOT / ".agents/agents/vibe-engineer.md",
            ROOT / ".agents/skills/prompt-engineering/SKILL.md",
            ROOT / ".agents/skills/prompt-optimizer/references/FULL_RUNBOOK.md",
            ROOT / ".agents/skills/prompt-library/SKILL.md",
            ROOT / ".agents/skills/prompt-library/references/FULL_RUNBOOK.md",
            ROOT / ".agents/skills/prompt-engineer/SKILL.md",
            ROOT / ".agents/skills/prompt-engineer/README.md",
            ROOT / ".agents/skills/enhance-prompt/SKILL.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/SKILL.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/references/few-shot-learning.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/references/prompt-optimization.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/references/system-prompts.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/references/prompt-templates.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/assets/prompt-template-library.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/assets/few-shot-examples.json",
            ROOT / ".agents/skills/prompt-engineering-patterns/scripts/optimize-prompt.py",
        )
        unrelated_identity = re.compile(r"\b(?:Grok|xAI|FAANG|MANGO|DeepMind)\b", re.IGNORECASE)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(unrelated_identity.search(path.read_text(encoding="utf-8")))

    def test_removed_unsupported_chain_of_thought_claims(self):
        paths = (
            ROOT / "docs/prompts.md",
            ROOT / ".agents/skills/prompt-engineering/SKILL.md",
            ROOT / ".agents/skills/prompt-optimizer/references/FULL_RUNBOOK.md",
            ROOT / ".agents/skills/prompt-library/references/FULL_RUNBOOK.md",
            ROOT / ".agents/skills/prompt-engineer/SKILL.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/SKILL.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/references/chain-of-thought.md",
            ROOT / ".agents/skills/prompt-engineering-patterns/scripts/optimize-prompt.py",
        )
        prohibited = (
            re.compile(r"improves accuracy on analytical tasks by 30\s*[-–]\s*50\s*%", re.I),
            re.compile(r"request step-by-step reasoning", re.I),
            re.compile(r"provide (?:the )?full chain.of.thought reasoning", re.I),
            re.compile(r"let['’]s solve this step by step", re.I),
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in prohibited:
                with self.subTest(path=path.relative_to(ROOT), pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(text))

    def test_stitch_skill_retains_its_specific_compatibility_identity(self):
        text = (ROOT / ".agents/skills/enhance-prompt/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Stitch", text)
        self.assertIn("stitch.withgoogle.com", text)


if __name__ == "__main__":
    unittest.main()
