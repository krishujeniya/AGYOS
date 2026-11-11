import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / ".agents/skills/faceless-shorts-engine/scripts"))
from generate_shorts_manifest import VALID_STYLES, build_manifest


class FacelessManifestTests(unittest.TestCase):
    def test_style_ids_match_the_supplied_toolkit(self):
        self.assertEqual(
            set(VALID_STYLES),
            {"deep-dive", "night-file", "inside-out", "stick-story", "paper-atlas", "tall-tale"},
        )

    def test_plan_does_not_invent_voice_timing_or_render_settings(self):
        plan = build_manifest("Example", "A sourced topic", "deep-dive", 35)
        self.assertEqual(plan["style"]["key"], "deep-dive")
        self.assertEqual(plan["scenes"], [])
        self.assertIsNone(plan["narration"]["voice_id"])
        self.assertIsNone(plan["narration"]["mode"])
        self.assertIsNone(plan["subtitles"]["timing_source"])
        self.assertEqual(plan["render"], {})
        self.assertNotIn("fps", plan["project"])
        self.assertNotIn("estimated_word_count", plan["project"])

    def test_rejects_missing_brief_fields_and_nonpositive_duration(self):
        for values in (
            ("", "topic", "deep-dive", 35),
            ("title", "", "deep-dive", 35),
            ("title", "topic", "deep-dive", 0),
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                build_manifest(*values)

    def test_cli_writes_plan_and_refuses_to_replace_without_force(self):
        script = repo_root / ".agents/skills/faceless-shorts-engine/scripts/generate_shorts_manifest.py"
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "plan.json"
            command = [
                sys.executable,
                str(script),
                "--title", "Example",
                "--topic", "A sourced topic",
                "--style", "deep-dive",
                "--out", str(output),
            ]
            created = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(created.returncode, 0, created.stderr)
            self.assertEqual(json.loads(output.read_text())["status"], "planning_only")

            refused = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(refused.returncode, 2)
            self.assertIn("already exists", refused.stderr)

            replaced = subprocess.run(command + ["--force"], text=True, capture_output=True, check=False)
            self.assertEqual(replaced.returncode, 0, replaced.stderr)


if __name__ == "__main__":
    unittest.main()
