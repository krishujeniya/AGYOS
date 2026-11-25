"""Tests for Software Bill of Materials (SBOM) and License Compliance."""

import json
from pathlib import Path
import unittest

from scripts.generate_sbom import generate_sbom, ALLOWED_LICENSES

ROOT = Path(__file__).resolve().parents[2]


class SbomAndLicenseTests(unittest.TestCase):
    def test_sbom_generation_produces_compliant_report(self):
        doc, compliant = generate_sbom()
        self.assertTrue(compliant, "All runtime components must adhere to allowed licenses")
        self.assertEqual(doc["bomFormat"], "CycloneDX-lite")
        self.assertGreater(doc["compliance"]["totalComponents"], 0)
        self.assertEqual(doc["compliance"]["nonCompliantCount"], 0)
        self.assertEqual(doc["compliance"]["status"], "PASSED")

    def test_sbom_contains_pinned_python_components(self):
        doc, _ = generate_sbom()
        py_components = [c for c in doc["components"] if c["ecosystem"] == "pypi"]
        names = {c["name"].lower() for c in py_components}
        self.assertIn("jsonschema", names)
        self.assertIn("pyyaml", names)
        for c in py_components:
            self.assertIn(c["license"], ALLOWED_LICENSES)
            self.assertTrue(c["allowed"])

    def test_sbom_contains_node_runtime_components(self):
        doc, _ = generate_sbom()
        node_components = [c for c in doc["components"] if c["ecosystem"] == "npm"]
        if node_components:
            for c in node_components:
                self.assertIn(c["license"], ALLOWED_LICENSES)
                self.assertTrue(c["allowed"])


if __name__ == "__main__":
    unittest.main()
