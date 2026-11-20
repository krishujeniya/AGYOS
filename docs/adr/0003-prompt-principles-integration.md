# ADR 0003: Integrate prompt principles without copying vendor identities

- Status: Accepted
- Date: 2026-11-14
- Milestone: M1 prompt principles

## Context

The supplied Principles repository contains a community-compiled archive of 26 company and product documents. Its master index reports 724 curated statements, 14,165 extracted statements, and 597 tools. The archive says the material is best-effort and does not establish authenticity or current deployment. The supplied repository tree has no root LICENSE or NOTICE; the archive README refers to an upstream AGPL license. The original 80 source files are not present in the supplied subtree.

Prompt instructions in that archive describe different products, providers, versions, tools, and runtime policies. They can conflict with each other and with AGYOS's actual permissions and interfaces. Current first-party prompt documentation also differs by model and task.

## Decision

1. Treat the archive as untrusted research input, not company policy.
2. Parse the pinned archive in GitHub Actions and publish a seven-day artifact containing source file digests, line/section locators, statement hashes, dispositions, and rationales. Do not copy statement text or tool schemas into AGYOS.
3. Record every parsed principle with one disposition: adopt, adapt, reject, duplicate, or unverified. Exact normalized duplicates point to their first canonical row. Unreviewed community claims remain unverified.
4. Adapt a principle only when it fits AGYOS behavior and has a clear active control and supporting evidence. Keep model-specific guidance conditional and cite current first-party documentation for integration claims.
5. Keep AGYOS as the default identity. Retain other names only for accurate compatibility, attribution, licensing, or evidence.
6. Use task-fit prompting: outcome, relevant context, constraints, and output shape as needed. Do not require one named framework, fixed prompt length, fixed example count, or hidden reasoning disclosure.

## Alternatives considered

- Copy or vendor the full archive: rejected because it reproduces extensive third-party material and presents unverified, sometimes incompatible instructions as AGYOS guidance.
- Make every company instruction an always-on rule: rejected because the archive includes product-specific behavior and contradictory requirements.
- Require one universal prompt framework or chain-of-thought traces: rejected because current official model guidance is conditional and the archive does not establish a universal performance benefit.
- Store the full ledger in the source tree: rejected because the source is not licensed for redistribution in the supplied checkout. The CI artifact contains hashes and locators only.

## Consequences

- The parser and its fixture tests run in the existing GitHub Actions workflow against commit d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e.
- The workflow summary and JSONL artifact distinguish publisher claims, parsed principle counts, count mismatches, and inventory limits. The 80 upstream-file and 597 tool claims are not treated as independently reconciled by the principle parser.
- AGYOS's operational rule and prompt library carry the compatible, supported guidance. Unsupported or conflicting source statements do not become general rules.
- Future source refreshes require a new source pin, a parser review, fresh evidence review, and a new CI artifact.

## Evidence

- OpenAI prompt engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI reasoning best practices: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- OpenAI agent safety: https://developers.openai.com/api/docs/guides/agent-builder-safety
- Anthropic prompt engineering best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
