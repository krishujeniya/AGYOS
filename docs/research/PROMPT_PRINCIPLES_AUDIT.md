# Prompt principles archive audit

Status: source interpretation documented; exact parser reconciliation is pending a corrected milestone GitHub Actions run.

The first exact-revision attempt, [CI run 43572120201](https://github.com/krishujeniya/AGYOS/actions/runs/43572120201) on `dbb6f8df3c352384a8543c8908aab5a28082bc19`, failed before reconciliation. Its parser recognized 724 curated entries but no extracted entries because it expected an exact exhaustive heading and unbulleted count metadata. That zero is a parser-format failure, not evidence that the archive contains no extracted statements. The follow-up accepts the observed source format; all counts remain pending until its exact-run artifact is reviewed.

## Source and provenance

- Supplied source: [Principles Prompt archive](https://github.com/krishujeniya/Principles/tree/d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e/Prompt) at commit d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e.
- The checked-out repository tree contains 26 merged company/product Markdown documents, a README, and a master index. The original source files listed by the publisher are not in this subtree.
- The index reports 80 source files, 724 curated statements, 14,165 extracted statements, 14,889 combined statements, and 597 tools. These values are publisher claims until the CI parser reconciles the principle counts. The parser does not independently reconcile the absent 80 source files or the tool inventory.
- The archive describes itself as a community compilation and says its principle lists are best-effort, paraphrased, and not proof of current company policy. The supplied repository tree has no root LICENSE or NOTICE. Its README refers to an AGPL license in the upstream collection. AGYOS does not copy archive prose or tool schemas.

## Statement units and count checks

The CI parser counts two declared classes in each company document:

1. Curated statements: individually numbered entries between the document's Principle catalog heading and its repository-source or Part II boundary.
2. Extracted statements: top-level, non-keyword list items beneath the Complete Unified Company-Wide Principles by Domain heading and before the tool inventory heading.

Each record stores its source commit, repository-relative path, source-file SHA-256, section, line number, source ordinal, statement SHA-256, and disposition. It does not store the statement text. The parser also compares per-file metadata and category counts to parsed records, then compares aggregate counts to the master index. It writes the ledger and count report under the CI runner's temporary directory and uploads them as the prompt-principles-ledger artifact for seven days.

These units account for the archive's declared principle entries, not every instruction in the absent upstream files. A mismatch or unrecognized section is reported and fails the parser step. No completeness claim is valid until the exact-run artifact shows matching per-file, category, and aggregate principle counts.

## Dispositions and AGYOS changes

- Four reviewed curated entries are adapted into AGYOS controls: task-fit response detail and treatment of retrieved content as untrusted task data. Their ledger rows include control paths and current first-party evidence.
- Exact normalized duplicate statements point to the first canonical ledger row.
- Other community-compiled statements default to unverified unless a reviewed disposition says otherwise. This does not mean every archived instruction is safe, compatible, or active company policy.
- The operational rule is task-fit: specify outcome, relevant context, constraints, and output shape as needed; use examples and structure only when they help; do not request hidden reasoning traces or assert universal performance gains.
- Active AGYOS prompt identity is AGYOS. Company personas and company-specific aesthetics were removed from general prompt templates. Product names remain only where a real integration requires them, where upstream attribution requires them, or in evidence citations. The Stitch-specific enhancement skill retains its compatibility identity.
- The prompt documentation reference path is retained as a pointer to the canonical library.

## Evidence for transferred guidance

- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) describes prompt roles, context, formatting, examples, and evaluation, while noting that needs differ by model.
- [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) advises specific outcome and constraint instructions and notes that step-by-step prompting can fail to help some reasoning models.
- [OpenAI agent safety](https://developers.openai.com/api/docs/guides/agent-builder-safety) describes prompt-injection risks from untrusted input and recommends keeping external data from directly controlling agent behavior.
- [OpenAI computer-use safety](https://developers.openai.com/api/docs/guides/tools-computer-use) treats third-party page and tool content as untrusted and distinguishes it from user permission.
- [Anthropic prompt engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) recommends clear instructions and relevant examples while describing behavior that varies by model.

These sources support narrow, conditional techniques. They do not verify the archive as company policy or establish one prompt format that is best for every model.

## Remaining limits

- Parsed counts, disposition totals, source-file digests, and the exact Actions run are recorded by the milestone workflow summary and its artifact. They remain pending until that workflow completes on the reviewed revision.
- The upstream files and license text are absent from the supplied checkout. This audit does not make a legal conclusion about the source collection.
- Community summaries can omit instructions or flatten context-specific differences. The parser cannot restore omitted source material or establish authenticity.
