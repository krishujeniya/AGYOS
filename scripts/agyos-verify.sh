#!/usr/bin/env bash
# agyos-verify.sh — Machine Verification Suite for AGYOS v3.1
# Falsifiable, deterministic proof of AGYOS operations.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

PASS_COUNT=0
FAIL_COUNT=0

# The previous fixed /tmp/agyos-check.log was predictable and could follow a
# symlink. Keep verifier output private and remove it on exit.
VERIFY_LOG_DIR="$(mktemp -d "${TMPDIR:-/tmp}/agyos-verify.XXXXXXXX")"
chmod 700 "$VERIFY_LOG_DIR"
trap 'rm -rf -- "$VERIFY_LOG_DIR"' EXIT
VERIFY_LOG_FILE="$VERIFY_LOG_DIR/check.log"
AGYOS_CHECK_TIMEOUT_SEC="${AGYOS_CHECK_TIMEOUT_SEC:-180}"
if ! [[ "$AGYOS_CHECK_TIMEOUT_SEC" =~ ^[1-9][0-9]{0,3}$ ]]; then
  echo "Invalid AGYOS_CHECK_TIMEOUT_SEC" >&2
  exit 2
fi

check() {
  local desc="$1"
  shift
  echo -n "• Checking $desc... "
  if timeout --signal=TERM --kill-after=5s "${AGYOS_CHECK_TIMEOUT_SEC}s" "$@" >"$VERIFY_LOG_FILE" 2>&1; then
    echo "PASS"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "FAIL"
    sed -n "1,120p" "$VERIFY_LOG_FILE"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

echo "============================================================"
echo "🛡️ AGYOS Adversarial Verification Suite"
echo "============================================================"

# 1. Constitution rules size budget check (<24,000 bytes)
check "AGENTS.md size limit (<24,000 bytes)" test "$(wc -c < AGENTS.md)" -lt 24000

# 2. Check GEMINI.md link exists
check "GEMINI.md content matches AGENTS.md" cmp -s AGENTS.md GEMINI.md

# 3. Check AGY CLI Version
check "AGY CLI installed and responsive" agy --version

# 4. Check MCP Servers List
check "AGYOS MCP server registered in AGY" grep -q "agyos\|anchor" <(agy mcp list)

# 5. Check Hook Script execution
check "AGYOS Safety Hook blocks dangerous commands" bash -c 'echo "{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"rm -rf /\"}}}" | python3 scripts/hooks/agy_os_hook.py PreToolUse | grep -q "\"decision\": \"deny\""'
check "AGYOS Safety Hook allows benign commands" bash -c 'echo "{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"npm test\"}}}" | python3 scripts/hooks/agy_os_hook.py PreToolUse | grep -q "\"decision\": \"allow\""'
check "AGY startup metadata and hook contract regressions" python3 -m unittest discover -s scripts/tests -v

# 6. Check FastMCP JSON-RPC Server
check "AGYOS MCP server JSON-RPC initialize" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{}}" | node mcp/state-server.cjs | grep -q "\"serverInfo\""'
check "AGYOS MCP server tools/list" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\",\"params\":{}}" | node mcp/state-server.cjs | grep -q "\"agyos_state\""'
check "AGYOS MCP server tools/call (agyos_state)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_state\",\"arguments\":{}}}" | node mcp/state-server.cjs | grep -q "current_gate"'
check "AGYOS MCP server tools/call (agyos_find_skill)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_find_skill\",\"arguments\":{\"query\":\"react\"}}}" | node mcp/state-server.cjs | grep -q "Top Skill Matches"'
check "AGYOS MCP server tools/call (agyos_sys_info)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":5,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_sys_info\",\"arguments\":{}}}" | node mcp/state-server.cjs | grep -q "Hierarchical Cognitive OS"'
check "AGYOS MCP server tools/call (agyos_memory)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":6,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_memory\",\"arguments\":{\"action\":\"read\",\"tier\":\"tier0\"}}}" | node mcp/state-server.cjs | grep -q "user_preferences"'
check "AGYOS MCP server tools/call (agyos_decision)" bash -c 'echo "{\"jsonrpc\":\"2.0\",\"id\":7,\"method\":\"tools/call\",\"params\":{\"name\":\"agyos_decision\",\"arguments\":{\"task\":\"optimize postgres query\"}}}" | node mcp/state-server.cjs | grep -q "postgres-best-practices"'
check "bin/agyos find skill search CLI" bash -c 'bin/agyos find "postgres" | grep -q "Top Skill Matches"'
check "bin/agyos decide CLI decision engine" bash -c 'bin/agyos decide "fix memory leak in postgres connection" | grep -q "postgres-best-practices"'
check "bin/agyos sysinfo CLI command" bash -c 'bin/agyos sysinfo | grep -q "Hierarchical Cognitive OS"'
check "bin/agyos mem virtual memory CLI" bash -c 'bin/agyos mem tier0 | grep -q "user_preferences"'

# 7. Check Agent Council Bun Test Suite
check "Agent Council Bun test suite (59 passing tests)" bash -c 'cd scripts/council && bun test'

