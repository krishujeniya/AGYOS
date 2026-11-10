#!/usr/bin/env bash
# Kaggle MCP launcher
# Reads the Kaggle Bearer token from ~/.config/kaggle-mcp/token (chmod 600).
# No tokens are stored in any repository or agy config file.
#
# To rotate the token: echo -n "KGAT_newtoken" > ~/.config/kaggle-mcp/token
set -euo pipefail

TOKEN_FILE="${KAGGLE_MCP_TOKEN_FILE:-$HOME/.config/kaggle-mcp/token}"

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "ERROR: Kaggle token file not found at $TOKEN_FILE" >&2
  echo "Create it: echo -n 'KGAT_yourtoken' > $TOKEN_FILE && chmod 600 $TOKEN_FILE" >&2
  exit 1
fi

# Verify file permissions — refuse to run if readable by group/other
PERMS=$(stat -c "%a" "$TOKEN_FILE")
if [[ "$PERMS" != "600" && "$PERMS" != "400" ]]; then
  echo "ERROR: $TOKEN_FILE has insecure permissions ($PERMS). Run: chmod 600 $TOKEN_FILE" >&2
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: Token file $TOKEN_FILE is empty." >&2
  exit 1
fi

exec npx -y mcp-remote https://www.kaggle.com/mcp \
  --header "Authorization: Bearer $TOKEN"
