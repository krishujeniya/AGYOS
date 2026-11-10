---
name: organic-film-de-ai
description: >-
  Master craft and CLI engine for transforming AI-generated and AI-edited video into authentic,
  organic cinema. Eliminates the artificial 'AI sheen' (waxy skin, hyper-saturation, sliding camera,
  sterile silence, and staccato motion) using photochemical 35mm film grain, highlight halation bloom,
  lens optical distortion, handheld micro-drift, 180-degree shutter motion blur, Kodak 2383 tone curves,
  and room impulse acoustics. Integrates with the entire AGYOS video editing ecosystem.
metadata:
  version: 1.0.0
  license: MIT
---

# Organic Film Craft & De-AI Video Engine (2026 Reference)

A specialized production runbook for eliminating the visual, temporal, and acoustic hallmarks of generative AI media. Converts sterile, plastic diffusion outputs into authentic, human-crafted cinema using optical physics, photochemical emulsion science, and traditional editing craft.

---

## 1. Anatomy of the AI Look vs. Authentic Film Craft

| Defect Dimension | AI Generation & Editing Hallmarks | Organic Cinema & Human Craft | Remediation Strategy |
|---|---|---|---|
| **Skin & Surface** | Waxy, plastic denoised skin; zero pores; flat uniform surfaces | Physical skin micro-texture; sub-surface scattering; specular highlights | Luminance-weighted 35mm photochemical film grain synthesis |
| **Highlight Rolloff** | Hard digital clipping at pure white (255); harsh digital edge transitions | Photochemical halation bloom (red-orange glow bleeding into midtones) | Multi-pass FFmpeg halation filter (`lutyuv` -> `gblur` -> `colorbalance` -> `blend=screen`) |
| **Color Density** | Hyper-saturated primaries; crushed blacks with zero shadow detail | Kodak 2383 / Fuji 3513 print stock density: lifted toe (2-3%), soft shoulder rolloff | Film print S-curve tone-mapping (`curves`), subtractive color saturation |
| **Lens Physics** | Rectilinear computer-generated geometry; zero distortion; zero optical aberration | Cosine-4th optical vignetting; subtle barrel curvature; micro chromatic aberration | `vignette=PI/4`, `lenscorrection`, subpixel edge channel displacement |
| **Camera Dynamics** | Uncanny linear "slider on ice" dolly; robotic constant velocity; zero breathing | Handheld camera micro-sway; human respiratory cadence; mechanical inertia damping | Low-frequency sinusoidal/Perlin translation drift injection |
| **Motion Cadence** | Staccato AI diffusion frame stepping; unnatural warping on fast action | Physical 180-degree shutter angle (1/48s at 24fps) optical motion blur | Frame blending (`tblend=all_mode=average`) and optical flow interpolation |
| **Editing Rhythms** | Predictable 2.0s clip intervals; frantic uniform jump-cuts; bouncing neon text | Walter Murch's Rule of Six (Emotion 51%, Story 23%, Rhythm 10%); asymmetric shot lengths | L-cuts, J-cuts, motivated cutaways, clean typography without pop animations |
| **Dialogue & Tone** | Robotic vocoder phase buzz; sterile digital silence between words; flat prosody | Natural chest resonance; proximity effect; human pauses; subtle room tone | Vocal warmth EQ (`highpass=80,lowpass=14000`); gentle analog companding |
| **Acoustic Space** | Completely dry audio; no physical room boundaries; no environmental physics | Real room tone bed; early acoustic reflections; convolutional room impulse responses | Convolution reverb (`afir` or multi-tap `aecho`); continuous room tone bed mix (`amix`) |
| **Audio-Visual Mix** | Generic music blasted over dialogue without ducking | Dynamic sidechain ducking (-12dB attenuation during speech); locked Foley transients | `sidechaincompress` audio filtergraph; precise frame-locked Foley |

---

## 2. GitHub & Open-Source Tool Ecosystem

