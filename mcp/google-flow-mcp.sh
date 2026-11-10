#!/usr/bin/env bash
# Google Flow MCP Server launcher
# Source: ParkSangGwon/google-flow-mcp
# Reuses authenticated session and cookies from current Chrome profile
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${SCRIPT_DIR}/../integrations/google-flow-mcp"

export FLOW_MCP_CHROME_PATH="${FLOW_MCP_CHROME_PATH:-/usr/bin/google-chrome}"
export FLOW_MCP_USER_DATA_DIR="${FLOW_MCP_USER_DATA_DIR:-$HOME/.google-flow-chrome}"
export FLOW_MCP_PROFILE_DIRECTORY="${FLOW_MCP_PROFILE_DIRECTORY:-Default}"
export FLOW_MCP_CDP_PORT="${FLOW_MCP_CDP_PORT:-9333}"
export FLOW_MCP_STATE_DIR="${FLOW_MCP_STATE_DIR:-$HOME/.google-flow-mcp}"
export FLOW_MCP_HEADLESS="${FLOW_MCP_HEADLESS:-true}"

# Synchronize active Google session, cookies, and auth state from current Chrome profile
SRC_DIR="$HOME/.config/google-chrome"
DEST_DIR="${FLOW_MCP_USER_DATA_DIR}"

if [ -d "$SRC_DIR/Default" ]; then
    mkdir -p "$DEST_DIR/Default"
    cp -p "$SRC_DIR/Local State" "$DEST_DIR/" 2>/dev/null || true
    cp -p "$SRC_DIR/Default/Cookies"* "$DEST_DIR/Default/" 2>/dev/null || true
    cp -p "$SRC_DIR/Default/Login Data"* "$DEST_DIR/Default/" 2>/dev/null || true
    cp -p "$SRC_DIR/Default/Preferences" "$DEST_DIR/Default/" 2>/dev/null || true
    cp -pr "$SRC_DIR/Default/Local Storage" "$DEST_DIR/Default/" 2>/dev/null || true
    cp -pr "$SRC_DIR/Default/Session Storage" "$DEST_DIR/Default/" 2>/dev/null || true
fi

exec node "${REPO_DIR}/dist/cli.js" "${@:-serve}"
