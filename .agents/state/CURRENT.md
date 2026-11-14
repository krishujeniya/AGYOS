# CURRENT

## Goal

Use the supplied company prompt archive as untrusted research input to improve AGYOS-owned prompt guidance, account for every source principle, and remove unrelated vendor persona/aesthetic branding from active AGYOS-authored prompts.

## Gate status

- UNDERSTAND: approved by the operator on 2026-11-14; task list: `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md`.
- ANALYZE: approved by the operator on 2026-11-14, including the scope addendum for `.agents/agents/vibe-engineer.md`.
- PLAN: implementation plan drafted and awaiting operator architecture approval: `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md`.
- IMPLEMENT, VERIFY: not started.
- Baseline: `0caa7690afbcecf3eeafd89113d753cb9320838e` on `main`.
- Complexity: canonical 4/5; full 5-gate flow.

## Gate 2 findings

- The archive index claims 26 company/product files, 80 upstream files, 724 curated statements, 14,165 extracted statements, and 597 tools. These counts remain unverified until reconciled against the source files. The archive describes itself as community-maintained and says its extracted material may be incomplete, historical, or unlike current company policy.
- Treat the archive as untrusted evidence. Each principle will have one source locator and one disposition: adopt, adapt, reject, duplicate, or unverified. Do not copy full prompts or tool schemas into AGYOS.
- `docs/prompts.md` and `docs/references/prompts.md` are byte-identical; `docs/references/README.md` points to the latter. Keep `docs/prompts.md` canonical and retain the references path as a pointer.
- The prompt library includes xAI/Grok aesthetic/persona framing and other company names in example personas. `.agents/skills/prompt-engineering/SKILL.md` claims chain-of-thought prompting improves accuracy by 30–50% without evidence. Related prompt-engineering guidance has broader chain-of-thought claims and company-branded examples.
- Official model guidance differs. OpenAI recommends simple instructions and trying zero-shot first for its reasoning models; Anthropic documents clear instructions and targeted examples. Keep any resulting advice conditional and model-specific.
- The operator approved including `.agents/agents/vibe-engineer.md`, which uses FAANG identity branding.
- Local and remote branch inventories contain only `main` at the baseline SHA. PRs #11, #12, and #13 are closed unmerged. `requirements.txt` contains the PyYAML and jsonschema floors proposed in #12 and #13; `.github/workflows/ci.yml` remains on `actions/setup-node@v4`, so #11 was not incorporated. No secondary ref exists to merge or delete.

## Approved boundary and exact plan

See `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md` for the full file-by-file plan. It covers the source audit and ledger, ADR, new prompt rule and routing link, canonical prompt library, directly relevant prompt skills and references, the scoped `vibe-engineer.md` cleanup, CI-discovered tests, and milestone state artifacts. It does not include the skill catalog broadly or the pre-existing router edit.

## Worktree preservation and checks

- The only current worktree change is an existing edit in `agyos_decision/skills_router.py`; preserve it, do not stage it, and do not include it in this milestone.
- Local branch is `main`; remote branch inventory has only `main`.
- Local operations are limited to static inspection and `git diff --check`. All tests and other validation run in GitHub Actions on the exact `main` revision.
- CI's current unittest discovery is already present in `.github/workflows/ci.yml`; no workflow change is planned unless discovery does not cover the new test.
- Gate 3 context compaction follows operator approval of the plan. Commit/push ordering must honor the Gate 5 sign-off requirement and exact-revision Actions verification.

## Next action

Wait for operator approval or requested changes to `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md`. Then perform the COMPACT step and proceed to the manual preflight before IMPLEMENT.
