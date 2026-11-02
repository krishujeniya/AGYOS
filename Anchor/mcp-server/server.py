#!/usr/bin/env python3
"""
ANCHOR MCP Server
A read-only Model Context Protocol server exposing ANCHOR state.
Requires: pip install mcp
"""

import os
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Define the server
mcp = FastMCP("ANCHOR State Server")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
STATE_DIR = PROJECT_ROOT / ".agents" / "state"

@mcp.resource("anchor://state")
def get_state() -> str:
    """Read the current ANCHOR state.json"""
    state_file = STATE_DIR / "state.json"
    if not state_file.exists():
        return json.dumps({"error": "state.json not found"})
    return state_file.read_text()

@mcp.tool()
def anchor_state() -> str:
    """Get the current ANCHOR state"""
    return get_state()

@mcp.resource("anchor://current")
def get_current() -> str:
    """Read the CURRENT.md session summary"""
    current_file = STATE_DIR / "CURRENT.md"
    if not current_file.exists():
        return "No CURRENT.md found."
    return current_file.read_text()

@mcp.resource("anchor://telemetry")
def get_telemetry() -> str:
    """Read the telemetry log"""
    telemetry_file = STATE_DIR / "telemetry.jsonl"
    if not telemetry_file.exists():
        return ""
    return telemetry_file.read_text()

@mcp.resource("anchor://graph")
def get_graph() -> str:
    """Read the context-graph.json dependency index"""
    graph_file = STATE_DIR / "context-graph.json"
    if not graph_file.exists():
        return json.dumps({"nodes": [], "edges": [], "invariants": []})
    return graph_file.read_text()

@mcp.tool()
def anchor_checkpoint(milestone_id: str) -> str:
    """Get the checkpoint audit trail for a specific milestone"""
    checkpoints_dir = (STATE_DIR / "checkpoints").resolve()
    checkpoint_file = (checkpoints_dir / f"{milestone_id}.md").resolve()
    if not str(checkpoint_file).startswith(str(checkpoints_dir)) or not checkpoint_file.exists():
        return f"Checkpoint for {milestone_id} not found."
    return checkpoint_file.read_text()


if __name__ == "__main__":
    mcp.run()
