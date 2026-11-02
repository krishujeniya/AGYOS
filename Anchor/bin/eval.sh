#!/usr/bin/env bash
# eval.sh — ANCHOR Evaluation Harness
# Evaluates skills integrity and backwards-compatibility against archived milestones.

set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
AGENTS_DIR="${PROJECT_ROOT}/.agents"

echo "🧪 Starting ANCHOR Eval Harness..."

source "${PROJECT_ROOT}/bin/state.sh"

# Phase 1: Current State
echo ""
echo "▶️ Phase 1: Current State Verification"
if bash "${AGENTS_DIR}/skills/anchor-verify/scripts/verify.sh" "$PROJECT_ROOT" > /dev/null; then
  echo "  ✅ Current state and skills pass verify.sh"
else
  echo "  ❌ Current state failed verify.sh checks."
  # Run again without swallowing output so the user sees the error
  bash "${AGENTS_DIR}/skills/anchor-verify/scripts/verify.sh" "$PROJECT_ROOT"
  exit 1
fi

# Phase 2: Historical Archive Regression (Checkpoints)
# Phase 2: Historical Checkpoint Regression
echo ""
echo "▶️ Phase 2: Historical Checkpoint Regression"
ARCHIVE_DIR="${AGENTS_DIR}/state/checkpoints/archive"
FAIL=0
TOTAL=0

# Gather checkpoints to test (fixtures + archives)
CHECKPOINTS=()
if [ -f "${AGENTS_DIR}/eval_fixtures/golden_checkpoint.md" ]; then
  CHECKPOINTS+=("${AGENTS_DIR}/eval_fixtures/golden_checkpoint.md")
fi
if [ -d "$ARCHIVE_DIR" ]; then
  while IFS= read -r cpfile; do
    [ -n "$cpfile" ] && CHECKPOINTS+=("$cpfile")
  done <<< "$(find "$ARCHIVE_DIR" -name "*.md" -type f 2>/dev/null)"
fi

