---
name: gemini-notebook
description: Comprehensive operational runbook for Google Gemini Notebook (formerly NotebookLM) programmatic access via CLI (nlm) and MCP server (gemini-notebook-mcp), based on jacob-bd/gemini-notebook-mcp-cli. Source-grounded queries, multi-format sources, automated research, studio audio/video artifacts, and Google Workspace exports.
---

# Gemini Notebook Operations Runbook

This runbook defines patterns for interacting with Google Gemini Notebook (formerly Google NotebookLM) programmatically using the `gemini-notebook-mcp` FastMCP server and the `nlm` command-line interface based on [`jacob-bd/gemini-notebook-mcp-cli`](https://github.com/jacob-bd/gemini-notebook-mcp-cli).

## Core Capabilities

- **Source-Grounded Extraction**: Query notebooks with direct citations mapped to uploaded source text, minimizing hallucinations.
- **Multimodal Ingestion**: Ingest web URLs, raw text, local files (PDFs, text files), and Google Drive assets.
- **Automated Research Pipelines**: Run Web or Drive research tasks in fast or deep mode to discover and import new sources.
- **Studio Artifacts**: Synthesize notebook contents into Audio Overviews, video scripts, infographics, slide decks, study guides, quizzes, and interactive reports.
- **Google Workspace Export**: Export structured tables to Google Sheets and reports to Google Docs.

## Prerequisites and Setup

Follow [references/AUTHENTICATION.md](references/AUTHENTICATION.md) for credential setup.

1. Ensure session cookies exist in `~/.config/gemini-notebook-mcp/cookies` (file permissions `600`) or set the `NOTEBOOKLM_COOKIES` environment variable.
2. The launcher script [mcp/gemini-notebook-mcp.sh](../../../mcp/gemini-notebook-mcp.sh) manages headless execution and loopback binding.
3. Access via AGYOS CLI:
   ```bash
   bin/agyos nlm <command>
   bin/agyos gemini-notebook <command>
   ```

## Standard Workflows

### 1. Source-Grounded Document Research

When tasked with querying documentation or proprietary materials:

1. **List available notebooks**:
   ```bash
   bin/agyos nlm notebook list
   ```
2. **Retrieve or verify notebook contents**:
   ```bash
   bin/agyos nlm notebook get <notebook_id>
   ```
3. **Execute targeted query**:
   ```bash
   bin/agyos nlm chat query <notebook_id> "Specify the API contract requirements for authentication tokens."
   ```
4. **Extract specific source text**: If a query returns ambiguous citations, inspect the full underlying text with:
   ```bash
   bin/agyos nlm source content <notebook_id> <source_id>
   ```

### 2. Deep Research Discovery

When initiating research on a new topic:

1. **Launch automated research**:
   ```bash
   bin/agyos nlm research start --query "Distributed consensus algorithms comparative benchmarks" --source web --mode deep
   ```
2. **Monitor task progress**: Poll the returned `task_id`:
   ```bash
   bin/agyos nlm research status <task_id>
   ```
3. **Import candidate sources**: Once the research status is completed, import selected sources into a notebook:
   ```bash
   bin/agyos nlm research import <task_id> <notebook_id>
   ```

### 3. Studio Synthesis and Audio Overviews

1. Request user confirmation before initiating studio generation:
   - Creating Audio Overviews, videos, or slide decks consumes quota and takes several minutes to render.
2. Trigger generation with confirmation:
   ```bash
   bin/agyos nlm studio create audio <notebook_id> --confirm
   ```
3. Check completion status:
   ```bash
   bin/agyos nlm studio status <notebook_id>
   ```
4. Download the generated artifact:
   ```bash
   bin/agyos nlm studio download <notebook_id> <artifact_id> --output-dir ./artifacts
   ```

## Operational Safety Invariants

1. **Mandatory Confirmation**: Irreversible deletions (`notebook_delete`, `source_delete`, `chat_delete`, `studio_delete`) and resource-heavy studio generations (`studio_create`, `studio_revise`) require explicit confirmation. Never set `confirm=True` without operator approval.
2. **Headless Execution**: Never attempt to launch graphical desktop browsers on server environments. Authentication uses saved cookies or CDP extraction via [mcp/gemini-notebook-mcp.sh](../../../mcp/gemini-notebook-mcp.sh).
3. **Credential Isolation**: Keep cookies inside `~/.config/gemini-notebook-mcp/cookies` with mode `600`. Never commit session tokens or cookies to git.

## Reference Documentation

- [references/AUTHENTICATION.md](references/AUTHENTICATION.md): Detailed guide for cookie extraction and protected keychain storage.
- [references/CLI_GUIDE.md](references/CLI_GUIDE.md): Complete list of `nlm` subcommands and arguments.
- [references/MCP_TOOLS_REFERENCE.md](references/MCP_TOOLS_REFERENCE.md): Full inventory of all 53 FastMCP tools and schemas.
