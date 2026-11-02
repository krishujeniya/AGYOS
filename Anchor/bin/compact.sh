#!/usr/bin/env bash

# ANCHOR Context Compactor (COMPACT gate)
# Generates a fresh CURRENT.md skeleton for the agent to populate before IMPLEMENT.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="${PROJECT_ROOT}/.agents/state"
CURRENT_FILE="${STATE_DIR}/CURRENT.md"
GRAPH_FILE="${STATE_DIR}/context-graph.json"

mkdir -p "$STATE_DIR"

if [ ! -f "$GRAPH_FILE" ]; then
    echo "Warning: No context-graph.json found. Creating a minimal skeleton."
    NODES="None"
else
    # Extract nodes if possible using jq
    if command -v jq >/dev/null 2>&1; then
        NODES=$(jq -r '.nodes[].id' "$GRAPH_FILE" 2>/dev/null || echo "Failed to parse context graph.")
    else
        NODES="jq not installed, cannot parse context graph."
    fi
fi

cat <<EOF > "$CURRENT_FILE"
# CURRENT.md (Structured Handoff)

## 1. Goal
*(Agent: Summarize the current approved implementation plan goal here)*

## 2. Spec Pointer
*(Agent: Link to the specific milestone or plan artifact)*

## 3. File List & Context Graph
*(Agent: List only the files actively being modified)*
**Tracked Modules:**
$NODES

## 4. Open Questions
*(Agent: Any unresolved ambiguities)*

## 5. Next Action
*(Agent: The immediate next command or step to take in IMPLEMENT)*

EOF

echo "Generated compact skeleton at $CURRENT_FILE"