if [ ${#CHECKPOINTS[@]} -gt 0 ]; then
  for cp in "${CHECKPOINTS[@]}"; do
    relpath="${cp#"$PROJECT_ROOT"/}"
    TOTAL=$((TOTAL + 1))
    # Must have Goal:, ## Gate:, and either HALT or COMPLETE
    has_goal=$(grep -c "^Goal:" "$cp" || true)
    has_gate=$(grep -c "^## Gate:" "$cp" || true)
    has_result=$(grep -ci "halt\|complete" "$cp" || true)

    if [ "$has_goal" -eq 0 ] || [ "$has_gate" -eq 0 ] || [ "$has_result" -eq 0 ]; then
      echo "  ❌ FAIL: $relpath (schema mismatch)"
      FAIL=$((FAIL + 1))
    else
      echo "  ✅ PASS: $relpath (schema valid)"
    fi
  done
fi

if [ "$TOTAL" -eq 0 ]; then
  echo "  (No archived checkpoints found to test)"
fi

# Phase 3: Behavioral Script Testing
echo ""
echo "▶️ Phase 3: Behavioral Script Testing"

# 1. verify.sh on corrupt state MUST FAIL
echo -n "  - verify.sh catches corrupt state... "
if bash "${AGENTS_DIR}/skills/anchor-verify/scripts/verify.sh" "${PROJECT_ROOT}/.agents/eval_fixtures/corrupt_state" > /dev/null 2>&1; then
  echo "❌ FAIL (Did not catch corruption)"
  FAIL=$((FAIL + 1))
else
  echo "✅ PASS"
fi

# 2. scan-security.sh on leaked secret MUST FAIL
echo -n "  - scan-security.sh catches leaked secret... "
if bash "${AGENTS_DIR}/skills/anchor-scout/scripts/scan-security.sh" "${PROJECT_ROOT}/.agents/eval_fixtures/leaked_secret" > /dev/null 2>&1; then
  echo "❌ FAIL (Did not catch secret)"
  FAIL=$((FAIL + 1))
else
  echo "✅ PASS"
fi

# 3. scan-security.sh on clean project MUST PASS
echo -n "  - scan-security.sh passes clean project... "
if bash "${AGENTS_DIR}/skills/anchor-scout/scripts/scan-security.sh" "${PROJECT_ROOT}/.agents/eval_fixtures/clean_secret" > /dev/null 2>&1; then
  echo "✅ PASS"
else
  echo "❌ FAIL (False positive)"
  FAIL=$((FAIL + 1))
fi

# 4. scan.sh parses quote_in_filename cleanly
echo -n "  - scan.sh handles escaped quotes... "
if bash "${AGENTS_DIR}/skills/anchor-graph/scripts/scan.sh" "${PROJECT_ROOT}/.agents/eval_fixtures/adversarial/quote_in_filename" | jq . > /dev/null 2>&1; then
  echo "✅ PASS"
else
  echo "❌ FAIL (JSON parsing broke)"
  FAIL=$((FAIL + 1))
fi

# 5. verify.sh on malformed_skill MUST FAIL
echo -n "  - verify.sh catches malformed skills... "
if bash "${AGENTS_DIR}/skills/anchor-verify/scripts/verify.sh" "${PROJECT_ROOT}/.agents/eval_fixtures/adversarial/malformed_skill" > /dev/null 2>&1; then
  echo "❌ FAIL (Did not catch malformed skill)"
  FAIL=$((FAIL + 1))
else
  echo "✅ PASS"
fi

# 6. drift-check.sh on untracked file MUST FAIL
echo -n "  - drift-check.sh catches untracked files... "
TEST_DIR=$(mktemp -d)
cp -r "${PROJECT_ROOT}/.agents" "$TEST_DIR/"
cp -r "${PROJECT_ROOT}/bin" "$TEST_DIR/"
git init "$TEST_DIR" > /dev/null 2>&1
git -C "$TEST_DIR" config user.email "test@example.com"
git -C "$TEST_DIR" config user.name "Test User"
git -C "$TEST_DIR" commit --allow-empty -m "init" > /dev/null 2>&1 || true
LAST_HASH=$(git -C "$TEST_DIR" rev-parse HEAD 2>/dev/null || echo "fake")
jq --arg hash "$LAST_HASH" '.last_known_commit = $hash' "${TEST_DIR}/.agents/state/state.json" > "${TEST_DIR}/.agents/state/state.json.tmp" && mv "${TEST_DIR}/.agents/state/state.json.tmp" "${TEST_DIR}/.agents/state/state.json"
touch "${TEST_DIR}/drift_mock.test"
if bash "${TEST_DIR}/bin/drift-check.sh" > /dev/null 2>&1; then
  echo "❌ FAIL (Did not catch untracked file)"
  FAIL=$((FAIL + 1))
else
  echo "✅ PASS"
fi
rm -rf "$TEST_DIR"

# 7. drift-check.sh on stale commit MUST FAIL
echo -n "  - drift-check.sh blocks stale/detached state... "
TEST_DIR=$(mktemp -d)
cp -r "${PROJECT_ROOT}/.agents" "$TEST_DIR/"
cp -r "${PROJECT_ROOT}/bin" "$TEST_DIR/"
git init "$TEST_DIR" > /dev/null 2>&1
git -C "$TEST_DIR" config user.email "test@example.com"
git -C "$TEST_DIR" config user.name "Test User"
git -C "$TEST_DIR" commit --allow-empty -m "init" > /dev/null 2>&1 || true
jq '.last_known_commit = "fakehash123"' "${TEST_DIR}/.agents/state/state.json" > "${TEST_DIR}/.agents/state/state.json.tmp" && mv "${TEST_DIR}/.agents/state/state.json.tmp" "${TEST_DIR}/.agents/state/state.json"
if bash "${TEST_DIR}/bin/drift-check.sh" > /dev/null 2>&1; then
  echo "❌ FAIL (Did not block detached state)"
  FAIL=$((FAIL + 1))
else
  echo "✅ PASS"
fi
rm -rf "$TEST_DIR"

# 8. state-validate.sh repairs state.json corruption (CT-004)
echo -n "  - state-validate.sh repairs state.json (CT-004)... "
TEST_DIR=$(mktemp -d)
cp -r "${PROJECT_ROOT}/.agents" "$TEST_DIR/"
cp -r "${PROJECT_ROOT}/bin" "$TEST_DIR/"
echo '{ "corrupted": true }' > "${TEST_DIR}/.agents/state/state.json"
bash "${TEST_DIR}/bin/state-validate.sh" > /dev/null 2>&1
if jq -e 'has("project")' "${TEST_DIR}/.agents/state/state.json" > /dev/null 2>&1; then
  echo "✅ PASS"
else
  echo "❌ FAIL (Did not repair state)"
  FAIL=$((FAIL + 1))
fi
rm -rf "$TEST_DIR"

echo ""
echo "=== Eval Summary ==="
if [ "$FAIL" -gt 0 ]; then
  echo "RESULT: FAIL ($FAIL historical regressions)"
  exit 1
else
  echo "RESULT: PASS (0 regressions)"
  exit 0
fi