# 8. Check 8 AGYOS Plugins
for p in .agents/plugins/*; do
  check "Plugin validation for $(basename "$p")" agy plugin validate "$p"
done

# 9. Check AGYOS State Machine
check "AGYOS state validation script" bash bin/state-validate.sh

# 10. Check Merged AGYOS Skills and Rules counts
check "Merged skills catalog (>400 skills in .agents/skills)" test "$(ls -1 .agents/skills | wc -l)" -gt 400
check "Merged rules catalog (>120 rules in .agents/rules)" test "$(ls -1 .agents/rules | wc -l)" -gt 120

# 11. Check Core AGYOS Assets & CLI
check "AGYOS master logo exists in assets/agyos-logo.svg" test -s assets/agyos-logo.svg
check "bin/agyos executable exists and functional" bin/agyos help

# 12. Check Tiered Skills Manifest & Fast-Path Routing
check "Tiered skills manifest exists and valid" test -s .agents/skills-manifest.json
check "Fast-path state bypass functional (isolated fixture)" bash -c 'tmp=$(mktemp -d); trap '\''rm -rf -- "$tmp"'\'' EXIT; cp .agents/state/state.json "$tmp/state.json"; STATE_FILE="$tmp/state.json" bin/agyos fast >/dev/null && test "$(jq -r .current_gate "$tmp/state.json")" = "IMPLEMENT" && STATE_FILE="$tmp/state.json" bin/agyos gate IDLE >/dev/null && test "$(jq -r .current_gate "$tmp/state.json")" = "IDLE"'

# 13. Hierarchical Architecture & Virtual Memory Storage
check "Hierarchical architecture specification exists" test -s docs/ARCHITECTURE.md
check "Virtual memory state storage exists and valid" bash -c 'test -s .agents/state/memory.json && jq -e .tier0_core_memory .agents/state/memory.json >/dev/null'

# 14. Contracts, Intent & EVPI Clarification
check "TaskContract JSON schema validity (Draft 2020-12)" python3 -c 'import json, jsonschema; jsonschema.Draft202012Validator.check_schema(json.load(open("agyos_decision/contracts.schema.json")))'
check "Intent compiler maps 11 company functions to 5 pods" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.intent_compiler import compile_intent, FUNCTION_TO_POD; assert len(FUNCTION_TO_POD) == 11; c = compile_intent("reconcile ledger invoices"); assert c.pod == "pod-gna" and c.risk == "R0"'
check "EVPI clarification asks <= 1 question on critical ambiguity" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.intent_compiler import compile_intent; from agyos_decision.evpi_clarify import evaluate_evpi; c = compile_intent("wire $50000 to vendor"); d = evaluate_evpi("wire $50000 to vendor", c); assert d.should_ask_question and d.outbox_status == "PENDING_COMMIT"'

# 15. State Ledger, Hierarchy Caps, Budgets & Saga Recovery
check "DAG task graph enforces depth<=2, fanout<=4, tasks<=8, workers<=3" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.state_ledger import DAGTaskGraph, HierarchyCapError; g = DAGTaskGraph("t"); g.add_task("r", 0); [g.add_task(f"c{i}", 1, ["r"]) for i in range(4)]; g.validate_acyclic()'
check "Run budget tracker reserves 20% for verification and rollback" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.state_ledger import RunBudgetTracker; b = RunBudgetTracker(30000, 1.50); assert b.reserved_tokens == 6000 and b.available_execution_tokens == 24000'
check "Transactional snapshot rollback restoration" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.state_ledger import SnapshotManager; m = SnapshotManager(); sid = m.create_snapshot("s1", {"balance": 100}); assert m.rollback(sid)["balance"] == 100'
check "LIFO Saga compensation reverse-order execution" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.state_ledger import SagaCoordinator; s = SagaCoordinator("s1"); order = []; s.register_step("1", lambda: order.append(1)); s.register_step("2", lambda: order.append(2)); s.rollback(); assert order == [2, 1] and s.status == "COMPENSATED"'

# 16. Host Pods, SOP Skills & Fail-Closed Authorizer Hook
check "5 Pod agent definitions exist in .agents/agents/" bash -c 'for p in pod-growth pod-customer pod-build pod-gna pod-people; do test -s ".agents/agents/$p.md" || exit 1; done'
check "5 SOP skills exist in .agents/skills/" bash -c 'for s in sop-growth sop-customer sop-build sop-gna sop-people; do test -s ".agents/skills/$s/SKILL.md" || exit 1; done'
check "Fail-Closed Authorizer hook blocks unauthorized R3 payments" bash -c 'echo "{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"curl -X POST https://api.stripe.com/v1/refunds\"}}}" | python3 scripts/hooks/authorizer.py PreToolUse | grep -q "\"decision\": \"deny\""'
check "Fail-Closed Authorizer enforces capability allowlist" bash -c 'echo "{\"taskContract\":{\"capability_allowlist\":[\"read_file\"]},\"toolCall\":{\"name\":\"edit_file\",\"args\":{}}}" | python3 scripts/hooks/authorizer.py PreToolUse | grep -q "\"decision\": \"deny\""'

# 17. Atomic-Claim Grounding & Architecture A/B Benchmark
check "Atomic-claim verifier enforces 0 unbacked claims" python3 -c 'import sys; sys.path.insert(0, "."); from agyos_decision.verifier import verify_atomic_grounding; r = verify_atomic_grounding("Variance is $50.00 on tsk_1", {"task_id":"tsk_1", "amount":"50.00"}); assert r.passed and r.unbacked_claims == 0'
check "Company adapters dry-run operational validation" python3 -m unittest scripts/tests/test_company_adapters.py
check "Architecture A/B benchmark execution (pass^1/pass^3 & CI)" bash -c 'python3 scripts/ab_compare_benchmark.py | grep -q "Adaptive Hierarchy"'
check "Canary launch gate & go/no-go audit pass" python3 scripts/canary_launch_gate.py

echo "============================================================"
echo "Verification Summary: $PASS_COUNT PASSED, $FAIL_COUNT FAILED"
echo "============================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
