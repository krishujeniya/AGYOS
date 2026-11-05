"""Exercise the real commit gate with staged Git fixtures."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class TestRatchetTests(unittest.TestCase):
    def run_gate(self, before, after):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / "bin").mkdir()
            for name in ("gate-check.sh", "state.sh"):
                shutil.copy2(ROOT / "bin" / name, repo / "bin" / name)
            state = repo / ".agents/state/state.json"
            state.parent.mkdir(parents=True)
            state.write_text(json.dumps({"current_gate": "IDLE", "current_milestone": None, "iteration": 1}))
            def git(*args):
                return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=True)
            git("init", "-q")
            fixture = repo / "test_fixture.py"
            fixture.write_text(before)
            git("add", "test_fixture.py")
            git("-c", "user.name=Gate Test", "-c", "user.email=gate@example.invalid",
                "-c", "core.hooksPath=/dev/null", "commit", "-qm", "fixture baseline")
            fixture.write_text(after)
            git("add", "test_fixture.py")
            return subprocess.run(["bash", "bin/gate-check.sh"], cwd=repo, text=True, capture_output=True)

    def test_zero_assertion_file_does_not_abort_gate(self):
        result = self.run_gate("# original fixture\n", "# updated fixture\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_removed_assertion_still_blocks_commit(self):
        result = self.run_gate("assert 1 == 1\n", "# removed\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("TEST RATCHET", result.stdout)


if __name__ == "__main__":
    unittest.main()
