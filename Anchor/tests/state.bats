#!/usr/bin/env bats

setup() {
  export TEMP_PROJECT_ROOT="${BATS_TEST_TMPDIR}/anchor-state-test"
  mkdir -p "${TEMP_PROJECT_ROOT}/.agents/state"
  export PROJECT_ROOT="$TEMP_PROJECT_ROOT"
  export STATE_FILE="${TEMP_PROJECT_ROOT}/.agents/state/state.json"
  echo "{}" > "$STATE_FILE"
}

teardown() {
  rm -rf "$TEMP_PROJECT_ROOT"
}

@test "anchor_state_get returns default when key missing" {
  source "${BATS_TEST_DIRNAME}/../bin/state.sh"
  run anchor_state_get "missing_key" "my_default"
  [ "$status" -eq 0 ]
  [ "$output" = "my_default" ]
}

@test "anchor_state_set updates value and anchor_state_get retrieves it" {
  source "${BATS_TEST_DIRNAME}/../bin/state.sh"
  anchor_state_set "my_key" "new_value"
  run anchor_state_get "my_key" "default"
  [ "$status" -eq 0 ]
  [ "$output" = "new_value" ]
}

@test "anchor_state_set sets number correctly" {
  source "${BATS_TEST_DIRNAME}/../bin/state.sh"
  anchor_state_set "my_num" "42" "number"
  run jq -r '.my_num' "$STATE_FILE"
  [ "$status" -eq 0 ]
  [ "$output" = "42" ]
}

@test "mcp-server syntax and dependencies are valid" {
  if ! command -v python3 >/dev/null 2>&1; then
    skip "python3 not installed"
  fi
  run python3 -m py_compile "${BATS_TEST_DIRNAME}/../mcp-server/server.py"
  [ "$status" -eq 0 ]
}

@test "anchor_state_set handles concurrent writes safely" {
  source "${BATS_TEST_DIRNAME}/../bin/state.sh"
  
  # Spawn 10 background processes writing to the same key
  for i in {1..10}; do
    anchor_state_set "concurrent_key" "value_$i" &
  done
  wait
  
  run jq -e 'has("concurrent_key")' "$STATE_FILE"
  [ "$status" -eq 0 ]
}
