#!/usr/bin/env bash
# Google Flow MCP Server launcher
# Source: ParkSangGwon/google-flow-mcp
# Reuses authenticated session and cookies from current Chrome profile
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${SCRIPT_DIR}/../integrations/google-flow-mcp"

export FLOW_MCP_CHROME_PATH="${FLOW_MCP_CHROME_PATH:-${SCRIPT_DIR}/../bin/obscura}"
export FLOW_MCP_USER_DATA_DIR="${FLOW_MCP_USER_DATA_DIR:-$HOME/.obscura-flow-profile}"
export FLOW_MCP_PROFILE_DIRECTORY="${FLOW_MCP_PROFILE_DIRECTORY:-Default}"
export FLOW_MCP_CDP_PORT="${FLOW_MCP_CDP_PORT:-9333}"
export FLOW_MCP_STATE_DIR="${FLOW_MCP_STATE_DIR:-$HOME/.google-flow-mcp}"
export FLOW_MCP_HEADLESS="true"
export FLOW_MCP_USE_OBSCURA="1"

# Ensure headless CDP endpoint is reachable via Obscura; never launch Chrome
if ! curl -s -m 1 "http://127.0.0.1:${FLOW_MCP_CDP_PORT}/json/version" >/dev/null 2>&1; then
    bash "${SCRIPT_DIR}/../bin/obscura" cdp --port "${FLOW_MCP_CDP_PORT}" >/dev/null 2>&1 &
    sleep 1
fi

if [[ -f "${REPO_DIR}/dist/cli.js" ]]; then
    exec node "${REPO_DIR}/dist/cli.js" "${@:-serve}"
elif command -v google-flow-mcp >/dev/null 2>&1; then
    exec google-flow-mcp "${@:-serve}"
else
    exec npx -y @park-sang-gwon/google-flow-mcp "${@:-serve}"
fi
