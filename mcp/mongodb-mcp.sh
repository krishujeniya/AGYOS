#!/usr/bin/env bash
# MongoDB MCP Server launcher
# Bridges local AI agents with MongoDB databases and MongoDB Atlas clusters.
# Upstream repository: https://github.com/mongodb-js/mongodb-mcp-server
# Auth: Managed via MongoDB Atlas CLI (`atlas`) Service Account credentials.
# Credentials live in ~/.config/mongodb-mcp/credentials (chmod 600).
set -euo pipefail

CREDS_FILE="${MONGODB_MCP_CREDS_FILE:-$HOME/.config/mongodb-mcp/credentials}"

if [[ ! -f "$CREDS_FILE" ]]; then
  echo "ERROR: MongoDB credentials file not found at $CREDS_FILE" >&2
  echo "Authenticate with Atlas CLI ('atlas auth login') and generate credentials." >&2
  exit 1
fi

# Verify strict file permissions (refuse to run if group/other can read)
PERMS=$(stat -c "%a" "$CREDS_FILE")
if [[ "$PERMS" != "600" && "$PERMS" != "400" ]]; then
  echo "ERROR: $CREDS_FILE has insecure permissions ($PERMS). Run: chmod 600 $CREDS_FILE" >&2
  exit 1
fi

# Export credentials safely into environment
set -a
# shellcheck disable=SC1090
source "$CREDS_FILE"
set +a

# Ensure Node and binary paths are in PATH
export PATH="$HOME/.config/nvm/versions/node/v24.11.1/bin:$PATH"

if command -v mongodb-mcp-server >/dev/null 2>&1; then
  exec mongodb-mcp-server "$@"
else
  exec npx -y mongodb-mcp-server "$@"
fi
