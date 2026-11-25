#!/usr/bin/env python3
"""
AI Video Repair & Enhancement Utility.
Provides CLI operations for auditing, stabilizing, deflickering, debanding,
measuring EBU R128 loudness, and two-pass mastering audio for AI-generated
and recorded video clips.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, Optional


def calculate_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def probe_video(filepath: str) -> Dict[str, Any]:
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


def run_ffmpeg(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Execute FFmpeg command with error handling."""
    cmd = ["ffmpeg", "-y"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"FFmpeg error: {res.stderr}\n")
        sys.exit(res.returncode)
    return res


def build_deflicker_filter(size: int = 5, mode: str = "am") -> str:
    """Build moving-average luminance deflicker filter."""
    return f"deflicker=size={size}:mode={mode}"


def build_deband_filter(threshold: float = 0.015) -> str:
    """Build gradient debanding filter."""
    return f"deband=1thr={threshold}:2thr={threshold}:3thr={threshold}"


def build_repair_filter() -> str:
    """Build combined structural repair filter (deflicker -> deband -> subtle contrast).

    Must run BEFORE any film grain or halation pass so temporal filters do not
    treat synthetic grain as flicker noise.
    """
    return f"{build_deflicker_filter()},{build_deband_filter()},eq=contrast=1.02:saturation=1.03"


def build_audio_master_filter(target_lufs: float = -14.0, true_peak: float = -1.0, lra: float = 9.0) -> str:
    """Build single-pass noise reduction + loudness normalization filter."""
    return f"afftdn=nf=-25,loudnorm=I={target_lufs}:TP={true_peak}:LRA={lra}"


def build_loudnorm_pass2_filter(
    measured: Dict[str, Any],
    target_lufs: float = -14.0,
    true_peak: float = -1.0,
    lra: float = 11.0,
) -> str:
    """Build linear two-pass loudnorm filter from pass-1 JSON measurements."""
    return (
        f"loudnorm=I={target_lufs}:TP={true_peak}:LRA={lra}:"
        f"measured_I={measured['input_i']}:"
        f"measured_TP={measured['input_tp']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:linear=true"
    )


def parse_loudnorm_json(stderr_text: str) -> Optional[Dict[str, Any]]:
    """Extract the JSON summary block emitted by FFmpeg loudnorm=print_format=json."""
    matches = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", stderr_text, re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None


def parse_ebur128_summary(stderr_text: str) -> Dict[str, Optional[float]]:
    """Parse integrated loudness (LUFS), LRA, and true peak (dBTP) from ebur128 output."""
    integrated = None
    lra = None
    true_peak = None

    m_i = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", stderr_text)
    if m_i:
        integrated = float(m_i.group(1))
    m_lra = re.search(r"Loudness range:\s*\n\s*LRA:\s*(-?\d+(?:\.\d+)?)\s*LU", stderr_text)
    if m_lra:
        lra = float(m_lra.group(1))
    m_tp = re.search(r"True peak:\s*\n\s*Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", stderr_text)
    if m_tp:
        true_peak = float(m_tp.group(1))

    return {
        "integrated_lufs": integrated,
        "lra_lu": lra,
        "true_peak_dbtp": true_peak,
    }


def audit_clip(input_path: str, as_json: bool = False) -> Dict[str, Any]:
    """Audit clip metadata and output custody verification details."""
    digest = calculate_sha256(input_path)
    meta = probe_video(input_path)
    v_stream = next((s for s in meta.get("streams", []) if s["codec_type"] == "video"), None)
    a_stream = next((s for s in meta.get("streams", []) if s["codec_type"] == "audio"), None)

    report: Dict[str, Any] = {
        "file": input_path,
        "sha256": digest,
        "duration_s": float(meta.get("format", {}).get("duration", 0.0) or 0.0),
        "size_bytes": int(meta.get("format", {}).get("size", 0) or 0),
        "video": None,
        "audio": None,
    }
    if v_stream:
        report["video"] = {
            "codec": v_stream.get("codec_name", "unknown"),
            "width": v_stream.get("width"),
            "height": v_stream.get("height"),
            "fps": v_stream.get("r_frame_rate", "unknown"),
            "pix_fmt": v_stream.get("pix_fmt", "unknown"),
        }
    if a_stream:
        report["audio"] = {
            "codec": a_stream.get("codec_name", "unknown"),
            "sample_rate": a_stream.get("sample_rate", "unknown"),
            "channels": a_stream.get("channels"),
        }

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print(f"File: {input_path}")
        print(f"SHA-256: {digest}")
        if report["video"]:
            v = report["video"]
            print(f"Video: {v['codec']} {v['width']}x{v['height']} @ {v['fps']} fps ({v['pix_fmt']})")
        if report["audio"]:
            a = report["audio"]
            print(f"Audio: {a['codec']} {a['sample_rate']} Hz ({a['channels']} ch)")
    return report


def apply_deflicker(input_path: str, output_path: str) -> None:
    """Apply moving-average luminance deflicker filter."""
    vf = build_deflicker_filter()
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
    vf = build_deband_filter()
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


def apply_audio_mastering(input_path: str, output_path: str, target_lufs: float = -14.0) -> None:
    """Clean background noise and apply two-pass loudness normalization."""
    pass1 = run_ffmpeg([
        "-i", input_path,
        "-af", f"afftdn=nf=-25,loudnorm=I={target_lufs}:TP=-1.0:LRA=11:print_format=json",
        "-f", "null", "-",
    ])
    measured = parse_loudnorm_json(pass1.stderr)
    if measured:
        af = f"afftdn=nf=-25,{build_loudnorm_pass2_filter(measured, target_lufs=target_lufs)}"
    else:
        af = build_audio_master_filter(target_lufs=target_lufs)

    run_ffmpeg([
        "-i", input_path,
        "-c:v", "copy",
        "-af", af,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Mastered audio video saved to {output_path}")


def apply_full_repair(input_path: str, output_path: str, target_lufs: float = -14.0) -> None:
    """Chain deflicker, deband, color grade, and audio normalization."""
    vf = build_repair_filter()
    af = build_audio_master_filter(target_lufs=target_lufs)
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
    parser.add_argument("--lufs", type=float, default=-14.0, help="Target integrated loudness in LUFS")
    parser.add_argument("--json", action="store_true", help="Output JSON for audit command")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.stderr.write(f"Error: input file {args.input} does not exist.\n")
        sys.exit(1)

    if args.command == "audit":
        audit_clip(args.input, as_json=args.json)
    elif args.command == "deflicker":
        apply_deflicker(args.input, args.output)
    elif args.command == "deband":
        apply_deband(args.input, args.output)
    elif args.command == "stabilize":
        apply_stabilization(args.input, args.output)
    elif args.command == "audio":
        apply_audio_mastering(args.input, args.output, target_lufs=args.lufs)
    elif args.command == "full":
        apply_full_repair(args.input, args.output, target_lufs=args.lufs)


if __name__ == "__main__":
    main()
