---
name: web-fuzzing-ffuf
description: "Run scoped web-content discovery with ffuf for an owned or explicitly authorized target. Use only with a written target list, permitted test window, and agreed request limits."
risk: safe
source: https://github.com/jthack/ffuf_claude_skill
date_added: '2026-02-27'
---

# Authorized ffuf testing

Use ffuf only for a system the user owns or has explicitly authorized for testing. A domain name in a prompt is not proof of authorization.

## Before any network request

1. Confirm written scope: exact hosts and paths, excluded systems, allowed methods, test window, request-rate limit, and stop contact.
2. Confirm the user explicitly authorized this scan and that the target resolves to the approved environment. Do not scan third-party or production targets by inference.
3. Check that `ffuf` and the selected wordlist are installed; inspect `ffuf -h` for the installed version. Do not install tools or download wordlists without approval.
4. Prepare the command for review with the explicit target and rate constraints. Do not add recursive, subdomain, authentication, or destructive probes unless those are in scope.
5. Stop on elevated errors, unexpected load, rate-limit responses, or any request outside the approved target list.

## Report

Record the exact command, target, time window, tool version, wordlist source, and output file location. Redact tokens and personal data. Separate observed responses from interpretations; do not claim a vulnerability without validating the evidence.

See the [upstream ffuf skill](https://github.com/jthack/ffuf_claude_skill) and the official ffuf documentation for current options. Never treat this runbook as authorization to scan.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
