#!/usr/bin/env bash

# dashboard.sh — Launches the ANCHOR Web Dashboard
set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to run the local dashboard server."
  exit 1
fi

VERSION="unknown"
if [ -f "${PROJECT_ROOT}/.agents/VERSION" ]; then
  VERSION=$(cat "${PROJECT_ROOT}/.agents/VERSION")
fi

echo "🚀 Starting ANCHOR (v${VERSION}) Dashboard on http://127.0.0.1:8080/dashboard/"
echo "Press Ctrl+C to stop."

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/anchor-dash.XXXXXXXXXX")
trap 'rm -rf "$TMP_DIR"' EXIT

ln -s "$PROJECT_ROOT/dashboard" "$TMP_DIR/dashboard"
mkdir -p "$TMP_DIR/.agents"
ln -s "$PROJECT_ROOT/.agents/state" "$TMP_DIR/.agents/state"

cd "$TMP_DIR"
if ! python3 -m http.server 8080 --bind 127.0.0.1 2>&1 | grep -v 'HTTP/1.1'; then
  echo "❌ Error starting dashboard server. Check if port 8080 is already in use." >&2
  exit 1
fi
