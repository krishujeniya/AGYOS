---
name: prompt-optimizer
description: Analyze a draft prompt for intent, constraints, and missing context, then return a ready-to-use revision with a concise diagnosis. Advisory only; does not execute the drafted task. Use for requests to optimize, improve, or rewrite prompts, including 优化prompt, 改进prompt, 怎么写prompt, or 帮我优化这个指令; not for code or performance optimization.
metadata:
  origin: community
  author: YannJY02
  version: "1.0.0"
---
# Prompt Optimizer

Analyze a draft prompt for intent, constraints, and missing context, then return a ready-to-use revision with a concise diagnosis. Advisory only; does not execute the drafted task. Use for requests to optimize, improve, or rewrite prompts, including 优化prompt, 改进prompt, 怎么写prompt, or 帮我优化这个指令; not for code or performance optimization.

## Workflow

1. Identify the requested outcome, audience, context, constraints, and output format.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Preserve the user's intent and ask only when a missing detail blocks a useful prompt.
4. Return revised prompt text and a short diagnosis when useful. This skill does not execute the drafted prompt.
5. Keep AGYOS as the default identity in AGYOS-authored prompts. Retain third-party names only for compatibility, attribution, or evidence.
6. Follow current project rules; a prompt template does not grant permission for external, paid, or destructive actions.
