#!/usr/bin/env node
/**
 * AGYOS FastMCP Server for AGY-OS
 * Zero-dependency, high-speed Model Context Protocol server over Stdio JSON-RPC 2.0.
 * Exposes AGYOS state, milestones, telemetry, and dependency graph.
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const privateVault = require("../scripts/agyos-runtime/lib/private-vault.cjs");

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
    description: "Search the physical AGYOS skill catalog for relevant specialist runbooks. Read and apply the chosen runbook before specialist work.",
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
        },
        include_runbook: {
          type: "boolean",
          description: "Return the selected SKILL.md contents. Delivery does not certify execution."
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
    security_posture: {
      entire_os_e2ee: false,
      encrypted_envelope_exchange: "opt_in_endpoint_file_exchange",
      mcp_memory_writes: privateVault.isInitialized()
        ? "encrypted_local_vault_only" : "blocked_until_vault_init",
      existing_state_logs_checkpoints: "plaintext_unmigrated",
      external_model_prompts: "provider_accessible",
      verified_production_security: false
    },
    health: "Core services available; encryption coverage is partial"
  };
}

let unlockedVaultPassphrase = null;

function publicMemoryBaseline() {
  // This tracked file contains only non-secret legacy defaults. Never mutate it.
  const data = JSON.parse(fs.readFileSync(MEMORY_FILE, "utf8"));
  if (!data || typeof data !== "object" || Array.isArray(data))
    throw new Error("Invalid public legacy memory baseline");
  return data;
}
function encryptedMemory() {
  // A configured encrypted vault must fail closed on missing credentials.
  if (!privateVault.isInitialized()) return {};
  if (unlockedVaultPassphrase === null)
    unlockedVaultPassphrase = privateVault.getPassphrase();
  return privateVault.readVault(privateVault.vaultPath(), unlockedVaultPassphrase);
}
function handleMemoryOperation(args) {
  const { action, tier = "tier0", key, value } = args;
  const tierMap = { tier0: "tier0_core_memory", tier1: "tier1_recall_memory", tier2: "tier2_archival_index" };
  if (!Object.hasOwn(tierMap, tier)) throw new Error("Unsupported memory tier");
  if (key !== undefined && (typeof key !== "string" ||
      !/^[a-zA-Z][a-zA-Z0-9_-]{0,127}$/.test(key) || key === "__proto__" ||
      key === "prototype" || key === "constructor"))
    throw new Error("Invalid memory key");
  if (!["read", "list", "write"].includes(action))
    throw new Error("Unsupported memory action");

  const legacy = publicMemoryBaseline();
  const privateData = encryptedMemory();
  const tierKey = tierMap[tier];
  const currentTierData = { ...(legacy[tierKey] || {}), ...(privateData[tierKey] || {}) };

  if (action === "read" || action === "list") {
    const result = action === "list" || !key
      ? currentTierData : (Object.hasOwn(currentTierData, key) ? currentTierData[key] : "Key not found");
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }

  if (!key || typeof value !== "string" || Buffer.byteLength(value, "utf8") > 64 * 1024)
    throw new Error("A key and bounded string value are required");
  if (!privateVault.isInitialized())
    throw new Error("Encrypted memory not initialized: use bin/agyos secure vault-init");
  if (unlockedVaultPassphrase === null)
    unlockedVaultPassphrase = privateVault.getPassphrase();

  let parsedValue;
  try { parsedValue = JSON.parse(value); } catch { parsedValue = value; }
  privateVault.updateVault(privateVault.vaultPath(), unlockedVaultPassphrase, current => ({
    ...current,
    [tierKey]: { ...(current[tierKey] || {}), [key]: parsedValue }
  }));
  return { content: [{ type: "text", text: "Private memory saved in encrypted local vault." }] };
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
  const { execFileSync } = require("child_process");
  const count = Number.isFinite(limit) ? Math.max(0, Math.min(Math.floor(limit), 20)) : 5;
  const code = [
    "import json,sys",
    "from agyos_decision.skills_router import load_catalog,select_best_skills",
    "catalog=load_catalog()",
    "categories={s['id']:(s.get('category','')+' '+s.get('module','')).lower() for s in json.load(open('docs/skills-data.json'))} if sys.argv[3] else {}",
    "catalog=[s for s in catalog if not sys.argv[3] or sys.argv[3].lower() in categories.get(s['name'],'')]",
    "print(json.dumps(select_best_skills(sys.argv[1],catalog,limit=int(sys.argv[2]))))"
  ].join("\n");
  const output = execFileSync("python3", ["-c", code, query || "", String(count), category || ""], {
    cwd: PROJECT_ROOT, encoding: "utf8", maxBuffer: 4 * 1024 * 1024
  });
  return JSON.parse(output);
}

function formatSkillSearchResults(matches, query) {
  if (matches.length === 0) {
    return `No matching skills found in AGYOS catalog for query: "${query}".`;
  }
  let resultText = `### AGYOS Top Skill Matches for: "${query}"\n\n`;
  matches.forEach((m, idx) => {
    resultText += `${idx + 1}. **\`${m.name}\`** (Tier ${m.tier || 1})\n`;
    resultText += `   - **Path**: \`${m.path}/SKILL.md\`\n`;
    resultText += `   - **Description**: ${m.description || "No description."}\n`;
    resultText += `   - **Inspection**: \`bin/agyos skill ${m.name}\`\n\n`;
  });
  resultText += `> **Search-First Autonomous Invariant**: Read the best matching runbook, apply its relevant steps, and verify the result. Selection alone does not certify execution.`;
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
    const matches = searchSkills(args.query || "", args.limit ?? 5, args.category);
    return { content: [{ type: "text", text: formatSkillSearchResults(matches, args.query || "") }] };
  }
  if (name === "agyos_decision") {
    const task = args.task || "";
    try {
      const { execFileSync } = require("child_process");
      const scriptPath = path.join(PROJECT_ROOT, "scripts", "agyos-decision.py");
      const argv = [scriptPath, task, "--json"];
      if (args.include_runbook === true) argv.push("--runbook");
      const stdout = execFileSync("python3", argv, { encoding: "utf8", maxBuffer: 4 * 1024 * 1024 });
      return { content: [{ type: "text", text: stdout.trim() }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: JSON.stringify({ error: String(err) }) }] };
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

const MAX_MCP_LINE_BYTES = 1024 * 1024;
function rpcError(id, code, message) {
  process.stdout.write(JSON.stringify({
    jsonrpc: "2.0", id, error: { code, message }
  }) + "\n");
}
function rpcResult(id, result) {
  process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result }) + "\n");
}
const rl = readline.createInterface({
  input: process.stdin,
  terminal: false,
  crlfDelay: Infinity
});
rl.on("line", line => {
  if (!line.trim()) return;
  // readline still buffers a line prior to callback. This bounds parsing and
  // downstream execution, not total input buffering; process isolation remains required.
  if (Buffer.byteLength(line, "utf8") > MAX_MCP_LINE_BYTES) {
    rpcError(null, -32600, "MCP input exceeds 1 MiB");
    return;
  }
  let request;
  try {
    request = JSON.parse(line);
  } catch {
    rpcError(null, -32700, "Parse error");
    return;
  }
  if (!request || typeof request !== "object" || Array.isArray(request) ||
      request.jsonrpc !== "2.0" || typeof request.method !== "string") {
    rpcError(null, -32600, "Invalid JSON-RPC request");
    return;
  }
  const { id, method, params } = request;
  if (id === undefined || id === null) {
    // MCP notifications never receive a response.
    return;
  }
  if (typeof id !== "number" && typeof id !== "string") {
    rpcError(null, -32600, "Invalid request ID");
    return;
  }
  if (method === "initialize") {
    rpcResult(id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "anchor-state-server", version: "2.5.1" }
    });
    return;
  }
  if (method === "tools/list") {
    rpcResult(id, { tools: TOOLS });
    return;
  }
  if (method === "tools/call") {
    if (!params || typeof params !== "object" || Array.isArray(params) ||
        typeof params.name !== "string" ||
        (params.arguments !== undefined &&
         (!params.arguments || typeof params.arguments !== "object" ||
          Array.isArray(params.arguments)))) {
      rpcError(id, -32602, "Invalid tool arguments");
      return;
    }
    const tool = TOOLS.find(item => item.name === params.name);
    if (!tool) {
      rpcError(id, -32602, "Unknown tool");
      return;
    }
    const args = params.arguments || {};
    for (const required of tool.inputSchema.required || []) {
      if (!Object.prototype.hasOwnProperty.call(args, required)) {
        rpcError(id, -32602, "Missing required tool argument");
        return;
      }
    }
    try {
      rpcResult(id, handleToolCall(params.name, args));
    } catch {
      // Never disclose local filesystem paths, key file errors, stack traces
      // or stderr from subprocesses through a public MCP result.
      rpcResult(id, {
        isError: true, content: [{
          type: "text", text: "AGYOS tool failed; consult local protected diagnostics."
        }]
      });
    }
    return;
  }
  if (method === "ping") {
    rpcResult(id, {});
    return;
  }
  rpcError(id, -32601, "Method not found");
});
