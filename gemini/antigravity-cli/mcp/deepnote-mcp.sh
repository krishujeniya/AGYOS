#!/usr/bin/env bash
# Deepnote MCP launcher
# Reads API key from DEEPNOTE_API_KEY env var or ~/.config/deepnote-mcp/token
set -euo pipefail

TOKEN_FILE="${DEEPNOTE_MCP_TOKEN_FILE:-$HOME/.config/deepnote-mcp/token}"

if [[ -n "${DEEPNOTE_API_KEY:-}" ]]; then
  KEY="$DEEPNOTE_API_KEY"
elif [[ -f "$TOKEN_FILE" ]]; then
  KEY=$(cat "$TOKEN_FILE")
else
  echo "ERROR: DEEPNOTE_API_KEY not set and token file not found at $TOKEN_FILE" >&2
  echo "Setup: echo -n 'your_api_key' > ~/.config/deepnote-mcp/token && chmod 600 ~/.config/deepnote-mcp/token" >&2
  exit 1
fi

if [[ -z "$KEY" ]]; then
  echo "ERROR: Deepnote API key is empty." >&2
  exit 1
fi

export DEEPNOTE_API_KEY="$KEY"
exec npx -y @deepnote/mcp
