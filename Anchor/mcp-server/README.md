# ANCHOR MCP Server

A read-only [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes the internal state of the ANCHOR framework to MCP-compatible clients (like Claude Code, Cursor, and others).

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running
Configure your MCP client to spawn this server:
```bash
python3 /path/to/Anchor/mcp-server/server.py
```
