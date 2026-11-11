#!/usr/bin/env python3
"""
Scaffold and validate execution manifests for faceless shorts production.
Produces a standardized shorts_manifest.json with scenes, audio cues, and camera choreography.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

VALID_STYLES = {
    "tall_tale_3d": {
        "name": "Tall Tale 3D",
        "default_voice": "am_adam",
        "pacing_sec": 1.8,
        "camera": "wide_angle_macro_zooms",
    },
    "deep_dive_3d": {
        "name": "Deep Dive 3D",
        "default_voice": "af_bella",
        "pacing_sec": 2.0,
        "camera": "anatomical_orbit_push_in",
    },
    "inside_out": {
        "name": "Inside Out",
        "default_voice": "af_bella",
        "pacing_sec": 2.0,
        "camera": "isometric_exploded_slices",
    },
    "stick_story": {
        "name": "Stick Story",
        "default_voice": "am_adam",
        "pacing_sec": 1.5,
        "camera": "jump_cut_split_screen",
    },
    "night_file_3d": {
        "name": "Night File 3D",
        "default_voice": "am_michael",
        "pacing_sec": 2.2,
        "camera": "slow_creeping_dolly_fog",
    },
    "paper_atlas": {
        "name": "Paper Atlas",
        "default_voice": "bm_george",
        "pacing_sec": 2.0,
        "camera": "top_down_map_tracking",
    },
}


def build_manifest(title: str, topic: str, style_key: str, duration_sec: int = 35) -> Dict[str, Any]:
    if style_key not in VALID_STYLES:
        raise ValueError(f"Unknown style '{style_key}'. Valid choices: {list(VALID_STYLES.keys())}")

    style_cfg = VALID_STYLES[style_key]
    estimated_words = int(duration_sec * 2.5)  # ~150 words per minute

    manifest: Dict[str, Any] = {
        "schema_version": "1.0",
        "project": {
            "title": title,
            "topic": topic,
            "target_duration_sec": duration_sec,
            "estimated_word_count": estimated_words,
            "aspect_ratio": "9:16",
            "resolution": {"width": 1080, "height": 1920},
            "fps": 30,
        },
        "style": {
            "key": style_key,
            "display_name": style_cfg["name"],
            "camera_profile": style_cfg["camera"],
            "visual_pacing_interval_sec": style_cfg["pacing_sec"],
        },
        "audio": {
            "tts_engine": "kokoro_onnx",
            "voice_profile": style_cfg["default_voice"],
            "target_sample_rate": 24000,
            "ducking_db": -18.0,
            "integrated_lufs": -14.0,
            "sfx_cue_sheet": [
                {"event": "hook_drop", "offset_sec": 0.5, "sfx": "sfx_pop.wav"},
                {"event": "first_shift", "offset_sec": style_cfg["pacing_sec"], "sfx": "sfx_whoosh.wav"},
            ],
        },
        "subtitles": {
            "engine": "whisper_word_level",
            "model": "base.en",
            "font_family": "Montserrat Black",
            "font_size_px": 84,
            "primary_color": "#FFFFFF",
            "highlight_color": "#FFE500",
            "outline_color": "#000000",
            "outline_width_px": 5,
            "vertical_alignment_percent": 68,
        },
        "photochemical_finishing": {
            "enabled": True,
            "lut": "kodak_2383",
            "halation": True,
            "grain_intensity": 0.15,
            "audio_loudness_target": -14.0,
        },
        "scenes": [
            {
                "scene_id": 1,
                "role": "hook_punchline",
                "start_sec": 0.0,
                "end_sec": 2.5,
                "camera": "extreme_close_up",
                "sfx": ["sfx_pop.wav"],
            },
            {
                "scene_id": 2,
                "role": "development_exposition",
                "start_sec": 2.5,
                "end_sec": 10.0,
                "camera": "tracking_orbit",
                "sfx": ["sfx_whoosh.wav"],
            },
        ],
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a faceless short manifest")
    parser.add_argument("--title", required=True, help="Title of the short")
    parser.add_argument("--topic", required=True, help="Core subject or story premise")
    parser.add_argument(
        "--style",
        choices=list(VALID_STYLES.keys()),
        default="tall_tale_3d",
        help="Animation style preset",
    )
    parser.add_argument("--duration", type=int, default=35, help="Target duration in seconds")
    parser.add_argument("--out", type=str, default="shorts_manifest.json", help="Output path")

    args = parser.parse_args()
    manifest = build_manifest(args.title, args.topic, args.style, args.duration)

    out_path = Path(args.out)
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Scaffolded faceless short manifest written to {out_path}")


if __name__ == "__main__":
    main()
