"""Privacy audit outputs metadata only and never claims blanket E2EE."""
from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "scripts/agyos-privacy-audit.py"


class PrivacyAuditTests(unittest.TestCase):
    def test_audit_reports_unencrypted_trust_boundaries(self):
        result = subprocess.run(
            [sys.executable, str(AUDIT)],
            capture_output=True, text=True, check=True, timeout=20,
        )
        report = json.loads(result.stdout)
        self.assertFalse(report["full_e2ee"])
        self.assertEqual(report["conclusion"], "PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE")
        self.assertGreaterEqual(len(report["surfaces"]), 4)
        self.assertTrue(any(item["surface"] == ".agents/state/state.json" for item in report["surfaces"]))
        self.assertNotIn('"project": "New ANCHOR Project"', result.stdout)
        self.assertNotIn('"user_preferences":', result.stdout)

    def test_strict_mode_cannot_claim_complete_encryption(self):
        result = subprocess.run(
            [sys.executable, str(AUDIT), "--strict"],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["full_e2ee"])


if __name__ == "__main__":
    unittest.main()
