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
  },
  {
    name: "agyos_find_skill",
    description: "Search the unified AGYOS catalog of 1,838+ skills to find the best matching specialist skills for any task, prompt, technology, or problem domain.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Task description, programming language, framework, problem, or keywords (e.g. 'react animation', 'postgres migration', 'docker deploy', 'stripe webhook', 'bug diagnosis')"
        },
        limit: {
          type: "number",
          description: "Maximum number of matching skills to return (default: 5, max: 20)"
        },
        category: {
          type: "string",
          description: "Optional category filter"
        }
      },
      required: ["query"]
    }
  }
];

let cachedSkills = null;

function loadSkills() {
  if (cachedSkills) return cachedSkills;
  const docsDataFile = path.join(PROJECT_ROOT, "docs", "skills-data.json");
  if (fs.existsSync(docsDataFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(docsDataFile, "utf8"));
      cachedSkills = data.map(item => ({
        name: item.id || item.name,
        tier: item.tier || 1,
        description: item.description || "",
        path: item.path || `.agents/skills/${item.id}`,
        category: (item.category || item.module || "").toLowerCase()
      }));
      return cachedSkills;
    } catch (e) {}
  }
  const manifestFile = path.join(PROJECT_ROOT, ".agents", "skills-manifest.json");
  if (fs.existsSync(manifestFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
      cachedSkills = (data.skills || []).map(item => ({
        ...item,
        category: ""
      }));
      return cachedSkills;
    } catch (e) {}
  }
  return [];
}

function searchSkills(query, limit = 5, category = null) {
  const skills = loadSkills();
  if (!query || typeof query !== "string") {
    return skills.slice(0, limit);
  }
  
  const cleanQuery = query.toLowerCase().trim();
  const tokens = cleanQuery.split(/[\s,._-]+/).filter(t => t.length > 0);
  const scored = [];
  const catFilter = category ? category.toLowerCase().trim() : null;
  
  for (const s of skills) {
    if (catFilter && s.category && !s.category.includes(catFilter)) {
      continue;
    }
    const sName = (s.name || "").toLowerCase();
    const sDesc = (s.description || "").toLowerCase();
    let score = 0;
    
    if (sName === cleanQuery) {
      score += 150;
    } else if (cleanQuery.length > 1 && sName.includes(cleanQuery)) {
      score += 60;
    }
    
    for (const token of tokens) {
      if (sName === token) score += 40;
      else if (token.length > 1 && sName.includes(token)) score += 20;
      
      if (token.length > 2 && sDesc.includes(token)) score += 6;
    }
    
    if (score > 0) {
      if (s.tier === 1) score += 4; // Tier 1 core software boost
      scored.push({ skill: s, score });
    }
  }
  
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, Math.min(limit, 20)).map(item => item.skill);
}

function formatSkillSearchResults(matches, query) {
  if (matches.length === 0) {
    return `No matching skills found in AGYOS catalog for query: "${query}".`;
  }
  let resultText = `### 🎯 AGYOS Top Skill Matches for: "${query}"\n\n`;
  matches.forEach((m, idx) => {
    resultText += `${idx + 1}. **\`${m.name}\`** (Tier ${m.tier || 1})\n`;
    resultText += `   - **Path**: \`${m.path}/SKILL.md\`\n`;
    resultText += `   - **Description**: ${m.description || "No description."}\n`;
    resultText += `   - **Inspection**: \`bin/agyos skill ${m.name}\`\n\n`;
  });
  resultText += `> **Search-First Autonomous Invariant**: Ingest the top matching skill runbook before modifying code.`;
  return resultText;
}

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
    return { content: [{ type: "text", text: fs.readFileSync(file, "utf8") }] };
  }
  if (name === "agyos_find_skill" || name === "anchor_find_skill") {
    const matches = searchSkills(args.query || "", args.limit || 5, args.category);
    return { content: [{ type: "text", text: formatSkillSearchResults(matches, args.query || "") }] };
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
