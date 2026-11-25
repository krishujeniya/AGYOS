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
            cp_dir = tmp_root / "state" / "checkpoints"
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
            state_dir = tmp_root / "state"
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
                if (ROOT.parent / "bin" / name).exists():
                    shutil.copy2(ROOT.parent / "bin" / name, bin_dir / name)

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
            state_dir = tmp_root / "state" / "checkpoints"
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
            state_dir = tmp_root / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Setup clean test files in tmp_root
            (tmp_root / "agyos_decision").mkdir()
            (tmp_root / "agyos_decision" / "app.py").write_text("def hello():\n    return 'clean'\n", encoding="utf-8")

            review_ctx = execute_review(ctx, root_dir=tmp_root)
            self.assertEqual(review_ctx.stage_statuses[AutonomousCycleStage.REVIEW.value], StageStatus.PASS.value)
            self.assertEqual(review_ctx.review_verdict, "PASS")
            self.assertEqual(len(review_ctx.review_findings), 0)

    def test_stage_5_test_static_verification(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("static test verify", root_dir=tmp_root)
            state_dir = tmp_root / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Setup clean environment in tmp_root
            (tmp_root / ".github" / "workflows").mkdir(parents=True)
            (tmp_root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (tmp_root / "agyos_decision").mkdir()
            (tmp_root / "agyos_decision" / "app.py").write_text("def test():\n    pass\n", encoding="utf-8")

            test_ctx = execute_test(ctx, root_dir=tmp_root)
            self.assertEqual(test_ctx.test_verdict, "PASS")
            self.assertEqual(len(test_ctx.test_errors), 0)

    def test_stage_6_ship_invariants(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True, timeout=10)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "commit", "--allow-empty", "-m", "initial commit"], cwd=tmp_root, capture_output=True, check=True, timeout=10)

            # Verify git invariants helper
            ok, msg = check_git_invariants(tmp_root)
            self.assertTrue(ok, f"Git invariant check failed: {msg}")

            ctx = execute_think("ship milestone verification", root_dir=tmp_root)
            state_dir = tmp_root / "state" / "checkpoints"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Review and Test gates must pass before entering Ship
            ctx.stage_statuses[AutonomousCycleStage.REVIEW.value] = StageStatus.PASS.value
            ctx.review_verdict = "PASS"
            ctx.stage_statuses[AutonomousCycleStage.TEST.value] = StageStatus.PASS.value
            ctx.test_verdict = "PASS"

            ship_ctx = execute_ship(ctx, root_dir=tmp_root, auto_push=False)
            self.assertEqual(ship_ctx.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.PASS.value)
            self.assertTrue("PENDING_OPERATOR_APPROVAL" in ship_ctx.delivery_status or "CLEAN" in ship_ctx.delivery_status)

    def test_stage_6_ship_blocked_when_review_or_test_fails_or_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True, timeout=10)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "commit", "--allow-empty", "-m", "initial commit"], cwd=tmp_root, capture_output=True, check=True, timeout=10)

            # 1. Missing review -> BLOCKED
            ctx1 = execute_think("task missing review", root_dir=tmp_root)
            ship_ctx1 = execute_ship(ctx1, root_dir=tmp_root, auto_push=False)
            self.assertEqual(ship_ctx1.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.BLOCKED.value)
            self.assertIn("Review gate failed or not passed", ship_ctx1.delivery_status)

            # 2. Failed review -> BLOCKED
            ctx2 = execute_think("task failed review", root_dir=tmp_root)
            ctx2.stage_statuses[AutonomousCycleStage.REVIEW.value] = StageStatus.FAIL.value
            ctx2.review_verdict = "FAIL"
            ship_ctx2 = execute_ship(ctx2, root_dir=tmp_root, auto_push=False)
            self.assertEqual(ship_ctx2.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.BLOCKED.value)
            self.assertIn("Review gate failed or not passed", ship_ctx2.delivery_status)

            # 3. Missing test -> BLOCKED
            ctx3 = execute_think("task missing test", root_dir=tmp_root)
            ctx3.stage_statuses[AutonomousCycleStage.REVIEW.value] = StageStatus.PASS.value
            ctx3.review_verdict = "PASS"
            ship_ctx3 = execute_ship(ctx3, root_dir=tmp_root, auto_push=False)
            self.assertEqual(ship_ctx3.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.BLOCKED.value)
            self.assertIn("Test gate failed or not passed", ship_ctx3.delivery_status)

            # 4. Failed test -> BLOCKED
            ctx4 = execute_think("task failed test", root_dir=tmp_root)
            ctx4.stage_statuses[AutonomousCycleStage.REVIEW.value] = StageStatus.PASS.value
            ctx4.review_verdict = "PASS"
            ctx4.stage_statuses[AutonomousCycleStage.TEST.value] = StageStatus.FAIL.value
            ctx4.test_verdict = "FAIL"
            ship_ctx4 = execute_ship(ctx4, root_dir=tmp_root, auto_push=False)
            self.assertEqual(ship_ctx4.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.BLOCKED.value)
            self.assertIn("Test gate failed or not passed", ship_ctx4.delivery_status)

    def test_stage_6_ship_scoped_staging_only(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True, timeout=10)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "commit", "--allow-empty", "-m", "initial commit"], cwd=tmp_root, capture_output=True, check=True, timeout=10)

            # Create an unrelated file
            (tmp_root / "unrelated.txt").write_text("unrelated changes", encoding="utf-8")

            ctx = execute_think("scoped staging check", root_dir=tmp_root)
            ctx.stage_statuses[AutonomousCycleStage.REVIEW.value] = StageStatus.PASS.value
            ctx.review_verdict = "PASS"
            ctx.stage_statuses[AutonomousCycleStage.TEST.value] = StageStatus.PASS.value
            ctx.test_verdict = "PASS"
            ctx.build_files = []  # No build files associated with this milestone

            ship_ctx = execute_ship(ctx, root_dir=tmp_root, auto_push=True)
            self.assertEqual(ship_ctx.stage_statuses[AutonomousCycleStage.SHIP.value], StageStatus.BLOCKED.value)
            self.assertIn("No scoped build files identified", ship_ctx.delivery_status)

            # Verify unrelated file was NOT staged
            st_res = subprocess.run(["git", "status", "--porcelain"], cwd=tmp_root, capture_output=True, text=True, check=True)
            self.assertTrue(st_res.stdout.startswith("?? unrelated.txt"), "Unrelated file must remain untracked/unstaged")

    def test_stage_7_reflect_handoff(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("reflect and handover", root_dir=tmp_root)
            state_dir = tmp_root / "state" / "checkpoints"
            state_dir.mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")

            # Setup AI_HANDOFF.md
            (tmp_root / "AI_HANDOFF.md").write_text("# Prior handoff\n", encoding="utf-8")

            # Set all prior stages as passed
            for stage in (AutonomousCycleStage.PLAN, AutonomousCycleStage.BUILD, AutonomousCycleStage.REVIEW, AutonomousCycleStage.TEST, AutonomousCycleStage.SHIP):
                ctx.stage_statuses[stage.value] = StageStatus.PASS.value
            ctx.review_verdict = "PASS"
            ctx.test_verdict = "PASS"
            ctx.delivery_status = "CLEAN (No pending uncommitted changes)"

            reflect_ctx = execute_reflect(ctx, root_dir=tmp_root)
            self.assertEqual(reflect_ctx.stage_statuses[AutonomousCycleStage.REFLECT.value], StageStatus.PASS.value)
            self.assertTrue(len(reflect_ctx.handoff_entry) > 0)
            self.assertIn("Task: reflect and handover", reflect_ctx.handoff_entry)
            self.assertIn("Branch: `main`", reflect_ctx.handoff_entry)

            # Check that AI_HANDOFF was updated
            updated_handoff = (tmp_root / "AI_HANDOFF.md").read_text(encoding="utf-8")
            self.assertIn("reflect and handover", updated_handoff)

    def test_stage_7_reflect_records_failure_on_blocked_stage(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            ctx = execute_think("reflect failure case", root_dir=tmp_root)
            state_dir = tmp_root / "state"
            state_dir.mkdir(parents=True)
            (state_dir / "checkpoints").mkdir(parents=True)
            (state_dir / f"{ctx.milestone_id}.md").write_text("# Initial", encoding="utf-8")
            (state_dir / "state.json").write_text(json.dumps({"current_gate": "SHIP"}), encoding="utf-8")
            (tmp_root / "AI_HANDOFF.md").write_text("# Prior handoff\n", encoding="utf-8")

            # Stage failed/blocked
            ctx.stage_statuses[AutonomousCycleStage.SHIP.value] = StageStatus.BLOCKED.value
            ctx.delivery_status = "BLOCKED: Test gate failed or not passed"

            reflect_ctx = execute_reflect(ctx, root_dir=tmp_root)
            self.assertEqual(reflect_ctx.stage_statuses[AutonomousCycleStage.REFLECT.value], StageStatus.FAIL.value)
            self.assertIn("FAILED or BLOCKED", reflect_ctx.reflection_summary)

            # AI_HANDOFF must NOT be updated with success
            updated_handoff = (tmp_root / "AI_HANDOFF.md").read_text(encoding="utf-8")
            self.assertEqual(updated_handoff, "# Prior handoff\n")

            # state.json current_gate must be BLOCKED
            state = json.loads((state_dir / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["current_gate"], "BLOCKED")

    def test_full_cycle_execution(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bin_dir = tmp_root / "bin"
            bin_dir.mkdir()
            for name in ("agyos", "state.sh", "state-validate.sh"):
                shutil.copy2(ROOT.parent / "bin" / name, bin_dir / name)

            # Initialize git repo in tmp_root to verify git invariants
            subprocess.run(["git", "init", "-b", "main"], cwd=tmp_root, capture_output=True, check=True, timeout=10)
            subprocess.run(["git", "config", "user.name", "Krish Ujeniya"], cwd=tmp_root, check=True, timeout=10)
            subprocess.run(["git", "config", "user.email", "100012208+krishujeniya@users.noreply.github.com"], cwd=tmp_root, check=True, timeout=10)
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
