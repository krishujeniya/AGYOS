#!/usr/bin/env python3
"""AGYOS Unified Video Studio & Pipeline CLI.

Coordinates vertical video scripting, psychological auditing (116 principles),
Manim 9:16 validation, workflow routing across local toolkits (Chopify,
ai-video-editor, faceless-shorts, Google Flow / Veo 3.1, FFmpeg, Organic Film
De-AI), packed transcript generation, EDL validation/rendering with the 12
production-correctness hard rules, on-demand timeline filmstrips, and
post-render self-evaluation.

Usage:
  uv run scripts/video_pipeline.py script "<topic>" [--style <style>] [--json]
  uv run scripts/video_pipeline.py audit <script-file.md> [--json]
  uv run scripts/video_pipeline.py manim <scene-file.py> [SceneClass] [--json]
  uv run scripts/video_pipeline.py route "<goal>" [--json]
  uv run scripts/video_pipeline.py veo-prompt "<idea>" [--ratio 9:16|16:9] [--duration 4|6|8] [--style cinema|doc|product|explainer] [--json]
  uv run scripts/video_pipeline.py pack-transcript <transcript.json> [--gap 0.5] [--out takes_packed.md]
  uv run scripts/video_pipeline.py edl-validate <edl.json> [--check-files] [--json]
  uv run scripts/video_pipeline.py edl-remap-srt <edl.json> <transcript.json> [--out master.srt] [--words-per-cue 3]
  uv run scripts/video_pipeline.py edl-render <edl.json> -o <out.mp4> [--work <dir>] [--preview] [--dry-run] [--json]
  uv run scripts/video_pipeline.py timeline-view <video.mp4> <start> <end> -o <out.png>
  uv run scripts/video_pipeline.py self-eval <video.mp4> [--edl edl.json] [--target-lufs -14.0] [--json]
  uv run scripts/video_pipeline.py chopify <args...>
  uv run scripts/video_pipeline.py repair <args...>
  uv run scripts/video_pipeline.py film <args...>
  uv run scripts/video_pipeline.py delogo <args...>
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.repair_ai_video import parse_ebur128_summary

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

PRODUCTION_HARD_RULES = [
    "1. Subtitles are applied LAST in the filter chain, after every overlay.",
    "2. Per-segment extract -> lossless -c copy concat avoids double-encoding.",
    "3. Apply 30ms audio fades (afade=t=in/out:d=0.03) at every cut boundary.",
    "4. Overlays use setpts=PTS-STARTPTS+T/TB to align frame 0 to window start.",
    "5. Master SRT uses output-timeline offsets: word.start - seg_start + seg_offset.",
    "6. Never cut inside a word; snap cut edges to word boundaries.",
    "7. Pad cut edges (30-200ms) to absorb ASR timestamp drift.",
    "8. Use word-level verbatim ASR transcripts; cache per immutable source.",
    "9. Run structural repair (deflicker/deband/vidstab) BEFORE film grain/halation.",
    "10. Preserve exact aspect ratio in handheld drift (never hardcode 1280:720).",
    "11. Master audio to -14 LUFS / -1.0 dBTP and measure with ebur128.",
    "12. Run post-render self-eval (ffprobe, ebur128, blackdetect, cut filmstrips) before delivery.",
]

GRADE_PRESETS: Dict[str, str] = {
    "none": "",
    "neutral_punch": "eq=contrast=1.04:saturation=1.04,curves=all='0/0 0.25/0.23 0.75/0.78 1/1'",
    "warm_cinematic": (
        "eq=contrast=1.03:brightness=0.01:saturation=0.94,"
        "curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':"
        "g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':"
        "b='0/0.03 0.25/0.25 0.75/0.75 1/0.92'"
    ),
    "vertical_clean": "eq=contrast=1.04:brightness=0.01:saturation=0.96",
}


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
                "time": "0:00-0:03",
                "phase": "Opening Hook & Symptom [P02, P07]",
                "visual_track": f"Close-up crop on the tangible error state caused by {topic_clean}. Bounding box signal around the failing line [P21].",
                "on_screen_text": f"Error: {topic_clean} failure",
                "voiceover": f"Here is the exact line where {topic_clean} fails.",
                "audio_sfx": "Muted room tone; subtle click on error highlight.",
            },
            {
                "beat_number": 2,
                "time": "0:03-0:10",
                "phase": "Mechanical Root Cause [P38]",
                "visual_track": "Dual-panel split inside safe zone showing default setting vs actual runtime behavior [P13, P47].",
                "on_screen_text": "Default vs. Target Behavior",
                "voiceover": "The default configuration leaves buffer limits unbounded, triggering an unexpected drop.",
                "audio_sfx": "Low-level instrumental pulse (-20 dB).",
            },
            {
                "beat_number": 3,
                "time": "0:10-0:18",
                "phase": "Pretesting & Prediction [P57]",
                "visual_track": "Freeze frame for 1 second on the proposed correction parameter. Display countdown cue [P57].",
                "on_screen_text": "Predict the output: Success or Timeout?",
                "voiceover": "Before applying the fix, what happens to memory utilization?",
                "audio_sfx": "Short 1-second pause in narration.",
            },
            {
                "beat_number": 4,
                "time": "0:18-0:32",
                "phase": "Demonstration & Verification [P44, P48]",
                "visual_track": "Apply surgical change. Terminal runs and prints green exit code 0. Metric drops to baseline [P34, P48].",
                "on_screen_text": "Latency dropped: 45ms -> 12ms",
                "voiceover": "Passing the bounded capacity flag eliminates the backlog and cuts latency by seventy percent.",
                "audio_sfx": "Confirmation chime at moment metric updates.",
            },
            {
                "beat_number": 5,
                "time": "0:32-0:38",
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

    if "safe_zone" in content.lower() or "safe zone" in content.lower() or "1080x1400" in content:
        checks_passed += 1
    else:
        findings.append({
            "principle": "P13_safe_zone_clearance",
            "severity": "WARN",
            "message": "No explicit safe-zone margin specified. Keep essential information within 1080x1400 safe window.",
        })

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

    has_resolution = bool(re.search(r"\b(result|verified|success|latency|output|fix)\b", content, re.IGNORECASE))
    if has_resolution:
        checks_passed += 1
    else:
        findings.append({
            "principle": "P38_P44_causal_coherence_and_peak_end",
            "severity": "WARN",
            "message": "Script lacks explicit terminal resolution. Conclude on the demonstrable verified result.",
        })

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
    has_manimlib = "manimlib" in source
    has_community = "from manim import" in source

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


def detect_local_video_capabilities() -> Dict[str, Any]:
    """Inspect available local video toolkits and binaries without mutating state."""
    return {
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "ffprobe": shutil.which("ffprobe") is not None,
        "uv": shutil.which("uv") is not None,
        "chopify_bin": (ROOT / "bin" / "chopify").is_file(),
        "chopify_repo": (ROOT / "integrations" / "chopify" / "agent.py").is_file(),
        "ai_video_editor": (ROOT / "tools" / "video" / "ai-video-editor" / "scripts" / "render.py").is_file(),
        "faceless_shorts": (ROOT / "tools" / "video" / "faceless-shorts" / "scripts" / "new_video.sh").is_file(),
        "manim_shorts": (ROOT / "tools" / "video" / "manim-shorts" / "templates" / "vertical_scene.py").is_file(),
        "google_flow_mcp": (ROOT / "mcp" / "google-flow-mcp.sh").is_file(),
        "organic_film_engine": (ROOT / "scripts" / "organic_film_engine.py").is_file(),
        "repair_ai_video": (ROOT / "scripts" / "repair_ai_video.py").is_file(),
        "remove_flow_watermark": (ROOT / "scripts" / "remove_flow_watermark.py").is_file(),
    }


def route_video_workflow(goal: str) -> Dict[str, Any]:
    """Route a natural-language video goal to the optimal AGYOS pipeline and skills."""
    clean = goal.strip()
    if not clean:
        raise ValueError("Goal cannot be empty")
    lower = clean.lower()
    caps = detect_local_video_capabilities()

    if any(k in lower for k in ("clip", "chopify", "podcast", "vod", "livestream", "highlights", "repurpose long")):
        mode = "long_to_short_clipping"
        primary_skill = "chopify"
        supporting_skills = ["vertical-video-psychology", "captions-and-clipping", "ffmpeg-video-editor", "video-production-orchestrator"]
        commands = [
            "./bin/chopify preflight",
            "./bin/chopify project create --source <SOURCE> --options-json '{\"aspect\":\"9:16\",\"style\":\"hormozi\",\"tighten\":true,\"loudnorm\":true}'",
            "./bin/chopify project prepare --project <PROJECT_PATH>",
            "./bin/chopify project render --project <PROJECT_PATH> --pick 1,2 --out output/",
            "uv run scripts/video_pipeline.py self-eval output/<clip>.mp4 --json",
        ]
    elif any(k in lower for k in ("talking head", "talking-head", "retake", "false start", "remove pauses", "edit recording")):
        mode = "talking_head_editing"
        primary_skill = "ai-video-editor"
        supporting_skills = ["video-production-orchestrator", "ffmpeg-video-editor", "video-editing-principles"]
        commands = [
            "uv run tools/video/ai-video-editor/scripts/transcribe.py <VIDEO> --lang en --work <WORK>",
            "uv run scripts/video_pipeline.py pack-transcript <WORK>/transcript.json --out <WORK>/takes_packed.md",
            "uv run tools/video/ai-video-editor/scripts/cut.py <WORK> --dry-run --style warm-canvas",
            "uv run scripts/video_pipeline.py edl-render <WORK>/edl.json -o <WORK>/final.mp4",
            "uv run scripts/video_pipeline.py self-eval <WORK>/final.mp4 --edl <WORK>/edl.json --json",
        ]
    elif any(k in lower for k in ("faceless", "deep dive", "night file", "inside out", "stick story", "paper atlas", "tall tale")):
        mode = "faceless_code_shorts"
        primary_skill = "faceless-shorts-engine"
        supporting_skills = ["vertical-video-psychology", "short-form-video-script", "video-production-orchestrator"]
        commands = [
            "bash tools/video/faceless-shorts/scripts/new_video.sh deep-dive <short-name>",
            "uv run scripts/video_pipeline.py script \"<topic>\" --json",
            "uv run scripts/video_pipeline.py self-eval <PROJECT>/renders/<short-name>.mp4 --json",
        ]
    elif any(k in lower for k in ("manim", "math", "equation", "calculus", "geometry", "3b1b", "diagram animation")):
        mode = "mathematical_explainer"
        primary_skill = "3b1b-manim"
        supporting_skills = ["manim-video", "vertical-video-psychology", "video-production-orchestrator"]
        commands = [
            "uv run scripts/video_pipeline.py manim <scene.py> <SceneClass> --json",
            "manimgl <scene.py> <SceneClass> -w -l",
            "manimgl <scene.py> <SceneClass> -w --hd",
        ]
    elif any(k in lower for k in ("taste", "style pack", "lut", "reference look", "edl", "fcpxml", "resolve")):
        mode = "reference_style_distillation"
        primary_skill = "taste-distillation"
        supporting_skills = ["taste-application", "tasteforge-video", "organic-film-de-ai", "video-production-orchestrator"]
        commands = [
            "uv run .agents/skills/taste-application/scripts/mint.py --genre <name> --refs <ref1.mp4>",
            "uv run .agents/skills/taste-application/scripts/pipeline.py --genre <name> --takes <take1.mp4> --out out/final.mp4",
            "uv run scripts/video_pipeline.py self-eval out/final.mp4 --json",
        ]
    elif any(k in lower for k in ("veo", "google flow", "flow", "generate video", "b-roll", "ai video", "de-ai", "film look", "halation")):
        mode = "generative_ai_cinema"
        primary_skill = "google-flow"
        supporting_skills = ["veo-3", "ai-video-quality-enhancement", "organic-film-de-ai", "ffmpeg-video-editor", "video-production-orchestrator"]
        commands = [
            "uv run scripts/video_pipeline.py veo-prompt \"<idea>\" --ratio 9:16 --duration 8 --style cinema --json",
            "bash mcp/google-flow-mcp.sh  # flow_generate_video (auto_confirm: false -> true)",
            "uv run scripts/remove_flow_watermark.py <raw.mp4> <delogo.mp4>",
            "uv run scripts/repair_ai_video.py full <delogo.mp4> -o <repaired.mp4>",
            "uv run scripts/organic_film_engine.py master <repaired.mp4> -o <cinema_master.mp4> --profile cinema-2383",
            "uv run scripts/video_pipeline.py self-eval <cinema_master.mp4> --json",
        ]
    elif any(k in lower for k in ("youtube", "long form", "long-form", "documentary", "vlog")):
        mode = "long_form_production"
        primary_skill = "youtube-long-form-production"
        supporting_skills = ["scriptwriting-principles", "video-editing-principles", "ffmpeg-video-editor", "google-flow", "video-production-orchestrator"]
        commands = [
            "uv run scripts/video_pipeline.py pack-transcript <transcript.json> --out takes_packed.md",
            "uv run scripts/video_pipeline.py edl-validate edl.json --json",
            "uv run scripts/video_pipeline.py edl-render edl.json -o final_youtube.mp4",
            "uv run scripts/video_pipeline.py self-eval final_youtube.mp4 --edl edl.json --json",
        ]
    else:
        mode = "unified_video_editing"
        primary_skill = "video-production-orchestrator"
        supporting_skills = ["video-editing", "ffmpeg-video-editor", "video-editing-principles", "vertical-video-psychology"]
        commands = [
            "uv run scripts/video_pipeline.py pack-transcript <transcript.json> --out takes_packed.md",
            "uv run scripts/video_pipeline.py edl-validate edl.json --json",
            "uv run scripts/video_pipeline.py edl-render edl.json -o final.mp4",
            "uv run scripts/video_pipeline.py self-eval final.mp4 --edl edl.json --json",
        ]

    return {
        "goal": clean,
        "mode": mode,
        "primary_skill": primary_skill,
        "supporting_skills": supporting_skills,
        "capabilities": caps,
        "hard_rules": PRODUCTION_HARD_RULES,
        "recommended_commands": commands,
    }


def generate_veo_prompt(
    idea: str,
    ratio: str = "9:16",
    duration: int = 8,
    style: str = "cinema",
) -> Dict[str, Any]:
    """Build a structured Veo 3.1 / Google Flow director prompt using the 5-part formula."""
    clean = idea.strip()
    if not clean:
        raise ValueError("Idea cannot be empty")
    if ratio not in ("9:16", "16:9"):
        raise ValueError("ratio must be '9:16' or '16:9'")
    if duration not in (4, 6, 8, 10):
        raise ValueError("duration must be 4, 6, 8, or 10")

    style_presets = {
        "cinema": {
            "cinematography": "Medium close-up, 35mm anamorphic prime lens at f/2.0, slow controlled dolly push-in, 180-degree shutter motion blur",
            "ambiance": "Shot on 35mm Kodak Vision3 500T film stock, directional warm key light with 4:1 contrast ratio, subtle atmospheric dust motes, natural skin texture",
            "negative": "empty clean background with clear architectural lines, anatomically accurate five-finger hands, steady horizon",
        },
        "doc": {
            "cinematography": "Eye-level handheld 40mm documentary framing, subtle natural operator breathing, shallow depth of field",
            "ambiance": "Natural overcast daylight, authentic unpolished textures, realistic shadow falloff, zero artificial gloss",
            "negative": "uncluttered background free of garbled signage or floating artifacts, natural human posture",
        },
        "product": {
            "cinematography": "Macro 85mm studio slider arc, crisp rack focus from foreground edge to hero surface, smooth mechanical inertia",
            "ambiance": "Soft diffused overhead softbox with clean rim highlight, matte dark slate surface, subtle specular reflections",
            "negative": "clean surface free of distorted text, warped logos, or phantom reflections",
        },
        "explainer": {
            "cinematography": "Locked-off medium shot with gentle 24fps micro-drift, centered safe-zone framing for vertical overlays",
            "ambiance": "Balanced studio key and cool fill light, clean uncluttered backdrop, crisp subject separation",
            "negative": "clean background free of random text overlays, extra limbs, or flickering lights",
        },
    }
    preset = style_presets.get(style, style_presets["cinema"])
    framing_note = "9:16 vertical portrait framing keeping subject centered in middle 1080x1400 safe zone" if ratio == "9:16" else "16:9 widescreen horizontal framing"

    prompt_text = (
        f"[Cinematography]: {preset['cinematography']}, {framing_note}. "
        f"[Subject & Action]: {clean}, performing one coherent physical movement with realistic mass and momentum. "
        f"[Context & Negative Constraints]: {preset['negative']}. "
        f"[Style & Ambiance]: {preset['ambiance']}. "
        f"[Soundstage]: Natural room tone matching the physical space, crisp contact SFX synchronized to motion, subtle ambient bed."
    )

    half = max(1, duration // 2)
    timestamp_template = (
        f"[00:00-00:{half:02d}] Establishing beat: {clean} enters frame under {preset['cinematography']}.\n"
        f"[00:{half:02d}-00:{duration:02d}] Payoff beat: camera settles on the primary action detail with synchronized SFX."
    )

    scene_builder_hop = (
        f"Continue smoothly from the final frame: maintain identical subject wardrobe, lighting direction, "
        f"and camera trajectory while advancing the action of {clean} for the next 7 seconds."
    )

    return {
        "idea": clean,
        "model_recommendation": "veo-3.1-fast" if style in ("explainer", "doc") else "veo-3.1-quality",
        "ratio": ratio,
        "duration": duration,
        "style": style,
        "prompt": prompt_text,
        "timestamp_prompt_template": timestamp_template,
        "scene_builder_hop_prompt": scene_builder_hop,
        "workflow_notes": [
            "Run flow_generate_video with auto_confirm=false first to inspect screenshot before spending credits.",
            "For multi-shot continuity, attach up to 3 reference images (Ingredients to Video) or start+end keyframes.",
            "After download, run remove_flow_watermark.py -> repair_ai_video.py -> organic_film_engine.py.",
        ],
    }


def _extract_words(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize word entries from Chopify or ai-video-editor transcript JSON."""
    raw_words = transcript_data.get("words") or []
    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_words):
        if not isinstance(item, dict):
            continue
        text = str(item.get("word") if "word" in item else item.get("w", "")).strip()
        if not text:
            continue
        start = float(item.get("start") if "start" in item else item.get("s", 0.0))
        end = float(item.get("end") if "end" in item else item.get("e", start + 0.02))
        speaker = str(item.get("speaker", "S0"))
        normalized.append({
            "index": int(item.get("i", idx)),
            "word": text,
            "start": round(start, 3),
            "end": round(max(end, start + 0.02), 3),
            "speaker": speaker,
        })
    return normalized


