---
name: ai-video-quality-enhancement
description: >-
  Master reference and CLI toolkit for repairing AI-generated video defects (Google Flow & Veo 2026).
  Maps 200 forensic detection principles to actionable restoration pipelines using FFmpeg,
  CodeFormer, Real-ESRGAN, Video2X, ProPainter, DeepFilterNet, Demucs, whisper.cpp, PySceneDetect,
  VapourSynth, VidStab, and VMAF. Includes generation-time prompt engineering for Google Flow studio.
metadata:
  version: 1.0.0
  license: MIT
---

# AI Video Quality Enhancement & Repair Toolkit (2026 Reference)

A production-grade engineering runbook for diagnosing and repairing visual, temporal, physical, anatomical, and acoustic defects in AI-generated video media (specifically Google Flow and Veo), using a hybrid workflow of generation-time prompting and Linux CLI tools.

---

## 1. Operating Invariants & Philosophy

### A. Quality Enhancement vs. Provenance Alteration
- **Target Objective**: Improve visual fidelity, temporal stability, anatomical accuracy, physics plausibility, and audio clarity.
- **Out-of-Scope**: Circumventing cryptographic provenance (C2PA), attempting to strip Google DeepMind SynthID neural watermarks, or falsifying camera sensor authenticity. SynthID operates within latent diffusion tensors and cannot be stripped by post-processing without destroying signal integrity. Always declare synthetic media in compliance with platform guidelines (e.g. YouTube Altered Content).

### B. Regeneration vs. Post-Processing Decision Rule
- **The Filter Limit**: No post-processing CLI filter can construct non-existent hand anatomy, resolve impossible room geometry, or fabricate authentic human expression transitions.
- **Decision Hierarchy**:
  1. *Major Structural Defects* (extra limbs, morphing faces, impossible physics): **Regenerate in Google Flow** using consistent reference frames and targeted editing prompts.
  2. *Localized Artifacts & Text Errors*: **Mask and inpaint** using ProPainter or composite graphic overlays.
  3. *Global Technical Defects* (luminance flicker, camera jitter, color banding, noisy audio): **Filter programmatically** via FFmpeg, VidStab, and DeepFilterNet.

### C. The Temporal Inconsistency Penalty
Frame-by-frame enhancements (e.g. naive static image upscaling or per-frame face sharpening) introduce temporal boiling, shimmering edges, and phase chatter across adjacent frames. All CLI pipelines in this toolkit use temporal windowing, optical flow guidance, or multi-frame propagation.

---

## 2. Core CLI Toolkit Index

| Tool | Primary Function | Execution Context | Key Advantage |
|---|---|---|---|
| **FFmpeg + FFprobe** | Filtering, remuxing, deflicker, deband, loudness | Linux CPU / NVENC | Industry foundation; zero quality loss on copy remuxing |
| **VidStab (FFmpeg)** | Two-pass camera stabilization | Linux CLI | Eliminates irregular generative camera wobble |
| **CodeFormer** | Face detail restoration | Python / PyTorch (GPU) | Adjustable fidelity parameter (`-w`) prevents identity drift |
| **Real-ESRGAN / Video2X** | Super-resolution video upscaling | Vulkan / PyTorch | Temporal video models minimize frame flickering |
| **ProPainter / SAM 2** | Dual-domain flow-guided video inpainting | Python / PyTorch (CUDA) | Fills masked regions using optical flow propagation |
| **DeepFilterNet 3** | Deep-learning speech enhancement | Rust CLI (`deep-filter`) | Low-latency, full-band (48kHz) speech denoising |
| **Demucs (v4)** | Music & speech stem separation | Python / PyTorch | Isolate clean dialogue from muddy generative music |
| **whisper.cpp** | Speech-to-text subtitle generation | C/C++ CLI | Fast, local execution generating synchronized `.srt` tracks |
| **PySceneDetect** | Automated cut and shot boundary detection | Python CLI | Isolates damaged generative shots for targeted triage |
| **VMAF (libvmaf)** | Objective perceptual video quality scoring | FFmpeg Filter | Measures structural degradation against source references |

---

## 3. Mapping: 200 Forensic Principles to Remediation Strategies

