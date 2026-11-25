#!/usr/bin/env python3
"""
Automated watermark removal for Google Flow / Veo videos.
Detects the corner watermark box automatically (with deterministic resolution
fallbacks when PIL/numpy are unavailable) and applies FFmpeg delogo inpainting.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def get_video_info(video_path: Path) -> Tuple[int, int]:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "json", str(video_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    video_stream = next(s for s in data["streams"] if "width" in s)
    return int(video_stream["width"]), int(video_stream["height"])


def fallback_watermark_box(width: int, height: int) -> Tuple[int, int, int, int]:
    """Return deterministic bottom-right delogo coordinates for standard resolutions."""
    if width == 1280 and height == 720:
        return 1236, 688, 36, 22
    if width == 720 and height == 1280:
        return 676, 1248, 36, 22
    if width == 1920 and height == 1080:
        return 1854, 1032, 54, 33
    if width == 1080 and height == 1920:
        return 1014, 1872, 54, 33
    return (
        max(0, int(width * 0.965)),
        max(0, int(height * 0.955)),
        max(10, int(width * 0.03)),
        max(10, int(height * 0.03)),
    )


def detect_watermark_box(video_path: Path, width: int, height: int) -> Tuple[int, int, int, int]:
    """Detect bottom-right watermark bounding box, falling back cleanly if PIL/numpy absent."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return fallback_watermark_box(width, height)

    tmp_frame = Path(f"/tmp/flow_wm_detect_{video_path.stem}.png")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", str(video_path),
            "-vframes", "1", str(tmp_frame),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        img = Image.open(tmp_frame)
        search_w = int(width * 0.08)
        search_h = int(height * 0.08)
        crop = np.array(img)[height - search_h : height - 5, width - search_w : width - 5]

        luminance = np.mean(crop, axis=2)
        bg_median = np.median(luminance)
        y_indices, x_indices = np.where(luminance > (bg_median + 25))

        if len(x_indices) > 5:
            min_x = (width - search_w) + int(np.min(x_indices)) - 4
            max_x = (width - search_w) + int(np.max(x_indices)) + 4
            min_y = (height - search_h) + int(np.min(y_indices)) - 4
            max_y = (height - search_h) + int(np.max(y_indices)) + 4
            w = max_x - min_x
            h = max_y - min_y
            return max(0, min_x), max(0, min_y), max(10, w), max(10, h)
    finally:
        tmp_frame.unlink(missing_ok=True)

    return fallback_watermark_box(width, height)


def remove_watermark(input_path: str, output_path: Optional[str] = None, as_json: bool = False) -> str:
    input_file = Path(input_path).resolve()
    if not input_file.exists():
        print(f"Error: input file {input_file} not found.", file=sys.stderr)
        sys.exit(1)

    if not output_path:
        output_file = input_file.parent / f"{input_file.stem}_clean{input_file.suffix}"
    else:
        output_file = Path(output_path).resolve()

    width, height = get_video_info(input_file)
    x, y, w, h = detect_watermark_box(input_file, width, height)
    delogo_filter = f"delogo=x={x}:y={y}:w={w}:h={h}"

    cmd = [
        "ffmpeg", "-y", "-i", str(input_file),
        "-vf", delogo_filter,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(output_file),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    if as_json:
        print(json.dumps({
            "input": str(input_file),
            "output": str(output_file),
            "resolution": f"{width}x{height}",
            "delogo_box": {"x": x, "y": y, "w": w, "h": h},
            "filter": delogo_filter,
        }, indent=2))
    else:
        print(f"Detected watermark zone on {width}x{height} frame: x={x}, y={y}, w={w}, h={h}")
        print(f"Successfully created clean video: {output_file}")
    return str(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Google Flow / Veo watermark removal")
    parser.add_argument("input", help="Input MP4 path")
    parser.add_argument("output", nargs="?", default=None, help="Optional output MP4 path")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")
    args = parser.parse_args()
    remove_watermark(args.input, args.output, as_json=args.json)


if __name__ == "__main__":
    main()
