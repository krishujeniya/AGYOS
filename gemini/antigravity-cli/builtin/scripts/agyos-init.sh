#!/usr/bin/env bash
# agyos-init.sh — Universal Zero-Config Bootstrapper for AGYOS
# Configures Antigravity CLI (AGY CLI) with the 5-Gate AGYOS Governance,
# multi-model Agent Council, FastMCP servers, ECC capabilities, and 8 modular AGYOS plugins.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "⚡ AGYOS: Initializing Autonomous Cognitive Operating System"
echo "============================================================"

# 1. Dependency checks
echo "Checking core runtimes..."
for cmd in agy bun node uv git jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "❌ Missing required command: $cmd"
    exit 1
  fi
  echo "  ✓ $cmd found"
done

# 2. Materialize AGY host manifests before discovery or packaging.
(cd ../.. && node gemini/antigravity-cli/scripts/materialize-documents.mjs)

# 3. State & Governance initialization
echo "Validating AGYOS State Machine..."
mkdir -p state/checkpoints state/decisions
bash bin/state-validate.sh
echo "  ✓ State machine validated"

# 4. Lifecycle Hooks
echo "Verifying AGYOS lifecycle hooks..."
chmod +x scripts/hooks/agy_os_hook.py
echo "  ✓ hooks.json active"

# 5. FastMCP Server
echo "Verifying AGYOS FastMCP Server..."
chmod +x mcp/agyos-state-server.cjs mcp/state-server.cjs
echo "  ✓ AGYOS MCP server ready"

# 6. Packaging & Validating 8 AGYOS Plugins
echo "Validating AGYOS Plugins..."
uv run --no-project scripts/package_agyos_plugins.py
for p in ../config/plugins/*; do
  agy plugin validate "$p" >/dev/null
done
echo "  ✓ All 8 AGYOS plugins verified"

# 7. Sync Skills & Catalog
echo "Compiling skills catalog..."
uv run --no-project scripts/build_docs_data.py >/dev/null
echo "  ✓ Skills database compiled"

echo ""
echo "============================================================"
echo "✅ AGYOS core initialization and plugin validation completed on AGY CLI $(agy --version)"
echo "Note: third-party channels, encrypted storage, host permissions and production workflows require separate verification."
echo "============================================================"
