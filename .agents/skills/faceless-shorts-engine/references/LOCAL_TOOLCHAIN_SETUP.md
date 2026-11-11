# Local toolchain notes

These notes are grounded in the supplied faceless-shorts README and scripts. Confirm the files
and flags in the toolkit currently selected; do not treat these source snapshots as a guarantee
that a machine is already configured.

## Runtime and first setup

The source README lists Node.js 22+, Python 3.10+, FFmpeg/ffprobe, and Google Chrome or compatible
Chromium. Its scripts/setup.sh creates a private environment under ~/.faceless-shorts/venv,
installs NumPy, SciPy, Kokoro ONNX, and faster-whisper, then downloads a Kokoro voice and Whisper
small.en model. The README estimates about 0.9 GB of first-use downloads. Confirm disk space,
network use, and the user's approval before running setup.

The render path is code-drawn scenes in a local browser, frame capture through
tools/capture.mjs, audio mixing, and FFmpeg encoding. Do not describe this bundle as Remotion,
cloud rendering, or fully offline before first setup.

## Source-backed commands

From the toolkit root:

    bash scripts/setup.sh
    bash scripts/selftest.sh
    bash scripts/new_video.sh --list
    bash scripts/new_video.sh deep-dive my-short

selftest.sh renders samples and writes review media. Run it only when the user asked for
verification or approved the resulting local files and compute use.

After replacing the example with the confirmed toolkit directory, run package-level voice tools
through its launcher and pass the generated project path:

    KIT_ROOT=/path/to/faceless-shorts
    PROJECT="$HOME/faceless-shorts/my-short"
    "$KIT_ROOT/scripts/py" "$KIT_ROOT/scripts/voice.py" --list
    "$KIT_ROOT/scripts/py" "$KIT_ROOT/scripts/voice.py" "$PROJECT"
    "$KIT_ROOT/scripts/py" "$KIT_ROOT/scripts/words.py" "$PROJECT"

For a user's recording, pass its path to words.py with --audio. Run the project-level steps below
from the generated project directory:

    cd "$PROJECT"
    node tools/capture.mjs check
    node tools/capture.mjs cues
    "$KIT_ROOT/scripts/py" tools/mix.py .
    node tools/capture.mjs sheet review/all.jpg 0.5 10
    node tools/capture.mjs video renders/my-short.mp4

Check each program's current help and project layout first. Keep model caches, venvs, generated
audio, and rendered videos in their documented locations; do not place them in AGYOS source files.

## Model and audio behavior

- The supplied voice tool exposes supported voices through voice.py --list; use that result
  instead of copying voice IDs from another toolkit or an older guide.
- The supplied word-timing tool uses Whisper small.en. For generated narration it can estimate
  word intervals from line timing if Whisper cannot load. For a user's recording it reports an
  error if transcription fails; do not silently substitute estimated timing.
- The capture tool defaults to 30 fps, with its frame rate configurable in the source. Confirm the
  final file rather than assuming a requested frame rate was achieved.
- The capture tool reports when a render has no mixed audio. Treat that as a failed deliverable
  until audio is mixed and verified.

The package README describes its assets as locally run and free for use in videos. This does not
mean setup has no bandwidth, storage, compute, or electricity cost.
