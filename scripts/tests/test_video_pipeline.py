"""Regression and unit tests for AGYOS video pipeline."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.video_pipeline import (
    audit_video_content,
    generate_vertical_script,
    validate_manim_scene,
)

ROOT = Path(__file__).resolve().parents[2]


class VideoPipelineScriptTests(unittest.TestCase):
    def test_generate_vertical_script_structure(self) -> None:
        script = generate_vertical_script("Memory Leaks in Python")

        self.assertEqual(script["format"], "9:16 Vertical Short (1080x1920)")
        self.assertEqual(script["safe_zone"]["active_window"], "1080x1400")
        self.assertEqual(script["safe_zone"]["top_clearance_px"], 200)
        self.assertEqual(script["safe_zone"]["bottom_clearance_px"], 320)
        self.assertIn("P13_safe_zone_clearance", script["principles_applied"])
        self.assertIn("P24_dual_track_captions", script["principles_applied"])
        self.assertIn("P114_prospective_memory_hold", script["principles_applied"])

    def test_generate_vertical_script_beats_and_dual_track(self) -> None:
        script = generate_vertical_script("Postgres Connection Pooling")
        beats = script["beats"]

        self.assertEqual(len(beats), 5)
        for beat in beats:
            self.assertIn("visual_track", beat)
            self.assertIn("voiceover", beat)
            self.assertIn("on_screen_text", beat)
            self.assertIn("audio_sfx", beat)

        self.assertEqual(script["terminal_reference_card"]["duration_seconds"], 2.0)

    def test_generate_vertical_script_empty_topic_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            generate_vertical_script("   ")


class VideoPipelineAuditTests(unittest.TestCase):
    def test_audit_passes_compliant_generated_script(self) -> None:
        script = generate_vertical_script("TCP Retransmission Spikes")
        # Render into markdown representation
        md_text = f"""# {script['title']}
Safe zone: 1080x1400 active window.
Visual track: display terminal output and error highlight.
Voiceover track: narration explains root cause.
Resolution: latency dropped and verified fix.
Hold static card at terminal for 2 seconds.
When deployment fails, run the diagnostics check.
"""
        result = audit_video_content(md_text)
        self.assertEqual(result["status"], "PASS")
        self.assertGreaterEqual(result["score"], 80)
        self.assertEqual(len(result["findings"]), 0)

    def test_audit_detects_vague_hype_hooks(self) -> None:
        content = "This changes everything! Watch until the end to discover the secret."
        result = audit_video_content(content)

        self.assertLess(result["score"], 80)
        severities = [f["severity"] for f in result["findings"]]
        self.assertIn("FAIL", severities)
        principles = [f["principle"] for f in result["findings"]]
        self.assertIn("P02_P08_calibrated_specificity", principles)

    def test_audit_detects_coercive_call_to_action(self) -> None:
        content = """Safe zone 1080x1400.
Visual track: error crop.
Voiceover: explanation.
Resolution: fix verified.
Terminal hold card: 2 seconds.
You must do this right now or your cluster will break!
"""
        result = audit_video_content(content)
        principles = [f["principle"] for f in result["findings"]]
        self.assertIn("P103_P104_autonomy_and_implementation_intentions", principles)


class VideoPipelineManimTests(unittest.TestCase):
    def test_validate_manim_scene_with_vertical_scene_template(self) -> None:
        template_path = ROOT / "tools/video/manim-shorts/templates/vertical_scene.py"
        self.assertTrue(template_path.is_file())

        result = validate_manim_scene(str(template_path))
        self.assertTrue(result["valid"])
        self.assertIn("VerticalScene", result["discovered_classes"])
        self.assertTrue(result["vertical_configured"])
        self.assertIn("preview_smoke", result["headless_commands"])
        self.assertIn("-w -l", result["headless_commands"]["preview_smoke"])
        self.assertIn("-w --hd", result["headless_commands"]["production_hd"])
        self.assertIn("-s", result["headless_commands"]["thumbnail_export"])

    def test_validate_manim_scene_with_example_scene(self) -> None:
        example_path = ROOT / "tools/video/manim-shorts/assets/example_scene.py"
        self.assertTrue(example_path.is_file())

        result = validate_manim_scene(str(example_path))
        self.assertTrue(result["valid"])
        self.assertIn("ExponentialConvergenceScene", result["discovered_classes"])
        self.assertTrue(result["vertical_configured"])

    def test_validate_manim_scene_syntax_error(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("def broken_code(:\n    pass\n")
            f_path = f.name

        try:
            result = validate_manim_scene(f_path)
            self.assertFalse(result["valid"])
            self.assertIn("syntax error", result["error"].lower())
        finally:
            Path(f_path).unlink(missing_ok=True)

    def test_validate_manim_scene_missing_file_raises_error(self) -> None:
        with self.assertRaises(FileNotFoundError):
            validate_manim_scene("non_existent_scene_file.py")


if __name__ == "__main__":
    unittest.main()
