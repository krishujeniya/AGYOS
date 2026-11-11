# AGYOS skill catalog audit report

Date: 2026-11-11<br>
Branch: `main`<br>
Baseline revision: `3056ca61d85dfc026c7b8540cbddc97d9a8c3238`

## Scope and conclusion

The approved audit baseline contained 1,982 direct skill entrypoints. The work then added one OpenWhispr skill, so the current catalog contains 1,983 skills. The audit covered the baseline entrypoints, their local Markdown references, catalog metadata and indexes, catalog routing, and current catalog-facing documentation. The flat `.agents/skills/` root was retained; existing IDs were not deleted or renamed.

The current structural checks pass: all 1,983 skills are indexed, all main entrypoints are below 300 lines, no duplicate descriptions remain, and the catalog auditor reports zero structural findings or unresolved local Markdown links. This does not establish that every technical, legal, medical, security, or host-specific claim in every reference is current or correct. The report keeps those content-review limits explicit.

## Work completed

- Moved 613 long `SKILL.md` bodies to skill-local `references/FULL_RUNBOOK.md` files and left concise entrypoints. Independent comparison found 592 byte-identical source bodies after reversing link rewrites; the other 21 have documented metadata, content, safety, or link corrections, with no unexplained truncation.
- Repaired 34 broken local Markdown targets, converted 31 local `file://` links to checkout-relative links, and replaced 27 root-relative vendor documentation paths with direct vendor documentation links.
- Corrected discovery descriptions and closely coupled introductory summaries, including placeholder, duplicate, truncated, and misleading text. The old `agyos-self-improvement` catalog count was removed and its metadata version was incremented.
- Corrected the Azure Key Vault key and secret TypeScript clients, removed an undefined audio-transcriber helper dependency, and separated Node.js material from the Python architect runbook while linking to the Node.js skill.
- Replaced unsupported performance-result language in selected prompt-tuning, debugging, and implementation guides with measurement requirements or clearly labeled examples.
- Rewrote `production-code-audit` so audits are read-only by default, fixes stay within explicit authorization, findings include evidence and coverage limits, and unmeasured performance or compliance claims are not presented as results.
- Replaced ten imported placeholder skills with source-informed task procedures. Resolved all eight duplicate-body groups found in the approved baseline: legacy IDs now have distinct procedures or point to canonical runbooks, and required local assets remain available. Six compatibility IDs now point to canonical guidance; one (`tech-debt-cleanup`) was also part of the baseline duplicate set, so five are additional alias cases. No existing ID was removed.
- Closed the independent review's remaining source-backed accuracy findings: X Articles now checks Premium Plus eligibility, the Spec Kit updater is marked archived with its documented host prerequisites, Speed Reader is limited to Claude Code on macOS, and the scientific-research source metadata uses the canonical repository URL.
- Updated the Azure hosted-agent guide from an obsolete preview class to the current documented `HostedAgentDefinition` and `ContainerConfiguration` pattern, with explicit cloud-cost and deployment approval gates.
- Added the `skill_catalog_maintenance` router domain and frozen catalog-maintenance cases.
- Added `.agents/skills/openwhispr/SKILL.md` from the OpenWhispr repository, quickstart, local-model, privacy, macOS, and MCP documentation. Version 1.0.2 distinguishes System Audio from optional Screen Recording, Claude Connector OAuth consent from API-key scope selection, and explains that a read-only OAuth smoke test does not narrow permissions. Its frozen task case resolves to `openwhispr`.
- Replaced all 28 legacy Remotion Markdown rule bodies with exact compatibility pointers to canonical rules. Retained the three duplicate TSX examples at legacy paths and tested their byte equality for link compatibility.
- Updated current catalog counts and qualified skill-discovery claims in current-facing documentation, including the README, AGENTS, docs homepage, site landing page, and tracker. Marked the security threat model's old inventory as a dated baseline and added the current count without claiming the model was re-audited. Historical handoffs and the existing faceless-video work were preserved.

## Catalog measurements

`python3 -B scripts/audit_skill_catalog.py --json` scanned 1,983 skills and reported:

- Structural findings: **0**.
- Duplicate description groups: **0**.
- Main entrypoints at or above 300 lines: **0**.
- Review candidates: **310** — 309 descriptions longer than the auditor's 300-character heuristic and the retained `android_ui_verification` underscore ID.
- Exact duplicate-body groups: **0**. All eight groups from the 1,982-skill baseline and the identified near-duplicate aliases were reviewed; the final scanner found none.
- Freshness keyword candidates: **7,657**. These are keyword matches for manual triage, not verified defects or individually checked claims.

The eight baseline overlap groups were: `agents-v2-py` / `hosted-agents-v2-py`; `brand-design-system` / `brand-guidelines-community`; `codebase-tech-debt` / `tech-debt-cleanup`; `context-restore` / `refactor-context-restore`; `diagnostics-analysis` / `error-analysis`; `doc-generator` / `documentation-generation-doc-generate`; `error-multi-review` / `perf-test-review`; and `internal-comms-community` / `internal-team-communications`. Overlaps with different task triggers retain distinct procedures; compatibility IDs point to one canonical runbook. Compatibility pointers cover `brand-guidelines`, `tech-debt-cleanup` (also in the baseline set), the three `fp-*` IDs, and `remotion-best-practices`. The internal communications canonical runbook uses the four examples stored beside it; legacy resource paths remain as pointers. All IDs and local compatibility assets remain available.

