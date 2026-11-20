# Prompt principles archive audit

Status: principle-ledger accounting reconciled by GitHub Actions. The audit artifact first passed on implementation commit `98486147dbab917deee345fd4c36498f5901bc01` and was reproduced on evidence commit `9d89d84c333f7fe144d2083c834cd9c6beb8302a` in [CI run 43577287826](https://github.com/krishujeniya/AGYOS/actions/runs/43577287826). The final status-record revision `31b4018d38cfe68cae669f5df689c257ccc8b069` passed CI run [43579658988](https://github.com/krishujeniya/AGYOS/actions/runs/43579658988) and Pages run [43579658930](https://github.com/krishujeniya/AGYOS/actions/runs/43579658930). The ledger contains 14,888 principle rows plus one separately classified metadata row, accounting for the publisher's 14,889 combined source rows with no parser mismatches.

The first exact-revision attempt, [CI run 43572120201](https://github.com/krishujeniya/AGYOS/actions/runs/43572120201) on `dbb6f8df3c352384a8543c8908aab5a28082bc19`, failed before reconciliation. Its parser recognized 724 curated entries but no extracted entries because it expected an exact exhaustive heading and unbulleted count metadata. That zero is a parser-format failure, not evidence that the archive contains no extracted statements.

The second attempt, [CI run 43574183754](https://github.com/krishujeniya/AGYOS/actions/runs/43574183754) on `99c26eb16b79a0ebefa41b98044bf973bbc53dd6`, parsed 724 curated and 14,164 exhaustive principle entries, for 14,888 ledger rows, against the publisher's claim of 14,889 combined rows. The difference was in `ANTHROPIC.md`: section 3.1 declares 129 rows, while it contains 128 non-keyword principles and one keyword metadata bullet at [line 190](https://github.com/krishujeniya/Principles/blob/d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e/Prompt/ANTHROPIC.md#L190).

The audit, [CI run 43576647191](https://github.com/krishujeniya/AGYOS/actions/runs/43576647191) on implementation commit `98486147dbab917deee345fd4c36498f5901bc01`, passed with `publisher_rows_reconciled_with_metadata` and no mismatches. It reports 724 curated and 14,164 exhaustive principle statements (14,888 ledger rows), plus one keyword metadata row, for 14,889 accounted publisher source rows. The artifact records the metadata path, section, line, and SHA-256 without storing its text. Dispositions are 4 adapted and 14,884 unverified. The artifact is retained by Actions for seven days. The evidence-only revision `9d89d84c333f7fe144d2083c834cd9c6beb8302a` passed the same audit in [CI run 43577287826](https://github.com/krishujeniya/AGYOS/actions/runs/43577287826) and deployed in [Pages run 43577287798](https://github.com/krishujeniya/AGYOS/actions/runs/43577287798); its artifact confirms the same counts and disposition totals.

## Source and provenance

- Supplied source: [Principles Prompt archive](https://github.com/krishujeniya/Principles/tree/d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e/Prompt) at commit d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e.
- The checked-out repository tree contains 26 merged company/product Markdown documents, a README, and a master index. The original source files listed by the publisher are not in this subtree.
- The index reports 80 source files, 724 curated statements, 14,165 extracted rows, 14,889 combined rows, and 597 tools. CI reconciled the combined source-row count by separating one keyword metadata row from 14,888 principle statements. The parser does not independently reconcile the absent 80 source files or the tool inventory; the 597-tool count remains a publisher claim.
- The archive describes itself as a community compilation and says its principle lists are best-effort, paraphrased, and not proof of current company policy. The supplied repository tree has no root LICENSE or NOTICE. Its README refers to an AGPL license in the upstream collection. AGYOS does not copy archive prose or tool schemas.

## Statement units and count checks

The CI parser counts two declared classes in each company document:

1. Curated statements: individually numbered entries between the document's Principle catalog heading and its repository-source or Part II boundary.
2. Extracted statements: top-level, non-keyword list items beneath the Complete Unified Company-Wide Principles by Domain heading and before the tool inventory heading.

Keyword metadata bullets are hashed and located in the count summary but are excluded from principle records. This preserves the source row accounting without treating a keyword index as an instruction.

Each principle record stores its source commit, repository-relative path, source-file SHA-256, section, line number, source ordinal, statement SHA-256, and disposition. It does not store the statement text. The parser compares per-file declarations with principle records and separately classified metadata, then reports aggregate principle counts and accounted source-row totals against the master index. It writes the ledger and count report under the CI runner's temporary directory and uploads them as the prompt-principles-ledger artifact for seven days.

These units account for the archive's declared principle entries, not every instruction in the absent upstream files. A mismatch or unrecognized section is reported and fails the parser step. The final exact-run artifact reconciles all 26 company documents and aggregate publisher source rows: 14,888 principle ledger rows and one separately classified metadata row. It does not establish coverage of the 80 absent upstream prompt files.

## Dispositions and AGYOS changes

- Four reviewed curated entries are adapted into AGYOS controls: task-fit response detail and treatment of retrieved content as untrusted task data. Their ledger rows include control paths and current first-party evidence. The other 14,884 principle rows are explicitly unverified.
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

- Parsed counts, disposition totals, and source-file digests are recorded in the [CI artifact](https://github.com/krishujeniya/AGYOS/actions/runs/43577287826). Count reconciliation passed on implementation commit `98486147dbab917deee345fd4c36498f5901bc01` and the evidence-only revision `9d89d84c333f7fe144d2083c834cd9c6beb8302a`.
- The upstream files and license text are absent from the supplied checkout. This audit does not make a legal conclusion about the source collection.
- Community summaries can omit instructions or flatten context-specific differences. The parser cannot restore omitted source material or establish authenticity.
