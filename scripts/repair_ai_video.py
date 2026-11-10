#!/usr/bin/env python3
"""
AI Video Repair & Enhancement Utility.
Provides CLI operations for stabilizing, deflickering, debanding,
and mastering audio for AI-generated video clips.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def calculate_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def probe_video(filepath: str) -> dict:
    """Extract stream and format metadata using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-of", "json",
        filepath,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def run_ffmpeg(args: list[str]) -> None:
    """Execute FFmpeg command with error handling."""
    cmd = ["ffmpeg", "-y"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"FFmpeg error: {res.stderr}\n")
        sys.exit(res.returncode)


def audit_clip(input_path: str) -> None:
    """Audit clip metadata and output custody verification details."""
    digest = calculate_sha256(input_path)
    meta = probe_video(input_path)
    v_stream = next((s for s in meta.get("streams", []) if s["codec_type"] == "video"), None)
    a_stream = next((s for s in meta.get("streams", []) if s["codec_type"] == "audio"), None)

    print(f"File: {input_path}")
    print(f"SHA-256: {digest}")
    if v_stream:
        w, h = v_stream.get("width"), v_stream.get("height")
        fps = v_stream.get("r_frame_rate", "unknown")
        codec = v_stream.get("codec_name", "unknown")
        print(f"Video: {codec} {w}x{h} @ {fps} fps")
    if a_stream:
        acodec = a_stream.get("codec_name", "unknown")
        sr = a_stream.get("sample_rate", "unknown")
        print(f"Audio: {acodec} {sr} Hz")


def apply_deflicker(input_path: str, output_path: str) -> None:
    """Apply moving-average luminance deflicker filter."""
    vf = "deflicker=size=5:mode=am"
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Deflickered video saved to {output_path}")


def apply_deband(input_path: str, output_path: str) -> None:
    """Apply gradient debanding filter."""
    vf = "deband=1thr=0.015:2thr=0.015:3thr=0.015"
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Debanded video saved to {output_path}")


def apply_stabilization(input_path: str, output_path: str) -> None:
    """Perform two-pass VidStab camera stabilization."""
    trf_file = f"/tmp/transforms_{os.getpid()}.trf"
    pass1_vf = f"vidstabdetect=stepsize=6:shakiness=5:accuracy=15:result={trf_file}"
    run_ffmpeg(["-i", input_path, "-vf", pass1_vf, "-f", "null", "-"])

    pass2_vf = f"vidstabtransform=smoothing=25:input={trf_file}:zoom=3:optzoom=1,unsharp=5:5:0.5"
    run_ffmpeg([
        "-i", input_path,
        "-vf", pass2_vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    if os.path.exists(trf_file):
        os.remove(trf_file)
    print(f"Stabilized video saved to {output_path}")


def apply_audio_mastering(input_path: str, output_path: str) -> None:
    """Clean background noise and normalize loudness to -14 LUFS."""
    af = "afftdn=nf=-25,loudnorm=I=-14:TP=-1.0:LRA=9"
    run_ffmpeg([
        "-i", input_path,
        "-c:v", "copy",
        "-af", af,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Mastered audio video saved to {output_path}")


def apply_full_repair(input_path: str, output_path: str) -> None:
    """Chain deflicker, deband, color grade, and audio normalization."""
    vf = "deflicker=size=5:mode=am,deband=1thr=0.015:2thr=0.015:3thr=0.015,eq=contrast=1.02:saturation=1.03"
    af = "afftdn=nf=-20,loudnorm=I=-14:TP=-1.0:LRA=9"
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-map_metadata", "-1",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Full repair completed and saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Video Quality Repair CLI")
    parser.add_argument("command", choices=["audit", "deflicker", "deband", "stabilize", "audio", "full"])
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("-o", "--output", default="output_repaired.mp4", help="Path to output video file")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.stderr.write(f"Error: input file {args.input} does not exist.\n")
        sys.exit(1)

    if args.command == "audit":
        audit_clip(args.input)
    elif args.command == "deflicker":
        apply_deflicker(args.input, args.output)
    elif args.command == "deband":
        apply_deband(args.input, args.output)
    elif args.command == "stabilize":
        apply_stabilization(args.input, args.output)
    elif args.command == "audio":
        apply_audio_mastering(args.input, args.output)
    elif args.command == "full":
        apply_full_repair(args.input, args.output)


if __name__ == "__main__":
    main()
