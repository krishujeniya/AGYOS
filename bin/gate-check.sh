#!/usr/bin/env bash
# gate-check.sh — Git pre-commit hook for ANCHOR
set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
STATE_FILE="${STATE_FILE:-${PROJECT_ROOT}/.agents/state/state.json}"

if [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

source "${PROJECT_ROOT}/bin/state.sh"
CURRENT_GATE=$(anchor_state_get "current_gate" "null")
MILESTONE=$(anchor_state_get "current_milestone" "null")
ITERATION=$(anchor_state_get "iteration" "0")

if [ "${ANCHOR_HUMAN:-0}" -eq 1 ]; then
  echo "⚠️ ANCHOR: Human bypass active. Allowing commit."
  exit 0
fi

# 1. Reject commits if current_gate is a HITL gate
if [[ "$CURRENT_GATE" == "UNDERSTAND" || "$CURRENT_GATE" == "ANALYZE" || "$CURRENT_GATE" == "PLAN" || "$CURRENT_GATE" == "VERIFY" ]]; then
  echo "❌ ANCHOR: Cannot commit manually or autonomously during HITL gate ($CURRENT_GATE)."
  echo "Please complete the gate or run rollback."
  exit 1
fi

# 2. During IMPLEMENT, reject if no checkpoint block exists for current iteration
if [[ "$CURRENT_GATE" == "IMPLEMENT" && "$MILESTONE" != "null" ]]; then
  CHECKPOINT_FILE="${PROJECT_ROOT}/.agents/state/checkpoints/${MILESTONE}.md"
  if [ -f "$CHECKPOINT_FILE" ]; then
    json_blocks=$(awk '/^```json/{flag=1; next} /^```/{flag=0; next} flag' "$CHECKPOINT_FILE" 2>/dev/null || echo "")
    if ! echo "$json_blocks" | jq -e "select(.iteration == ${ITERATION})" >/dev/null 2>&1; then
      echo "❌ ANCHOR: Cannot commit during IMPLEMENT without a structured JSON checkpoint block for Iteration ${ITERATION}."
      exit 1
    fi
  fi
fi

# 3. Test Ratchet Rule: Check for removed assertions in modified test files
STAGED_TEST_FILES=$(git diff --cached --name-only --diff-filter=M | grep -iE '(^|/)(tests?|__tests__|specs?)(/|$)|(^|/)(test_[^/]*|[^/]*_test|[^/]*\.test|[^/]*\.spec|spec_[^/]*)\.(py|pyi|[cm]?[jt]sx?)$' || true)
if [ -n "$STAGED_TEST_FILES" ]; then
  # Check if an override is documented in the checkpoint
  OVERRIDE_RATCHET=0
  if [[ "$CURRENT_GATE" == "IMPLEMENT" && "$MILESTONE" != "null" ]]; then
    CHECKPOINT_FILE="${PROJECT_ROOT}/.agents/state/checkpoints/${MILESTONE}.md"
    if [ -f "$CHECKPOINT_FILE" ]; then
      json_blocks=$(awk '/^```json/{flag=1; next} /^```/{flag=0; next} flag' "$CHECKPOINT_FILE" 2>/dev/null || echo "")
      if echo "$json_blocks" | jq -e 'select(.override_test_ratchet == true)' >/dev/null 2>&1; then
        OVERRIDE_RATCHET=1
        echo "⚠️ ANCHOR TEST RATCHET: Structured override note found in checkpoint. Allowing assertion removal."
      fi
    fi
  fi

  if [ "$OVERRIDE_RATCHET" -eq 0 ]; then
    while IFS= read -r file; do
      [ -z "$file" ] && continue
      # awk returns a successful numeric zero when no assertion patterns match.
      OLD_ASSERTS=$( (git show HEAD:"$file" 2>/dev/null || echo "") | awk 'tolower($0) ~ /assert|expect|t\.|test\(|it\(/ {n++} END {print n+0}' )
      NEW_ASSERTS=$( (git show :0:"$file" 2>/dev/null || echo "") | awk 'tolower($0) ~ /assert|expect|t\.|test\(|it\(/ {n++} END {print n+0}' )
      if [ "$NEW_ASSERTS" -lt "$OLD_ASSERTS" ]; then
        echo "❌ ANCHOR TEST RATCHET: You deleted or weakened a test assertion in $file"
        echo "   Previous assertion count: $OLD_ASSERTS"
        echo "   New assertion count: $NEW_ASSERTS"
        echo "Failing tests may never be deleted, skipped, or weakened to make VERIFY pass."
        echo "To override, document 'Override-Test-Ratchet' in the current milestone checkpoint."
        exit 1
      fi
    done <<< "$STAGED_TEST_FILES"
  fi
fi

exit 0