| Repository / Project | Primary Function | Command-Line Usage / Integration |
|---|---|---|
| **`openfilm/openfilm`** | Agentic multi-track video composition | Browser-based timeline preview and web-stack shot composition (`npx skills add openfilm/openfilm`) |
| **`FFmpeg` (Native Filtergraphs)** | Photochemical film emulation & mastering | Full-featured command-line filter graphs for halation, film grain, lens distortion, and LUFS mastering |
| **`sczhou/CodeFormer`** | High-fidelity face texture restoration | Restores realistic eye, iris, and teeth anatomy with `-w 0.9` fidelity lock |
| **`sczhou/ProPainter` / `SAM 2`** | Flow-guided object removal & inpainting | Dual-domain temporal inpainting to eliminate localized generative errors |
| **`Rikorose/DeepFilterNet`** | Real-time speech enhancement | Rust CLI (`deep-filter --pf --compensate-delay`) to strip synthetic noise beds |
| **`facebookresearch/demucs`** | Hybrid Transformer stem separation | Separates dialogue, music, and effects (`demucs --two-stems vocals -n htdemucs_ft`) |
| **`ggml-org/whisper.cpp`** | Local transcription & subtitle alignment | Generates accurate `.srt` subtitles (`whisper-cli -m models/ggml-base.en.bin -osrt`) |
| **`Breakthrough/PySceneDetect`** | Automated shot boundary detection | Isolates distinct cuts (`scenedetect -i input.mp4 detect-content split-video`) |

---

## 3. The 6-Stage Organic Transformation Engine

### Stage 1: Photochemical Color Science (Kodak 2383 Print Stock Emulation)
Real film print stock compresses dynamic range with a gentle S-curve: lifting deepest blacks to a rich dark navy/teal (toe) and rolling off highlights into warm cream (shoulder).

```bash
# Film S-Curve, Toe Lift, and Subtractive Desaturation
ffmpeg -i input.mp4 -vf "
  eq=contrast=1.03:brightness=0.01:saturation=0.94,
  curves=r='0/0.02 0.25/0.22 0.75/0.79 1/0.97':
         g='0/0.01 0.25/0.23 0.75/0.78 1/0.96':
         b='0/0.03 0.25/0.25 0.75/0.75 1/0.92'
" -c:v libx264 -crf 17 -preset slow -c:a copy output_graded.mp4
```

### Stage 2: Photochemical Halation Bloom
Light scattering across the back of the film emulsion causes bright red-orange halos around highlights:

```bash
# Isolate highlights >205 luma, blur, tint red/orange, and screen-blend back
ffmpeg -i input.mp4 -filter_complex "
  [0:v]split=2[base][glow];
  [glow]lutyuv=y='if(gt(val,205),val,0)':u=128:v=128[highlights];
  [highlights]gblur=sigma=22:steps=3[blurred];
  [blurred]colorbalance=rs=0.45:gs=-0.15:bs=-0.35[tinted];
  [base][tinted]blend=all_mode='screen':all_opacity=0.32[out]
" -map "[out]" -c:v libx264 -crf 17 -preset slow -c:a copy output_halation.mp4
```

### Stage 3: Organic 35mm Film Grain Synthesis
Physical film grain consists of random silver halide crystals suspended in gelatin. Unlike digital noise, grain is most visible in midtones and suppressed in deep shadows and bright highlights:

```bash
# Temporal and uniform grain with luminance compensation
ffmpeg -i input.mp4 -vf "
  noise=c0s=11:c0f=t+u:c1s=7:c1f=t+u:c2s=7:c2f=t+u,
  unsharp=3:3:0.4:3:3:0.0
" -c:v libx264 -crf 17 -preset slow -c:a copy output_grain.mp4
```

### Stage 4: Optical Lens Physics (Vignetting & Barrel Curvature)
Real anamorphic and spherical cinema lenses suffer from optical light falloff and gentle radial curvature:

```bash
# Natural optical vignette and subtle spherical barrel distortion
ffmpeg -i input.mp4 -vf "
  vignette=PI/4.5,
  lenscorrection=cx=0.5:cy=0.5:k1=-0.015:k2=0.005
" -c:v libx264 -crf 17 -preset slow -c:a copy output_optics.mp4
```

