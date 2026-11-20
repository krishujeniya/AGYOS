"""Unit and regression tests for AGYOS 7-Step Autonomous Cycle Engine."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.cycle import (
    AutonomousCycleStage,
    CycleContext,
    StageStatus,
    check_git_invariants,
    execute_build,
    execute_plan,
    execute_reflect,
    execute_review,
    execute_ship,
    execute_test,
    execute_think,
    get_next_milestone_id,
    read_state_file,
    run_autonomous_cycle,
    slugify_goal,
    validate_goal,
    write_state_file,
)


class AutonomousCycleTests(unittest.TestCase):
    def test_validate_goal(self):
        self.assertEqual(validate_goal("  build user authentication  "), "build user authentication")
        with self.assertRaises(ValueError):
            validate_goal("no")
        with self.assertRaises(ValueError):
            validate_goal(42)  # type: ignore
        with self.assertRaises(ValueError):
            validate_goal("x" * 3001)

    def test_slugify_goal(self):
        self.assertEqual(slugify_goal("Implement OAuth2 JWT Token Flow"), "implement-oauth2-jwt-token")
        self.assertEqual(slugify_goal(""), "task")

    def test_get_next_milestone_id(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            cp_dir = tmp_root / ".agents" / "state" / "checkpoints"
            cp_dir.mkdir(parents=True)
            self.assertEqual(get_next_milestone_id(tmp_root, "feature"), "M1-feature")
            (cp_dir / "M1-old.md").write_text("old", encoding="utf-8")
            (cp_dir / "M2-existing.md").write_text("existing", encoding="utf-8")
            self.assertEqual(get_next_milestone_id(tmp_root, "feature"), "M3-feature")

    def test_stage_1_think(self):
        ctx = execute_think("optimize postgresql query latency and connection pool", root_dir=ROOT)
        self.assertEqual(ctx.stage_statuses[AutonomousCycleStage.THINK.value], StageStatus.PASS.value)
        self.assertTrue(len(ctx.role_id) > 0)
        self.assertTrue(len(ctx.role_title) > 0)
        self.assertTrue(len(ctx.skill_name) > 0)
        self.assertIn("postgres", ctx.skill_name.lower())
        self.assertIn("complexity", ctx.to_dict())
        self.assertEqual(ctx.current_stage, AutonomousCycleStage.PLAN.value)

    def test_stage_2_plan_in_isolation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("add oauth authentication", root_dir=tmp_root)

            # Setup minimal state environment
            state_dir = tmp_root / ".agents" / "state"
            state_dir.mkdir(parents=True)
            write_state_file(state_dir / "state.json", {
                "project": "AGYOS",
                "current_gate": "IDLE",
                "current_milestone": None,
            })

            # Mock bin/agyos gate calls by skipping subprocess failure or mocking
            bin_dir = tmp_root / "bin"
            bin_dir.mkdir()
            for name in ("agyos", "state.sh", "state-validate.sh"):
                if (ROOT / "bin" / name).exists():
                    shutil.copy2(ROOT / "bin" / name, bin_dir / name)

            plan_ctx = execute_plan(ctx, root_dir=tmp_root)
            self.assertEqual(plan_ctx.stage_statuses[AutonomousCycleStage.PLAN.value], StageStatus.PASS.value)
            self.assertTrue(len(plan_ctx.tasks) >= 3)
            self.assertTrue(len(plan_ctx.acceptance_criteria) >= 2)

            checkpoint_file = state_dir / "checkpoints" / f"{plan_ctx.milestone_id}.md"
            self.assertTrue(checkpoint_file.exists())
            content = checkpoint_file.read_text(encoding="utf-8")
            self.assertIn("Planned Tasks", content)
            self.assertIn("Acceptance Criteria", content)

            current_md = state_dir / "CURRENT.md"
            self.assertTrue(current_md.exists())

    def test_stage_3_build_tracking(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("refactor backend handler", root_dir=tmp_root)
            state_dir = tmp_root / ".agents" / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            build_ctx = execute_build(ctx, root_dir=tmp_root, target_files=["src/server.py", "tests/test_server.py"])
            self.assertEqual(build_ctx.stage_statuses[AutonomousCycleStage.BUILD.value], StageStatus.PASS.value)
            self.assertEqual(len(build_ctx.build_files), 2)
            self.assertIn("src/server.py", build_ctx.build_files)

    def test_stage_4_review_checks(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("security audit", root_dir=tmp_root)
            state_dir = tmp_root / ".agents" / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Review against actual ROOT codebase
            review_ctx = execute_review(ctx, root_dir=ROOT)
            self.assertIn(review_ctx.review_verdict, ("PASS", "FAIL"))
            self.assertIsInstance(review_ctx.review_findings, list)

    def test_stage_5_test_static_verification(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("static test verify", root_dir=tmp_root)
            state_dir = tmp_root / ".agents" / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            test_ctx = execute_test(ctx, root_dir=ROOT)
            self.assertEqual(test_ctx.test_verdict, "PASS")
            self.assertEqual(len(test_ctx.test_errors), 0)

    def test_stage_6_ship_invariants(self):
        # Verify git invariants helper
        ok, msg = check_git_invariants(ROOT)
        self.assertTrue(ok, f"Git invariant check failed: {msg}")

        ctx = execute_think("ship milestone verification", root_dir=ROOT)
        state_dir = ROOT / ".agents" / "state" / "checkpoints"
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

        try:
            ship_ctx = execute_ship(ctx, root_dir=ROOT, auto_push=False)
            self.assertEqual(ship_ctx.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.PASS.value)
            self.assertIn("READY", ship_ctx.delivery_status) or self.assertIn("CLEAN", ship_ctx.delivery_status)
        finally:
            # Clean up dummy test checkpoint if created in real repo
            test_cp = state_dir / f"{ctx.milestone_id}.md"
            if test_cp.exists():
                test_cp.unlink()

    def test_stage_7_reflect_handoff(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("reflect and handover", root_dir=tmp_root)
            state_dir = tmp_root / ".agents" / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Setup AI_HANDOFF.md
            (tmp_root / "AI_HANDOFF.md").write_text("# Prior handoff\n", encoding="utf-8")

            reflect_ctx = execute_reflect(ctx, root_dir=tmp_root)
            self.assertEqual(reflect_ctx.stage_statuses[AutonomousCycleStage.REFLECT.value], StageStatus.PASS.value)
            self.assertTrue(len(reflect_ctx.handoff_entry) > 0)
            self.assertIn("Task: reflect and handover", reflect_ctx.handoff_entry)
            self.assertIn("Branch: `main`", reflect_ctx.handoff_entry)

            # Check that AI_HANDOFF was updated
            updated_handoff = (tmp_root / "AI_HANDOFF.md").read_text(encoding="utf-8")
            self.assertIn("reflect and handover", updated_handoff)

    def test_full_cycle_execution(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bin_dir = tmp_root / "bin"
            bin_dir.mkdir()
            for name in ("agyos", "state.sh", "state-validate.sh"):
                shutil.copy2(ROOT / "bin" / name, bin_dir / name)

            # Initialize git repo in tmp_root to verify git invariants
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True)
            (tmp_root / ".github" / "workflows").mkdir(parents=True)
            (tmp_root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (tmp_root / "AI_HANDOFF.md").write_text("# Baseline handoff\n", encoding="utf-8")

            ctx = run_autonomous_cycle(
                goal="improve database query throughput",
                root_dir=tmp_root,
                auto_push=False,
            )

            # Verify all 7 stages passed
            for stage in AutonomousCycleStage:
                self.assertEqual(
                    ctx.stage_statuses[stage.value],
                    StageStatus.PASS.value,
                    f"Stage {stage.value} did not pass: {ctx.to_dict()}"
                )
            self.assertTrue(len(ctx.milestone_id) > 0)
            self.assertTrue(ctx.completed_at is not None)


if __name__ == "__main__":
    unittest.main()
