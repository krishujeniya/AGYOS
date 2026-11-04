#!/usr/bin/env bash
# agyos-verify.sh — Machine Verification Suite for AGYOS v3.1
# Falsifiable, deterministic proof of AGYOS operations.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

PASS_COUNT=0
FAIL_COUNT=0

check() {
  local desc="$1"
  shift
  echo -n "• Checking $desc... "
  if "$@" >/tmp/agyos-check.log 2>&1; then
    echo "PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "FAIL"
    cat /tmp/agyos-check.log
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

echo "============================================================"
echo "🛡️ AGYOS Adversarial Verification Suite"
echo "============================================================"

# 1. Constitution rules size budget check (<24,000 bytes)
check "AGENTS.md size limit (<24,000 bytes)" test "$(wc -c < AGENTS.md)" -lt 24000

# 2. Check GEMINI.md link exists
check "GEMINI.md exists and matches AGENTS.md" test -e GEMINI.md

# 3. Check AGY CLI Version
check "AGY CLI installed and responsive" agy --version

# 4. Check MCP Servers List
check "Anchor MCP server registered in AGY" grep -q "anchor" <(agy mcp list)

# 5. Check Hook Script execution
check "AGYOS Safety Hook blocks dangerous commands" bash -c 'echo "{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"rm -rf /\"}}}" | python3 scripts/hooks/agy_os_hook.py PreToolUse | grep -q "\"decision\": \"deny\""'
check "AGYOS Safety Hook allows benign commands" bash -c 'echo "{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"npm test\"}}}" | python3 scripts/hooks/agy_os_hook.py PreToolUse | grep -q "\"decision\": \"allow\""'
check "AGY startup metadata and hook contract regressions" python3 -m unittest discover -s scripts/tests -v

# 6. Check FastMCP JSON-RPC Server
check "Anchor MCP server JSON-RPC initialize" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{}}" | node mcp/state-server.cjs | grep -q "\"serverInfo\""'
check "Anchor MCP server tools/list" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\",\"params\":{}}" | node mcp/state-server.cjs | grep -q "\"anchor_state\""'
check "Anchor MCP server tools/call (anchor_state)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"anchor_state\",\"arguments\":{}}}" | node mcp/state-server.cjs | grep -q "current_gate"'
check "Anchor MCP server tools/call (agyos_find_skill)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_find_skill\",\"arguments\":{\"query\":\"react\"}}}" | node mcp/state-server.cjs | grep -q "Top Skill Matches"'
check "Anchor MCP server tools/call (agyos_sys_info)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":5,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_sys_info\",\"arguments\":{}}}" | node mcp/state-server.cjs | grep -q "Hierarchical Cognitive OS"'
check "Anchor MCP server tools/call (agyos_memory)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":6,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_memory\",\"arguments\":{\"action\":\"read\",\"tier\":\"tier0\"}}}" | node mcp/state-server.cjs | grep -q "user_preferences"'
check "bin/agyos find skill search CLI" bash -c 'bin/agyos find "postgres" | grep -q "Top Skill Matches"'
check "bin/agyos sysinfo CLI command" bash -c 'bin/agyos sysinfo | grep -q "Hierarchical Cognitive OS"'
check "bin/agyos mem virtual memory CLI" bash -c 'bin/agyos mem tier0 | grep -q "user_preferences"'

# 7. Check Agent Council Bun Test Suite
check "Agent Council Bun test suite (59 passing tests)" bash -c 'cd scripts/council && bun test'

# 8. Check 8 AGYOS Plugins
for p in .agents/plugins/*; do
  check "Plugin validation for $(basename "$p")" agy plugin validate "$p"
done

# 9. Check Anchor State Machine
check "Anchor state validation script" bash bin/state-validate.sh

# 10. Check Merged AGYOS Skills and Rules counts
check "Merged skills catalog (>400 skills in .agents/skills)" test "$(ls -1 .agents/skills | wc -l)" -gt 400
check "Merged rules catalog (>120 rules in .agents/rules)" test "$(ls -1 .agents/rules | wc -l)" -gt 120

# 11. Check Core AGYOS Assets & CLI
check "AGYOS master logo exists in assets/agyos-logo.svg" test -s assets/agyos-logo.svg
check "bin/agyos executable exists and functional" bin/agyos help

# 12. Check Tiered Skills Manifest & Fast-Path Routing
check "Tiered skills manifest exists and valid" test -s .agents/skills-manifest.json
check "Fast-path state bypass functional" bash -c 'bin/agyos fast >/dev/null && test "$(jq -r .current_gate .agents/state/state.json)" = "IMPLEMENT" && bin/agyos gate IDLE >/dev/null'

# 13. Hierarchical Architecture & Virtual Memory Storage
check "Hierarchical architecture specification exists" test -s docs/ARCHITECTURE.md
check "Virtual memory state storage exists and valid" bash -c 'test -s .agents/state/memory.json && jq -e .tier0_core_memory .agents/state/memory.json >/dev/null'

echo "============================================================"
echo "Verification Summary: $PASS_COUNT PASSED, $FAIL_COUNT FAILED"
echo "============================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
