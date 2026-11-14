#!/usr/bin/env bash
# state.sh — ANCHOR State Access Abstraction Layer
# Exposes helper functions to read and write state.json.

STATE_FILE="${STATE_FILE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.agents/state/state.json}"

# anchor_state_get <key> [default_value]
# Returns the value of the key from state.json, or default_value if missing/null.
anchor_state_get() {
  local key="$1"
  local default_val="${2:-}"
  
  if [ ! -f "$STATE_FILE" ]; then
    echo "$default_val"
    return 0
  fi
  
  local val
  val=$(jq -r --arg k "$key" '.[$k] // empty' "$STATE_FILE" 2>/dev/null || echo "")
  
  if [ -z "$val" ]; then
    echo "$default_val"
  else
    echo "$val"
  fi
}

# anchor_state_set <key> <value> [<type>]
# Updates a key in state.json. Use type="number" for integers.
anchor_state_set() {
  local key="$1"
  local val="$2"
  local type="${3:-string}"

  if [ "$key" = "current_gate" ]; then
    echo "Error: current_gate must be changed through anchor_gate_transition." >&2
    return 2
  fi
  
  if [ ! -f "$STATE_FILE" ]; then
    echo "Error: state.json not found." >&2
    return 1
  fi
  
  (
    flock -x 200
    if [ "$type" = "number" ]; then
      jq --arg k "$key" --argjson v "$val" '.[$k] = $v' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    else
      jq --arg k "$key" --arg v "$val" '.[$k] = $v' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    fi
  ) 200>"${STATE_FILE}.lock"
}

# anchor_gate_transition <target> [fast]
# Enforce the AGYOS gate graph while holding the state lock.
anchor_gate_transition() {
  local target="$1"
  local mode="${2:-normal}"
  local current complexity allowed
  case "$target" in
    IDLE|UNDERSTAND|ANALYZE|PLAN|IMPLEMENT|VERIFY) ;;
    *) echo "Error: invalid gate '$target'." >&2; return 2 ;;
  esac

  if [ ! -f "$STATE_FILE" ]; then
    echo "Error: state.json not found." >&2
    return 1
  fi

  (
    flock -x 200
    current=$(jq -r '.current_gate // "IDLE"' "$STATE_FILE")
    complexity=$(jq -r '.complexity_score // empty' "$STATE_FILE")
    allowed=0
    case "$current:$target:$mode" in
      IDLE:UNDERSTAND:normal|UNDERSTAND:ANALYZE:normal|ANALYZE:PLAN:normal|PLAN:IMPLEMENT:normal|IMPLEMENT:VERIFY:normal|VERIFY:IDLE:normal)
        allowed=1 ;;
      ANALYZE:IMPLEMENT:fast)
        if [[ "$complexity" =~ ^[0-9]+$ ]] && [ "$complexity" -ge 1 ] && [ "$complexity" -le 2 ]; then
          allowed=1
        else
          echo "Error: fast path requires complexity_score 1 or 2 after ANALYZE (found '${complexity:-missing}')." >&2
        fi ;;
    esac
    if [ "$allowed" -ne 1 ]; then
      echo "Error: invalid gate transition $current -> $target${mode:+ ($mode)}." >&2
      exit 1
    fi
    jq --arg gate "$target" '.current_gate = $gate' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
  ) 200>"${STATE_FILE}.lock"
}

# anchor_state_lock_run <command> [args...]
# Executes a command safely holding the state.json lock
anchor_state_lock_run() {
  if [ ! -f "$STATE_FILE" ]; then
    echo "Error: state.json not found." >&2
    return 1
  fi
  (
    flock -x 200
    "$@"
  ) 200>"${STATE_FILE}.lock"
}
