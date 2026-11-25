"""Regression and unit tests for AGYOS video pipeline."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.video_pipeline import (
    audit_video_content,
    build_edl_ffmpeg_plan,
    generate_veo_prompt,
    generate_vertical_script,
    pack_transcript,
    parse_blackdetect_output,
    remap_srt_for_edl,
    route_video_workflow,
    validate_edl,
    validate_manim_scene,
)
from scripts.organic_film_engine import (
    build_handheld_drift_filter,
    build_organic_master_filter_complex,
)
from scripts.repair_ai_video import (
    build_loudnorm_pass2_filter,
    build_repair_filter,
    parse_ebur128_summary,
)
from scripts.remove_flow_watermark import fallback_watermark_box

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
        template_path = ROOT / "plugins/tools/video/manim-shorts/templates/vertical_scene.py"
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
        example_path = ROOT / "plugins/tools/video/manim-shorts/assets/example_scene.py"
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


class VideoStudioWorkflowAndEdlTests(unittest.TestCase):
    def test_route_video_workflow_selects_expected_pipelines(self) -> None:
        clip_route = route_video_workflow("clip this podcast into vertical shorts with chopify")
        self.assertEqual(clip_route["mode"], "long_to_short_clipping")
        self.assertEqual(clip_route["primary_skill"], "chopify")

        flow_route = route_video_workflow("generate cinematic b-roll with google flow and remove AI look")
        self.assertEqual(flow_route["mode"], "generative_ai_cinema")
        self.assertEqual(flow_route["primary_skill"], "google-flow")

        manim_route = route_video_workflow("create a 3b1b manim calculus animation")
        self.assertEqual(manim_route["mode"], "mathematical_explainer")
        self.assertEqual(manim_route["primary_skill"], "3b1b-manim")

    def test_generate_veo_prompt_follows_five_part_formula(self) -> None:
        res = generate_veo_prompt("a watchmaker assembling brass gears", ratio="9:16", duration=8, style="cinema")
        self.assertEqual(res["ratio"], "9:16")
        self.assertEqual(res["duration"], 8)
        for marker in ("[Cinematography]:", "[Subject & Action]:", "[Context & Negative Constraints]:", "[Style & Ambiance]:", "[Soundstage]:"):
            self.assertIn(marker, res["prompt"])
        self.assertIn("[00:00-00:04]", res["timestamp_prompt_template"])

    def test_pack_transcript_supports_chopify_and_editor_schemas(self) -> None:
        chopify_tr = {
            "source": "/tmp/podcast.mp4",
            "duration": 12.0,
            "words": [
                {"word": "First", "start": 0.5, "end": 0.9},
                {"word": "line.", "start": 0.95, "end": 1.3},
                {"word": "Second", "start": 2.5, "end": 2.9},
                {"word": "line.", "start": 2.95, "end": 3.4},
            ],
        }
        packed = pack_transcript(chopify_tr, gap_threshold=0.5)
        self.assertIn("## podcast", packed)
        self.assertIn("(silence 1.20s)", packed)
        self.assertIn("w0-w1: First line.", packed)
        self.assertIn("w2-w3: Second line.", packed)

    def test_edl_validate_remap_srt_and_ffmpeg_plan_hard_rules(self) -> None:
        edl = {
            "version": 1,
            "sources": {"A": "/tmp/a.mp4"},
            "ranges": [
                {"source": "A", "start": 1.0, "end": 4.0, "beat": "HOOK"},
                {"source": "A", "start": 10.0, "end": 15.0, "beat": "PAYOFF"},
            ],
            "grade": "warm_cinematic",
            "overlays": [{"file": "/tmp/ov.mp4", "start_in_output": 2.0, "duration": 3.0}],
            "subtitles": "/tmp/master.srt",
        }
        val = validate_edl(edl, check_files=False)
        self.assertTrue(val["valid"])
        self.assertEqual(val["total_duration_s"], 8.0)
        self.assertEqual(val["segments"][1]["output_start"], 3.0)

        words = [
            {"word": "Hook", "start": 1.2, "end": 1.6},
            {"word": "word.", "start": 1.7, "end": 2.1},
            {"word": "Payoff", "start": 10.5, "end": 11.0},
            {"word": "here.", "start": 11.1, "end": 11.5},
        ]
        srt = remap_srt_for_edl(edl, {"A": words}, words_per_cue=2)
        self.assertIn("00:00:00,200 --> 00:00:01,100", srt)
        self.assertIn("00:00:03,500 --> 00:00:04,500", srt)

        plan = build_edl_ffmpeg_plan(edl, "/tmp/out.mp4", "/tmp/work")
        self.assertTrue(plan["subtitles_applied_last"])
        self.assertEqual(plan["boundary_fade_seconds"], 0.03)
        seg0_cmd = " ".join(plan["segment_commands"][0])
        self.assertIn("afade=t=in:st=0:d=0.03", seg0_cmd)
        self.assertIn("afade=t=out:st=2.970:d=0.03", seg0_cmd)
        final_cmd = " ".join(plan["final_command"])
        self.assertIn("setpts=PTS-STARTPTS+2.000/TB", final_cmd)
        self.assertLess(final_cmd.index("overlay="), final_cmd.index("subtitles="))
        self.assertIn("loudnorm=I=-14:TP=-1.0:LRA=11", final_cmd)

    def test_organic_film_and_repair_helpers(self) -> None:
        drift_vertical = build_handheld_drift_filter(1080, 1920)
        self.assertIn("scale=1080:1920:flags=lanczos", drift_vertical)
        self.assertNotIn("1280:720", drift_vertical)

        master_fc = build_organic_master_filter_complex("vertical-clean", include_shutter=True)
        self.assertIn("tblend=all_mode=average", master_fc)
        self.assertIn("lenscorrection", master_fc)

        repair_vf = build_repair_filter()
        self.assertIn("deflicker=", repair_vf)
        self.assertIn("deband=", repair_vf)

        ebur_sample = """
        Summary:
          Integrated loudness:
            I:         -14.2 LUFS
          Loudness range:
            LRA:         6.4 LU
          True peak:
            Peak:       -1.1 dBFS
        """
        parsed = parse_ebur128_summary(ebur_sample)
        self.assertEqual(parsed["integrated_lufs"], -14.2)
        self.assertEqual(parsed["lra_lu"], 6.4)
        self.assertEqual(parsed["true_peak_dbtp"], -1.1)

        ln_filter = build_loudnorm_pass2_filter({
            "input_i": "-20.1",
            "input_tp": "-2.5",
            "input_lra": "7.2",
            "input_thresh": "-30.4",
            "target_offset": "0.3",
        })
        self.assertIn("linear=true", ln_filter)
        self.assertIn("measured_I=-20.1", ln_filter)

        blacks = parse_blackdetect_output("[blackdetect @ 0x1] black_start:1.5 black_end:2.0 black_duration:0.5")
        self.assertEqual(len(blacks), 1)
        self.assertEqual(blacks[0]["duration"], 0.5)

        self.assertEqual(fallback_watermark_box(1080, 1920), (1014, 1872, 54, 33))
        self.assertEqual(fallback_watermark_box(1280, 720), (1236, 688, 36, 22))


if __name__ == "__main__":
    unittest.main()
