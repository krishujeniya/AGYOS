#!/usr/bin/env bats
# tests/eval.bats
# Meta-verification: verifies that eval.sh works correctly.

setup() {
  export TEMP_PROJECT_ROOT="${BATS_TEST_TMPDIR}/anchor-eval-test"
  mkdir -p "$TEMP_PROJECT_ROOT"
  
  # Copy necessary scripts
  cp -r "${BATS_TEST_DIRNAME}/../bin" "$TEMP_PROJECT_ROOT/"
  cp -r "${BATS_TEST_DIRNAME}/../.agents" "$TEMP_PROJECT_ROOT/" || true
  cp "${BATS_TEST_DIRNAME}/../AGENTS.md" "$TEMP_PROJECT_ROOT/" || true
  
  cd "$TEMP_PROJECT_ROOT"
  # Initialize a fresh slate
  bash bin/init.sh
}

teardown() {
  rm -rf "$TEMP_PROJECT_ROOT"
}

@test "eval.sh passes on a clean initialization" {
  run bash bin/eval.sh
  [ "$status" -eq 0 ]
  [[ "$output" == *"RESULT: PASS"* ]]
}

@test "eval.sh fails if verify.sh fails (sabotage state)" {
  # Corrupt a skill to force verify.sh to fail in Phase 1
  echo "garbage" > .agents/skills/anchor-orchestrator/SKILL.md
  
  run bash bin/eval.sh
  [ "$status" -eq 1 ]
  [[ "$output" == *"RESULT: FAIL"* || "$output" == *"Current state failed verify.sh"* ]]
}

@test "eval.sh catches corrupted eval_fixtures" {
  # Modify eval_fixtures so one behavioral check fails
  echo "echo 'not caught'" > .agents/skills/anchor-scout/scripts/scan-security.sh
  
  run bash bin/eval.sh
  [ "$status" -eq 1 ]
  [[ "$output" == *"RESULT: FAIL"* ]]
}

@test "rollback.sh aborts on missing git repository" {
  rm -rf .git
  run bash bin/rollback.sh
  [ "$status" -eq 1 ]
}

@test "sandbox-run.sh blocks unauthorized access" {
  run bash bin/sandbox-run.sh "cat /etc/shadow"
  [ "$status" -ne 0 ]
}
