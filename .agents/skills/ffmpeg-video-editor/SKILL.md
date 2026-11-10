---
name: ffmpeg-video-editor
description: >-
  Automated, programmatic video and audio editing using local FFmpeg. Covers silence detection,
  audio ducking with sidechain compression, YouTube loudness normalization (-14 LUFS), B-roll overlay
  cutaways, dynamic zoom punch-ins, SRT caption styling, and multi-clip concatenation with transitions.
metadata:
  version: 1.0.0
license: MIT
---

# FFmpeg Video Editor

Programmatic video assembly and audio post-production engine for local shell workflows. Replaces manual graphical timeline tasks with deterministic, reproducible FFmpeg commands.

## Audio Engineering for YouTube

YouTube normalizes all video audio to **-14 LUFS integrated loudness** with a **-1.0 dB True Peak ceiling**. Audio mastered outside this target gets dynamically lowered by the YouTube platform, causing uneven volume across videos.

### Two-Pass Loudness Normalization (-14 LUFS)

Pass 1: Measure current audio profile
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json -f null -
```

Pass 2: Apply linear normalization with measured parameters
```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=11:\
measured_I=-21.4:\
measured_TP=-3.2:\
measured_LRA=9.1:\
measured_thresh=-32.0:\
offset=0.2 \
-c:v copy -c:a aac -b:a 192k output_normalized.mp4
```

### Dynamic Background Music Ducking

Automatically attenuates background music by 18dB whenever narration is active using sidechain compression:

```bash
ffmpeg -i voiceover.wav -i background_music.mp3 -filter_complex \
"[1:a]volume=0.35[music_base]; \
 [music_base][0:a]sidechaincompress=threshold=0.08:ratio=6:attack=20:release=300[ducked_music]; \
 [0:a][ducked_music]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
-map "[aout]" -c:a aac -b:a 192k mixed_audio.mp4
```

---

## Footage Assembly & Timing Automation

### Automated Silence Removal

Detects and strips dead air pauses longer than 400 milliseconds from talking head or screen recordings:

```bash
ffmpeg -i raw_take.mp4 -af "silencedetect=noise=-30dB:d=0.4" -f null - 2> silence.log
```

Remove silence intervals using the `silenceremove` filter:
```bash
ffmpeg -i raw_take.mp4 -af "silenceremove=start_periods=1:start_duration=0.1:start_threshold=-30dB:stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB" -c:v copy tight_take.mp4
```

### Dynamic 1.15x Zoom Punch-in

Creates visual rhythm during single-camera talking head segments to emphasize key arguments without jump cuts:

```bash
# Smooth punch-in between second 5 and second 10
ffmpeg -i input.mp4 -vf \
"zoompan=z='if(between(it,5,10),1.15,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30" \
-c:a copy punch_in.mp4
```

### Video Watermark Removal & Delogo Inpainting

Removes localized corner logos or watermarks using bilateral pixel interpolation:

```bash
# General syntax: delogo=x=<left>:y=<top>:w=<width>:h=<height>
# Example for 1280x720 video with bottom-right watermark:
ffmpeg -i input.mp4 -vf "delogo=x=1236:y=688:w=36:h=22" -c:a copy clean_output.mp4

# Automated python helper with auto-detection:
python3 scripts/remove_flow_watermark.py input.mp4 [clean_output.mp4]
```

---

## B-Roll Overlay & Cutaways

Inserts a generative Google Flow / Veo 3.1 B-roll clip over the primary voiceover track at a precise timestamp.

### Clean Cutaway with 0.5s Dissolve Fade

```bash
ffmpeg -i main_track.mp4 -i b_roll.mp4 -filter_complex \
"[1:v]scale=1920:1080,fade=t=in:st=0:d=0.5:alpha=1,fade=t=out:st=7.5:d=0.5:alpha=1[broll_fade]; \
 [0:v][broll_fade]overlay=0:0:enable='between(t,15,23)'[vout]" \
-map "[vout]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy final_cutaway.mp4
```

### Picture-in-Picture (PiP) Lower Third Box

Scales secondary footage into the bottom right corner with a subtle border:

```bash
ffmpeg -i primary.mp4 -i secondary.mp4 -filter_complex \
"[1:v]scale=480:270,pad=484:274:2:2:white[pip]; \
 [0:v][pip]overlay=W-w-40:H-h-40:enable='between(t,30,55)'[vout]" \
-map "[vout]" -map 0:a -c:v libx264 -c:a copy pip_output.mp4
```

---

## Multi-Clip Timeline Concatenation

### Lossless Stream Concatenation (Identical Codecs)

Create file list `inputs.txt`:
```text
file 'scene_01.mp4'
file 'scene_02.mp4'
file 'scene_03.mp4'
```

Concatenate without re-encoding:
```bash
ffmpeg -f concat -safe 0 -i inputs.txt -c copy assembled_full.mp4
```

### Transition Concatenation (Cross-Dissolve xfade)

Merges two scenes with an authentic 1-second film dissolve:

```bash
ffmpeg -i scene_01.mp4 -i scene_02.mp4 -filter_complex \
"[0:v][1:v]xfade=transition=dissolve:duration=1:offset=7[vout]; \
 [0:a][1:a]acrossfade=d=1[aout]" \
-map "[vout]" -map "[aout]" -c:v libx264 -crf 18 -c:a aac assembled_dissolve.mp4
```

---

## Subtitles & Hardcoded Captions

Burn custom-styled open captions for social snippets or high-retention YouTube intro sequences:

```bash
ffmpeg -i input.mp4 -vf \
"subtitles=captions.srt:force_style='Fontname=Arial,Fontsize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=0,Alignment=2,MarginV=40'" \
-c:a copy captioned_output.mp4
```

---

## YouTube Export Preset Standards

- **Container**: MP4
- **Video Codec**: H.264 (High Profile, Level 4.2)
- **Pixel Format**: YUV420p
- **Frame Rate**: Constant 24, 30, or 60 fps
- **GOP**: Keyframe interval equal to frame rate (1 keyframe per second)
- **Audio Codec**: AAC-LC, Stereo, 48kHz, 384 kbps (or 192 kbps minimum)

Command:
```bash
ffmpeg -i master.mp4 -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p -g 30 -bf 2 -crf 17 -preset slow -c:a aac -b:a 384k -ar 48000 youtube_final_master.mp4
```
