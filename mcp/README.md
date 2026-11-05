# Model Context Protocol (MCP) Daemons

This directory contains Model Context Protocol (MCP) daemon implementations.
All MCP tools reside directly in this directory with zero subfolders.

## Components

### `state-server.cjs` (Anchor FastMCP Daemon)
- **Runtime**: Node.js (Zero external dependencies, vanilla JSON-RPC 2.0 over standard I/O).
- **Protocol**: Model Context Protocol (MCP) v2024-11-05.
- **Transport**: `stdio`.
- **Registered Tools**:
  - `anchor_state`: Returns current active milestone, gate status, iteration count, and governance flags from `.agents/state/state.json`.
  - `anchor_current`: Read CURRENT.md human-readable session and milestone status summary.
  - `anchor_graph`: Read context-graph.json dependency index and invariant map.
  - `anchor_checkpoint`: Atomically appends structured machine execution records to `.agents/state/checkpoints/`.
  - `agyos_find_skill`: Search the unified catalog of skills to find the best matching specialist skills.
  - `agyos_sys_info`: Get full system overview including kernel status, active gate, and subsystem health.
  - `agyos_memory`: Hierarchical memory manager for cross-session continuity.

## Verification

The daemon is verified via deterministic JSON-RPC queries:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"anchor_state","arguments":{}}}' | node mcp/state-server.cjs
```

## Select and read a skill

Send this JSON-RPC line to `node mcp/state-server.cjs`:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"agyos_decision","arguments":{"task":"fix python crash","include_runbook":true}}}
```

The result contains the decision JSON and selected runbook. Without
`include_runbook`, `execution_status` remains `pending_runbook_read`; read the
returned `runbook_path` before specialist work. `runbook_returned` confirms
file delivery only. Scores are heuristics, not calibrated probabilities.
Apply relevant steps and report actual verification evidence.
