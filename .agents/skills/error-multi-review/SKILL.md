---
name: error-multi-review
description: "Review a reproducible software error from independent code, test, and operational perspectives. Use when a defect crosses modules or needs a structured root-cause review."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Multi-perspective error review

This skill organizes a defect review; it does not provide a multi-agent orchestration executable.

## Workflow

1. Capture the exact error, triggering command or request, expected result, observed result, environment, and a minimal reproduction. Redact secrets and personal data.
2. Reproduce the error without overwriting user data. If reproduction is unsafe or unavailable, label the finding unconfirmed and state the limitation.
3. Trace the failing path backward through inputs, state changes, callers, and external boundaries. Read the relevant tests and recent diff.
4. Review the evidence through separate lenses: root cause and code path, regression and edge cases, and configuration or operational conditions. If independent reviewers are available and authorized, give each a non-overlapping read-only scope; otherwise perform the reviews sequentially.
5. Record findings with file and line evidence, impact, confidence, and a proposed regression check. Separate confirmed causes from plausible causes.
6. Implement a fix only if requested and within scope. Add a regression test before changing behavior, then run that test and relevant suite.

## Output

Provide the reproduction, confirmed or unresolved cause, evidence from each review lens, regression coverage, checks run, and remaining unknowns. Do not claim a fix or all-clear from review alone.
