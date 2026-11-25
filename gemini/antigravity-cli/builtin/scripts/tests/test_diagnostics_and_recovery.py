"""Tests for Redacted Diagnostics Export and Disaster Recovery Restore Drill."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

from scripts.export_diagnostics import redact_string, collect_diagnostics


class DiagnosticsRedactionTests(unittest.TestCase):
    def test_redacts_github_and_aws_tokens(self):
        # Assemble probe token dynamically to prevent static pattern false alarms in repo
        sample_pat = "g" + "hp_" + "012345678901234567890123456789012345"
        sample_aws = "AKIA" + "0123456789ABCDEF"
        sample_bearer = "Bearer " + "ey" + "JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30"
        sample_sentinel = "AGYOS_" + "PRIVATE_" + "SENTINEL"
        sample_home = "/home/developer_name/project/repo"

        raw = f"PAT={sample_pat} AWS={sample_aws} AUTH={sample_bearer} S={sample_sentinel} P={sample_home}"
        redacted = redact_string(raw)

        self.assertNotIn(sample_pat, redacted)
        self.assertNotIn(sample_aws, redacted)
        self.assertNotIn(sample_bearer, redacted)
        self.assertNotIn(sample_sentinel, redacted)
        self.assertNotIn("/home/developer_name", redacted)

        self.assertIn("[REDACTED_GITHUB_TOKEN]", redacted)
        self.assertIn("[REDACTED_AWS_KEY]", redacted)
        self.assertIn("[REDACTED_BEARER_TOKEN]", redacted)
        self.assertIn("[REDACTED_SENTINEL]", redacted)
        self.assertIn("~", redacted)

    def test_collect_diagnostics_produces_clean_schema_without_secrets(self):
        data = collect_diagnostics(redact=True)
        self.assertEqual(data["schema_version"], "1.0.0")
        self.assertIn("git", data)
        self.assertIn("state_machine", data)
        self.assertIn("workspace_store", data)
        self.assertIn("environment", data)
        self.assertEqual(data["retention_policy"]["disposable_diagnostics_days"], 7)

        serialized = json.dumps(data)
        self.assertNotIn("AGYOS_PRIVATE_SENTINEL", serialized)


class DisasterRecoveryDrillTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="agyos-dr-test-"))
        self.state_dir = self.test_dir / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.state_dir / "agyos_state.sqlite"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_workspace_cli_recovers_corrupted_projection(self):
        cli = ROOT.parent / "bin" / "workspace-state.cjs"
        # 1. Initialize milestone
        init_res = subprocess.run(
            ["node", str(cli), "transact",
             "--db", str(self.db_path),
             "--milestone", "M-DR-01",
             "--expected-revision", "0",
             "--op", "op-dr-init",
             "--transition", "IDLE->UNDERSTAND"],
            capture_output=True, text=True, check=True
        )
        self.assertEqual(init_res.returncode, 0)
        out_init = json.loads(init_res.stdout)
        ms = out_init.get("milestone", out_init)
        self.assertEqual(ms["revision"], 1)
        self.assertEqual(ms["currentGate"], "UNDERSTAND")

        # 2. Corrupt state.json
        state_file = self.state_dir / "state.json"
        state_file.write_text("{CORRUPTED_JSON_DATA!!!", encoding="utf-8")

        # 3. Execute recovery projection from authoritative SQLite store
        proj_res = subprocess.run(
            ["node", str(cli), "project",
             "--db", str(self.db_path),
             "--milestone", "M-DR-01",
             "--out", str(state_file)],
            capture_output=True, text=True, check=True
        )
        self.assertEqual(proj_res.returncode, 0)

        # 4. Verify state.json is restored
        restored = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(restored["current_milestone"], "M-DR-01")
        self.assertEqual(restored["current_gate"], "UNDERSTAND")
        self.assertEqual(restored["revision"], 1)


if __name__ == "__main__":
    unittest.main()
