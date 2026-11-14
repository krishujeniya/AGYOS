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

## Gate 2 — CI scope addendum pending

- Current `main` is `016af8c77a489c625d8c6fb4237b4c8f83cc8a09`; prompt analysis originally used `0caa7690afbcecf3eeafd89113d753cb9320838e`.
- Actions run `43564095843` failed on missing `sql.js`; run `43564363489` failed on missing `ajv` in the state-store schema. The runtime dependency helper expects `scripts/agyos-runtime/package.json`, which is absent.
- This baseline failure is outside the approved prompt boundary. The operator was asked whether to include a minimal runtime dependency manifest/lockfile and CI install step. Do not advance to Gate 3 approval or modify runtime dependencies until scope is resolved.
- The routing change in `4315ea62` and state-store change in `016af8c` are already committed in `main`; they remain outside this milestone.

## Gate 2 — CI scope addendum resolved

- Operator approved including a minimal CI blocker fix on 2026-11-14.
- Commits `016af8c` and `3e67d21` changed state-store imports to load optional `sql.js` and `ajv` dependencies only when needed; they are already on `main` and remain outside the prompt-principles changeset.
- Full CI run `43564722594` passed on `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`. No new runtime dependency manifest or workflow install step is required for the observed baseline failure.
- Gate 3 plan draft updated to use `e0d9bbfc` as the current main baseline. Operator architecture approval is pending.

## Gate 3 — PLAN resumed

- CI blocker scope addendum approved by the operator. The observed failures were resolved on `main` by `016af8c` and `3e67d21`; complete CI passed on `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6` in run `43564722594`.
- Updated plan and milestone records to use `e0d9bbfc` as the current baseline. No dependency manifest or CI install step is included because the latest complete run passes.
- `git diff --check` passed on the current plan/state diff. No local tests or builds were run.
- Architecture approval and context compaction remain pending.


## Gate 3 — PLAN

- pass: operator replied `y` to `docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md` on 2026-11-14.
- pass: operator approved the three proposed context-graph invariants; they were added while preserving all prior invariants.
- plan baseline: `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`; complete CI run `43564722594` passed on this revision.

## Gate 3.5 — COMPACT

- pass: `bash bin/compact.sh` completed after plan approval; CURRENT was repopulated from the approved plan and updated context graph.

- state: current gate moved to IMPLEMENT at baseline `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`; manual preflight is next.

## Preflight — IMPLEMENT entry

- preflight: PARTIAL — checked 33 planned files; 28 exist and 5 are new deliverables.
  - missing: `docs/research/PROMPT_PRINCIPLES_AUDIT.md`, `docs/research/prompt-principles-ledger.jsonl`, `docs/adr/0003-prompt-principles-integration.md`, `.agents/rules/agyos-prompt-principles.md`, `scripts/tests/test_prompt_principles.py`.
  - existing prompt documents, related skills/references, `vibe-engineer.md`, routing rule, CI workflow, and all milestone state paths were inspected before editing.
- `git diff --check` passed on plan and state changes. No local tests, builds, dependency resolution, or linters were run.
- implementation starts with source-archive inventory and per-statement accounting design.

## Gate 3 — PLAN amendment

- New provenance finding: the supplied Prompt directory is the clean `Prompt/` subtree of `krishujeniya/Principles` at `d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e`; the repository tree inspected has no root `LICENSE` or `NOTICE`, while the archive README refers to an upstream AGPL license.
- Amended design: do not copy the archive into AGYOS. Sparse-check out the pinned public source in existing GitHub Actions, parse and reconcile source units there, emit only hashes and locators in the JSONL ledger artifact, and keep the source prose out of the artifact and repository.
- Added `scripts/audit_prompt_principles.py`, CI changes to `.github/workflows/ci.yml`, parser fixture coverage, and the generated Actions artifact node to the graph and plan.
- The detailed JSONL ledger is now a CI artifact rather than a committed file. The committed report and parser preserve the method after the artifact expires.
- The original PLAN approval and three graph invariants remain recorded. Operator approved this amendment on 2026-11-14.
- `bash bin/compact.sh` completed after approval; CURRENT was repopulated with the amended plan and implementation scope.
- Repeated preflight: 33 planned repository paths checked; 28 exist and 5 are new deliverables: audit report, parser, ADR, rule, and parser test. The ledger JSONL is a CI artifact, not a repository path.
- State moved to `current_gate=IMPLEMENT` at baseline `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`. Local verification remains static inspection and `git diff --check` only.

