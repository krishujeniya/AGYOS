# Talking-head edit workflow

This is an operating map for the separately supplied ai-video-editor toolkit. Confirm commands
against its current --help output and source before use. Its project files are generated in a
dedicated work directory; keep the original clip unchanged.

## Setup and cost boundary

The source README lists Python 3.9+, FFmpeg/ffprobe, faster-whisper, Playwright, NumPy, Pillow, and
headless Chromium. It estimates about 150 MB for Chromium and 0.5–1.6 GB for first-use Whisper
weights. These are estimates from the supplied README, not measured values for the current machine.

Do not run scripts/setup.py in install mode without the user's approval. Its source installs into
the active Python interpreter and retries with --break-system-packages after a pip failure. Prefer
an isolated virtual environment at a user-approved location. Ask before installing software,
downloading models, or using system package managers. The toolkit uses local processing; "no paid
API" does not mean no bandwidth, storage, compute, or electricity use.

## Transcript, cut plan, and render

Set KIT_ROOT to the confirmed toolkit directory, VIDEO to the input clip, and WORK to a new,
non-existing output directory. For the supplied bundle at its provided location, use the path below;
change it only if the toolkit was confirmed elsewhere. The prompts collect the clip and new work
directory paths; verify the clip exists and the work directory does not before continuing. For a
known English recording, select English explicitly; use auto when language is uncertain. The source
code's model choice depends on language and detected CUDA, so tell the user when a large first
download or slow CPU run is likely.

    KIT_ROOT="/home/ai/Downloads/ai-video-editor"
    read -r -p 'Input clip path: ' VIDEO
    read -r -p 'New, non-existing work directory path: ' WORK
    read -r -p 'Transcription language (en, hi, or auto): ' TRANSCRIBE_LANG
    python3 "$KIT_ROOT/scripts/setup.py" --check
    python3 "$KIT_ROOT/scripts/transcribe.py" "$VIDEO" --lang "$TRANSCRIBE_LANG" --work "$WORK"
    python3 "$KIT_ROOT/scripts/cut.py" "$WORK" --dry-run --style warm-canvas --captions no

Review transcript.txt and transcript.json, including low-confidence words marked by the tool.
Correct recognition errors and listen to the original audio around every proposed content cut.
If considering a retake or false-start removal, write edits.json with inclusive word indexes and a
reason. Similar wording alone does not prove a line is a retake; the later take may change meaning.
The cut script's --dry-run still writes cut_plan.json and edit.json. Use only the new WORK directory
and tell the user these planning files will be created.

After approval, repeat the cut command with the same options and remove --dry-run:

    python3 "$KIT_ROOT/scripts/cut.py" "$WORK" --style warm-canvas --captions no

If WORK/edits.json contains the approved mistake ranges, cut.py reads it by default. This writes
cut.mp4 and updated transcripts; it can replace files with those names, so keep WORK new and do not
reuse an existing project. Re-read transcript_edited.txt and transcript_edited.json before timing
graphics.

Write story.js from the toolkit's story guide and the selected style's source helpers. Keep each
graphics span aligned to the edited transcript times. Use the preview/check tools before the final
render:

    python3 "$KIT_ROOT/scripts/render.py" "$WORK" --check
    python3 "$KIT_ROOT/scripts/render.py" "$WORK" --stills auto
    python3 "$KIT_ROOT/scripts/render.py" "$WORK" --out "$WORK/final-reviewed.mp4"

The --check command also writes page.html in WORK and serves the local preview while it runs; the
stills command writes its contact sheet. Open the generated contact sheet and inspect representative
full-size frames. Confirm the final file contains audible speech and that the chosen caption,
graphics, and crop settings match the approved plan. Use a fresh output name if it already exists.

## Source limits

The source skill documents 16:9 output. Its cut script center-crops non-16:9 input to 16:9; do not
promise native vertical or square editing. The source package supports one continuous recording
per edit. Do not join clips or change aspect ratio without a separate, reviewed plan.
