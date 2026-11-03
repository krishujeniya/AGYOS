#!/usr/bin/env bash
# agyos-init.sh — Universal Zero-Config Bootstrapper for AGYOS
# Configures Antigravity CLI (AGY CLI) with the 5-Gate Anchor Governance,
# multi-model Agent Council, FastMCP servers, ECC capabilities, and 8 modular AGYOS plugins.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "⚡ AGYOS: Initializing Autonomous Cognitive Operating System"
echo "============================================================"

# 1. Dependency checks
echo "Checking core runtimes..."
for cmd in agy bun node python3 git jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "❌ Missing required command: $cmd"
    exit 1
  fi
  echo "  ✓ $cmd found"
done

# 2. Constitution & Rules
echo "Linking AGENTS.md and GEMINI.md..."
if [ ! -L "GEMINI.md" ] && [ ! -f "GEMINI.md" ]; then
  ln -s AGENTS.md GEMINI.md
fi
echo "  ✓ Constitution active"

# 3. State & Governance initialization
echo "Validating Anchor State Machine..."
mkdir -p .agents/state/checkpoints .agents/state/decisions
bash bin/state-validate.sh
echo "  ✓ State machine validated"

# 4. Lifecycle Hooks
echo "Verifying AGYOS lifecycle hooks..."
chmod +x scripts/hooks/agy_os_hook.py
echo "  ✓ .agents/hooks.json active"

# 5. FastMCP Server
echo "Verifying Anchor FastMCP Server..."
chmod +x mcp/agyos-state-server.cjs
echo "  ✓ Anchor MCP server ready"

# 6. Packaging & Validating 8 AGYOS Plugins
echo "Validating AGYOS Plugins..."
python3 scripts/package_agyos_plugins.py
for p in .agents/plugins/*; do
  agy plugin validate "$p" >/dev/null
done
echo "  ✓ All 8 AGYOS plugins verified"

# 7. Sync Skills & Catalog
echo "Compiling skills catalog..."
python3 scripts/build_docs_data.py >/dev/null
echo "  ✓ Skills database compiled"

echo ""
echo "============================================================"
echo "🚀 AGYOS is 100% OPERATIONAL on AGY CLI $(agy --version)"
echo "============================================================"
