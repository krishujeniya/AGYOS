# Eight-Source AGYOS Integration Plan

## Scope and baseline

Target: `krishujeniya/AGYOS` at `6d7c6b2593d12d707bb98b7324eeb89070733e3e`. The default branch was `main`. Historical GitHub Actions CI on this exact baseline reported success; no full local checkout, live AGY CLI, installed MCPs, or hardware/cloud credentials were available to this integration session. Preserve the existing six-layer hierarchy, five gates, five pods, decision engine, security hooks and read-only defaults.

The existing manifest at the baseline contains 1,862 physical skills (389 Tier 1, 1,473 Tier 2), 81 agent definitions, 99 workflow entries including non-workflow code, 8 plugin folders, and 10 test-suite entries under `scripts/tests`. The upstream sources remain untrusted. Existing AGYOS skills and rules are authoritative.

## Eight-source integration matrix

| Source | Pinned SHA (prefix) | Proposed and delivered path | Decision | Reason |
| --- | --- | --- | --- | --- |
| x1xhlol/system-prompts-and-models-of-ai-tools | `162db92f` | `agyos-academic-research` + registry | REFERENCE | GPL-3.0 and uncertain prompt authenticity; no prompt injection into host |
| sickn33/agentic-awesome-skills | `828257c3` | `agyos-decision` + registry | REUSE | AGYOS already has a large skill catalog; AAS content has additional licensing exceptions |
| avinash201199/founders-kit | `996e77be` | `agyos-founder-guide` | ENHANCE | Startup reference directory, not executable integration |
| ayush488-glitch/ai-career-planner-skill | `48a4467f` | `interview-coach` | ADAPT | Reuse coaching while removing earnings guarantees and mandatory intake |
| ayush488-glitch/ai-engineering-os | `56caee19` | `ml-engineer` | ADAPT | F1 ready, F2-F4 previews; upstream source license not found |
| garrytan/gstack | `d479c5bf` | `code-reviewer` | ENHANCE | Adapt review/QA process, not Claude/Bun hooks |
| Panniantong/Agent-Reach | `c70ae6da` | `research-ops` + optional Python CLI adapter | ADAPT | Safe, read-only public-channel boundary; authenticated operations excluded |
| microsoft/edge-ai | `48ddff0c` | `ml-engineer` | ADAPT | Azure blueprint references, not automatic provisioning |

The source-of-truth machine-readable record is `integrations/registry/sources.json`. The method in this table classifies the **reviewed top-level integration**, not every upstream file. Every source is represented; that does not mean every upstream feature is usable.

## Filesystem changes and migration

New: `integrations/registry/sources.json`, `agyos_decision/integrations/source_registry.py`, `agyos_decision/integrations/agent_reach_adapter.py`, `scripts/tests/test_external_sources.py`, and documentation under `docs/integrations/`. Modified: existing `agyos_decision/skills_router.py`, `intent_compiler.py`, six existing knowledge-oriented AGYOS runbooks, and README.

There are no new active skill directories, no vendored sources, no AGYOS replacement router, no new hooks, no automatic CLI downloads, and no changed deployment infrastructure. A narrow intent refinement delegates to *existing* physical `SKILL.md` paths only. Existing discovery and the 1,862-skill manifest stay the authority. No generation change is required because the physical catalog is unchanged.

## Rollout / rollback

1. Keep the feature on a separate branch and open a draft PR for review.
2. Run Python compile checks, all Python unit tests, catalog and generated-doc reproducibility, and CI.
3. Verify eight natural-language source cases and negative cases (missing CLI, malformed JSON, duplicate registry IDs, path forgery, unapproved actions).
4. Audit the diff and inspect license/source attribution.
5. Enable optional Agent Reach **only** after the operator verifies official provenance and installation in their own Ubuntu/AGY environment.
6. For rollback, close the draft PR or revert the integration commits; no state migration or upstream files need cleaning.

## Acceptance: bounded, measured outcomes

- Eight pinned source records with a reviewed high-level disposition, license note, evidence path, and explicit limitations.
- Native routing returns existing runbooks with `integration_sources` evidence and `native_skill_routed_not_executed` status, never an execution claim.
- Agent Reach adapter fails closed without an executable and refuses unauthorized operations.
- Regression and CI results are recorded with actual evidence, not assumed.
- Upstream catalogs, credentials, remote actions, and production infrastructure remain inactive.
- Full upstream component-level audit, optional runtime end-to-end tests and live AGY host verification are explicitly **outstanding** rather than falsely marked complete.
