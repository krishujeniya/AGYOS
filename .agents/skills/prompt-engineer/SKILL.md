---
name: prompt-engineer
description: "Transforms user requests into clear prompts using optional task-fit structures, examples, and output contracts."
category: automation
risk: safe
source: community
tags: "[prompt-engineering, optimization, frameworks, ai-enhancement]"
date_added: "2026-02-27"
---

# Prompt Engineer

Use this skill to turn a user's request into a clear prompt for the intended task. Follow `.agents/rules/agyos-prompt-principles.md`.

## Workflow

1. Identify the desired result, audience, context, constraints, and output shape from the user's request.
2. Preserve the user's intent and language. Ask a concise question only when a missing detail would materially change the prompt.
3. Write the shortest prompt that states the required outcome and boundaries.
4. Add examples, a role, ordered stages, or a schema only when they address a real ambiguity or repeatable need.
5. For multi-stage work, list deliverables and observable completion checks. Do not ask for hidden reasoning or private traces.
6. Return the prompt in the user's requested format. State important assumptions when they affect use.

## Optional structures

Use fields such as `Goal`, `Context`, `Constraints`, and `Output` when they make the task easier to follow. Named frameworks are optional memory aids, not required steps or guarantees of quality. Do not combine frameworks by default.

## Review

- Confirm that every instruction supports the requested task.
- Remove invented facts, irrelevant persona details, repeated constraints, and unsupported performance claims.
- Keep AGYOS as the default identity in AGYOS-authored prompts. Retain a third-party name only for compatibility, attribution, or evidence.
- For repeated use, evaluate the prompt on representative cases against explicit task-specific criteria.
