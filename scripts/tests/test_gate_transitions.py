"""Verify the AGYOS gate transition graph using isolated state files."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GateTransitionTests(unittest.TestCase):
    def project(self, current="IDLE", complexity=4):
        temp = tempfile.TemporaryDirectory()
        project = Path(temp.name)
        (project / "bin").mkdir()
        for name in ("agyos", "state.sh"):
            shutil.copy2(ROOT / "bin" / name, project / "bin" / name)
        state = project / ".agents/state/state.json"
        state.parent.mkdir(parents=True)
        state.write_text(json.dumps({"current_gate": current, "complexity_score": complexity}))
        return temp, project, state

    def run_cli(self, project, state, *args):
        env = os.environ.copy()
        env["STATE_FILE"] = str(state)
        return subprocess.run(
            ["bash", "bin/agyos", *args], cwd=project, env=env,
            text=True, capture_output=True,
        )

    def test_normal_gate_sequence_and_completion(self):
        temp, project, state = self.project()
        with temp:
            for gate in ("UNDERSTAND", "ANALYZE", "PLAN", "IMPLEMENT", "VERIFY", "IDLE"):
                result = self.run_cli(project, state, "gate", gate)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(state.read_text())["current_gate"], gate)

    def test_skipped_gate_and_unknown_gate_are_rejected_without_mutation(self):
        temp, project, state = self.project()
        with temp:
            for target in ("IMPLEMENT", "NOT_A_GATE"):
                result = self.run_cli(project, state, "gate", target)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(state.read_text())["current_gate"], "IDLE")

    def test_generic_state_setter_cannot_bypass_gate_graph(self):
        temp, project, state = self.project()
        with temp:
            env = os.environ.copy()
            env["STATE_FILE"] = str(state)
            result = subprocess.run(
                ["bash", "-c", 'source bin/state.sh; anchor_state_set current_gate VERIFY'],
                cwd=project, env=env, text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("anchor_gate_transition", result.stderr)
            self.assertEqual(json.loads(state.read_text())["current_gate"], "IDLE")

    def test_fast_path_requires_analyzed_low_complexity_task(self):
        temp, project, state = self.project(current="ANALYZE", complexity=2)
        with temp:
            accepted = self.run_cli(project, state, "fast")
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            saved = json.loads(state.read_text())
            self.assertEqual(saved["current_gate"], "IMPLEMENT")
            self.assertEqual(saved["complexity_score"], 2)

        temp, project, state = self.project(current="ANALYZE", complexity=4)
        with temp:
            rejected = self.run_cli(project, state, "fast")
            self.assertNotEqual(rejected.returncode, 0)
            saved = json.loads(state.read_text())
            self.assertEqual(saved["current_gate"], "ANALYZE")
            self.assertEqual(saved["complexity_score"], 4)

        temp, project, state = self.project(current="IDLE", complexity=1)
        with temp:
            rejected = self.run_cli(project, state, "fast")
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(json.loads(state.read_text())["current_gate"], "IDLE")


if __name__ == "__main__":
    unittest.main()
