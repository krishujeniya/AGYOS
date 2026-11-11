---
name: youtube-long-form-production
description: >-
  End-to-end engineering pipeline for high-retention, long-form YouTube videos (8-25 minutes).
  Integrates packaging pre-production, 4-act retention scripting, B-roll generation with Google Flow
  and Veo 3.1, audio mastering to -14 LUFS, and programmatic editing via FFmpeg.
metadata:
  version: 1.0.0
license: MIT
---

# YouTube Long-Form Production

Systematic production framework for engineering high-retention YouTube long-form videos (8 to 25 minutes). Covers market validation, packaging pre-production, retention scriptwriting, B-roll generation with Google Flow, and automated audio/video post-production.

## Core Directing Invariants

1. **Packaging Before Scripting**: Never write a script without at least 3 verified title/thumbnail pairs. If an idea cannot be packaged into a compelling click proposition, it will not earn views regardless of production quality.
2. **Immediate Proof of Concept (First 30 Seconds)**: Pay off the thumbnail and title within the first 30 seconds. Never open with a greeting ("Hey guys"), channel logo sting, or housekeeping announcements.
3. **Pacing Resets Every 5-7 Seconds**: Change visual information (B-roll cutaway, camera punch-in, graphic callout, screen recording, lower third) every 5 to 7 seconds to maintain active attention.
4. **Session Extension Dominance**: Structure the video ending as a psychological bridge to another video in the channel catalog rather than a slow concluding wind-down.

---

## Stage 1: Packaging Pre-Production

### Title Architecture (Test 3 Distinct Angles)
- **Angle 1 (Curiosity Gap)**: Focus on an unexpected counterintuitive result (*"Why Silicon Valley Stopped Writing Code"*).
- **Angle 2 (High Stakes)**: Focus on personal consequence or risk (*"The Database Mistake That Cost Us $84,000"*).
- **Angle 3 (Systemic Deep-Dive)**: Authoritative, definitive framework (*"How Modern High-Frequency Trading Actually Works"*).

### Thumbnail Direction
- **Rule of Visual Contrast**: Foreground subject must maintain at least 4.5:1 luminance contrast against background.
- **Maximum 3-Word Text**: Thumbnail text must complement, not repeat, the title words.
- **Expression & Gaze**: If using human face, direct eye contact or gaze aimed toward the core visual element.

---

## Stage 2: The 4-Act Retention Script Architecture

```
0:00 ─── Act 1: The Hook & The Unresolved Loop (0:00 - 0:45)
          Pay off packaging immediately. Introduce the central conflict.
          
0:45 ─── Act 2: Context & Early Payoff (0:45 - 3:30)
          Establish foundational knowledge. Deliver one rapid insight to reward the viewer.
          
3:30 ─── Act 3: Escalation & Depth (3:30 - 14:00)
          Segmented into 3-minute sub-chapters. Open a new curiosity loop before closing the old one.
          
14:00 ── Act 4: The Climax & Session Bridge (14:00 - End)
          Deliver final resolution. Cut immediately to next suggested video (zero outro filler).
```

### Script Notation Standard
Every long-form script must contain concrete production cues:

```text
[VISUAL]: Primary camera / talking head (Medium close-up, 50mm).
[AUDIO]: Voiceover narration with steady, conversational pacing (155 WPM).
[TEXT OVERLAY]: "Target: 99.999% Availability" in clean sans-serif typography.
[B-ROLL CUE]: Cinematic Google Flow clip: Server rack interior with pulsing fiber optic lights.
[SFX]: Subtle digital data chirp matching text appearance.
```

---

## Stage 3: Generative B-Roll via Google Flow & Veo 3.1

Use [google-flow](../google-flow/SKILL.md) to generate high-fidelity B-roll clips headlessly:

1. **Extract B-Roll List from Script**:
   Identify 10-20 specific cutaways needed throughout the narrative (establishing shots, metaphorical scenes, mechanical details).
2. **Apply [veo-3](../veo-3/SKILL.md) Prompt Structure**:
   Structure each clip with subject, physical action, camera trajectory, lighting mood, and synchronized ambient sound.
3. **Execute Headless Generation**:
   Run `flow_generate_video` with `model="veo-3.1-quality"`, `ratio="16:9"`, and `duration=8`.
4. **Extend for Long Takes**:
   For scenes requiring continuous coverage over 8 seconds, use `flow_scene_add` followed by `flow_scene_extend` to generate matching continuation clips.

---

## Stage 4: Voiceover & Audio Mastering

1. **Voiceover Generation**:
   Generate narration audio at 48kHz, mono or stereo, maintaining conversational cadence.
2. **Sound Effects Placement**:
   Add subtle SFX (whooshes, risers, mechanical clicks, sub-bass hits) at topic transitions and visual changes.
3. **Dynamic Music Ducking**:
   Duck background music by 18dB during voiceover using sidechain compression via [ffmpeg-video-editor](../ffmpeg-video-editor/SKILL.md).
4. **Mastering Standard**:
   Normalize final audio mix to **-14 LUFS integrated loudness** and **-1.0 dB True Peak ceiling**.

---

## Stage 5: Programmatic Assembly via FFmpeg

Run automated assembly using recipes from [ffmpeg-video-editor](../ffmpeg-video-editor/SKILL.md):

```bash
# 1. Strip silence intervals > 400ms
ffmpeg -i raw_voiceover.mp4 -af "silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-30dB" clean_voice.mp4

# 2. Composite B-roll overlay cutaways
ffmpeg -i clean_voice.mp4 -i b_roll_scene1.mp4 -filter_complex \
"[1:v]scale=1920:1080,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=7.7:d=0.3:alpha=1[broll]; \
 [0:v][broll]overlay=0:0:enable='between(t,12,20)'[vout]" \
-map "[vout]" -map 0:a -c:v libx264 -crf 17 -c:a copy assembled_cut.mp4

# 3. Two-pass -14 LUFS loudness mastering
ffmpeg -i assembled_cut.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=11 -c:v copy final_youtube_master.mp4
```

---

## Stage 6: YouTube Metadata & Launch Checklist

- [ ] **Title**: Primary search keyword placed in first 40 characters.
- [ ] **Thumbnail**: High-contrast, maximum 3 words text, verified at 120x68 mobile size.
- [ ] **Chapters / Timestamps**: Included in video description with keyword-rich titles:
  ```text
  0:00 - The Infrastructure Paradox
  1:42 - Why Traditional Clusters Break Under Load
  4:15 - Architecture Breakdown: Zero-Copy Queues
  8:30 - Live Benchmark & Failure Injection
  12:45 - What to Build Instead
  ```
- [ ] **Description Above-the-Fold**: First 2 lines provide direct value and keyword context without greeting boilerplate.
- [ ] **Pinned Comment**: Contains open-ended question to drive comment velocity during first 24 hours.
- [ ] **End Screen Card**: Links to complementary video to trigger algorithm session chaining.