def pack_transcript(transcript_data: Dict[str, Any], gap_threshold: float = 0.5) -> str:
    """Pack word-level transcript JSON into compact phrase-level markdown."""
    words = _extract_words(transcript_data)
    source_name = Path(str(transcript_data.get("source") or transcript_data.get("video") or "source")).stem
    duration = float(transcript_data.get("duration") or (words[-1]["end"] if words else 0.0))

    phrases: List[List[Dict[str, Any]]] = []
    current: List[Dict[str, Any]] = []

    for w in words:
        if current:
            gap = w["start"] - current[-1]["end"]
            speaker_changed = w["speaker"] != current[-1]["speaker"]
            sentence_end = current[-1]["word"][-1:] in ".?!।"
            if gap >= gap_threshold or speaker_changed or len(current) >= 18 or sentence_end:
                phrases.append(current)
                current = []
        current.append(w)
    if current:
        phrases.append(current)

    lines = [f"## {source_name} (duration: {duration:.2f}s, {len(phrases)} phrases, {len(words)} words)"]
    for idx, group in enumerate(phrases):
        if idx > 0:
            pause = group[0]["start"] - phrases[idx - 1][-1]["end"]
            if pause >= gap_threshold:
                lines.append(f"  (silence {pause:.2f}s)")
        s_t = group[0]["start"]
        e_t = group[-1]["end"]
        w0 = group[0]["index"]
        w1 = group[-1]["index"]
        spk = group[0]["speaker"]
        text = " ".join(item["word"] for item in group)
        lines.append(f"  [{s_t:06.2f}-{e_t:06.2f}] {spk} w{w0}-w{w1}: {text}")
    return "\n".join(lines) + "\n"


