#!/usr/bin/env bash
# Gemini Notebook (formerly NotebookLM) MCP Server & CLI launcher
# Upstream: https://github.com/jacob-bd/gemini-notebook-mcp-cli
# Provides programmatic access to Gemini Notebook via FastMCP and the 'nlm' CLI.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${NOTEBOOKLM_CONFIG_DIR:-$HOME/.config/gemini-notebook-mcp}"
TOKEN_FILE="${NOTEBOOKLM_TOKEN_FILE:-$CONFIG_DIR/cookies}"
LEGACY_TOKEN_FILE="$HOME/.config/notebooklm-mcp/cookies"

# Resolve cookies from environment variable, current config, or legacy config
if [[ -z "${NOTEBOOKLM_COOKIES:-}" ]]; then
  if [[ -s "$TOKEN_FILE" ]]; then
    export NOTEBOOKLM_COOKIES="$(cat "$TOKEN_FILE")"
  elif [[ -s "$LEGACY_TOKEN_FILE" ]]; then
    export NOTEBOOKLM_COOKIES="$(cat "$LEGACY_TOKEN_FILE")"
  fi
fi

# Operating defaults: loopback bind and bounded headless recovery
export NOTEBOOKLM_AUTH_MAX_HEADLESS_FAILURES="${NOTEBOOKLM_AUTH_MAX_HEADLESS_FAILURES:-3}"
export NOTEBOOKLM_HL="${NOTEBOOKLM_HL:-en}"

MODE="${1:-mcp}"
if [[ "$MODE" == "cli" || "$MODE" == "nlm" ]]; then
  shift || true
  if command -v nlm >/dev/null 2>&1; then
    exec nlm "$@"
  else
    exec uvx --from notebooklm-mcp-cli nlm "$@"
  fi
fi

# Run the FastMCP server
if command -v notebooklm-mcp >/dev/null 2>&1; then
  exec notebooklm-mcp "$@"
else
  exec uvx --from notebooklm-mcp-cli notebooklm-mcp "$@"
fi
