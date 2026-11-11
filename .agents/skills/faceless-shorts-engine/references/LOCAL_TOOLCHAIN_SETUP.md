# Local Faceless Video Toolchain Setup

Technical reference for configuring and executing the zero-cost local video generation stack without paid API subscriptions or external cloud dependencies.

---

## 1. System Requirements & Dependency Architecture

The pipeline requires three core local runtime components:
- **Python 3.10+**: Orchestration, script writing, speech synthesis, and subtitle alignment.
- **Node.js 18+ & npm/pnpm**: Remotion composition engine and React animation templates.
- **FFmpeg 5.0+**: Hardware-accelerated encoding (`h264_nvenc` or `libx264`), audio normalisation, and filter graph compositing.

### Verification Commands
```bash
python3 --version
node --version
ffmpeg -version | head -n 1
```

---

## 2. Speech Synthesis: Offline Kokoro TTS

Kokoro is an open-weights, high-fidelity neural text-to-speech model providing studio-grade generation at zero runtime cost.

### Installation via uv or pip
```bash
pip install kokoro-onnx soundfile
# or via uv:
uv pip install kokoro-onnx soundfile
```

### Voice Profiles & Genre Mapping
| Voice ID | Gender / Accent | Vocal Tone | Recommended Short Style |
|---|---|---|---|
| `am_adam` | American Male | High energy, crisp, engaging | Tall Tale 3D, Stick Story |
| `am_michael` | American Male | Deep, resonant, grave | Night File 3D |
| `af_bella` | American Female | Articulate, warm, dynamic | Deep Dive 3D, Inside Out |
| `af_nicole` | American Female | Professional, authoritative | General Explainer |
| `bm_george` | British Male | Classic documentary cadence | Paper Atlas |

### Python Generation Script
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
sf.write("output_voice.wav", samples, sample_rate)
```

---

## 3. Subtitle Alignment: Word-Level Whisper

To generate kinetic, word-synced subtitles with active word highlights, use local Whisper models via `faster-whisper`.

### Installation
```bash
pip install faster-whisper
```

### Word Timestamp Extraction
```python
import json
from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu", compute_type="int8")
segments, info = model.transcribe("output_voice.wav", word_timestamps=True)

words_data = []
for segment in segments:
    for word in segment.words:
        words_data.append({
            "word": word.word.strip().upper(),
            "start": round(word.start, 3),
            "end": round(word.end, 3),
            "probability": round(word.probability, 3)
        })

with open("captions_word_level.json", "w") as f:
    json.dump(words_data, f, indent=2)
```

### Subtitle Visual Formatting
- **Position**: Centered horizontally, vertical position at `Y = 65%` to `70%` (clears TikTok/Reels UI buttons).
- **Typography**: Heavy geometric sans-serif (e.g. Montserrat Black, Arial Black, The Bold Font).
- **Active Word Accent**: Highlight active word with `#FFE500` (Safety Yellow) or `#00FF66` (Signal Green) while surrounding words render in white (`#FFFFFF`) with a 3px black stroke.

---

## 4. Video Assembly & Audio Ducking via FFmpeg

When not rendering through Remotion, pure FFmpeg can assemble speech, background music, sound effects, and video layers:

### Sidechain Audio Ducking
Ducks background music by -18dB whenever speech audio is active:
```bash
ffmpeg -i speech.wav -i music.mp3 -filter_complex \
"[1:a]volume=0.15[music]; \
 [0:a][music]amix=inputs=2:duration=first:dropout_transition=2[outa]" \
-map "[outa]" -c:a aac -b:a 192k mixed_audio.aac
```

### Video Rendering Specification
- **Resolution**: 1080 x 1920 (9:16 vertical).
- **Frame Rate**: 30 fps (standard) or 60 fps (fluid motion).
- **Video Bitrate**: 12–16 Mbps CBR/VBR, high profile.
- **Color Primaries**: BT.709, YUV420p pixel format for universal mobile playback.