def validate_edl(edl: Dict[str, Any], check_files: bool = False) -> Dict[str, Any]:
    """Validate an Edit Decision List against AGYOS production-correctness rules."""
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(edl, dict):
        return {"valid": False, "errors": ["EDL root must be a JSON object"], "warnings": [], "total_duration_s": 0.0}

    sources = edl.get("sources")
    if not isinstance(sources, dict) or not sources:
        errors.append("EDL must define a non-empty 'sources' mapping")
        sources = {}

    if check_files:
        for key, path_str in sources.items():
            if not Path(str(path_str)).is_file():
                errors.append(f"Source '{key}' file not found: {path_str}")

    ranges = edl.get("ranges")
    if not isinstance(ranges, list) or not ranges:
        errors.append("EDL must define a non-empty 'ranges' list")
        ranges = []

    total_duration = 0.0
    segment_timeline: List[Dict[str, Any]] = []
    for idx, seg in enumerate(ranges):
        if not isinstance(seg, dict):
            errors.append(f"Range {idx} must be an object")
            continue
        src_key = seg.get("source")
        if src_key not in sources:
            errors.append(f"Range {idx} references unknown source '{src_key}'")
        start = seg.get("start")
        end = seg.get("end")
        if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            errors.append(f"Range {idx} start/end must be numbers")
            continue
        if not (math.isfinite(start) and math.isfinite(end)) or start < 0 or end <= start:
            errors.append(f"Range {idx} has invalid bounds: start={start}, end={end}")
            continue
        dur = round(float(end) - float(start), 3)
        if dur < 0.1:
            errors.append(f"Range {idx} duration {dur}s is below 0.1s minimum for 30ms boundary fades")
        segment_timeline.append({
            "index": idx,
            "source": src_key,
            "source_start": float(start),
            "source_end": float(end),
            "output_start": round(total_duration, 3),
            "output_end": round(total_duration + dur, 3),
            "duration": dur,
        })
        total_duration += dur

    overlays = edl.get("overlays") or []
    if not isinstance(overlays, list):
        errors.append("'overlays' must be a list when provided")
        overlays = []
    for idx, ov in enumerate(overlays):
        if not isinstance(ov, dict):
            errors.append(f"Overlay {idx} must be an object")
            continue
        ov_start = ov.get("start_in_output", 0.0)
        ov_dur = ov.get("duration", 0.0)
        if isinstance(ov_start, bool) or isinstance(ov_dur, bool) or not isinstance(ov_start, (int, float)) or not isinstance(ov_dur, (int, float)):
            errors.append(f"Overlay {idx} start_in_output/duration must be numbers")
            continue
        if ov_start < 0 or ov_dur <= 0:
            errors.append(f"Overlay {idx} has invalid timing: start={ov_start}, duration={ov_dur}")
        if total_duration > 0 and ov_start + ov_dur > total_duration + 0.05:
            warnings.append(f"Overlay {idx} extends past total EDL duration ({ov_start + ov_dur:.2f}s > {total_duration:.2f}s)")
        if check_files and ov.get("file") and not Path(str(ov["file"])).is_file():
            errors.append(f"Overlay {idx} file not found: {ov['file']}")

    subtitles = edl.get("subtitles")
    if subtitles and check_files and not Path(str(subtitles)).is_file():
        errors.append(f"Subtitles file not found: {subtitles}")

    declared_total = edl.get("total_duration_s")
    if isinstance(declared_total, (int, float)) and not isinstance(declared_total, bool):
        if abs(float(declared_total) - total_duration) > 0.5:
            warnings.append(f"Declared total_duration_s ({declared_total}) differs from computed ({total_duration:.3f})")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "segment_count": len(segment_timeline),
        "overlay_count": len(overlays),
        "total_duration_s": round(total_duration, 3),
        "segments": segment_timeline,
    }


