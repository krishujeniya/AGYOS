#!/usr/bin/env node
/**
 * ANCHOR FastMCP Server for AGY-OS
 * Zero-dependency, high-speed Model Context Protocol server over Stdio JSON-RPC 2.0.
 * Exposes Anchor state, milestones, telemetry, and dependency graph.
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");

// Discover project root
function findProjectRoot() {
  let curr = path.resolve(__dirname, "..");
  while (curr !== "/" && !fs.existsSync(path.join(curr, ".git"))) {
    curr = path.resolve(curr, "..");
  }
  return curr;
}

const PROJECT_ROOT = findProjectRoot();
const STATE_DIR = path.join(PROJECT_ROOT, ".agents", "state");

const TOOLS = [
  {
    name: "anchor_state",
    description: "Get the current ANCHOR state including active gate, milestone, iteration, and invariants",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "anchor_current",
    description: "Read the CURRENT.md human-readable session and milestone status summary",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "anchor_graph",
    description: "Read the context-graph.json dependency index and invariant map",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "anchor_checkpoint",
    description: "Get the checkpoint audit trail for a specific milestone",
    inputSchema: {
      type: "object",
      properties: {
        milestone_id: {
          type: "string",
          description: "The milestone identifier (e.g. M1-quality-rules)"
        }
      },
      required: ["milestone_id"]
    }
  }
];

function handleToolCall(name, args) {
  if (name === "anchor_state") {
    const file = path.join(STATE_DIR, "state.json");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : JSON.stringify({ error: "state.json not found" }, null, 2);
    return { content: [{ type: "text", text }] };
  }
  if (name === "anchor_current") {
    const file = path.join(STATE_DIR, "CURRENT.md");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "No CURRENT.md found.";
    return { content: [{ type: "text", text }] };
  }
  if (name === "anchor_graph") {
    const file = path.join(STATE_DIR, "context-graph.json");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : JSON.stringify({ nodes: [], edges: [], invariants: [] });
    return { content: [{ type: "text", text }] };
  }
  if (name === "anchor_checkpoint") {
    const safeMilestone = (args.milestone_id || "").replace(/[^a-zA-Z0-9_-]/g, "");
    const file = path.join(STATE_DIR, "checkpoints", `${safeMilestone}.md`);
    if (!fs.existsSync(file)) {
      return { content: [{ type: "text", text: `Checkpoint for '${safeMilestone}' not found.` }] };
    }
    const text = fs.readFileSync(file, "utf8");
    return { content: [{ type: "text", text }] };
  }
  throw new Error(`Unknown tool: ${name}`);
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on("line", (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  try {
    const request = JSON.parse(trimmed);
    const { id, method, params } = request;

    // Notifications (no id)
    if (id === undefined || id === null) {
      return;
    }

    if (method === "initialize") {
      const response = {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: params?.protocolVersion || "2024-11-05",
          capabilities: {
            tools: {}
          },
          serverInfo: {
            name: "anchor-state-server",
            version: "2.5.0"
          }
        }
      };
      process.stdout.write(JSON.stringify(response) + "\n");
      return;
    }

    if (method === "tools/list") {
      const response = {
        jsonrpc: "2.0",
        id,
        result: {
          tools: TOOLS
        }
      };
      process.stdout.write(JSON.stringify(response) + "\n");
      return;
    }

    if (method === "tools/call") {
      const { name, arguments: toolArgs } = params;
      try {
        const result = handleToolCall(name, toolArgs || {});
        const response = {
          jsonrpc: "2.0",
          id,
          result
        };
        process.stdout.write(JSON.stringify(response) + "\n");
      } catch (err) {
        const response = {
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true
          }
        };
        process.stdout.write(JSON.stringify(response) + "\n");
      }
      return;
    }

    if (method === "ping") {
      process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result: {} }) + "\n");
      return;
    }

    // Default method not found
    process.stdout.write(JSON.stringify({
      jsonrpc: "2.0",
      id,
      error: { code: -32601, message: `Method not found: ${method}` }
    }) + "\n");
  } catch (err) {
    // Malformed JSON
  }
});
