#!/usr/bin/env bash
# Obscura MCP Server Launcher for AGYOS
# Native headless browser engine written in Rust (h4ckf0r0day/obscura).
# Strictly headless execution: never opens a GUI window.
# Drop-in replacement for Chrome DevTools Protocol (CDP) & AI agent browsing.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Strict headless environment enforcement
export HEADLESS=1
export OBSCURA_HEADLESS=1
export DISPLAY=""
export PUPPETEER_HEADLESS=true
export PLAYWRIGHT_HEADLESS=true

# 1. Local compiled Obscura binary candidate check
for candidate in \
  "$(command -v obscura 2>/dev/null || true)" \
  "${HOME}/.cargo/bin/obscura" \
  "${HOME}/.local/bin/obscura" \
  "/usr/local/bin/obscura" \
  "${PROJECT_ROOT}/bin/obscura-bin"; do
  if [[ -n "$candidate" && -x "$candidate" ]]; then
    exec "$candidate" mcp "$@"
  fi
done

# 2. Containerized runtime via official Docker image (h4ckf0r0day/obscura)
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    exec docker run --rm -i \
      -e "OBSCURA_HEADLESS=1" \
      -e "HEADLESS=1" \
      h4ckf0r0day/obscura mcp "$@"
  fi
fi

# 3. Dedicated AGYOS FastMCP headless daemon
exec node "${SCRIPT_DIR}/obscura-server.cjs" "$@"