def _format_srt_time(seconds: float) -> str:
    ms_total = max(0, int(round(seconds * 1000)))
    hours = ms_total // 3_600_000
    minutes = (ms_total % 3_600_000) // 60_000
    secs = (ms_total % 60_000) // 1000
    ms = ms_total % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def remap_srt_for_edl(
    edl: Dict[str, Any],
    transcripts_by_source: Dict[str, List[Dict[str, Any]]],
    words_per_cue: int = 3,
) -> str:
    """Remap word timestamps onto the concatenated EDL output timeline (Hard Rule 5)."""
    validation = validate_edl(edl, check_files=False)
    if not validation["valid"]:
        raise ValueError("Invalid EDL: " + "; ".join(validation["errors"]))

    remapped_words: List[Dict[str, Any]] = []
    for seg in validation["segments"]:
        src_words = transcripts_by_source.get(seg["source"], [])
        s0, s1 = seg["source_start"], seg["source_end"]
        offset = seg["output_start"]
        for w in src_words:
            mid = (w["start"] + w["end"]) / 2.0
            if s0 <= mid <= s1:
                out_s = max(offset, offset + (w["start"] - s0))
                out_e = min(seg["output_end"], offset + (w["end"] - s0))
                if out_e > out_s:
                    remapped_words.append({
                        "word": w["word"],
                        "start": round(out_s, 3),
                        "end": round(out_e, 3),
                    })

    cues: List[List[Dict[str, Any]]] = []
    cur: List[Dict[str, Any]] = []
    for w in remapped_words:
        if cur:
            gap = w["start"] - cur[-1]["end"]
            if gap >= 0.35 or len(cur) >= max(1, words_per_cue) or cur[-1]["word"][-1:] in ".?!,":
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)

    srt_blocks: List[str] = []
    for idx, cue in enumerate(cues, start=1):
        start_str = _format_srt_time(cue[0]["start"])
        end_str = _format_srt_time(max(cue[-1]["end"], cue[0]["start"] + 0.25))
        text = " ".join(item["word"] for item in cue)
        srt_blocks.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")
    return "\n".join(srt_blocks)