## Gate 3 — generated-catalog scope amendment

- pass: operator approved adding checked-in skill catalog outputs on 2026-11-14 so revised skill descriptions can remain synchronized.
- Added the five skill catalog outputs and two generated site metadata outputs checked by the existing workflow to the approved scope. CI is the only source for refreshed generated content; no local generator will run.
- Expanded preflight: 40 planned repository paths, 35 existing and 5 new deliverables. The seven added catalog paths already exist and are generated by the existing CI workflow.
- First CI run may expose stale catalog files after generating and uploading `agyos-skill-catalog-generated`; apply only that artifact's changed outputs, then request renewed Gate 5 sign-off before the catalog-refresh commit.

## Gate 4 — IMPLEMENT progress

- Rewrote the canonical AGYOS prompt library, prompt skill runbooks, task pattern references, example data, and Vibe Engineer identity. Product names remain only for the Stitch integration, source attribution, or cited official guidance.
- Added the prompt-principles rule, ADR, source audit report, pinned-source parser, CI fixture coverage, and seven-day JSONL/count artifact. The parser records hashes and locators without source statement text and emits an input-error summary when source parsing cannot start.
- Added a caller-selected score target to the optimizer helper, removed the default hidden-reasoning variation, and added CI behavior coverage. Extracted helpers keep the changed optimizer methods under the repository's 50-line limit.
- New or updated regression tests: 2 new cases for disposition completeness and optimizer target behavior; parser fixture expectations and prompt-surface coverage were also updated. Tests remain unrun locally.
- `git diff --check` passed for tracked and new files. The independent checker completed a read-only static review with no remaining findings. Exact-revision Actions results and generated catalog outputs remain pending.
- Confirmed the active branch remains `main`; no commit, push, branch, or worktree was created. Gate 5 operator sign-off is required before the first CI-triggering push.
- Gate 5 approval: operator replied `y` on 2026-11-14 to the scoped `main` commit/push that triggers CI. Scope is the reviewed implementation; no generated catalog files are included in this first commit. Renewed sign-off is required before committing refreshed catalog outputs.

```json
{"milestone":"M1-prompt-principles","iteration":1,"publisher_company_document_claim":26,"publisher_principle_claim":14889,"new_regression_cases":2,"local_tests_run":0,"ci_ledger_rows":"pending","generated_catalog_outputs_from_actions":false}
```

## Gate 5 — first exact-revision CI attempt and follow-up