This matrix pairs the 11 defect categories from `ai-video-detection-forensics` with verified repair methods.

### Category 1: Watermarks and Provenance (Principles 1–20)
- **Principle Focus**: File custody, digital origin, manifest records.
- **Improvement Strategy**: Maintain untouched archive copies. Store source files with SHA-256 hashes. For visible corner indicator marks, apply spatial inpainting via `scripts/remove_flow_watermark.py`. Preserve C2PA metadata integrity through `c2patool`.

### Category 2: File Metadata and Encoding (Principles 21–35)
- **Principle Focus**: Container atoms, variable frame rates, missing stream headers.
- **Improvement Strategy**: Remux container to constant frame rate (CFR), standardize color tags (`bt709`), and clean container comments.
  ```bash
  ffmpeg -i input.mp4 -r 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:v libx264 -crf 17 -preset slow -c:a aac -b:a 192k -movflags +faststart output_clean.mp4
  ```

### Category 3: Temporal Consistency and Flickering (Principles 36–55)
- **Principle Focus**: Brightness oscillation, edge buzzing, object morphing.
- **Improvement Strategy**:
  1. *Luminance Deflicker*: Apply moving-average luminance stabilization (`deflicker=size=5:mode=am`).
  2. *Camera Wobble*: Run two-pass VidStab (`vidstabdetect` then `vidstabtransform`).
  3. *Persistent Morphing*: Isolate shot via PySceneDetect and regenerate in Google Flow with reference frames.

### Category 4: Faces, Eyes, Expressions, and Speech (Principles 56–75)
- **Principle Focus**: Asymmetrical pupils, teeth distortion, unnatural blinks, plastic skin.
- **Improvement Strategy**:
  1. *Face Restoration*: Run CodeFormer with high fidelity (`-w 0.8` to `1.0`) to restore iris boundaries and teeth without replacing character likeness:
     ```bash
     python inference_codeformer.py -i input_shot.mp4 -w 0.9 --bg_upsampler realesrgan --face_upsample --save_video_fps 24
     ```
  2. *Severe Eye/Lip Deformity*: Regenerate in Flow using high-resolution facial reference images.

### Category 5: Hands, Body, and Clothing (Principles 76–95)
- **Principle Focus**: Fused fingers, incorrect joints, changing cloth patterns, gliding feet.
- **Improvement Strategy**:
  1. *Anatomy Failure*: Generative post-filters cannot re-sculpt human anatomy. Re-prompt in Flow with explicit anatomy constraints: `"anatomically correct hands, 5 distinct fingers, static clothing texture"`.
  2. *Localized Inpainting*: For single malformed frames, export PNG sequence, patch in photo editor, and re-insert.

### Category 6: Objects, Backgrounds, and Text (Principles 96–115)
- **Principle Focus**: Gibberish lettering, drifting room walls, melting furniture.
- **Improvement Strategy**:
  1. *Text / Logos*: Composite vector typography over moving footage using motion tracking (Blender or After Effects).
  2. *Background Inpainting*: Track background region with SAM 2 and run ProPainter:
     ```bash
     python inference_propainter.py --video input.mp4 --mask masks/ --fp16
     ```

### Category 7: Physics, Motion, and Interactions (Principles 116–135)
- **Principle Focus**: Floating objects, reverse gravity, impossible collisions, missing shadows.
- **Improvement Strategy**:
  1. *Motion Re-timing*: Adjust speed curves with optical flow (`setpts`, `minterpolate`) to restore natural gravitational momentum.
  2. *Interaction Logic*: When collisions or liquid flows violate physics, regenerate the clip in Flow specifying mass and momentum.

### Category 8: Lighting, Optics, and Camera (Principles 136–150)
- **Principle Focus**: Inconsistent shadow angles, mismatched white balance, gradient color banding.
- **Improvement Strategy**:
  1. *Gradient Debanding*: Eliminate stepped color quantization:
     ```bash
     ffmpeg -i input.mp4 -vf "deband=1thr=0.02:2thr=0.02:3thr=0.02" -c:v libx264 -crf 17 -c:a copy output_deband.mp4
     ```
  2. *Color Matching*: Normalize contrast and saturation across shots using `eq` or 3D LUT tables.

