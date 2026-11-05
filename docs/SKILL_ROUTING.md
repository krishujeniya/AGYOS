# Skill selection and catalog maintenance

For every task, discover a relevant skill, read its `SKILL.md`, apply the applicable
steps, and verify the result. Repeat discovery when the task changes. Reading a
runbook does not prove that its instructions were followed.

## Scope and acceptance criteria

This update covers the decision router, CLI and MCP entry points, shared rules,
skill discovery metadata, manifest and documentation generators, regression tests,
CI, README, and handoff. Existing specialist procedures and attribution are
preserved. No paid calls or global runtime installation are required.

- Every physical skill has parseable YAML with its directory name and a useful description.
- Both generated skill indexes cover the physical catalog without duplicate IDs.
- All curated routes point to existing runbooks inside the checkout.
- Task intent takes priority over a language keyword; phrases use word boundaries.
- Unknown tasks use the decision runbook instead of an unrelated specialist.
- CLI and MCP can return the selected runbook; selection alone stays pending.
- Risk and structural work cannot become a trivial edit merely because a prompt is short.
- Full offline tests, catalog validation, syntax checks, and independent review precede push.

## Implementation and checks

Shared parsing lives in `agyos_decision/catalog.py`; routing lives in
`agyos_decision/skills_router.py`. `scripts/agyos-decision.py`, `bin/agyos`, and
`mcp/state-server.cjs` expose the same decision pipeline. Catalog generators read
the same metadata and operate only in this checkout.

```bash
python3 scripts/build_tiered_skills_manifest.py
python3 scripts/build_docs_data.py
python3 -m unittest discover -s scripts/tests -v
python3 -m compileall -q agyos_decision scripts
node --check mcp/state-server.cjs
bash scripts/agyos-verify.sh
```

## Operating contract

Use `bin/agyos decide "<task>" --json --runbook`, or MCP `agyos_decision` with
`include_runbook: true`. Without the option, read `runbook_path` with the host's
file reader or use `bin/agyos skill <primary_skill>`. Runbook references are
relative to the repository root, even when the CLI is started elsewhere.

Scores and `confidence` are deterministic matching heuristics, not calibrated
probabilities. `execution_status` is `pending_runbook_read` until the entry point
returns the file, then `runbook_returned`. Neither status certifies execution.
The assistant must still apply the steps and report actual checks. Generic
requests receive `selection_status: fallback` and require inspection of the
objective before specialist work.

Rules apply by relevance: common rules plus the language, risk, and workflow
rules needed for the task. The shared routing rule governs all skill selection;
loading the entire catalog into a prompt is unnecessary. Explicit user constraints,
host permissions, existing authorization, and supported tools take precedence
over a runbook's example commands. Task routing never authorizes publication,
payments, messages, or deployment.

## Limits

This is an offline routing and metadata check. It cannot guarantee that every
assistant host invokes skills or that all specialist instructions are correct.
Some inherited skill files contain historical fragments; repairing their
discovery headers preserves those bodies rather than inventing missing source.
Read and assess a selected runbook before following it. Lifecycle permission
hooks remain separate; no undocumented hook response fields are introduced.

## Verified update, 2026-11-05

- 75 Python tests passed, including 17 routing/catalog tests and real local CLI/MCP integration.
- 59 council tests and 51 host verification checks passed.
- All 1,862 skill headers and 141 rule headers/size limits passed validation.
- Both manifests and generated documentation reproduced byte-for-byte.
- Repository Python syntax, Node syntax, shell syntax, and diff whitespace checks passed.
- Independent checker approved the scoped update after regression fixes.
- Redacted Gitleaks scans found no leaks in the three existing outgoing commits or tracked diff; staged changes are scanned before commit.
- Rendered docs checked at 390x844 and 1440x900; keyboard Enter activated the updated Copy button. Live deployment acceptance remains separate.

| Before | After | Why |
| --- | --- | --- |
| Probability and fixed fast-path claims | Heuristic matching and explicit risk-aware complexity | Describe implemented behavior accurately. |
| Selection shown without instructions | CLI/MCP optionally return the runbook | Make the next required action available. |
| Specialist names copied as commands | Catalog entries use `bin/agyos skill <id>` | Give every entry a working local inspection command. |

The pre-commit assertion counter was also fixed to accept zero matches while still blocking assertion removal; two staged Git fixture regressions passed.
