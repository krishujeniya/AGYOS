#!/usr/bin/env python3
"""Create a planning scaffold for a code-rendered faceless short.

The output is not a renderer configuration. Voice, scene timing, sound, and export
settings stay unset until they are selected and verified for the chosen toolkit.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VALID_STYLES = {
    "deep-dive": "Stylized 3D body and science explainers",
    "night-file": "Mystery and true-crime stories",
    "inside-out": "Flat 2D mechanisms and what-happens-if explainers",
    "stick-story": "Survival scenarios and decision steps",
    "paper-atlas": "Historical events, routes, and maps",
    "tall-tale": "Funny or surprising true stories",
}


def build_manifest(
    title: str,
    topic: str,
    style_key: str,
    duration_sec: int = 30,
) -> dict[str, Any]:
    """Build an unverified creative plan without guessing production settings."""
    clean_title = title.strip()
    clean_topic = topic.strip()
    if not clean_title:
        raise ValueError("title must not be empty")
    if not clean_topic:
        raise ValueError("topic must not be empty")
    if style_key not in VALID_STYLES:
        raise ValueError(f"unknown style {style_key!r}; choose one of {', '.join(VALID_STYLES)}")
    if duration_sec <= 0:
        raise ValueError("duration must be a positive number of seconds")

    return {
        "schema_version": "1.1",
        "status": "planning_only",
        "project": {
            "title": clean_title,
            "topic": clean_topic,
            "target_duration_sec": duration_sec,
            "aspect_ratio": "9:16",
        },
        "style": {
            "key": style_key,
            "description": VALID_STYLES[style_key],
        },
        "sources": [],
        "narration": {
            "mode": None,
            "voice_id": None,
        },
        "subtitles": {
            "timing_source": None,
        },
        "scenes": [],
        "render": {},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Title for the short")
    parser.add_argument("--topic", required=True, help="Subject or story premise")
    parser.add_argument("--style", choices=VALID_STYLES, required=True, help="Toolkit style ID")
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Draft target in seconds; final runtime depends on the rendered narration (default: 30)",
    )
    parser.add_argument("--out", type=Path, default=Path("shorts_manifest.json"))
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    args = parser.parse_args()

    if args.out.exists() and not args.force:
        parser.error(f"{args.out} already exists; choose another --out path or pass --force")
    try:
        manifest = build_manifest(args.title, args.topic, args.style, args.duration)
    except ValueError as exc:
        parser.error(str(exc))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Planning scaffold written to {args.out}; no media was rendered.")


if __name__ == "__main__":
    main()
