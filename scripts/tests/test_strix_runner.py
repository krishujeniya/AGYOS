"""Regression and contract tests for AGYOS Strix security runner."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.strix_runner import (
    STRIX_ROOT,
    STRIX_SKILLS,
    check_status,
    list_skills,
    run_scan,
    test_inventory,
)

ROOT = Path(__file__).resolve().parents[2]


class StrixRunnerContractTests(unittest.TestCase):
    def test_strix_toolkit_present_and_path(self) -> None:
        status = check_status()
        self.assertTrue(status["strix_toolkit_present"])
        self.assertEqual(status["strix_path"], str(STRIX_ROOT))
        self.assertTrue(status["pyproject_found"])

    def test_strix_skills_count_and_membership(self) -> None:
        status = check_status()
        self.assertEqual(status["installed_skills_count"], len(STRIX_SKILLS))
        self.assertIn("penetration-testing-with-strix", status["installed_skills"])
        self.assertIn("managed-pentesting-with-strix", status["installed_skills"])
        self.assertIn("owasp-top-10-testing", status["installed_skills"])

    def test_list_skills_structure(self) -> None:
        skills = list_skills()
        self.assertEqual(len(skills), 9)
        names = [s["name"] for s in skills]
        self.assertIn("web-app-penetration-testing", names)
        self.assertIn("ci-security-scanning-with-strix", names)
        self.assertIn("find-security-vulnerabilities-in-code", names)
        for s in skills:
            self.assertTrue(Path(s["path"]).is_file())
            self.assertNotEqual(s["description"], "Not installed")

    def test_test_inventory(self) -> None:
        inv = test_inventory()
        self.assertGreater(inv["total_test_files"], 100)
        file_names = [f["name"] for f in inv["test_files"]]
        self.assertIn("test_execution.py", file_names)
        self.assertIn("test_sarif.py", file_names)

    def test_run_scan_dry_run(self) -> None:
        exit_code = run_scan(target="./", mode="quick", budget=10.0, dry_run=True)
        self.assertEqual(exit_code, 0)

    def test_direct_agy_mode_status(self) -> None:
        status = check_status()
        self.assertTrue(status.get("direct_agy_mode"))
        self.assertFalse(status.get("api_required"))
        self.assertTrue(status.get("agy_cli_available"))
        self.assertEqual(status.get("active_backend"), "agy")

    def test_meets_fail_threshold_evaluations(self) -> None:
        from scripts.agy_security_scanner import meets_fail_threshold

        self.assertTrue(meets_fail_threshold("critical", "high"))
        self.assertTrue(meets_fail_threshold("high", "high"))
        self.assertFalse(meets_fail_threshold("medium", "high"))
        self.assertFalse(meets_fail_threshold("low", "critical"))
        self.assertTrue(meets_fail_threshold("low", None))

    def test_direct_scan_clean_directory(self) -> None:
        import tempfile
        from scripts.agy_security_scanner import execute_agy_direct_scan

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            clean_file = tmp_path / "app.py"
            clean_file.write_text("def hello():\n    return 'Hello, World!'\n", encoding="utf-8")

            runs_dir = tmp_path / "strix_runs"
            exit_code = execute_agy_direct_scan(
                target=str(tmp_path),
                mode="quick",
                run_name="test_clean_run",
                output_base=runs_dir,
            )
            self.assertEqual(exit_code, 0)
            run_dir = runs_dir / "test_clean_run"
            self.assertTrue((run_dir / "run.json").is_file())
            self.assertTrue((run_dir / "findings.sarif").is_file())
            self.assertTrue((run_dir / "penetration_test_report.md").is_file())
            self.assertTrue((run_dir / "vulnerabilities.json").is_file())

    def test_database_uri_secret_detection(self) -> None:
        import tempfile
        from scripts.agy_security_scanner import AgySecurityScanner

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            vuln_file = tmp_path / "config.py"
            vuln_file.write_text("DB_URI = 'postgres://admin:SuperSecretPass123@db.internal:5432/prod'\n", encoding="utf-8")

            scanner = AgySecurityScanner(target=str(tmp_path), mode="quick")
            findings = scanner.scan()
            self.assertGreaterEqual(len(findings), 1)
            uri_finding = next((f for f in findings if "Database Connection URI" in f["title"]), None)
            self.assertIsNotNone(uri_finding)
            self.assertEqual(uri_finding["severity"], "critical")
            self.assertEqual(uri_finding["cwe_id"], "CWE-798")
