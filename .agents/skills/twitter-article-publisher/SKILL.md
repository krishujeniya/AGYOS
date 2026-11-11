---
name: twitter-article-publisher
description: "Prepare a Markdown article for X Articles and save a reviewed browser draft. Use when the publishing extension is available; obtain separate explicit approval before any public post."
risk: safe
source: https://github.com/wshuyi/x-article-publisher-skill
date_added: '2026-02-27'
---

# X Articles draft preparation

The upstream extension converts a Markdown article for the X Articles editor and saves a draft. It uses browser automation; availability and behavior depend on the installed host tools.

## Workflow

1. Confirm the exact article file, destination account, and whether the user asked for a local draft or an external draft.
2. Confirm the account has X Premium Plus, which the upstream guide lists as a prerequisite for Articles. If the account cannot open the Articles editor, stop external work and prepare a local Markdown/HTML draft instead.
3. Inspect the Markdown and referenced media locally. Do not change the source article unless asked. Verify links, images, table/Mermaid rendering, and any personal or confidential content.
4. Check that the publishing extension and browser tool are installed and authenticated. Do not ask for or display credentials; do not install browser tooling without authorization.
5. Show the converted article and media placement for review before saving an external draft. Saving a draft is an external account action and requires the user's request.
6. The upstream workflow says it saves a draft and does not auto-publish. Never publish or share publicly without separate explicit approval immediately before the action.
7. Verify the resulting draft status in the editor and report the exact outcome. If browser automation is unavailable, prepare a local Markdown/HTML draft instead.

See the current [X Article Publisher source](https://github.com/wshuyi/x-article-publisher-skill) for supported formatting and prerequisites.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