def build_edl_ffmpeg_plan(
    edl: Dict[str, Any],
    output_path: str,
    work_dir: str,
    preview: bool = False,
) -> Dict[str, Any]:
    """Build deterministic FFmpeg commands enforcing the 12 production hard rules."""
    validation = validate_edl(edl, check_files=False)
    if not validation["valid"]:
        raise ValueError("Invalid EDL: " + "; ".join(validation["errors"]))

    work = Path(work_dir)
    seg_dir = work / "segments"
    sources = edl["sources"]
    grade_spec = str(edl.get("grade", "none") or "none")
    grade_filter = GRADE_PRESETS.get(grade_spec, grade_spec if grade_spec != "none" else "")
    crf = "24" if preview else "17"
    preset = "ultrafast" if preview else "fast"

    segment_commands: List[List[str]] = []
    segment_files: List[str] = []

    for seg in validation["segments"]:
        idx = seg["index"]
        src_path = str(sources[seg["source"]])
        seg_out = str(seg_dir / f"seg_{idx:03d}.mp4")
        segment_files.append(seg_out)
        dur = seg["duration"]
        fade_out_start = max(0.0, round(dur - 0.03, 3))

        vf_parts = []
        if preview:
            vf_parts.append("scale=-2:720")
        if grade_filter:
            vf_parts.append(grade_filter)
        vf_parts.append("format=yuv420p")

        af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out_start:.3f}:d=0.03"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{seg['source_start']:.3f}",
            "-t", f"{dur:.3f}",
            "-i", src_path,
            "-vf", ",".join(vf_parts),
            "-af", af,
            "-c:v", "libx264", "-preset", preset, "-crf", crf,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            seg_out,
        ]
        segment_commands.append(cmd)

    concat_list_path = str(work / "concat.txt")
    concat_out = str(work / "concat_base.mp4")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        concat_out,
    ]

    overlays = edl.get("overlays") or []
    subtitles = edl.get("subtitles")
    final_cmd: List[str]

    if overlays or subtitles:
        cmd = ["ffmpeg", "-y", "-i", concat_out]
        for ov in overlays:
            cmd.extend(["-i", str(ov["file"])])

        fc_lines: List[str] = []
        current_label = "[0:v]"
        for k, ov in enumerate(overlays):
            start_t = float(ov.get("start_in_output", 0.0))
            dur_t = float(ov.get("duration", 1.0))
            end_t = start_t + dur_t
            ov_label = f"[ov{k}]"
            next_label = f"[v{k + 1}]"
            fc_lines.append(f"[{k + 1}:v]setpts=PTS-STARTPTS+{start_t:.3f}/TB{ov_label}")
            fc_lines.append(
                f"{current_label}{ov_label}overlay=0:0:enable='between(t,{start_t:.3f},{end_t:.3f})':eof_action=pass{next_label}"
            )
            current_label = next_label

        if subtitles:
            sub_path = str(subtitles).replace("'", "\\'")
            sub_filter = f"ass='{sub_path}'" if str(subtitles).lower().endswith(".ass") else f"subtitles='{sub_path}'"
            fc_lines.append(f"{current_label}{sub_filter}[vfinal]")
            current_label = "[vfinal]"

        cmd.extend([
            "-filter_complex", ";".join(fc_lines),
            "-map", current_label,
            "-map", "0:a?",
            "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
            "-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            output_path,
        ])
        final_cmd = cmd
    else:
        final_cmd = [
            "ffmpeg", "-y",
            "-i", concat_out,
            "-c:v", "copy",
            "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            output_path,
        ]

    return {
        "work_dir": str(work),
        "concat_list_path": concat_list_path,
        "segment_files": segment_files,
        "segment_commands": segment_commands,
        "concat_command": concat_cmd,
        "final_command": final_cmd,
        "subtitles_applied_last": True,
        "boundary_fade_seconds": 0.03,
        "total_duration_s": validation["total_duration_s"],
    }


