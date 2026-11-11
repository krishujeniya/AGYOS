---
name: vector-semantic-file-search
description: "Find files by meaning with the Vexor semantic-search CLI. Use when installed and configured; inspect the embedding provider and data boundary before indexing source files."
risk: safe
source: https://github.com/scarletkc/vexor
date_added: '2026-02-27'
---

# Vexor semantic file search

Use Vexor for natural-language search over a project index when its CLI is already installed and configured.

## Workflow

1. Check that `vexor` is available and inspect its installed-version help. Do not install it automatically.
2. Before indexing, inspect the project's `.vexorignore` and relevant configuration without printing API keys. Confirm whether embeddings or reranking use a remote provider; ask before sending private source files to any external service.
3. Search an existing index with the documented query command. The upstream README shows `vexor "query"` and `vexor search` as search entrypoints; check the current [CLI reference](https://github.com/scarletkc/vexor) for exact flags.
4. Build or refresh an index only when requested. Limit the indexed paths and exclude secrets, generated files, and unrelated data.
5. Treat results as candidate file matches. Open and verify the referenced files before relying on search snippets.

Vexor documents configurable embedding and reranking providers, including offline local-model use. Do not assume the current project is offline or that an index exists until its configuration is checked.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
