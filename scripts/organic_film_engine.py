#!/usr/bin/env python3
"""
Organic Film Craft & De-AI Processing Engine.
Transforms synthetic AI video into organic cinema by applying Kodak 2383
film curve tonemapping, highlight halation bloom, 35mm photochemical grain,
optical lens curvature, and acoustic room warmth.
"""

import argparse
import os
import subprocess
import sys


def run_ffmpeg(args: list[str]) -> None:
    """Execute FFmpeg command with error handling."""
    cmd = ["ffmpeg", "-y"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"FFmpeg error: {res.stderr}\n")
        sys.exit(res.returncode)


def apply_film_grade(input_path: str, output_path: str) -> None:
    """Apply Kodak 2383 print stock S-curve and subtractive desaturation."""
    vf = (
        "eq=contrast=1.03:brightness=0.01:saturation=0.94,"
        "curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':"
        "g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':"
        "b='0/0.03 0.25/0.25 0.75/0.75 1/0.92'"
    )
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
    fc = (
        "[0:v]split=2[base][glow];"
        "[glow]lutyuv=y='if(gt(val,205),val,0)':u=128:v=128[highlights];"
        "[highlights]gblur=sigma=22:steps=3[blurred];"
        "[blurred]colorbalance=rs=0.45:gs=-0.15:bs=-0.35[tinted];"
        "[base][tinted]blend=all_mode='screen':all_opacity=0.32[out]"
    )
    run_ffmpeg([
        "-i", input_path,
        "-filter_complex", fc,
        "-map", "[out]",
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Halation bloom applied to {output_path}")


def apply_film_grain(input_path: str, output_path: str) -> None:
    """Synthesize 35mm silver halide crystal grain."""
    vf = "noise=c0s=11:c0f=t+u:c1s=7:c1f=t+u:c2s=7:c2f=t+u,unsharp=3:3:0.4:3:3:0.0"
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
    vf = "vignette=PI/4.5,lenscorrection=cx=0.5:cy=0.5:k1=-0.015:k2=0.005"
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
    """Inject subtle sinusoidal camera breathing and operator micro-sway."""
    vf = (
        "crop=in_w-32:in_h-32:"
        "(in_w-out_w)/2+10*sin(t*1.4)+5*sin(t*3.2):"
        "(in_h-out_h)/2+7*cos(t*1.1)+3*cos(t*2.8),"
        "scale=1280:720"
    )
    run_ffmpeg([
        "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "0",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Handheld camera drift injected to {output_path}")


def apply_acoustic_room(input_path: str, output_path: str) -> None:
    """Apply vocal warmth EQ, room reflection echo, and -14 LUFS mastering."""
    af = "highpass=f=80,lowpass=f=14000,aecho=0.8:0.88:25|45:0.25|0.12,loudnorm=I=-14:TP=-1.0:LRA=9"
    run_ffmpeg([
        "-i", input_path,
        "-c:v", "copy",
        "-af", af,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        output_path,
    ])
    print(f"Acoustic room warmth mastered to {output_path}")


def apply_organic_master(input_path: str, output_path: str) -> None:
    """
    Execute full single-pass organic cinema transformation:
    Halation + Kodak 2383 Tonemapping + 35mm Grain + Optics + Acoustic Warmth.
    """
    fc = (
        "[0:v]split=2[base][glow];"
        "[glow]lutyuv=y='if(gt(val,205),val,0)':u=128:v=128[highlights];"
        "[highlights]gblur=sigma=22:steps=3[blurred];"
        "[blurred]colorbalance=rs=0.45:gs=-0.15:bs=-0.35[tinted];"
        "[base][tinted]blend=all_mode='screen':all_opacity=0.30,"
        "eq=contrast=1.03:brightness=0.01:saturation=0.94,"
        "curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':"
        "g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':"
        "b='0/0.03 0.25/0.25 0.75/0.75 1/0.92',"
        "noise=c0s=10:c0f=t+u:c1s=6:c1f=t+u:c2s=6:c2f=t+u,"
        "vignette=PI/4.5,"
        "lenscorrection=cx=0.5:cy=0.5:k1=-0.012:k2=0.004[vout]"
    )
    af = "highpass=f=80,lowpass=f=14000,aecho=0.8:0.88:25|45:0.25|0.12,loudnorm=I=-14:TP=-1.0:LRA=9"
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
    print(f"Master organic cinema video saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organic Film Craft & De-AI CLI")
    parser.add_argument(
        "command",
        choices=["grade", "halation", "grain", "optics", "handheld", "acoustic", "master"],
        help="Command operation to perform",
    )
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("-o", "--output", default="output_cinema.mp4", help="Path to output video file")

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
    elif args.command == "acoustic":
        apply_acoustic_room(args.input, args.output)
    elif args.command == "master":
        apply_organic_master(args.input, args.output)


if __name__ == "__main__":
    main()
