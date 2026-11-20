# Policy Guard Hook Rules

## Scope

- Hooks run static inspection only; heavy verification stays in GitHub Actions per the zero-local-builds invariant.
- All Python invocation goes through uv (`uv run`); bare `python` and `pip` are rejected.
- Writes outside `.agents/` and `scripts/` are blocked at PreToolUse.

## Gate enforcement

- Merge-class tool calls require the `gate:legal-cleared` label, which is granted only by an accepted license-clearance handoff (see rules/agyos-gate-legal-clearance.toon).
- PostToolUse lints every written `.toon` file against the blob-envelope schema and runs `git diff --check` on touched files.

## Stop summary

- The Stop hook prints the static verification summary (files linted, gates open, diffs clean) for the operator's release-approval decision.
