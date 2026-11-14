---
name: faceless-shorts-engine
description: >-
  Use when someone wants an original, code-rendered faceless vertical short with narration,
  word-timed captions, and animated scenes, or asks for one of the six styles in the supplied
  faceless-shorts toolkit.
metadata:
  version: 1.1.0
  tier: 1
  domain: video
  origin: user-supplied faceless-shorts toolkit and AGYOS workflow
---

# Faceless Shorts Engine

Use the source toolkit when it is available. This skill contains planning guidance and a manifest
scaffolder; it does not itself render video. The supplied renderer is JavaScript/Canvas in headless
Chrome plus FFmpeg. It is not Remotion.

## Find the toolkit and check the requested work

1. Check `tools/video/faceless-shorts` first, then the user-provided location, current project,
   and skill folder for scripts/new_video.sh and styles/. Confirm the root also has
   scripts/voice.py and scripts/words.py. Set KIT_ROOT to that root. If absent, offer a
   script/shot plan; do
   not claim to have rendered a video or invent toolkit paths.
2. Reuse details already provided. Ask together only for missing choices that change the result:
   topic or source script, duration, style, voice, recorded narration versus local TTS, captions,
   and music. Defaults from the source skill are about 30 seconds, am_michael, local TTS, and
   the existing style example. Confirm before installing packages, creating a model environment,
   downloading model weights, or using a paid service.
3. For factual subjects, gather reliable sources and attach them to the script's sources field.
   Keep health, safety, crime, and historical claims proportionate to evidence. If a fact cannot be
   verified, omit it or label the uncertainty. Never invent quotes, statistics, or evidence.

## Plan before rendering

Show a compact plan with narration, source list, line/cut timing, selected style, shot descriptions,
caption treatment, music, and any assumptions. Wait for approval before building unless the user's
current or prior instruction already authorized the build. Ask only for missing information that
changes the result. Keep narration natural and continuous. The toolkit suggests roughly 90–110
words for 35 seconds, but the generated audio duration is authoritative. A seamless loop is
optional and must not distort the ending.

Choose among the six styles in
[the style reference](references/ANIMATION_STYLES_MANUAL.md). Read the selected toolkit
styles/<id>/STYLE.md and inspect its example before changing shots.js. The six short styles
are distinct from the seven Nafay 3D motion-graphics presets described in
[the provenance note](references/SOURCE_PROVENANCE.md).

## Build with the supplied toolkit

First inspect its README and setup script. The supplied package documents Node.js 22+, Python 3.10+,
FFmpeg/ffprobe, Chrome or Chromium, and a first setup that creates an environment and downloads
roughly 0.9 GB of voice and transcription models. These are source-package notes, not guarantees
about the current machine. Do not install or download without user authorization.

Use the toolkit's own voice list; do not assume a voice ID from an older runbook:

    "$KIT_ROOT/scripts/py" "$KIT_ROOT/scripts/voice.py" --list

For an approved project:

1. Create a fresh project with the toolkit's new_video.sh, using a valid style ID and a new
   short name. Use the path it prints as PROJECT; never overwrite an existing project.
2. Write script.json and src/shots.js from the reviewed plan. Keep each line natural to speak;
   align visual changes to meaning and words rather than a fixed reset interval.
3. Generate local narration with the toolkit's voice.py and PROJECT, or align a user's recording
   with words.py using PROJECT and the recording path. Then inspect data/words.txt; correct
   misheard or missing words before animation. The generated-voice path can fall back to estimated
   word timing if Whisper is unavailable; a supplied recording requires successful transcription.
4. From PROJECT, run node tools/capture.mjs check. Continue only on CHECK OK; generate cues and
   mix audio using the project tools.
5. Render a timestamped contact sheet and inspect it, then inspect key frames at full size.
   Check narration-to-image timing, readable captions, safe margins, collisions, continuity, and
   whether the chosen style rules hold. Fix issues and repeat the visual review before final render.
6. Render the requested range. Confirm the output exists, has the expected duration and video
   dimensions, and contains audible speech/music before reporting completion. The renderer can
   explicitly report SILENT when no mixed audio file exists.

The toolkit is local after setup, but setup requires network access to fetch models. Do not call
paid APIs, upload footage, publish, or share generated files unless the user separately requests
that action and authorizes its destination.

## Limits and handoff

- Use the toolkit's actual style IDs, voice list, flags, and output paths; check --help or source
  before relying on a command detail.
- scripts/generate_shorts_manifest.py only writes a planning JSON scaffold. It does not create
  narration, animation, or an MP4.
- Keep the original source package's README, attribution, and third-party notices with any copy.
- Report what was rendered and inspected separately from facts that were only planned. Never call a
  source prompt, model, or style tested unless it was actually run.

For setup details see [Local toolchain](references/LOCAL_TOOLCHAIN_SETUP.md); for writing and
pacing see [Script and timing guidance](references/RETENTION_AND_SCRIPTING_PLAYBOOK.md).