### Category 9: Speech, Sound, and Synchronization (Principles 151–170)
- **Principle Focus**: Noisy dialogue, robotic vocoder whine, unsynced footsteps, muddy mix.
- **Improvement Strategy**:
  1. *Stem Extraction*: Separate voice and backing tracks using Demucs (`demucs --two-stems vocals input.mp4`).
  2. *Speech Denoising*: Pass isolated vocal track through DeepFilterNet:
     ```bash
     deep-filter --pf --compensate-delay input_vocals.wav -o clean_vocals/
     ```
  3. *Loudness Mastering*: Mix cleaned vocals over Foley/music and normalize to YouTube standard (-14 LUFS / -1.0 dBTP).

### Category 10: Scene Logic and Continuity (Principles 171–185)
- **Principle Focus**: Anachronisms, impossible geography, costume shifts across cuts.
- **Improvement Strategy**:
  1. *Editorial Trimming*: Cut out continuity error frames on action or reverse angles using Walter Murch's Rule of Six.
  2. *Character Consistency*: Bind all generation prompts to a single character reference asset in Google Flow.

### Category 11: Computational Artifacts (Principles 186–200)
- **Principle Focus**: High-frequency FFT noise, checkerboard upsampling patterns, low VMAF score.
- **Improvement Strategy**:
  1. *Super-Resolution*: Upscale with Video2X (Real-ESRGAN backend) to eliminate pixel-grid interpolation artifacts.
  2. *Quality Validation*: Measure VMAF score against reference frames to guarantee broadcast grade (>92 VMAF score).

---

## 4. Production Shell Recipes (Ubuntu 22.04 / 24.04 LTS)

### Recipe A: Full Visual Pre-Flight Pass (Stabilize, Deflicker, Deband)
This unified FFmpeg pipeline stabilizes handheld motion, removes brightness fluctuation, and smooths color banding in a single encoding generation:

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-input.mp4}"
OUTPUT="${2:-master_repaired.mp4}"

# Pass 1: Camera motion analysis
ffmpeg -i "${INPUT}" \
  -vf "vidstabdetect=stepsize=6:shakiness=5:accuracy=15:result=transforms.trf" \
  -f null -

# Pass 2: Stabilization + Deflicker + Deband + Mastering
ffmpeg -i "${INPUT}" \
  -vf "vidstabtransform=smoothing=25:input=transforms.trf:zoom=3:optzoom=1,deflicker=size=5:mode=am,deband=1thr=0.015:2thr=0.015:3thr=0.015,unsharp=5:5:0.5" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -c:a copy \
  -movflags +faststart \
  "${OUTPUT}"

rm -f transforms.trf
echo "Repaired video written to ${OUTPUT}"
```

### Recipe B: Audio Restoration Pipeline (Demucs + DeepFilterNet + Loudnorm)
Extracts audio from video, isolates vocals, strips synthetic background noise, and masters to broadcast loudness:

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-input.mp4}"
OUTPUT="${2:-final_mix.mp4}"

# 1. Extract 48kHz WAV
ffmpeg -i "${INPUT}" -vn -acodec pcm_s16le -ar 48000 raw_audio.wav

# 2. Separate vocal stem with Demucs
python3 -m demucs.separate -n htdemucs_ft --two-stems vocals raw_audio.wav

# 3. Clean vocal stem with DeepFilterNet
deep-filter --pf --compensate-delay separated/htdemucs_ft/raw_audio/vocals.wav -o cleaned_vocals/

# 4. Remux cleaned vocals and instrumental with loudness normalization (-14 LUFS)
ffmpeg -i "${INPUT}" \
  -i "cleaned_vocals/vocals.wav" \
  -i "separated/htdemucs_ft/raw_audio/no_vocals.wav" \
  -filter_complex "[1:a][2:a]amix=inputs=2:weights=1.2 0.7,loudnorm=I=-14:TP=-1.0:LRA=9[aout]" \
  -map 0:v:0 -map "[aout]" \
  -c:v copy \
  -c:a aac -b:a 256k -ar 48000 \
  "${OUTPUT}"

rm -rf raw_audio.wav separated cleaned_vocals
echo "Restored audio remuxed to ${OUTPUT}"
```