### Stage 5: Handheld Camera Micro-Drift (Inertia & Respiration)
AI video often has an unnatural, perfectly locked or mechanical sliding camera. Injecting low-frequency sinusoidal breathing restores physical human operation:

```bash
# 2D camera breathing drift: 12px amplitude on X (1.4 Hz), 8px amplitude on Y (1.1 Hz)
ffmpeg -i input.mp4 -vf "
  crop=in_w-32:in_h-32:(in_w-out_w)/2+10*sin(t*1.4)+5*sin(t*3.2):(in_h-out_h)/2+7*cos(t*1.1)+3*cos(t*2.8),
  scale=1280:720
" -c:v libx264 -crf 17 -preset slow -c:a copy output_handheld.mp4
```

### Stage 6: Acoustic Room Presence & Human Audio Warmth
Real rooms have continuous acoustic beds and physical reverberation boundaries. To eliminate sterile AI silence:

```bash
# Highpass 80Hz (sub rumble), Lowpass 14kHz (vocoder fizz), early reflection echo, -14 LUFS mastering
ffmpeg -i input.mp4 -af "
  highpass=f=80,lowpass=f=14000,
  aecho=0.8:0.88:25|45:0.25|0.12,
  loudnorm=I=-14:TP=-1.0:LRA=9
" -c:v copy -c:a aac -b:a 192k -ar 48000 output_acoustic.mp4
```

---

## 4. Google Flow & Veo Prompt Directing for Organic Realism

Preventing the AI sheen begins at prompt composition. Instruct Google Flow with specific camera lenses, photochemical stock references, and lighting dynamics:

```text
[Aesthetic & Medium]: Shot on 35mm Kodak Vision3 500T 5219 film, Cooke Anamorphic /i prime lenses. Natural photochemical texture, soft highlight halation bloom, authentic shadow detail.
[Subject & Performance]: Medium shot of an architect reviewing blueprints, subtle eye micro-movements, authentic skin pores with natural perspiration sheen, wearing an unpressed textured wool sweater.
[Lighting & Environment]: Late afternoon warm sun spilling through dust-mote industrial windows. Directional key light with 4:1 contrast ratio, natural specular reflections in both eyes, soft diffuse shadows.
[Camera Work]: Handheld 40mm camera with natural breathing cadence, gentle operator weight shifts, physical 180-degree shutter motion blur on hand gestures, widescreen horizontal framing.
```

---

## 5. Master AGYOS Video Integration Architecture

To execute a world-class production, connect all specialized skills across the project lifecycle:

```
[1. PRE-PRODUCTION]
    ├── scriptwriting-principles ────► 4-Act Retention, Craig Mazin Transformation, Natural Dialogue
    └── youtube-long-form-production ──► 0.5s Pre-Hook, 90s Open Loops, Strategic B-Roll Map

[2. GENERATIVE PRODUCTION]
    ├── google-flow / veo-3 ────────► Headless Generation with 35mm Lens & Lighting Prompts
    └── scripts/remove_flow_watermark.py ──► Delogo Inpainting for Corner Marks

[3. DEFECT AUDIT & REMEDIATION]
    ├── ai-video-detection-forensics ──► Audit Against 200 Forensic Principles
    ├── PySceneDetect ─────────────────► Segment Cuts into Distinct Shots
    └── ai-video-quality-enhancement ──► CodeFormer (Faces) + ProPainter (Masked Objects)

[4. ORGANIC DE-AI ENGINE]
    ├── scripts/organic_film_engine.py ──► Halation + 35mm Grain + Kodak 2383 S-Curve
    └── Handheld Drift + Optical Vignette ──► Elimination of Mechanical Slider Movement

[5. EDITORIAL & AUDIO MASTERING]
    ├── video-editing-principles ─────► Walter Murch Rule of Six, Motivated Cuts, L/J Audio Cuts
    ├── ffmpeg-video-editor ───────────► Sidechain Ducking (-12dB), Room Tone Bed Injection
    └── Final Delivery ────────────────► -14 LUFS / -1.0 dBTP YouTube Master
```
