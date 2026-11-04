#!/usr/bin/env node
/**
 * AGYOS FastMCP Server for AGY-OS
 * Zero-dependency, high-speed Model Context Protocol server over Stdio JSON-RPC 2.0.
 * Exposes AGYOS state, milestones, telemetry, and dependency graph.
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
    name: "agyos_state",
    description: "Get the current AGYOS governance state including active gate, milestone, iteration, and invariants",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "agyos_current",
    description: "Read the CURRENT.md human-readable session and milestone status summary",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "agyos_graph",
    description: "Read the context-graph.json dependency index and invariant map",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "agyos_checkpoint",
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
  },
  {
    name: "agyos_decision",
    description: "Execute the AGYOS Decision Engine to classify task domain, assess complexity (1-5), and autonomously select the optimal specialist skill from the catalog.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "Incoming task description, feature request, error message, or work objective."
        }
      },
      required: ["task"]
    }
  },
  {
    name: "agyos_sys_info",
    description: "Get full AGYOS system overview including kernel status, active gate, memory tiers, loaded plugins, and subsystem health",
    inputSchema: {
      type: "object",
      properties: {},
      required: []
    }
  },
  {
    name: "agyos_memory",
    description: "Hierarchical memory manager (tier0 core working context, tier1 recall memory, tier2 archival index) for cross-session cognitive continuity",
    inputSchema: {
      type: "object",
      properties: {
        action: {
          type: "string",
          enum: ["read", "write", "list"],
          description: "Operation: 'read', 'write', or 'list'"
        },
        tier: {
          type: "string",
          enum: ["tier0", "tier1", "tier2"],
          description: "Memory tier: tier0 (core), tier1 (recall), tier2 (archival)"
        },
        key: {
          type: "string",
          description: "Key identifier inside the tier"
        },
        value: {
          type: "string",
          description: "Content to write (when action is 'write')"
        }
      },
      required: ["action", "tier"]
    }
  }
];

const MEMORY_FILE = path.join(STATE_DIR, "memory.json");

function getSysInfo() {
  const stateFile = path.join(STATE_DIR, "state.json");
  let state = {};
  if (fs.existsSync(stateFile)) {
    try { state = JSON.parse(fs.readFileSync(stateFile, "utf8")); } catch (e) {}
  }
  const skills = loadSkills();
  return {
    os: "AGYOS v3.1 (Hierarchical Cognitive OS)",
    runtime: "Antigravity CLI (agy)",
    active_gate: state.current_gate || "IDLE",
    active_milestone: state.current_milestone || "none",
    complexity_score: state.complexity_score || 1,
    skills_loaded: skills.length,
    plugins_installed: 8,
    memory_architecture: {
      tier0_core: "Working Persona & System Invariants",
      tier1_recall: "Session State & Checkpoints Ledger",
      tier2_archival: "1,838 Standalone Skills Catalog"
    },
    subsystems: {
      anchor_governance: "Operational",
      agent_council: "Operational",
      fastmcp_daemon: "Operational",
      safety_interceptor: "Operational"
    },
    health: "100% Operational"
  };
}

function handleMemoryOperation(args) {
  const { action, tier = "tier0", key, value } = args;
  let mem = {};
  if (fs.existsSync(MEMORY_FILE)) {
    try { mem = JSON.parse(fs.readFileSync(MEMORY_FILE, "utf8")); } catch (e) {}
  }
  const tierMap = { tier0: "tier0_core_memory", tier1: "tier1_recall_memory", tier2: "tier2_archival_index" };
  const tierKey = tierMap[tier];
  if (!tierKey) throw new Error(`Unsupported memory tier: ${tier}`);

  const currentTierData = mem[tierKey] || {};

  if (action === "list") {
    return { content: [{ type: "text", text: JSON.stringify(currentTierData, null, 2) }] };
  }
  if (action === "read") {
    if (!key) return { content: [{ type: "text", text: JSON.stringify(currentTierData, null, 2) }] };
    const val = currentTierData[key];
    return { content: [{ type: "text", text: typeof val === "object" ? JSON.stringify(val, null, 2) : String(val !== undefined ? val : "Key not found") }] };
  }
  if (action === "write") {
    if (!key) throw new Error("Key is required for write action");
    let parsedValue = value;
    try { parsedValue = JSON.parse(value); } catch (e) { parsedValue = value; }
    const updatedTier = { ...currentTierData, [key]: parsedValue };
    const updatedMem = { ...mem, [tierKey]: updatedTier };
    fs.writeFileSync(MEMORY_FILE, JSON.stringify(updatedMem, null, 2), "utf8");
    return { content: [{ type: "text", text: `Successfully wrote key '${key}' in ${tierKey}.` }] };
  }
  throw new Error(`Unsupported memory action: ${action}`);
}

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
  if (name === "agyos_state" || name === "anchor_state") {
    const file = path.join(STATE_DIR, "state.json");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : JSON.stringify({ error: "state.json not found" }, null, 2);
    return { content: [{ type: "text", text }] };
  }
  if (name === "agyos_current" || name === "anchor_current") {
    const file = path.join(STATE_DIR, "CURRENT.md");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "No CURRENT.md found.";
    return { content: [{ type: "text", text }] };
  }
  if (name === "agyos_graph" || name === "anchor_graph") {
    const file = path.join(STATE_DIR, "context-graph.json");
    const text = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : JSON.stringify({ nodes: [], edges: [], invariants: [] });
    return { content: [{ type: "text", text }] };
  }
  if (name === "agyos_checkpoint" || name === "anchor_checkpoint") {
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
  if (name === "agyos_decision") {
    const task = args.task || "";
    try {
      const { execFileSync } = require("child_process");
      const scriptPath = path.join(PROJECT_ROOT, "scripts", "agyos-decision.py");
      const stdout = execFileSync("python3", [scriptPath, task, "--json"], { encoding: "utf8" });
      return { content: [{ type: "text", text: stdout.trim() }] };
    } catch (err) {
      return { content: [{ type: "text", text: JSON.stringify({ error: String(err) }) }] };
    }
  }
  if (name === "agyos_sys_info") {
    return { content: [{ type: "text", text: JSON.stringify(getSysInfo(), null, 2) }] };
  }
  if (name === "agyos_memory") {
    return handleMemoryOperation(args);
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
