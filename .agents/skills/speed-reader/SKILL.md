---
name: speed-reader
description: "Present a Claude Code response in a rapid serial visual presentation reader with an ORP highlight. Use only when the skill is installed in Claude Code on macOS and the user wants that display."
risk: safe
source: "https://github.com/SeanZoR/claude-speed-reader"
date_added: "2026-02-27"
---

# Speed reader

Use this skill only when the upstream speed-reader skill is installed in Claude Code on macOS and the user asks to view text in its RSVP reader. The upstream launcher uses macOS `open`; this catalog entry does not install or provide that skill.

## Workflow

1. Confirm that Claude Code is running on macOS and the speed-reader skill is installed. If either prerequisite is missing, provide the text normally.
2. Send only the response or custom text the user asked to read. Do not forward private or unrelated conversation content.
3. Use the installed reader's documented controls: Space toggles playback, Left/Right changes speed, R restarts, and V replaces the text. Confirm these against the installed version if controls differ.
4. Stop playback when requested and return to the normal response view.

The upstream project describes a rapid serial visual presentation (RSVP) interface with an optimal recognition point (ORP) highlight. Its advertised words-per-minute figure is not a measured reading-speed guarantee. See the [source project](https://github.com/SeanZoR/claude-speed-reader).

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
