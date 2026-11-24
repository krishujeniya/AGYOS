#!/usr/bin/env python3
"""
Organic Film Craft & De-AI Processing Engine.
Transforms synthetic AI video into organic cinema by applying Kodak 2383
film curve tonemapping, highlight halation bloom, 35mm photochemical grain,
optical lens curvature, 180-degree shutter motion blur, aspect-preserving
handheld micro-drift, and acoustic room warmth.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Dict, Tuple


FILM_PROFILES: Dict[str, Dict[str, Any]] = {
    "cinema-2383": {
        "description": "Kodak 2383 print stock S-curve, halation bloom, 35mm grain, subtle optics, room warmth",
        "contrast": 1.03,
        "brightness": 0.01,
        "saturation": 0.94,
        "halation_opacity": 0.30,
        "grain_luma": 10,
        "grain_chroma": 6,
        "vignette": "PI/4.5",
        "k1": -0.012,
        "k2": 0.004,
    },
    "doc-neutral": {
        "description": "Restrained documentary finish with gentle highlight rolloff and fine grain",
        "contrast": 1.02,
        "brightness": 0.0,
        "saturation": 0.97,
        "halation_opacity": 0.16,
        "grain_luma": 6,
        "grain_chroma": 4,
        "vignette": "PI/5.5",
        "k1": -0.006,
        "k2": 0.002,
    },
    "vertical-clean": {
        "description": "Mobile-legible 9:16 finish preserving crisp text contrast with subtle organic texture",
        "contrast": 1.04,
        "brightness": 0.01,
        "saturation": 0.96,
        "halation_opacity": 0.18,
        "grain_luma": 7,
        "grain_chroma": 4,
        "vignette": "PI/6.0",
        "k1": -0.005,
        "k2": 0.001,
    },
}


def probe_dimensions(input_path: str) -> Tuple[int, int]:
    """Probe video width and height via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        input_path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data["streams"][0]
    return int(stream["width"]), int(stream["height"])


def run_ffmpeg(args: list[str]) -> None:
    """Execute FFmpeg command with error handling."""
    cmd = ["ffmpeg", "-y"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"FFmpeg error: {res.stderr}\n")
        sys.exit(res.returncode)


def build_film_grade_filter(contrast: float = 1.03, brightness: float = 0.01, saturation: float = 0.94) -> str:
    """Build Kodak 2383 print stock S-curve and subtractive desaturation filter."""
    return (
        f"eq=contrast={contrast}:brightness={brightness}:saturation={saturation},"
        "curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':"
        "g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':"
        "b='0/0.03 0.25/0.25 0.75/0.75 1/0.92'"
    )


def build_halation_filter_complex(opacity: float = 0.32) -> str:
    """Build photochemical red-orange highlight halation bloom filter_complex."""
    return (
        "[0:v]split=2[base][glow];"
        "[glow]lutyuv=y='if(gt(val,205),val,0)':u=128:v=128[highlights];"
        "[highlights]gblur=sigma=22:steps=3[blurred];"
        "[blurred]colorbalance=rs=0.45:gs=-0.15:bs=-0.35[tinted];"
        f"[base][tinted]blend=all_mode='screen':all_opacity={opacity}[out]"
    )


def build_film_grain_filter(luma_strength: int = 11, chroma_strength: int = 7) -> str:
    """Build 35mm silver halide crystal grain filter."""
    return (
        f"noise=c0s={luma_strength}:c0f=t+u:c1s={chroma_strength}:c1f=t+u:"
        f"c2s={chroma_strength}:c2f=t+u,unsharp=3:3:0.4:3:3:0.0"
    )


def build_lens_optics_filter(vignette: str = "PI/4.5", k1: float = -0.015, k2: float = 0.005) -> str:
    """Build optical lens vignetting and subtle spherical barrel distortion filter."""
    return f"vignette={vignette},lenscorrection=cx=0.5:cy=0.5:k1={k1}:k2={k2}"


def build_handheld_drift_filter(width: int | None = None, height: int | None = None) -> str:
    """Build aspect-preserving sinusoidal camera breathing and operator micro-sway filter.

    Preserves exact input dimensions (9:16, 16:9, 1:1, 4K) instead of hardcoding 1280x720.
    """
    if width and height:
        scale_expr = f"scale={width}:{height}:flags=lanczos"
    else:
        scale_expr = "scale=iw+32:ih+32:flags=lanczos"
    return (
        "crop=in_w-32:in_h-32:"
        "(in_w-out_w)/2+10*sin(t*1.4)+5*sin(t*3.2):"
        "(in_h-out_h)/2+7*cos(t*1.1)+3*cos(t*2.8),"
        f"{scale_expr}"
    )


def build_shutter_blur_filter() -> str:
    """Build 180-degree shutter angle optical motion blur approximation."""
    return "tblend=all_mode=average,framestep=1"


def build_acoustic_room_filter() -> str:
    """Build vocal warmth EQ, early room reflection, and -14 LUFS mastering filter."""
    return "highpass=f=80,lowpass=f=14000,aecho=0.8:0.88:25|45:0.25|0.12,loudnorm=I=-14:TP=-1.0:LRA=9"


