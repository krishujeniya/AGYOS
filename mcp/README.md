# AGYOS MCP Architecture & Daemons

This directory contains the Model Context Protocol (MCP) server implementations and example starter packages for the AGYOS ecosystem.

## Components

### 1. `agyos-state-server.cjs` (Anchor FastMCP Daemon)
- **Runtime**: Node.js (Zero external dependencies, vanilla JSON-RPC 2.0 over standard I/O).
- **Protocol**: Model Context Protocol (MCP) v2024-11-05.
- **Port / Transport**: `stdio`.
- **Registered Tools**:
  - `anchor_state`: Returns current active milestone, gate status, iteration count, and governance flags from `.agents/state/state.json`.
  - `anchor_checkpoint`: Atomically appends structured machine execution records to `.agents/state/checkpoints/`.
- **Registration**: Registered in `~/.gemini/config/mcp_config.json` under the server key `anchor`.

### 2. `examples/contra-mcp-starter/`
- Example MCP server development template demonstrating tool definition, prompt registration, and resource exposure.

## Verification

The FastMCP daemon is verified via deterministic JSON-RPC queries:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"anchor_state","arguments":{}}}' | node mcp/agyos-state-server.cjs
```
