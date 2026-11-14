# AGYOS Prompt Principles Upgrade — Implementation Plan

Status: Approved for IMPLEMENT on 2026-11-14, including the pinned-source CI checkout, generated-ledger artifact, and checked-in generated skill catalog outputs.
Milestone: `M1-prompt-principles`
Analysis baseline: `0caa7690afbcecf3eeafd89113d753cb9320838e`; latest `main` at plan review: `e0d9bbfc3abd9cee2da9567e94cb725c531c59b6`.

## Objective

Use the supplied company prompt archive as untrusted research input. Give every source principle a traceable disposition, apply compatible and supported principles to AGYOS prompt behavior, and remove unrelated company persona or aesthetic branding from active AGYOS-authored prompt copy. Keep provider and product names only where they explain an actual integration, compatibility constraint, attribution, or evidence source.

“All principles accounted for” means every source statement is inventoried and classified. It does not mean incompatible, unsupported, private-runtime, or contradictory vendor instructions become AGYOS rules.

## Gate 2 evidence and boundaries

- The archive at `/home/ai/Documents/projects/Freelance/Principles/Prompt/` is the `Prompt/` subtree of public repository `https://github.com/krishujeniya/Principles` at observed commit `d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e`. The checked-out source worktree was clean and aligned with `origin/main` during inspection. The index claims 724 curated statements plus 14,165 extracted statements, for 14,889 total, and 597 tools. Treat these as publisher-reported until the CI parser reconciles them.
- The archive describes itself as a community compilation derived from pinned upstream material, not authenticated company policy. Its README warns that principle lists are best-effort and may not cover every source instruction. The supplied repository tree has no root `LICENSE` or `NOTICE` file; its README refers to an AGPL license in the upstream source. Do not redistribute raw prompt text or tool schemas. Keep the source read-only and process a sparse checkout pinned to the observed commit only in GitHub Actions.
- `docs/prompts.md` and `docs/references/prompts.md` are byte-identical. `docs/references/README.md` links to the references copy, so that path will remain as a short canonical pointer after `docs/prompts.md` becomes the single maintained library.
- The current library assigns a monochrome aesthetic to xAI/Grok and also uses company names in example personas. The prompt-engineering skill says step-by-step prompting improves accuracy by 30–50% without a citation. Related prompt skills contain universal chain-of-thought claims, company-branded examples, and some provider-specific code. Provider code will be reviewed separately from general prompt advice.
- Official guidance is not uniform: OpenAI's reasoning guidance recommends simple prompts and trying zero-shot before few-shot for its reasoning models; Anthropic describes clear instructions and closely matched examples as useful. These are model-specific sources, not universal guarantees. The rule will express conditional choices and require task-specific evaluation. Sources: [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), and [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Recheck version-sensitive guidance during implementation.
- The operator approved adding `.agents/agents/vibe-engineer.md` after the scout found unrelated FAANG persona branding there.
- Earlier Actions runs failed when `sql.js` and then `ajv` were imported at module load. Commits `016af8c` and `3e67d21` made those imports lazy. The operator approved including a minimal CI fix if needed; the later change resolved the observed failures, so no new dependency manifest or install step is needed for this milestone. The complete CI run [43564722594](https://github.com/krishujeniya/AGYOS/actions/runs/43564722594) passed on `e0d9bbfc`.
- Local and live remote branch inventories contain only `main` at the baseline SHA. Dependabot PRs #11, #12, and #13 are closed and unmerged. Current `requirements.txt` contains the PyYAML and jsonschema floors proposed by #12 and #13; CI still uses `actions/setup-node@v4`, so #11 was not incorporated. There is no live secondary branch to merge or delete; do not recreate or revive those refs as part of this milestone.
- The routing edit in `agyos_decision/skills_router.py` is in `4315ea62`; lazy state-store imports are in `016af8c` and `3e67d21`. They are already in `main` and remain outside the prompt-principles change set. The current worktree contains the approved prompt-principles implementation; preserve unrelated existing work.

## Design decisions

1. Keep one operational rule set. Each record in the research ledger receives exactly one disposition: `adopt`, `adapt`, `reject`, `duplicate`, or `unverified`. Every row includes a source locator, stable statement hash, rationale, and an AGYOS control mapping when adopted or adapted. A duplicate points to its canonical row. A rejected or unverified row records why it is not active guidance.
2. Reconcile the archive's reported counts in GitHub Actions from a pinned, sparse checkout of `krishujeniya/Principles` at `d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e`. Define statement units from the archive's curated catalog entries and exhaustive principle entries; classify keyword metadata separately from principle statements and keep tool schemas and ordinary examples in separate inventory classes. Record parse ambiguities and count differences instead of guessing.
3. Generate the per-statement JSONL ledger as a CI artifact, not a committed copy of the source corpus. Each record contains hashes, source file/section/line locators, source attribution class, a disposition and rationale, and evidence links; it omits the statement text. The committed audit report documents the source and parser limits. CI summary and artifact report exact counts; an unverified archive statement remains explicitly unverified rather than being treated as policy.
4. Make prompting proportional to task risk and complexity. Specify outcome, relevant context, constraints, and output shape when they affect the result. Use examples, delimiters, role framing, decomposition, and evaluation only when they address a real task need. Do not require hidden reasoning disclosure, a fixed framework, a fixed number of examples, or a prompt-length floor.
5. Keep provider-specific instructions in clearly labeled integration examples or skills. Remove unrelated provider identity and aesthetic branding from general AGYOS prompt copy. Preserve required attribution, licensing notices, and accurate compatibility details.
6. Keep `docs/prompts.md` canonical. Replace `docs/references/prompts.md` with a short link and description so existing reference links continue to work without a duplicate copy.
7. Reuse existing GitHub Actions in `.github/workflows/ci.yml`. Add one checkout step for the pinned public source subtree, run the ledger parser and its unittest coverage in the existing CI job, and upload the generated JSONL plus a count/digest summary as an Actions artifact. Do not add another workflow, dependency installation, or a committed source copy. The observed baseline import failures are resolved on `main`.

## Exact implementation file plan

| Path | Change |
|---|---|
| `docs/research/PROMPT_PRINCIPLES_AUDIT.md` | New evidence report: source inventory, reconciled counts when CI completes, disposition method, source limitations, conflicts, authoritative corroboration, and mappings to AGYOS controls. Per-file digests are emitted in the CI summary artifact. |
| `scripts/audit_prompt_principles.py` | New deterministic parser for the pinned archive. Emit one JSONL record per declared principle with source commit, file digest, section/line locator, statement hash, disposition, rationale, and duplicate pointer; do not emit source statement text. Write only to the CI runner's temporary directory. |
| `.github/workflows/ci.yml` | Sparse-checkout the external source at the exact commit into `principles-source/`, run the parser and focused tests in the existing job, and upload the ledger/count summary artifact with `retention-days: 7`. |
| Actions artifact `prompt-principles-ledger.jsonl` | Generated under `$RUNNER_TEMP` only; it is not added to the AGYOS repository. Each row has a unique source locator/hash and one disposition. |
| `docs/adr/0003-prompt-principles-integration.md` | New decision record for provenance, conditional transfer, incompatible instructions, vendor-name retention, and future source refreshes. |
| `.agents/rules/agyos-prompt-principles.md` | New concise always-on rule for task-fit prompting, source grounding, untrusted input, output contracts, conditional examples/decomposition, evaluation, and branding boundaries. Keep below the repository's 24 KB rule limit. |
| `.agents/rules/common-skill-routing.md` | Add a narrow pointer from prompt-related tasks to the new rule and audited prompt skills. Preserve existing routing behavior and all current edits. |
| `docs/prompts.md` | Rework as the canonical AGYOS library: remove unrelated vendor aesthetic/persona framing, correct unsupported claims, keep useful task templates, and mark product-specific examples accurately. Replace raw brand-bearing historical prompt copy with normalized examples while retaining provenance in the audit. |
| `docs/references/prompts.md` | Replace duplicate content with a short pointer to `../prompts.md`; preserve this path for current links. |
| `docs/references/README.md` | Update the catalog description to match the canonical task-fit AGYOS prompt library after removing its fixed framework. |
| `.agents/skills/prompt-engineering/SKILL.md` | Remove the unsourced 30–50% accuracy claim and universal chain-of-thought requirement; provide model- and task-dependent guidance. |
| `.agents/skills/prompt-optimizer/SKILL.md` and `.agents/skills/prompt-optimizer/references/FULL_RUNBOOK.md` | Align prompt diagnosis and output with the new rule; retain any product-specific workflow only as a labeled compatibility example. |
| `.agents/skills/prompt-library/SKILL.md` and `.agents/skills/prompt-library/references/FULL_RUNBOOK.md` | Make framework selection optional and task-driven; keep required upstream attribution and licensing. |
| `.agents/skills/prompt-engineer/SKILL.md` and `.agents/skills/prompt-engineer/README.md` | Remove claims that a named framework or vendor identity guarantees results; use AGYOS as the default invocation identity and retain only relevant compatibility details. |
| `.agents/skills/enhance-prompt/SKILL.md` | Keep its Stitch-specific integration identity, but separate that compatibility guidance from general AGYOS prompt advice and remove decorative/vendor-style framing that is not required by the integration. |
| `.agents/skills/prompt-engineering-patterns/SKILL.md` | Reduce always-on instructions to concise, evidence-qualified steps and repair the reference pointer currently naming a missing `resources/implementation-playbook.md`. |
| `.agents/skills/prompt-engineering-patterns/references/chain-of-thought.md` | Replace universal performance claims and exposed reasoning traces with conditional task decomposition, concise answer checks, and references to current model-specific guidance. |
| `.agents/skills/prompt-engineering-patterns/references/few-shot-learning.md` | Remove fixed/universal examples guidance; describe when examples help and how to compare them on representative cases. |
| `.agents/skills/prompt-engineering-patterns/references/prompt-optimization.md` | Ground optimization in a fixed evaluation set, explicit quality criteria, and controlled comparisons; label unsupported performance claims. |
| `.agents/skills/prompt-engineering-patterns/references/prompt-templates.md` | Retain reusable structures only where their fields serve the task; remove fixed-framework requirements and unrelated vendor persona copy. |
| `.agents/skills/prompt-engineering-patterns/references/system-prompts.md` | Distinguish stable high-priority instructions from task-specific input and integration-specific behavior. |
| `.agents/skills/prompt-engineering-patterns/assets/few-shot-examples.json` | Audit examples for correctness and consistency with the updated guidance; retain only needed, non-conflicting examples. |
| `.agents/skills/prompt-engineering-patterns/assets/prompt-template-library.md` | Audit and align templates with the rule; remove unrelated company persona/aesthetic branding from general templates. |
| `.agents/skills/prompt-engineering-patterns/scripts/optimize-prompt.py` | Inspect generated prompt language and preserve runtime behavior unless a direct conflict is confirmed; any code change must be covered by CI tests. |
| `.agents/agents/vibe-engineer.md` | Replace FAANG-based identity with AGYOS role language while retaining concrete engineering requirements. This path is included by the operator's scope addendum. |
| `scripts/tests/test_prompt_principles.py` | New CI-discovered tests for parser fixtures, ledger schema and count reconciliation, disposition/mapping rules, duplicate links, active prompt brand boundaries, and removal of unsupported universal CoT claims. |
| `.agents/state/context-graph.json` | Add the existing prompt surfaces and their verified file references; preserve all current graph invariants. |
| `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md`, `.agents/state/CURRENT.md`, `.agents/state/state.json`, `.agents/state/checkpoints/M1-prompt-principles.md` | Maintain milestone evidence and gate state. |
| `.agents/skills/prompt-optimizer/SKILL.md`, `.agents/skills/prompt-library/SKILL.md`, `.agents/skills/prompt-engineer/SKILL.md`, `.agents/skills/prompt-engineering-patterns/SKILL.md`, `.agents/skills/enhance-prompt/SKILL.md` | Update frontmatter descriptions to remove unrelated product branding and unsupported general performance claims. Keep Stitch named only as the actual target integration. |
| `.agents/skills-manifest.json` | Refresh generated skill metadata from the approved skill descriptions. |
| `.agents/tier1-skills.json` | Refresh generated skill metadata from the approved skill descriptions. |
| `docs/skills-data.json` | Refresh generated documentation catalog from the approved skill descriptions. |
| `docs/ai-catalog.json` | Refresh generated AI skill catalog from the approved skill descriptions. |
| `docs/llms.txt` | Refresh generated skill summary from the approved skill descriptions. |
| `docs/sitemap.xml` | Include only if the existing CI generator changes this output. |
| `docs/robots.txt` | Include only if the existing CI generator changes this output. |

The existing workflow already discovers Python tests and uploads CI artifacts. The latest complete run passed after the state-store modules were changed to load optional dependencies only when needed. The archive checkout adds no runtime dependency and no local source-copy step. The generated ledger is retained as an artifact for the milestone run; the report and parser commit keep the methodology reproducible after artifact expiry.

## Verification and release sequence

- Before implementation, recheck the latest `main` revision and planned paths. The routing and state-store changes already in `main` are outside this milestone; preserve them without folding them into the prompt change set.
- During implementation, run no local tests, builds, linters, type checks, dependency setup, generators, or media tools. Locally, use static file inspection and `git diff --check` only.
- The operator approved the generated catalog outputs on 2026-11-14. Skill descriptions are catalog inputs. Obtain their refreshed contents only from the existing `agyos-skill-catalog-generated` Actions artifact; do not run catalog generators locally. The first exact-revision workflow may report stale generated outputs, but its catalog artifact must upload before the equality check. Apply only changed generated files, then obtain renewed Gate 5 sign-off before the catalog-refresh commit and run CI again on that exact revision.
- GitHub Actions must run the complete workflow on the exact `main` commit. The new test must be visible under `Check AGYOS startup contracts`; the parser must compare actual parsed units with publisher-reported counts, write its JSONL and digest summary to the runner temporary directory, and upload both as the named milestone artifact. A queued, missing, skipped, or failed run is pending/failing, not a pass. The current baseline run passed on `e0d9bbfc`; prompt changes still require a fresh complete run on their exact revision.
- `python -m unittest discover -s scripts/tests -p 'test_prompt_principles.py' -v` and `python scripts/audit_prompt_principles.py --source-dir principles-source/Prompt --output "$RUNNER_TEMP/prompt-principles-ledger.jsonl" --summary "$RUNNER_TEMP/prompt-principles-summary.json"` run only in Actions. The complete CI run remains required.
- Resolve the publication ordering as follows: finish implementation and static review; obtain the Gate 5 operator sign-off before creating the production commit; prepare the scoped commit/push script under `.agents/state/decisions/drafts/`; after the explicit sign-off, commit and push only the milestone files directly to `origin/main` with the required identity; then inspect Actions for that exact SHA. If CI fails, stop and return to implementation. A new production commit requires renewed Gate 5 sign-off. Do not create another branch or worktree.
- The requested context compaction is the `COMPACT` step after Gate 3 plan approval. It runs only after the operator approves this plan; afterward, repopulate `CURRENT.md` with this plan, exact scope, and next action.

## Acceptance criteria

- Every principle unit recognized by the parser is represented exactly once in the generated ledger artifact or covered by a clearly reported parsing limitation; publisher-reported, parsed, and reconciled counts are distinguished. The artifact has no raw source statement text and is linked from the CI run.
- Each adopted or adapted row maps to an active AGYOS control and has evidence plus a task-fit rationale. Unsupported, conflicting, vendor-runtime, duplicate, and unverified claims do not become universal rules.
- Active AGYOS prompt copy uses AGYOS identity and has no unrelated company persona or aesthetic branding. Allowed vendor names have a recorded compatibility, attribution, licensing, or evidence reason.
- The old unsupported 30–50% chain-of-thought claim is removed. No rule asks a model to expose hidden reasoning.
- Existing user work remains intact; no source archive file is changed; no non-main branch is created.
- The exact-revision GitHub Actions run passes the applicable suite before completion is claimed. The report names the SHA, run URL, counts, changed paths, and any limitations.

## Operator review

Original Gate 3 architecture and the three context-graph invariants were approved. The operator approved the pinned sparse checkout and CI artifact amendment on 2026-11-14 and later approved updating the checked-in generated catalog outputs to match revised skill descriptions. The supplied source has no root license file; the parser therefore emits only hashes and locators, not source prose.
