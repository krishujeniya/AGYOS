"""Unit tests for AGYOS TOON configuration parser and serializer (toon_config.py)."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.toon_config import (
    load_toon_config,
    dump_toon_config,
    load_toon_manifest,
    dump_toon_manifest,
)


class TestToonConfig(unittest.TestCase):
    def test_dump_and_load_simple_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toon"
            data = {
                "version": "3.1.0",
                "enabled": True,
                "timeout": 30,
                "threshold": 0.85,
                "tags": ["alpha", "beta", "gamma"],
            }
            dump_toon_config(data, path)
            loaded = load_toon_config(path)

            self.assertEqual(loaded["version"], "3.1.0")
            self.assertEqual(loaded["enabled"], True)
            self.assertEqual(loaded["timeout"], 30)
            self.assertEqual(loaded["threshold"], 0.85)
            self.assertEqual(loaded["tags"], ["alpha", "beta", "gamma"])

    def test_dump_and_load_tabular_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.toon"
            records = [
                {"name": "clean-code", "tier": "1", "domain": "engineering"},
                {"name": "pytest-runner", "tier": "2", "domain": "testing"},
                {"name": "systematic-debugging", "tier": "1", "domain": "engineering"},
            ]
            metadata = {
                "version": "3.1.0",
                "total_skills": 3,
            }
            dump_toon_manifest(records, path, key_name="skills", metadata=metadata)
            loaded_records = load_toon_manifest(path)

            self.assertEqual(len(loaded_records), 3)
            self.assertEqual(loaded_records[0]["name"], "clean-code")
            self.assertEqual(loaded_records[1]["tier"], "2")
            self.assertEqual(loaded_records[2]["domain"], "engineering")

    def test_json_fallback_when_toon_absent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "fallback.json"
            toon_path = Path(tmpdir) / "fallback.toon"
            json_path.write_text(json.dumps({"key": "value", "count": 42}), encoding="utf-8")

            # Asking for fallback.toon when only fallback.json exists
            loaded = load_toon_config(toon_path)
            self.assertEqual(loaded["key"], "value")
            self.assertEqual(loaded["count"], 42)

    def test_active_agents_config_toon_exists_and_parses(self):
        config_path = ROOT / ".agents" / "config.toon"
        self.assertTrue(config_path.is_file(), ".agents/config.toon should exist")
        cfg = load_toon_config(config_path)
        self.assertIn("linked_repos", cfg)

    def test_active_skills_manifest_toon_exists_and_parses(self):
        manifest_path = ROOT / ".agents" / "skills-manifest.toon"
        self.assertTrue(manifest_path.is_file(), ".agents/skills-manifest.toon should exist")
        records = load_toon_manifest(manifest_path)
        self.assertGreaterEqual(len(records), 2000, f"Expected >= 2000 skills in TOON manifest, got {len(records)}")

    def test_active_tier1_skills_toon_exists_and_parses(self):
        tier1_path = ROOT / ".agents" / "tier1-skills.toon"
        self.assertTrue(tier1_path.is_file(), ".agents/tier1-skills.toon should exist")
        records = load_toon_manifest(tier1_path)
        self.assertGreaterEqual(len(records), 300, f"Expected >= 300 tier 1 skills in TOON manifest, got {len(records)}")


if __name__ == "__main__":
    unittest.main()
