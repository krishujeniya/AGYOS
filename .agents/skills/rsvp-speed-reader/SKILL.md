---
name: rsvp-speed-reader
description: Present text in a word-by-word reading view with adjustable speed, pause controls, and readable typography.
---
s prior response into a word-by-word reading view.
- You need a quick reading aid rather than a document transformation or summary.

## Instructions

1. **Get the text:**
   - If `$ARGUMENTS` is provided, use that text
   - Otherwise, extract the main content from your **previous response** in this conversation

2. **Prepare the content:**
   - Strip markdown formatting (headers, bold, links, code blocks)
   - Keep clean, readable prose
   - Escape quotes and backslashes for JavaScript

3. **Write and launch:**
   - Read `~/.claude/skills/speed/data/reader.html`
   - Replace `<!-- CONTENT_PLACEHOLDER -->` with:
     ```html
     <script>window.SPEED_READER_CONTENT = "your escaped text";</script>
     <!-- CONTENT_PLACEHOLDER -->
     ```
   - Run: `open ~/.claude/skills/speed/data/reader.html`

4. **Confirm:** Tell the user it's opening. Mention `Space` to play/pause.

## Arguments
$ARGUMENTS

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