def build_organic_master_filter_complex(profile: str = "cinema-2383", include_shutter: bool = False) -> str:
    """Build single-pass organic cinema filter_complex for a named profile."""
    cfg = FILM_PROFILES.get(profile, FILM_PROFILES["cinema-2383"])
    shutter_prefix = "tblend=all_mode=average," if include_shutter else ""
    return (
        "[0:v]split=2[base][glow];"
        "[glow]lutyuv=y='if(gt(val,205),val,0)':u=128:v=128[highlights];"
        "[highlights]gblur=sigma=22:steps=3[blurred];"
        "[blurred]colorbalance=rs=0.45:gs=-0.15:bs=-0.35[tinted];"
        f"[base][tinted]blend=all_mode='screen':all_opacity={cfg['halation_opacity']},"
        f"{shutter_prefix}"
        f"eq=contrast={cfg['contrast']}:brightness={cfg['brightness']}:saturation={cfg['saturation']},"
        "curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':"
        "g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':"
        "b='0/0.03 0.25/0.25 0.75/0.75 1/0.92',"
        f"noise=c0s={cfg['grain_luma']}:c0f=t+u:c1s={cfg['grain_chroma']}:c1f=t+u:c2s={cfg['grain_chroma']}:c2f=t+u,"
        f"vignette={cfg['vignette']},"
        f"lenscorrection=cx=0.5:cy=0.5:k1={cfg['k1']}:k2={cfg['k2']}[vout]"
    )


def apply_film_grade(input_path: str, output_path: str) -> None:
    """Apply Kodak 2383 print stock S-curve and subtractive desaturation."""
    vf = build_film_grade_filter()
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Film graded video saved to {output_path}")


def apply_halation(input_path: str, output_path: str) -> None:
    """Apply photochemical red-orange highlight halation bloom."""
    fc = build_halation_filter_complex()
    run_ffmpeg([
        "-i", input_path,
        "-filter_complex", fc,
        "-map", "[out]",
        "-map", "0:a?",
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Halation bloom applied to {output_path}")


def apply_film_grain(input_path: str, output_path: str) -> None:
    """Synthesize 35mm silver halide crystal grain."""
    vf = build_film_grain_filter()
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Film grain synthesized to {output_path}")


def apply_lens_optics(input_path: str, output_path: str) -> None:
    """Apply optical lens vignetting and subtle spherical barrel distortion."""
    vf = build_lens_optics_filter()
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Lens optics applied to {output_path}")


def apply_handheld_drift(input_path: str, output_path: str) -> None:
    """Inject subtle sinusoidal camera breathing while preserving exact aspect ratio."""
    width, height = probe_dimensions(input_path)
    vf = build_handheld_drift_filter(width, height)
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Handheld camera drift ({width}x{height}) injected to {output_path}")


def apply_shutter_blur(input_path: str, output_path: str) -> None:
    """Apply 180-degree shutter angle motion blur approximation."""
    vf = build_shutter_blur_filter()
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"180-degree shutter motion blur applied to {output_path}")


def apply_acoustic_room(input_path: str, output_path: str) -> None:
    """Apply vocal warmth EQ, room reflection echo, and -14 LUFS mastering."""
    af = build_acoustic_room_filter()
    run_ffmpeg([
        "-i", input_path,
        "-c:v", "copy",
        "-af", af,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Acoustic room warmth mastered to {output_path}")


def apply_organic_master(
    input_path: str,
    output_path: str,
    profile: str = "cinema-2383",
    include_shutter: bool = False,
) -> None:
    """Execute full single-pass organic cinema transformation."""
    fc = build_organic_master_filter_complex(profile=profile, include_shutter=include_shutter)
    af = build_acoustic_room_filter()
    run_ffmpeg([
        "-i", input_path,
        "-filter_complex", fc,
        "-map", "[vout]",
        "-map", "0:a?",
        "-af", af,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-map_metadata", "-1",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Master organic cinema video ({profile}) saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organic Film Craft & De-AI CLI")
    parser.add_argument(
        "command",
        choices=["grade", "halation", "grain", "optics", "handheld", "shutter", "acoustic", "master"],
        help="Command operation to perform",
    )
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("-o", "--output", default="output_cinema.mp4", help="Path to output video file")
    parser.add_argument(
        "--profile",
        choices=sorted(FILM_PROFILES.keys()),
        default="cinema-2383",
        help="Film finishing profile for master command",
    )
    parser.add_argument("--shutter", action="store_true", help="Include 180-degree shutter motion blur in master")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.stderr.write(f"Error: input file {args.input} does not exist.\n")
        sys.exit(1)

    if args.command == "grade":
        apply_film_grade(args.input, args.output)
    elif args.command == "halation":
        apply_halation(args.input, args.output)
    elif args.command == "grain":
        apply_film_grain(args.input, args.output)
    elif args.command == "optics":
        apply_lens_optics(args.input, args.output)
    elif args.command == "handheld":
        apply_handheld_drift(args.input, args.output)
    elif args.command == "shutter":
        apply_shutter_blur(args.input, args.output)
    elif args.command == "acoustic":
        apply_acoustic_room(args.input, args.output)
    elif args.command == "master":
        apply_organic_master(args.input, args.output, profile=args.profile, include_shutter=args.shutter)


if __name__ == "__main__":
    main()
