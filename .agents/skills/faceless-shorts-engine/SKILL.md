---
name: faceless-shorts-engine
description: >-
  Autonomous pipeline for producing zero-cost animated faceless vertical shorts (YouTube Shorts,
  TikTok, Instagram Reels) using local AI voice synthesis (Kokoro), word-synced subtitles (Whisper),
  6 animation styles (Tall Tale 3D, Deep Dive 3D, Inside Out, Stick Story, Night File 3D, Paper Atlas),
  and automated FFmpeg/Remotion compositing with organic photochemical film finishing.
metadata:
  version: 1.0.0
  tier: 1
  domain: video
  origin: Antigravity / Nafay 3D / Kokoro / Whisper
---

# Faceless Shorts Engine (Zero-Cost Vertical Video Pipeline)

Guides the end-to-end creation of automated, high-retention vertical animated shorts (9:16 aspect ratio) for YouTube Shorts, TikTok, and Instagram Reels without paid API subscriptions or cloud video rendering fees.

For deep technical specifications, inspect the reference documents:
- [Animation Styles Manual](references/ANIMATION_STYLES_MANUAL.md)
- [Local Toolchain Setup](references/LOCAL_TOOLCHAIN_SETUP.md)
- [Retention & Scripting Playbook](references/RETENTION_AND_SCRIPTING_PLAYBOOK.md)

---

## 0. Zero-Cost Local Operating Invariants

1. **Zero External API Costs**: All neural speech generation (Kokoro TTS), subtitle transcription (OpenAI Whisper), and video compositing run locally on device hardware. Never invoke paid cloud APIs (e.g. ElevenLabs, HeyGen, Runway) without explicit written user authorization.
2. **Deterministic Offline Execution**: The entire pipeline functions with or without an active internet connection once local weights (`kokoro-v0_19.onnx`, Whisper `base.en`) and dependencies are cached.
3. **9:16 Mobile Native Format**: All final outputs render at 1080x1920 resolution, 30fps or 60fps, with universal H.264 video and AAC audio encoding.
4. **Authentic Directing & Anti-Slop Voice**: Scripts must avoid generic AI narrative formulas. Never use conversational filler, greetings, or artificial pleasantries. Hook the viewer in the first 2 seconds.

---

## 1. System Requirements & Setup Protocol

Verify core local binaries before initiating production:
```bash
python3 --version   # Python 3.10+
node --version      # Node.js 18+
ffmpeg -version     # FFmpeg 5.0+ with libx264
```

### Python Package Dependencies
```bash
pip install kokoro-onnx soundfile faster-whisper
# or via uv:
uv pip install kokoro-onnx soundfile faster-whisper
```

---

## 2. Viral Retention & Scriptwriting Rules

1. **In Medias Res Hook (0.00s–2.00s)**:
   - Ban all introductions (*"Hey everyone"*, *"Did you know"*, *"Today we explore"*).
   - Start directly with the punchline, anomaly, or extreme condition:
     *Example*: "In 1999, a customer bought an entire bank for one dollar."
2. **The 2-Second Visual Reset**:
   - Camera perspectives, character poses, or visual layers must reset every 1.5–2.0 seconds.
   - Alternate between wide establishing shots, extreme macro snap zooms, cutaway schematics, and horizontal pans.
3. **Algorithmic Seamless Loop**:
   - The final sentence must seamlessly and grammatically connect into the opening sentence.
   - *Example closing*: "And that is how..." -> *Loops into opening*: "...he bought an entire bank for one dollar."
4. **Pacing & Word Count**:
   - Spoken pace: 150–165 words per minute.
   - 35-second short: Exactly 80–90 words.
   - 55-second short: Exactly 135–150 words (never exceed 59 seconds).

---

## 3. The 6 Standardized Animation Styles

Select one of the 6 core visual styles based on topic intent:

