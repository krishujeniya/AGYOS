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
