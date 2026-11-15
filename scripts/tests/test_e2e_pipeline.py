"""Unit and regression tests for AGYOS End-to-End Autonomous Pipeline Engine."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.agyos_e2e import (
    check_git_invariants,
    deliver_milestone,
    execute_static_verification,
    get_next_milestone_id,
    init_milestone,
    plan_task,
    read_state_file,
    slugify_task,
    validate_prompt,
    write_state_file,
)


class EndToEndPipelineTests(unittest.TestCase):
    def test_delivery_requires_trusted_approval_and_never_claims_commit(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = deliver_milestone(
                "M1-safe-delivery",
                {"prompt": "publish change"},
                auto_push=True,
                root_dir=Path(tmp_dir),
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIsNone(result["committed_sha"])
        self.assertFalse(result["pushed"])

    def test_validate_prompt(self):
        self.assertEqual(validate_prompt("  build new auth flow  "), "build new auth flow")
        with self.assertRaises(ValueError):
            validate_prompt("hi")
        with self.assertRaises(ValueError):
            validate_prompt(123)  # type: ignore
        with self.assertRaises(ValueError):
            validate_prompt("a" * 3001)

    def test_slugify_task(self):
        self.assertEqual(slugify_task("Add OAuth2 Google Auth Provider"), "add-oauth2-google-auth")
        self.assertEqual(slugify_task(""), "task")

    def test_get_next_milestone_id(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            cp_dir = tmp_root / ".agents" / "state" / "checkpoints"
            cp_dir.mkdir(parents=True)
            self.assertEqual(get_next_milestone_id(tmp_root, "feature"), "M1-feature")
            (cp_dir / "M1-old.md").write_text("old")
            (cp_dir / "M2-existing.md").write_text("existing")
            self.assertEqual(get_next_milestone_id(tmp_root, "feature"), "M3-feature")

    def test_plan_task_structure(self):
        plan = plan_task("optimize postgres indexing strategy", root_dir=ROOT)
        self.assertEqual(plan["pod"], "pod-build")
        self.assertIn("complexity_score", plan)
        self.assertIn("fast_path", plan)
        self.assertIn("skill", plan)
        self.assertIn("model", plan)
        self.assertIn("evpi", plan)
        self.assertIn("contract", plan)
        self.assertEqual(plan["contract"]["pod"], "pod-build")

    def test_plan_fast_path_for_simple_task(self):
        plan = plan_task("fix typo in README", root_dir=ROOT)
        self.assertTrue(plan["fast_path"])
        self.assertLessEqual(plan["complexity_score"], 2)

    def test_plan_irreversible_action_evpi(self):
        plan = plan_task("wire $50000 to vendor bank account", root_dir=ROOT)
        self.assertEqual(plan["risk"], "R3")
        self.assertTrue(plan["evpi"]["should_ask_question"])
        self.assertEqual(plan["evpi"]["outbox_status"], "PENDING_COMMIT")

    def test_isolated_milestone_initialization(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bin_dir = tmp_root / "bin"
            bin_dir.mkdir()
            for name in ("agyos", "state.sh", "state-validate.sh"):
                shutil.copy2(ROOT / "bin" / name, bin_dir / name)

            state_dir = tmp_root / ".agents" / "state"
            state_dir.mkdir(parents=True)
            write_state_file(state_dir / "state.json", {
                "project": "AGYOS",
                "current_gate": "IDLE",
                "current_milestone": None,
                "complexity_score": 1,
            })

            plan = {
                "prompt": "fix single comment typo",
                "milestone_id": "M9-fix-typo",
                "pod": "pod-build",
                "risk": "R1",
                "complexity_score": 1,
                "fast_path": True,
                "skill": {"name": "diagnosing-bugs"},
                "model": {"model_id": "gemini-3.8-flash"},
                "evpi": {"assumptions_applied": []},
                "contract": {"task_id": "tsk_test", "pod": "pod-build"},
            }

            result = init_milestone(plan, root_dir=tmp_root)
            self.assertEqual(result["status"], "INITIALIZED")
            self.assertEqual(result["current_gate"], "IMPLEMENT")

            state = read_state_file(state_dir / "state.json")
            self.assertEqual(state["current_gate"], "IMPLEMENT")
            self.assertEqual(state["current_milestone"], "M9-fix-typo")

            checkpoint_file = state_dir / "checkpoints" / "M9-fix-typo.md"
            self.assertTrue(checkpoint_file.exists())
            self.assertIn("Gate UNDERSTAND -> ANALYZE -> IMPLEMENT", checkpoint_file.read_text())

            current_file = state_dir / "CURRENT.md"
            self.assertTrue(current_file.exists())
            self.assertIn("M9-fix-typo", current_file.read_text())

    def test_git_invariants_verification(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            import subprocess
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True)
            subprocess.run(["git", "commit", "--allow-empty", "-m", "initial commit"], cwd=tmp_root, capture_output=True, check=True)

            ok, reason = check_git_invariants(tmp_root)
            self.assertTrue(ok, reason)

            # Test invariant rejection on divergent feature branch
            subprocess.run(["git", "checkout", "-b", "feature/divergent"], cwd=tmp_root, capture_output=True, check=True)
            bad_branch_ok, bad_branch_reason = check_git_invariants(tmp_root)
            self.assertFalse(bad_branch_ok)
            self.assertIn("branch invariant violation", bad_branch_reason.lower())

            # Return to main and test invariant rejection on unverified identity
            subprocess.run(["git", "checkout", "main"], cwd=tmp_root, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Unauthorized Committer"], cwd=tmp_root, check=True)
            bad_name_ok, bad_name_reason = check_git_invariants(tmp_root)
            self.assertFalse(bad_name_ok)
            self.assertIn("identity invariant violation", bad_name_reason.lower())


if __name__ == "__main__":
    unittest.main()
