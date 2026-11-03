#!/usr/bin/env bash
# rollback.sh — ANCHOR Rollback Mechanism
# Reverts the repository to the last_known_commit, destroying any
# half-finished agent work. Refuses to run if human drift is detected.

set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "$0")/.." && pwd)
STATE_FILE="${STATE_FILE:-${PROJECT_ROOT}/.agents/state/state.json}"
CURRENT_FILE="${PROJECT_ROOT}/.agents/state/CURRENT.md"

echo "⏪ Starting ANCHOR Rollback..."

if [ ! -f "$STATE_FILE" ]; then
  echo "❌ No state.json found. Cannot rollback."
  exit 1
fi

source "${PROJECT_ROOT}/bin/state.sh"

LAST_COMMIT=$(anchor_state_get "last_known_commit_COMPACT" "")
if [ -z "$LAST_COMMIT" ] || [ "$LAST_COMMIT" = "null" ]; then
  LAST_COMMIT=$(anchor_state_get "last_known_commit" "")
fi

if [ -z "$LAST_COMMIT" ]; then
  echo "❌ No last_known_commit found in state.json. Cannot rollback safely."
  exit 1
fi

if ! git -C "$PROJECT_ROOT" cat-file -t "$LAST_COMMIT" >/dev/null 2>&1; then
  echo "❌ last_known_commit ($LAST_COMMIT) is not a valid git object."
  exit 1
fi

# Step 1: Safety Check via drift-check.sh
echo "  - Checking for out-of-band human drift..."
if ! bash "${PROJECT_ROOT}/bin/drift-check.sh" --commits-only > /dev/null 2>&1; then
  echo "❌ ROLLBACK ABORTED: Human drift detected."
  echo "   Modifications have been made since the last milestone completed."
  echo "   Rolling back would destroy that work. Please resolve manually."
  exit 1
fi

# Step 2: Safety Backup & Rollback
echo "  - Drift check passed. No human edits detected."

TIMESTAMP=$(date -u +%Y%m%d%H%M%S)
MILESTONE=$(anchor_state_get "current_milestone" "unknown")
RESCUE_BRANCH="anchor-rescue/${MILESTONE}-${TIMESTAMP}"
CURRENT_BRANCH=$(git -C "$PROJECT_ROOT" branch --show-current || echo "main")

echo "  - Creating rescue branch: $RESCUE_BRANCH"
if ! git -C "$PROJECT_ROOT" checkout -b "$RESCUE_BRANCH" > /dev/null 2>&1; then
  echo "❌ ROLLBACK ABORTED: Failed to create rescue branch."
  exit 1
fi

echo "  - Committing untracked/uncommitted files to rescue branch..."
git -C "$PROJECT_ROOT" add -A
if ! git -C "$PROJECT_ROOT" diff --cached --quiet; then
  # Preserve patch as a second safeguard
  mkdir -p "${PROJECT_ROOT}/.agents/state/checkpoints/archive"
  git -C "$PROJECT_ROOT" diff --cached > "${PROJECT_ROOT}/.agents/state/checkpoints/archive/rollback-rescue-${TIMESTAMP}.patch" || true
  if ! git -C "$PROJECT_ROOT" commit -m "Rescue commit: Auto-saved before rollback ${TIMESTAMP}" > /dev/null 2>&1; then
    echo "❌ ROLLBACK ABORTED: Failed to create rescue commit."
    exit 1
  fi
fi

echo "  - Reverting repository to $LAST_COMMIT on original branch..."
git -C "$PROJECT_ROOT" checkout "$CURRENT_BRANCH" > /dev/null 2>&1
git -C "$PROJECT_ROOT" reset --hard "$LAST_COMMIT" > /dev/null
git -C "$PROJECT_ROOT" clean -fd > /dev/null
echo "  - Repository restored."

# Step 3: State Reset
echo "  - Resetting ANCHOR state to IDLE..."
anchor_state_set "current_gate" null
anchor_state_set "current_milestone" null
anchor_state_set "iteration" 0 "number"
anchor_state_set "tokens_used" 0 "number"
anchor_state_set "no_progress_strikes" 0 "number"

cat << 'EOF' > "$CURRENT_FILE"
# CURRENT
- active_gate: IDLE
- target: none
- iteration: 0/10
- last_gate_result: Milestone rolled back
- last_action: rollback
- next_action: wait for new task
- open_questions: none
EOF

echo "✅ Rollback complete. ANCHOR is back to a clean slate."
