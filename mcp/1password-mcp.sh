#!/usr/bin/env bash
# 1Password MCP Server Launcher
# Reads service account token from OP_SERVICE_ACCOUNT_TOKEN or ~/.config/1password-mcp/token
set -euo pipefail

TOKEN_FILE="${OP_MCP_TOKEN_FILE:-$HOME/.config/1password-mcp/token}"

if [[ -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]]; then
  export OP_SERVICE_ACCOUNT_TOKEN="$OP_SERVICE_ACCOUNT_TOKEN"
elif [[ -f "$TOKEN_FILE" ]]; then
  export OP_SERVICE_ACCOUNT_TOKEN="$(cat "$TOKEN_FILE")"
fi

exec node "/home/ai/Documents/projects/Freelance/AGYOS/mcp/1password-mcp/server.js"
