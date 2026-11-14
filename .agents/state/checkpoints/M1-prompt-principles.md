# M1-prompt-principles

- created: 2026-11-14T05:03:44Z
- baseline: `0caa7690afbcecf3eeafd89113d753cb9320838e` (`main` at ANALYZE)
- current_gate: PLAN
- Skill-Versions:
  - anchor-draft-commit: 1.1.0
  - anchor-graph: 1.1.0
  - anchor-orchestrator: 1.1.0
  - anchor-preflight: 1.1.0
  - anchor-scope: 1.1.0
  - anchor-scout: 1.1.0
  - anchor-verify: 1.1.0

## Gate 1 — UNDERSTAND

- pass: operator replied `y` to `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md` on 2026-11-14.
- Task list covers complete source accounting, AGYOS integration, prompt/brand audit, CI-only verification, and preservation of existing work.

## Gate 2 — ANALYZE

- pass: operator replied `y` to the scope on 2026-11-14.
- scope addendum: operator approved adding `.agents/agents/vibe-engineer.md` after a read-only scan found unrelated FAANG persona branding.
- source research: the archive index claims 724 curated plus 14,165 extracted statements; counts remain publisher-reported until reconciled. The archive is community-maintained and not proof of current company policy.
- official-source review found model-specific differences in reasoning and example guidance; transfer will remain conditional.
- branch inventory: local and live remote contain only `main`; PRs #11, #12, and #13 are closed and unmerged. No secondary refs remain to merge or delete.
- baseline at ANALYZE: `0caa7690afbcecf3eeafd89113d753cb9320838e`.
- preservation: one pre-existing edit remains in `agyos_decision/skills_router.py`; it is outside this milestone and untouched.

## Gate 3 — PLAN

- status: implementation plan drafted and awaiting operator architecture approval at `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md`.
- context graph updated from explicit file references; all prior invariants preserved.
- no implementation changes or verification commands were made. Local validation remains limited to static inspection and `git diff --check`; test execution is reserved for GitHub Actions.
- Gate 3 approval, context compaction, and preflight are pending.
