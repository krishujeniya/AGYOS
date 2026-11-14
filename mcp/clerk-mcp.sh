#!/usr/bin/env bash
# Clerk Agent Toolkit MCP launcher
# Reads secret key from CLERK_SECRET_KEY env var or ~/.config/clerk-mcp/token
set -euo pipefail

TOKEN_FILE="${CLERK_MCP_TOKEN_FILE:-$HOME/.config/clerk-mcp/token}"

if [[ -n "${CLERK_SECRET_KEY:-}" ]]; then
  KEY="$CLERK_SECRET_KEY"
elif [[ -f "$TOKEN_FILE" ]]; then
  KEY=$(cat "$TOKEN_FILE")
else
  echo "ERROR: CLERK_SECRET_KEY not set and token file not found at $TOKEN_FILE" >&2
  echo "Setup: echo -n 'sk_live_...' > ~/.config/clerk-mcp/token && chmod 600 ~/.config/clerk-mcp/token" >&2
  exit 1
fi

if [[ -z "$KEY" ]]; then
  echo "ERROR: Clerk secret key is empty." >&2
  exit 1
fi

exec npx -y @clerk/agent-toolkit --secret-key "$KEY" --tools "*"