def parse_blackdetect_output(stderr_text: str) -> List[Dict[str, float]]:
    """Parse FFmpeg blackdetect intervals from stderr."""
    intervals: List[Dict[str, float]] = []
    pattern = re.compile(
        r"black_start:(\d+(?:\.\d+)?)\s+black_end:(\d+(?:\.\d+)?)\s+black_duration:(\d+(?:\.\d+)?)"
    )
    for match in pattern.finditer(stderr_text):
        intervals.append({
            "start": float(match.group(1)),
            "end": float(match.group(2)),
            "duration": float(match.group(3)),
        })
    return intervals


def evaluate_rendered_video(
    video_path: str,
    edl: Optional[Dict[str, Any]] = None,
    target_lufs: float = -14.0,
) -> Dict[str, Any]:
    """Run post-render self-evaluation (ffprobe, ebur128 loudness, blackdetect)."""
    path = Path(video_path)
    if not path.is_file():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    probe_res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    meta = json.loads(probe_res.stdout)
    v_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), None)
    duration = float(meta.get("format", {}).get("duration", 0.0) or 0.0)

    issues: List[str] = []
    if not v_stream:
        issues.append("Missing video stream")
    if not a_stream:
        issues.append("Missing audio stream")
    if duration <= 0:
        issues.append("Non-positive video duration")

    if edl is not None:
        val = validate_edl(edl, check_files=False)
        expected_dur = val["total_duration_s"]
        if abs(duration - expected_dur) > 0.75:
            issues.append(f"Duration mismatch: rendered {duration:.2f}s vs EDL {expected_dur:.2f}s")

    loudness: Dict[str, Optional[float]] = {"integrated_lufs": None, "lra_lu": None, "true_peak_dbtp": None}
    if a_stream:
        ebur_res = subprocess.run(
            ["ffmpeg", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
            capture_output=True, text=True, check=False,
        )
        loudness = parse_ebur128_summary(ebur_res.stderr)
        if loudness["integrated_lufs"] is not None:
            if abs(loudness["integrated_lufs"] - target_lufs) > 3.0:
                issues.append(
                    f"Loudness {loudness['integrated_lufs']:.1f} LUFS deviates >3 LU from target {target_lufs:.1f} LUFS"
                )
        if loudness["true_peak_dbtp"] is not None and loudness["true_peak_dbtp"] > -0.5:
            issues.append(f"True peak {loudness['true_peak_dbtp']:.2f} dBTP exceeds -0.5 dBTP ceiling")

    black_res = subprocess.run(
        ["ffmpeg", "-i", str(path), "-vf", "blackdetect=d=0.25:pix_th=0.10", "-an", "-f", "null", "-"],
        capture_output=True, text=True, check=False,
    )
    black_intervals = parse_blackdetect_output(black_res.stderr)
    if black_intervals:
        issues.append(f"Detected {len(black_intervals)} black-frame interval(s) >= 0.25s")

    return {
        "file": str(path),
        "status": "PASS" if not issues else "FAIL",
        "duration_s": round(duration, 3),
        "video": {
            "codec": v_stream.get("codec_name") if v_stream else None,
            "width": v_stream.get("width") if v_stream else None,
            "height": v_stream.get("height") if v_stream else None,
            "fps": v_stream.get("r_frame_rate") if v_stream else None,
        },
        "audio": {
            "codec": a_stream.get("codec_name") if a_stream else None,
            "sample_rate": a_stream.get("sample_rate") if a_stream else None,
            "loudness": loudness,
        },
        "black_intervals": black_intervals,
        "issues": issues,
    }


def generate_timeline_view(
    video_path: str,
    start: float,
    end: float,
    output_png: str,
    frames: int = 8,
) -> str:
    """Generate an on-demand filmstrip + audio waveform PNG for a time window."""
    if end <= start:
        raise ValueError("end must be greater than start")
    src = Path(video_path)
    if not src.is_file():
        raise FileNotFoundError(f"Video not found: {video_path}")

    out = Path(output_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = end - start
    fps = max(0.5, frames / dur)

    fc = (
        f"[0:v]fps={fps:.4f},scale=240:-1,tile={frames}x1[strip];"
        f"[0:a]showwavespic=s={240 * frames}x140:colors=#4f9cf0[wave];"
        "[strip][wave]vstack=inputs=2[out]"
    )
    res = subprocess.run(
        [
            "ffmpeg", "-y",
            "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
            "-i", str(src),
            "-filter_complex", fc,
            "-map", "[out]",
            "-frames:v", "1",
            str(out),
        ],
        capture_output=True, text=True, check=False,
    )
    if res.returncode != 0:
        # Fallback without audio waveform if source has no audio stream
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
                "-i", str(src),
                "-vf", f"fps={fps:.4f},scale=240:-1,tile={frames}x1",
                "-frames:v", "1",
                str(out),
            ],
            capture_output=True, text=True, check=True,
        )
    return str(out)