### Recipe C: Automated Shot Extraction with PySceneDetect
Splits a long generative clip into distinct shots to identify defective sections:

```bash
scenedetect -i input.mp4 \
  detect-content --threshold 27.0 \
  split-video --output shots/ \
  save-images --output shots/thumbnails/
```

---

## 5. Google Flow Generation-Time Defect Prevention

Preventing defects during generation produces cleaner results than post-processing recovery.

### A. The Anti-Hallucination Prompt Architecture
When composing video generation prompts in Google Flow studio, enforce physical and kinematic constraints:

```text
[Subject & Styling]: A cinematic medium close-up of a 35-year-old female mechanical engineer, steady focused gaze, natural subtle blinking, realistic skin pores without plastic smoothing, wearing a structured dark canvas work jacket.
[Setting & Lighting]: Industrial electronics lab, background soldering equipment stationary with rigid architectural lines. Directional 45-degree key light, natural specular catchlights in both pupils, soft shadow falloff on left cheek.
[Action & Motion]: She reaches right hand forward with 5 distinct fingers, grasping a steel caliper with natural thumb opposing grip, lifting it with realistic mass and momentum. Unbroken physical contact.
[Camera Work]: Subtle 35mm slider move to the left, 24fps widescreen horizontal framing, consistent depth of field, zero artificial warping or flickering.
```

### B. Iterative Refinement Prompt (Flow In-Studio Editor)
When modifying an existing clip in Flow's editor, use this defect-targeting refinement template:

```text
Refine this shot for high-end professional continuity and physical accuracy:
1. Maintain strict identity consistency for the central subject: preserve eye shape, facial bone structure, hair volume, and outfit details across all frames.
2. Correct hand and finger anatomy: ensure 5 anatomically proportioned fingers without blending or morphing during tool interaction.
3. Lock background geometry: prevent wall panels, windows, and technical machinery from drifting or breathing.
4. Stabilize illumination: eliminate sudden brightness flickering and maintain stationary shadow angles.
5. Preserve narrative pace: do not add extraneous characters or change the camera angle.
```

---

## 6. End-to-End 8-Stage Production Quality Workflow

Follow this sequence from raw generation to final release:

```
[01. INTAKE & HASH]
       │
       ▼
[02. PYSCENEDETECT AUDIT] ──► Inspect thumbnails & isolate defective shots
       │
       ▼
[03. DEFECT TRIAGE]
       ├──► Major geometry / limb defect ────► [04. FLOW REGENERATION]
       └──► Localized / global artifact ─────► [05. CLI RESTORATION]
                                                      │
                                                      ├── VidStab + Deflicker
                                                      ├── CodeFormer (Faces)
                                                      └── ProPainter (Masked Objects)
                                                      │
                                                      ▼
                                              [06. AUDIO MASTERING]
                                                      │ (Demucs + DeepFilterNet + LUFS)
                                                      ▼
                                              [07. VMAF & EYE VERIFICATION]
                                                      │ (Target: VMAF > 92)
                                                      ▼
                                              [08. MASTER DELIVERY & C2PA]
```

1. **Intake & Custody**: Record input SHA-256 and inspect stream metadata with `ffprobe`.
2. **Shot Segmentation**: Run PySceneDetect to isolate distinct cuts into `/shots`.
3. **Defect Triage**: Categorize each defect as structural (needs regeneration) or cosmetic (repaired via CLI).
4. **Flow Regeneration**: For deformed hands or morphing faces, re-run generation in Flow with tightened prompts and reference stills.
5. **CLI Technical Repair**: Apply Recipe A (VidStab, Deflicker, Deband) and CodeFormer/ProPainter as needed.
6. **Audio Mastering**: Clean dialogue via Demucs + DeepFilterNet and normalize to -14 LUFS.
7. **Quality Audit**: Compute VMAF against original frames to confirm no compression artifacts were introduced. Verify with human eye review.
8. **Master Packaging**: Remux with `-map_metadata -1`, standard H.264 high-profile tags, and document generation history in C2PA credentials.