- CI run [43572120201](https://github.com/krishujeniya/AGYOS/actions/runs/43572120201) completed with failure on `dbb6f8df3c352384a8543c8908aab5a28082bc19`.
- `Check AGY startup contracts`: 179 tests ran, 1 failed and 1 was skipped. The sole failure expected the shortened publisher-only status instead of the current explicit ledger-limit string; the fixture assertion now matches the returned contract.
- `Audit pinned prompt principles source`: failed because the parser expected unbulleted count metadata and an exact exhaustive heading. The run artifact reported 724 curated and 0 exhaustive rows; the latter is a parser mismatch, not a source count. No count reconciliation or completeness claim is made from this run.
- Deployment run [43572120384](https://github.com/krishujeniya/AGYOS/actions/runs/43572120384) passed.
- Applied only the changed files from CI artifact `agyos-skill-catalog-generated`: `.agents/skills-manifest.json`, `docs/skills-data.json`, and `docs/llms.txt`. No generator was run locally.
- Follow-up parser and fixture now cover bullet-prefixed metadata and a suffixed exhaustive heading. `git diff --check` passed; local tests and parser execution remain prohibited by repository policy.
- Preserved the earlier untracked executed helper as audit history and excluded it from follow-up staging; it stages the first change set and omits the refreshed catalogs. The separate guarded draft stages only the follow-up paths and checks the current `main` SHA, origin URL, remote SHA, and author identity.
- Independent static review passed after the JSON fence was corrected and the follow-up draft was checked for scope. Corrected exact-revision CI remains pending. Renewed Gate 5 operator approval is required before follow-up commit and push.

```json
{"milestone":"M1-prompt-principles","iteration":2,"source_format_fixes":["bullet-prefixed count metadata","suffixed exhaustive section heading"],"catalog_outputs_from_ci_artifact":3,"local_tests_run":0,"local_generators_run":0,"diff_check":"PASS","independent_checker":"PASS","corrected_ci":"pending","gate5_operator_approval":"pending"}
```

## Gate 5 — second exact-revision CI attempt and metadata accounting

- Operator approved the guarded follow-up push. Script `.agents/state/decisions/executed/20261114-075100-m1-prompt-principles-followup.sh` committed and pushed `99c26eb16b79a0ebefa41b98044bf973bbc53dd6` to `origin/main` with the required identity; the push output was successful.
- CI run [43574183754](https://github.com/krishujeniya/AGYOS/actions/runs/43574183754) passed startup contracts and the council job, then failed the source audit. Its artifact reports 724 curated and 14,164 exhaustive principle rows (14,888 total) against the publisher's 14,889 combined rows.
- The only discrepancy is ANTHROPIC section 3.1: it declares 129 source rows, while there are 128 non-keyword principle entries and one keyword metadata row at source line 190. This appears to explain the publisher's one-row excess; the metadata row will be hashed and located separately, not added to the principle ledger. This classification remains subject to the next CI artifact.
- Pages run [43574183813](https://github.com/krishujeniya/AGYOS/actions/runs/43574183813) passed. The generated-catalog equality step did not run after the audit failure.
- Iteration 3 changes the summary and fixture to classify keyword metadata, reconcile publisher source-row totals, and keep ledger rows limited to principles. It also asserts that keyword text is absent from the full summary and that `main()` accepts the reconciled status. No local tests, parser execution, or generators were run. Independent static review and `git diff --check` passed; corrected exact-revision CI remains pending.
- Renewed operator sign-off is required before another commit or push.

```json
{"milestone":"M1-prompt-principles","iteration":3,"latest_pushed_commit":"99c26eb16b79a0ebefa41b98044bf973bbc53dd6","startup_contracts":"PASS in CI 43574183754","parsed_principles":14888,"classified_metadata_rows_pending_reconciliation":1,"publisher_combined_claim":14889,"local_tests_run":0,"local_generators_run":0,"independent_checker":"PASS","diff_check":"PASS","corrected_ci":"pending","next_push_approval":"required"}
```

## Gate 5 — exact-revision verification after metadata accounting

- Operator approved the guarded metadata-accounting commit/push. Script `.agents/state/decisions/executed/20261114-082500-m1-prompt-metadata-reconciliation.sh` committed `98486147dbab917deee345fd4c36498f5901bc01` and pushed successfully to `origin/main` with the required identity.
- CI run [43576647191](https://github.com/krishujeniya/AGYOS/actions/runs/43576647191) passed on that SHA. Startup contracts, council regression, source audit, both artifact uploads, endpoint-encryption regression tests, and generated-catalog equality passed.
- Audit artifact reports 26 company documents; 724 curated and 14,164 exhaustive principle rows; 14,888 ledger records; one separately hashed keyword metadata row; and 14,889 accounted publisher source rows. Dispositions: 4 adapted, 14,884 unverified. There are no count mismatches, and the ledger contains no source statement text.
- Publisher claims of 80 upstream files and 597 tools remain unreconciled because those inventories are absent from the supplied subtree or outside the ledger. The archive's publisher count includes one keyword metadata row, which is not treated as an instruction.
- Pages run [43576647123](https://github.com/krishujeniya/AGYOS/actions/runs/43576647123) passed on the same SHA. The generated catalog equality check passed in CI.
- No local tests, parser, generators, builds, or dependency setup were run. Final counts are now recorded in the audit report and handoff; independent review and `git diff --check` passed. This evidence-only diff needs renewed sign-off before its commit/push and has no exact-revision Actions run yet.

```json
{"milestone":"M1-prompt-principles","iteration":4,"verified_code_commit":"98486147dbab917deee345fd4c36498f5901bc01","ci_run":"43576647191: PASS","pages_run":"43576647123: PASS","company_files":26,"curated_principles":724,"exhaustive_principles":14164,"principle_ledger_rows":14888,"non_principle_metadata_rows":1,"publisher_source_rows_accounted":14889,"dispositions":{"adapt":4,"unverified":14884},"count_mismatches":0,"local_tests_run":0,"local_generators_run":0,"evidence_commit_review":"PASS","evidence_commit_approval":"required"}
```
