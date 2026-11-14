# AGYOS Prompt Principles Upgrade — Implementation Plan

Status: PLAN draft; operator architecture approval pending.
Milestone: `M1-prompt-principles`
Baseline: `0caa7690afbcecf3eeafd89113d753cb9320838e` on `main`.

## Objective

Use the supplied company prompt archive as untrusted research input. Give every source principle a traceable disposition, apply compatible and supported principles to AGYOS prompt behavior, and remove unrelated company persona or aesthetic branding from active AGYOS-authored prompt copy. Keep provider and product names only where they explain an actual integration, compatibility constraint, attribution, or evidence source.

“All principles accounted for” means every source statement is inventoried and classified. It does not mean incompatible, unsupported, private-runtime, or contradictory vendor instructions become AGYOS rules.

## Gate 2 evidence and boundaries

- The archive at `/home/ai/Documents/projects/Freelance/Principles/Prompt/` contains 26 merged company/product files and a master index. The index claims 724 curated statements plus 14,165 extracted statements, for 14,889 total, and 597 tools. These are publisher-reported counts until independently reconciled against the source files.
- The archive describes itself as a community compilation. It says extracted material may be incomplete, historical, paraphrased, or not representative of current deployed company policy. The archive stays read-only; no raw prompt text or tool schemas will be copied wholesale into AGYOS.
- `docs/prompts.md` and `docs/references/prompts.md` are byte-identical. `docs/references/README.md` links to the references copy, so that path will remain as a short canonical pointer after `docs/prompts.md` becomes the single maintained library.
- The current library assigns a monochrome aesthetic to xAI/Grok and also uses company names in example personas. The prompt-engineering skill says step-by-step prompting improves accuracy by 30–50% without a citation. Related prompt skills contain universal chain-of-thought claims, company-branded examples, and some provider-specific code. Provider code will be reviewed separately from general prompt advice.
- Official guidance is not uniform: OpenAI's reasoning guidance recommends simple prompts and trying zero-shot before few-shot for its reasoning models; Anthropic describes clear instructions and closely matched examples as useful. These are model-specific sources, not universal guarantees. The rule will express conditional choices and require task-specific evaluation. Sources: [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), and [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Recheck version-sensitive guidance during implementation.
- The operator approved adding `.agents/agents/vibe-engineer.md` after the scout found unrelated FAANG persona branding there.
- Local and live remote branch inventories contain only `main` at the baseline SHA. Dependabot PRs #11, #12, and #13 are closed and unmerged. Current `requirements.txt` contains the PyYAML and jsonschema floors proposed by #12 and #13; CI still uses `actions/setup-node@v4`, so #11 was not incorporated. There is no live secondary branch to merge or delete; do not recreate or revive those refs as part of this milestone.
- The worktree has one pre-existing edit in `agyos_decision/skills_router.py`. It is excluded from this milestone, staging, commits, and edits.

## Design decisions

1. Keep one operational rule set. Each record in the research ledger receives exactly one disposition: `adopt`, `adapt`, `reject`, `duplicate`, or `unverified`. Every row includes a source locator, stable statement hash, rationale, and an AGYOS control mapping when adopted or adapted. A duplicate points to its canonical row. A rejected or unverified row records why it is not active guidance.
2. Reconcile the archive's reported counts before claiming complete source coverage. Define statement units from the archive's existing numbered principles and source-level principle entries; keep tool schemas and ordinary examples in separate inventory classes. Record parse ambiguities and count differences instead of guessing.
3. Store paraphrases and hashes in the ledger, not copied system prompts. Record source file digest, section/line locator, source attribution class, and evidence links. The audit report must distinguish archive claims, independently verified claims, AGYOS decisions, and remaining uncertainty.
4. Make prompting proportional to task risk and complexity. Specify outcome, relevant context, constraints, and output shape when they affect the result. Use examples, delimiters, role framing, decomposition, and evaluation only when they address a real task need. Do not require hidden reasoning disclosure, a fixed framework, a fixed number of examples, or a prompt-length floor.
5. Keep provider-specific instructions in clearly labeled integration examples or skills. Remove unrelated provider identity and aesthetic branding from general AGYOS prompt copy. Preserve required attribution, licensing notices, and accurate compatibility details.
6. Keep `docs/prompts.md` canonical. Replace `docs/references/prompts.md` with a short link and description so existing reference links continue to work without a duplicate copy.
7. Reuse the existing GitHub Actions unittest discovery in `.github/workflows/ci.yml`; do not add a duplicate workflow or edit CI unless implementation evidence shows the new test is not discovered.

## Exact implementation file plan