The 309 long descriptions remain for review because length alone does not show which routing terms should be removed. The ID `android_ui_verification` remains because it is referenced by the router and frozen tests. The mismatched legacy ID `win11-system-manager` now states its actual Spec Kit scope in metadata and body.

## Generated catalog state

- Physical skills: **1,983**.
- Complete manifest: **1,983** entries.
- Tier 1: **390** entries.
- Tier 2: **1,593** entries.
- Documentation catalog: **1,983** entries.
- Tier 1 membership is a subset of the complete manifest.
- The second generation pass reproduced all eight output artifacts byte-for-byte.

## Verification evidence

| Check | Result |
| --- | --- |
| `python3 -B scripts/audit_skill_catalog.py --json` | 1,983 scanned; 0 structural findings; 0 duplicate descriptions; 0 duplicate-body groups |
| `python3 -B -m unittest scripts.tests.test_skill_catalog scripts.tests.test_skill_routing -v` | 41 passed |
| Unfiltered `python3 -B -m unittest discover -s scripts/tests -v` | 156 run; 153 passed; 3 errors: `agy agent` exceeded 60 seconds, CLI round-trip exceeded 30 seconds, and MCP round-trip returned an error payload without `primary_skill` |
| Full Python suite with the host `agy` availability probe disabled | 156 run; 155 passed; 1 skipped (the host CLI integration test) |
| `python3 scripts/build_tiered_skills_manifest.py` | 1,983 total; 390 Tier 1; 1,593 Tier 2 |
| `python3 scripts/build_docs_data.py` | 1,983 documentation entries generated |
| Re-run both generators and compare eight output hashes | Byte-identical |
| `bash scripts/agyos-verify.sh` without host-test skip | Latest run: 50 passed, 1 failed; embedded full suite failed only on the non-terminating `agy agent` test. An earlier run also missed the MCP find-skill output check; direct JSON-RPC and the final wrapper rerun passed it. |
| `bash scripts/agyos-verify.sh` with host `agy` availability masked only during unittest discovery | 51 passed, 0 failed; embedded suite skips the single host-dependent CLI test |
| `bash bin/state-validate.sh` | Exit 0 |
| `bash bin/gate-check.sh` | Exit 0 during IMPLEMENT; not rerun in VERIFY because the commit gate intentionally waits for HITL sign-off |
| `bash .agents/skills/agyos-scout/scripts/scan-security.sh` | Pass; no secrets found |
| `git diff --check` | Pass |
| Independent read-only review | Confirmed the permission corrections, version assertion, 28 exact Remotion pointers and targets, tech-debt pointer, and retained TSX asset equality |

The filtered full-suite run and filtered AGYOS wrapper used a temporary `sitecustomize` shim that disabled only `shutil.which("agy")` during unittest discovery, causing the existing `skipUnless` host integration case to be skipped. No test file was changed to obtain that result. One unfiltered full-suite run had two additional subprocess integration errors; the later unfiltered AGYOS wrapper run had only the host CLI error, while the filtered rerun and focused routing tests passed. Do not treat those unfiltered errors as successful checks.

## Remaining verification limits

- The 309 long-description candidates need individual routing-quality review; the length heuristic alone is not a defect.
- The 7,657 freshness-keyword hits have not been individually source-checked. Currentness-sensitive claims beyond the specific fixes above remain unverified.
- Historical documents preserve their baseline counts. The current inventory is 1,983 skills; the threat-model inventory note updates only its count and does not claim that its 2026-11-08 threat analysis was re-audited.
- Skill instructions were not executed through each supported host. Local routing tests prove selection and delivery behavior only.
- The `.agents/state/decisions/drafts/20261111-111600-push-main.sh` diff and existing video-skill edits were present before this milestone and are protected baseline work, not part of this audit's changes.
- The standard full-suite run recorded one host CLI timeout and two subprocess integration errors; the later filtered run passed all other tests and explicitly skipped only the host-dependent CLI test. The unfiltered AGYOS wrapper recorded the same host-test limit; its final filtered run passed all 51 checks. This audit does not execute every skill through each supported runtime.

## Verification walkthrough (Quiz-Me)

1. **Design:** Why does the OpenWhispr runbook check Dictation, Note Recording, and Audio Upload separately? **Answer:** The product documents independent speech-to-text paths and data choices, so a local setting for one activity does not prove the other two stay on-device.
2. **Edge case:** If dictation is local but an audio upload uses cloud processing, what should be assumed? **Answer:** The upload may still send audio to the cloud; verify that activity's own engine and data setting before use.
3. **Change impact:** What catalog indexes changed with OpenWhispr? **Answer:** One new Tier 2 ID raises the current total to 1,983; Tier 1 remains 390 and Tier 2 becomes 1,593. The frozen routing case selects `openwhispr`.

The operator explicitly approved commit and GitHub push on 2026-11-11. At this report revision, publication is pending; deployment has not been requested.
