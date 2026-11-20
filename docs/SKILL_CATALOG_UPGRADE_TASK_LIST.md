# AGYOS skill catalog quality and organization

## Gate 1: task list

- Status: Gates 1–3 approved; implementation and scoped verification are complete with one documented host CLI test timeout. See the final verification ledger below and `docs/SKILL_CATALOG_AUDIT_REPORT.md`.
- Request: inspect every skill; improve use, quality, organization, and names where evidence supports it.
- Baseline: branch `main`, revision `3056ca61d85dfc026c7b8540cbddc97d9a8c3238`.
- Worktree: existing uncommitted changes are present, including the recent video-skill work and `.agents/state/decisions/drafts/20261111-111600-push-main.sh`. They are outside this task's change set and must be preserved.

## Scope

Review all 1,982 direct runbooks under `.agents/skills/*/SKILL.md` and their skill-local references. Changes, if approved, may touch:

- `.agents/skills/` descriptions, concise runbooks, references, and supported metadata.
- The skill router, catalog generators, catalog tests, and generated manifests.
- Current catalog-facing `AGENTS.md`, `GEMINI.md`, `README.md`, `docs/index.html`, and handoff counts.
- A task-specific audit/verification record.

Documentation scope addendum (2026-11-11): the user asked to verify completion across the docs, so reconciliation also covers `site/index.html`, `TRACKER.md`, and the skill inventory references in `docs/security/THREAT_MODEL.md`. The threat-model update labels its old count as baseline and records the new inventory only; its security analysis was not re-audited.

Skill scope addendum (2026-11-11): the user requested an OpenWhispr skill from `https://github.com/OpenWhispr/openwhispr`. This explicit extension adds one source-backed runbook, routing regression, generated-index entries, and the corresponding current catalog counts.

Keep the canonical skill directory flat because `.agents/skills/AGENTS.md` defines directory IDs as stable and the skill-authoring guidance requires a flat namespace. Improve organization through reliable metadata, categories, routing, and cross-references. Do not remove skills. Preserve IDs unless a concrete discoverability or validity defect justifies a rename; for each proposed rename, map every old reference and keep an alias or redirect where needed. Do not modify unrelated application code, global `~/.claude` data, or the pre-existing worktree changes.

## Acceptance criteria

1. Every direct catalog runbook has valid frontmatter, a unique directory-matching ID, and a description that accurately states when the skill applies.
2. Main `SKILL.md` files meet the repository's `<300`-line limit; detailed material stays in linked references with valid local paths.
3. Every local Markdown link from a skill runbook resolves. Duplicate descriptions and bodies receive an evidence-based Keep, Improve, or alias/merge recommendation; no skill is deleted as part of this work.
4. Every rename has an old-ID → new-ID map, updated references, and a regression case. Existing stable IDs remain when renaming gives no clear benefit.
5. Router cases cover catalog-maintenance requests and representative variants; the chosen skill fits the user's intent, and existing frozen cases still pass.
6. The complete manifest and generated documentation indexes cover the physical catalog with no duplicate IDs; the Tier 1 index matches its intended subset. Current documentation uses accurate counts; historical reports retain their original dated counts.
7. Each changed skill is reviewed against its source and relevant dependent skills. Time-sensitive technical claims are checked against primary sources or explicitly marked unverified.
8. Relevant catalog/routing tests, generators, diff checks, and independent review pass. No test assertion is removed or weakened, and unrelated worktree changes remain untouched.

## Ordered work

1. **Baseline and inventory:** record the exact 1,982 IDs; scan metadata, descriptions, file lengths, local links, duplicate signatures, nested assets, and all references to candidate IDs.
2. **Full review:** assess each skill in four non-overlapping ID ranges; label findings as confirmed, heuristic, or requiring current external-source verification.
3. **Prioritize:** create an old-ID → new-ID map only for justified rename candidates; separate safe metadata/link fixes from merges, retirements, and content rewrites.
4. **Improve in bounded batches:** add or update tests first; correct the highest-impact trigger, link, and content defects; keep long references out of the main runbooks.
5. **Synchronize:** regenerate manifests and documentation indexes; correct current count claims while preserving dated historical records.
6. **Verify:** re-inventory all IDs and links, run the catalog/routing suite and applicable repository checks, review the diff independently, and record remaining freshness or host-execution gaps.

## Verified baseline findings

The findings in this section describe the pre-implementation baseline. Their current resolution status is recorded in **Implementation progress** below; dated baseline counts are intentionally retained for comparison.

These are static findings, not implementation approval or a claim that all content has been fact-checked:

- The physical catalog and complete manifest each contain 1,982 IDs; the Tier 1 index contains its 396-skill subset. All 1,982 YAML headers parsed in the inventory scan.
- 609 main runbooks exceed 300 lines; 68 exceed 800 lines. `elite-python-architect/SKILL.md` is 10,069 lines.
- 20 skills share the placeholder description `One sentence - what this skill does and when to invoke it`.
- Eight groups have runbook bodies that are identical after whitespace and case normalization; these need semantic and reference review before any consolidation.
- The ID `android_ui_verification` uses an underscore, contrary to the skill-authoring naming guidance; the router and a frozen test reference it.
- A syntax-aware pass over primary runbooks found 15 local Markdown links whose targets do not exist.
- At baseline, `README.md`, `AGENTS.md`, `GEMINI.md`, and `docs/index.html` claimed 1,862 skills; the self-improvement skill description said 1,970+. Current-facing counts were updated; historical handoffs and dated audit reports retain their original counts.
- A 4,883-character frontmatter block in `planning-with-files/SKILL.md` includes host-specific hook commands. Its behavior under supported AGYOS hosts has not been verified.
- The exact user request routed to `agyos-decision`; a similar catalog-audit paraphrase routed to `security-review`. Routing stability needs targeted cases.
- Fresh `scripts.tests.test_skill_routing` baseline: 17 passed. The redacted repository secret scan reported no findings. No skill content has been changed for this task.

