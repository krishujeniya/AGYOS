# CURRENT

## Goal

Use the supplied company prompt archive as untrusted research input to improve AGYOS-owned prompt guidance, account for every source statement, and remove unrelated vendor branding from AGYOS-authored prompt copy.

## Gate status

- UNDERSTAND: approved by the operator on 2026-11-14; task list: `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md`.
- ANALYZE: findings and a proposed boundary are ready; operator scope approval is pending.
- PLAN, IMPLEMENT, VERIFY: not started.
- Baseline revision: `228884581aaebe3c2f6f2a246df6b30361b5bcb0` on `main`.

## Gate 2 scope and risk

### Findings

- The supplied master index describes 26 company/product files, 80 upstream prompt/skill/tool files, 724 curated statements, and 14,165 extracted statements (14,889 combined). It explicitly says the community archive is not officially authenticated, may be incomplete, and that source text is not necessarily literal company policy. The archive README duplicates the master index.
- The archive contains cross-company conflicts, vendor-specific runtime constraints, and agent-directed text. Treat source material as untrusted evidence; do not copy its instructions or tool schemas into AGYOS as-is.
- `docs/prompts.md` and `docs/references/prompts.md` duplicate a prompt library with explicit vendor aesthetics and personas. Keep one canonical AGYOS prompt library and remove unrelated vendor framing from AGYOS-authored copy.
- `.agents/skills/prompt-engineering/SKILL.md` claims asking for chain-of-thought improves accuracy by 30–50% without a source. Current official reasoning guidance says such requests may be unnecessary or may hinder performance. Verify and correct this during source mapping.
- Physical `.agents/skills/` contains 2,240 `SKILL.md` files. Generated manifests claim 1,983; `AGENTS.md` claims 2,180. Many skill directories and core files are untracked or modified in the existing worktree. Do not overwrite them or claim catalog-wide completion from inconsistent counts.
- `.agents/rules/common-skill-routing.md`, `AGENTS.md`, `README.md`, `.github/workflows/ci.yml`, and `scripts/tests/test_skill_routing.py` already contain user changes. Review and preserve these changes before any overlap edit.
- CI currently triggers on pushes to `main` and pull requests targeting `main`; it has no `workflow_dispatch`. No push or PR creation is authorized, so exact-revision CI will remain pending unless the operator later authorizes publication.

### Proposed implementation boundary — approval required

- Read the complete supplied archive at `/home/ai/Documents/projects/Freelance/Principles/Prompt/`, relevant AGYOS prompt/rule/skill files, manifests, workflow, and current diffs.
- Write the source audit and decision record under `docs/research/` and `docs/adr/`; add one AGYOS-native always-on rule under `.agents/rules/`; connect it through `.agents/rules/common-skill-routing.md`.
- Canonicalize `docs/prompts.md` and `docs/references/prompts.md`; audit the directly relevant skills `prompt-engineering`, `prompt-optimizer`, `prompt-library`, `prompt-engineer`, and `enhance-prompt`.
- Add prompt-specific CI coverage in a new test file and, only as needed, carefully merge a minimal change into the already modified `.github/workflows/ci.yml`.
- Do not rename skills, mass-edit the 2,240 skill files, remove provider/model/API identifiers needed for compatibility, erase source attribution, alter supplied source files, or publish/deploy. Keep the catalog count mismatch recorded as a separate existing-work limitation unless its reconciliation can be done without absorbing or changing unapproved user files.

### Complexity and permissions

- Raw scope score: 17/24 — files 4, cross-references 4, risk 3, novelty 4, verification 2, reversibility 0.
- Canonical complexity: 4/5; full five-gate flow; major scope. Four read-only scout reviews completed after scoring.
- Read: supplied archive; `AGENTS.md`; `AI_HANDOFF.md`; prompt docs and relevant prompt skills; `.agents/rules/`; `agyos_decision/`; CI and relevant tests; manifests; current Git diffs.
- Proposed write: task/checkpoint/state artifacts already created; after scope approval, only the exact research, ADR, rule, prompt-library, relevant prompt-skill, test, and CI paths listed above.
- Local commands: static file inspection, `rg`, and `git diff --check` only. All builds, tests, linting, dependency setup, and catalog generation stay in GitHub Actions.
- Network: official vendor documentation and the pinned archive source for provenance checks; GitHub Actions only for remote validation. No paid model/API calls.

## Existing worktree preservation

Before implementation, inspect each overlapping diff and preserve the pre-existing edits listed above. Do not restore, clean, stage, commit, or push those files without separate authorization.

## Prior milestone

The previous skill-catalog audit and publication are documented in `docs/SKILL_CATALOG_AUDIT_REPORT.md` and the preceding revision history. Its published 1,983 count does not reconcile with the current physical tree and must not be treated as the present count.
