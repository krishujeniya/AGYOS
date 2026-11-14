---
name: ai-video-editor
description: >-
  Use when someone provides a local talking-head recording and wants transcript-guided pause or
  retake cuts, optional captions, or code-drawn motion graphics rendered into an edited video.
metadata:
  version: 1.0.0
  tier: 2
  domain: video
  origin: user-supplied ai-video-editor toolkit
---

# Local Talking-Head Video Editor

Use this for editing an existing recording. It is separate from generated-scene tools, faceless
shorts, filming advice, and long-video-to-short clipping.

## Locate the actual toolkit

The repository copy is `tools/video/ai-video-editor`. Confirm it contains
scripts/transcribe.py, scripts/cut.py, scripts/render.py, engine/player.js, and styles/index.json,
then set KIT_ROOT to that path. A user-provided alternate root is also valid. The AGYOS skill does
not include or duplicate the renderer. If no toolkit is present, stop at an edit plan and ask for
its location; do not invent script paths or claim an export.

Use a new, user-approved work directory separate from the source clip. Pass it with transcribe.py's
--work option so generated files do not land beside the original recording. Never overwrite an
existing work directory or source file.

## Intake and edit plan

Reuse information the user already gave. Ask together only for choices that affect the edit:
language, pause-cut preference, whether to consider retakes, caption preference and writing system,
style, graphics density, and whether they want to review the cut and graphics plans. Probe the
source dimensions and show the crop consequence before editing any non-16:9 clip; the toolkit
center-crops it to 16:9.

Defaults from the supplied toolkit are natural pauses retained, obvious silence removed, no captions,
light graphics, and Warm Canvas for talking-head footage. Treat those as editable defaults. Preserve
the speaker's meaning, sequence, and authentic delivery. Do not remove an ambiguous phrase, rewrite
the narration, or infer a retake without review.

Before cutting spoken content, show the proposed mistake-cut list with timestamps, transcript text,
and reason. Before writing graphics, show the beat list and any visible claims or numbers. Wait for
approval unless the user has already authorized those specific edits. Do not render a full video
from a storyboard alone.

## Build and review

Follow [the toolkit workflow](references/TOOLKIT_WORKFLOW.md). Correct the transcript before
planning graphics. Read the selected style's style.md, base.js, and example; use
[the seven-style map and provenance notes](references/STYLES_AND_PROVENANCE.md).

Run the toolkit's cut preview before applying removals. After writing story.js, run render.py
--check and create a contact sheet with render.py --stills auto. Listen to the original audio around
each proposed spoken-content removal and verify low-confidence transcript words. Inspect the whole
sheet and full-size frames for word timing, transcript fidelity, legibility, speaker framing, overlaps,
misleading graphics, and style consistency. Fix and inspect again before final rendering.

Check the exported file's actual duration, dimensions, frame rate, and audio. Report the output path
and what was checked. Distinguish a command completing from a human visual review. Do not upload,
publish, or send the video elsewhere unless separately requested and authorized.
