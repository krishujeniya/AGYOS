# CURRENT (Structured Handoff)

## 1. Goal

Use the supplied company prompt archive as untrusted research input to improve AGYOS prompt behavior, account for every parsed principle with a traceable disposition, and remove unrelated company persona or aesthetic branding from active AGYOS-authored prompt copy.

## 2. Spec

- Approved plan: `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md`.
- Task list: `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md`.
- Milestone: `M1-prompt-principles`.
- Source: read-only `krishujeniya/Principles` commit `d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e`, sparse path `Prompt/`.

## 3. Implementation scope

- New audit/parser outputs: `docs/research/PROMPT_PRINCIPLES_AUDIT.md`, `scripts/audit_prompt_principles.py`, CI artifact `prompt-principles-ledger.jsonl`.
- Decision and behavior: `docs/adr/0003-prompt-principles-integration.md`, `.agents/rules/agyos-prompt-principles.md`, `.agents/rules/common-skill-routing.md`.
- Prompt surfaces: `docs/prompts.md`, `docs/references/prompts.md`, directly relevant prompt skills and references under `.agents/skills/`, `.agents/agents/vibe-engineer.md`, and generated catalog outputs affected by revised skill descriptions.
- CI and regression: `.github/workflows/ci.yml`, `scripts/tests/test_prompt_principles.py`.
- Gate tracking: `.agents/state/context-graph.json`, `.agents/state/state.json`, this handoff, and `.agents/state/checkpoints/M1-prompt-principles.md`.
- Preserve unrelated existing edits and the source archive. Do not create branches or worktrees.

## 4. Evidence and constraints

- UNDERSTAND, ANALYZE, original PLAN, source-checkout/artifact amendment, and generated-catalog scope amendment approved on 2026-11-14.
- Baseline is `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`; full CI run `43564722594` passed there.
- Expanded preflight after catalog-scope approval: 40 planned repository paths; 35 existed and 5 are new deliverables. The seven generated catalog outputs are checked in and will be refreshed from Actions.
- Publisher claims 14,889 principles; the parser must reconcile actual source units and report ambiguities without guessing.
- The source repo lacks a root LICENSE/NOTICE; preserve provenance and emit hashes/locators, not source statement prose.
- Local operations: read-only inspection and `git diff --check`. Run tests, parser, builds, dependency setup, and validation only in GitHub Actions.
- No production commit or push before Gate 5 operator sign-off.

## 5. Next action

Static review is complete. Await Gate 5 operator sign-off before the scoped `main` commit and push that trigger exact-revision CI. The first run produces the generated catalog artifact; the checked-in catalog comparison may fail until that artifact is applied. Request renewed Gate 5 sign-off before a follow-up catalog commit. Tests, parser, generators, and full CI remain unrun on this working revision.
