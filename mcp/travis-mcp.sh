#!/usr/bin/env bash
# Travis CI MCP launcher
# Reads Travis CI token from ~/.config/travis-mcp/token (chmod 600) or TRAVIS_CI_TOKEN env var.
# Does not persist tokens in code or VCS repositories.
set -euo pipefail

TOKEN_FILE="${TRAVIS_MCP_TOKEN_FILE:-$HOME/.config/travis-mcp/token}"

if [[ -n "${TRAVIS_CI_TOKEN:-}" ]]; then
  TOKEN="$TRAVIS_CI_TOKEN"
elif [[ -f "$TOKEN_FILE" ]]; then
  PERMS=$(stat -c "%a" "$TOKEN_FILE" 2>/dev/null || stat -f "%Op" "$TOKEN_FILE" 2>/dev/null || echo "600")
  TOKEN=$(cat "$TOKEN_FILE")
else
  echo "ERROR: TRAVIS_CI_TOKEN is not set and token file not found at $TOKEN_FILE" >&2
  echo "Setup: mkdir -p ~/.config/travis-mcp && echo -n 'your_token' > ~/.config/travis-mcp/token && chmod 600 ~/.config/travis-mcp/token" >&2
  exit 1
fi

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: Travis token is empty." >&2
  exit 1
fi

export TRAVIS_API_TOKEN="$TOKEN"
export TRAVIS_API_URL="${TRAVIS_API_URL:-https://api.travis-ci.com}"

exec node "/home/ai/Documents/projects/Freelance/AGYOS/mcp/mcp-travis/dist/index.js"
