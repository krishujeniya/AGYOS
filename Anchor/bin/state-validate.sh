#!/usr/bin/env bash
# state-validate.sh — Schema validation and self-repair for state.json

set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
STATE_FILE="${STATE_FILE:-${PROJECT_ROOT}/.agents/state/state.json}"

if [ ! -f "$STATE_FILE" ]; then
  echo "State file missing, initializing defaults..."
  bash "${PROJECT_ROOT}/bin/init.sh"
  exit 0
fi

(
  flock -x 200
  
  if ! jq . "$STATE_FILE" >/dev/null 2>&1; then
    echo "1" > "${STATE_FILE}.repair_flag"
    exit 0
  fi

  for field in project current_gate current_milestone iteration iteration_cap token_budget max_cost_usd max_wall_clock_minutes tokens_used no_progress_strikes hitl_approvals last_updated last_known_commit last_known_commit_COMPACT skill_versions; do
    if ! jq -e "has(\"$field\")" "$STATE_FILE" > /dev/null 2>&1; then
      echo "⚠️ State file missing field: $field. Repairing..."
      case "$field" in
        iteration|tokens_used|no_progress_strikes) jq --arg k "$field" '.[$k] = 0' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        iteration_cap) jq --arg k "$field" '.[$k] = 10' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        token_budget) jq --arg k "$field" '.[$k] = 50000' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        max_cost_usd) jq --arg k "$field" '.[$k] = 10.0' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        max_wall_clock_minutes) jq --arg k "$field" '.[$k] = 60' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        hitl_approvals|skill_versions) jq --arg k "$field" '.[$k] = {}' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
        *) jq --arg k "$field" '.[$k] = null' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE" ;;
      esac
    fi
  done
) 200>"${STATE_FILE}.lock"

if [ -f "${STATE_FILE}.repair_flag" ]; then
  rm -f "${STATE_FILE}.repair_flag"
  echo "⚠️ State file corrupted (invalid JSON). Repairing..."
  cp "$STATE_FILE" "${STATE_FILE}.corrupt.$(date +%s)"
  rm -f "$STATE_FILE"
  bash "${PROJECT_ROOT}/bin/init.sh"
  exit 0
fi

exit 0