| Style | Aesthetic Character | Ideal Topic Domains | Recommended Voice |
|---|---|---|---|
| **Tall Tale 3D** | 2D illustrated character cutouts inside miniature 3D worlds | Crazy loopholes, true crime heists, bizarre history | `am_adam` |
| **Deep Dive 3D** | Zack D. Films style 3D anatomical cutaways & x-ray organs | Medical phenomena, biological hazards, body explainers | `af_bella` |
| **Inside Out** | 2D technical exploded diagrams and blueprint schematics | Mechanical engineering, physical experiments, watchmaking | `af_bella` |
| **Stick Story** | High-contrast vector stick figures with hazard markers | Survival dilemmas, decision trees, logic riddles | `am_adam` |
| **Night File 3D** | Noir low-key lighting, volumetric fog, dark archival files | Unsolved mysteries, disappearances, cold case archives | `am_michael` |
| **Paper Atlas** | Aged parchment maps with animated campaign trails & tokens | Historical battles, ancient empires, maritime routes | `bm_george` |

See [Animation Styles Manual](references/ANIMATION_STYLES_MANUAL.md) for camera angles and shader settings.

---

## 4. Speech Synthesis & Kinetic Subtitle Alignment

### Step 1: Local Kokoro Audio Generation
```python
import soundfile as sf
from kokoro_onnx import Kokoro

kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
samples, sample_rate = kokoro.create(
    text="In 1999, a customer bought an entire bank for one dollar.",
    voice="am_adam",
    speed=1.05,
    lang="en-us"
)
sf.write("speech.wav", samples, sample_rate)
```

### Step 2: Whisper Word-Level Timestamps
```python
from faster_whisper import WhisperModel
import json

model = WhisperModel("base.en", device="cpu", compute_type="int8")
segments, _ = model.transcribe("speech.wav", word_timestamps=True)
words = [{"word": w.word.strip().upper(), "start": w.start, "end": w.end} for s in segments for w in s.words]
with open("captions.json", "w") as f:
    json.dump(words, f, indent=2)
```

### Subtitle Visual Standard
- Font: Heavy sans-serif (e.g. Montserrat Black).
- Base Color: `#FFFFFF` with 4px black outline.
- Active Word Highlight: `#FFE500` (Safety Yellow) or `#00FF66` (Signal Green).
- Vertical Position: `Y = 68%` to avoid TikTok and Reels UI overlays.

---

## 5. Foley, Audio Ducking & Video Assembly

1. **Foley Cue Sheet**:
   - `sfx_pop.wav`: Sync to character expression changes and text card reveals.
   - `sfx_whoosh.wav`: Sync to camera snap zooms and wipe transitions.
   - `sfx_ding.wav`: Sync to money figures and breakthrough choices.
   - `sfx_impact.wav`: Sync to dramatic revelations and anatomical cutaways.
2. **Audio Ducking**:
   - Background music must be ducked by -18dB under speech.
   - Master integrated loudness to -14 LUFS (EBU R128).
3. **FFmpeg Assembly Filter**:
   ```bash
   ffmpeg -i speech.wav -i music.mp3 -filter_complex \
   "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=first[outa]" \
   -map "[outa]" -c:a aac -b:a 192k audio_mixed.aac
   ```

---

## 6. Photochemical Film Finishing & Anti-AI Polish

To eliminate the artificial digital AI sheen and give animated 3D/2D renders a cinematic look, pass the composited MP4 through the AGYOS organic film engine:

```bash
python3 scripts/organic_film_engine.py input_short.mp4 output_cinematic_short.mp4 \
  --lut kodak_2383 \
  --grain 0.15 \
  --halation \
  --loudness -14
```

This applies:
- Kodak 2383 film stock color S-curve.
- CineStill-style halation bloom around high-luminance highlights.
- Organic 35mm silver halide grain simulation.
- Two-pass EBU R128 audio mastering.

---

## 7. Execution Checklist & Verification

Before publishing or rendering a faceless short:
- [ ] First spoken sentence delivers premise or anomaly within 0.00s–2.00s.
- [ ] Total word count matches target duration (150–165 words/minute; <59s total).
- [ ] Camera perspective or character state shifts at least once every 2 seconds.
- [ ] Last spoken phrase seamlessly loops into the opening phrase.
- [ ] Subtitle text is positioned above Y=65% to avoid platform UI clipping.
- [ ] Background music is ducked by -18dB under speech.
- [ ] Render resolution is exactly 1080x1920 (9:16) at 30 or 60 fps.
- [ ] No external paid APIs were invoked.
