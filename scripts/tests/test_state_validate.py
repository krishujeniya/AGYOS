"""Exercise state-file initialization and recovery in isolated locations."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class StateValidationTests(unittest.TestCase):
    def run_validator(self, state_file, path_prefix=None):
        env = os.environ.copy()
        env["STATE_FILE"] = str(state_file)
        if path_prefix:
            env["PATH"] = f"{path_prefix}{os.pathsep}{env.get('PATH', '')}"
        return subprocess.run(
            ["bash", str(ROOT / "bin/state-validate.sh")],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )

    def test_missing_state_avoids_running_the_full_project_initializer(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            state = project / ".agents/state/state.json"
            result = self.run_validator(state)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(state.read_text())
            self.assertEqual(payload["project"], "AGYOS")
            self.assertIsNone(payload["current_gate"])
            self.assertEqual(payload["hitl_approvals"], {})
            self.assertFalse((project / ".claude.json").exists())
            self.assertFalse((project / ".cursor").exists())

    def test_corrupt_state_is_backed_up_before_state_only_recovery(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / ".agents/state/state.json"
            state.parent.mkdir(parents=True)
            state.write_text("{broken json")
            result = self.run_validator(state)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNone(json.loads(state.read_text())["current_gate"])
            backups = list(state.parent.glob("state.json.corrupt.*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "{broken json")

    def test_invalid_gate_value_fails_without_replacing_state(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state.json"
            payload = {
                "project": "AGYOS",
                "current_gate": "FINISHED",
                "current_milestone": None,
                "iteration": 0,
                "iteration_cap": 10,
                "token_budget": 50000,
                "max_cost_usd": 10.0,
                "max_wall_clock_minutes": 60,
                "tokens_used": 0,
                "no_progress_strikes": 0,
                "hitl_approvals": {},
                "last_updated": "2026-11-12T00:00:00Z",
                "last_known_commit": "",
                "last_known_commit_COMPACT": None,
                "skill_versions": {},
            }
            state.write_text(json.dumps(payload))
            result = self.run_validator(state)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(state.read_text())["current_gate"], "FINISHED")

    def test_jq_execution_error_preserves_existing_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = root / "state.json"
            original = '{"project":"keep-me","current_gate":null}\n'
            state.write_text(original)
            shim_dir = root / "bin"
            shim_dir.mkdir()
            jq = shim_dir / "jq"
            jq.write_text("#!/bin/sh\nexit 2\n")
            jq.chmod(0o755)

            result = self.run_validator(state, shim_dir)

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(state.read_text(), original)
            self.assertEqual(list(root.glob("state.json.corrupt.*")), [])


if __name__ == "__main__":
    unittest.main()