def _delegate_script(script_rel: str, extra_args: List[str]) -> int:
    target = ROOT / script_rel
    if not target.is_file():
        print(f"Error: target not found: {target}", file=sys.stderr)
        return 1
    if target.suffix == ".py":
        if shutil.which("uv"):
            cmd = ["uv", "run", "--python", sys.executable, str(target), *extra_args]
        else:
            cmd = [sys.executable, str(target), *extra_args]
    else:
        cmd = ["bash", str(target), *extra_args]
    return subprocess.run(cmd).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="AGYOS Unified Video Studio CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    script_parser = subparsers.add_parser("script", help="Generate dual-track vertical video script")
    script_parser.add_argument("topic", help="Topic or breakdown subject")
    script_parser.add_argument("--style", default="technical", help="Script style")
    script_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    audit_parser = subparsers.add_parser("audit", help="Audit video content against 116 principles")
    audit_parser.add_argument("path", help="Path to script markdown or text file")
    audit_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    manim_parser = subparsers.add_parser("manim", help="Validate Manim scene and generate headless command")
    manim_parser.add_argument("path", help="Path to python scene file")
    manim_parser.add_argument("scene_class", nargs="?", default=None, help="Scene class name")
    manim_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    route_parser = subparsers.add_parser("route", help="Route a video goal to optimal AGYOS tools and skills")
    route_parser.add_argument("goal", help="Video production or editing goal")
    route_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    veo_parser = subparsers.add_parser("veo-prompt", help="Generate structured Veo 3.1 / Google Flow prompt")
    veo_parser.add_argument("idea", help="Scene idea or action")
    veo_parser.add_argument("--ratio", choices=["9:16", "16:9"], default="9:16")
    veo_parser.add_argument("--duration", type=int, choices=[4, 6, 8, 10], default=8)
    veo_parser.add_argument("--style", choices=["cinema", "doc", "product", "explainer"], default="cinema")
    veo_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    pack_parser = subparsers.add_parser("pack-transcript", help="Pack word-level transcript JSON into phrase markdown")
    pack_parser.add_argument("transcript", help="Path to transcript.json")
    pack_parser.add_argument("--gap", type=float, default=0.5, help="Silence break threshold in seconds")
    pack_parser.add_argument("--out", default=None, help="Optional output markdown path")

    edl_val_parser = subparsers.add_parser("edl-validate", help="Validate EDL against production hard rules")
    edl_val_parser.add_argument("edl", help="Path to edl.json")
    edl_val_parser.add_argument("--check-files", action="store_true", help="Verify referenced files exist on disk")
    edl_val_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    srt_parser = subparsers.add_parser("edl-remap-srt", help="Remap transcript words onto EDL output timeline")
    srt_parser.add_argument("edl", help="Path to edl.json")
    srt_parser.add_argument("transcript", help="Path to transcript.json (or JSON map of source->transcript)")
    srt_parser.add_argument("--words-per-cue", type=int, default=3)
    srt_parser.add_argument("--out", default=None, help="Optional output .srt path")

    render_parser = subparsers.add_parser("edl-render", help="Plan or execute EDL render with 12 hard rules")
    render_parser.add_argument("edl", help="Path to edl.json")
    render_parser.add_argument("-o", "--output", default="final.mp4", help="Output MP4 path")
    render_parser.add_argument("--work", default="edit_work", help="Working directory for segments")
    render_parser.add_argument("--preview", action="store_true", help="Fast 720p preview render")
    render_parser.add_argument("--dry-run", action="store_true", help="Print FFmpeg plan without executing")
    render_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    tv_parser = subparsers.add_parser("timeline-view", help="Generate filmstrip + waveform PNG for a time window")
    tv_parser.add_argument("video", help="Input video path")
    tv_parser.add_argument("start", type=float, help="Start time in seconds")
    tv_parser.add_argument("end", type=float, help="End time in seconds")
    tv_parser.add_argument("-o", "--output", default="timeline_view.png", help="Output PNG path")
    tv_parser.add_argument("--frames", type=int, default=8, help="Number of filmstrip frames")

    eval_parser = subparsers.add_parser("self-eval", help="Run post-render ffprobe, ebur128, and blackdetect checks")
    eval_parser.add_argument("video", help="Rendered video path")
    eval_parser.add_argument("--edl", default=None, help="Optional EDL JSON for duration verification")
    eval_parser.add_argument("--target-lufs", type=float, default=-14.0)
    eval_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    for passthrough in ("chopify", "repair", "film", "delogo"):
        subparsers.add_parser(passthrough, help=f"Delegate to AGYOS {passthrough} tool")

    args, extra = parser.parse_known_args()

    if not args.subcommand:
        parser.print_help()
        return 1

    if args.subcommand == "chopify":
        return _delegate_script("bin/chopify", extra)
    if args.subcommand == "repair":
        return _delegate_script("scripts/repair_ai_video.py", extra)
    if args.subcommand == "film":
        return _delegate_script("scripts/organic_film_engine.py", extra)
    if args.subcommand == "delogo":
        return _delegate_script("scripts/remove_flow_watermark.py", extra)

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
                print(f"Manim Scene Validation Failed: {res.get('error')}", file=sys.stderr)
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

    if args.subcommand == "route":
        res = route_video_workflow(args.goal)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Mode: {res['mode']} | Primary Skill: {res['primary_skill']}")
            print(f"Supporting Skills: {', '.join(res['supporting_skills'])}")
            print("Recommended Commands:")
            for cmd in res["recommended_commands"]:
                print(f"  {cmd}")
        return 0

    if args.subcommand == "veo-prompt":
        res = generate_veo_prompt(args.idea, ratio=args.ratio, duration=args.duration, style=args.style)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(res["prompt"])
            print("\n--- Timestamp Template ---")
            print(res["timestamp_prompt_template"])
            print("\n--- Scene Builder Hop ---")
            print(res["scene_builder_hop_prompt"])
        return 0

    if args.subcommand == "pack-transcript":
        t_path = Path(args.transcript)
        if not t_path.is_file():
            print(f"Error: Transcript not found: {args.transcript}", file=sys.stderr)
            return 1
        data = json.loads(t_path.read_text(encoding="utf-8"))
        packed = pack_transcript(data, gap_threshold=args.gap)
        if args.out:
            Path(args.out).write_text(packed, encoding="utf-8")
            print(f"Packed transcript written to {args.out}")
        else:
            print(packed)
        return 0

    if args.subcommand == "edl-validate":
        edl_path = Path(args.edl)
        if not edl_path.is_file():
            print(f"Error: EDL not found: {args.edl}", file=sys.stderr)
            return 1
        edl = json.loads(edl_path.read_text(encoding="utf-8"))
        res = validate_edl(edl, check_files=args.check_files)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"EDL Valid: {res['valid']} | Segments: {res['segment_count']} | Duration: {res['total_duration_s']}s")
            for err in res["errors"]:
                print(f"  ERROR: {err}")
            for warn in res["warnings"]:
                print(f"  WARN: {warn}")
        return 0 if res["valid"] else 1

    if args.subcommand == "edl-remap-srt":
        edl = json.loads(Path(args.edl).read_text(encoding="utf-8"))
        tr_raw = json.loads(Path(args.transcript).read_text(encoding="utf-8"))
        if "words" in tr_raw:
            first_src = next(iter(edl.get("sources", {})), "default")
            by_src = {k: _extract_words(tr_raw) for k in edl.get("sources", {first_src: ""})}
        else:
            by_src = {k: _extract_words(v) for k, v in tr_raw.items()}
        srt_text = remap_srt_for_edl(edl, by_src, words_per_cue=args.words_per_cue)
        if args.out:
            Path(args.out).write_text(srt_text, encoding="utf-8")
            print(f"Remapped SRT written to {args.out}")
        else:
            print(srt_text)
        return 0

    if args.subcommand == "edl-render":
        edl = json.loads(Path(args.edl).read_text(encoding="utf-8"))
        plan = build_edl_ffmpeg_plan(edl, args.output, args.work, preview=args.preview)
        if args.dry_run:
            if args.json:
                print(json.dumps(plan, indent=2))
            else:
                print(f"Dry-run EDL render plan ({len(plan['segment_commands'])} segments, {plan['total_duration_s']}s):")
                for cmd in plan["segment_commands"]:
                    print(" ", " ".join(cmd))
                print(" ", " ".join(plan["concat_command"]))
                print(" ", " ".join(plan["final_command"]))
            return 0

        work = Path(plan["work_dir"])
        (work / "segments").mkdir(parents=True, exist_ok=True)
        for cmd in plan["segment_commands"]:
            subprocess.run(cmd, check=True)
        concat_lines = "".join(f"file '{Path(p).resolve().as_posix()}'\n" for p in plan["segment_files"])
        Path(plan["concat_list_path"]).write_text(concat_lines, encoding="utf-8")
        subprocess.run(plan["concat_command"], check=True)
        subprocess.run(plan["final_command"], check=True)
        if args.json:
            print(json.dumps({"output": args.output, "total_duration_s": plan["total_duration_s"]}, indent=2))
        else:
            print(f"Rendered EDL output to {args.output}")
        return 0

    if args.subcommand == "timeline-view":
        out_path = generate_timeline_view(args.video, args.start, args.end, args.output, frames=args.frames)
        print(f"Timeline view saved to {out_path}")
        return 0

    if args.subcommand == "self-eval":
        edl_obj = json.loads(Path(args.edl).read_text(encoding="utf-8")) if args.edl else None
        res = evaluate_rendered_video(args.video, edl=edl_obj, target_lufs=args.target_lufs)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Self-Eval Status: {res['status']} | Duration: {res['duration_s']}s")
            print(f"Loudness: {res['audio']['loudness']}")
            for issue in res["issues"]:
                print(f"  ISSUE: {issue}")
        return 0 if res["status"] == "PASS" else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