| Path | Change |
|---|---|
| `docs/research/PROMPT_PRINCIPLES_AUDIT.md` | New evidence report: source inventory and digests, reconciled counts, disposition totals, source limitations, conflicts, authoritative corroboration, and mappings to AGYOS controls. |
| `docs/research/prompt-principles-ledger.jsonl` | New one-record-per-principle ledger with stable IDs, source locators and hashes, allowed disposition, rationale, mapping, evidence, confidence, and `duplicate_of` where required. No full prompt copies. |
| `docs/adr/0003-prompt-principles-integration.md` | New decision record for provenance, conditional transfer, incompatible instructions, vendor-name retention, and future source refreshes. |
| `.agents/rules/agyos-prompt-principles.md` | New concise always-on rule for task-fit prompting, source grounding, untrusted input, output contracts, conditional examples/decomposition, evaluation, and branding boundaries. Keep below the repository's 24 KB rule limit. |
| `.agents/rules/common-skill-routing.md` | Add a narrow pointer from prompt-related tasks to the new rule and audited prompt skills. Preserve existing routing behavior and all current edits. |
| `docs/prompts.md` | Rework as the canonical AGYOS library: remove unrelated vendor aesthetic/persona framing, correct unsupported claims, keep useful task templates, and mark product-specific examples accurately. Replace raw brand-bearing historical prompt copy with normalized examples while retaining provenance in the audit. |
| `docs/references/prompts.md` | Replace duplicate content with a short pointer to `../prompts.md`; preserve this path for current links. |
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
| `scripts/tests/test_prompt_principles.py` | New CI-discovered tests for ledger schema and count reconciliation, disposition/mapping rules, duplicate links, active prompt brand boundaries, and removal of unsupported universal CoT claims. |
| `.agents/state/context-graph.json` | Add the existing prompt surfaces and their verified file references; preserve all current graph invariants. |
| `docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md`, `.agents/state/CURRENT.md`, `.agents/state/state.json`, `.agents/state/checkpoints/M1-prompt-principles.md` | Maintain milestone evidence and gate state. |

No change is planned for `.github/workflows/ci.yml`: it already runs `python -m unittest discover -s scripts/tests -v` on `main` pushes. CI will prove discovery. No linked repositories are configured.

## Verification and release sequence

- Before implementation, manually inspect planned paths and existing diffs; do not stage, restore, or overwrite the pre-existing router edit.
- During implementation, run no local tests, builds, linters, type checks, dependency setup, generators, or media tools. Locally, use static file inspection and `git diff --check` only.
- GitHub Actions must run the complete existing workflow on the exact `main` commit. The new test must be visible under `Check AGYOS startup contracts`; a queued, missing, skipped, or failed run is pending/failing, not a pass.
- `python -m unittest discover -s scripts/tests -p 'test_prompt_principles.py' -v` is the focused verification command for the Actions runner. The complete CI run remains required.
- Resolve the publication ordering as follows: finish implementation and static review; obtain the Gate 5 operator sign-off before creating the production commit; prepare the scoped commit/push script under `.agents/state/decisions/drafts/`; after the explicit sign-off, commit and push only the milestone files directly to `origin/main` with the required identity; then inspect Actions for that exact SHA. If CI fails, stop and return to implementation. A new production commit requires renewed Gate 5 sign-off. Do not create another branch or worktree.
- The requested context compaction is the `COMPACT` step after Gate 3 plan approval. It runs only after the operator approves this plan; afterward, repopulate `CURRENT.md` with this plan, exact scope, and next action.

## Acceptance criteria

- Every archive principle is represented exactly once in the reconciled ledger or covered by a clearly reported parsing limitation; all reported and observed counts are distinguished.
- Each adopted or adapted row maps to an active AGYOS control and has evidence plus a task-fit rationale. Unsupported, conflicting, vendor-runtime, duplicate, and unverified claims do not become universal rules.
- Active AGYOS prompt copy uses AGYOS identity and has no unrelated company persona or aesthetic branding. Allowed vendor names have a recorded compatibility, attribution, licensing, or evidence reason.
- The old unsupported 30–50% chain-of-thought claim is removed. No rule asks a model to expose hidden reasoning.
- Existing user work remains intact; no source archive file is changed; no non-main branch is created.
- The exact-revision GitHub Actions run passes the applicable suite before completion is claimed. The report names the SHA, run URL, counts, changed paths, and any limitations.

## Operator review

Approve or revise this architecture before Gate 4. Also supply or approve 2–3 human-written structural invariants for the context graph; suggested candidates are: every adopted/adapted ledger row maps to an active AGYOS control; every duplicate ledger row points to one canonical row; and general AGYOS prompt copy contains vendor names only for documented compatibility, attribution, or evidence.
