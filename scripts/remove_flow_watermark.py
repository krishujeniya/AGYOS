#!/usr/bin/env python3
"""
Automated watermark removal for Google Flow / Veo videos.
Detects the corner watermark box automatically and applies FFmpeg inpainting.
"""

import sys
import subprocess
import json
from pathlib import Path
from PIL import Image
import numpy as np

def get_video_info(video_path: Path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "json", str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    video_stream = next(s for s in data["streams"] if "width" in s)
    return int(video_stream["width"]), int(video_stream["height"])

def detect_watermark_box(video_path: Path, width: int, height: int):
    # Extract frame 1 to temporary image
    tmp_frame = Path("/tmp/flow_wm_detect.png")
    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:01", "-i", str(video_path),
        "-vframes", "1", str(tmp_frame)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    img = Image.open(tmp_frame)
    # Focus on the bottom-right corner (last 80px horizontal, 50px vertical)
    search_w = int(width * 0.08)
    search_h = int(height * 0.08)
    crop = np.array(img)[height - search_h : height - 5, width - search_w : width - 5]

    # Watermark text has distinct higher luminance compared to local dark background
    luminance = np.mean(crop, axis=2)
    bg_median = np.median(luminance)
    y_indices, x_indices = np.where(luminance > (bg_median + 25))

    tmp_frame.unlink(missing_ok=True)

    if len(x_indices) > 5:
        min_x = (width - search_w) + int(np.min(x_indices)) - 4
        max_x = (width - search_w) + int(np.max(x_indices)) + 4
        min_y = (height - search_h) + int(np.min(y_indices)) - 4
        max_y = (height - search_h) + int(np.max(y_indices)) + 4
        w = max_x - min_x
        h = max_y - min_y
        return max(0, min_x), max(0, min_y), max(10, w), max(10, h)

    # Standard fallback coordinates for 1280x720 and 720x1280
    if width == 1280 and height == 720:
        return 1236, 688, 36, 22
    elif width == 720 and height == 1280:
        return 676, 1248, 36, 22
    else:
        # Relative scaling fallback
        return int(width * 0.965), int(height * 0.955), int(width * 0.03), int(height * 0.03)

def remove_watermark(input_path: str, output_path: str = None):
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
    print(f"Detected watermark zone on {width}x{height} frame: x={x}, y={y}, w={w}, h={h}")

    delogo_filter = f"delogo=x={x}:y={y}:w={w}:h={h}"
    cmd = [
        "ffmpeg", "-y", "-i", str(input_file),
        "-vf", delogo_filter,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        str(output_file)
    ]
    print(f"Applying filter: {delogo_filter} -> {output_file.name}")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    print(f"Successfully created clean video: {output_file}")
    return str(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 remove_flow_watermark.py <input.mp4> [output.mp4]")
        sys.exit(1)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    remove_watermark(sys.argv[1], out)