## Gate 1 approval

- Confirmed: operator replied `y` on 2026-11-11.

## Gate 2: scope and risk findings

Four non-overlapping read-only reviews covered all 1,982 skills. Findings below distinguish structural defects from items that need further verification:

- **Catalog integrity:** all 1,982 YAML headers parsed and directory IDs matched. The complete manifest covers all IDs; Tier 1 remains a subset.
- **Progressive disclosure:** 609 main runbooks exceed 300 lines, including 68 over 800 and four over 2,000; `elite-python-architect` is 10,069 lines. Long files make key instructions harder to find and changes harder to review.
- **Discovery metadata:** 20 descriptions are the same unfilled prompt. Other confirmed weak metadata includes slug-only descriptions followed by a second header, a JSON fragment used as a description, and `sharp-edges` with duplicate frontmatter. These headers parse, so existing catalog tests do not catch their discovery failure.
- **Content correctness:** `elite-python-architect` contains Node/Express/TypeScript guidance under a Python identity; two Azure Key Vault TypeScript examples instantiate the wrong client; `audio-transcriber` calls an undefined helper. High-stakes legal, health, PCI, security-statistic, and current SDK/platform claims were not checked against live primary sources.
- **References:** 15 unresolved local Markdown targets were confirmed in primary runbooks. A broader path scan found 135 unique missing `.md` target pairs across 57 skills; some are examples or generated output paths and still need triage. Absolute `file://` paths are also present.
- **Overlap and IDs:** eight groups of runbook bodies match after normalization, with additional near-duplicates. A shared body does not prove a merge is safe because IDs and triggers differ. One ID uses an underscore and has router/test references.
- **Host metadata:** 221 runbooks declare host-related fields; `planning-with-files` has a 4,883-character header containing hook commands. Actual host interpretation was not tested. The repo’s own discovery parser reads the first header only.
- **Routing/docs at baseline:** the exact user request selected `agyos-decision`, but a similar paraphrase selected `security-review`. The current README, AGENTS, GEMINI, and docs homepage then showed 1,862 skills; the implementation status below records the count and routing updates.
- **Security/dependencies:** `.agents/config.json` lists no linked repositories; the context graph has no nodes or invariants. The redacted scout scan passed with no findings. Skill code or embedded commands were not executed.

### Boundary for Gate 2 approval

Keep the approved Gate 1 boundary: `.agents/skills/`, local references, router/catalog generators/tests/indexes, and current catalog-facing documentation. The flat skill root and existing dirty worktree changes remain protected. No global `~/.claude` files, application code, external publication, skill deletion, or unreviewed bulk renames enter scope. Current legal, health, security, and API claims remain unverified until checked against primary sources.

The operator approved this boundary on 2026-11-11; the approval record and Gate 3 plan status follow.

### Gate 2 approval

- Confirmed: operator replied `y` to the Gate 2 scope and risk boundary on 2026-11-11.
- The approved boundary remains the Gate 1 scope above.
- The repo-wide dependency scan emitted a broad node inventory but no dependency edges. The scoped graph now records only relationships confirmed in imports and generator path constants; existing human invariants remain empty.

### Gate 3 plan

- Plan: `docs/SKILL_CATALOG_UPGRADE_PLAN.md`.
- Context graph: `.agents/state/context-graph.json`.
- Confirmed: operator replied `y` to the architecture plan and adopted the three proposed graph invariants on 2026-11-11.
- Status: Gate 3 approved; three graph invariants adopted; implementation preflight completed.

## Implementation progress

Implementation retained all 1,982 baseline IDs and the flat catalog. The operator later expanded scope to add one source-backed OpenWhispr skill, bringing the current catalog to 1,983. It moved 613 long entrypoints to linked full-runbook references; an independent comparison found no unexplained text loss. Confirmed metadata, link, and content defects were corrected, ten imported placeholder skills received source-informed workflows, and catalog auditing and routing regressions were added. No existing skill was deleted or renamed.

Current generated indexes contain 1,983 skills (390 Tier 1; 1,593 Tier 2). The catalog audit reports zero structural findings, zero duplicate descriptions, zero exact duplicate-body groups, and 310 review candidates: 309 long-description heuristics and the retained `android_ui_verification` naming outlier. The 7,657 freshness keyword matches are triage candidates, not verified defects. Six compatibility IDs now point to canonical guidance; five are additional alias cases beyond the eight baseline duplicate groups.

The eight duplicate-body groups from the original inventory were resolved through distinct procedures or explicit compatibility pointers while preserving every ID. Six compatibility IDs now resolve to canonical skills; five are additional alias cases beyond the eight baseline groups. The internal communications canonical skill uses its local examples, and legacy example/resource paths remain available where required. The `win11-system-manager` legacy ID is retained, but its metadata and instructions now identify its actual GitHub Spec Kit update scope. The 309 long descriptions have not been manually shortened because they may carry routing terms; this remains a review item. Currentness-sensitive claims outside the specifically corrected skills have not all been checked against live primary sources.

Focused catalog and router verification: 41 tests passed. The unfiltered full suite ran 156 tests and returned three errors: a 60-second `agy agent` timeout and two subprocess integration errors. The host-skipped suite ran 156, with 155 passed and that one test skipped; the filtered AGYOS wrapper passed all 51 checks with that host test skipped. State validation, security scan, generator reproducibility, AGYOS wrapper results, and independent review are recorded in `docs/SKILL_CATALOG_AUDIT_REPORT.md`; remaining runtime and content limits are explicit there.
