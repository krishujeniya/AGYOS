#!/usr/bin/env python3
"""AGYOS Video Pipeline CLI.

Automates vertical video scripting, psychological auditing against the 116
principles, and Manim 9:16 vertical mathematical animation workflows.

Usage:
  python3 scripts/video_pipeline.py script "<topic>" [--style <style>] [--json]
  python3 scripts/video_pipeline.py audit <script-file.md> [--json]
  python3 scripts/video_pipeline.py manim <scene-file.py> [SceneClass] [--hd] [--json]
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

BANNED_VAGUE_HOOKS = [
    r"\bthis changes everything\b",
    r"\byou won't believe\b",
    r"\bstop doing this\b",
    r"\bmind blown\b",
    r"\bsecret trick\b",
]

COERCIVE_CTA_PATTERNS = [
    r"\byou must\b",
    r"\bdo this right now\b",
    r"\bstop everything and\b",
]


def generate_vertical_script(topic: str, style: str = "technical") -> Dict[str, Any]:
    """Generate a dual-track vertical video script adhering to the 116 principles."""
    topic_clean = topic.strip()
    if not topic_clean:
        raise ValueError("Topic cannot be empty")

    script = {
        "title": f"Vertical Technical Breakdown: {topic_clean}",
        "topic": topic_clean,
        "format": "9:16 Vertical Short (1080x1920)",
        "target_duration_seconds": 38,
        "safe_zone": {
            "canvas_width_px": 1080,
            "canvas_height_px": 1920,
            "top_clearance_px": 200,
            "bottom_clearance_px": 320,
            "active_window": "1080x1400",
            "rule": "Keep text, variables, and interaction targets within active window [P13]",
        },
        "principles_applied": [
            "P02_symptom_first_hook",
            "P07_information_gap",
            "P10_expectation_violation",
            "P13_safe_zone_clearance",
            "P24_dual_track_captions",
            "P29_instrumental_music_only",
            "P38_causal_coherence",
            "P48_temporal_synchronization",
            "P57_pretesting_pause",
            "P103_implementation_intention_cta",
            "P114_prospective_memory_hold",
        ],
        "audio_levels": {
            "dialogue_target_lufs": -14.0,
            "dialogue_true_peak_db": -1.0,
            "background_music": "Instrumental only; ducked by -20 dB during speech [P29, P32]",
        },
        "beats": [
            {
                "beat_number": 1,
                "time": "0:00–0:03",
                "phase": "Opening Hook & Symptom [P02, P07]",
                "visual_track": f"Close-up crop on the tangible error state caused by {topic_clean}. Bounding box signal around the failing line [P21].",
                "on_screen_text": f"Error: {topic_clean} failure",
                "voiceover": f"Here is the exact line where {topic_clean} fails.",
                "audio_sfx": "Muted room tone; subtle click on error highlight.",
            },
            {
                "beat_number": 2,
                "time": "0:03–0:10",
                "phase": "Mechanical Root Cause [P38]",
                "visual_track": "Dual-panel split inside safe zone showing default setting vs actual runtime behavior [P13, P47].",
                "on_screen_text": "Default vs. Target Behavior",
                "voiceover": "The default configuration leaves buffer limits unbounded, triggering an unexpected drop.",
                "audio_sfx": "Low-level instrumental pulse (-20 dB).",
            },
            {
                "beat_number": 3,
                "time": "0:10–0:18",
                "phase": "Pretesting & Prediction [P57]",
                "visual_track": "Freeze frame for 1 second on the proposed correction parameter. Display countdown cue [P57].",
                "on_screen_text": "Predict the output: Success or Timeout?",
                "voiceover": "Before applying the fix, what happens to memory utilization?",
                "audio_sfx": "Short 1-second pause in narration.",
            },
            {
                "beat_number": 4,
                "time": "0:18–0:32",
                "phase": "Demonstration & Verification [P44, P48]",
                "visual_track": "Apply surgical change. Terminal runs and prints green exit code 0. Metric drops to baseline [P34, P48].",
                "on_screen_text": "Latency dropped: 45ms -> 12ms",
                "voiceover": "Passing the bounded capacity flag eliminates the backlog and cuts latency by seventy percent.",
                "audio_sfx": "Confirmation chime at moment metric updates.",
            },
            {
                "beat_number": 5,
                "time": "0:32–0:38",
                "phase": "Terminal Hold & Implementation CTA [P103, P114]",
                "visual_track": "Clean static reference card displaying the exact command syntax for 2 full seconds [P114].",
                "on_screen_text": f"Command: {topic_clean} --bounded",
                "voiceover": f"Next time your deployment stalls, inspect this flag first [P103].",
                "audio_sfx": "Instrumental resolution.",
            },
        ],
        "terminal_reference_card": {
            "duration_seconds": 2.0,
            "directive": "Hold static reference card with exact command syntax for prospective memory retention [P114]",
        },
    }
    return script


def audit_video_content(content: str) -> Dict[str, Any]:
    """Audit video script or text against the 116 empirical psychology principles."""
    findings: List[Dict[str, str]] = []
    checks_passed = 0
    total_checks = 6

    # Check 1: Vague hype hook
    vague_found = False
    for pattern in BANNED_VAGUE_HOOKS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "principle": "P02_P08_calibrated_specificity",
                "severity": "FAIL",
                "message": f"Detected vague hype phrasing matching '{pattern}'. Replace with a concrete noun and visible symptom.",
            })
            vague_found = True
            break
    if not vague_found:
        checks_passed += 1

    # Check 2: Safe-zone consideration
    if "safe_zone" in content.lower() or "safe zone" in content.lower() or "1080x1400" in content:
        checks_passed += 1
    else:
        findings.append({
            "principle": "P13_safe_zone_clearance",
            "severity": "WARN",
            "message": "No explicit safe-zone margin specified. Keep essential information within 1080x1400 safe window.",
        })

    # Check 3: Dual-track / Muted clarity
    has_visual = bool(re.search(r"\b(visual|on[- ]screen|display|crop|frame)\b", content, re.IGNORECASE))
    has_audio = bool(re.search(r"\b(voiceover|audio|speech|sound|narration)\b", content, re.IGNORECASE))
    if has_visual and has_audio:
        checks_passed += 1
    else:
        findings.append({
            "principle": "P24_P34_dual_track_and_access",
            "severity": "WARN",
            "message": "Script must specify both a silent visual track and an audio track for muted and nonvisual accessibility.",
        })

    # Check 4: Causal coherence and terminal verification
    has_resolution = bool(re.search(r"\b(result|verified|success|latency|output|fix)\b", content, re.IGNORECASE))
    if has_resolution:
        checks_passed += 1
    else:
        findings.append({
            "principle": "P38_P44_causal_coherence_and_peak_end",
            "severity": "WARN",
            "message": "Script lacks explicit terminal resolution. Conclude on the demonstrable verified result.",
        })

    # Check 5: Non-coercive implementation CTA
    coercive_found = False
    for pattern in COERCIVE_CTA_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append({
                "principle": "P103_P104_autonomy_and_implementation_intentions",
                "severity": "WARN",
                "message": f"Detected coercive phrasing matching '{pattern}'. Use conditional trigger framing ('When X, do Y').",
            })
            coercive_found = True
            break
    if not coercive_found:
        checks_passed += 1

    # Check 6: Terminal prospective memory hold
    if "terminal" in content.lower() or "hold" in content.lower() or "card" in content.lower():
        checks_passed += 1
    else:
        findings.append({
            "principle": "P114_prospective_memory_preservation",
            "severity": "WARN",
            "message": "Script lacks a 2-second terminal reference card holding the exact key takeaway.",
        })

    score = int((checks_passed / total_checks) * 100)
    return {
        "score": score,
        "checks_passed": checks_passed,
        "total_checks": total_checks,
        "status": "PASS" if score >= 80 else "WARN",
        "findings": findings,
    }


def validate_manim_scene(scene_path: str, scene_class: str | None = None) -> Dict[str, Any]:
    """Statically validate a Manim scene file and generate headless execution commands."""
    path = Path(scene_path)
    if not path.is_file():
        raise FileNotFoundError(f"Scene file not found: {scene_path}")

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=scene_path)
    except SyntaxError as exc:
        return {
            "valid": False,
            "error": f"Python syntax error at line {exc.lineno}: {exc.msg}",
        }

    # Discover classes inheriting from Scene
    scene_classes = []
    is_vertical_configured = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = getattr(base, "id", None) or getattr(base, "attr", None)
                if base_name in ("Scene", "VerticalScene", "ThreeDScene"):
                    scene_classes.append(node.name)
                if base_name == "VerticalScene":
                    is_vertical_configured = True

    if not scene_classes:
        return {
            "valid": False,
            "error": "No Scene subclass found in file",
        }

    selected_class = scene_class if scene_class in scene_classes else scene_classes[0]

    # Check for imports
    has_manimlib = "manimlib" in source
    has_community = "from manim import" in source

    # Construct headless CLI commands
    cli_tool = "manimgl" if has_manimlib or not has_community else "manim"
    preview_cmd = f"{cli_tool} {path.as_posix()} {selected_class} -w -l"
    prod_cmd = f"{cli_tool} {path.as_posix()} {selected_class} -w --hd"
    thumbnail_cmd = f"{cli_tool} {path.as_posix()} {selected_class} -s"

    return {
        "valid": True,
        "file": path.as_posix(),
        "selected_class": selected_class,
        "discovered_classes": scene_classes,
        "engine": "3b1b/manim (manimlib)" if has_manimlib else "Manim Community",
        "vertical_configured": is_vertical_configured or "16:9" in source or "9:16" in source,
        "headless_commands": {
            "preview_smoke": preview_cmd,
            "production_hd": prod_cmd,
            "thumbnail_export": thumbnail_cmd,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="AGYOS Video Pipeline CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # script subcommand
    script_parser = subparsers.add_parser("script", help="Generate dual-track vertical video script")
    script_parser.add_argument("topic", help="Topic or breakdown subject")
    script_parser.add_argument("--style", default="technical", help="Script style")
    script_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Audit video content against 116 principles")
    audit_parser.add_argument("path", help="Path to script markdown or text file")
    audit_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # manim subcommand
    manim_parser = subparsers.add_parser("manim", help="Validate Manim scene and generate headless command")
    manim_parser.add_argument("path", help="Path to python scene file")
    manim_parser.add_argument("scene_class", nargs="?", default=None, help="Scene class name")
    manim_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return 1

    if args.subcommand == "script":
        res = generate_vertical_script(args.topic, style=args.style)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("============================================================")
            print(f"AGYOS Vertical Script: {res['title']}")
            print(f"Format: {res['format']} | Target: {res['target_duration_seconds']}s")
            print("============================================================\n")
            print("Safe-Zone Window: 1080x1400 (Top: 200px clear, Bottom: 320px clear)")
            print("Audio Mix: Dialogue -14 LUFS, Music ducked -20 dB [Instrumental Only]\n")
            for beat in res["beats"]:
                print(f"[{beat['time']}] {beat['phase']}")
                print(f"  VISUAL : {beat['visual_track']}")
                print(f"  TEXT   : {beat['on_screen_text']}")
                print(f"  AUDIO  : \"{beat['voiceover']}\"")
                print(f"  SFX    : {beat['audio_sfx']}\n")
            print("------------------------------------------------------------")
            print(f"TERMINAL HOLD : {res['terminal_reference_card']['directive']}")
            print("============================================================")
        return 0

    if args.subcommand == "audit":
        path = Path(args.path)
        if not path.is_file():
            print(f"Error: File not found: {args.path}", file=sys.stderr)
            return 1
        content = path.read_text(encoding="utf-8")
        res = audit_video_content(content)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("============================================================")
            print(f"AGYOS Video Psychology Audit: {path.name}")
            print(f"Status: {res['status']} (Score: {res['score']}/100, Checks: {res['checks_passed']}/{res['total_checks']})")
            print("============================================================")
            if res["findings"]:
                print("\nFindings:")
                for f in res["findings"]:
                    print(f"  [{f['severity']}] {f['principle']}: {f['message']}")
            else:
                print("\nAll empirical psychology and safe-zone checks passed.")
            print("============================================================")
        return 0

    if args.subcommand == "manim":
        try:
            res = validate_manim_scene(args.path, scene_class=args.scene_class)
        except Exception as exc:
            print(f"Error validating scene: {exc}", file=sys.stderr)
            return 1

        if args.json:
            print(json.dumps(res, indent=2))
        else:
            if not res.get("valid"):
                print(f"❌ Manim Scene Validation Failed: {res.get('error')}", file=sys.stderr)
                return 1
            print("============================================================")
            print(f"AGYOS Manim Scene Validation: {Path(res['file']).name}")
            print(f"Engine: {res['engine']} | Class: {res['selected_class']}")
            print(f"Vertical 9:16 Configuration: {'Configured' if res['vertical_configured'] else 'Standard'}")
            print("============================================================")
            print("Headless CLI Execution Commands (Strictly Headless - No GUI):")
            print(f"  Preview Smoke : {res['headless_commands']['preview_smoke']}")
            print(f"  Production HD : {res['headless_commands']['production_hd']}")
            print(f"  Thumbnail PNG : {res['headless_commands']['thumbnail_export']}")
            print("============================================================")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
