#!/usr/bin/env bash
# state-validate.sh — validate and recover only the AGYOS state.json file.

set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
STATE_FILE="${STATE_FILE:-${PROJECT_ROOT}/.agents/state/state.json}"
STATE_DIR=$(dirname "$STATE_FILE")

write_defaults() {
  TEMP_FILE="${STATE_FILE}.tmp.$$"
  cat > "$TEMP_FILE" <<EOF
{
  "project": "AGYOS",
  "current_gate": null,
  "current_milestone": null,
  "iteration": 0,
  "iteration_cap": 10,
  "token_budget": 50000,
  "max_cost_usd": 10.0,
  "max_wall_clock_minutes": 60,
  "tokens_used": 0,
  "no_progress_strikes": 0,
  "hitl_approvals": {},
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "last_known_commit": "",
  "last_known_commit_COMPACT": null,
  "skill_versions": {}
}
EOF
  mv "$TEMP_FILE" "$STATE_FILE"
  TEMP_FILE=''
}

backup_corrupt_state() {
  local backup="${STATE_FILE}.corrupt.$(date +%s)"
  local suffix=0
  while [ -e "$backup" ]; do
    suffix=$((suffix + 1))
    backup="${STATE_FILE}.corrupt.$(date +%s).${suffix}"
  done
  cp -- "$STATE_FILE" "$backup"
  printf '%s\n' "$backup"
}

TEMP_FILE=''
cleanup_temp_file() {
  if [ -n "$TEMP_FILE" ]; then
    rm -f -- "$TEMP_FILE"
  fi
}

mkdir -p "$STATE_DIR"
(
  flock -x 200
  trap cleanup_temp_file EXIT

  if [ ! -e "$STATE_FILE" ] && [ ! -L "$STATE_FILE" ]; then
    echo "State file missing; initializing state.json defaults."
    write_defaults
  elif [ -L "$STATE_FILE" ] || [ ! -f "$STATE_FILE" ] || [ ! -r "$STATE_FILE" ]; then
    echo "Error: state.json is not a readable regular file; original path was preserved." >&2
    exit 1
  else
    if jq -e 'type == "object"' "$STATE_FILE" >/dev/null 2>&1; then
      :
    else
      jq_status=$?
      case "$jq_status" in
        1|4)
          backup=$(backup_corrupt_state)
          echo "State JSON is corrupt or is not an object; preserved original at $backup and initialized state.json defaults."
          write_defaults
          exit 0
          ;;
        *)
          echo "Error: jq could not inspect state.json (exit $jq_status); original was preserved." >&2
          exit "$jq_status"
          ;;
      esac
    fi

    defaults='{"project":"AGYOS","current_gate":null,"current_milestone":null,"iteration":0,"iteration_cap":10,"token_budget":50000,"max_cost_usd":10.0,"max_wall_clock_minutes":60,"tokens_used":0,"no_progress_strikes":0,"hitl_approvals":{},"last_updated":"","last_known_commit":"","last_known_commit_COMPACT":null,"skill_versions":{}}'
    TEMP_FILE="${STATE_FILE}.tmp.$$"
    if jq --argjson defaults "$defaults" '$defaults + .' "$STATE_FILE" > "$TEMP_FILE"; then
      :
    else
      jq_status=$?
      echo "Error: jq could not merge state defaults (exit $jq_status); original was preserved." >&2
      exit "$jq_status"
    fi

    if jq -e '
      (.project | type == "string") and
      (.current_gate == null or .current_gate == "IDLE" or .current_gate == "UNDERSTAND" or .current_gate == "ANALYZE" or .current_gate == "PLAN" or .current_gate == "IMPLEMENT" or .current_gate == "VERIFY") and
      (.current_milestone == null or (.current_milestone | type == "string")) and
      (.iteration | type == "number" and floor == . and . >= 0) and
      (.iteration_cap | type == "number" and floor == . and . >= 1) and
      (.token_budget | type == "number" and . >= 0) and
      (.max_cost_usd | type == "number" and . >= 0) and
      (.max_wall_clock_minutes | type == "number" and . >= 0) and
      (.tokens_used | type == "number" and . >= 0) and
      (.no_progress_strikes | type == "number" and . >= 0) and
      (.hitl_approvals | type == "object") and
      (.last_updated | type == "string") and
      (.last_known_commit == null or (.last_known_commit | type == "string")) and
      (.last_known_commit_COMPACT == null or (.last_known_commit_COMPACT | type == "string")) and
      (.skill_versions | type == "object") and
      ((has("complexity_score") | not) or (.complexity_score | type == "number" and floor == . and . >= 1 and . <= 5))
    ' "$TEMP_FILE" >/dev/null; then
      mv "$TEMP_FILE" "$STATE_FILE"
      TEMP_FILE=''
    else
      jq_status=$?
      case "$jq_status" in
        1|4)
          echo "Error: state.json has invalid field types or values; original content was preserved." >&2
          exit 1
          ;;
        *)
          echo "Error: jq could not validate state.json (exit $jq_status); original was preserved." >&2
          exit "$jq_status"
          ;;
      esac
    fi
  fi
) 200>"${STATE_FILE}.lock"

exit 0
