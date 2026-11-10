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

### `azure-mcp.sh` (Microsoft Azure MCP Server)
- **Runtime**: Node.js via `npx -y @azure/mcp@latest server start`.
- **Upstream**: [`microsoft/mcp`](https://github.com/microsoft/mcp).
- **Transport**: `stdio`.
- **Coverage**: Unified Azure operations across subscriptions, resource groups, App Service, Functions, AKS, ACR, Container Apps, Cosmos DB, Azure SQL, Blob Storage, Key Vault, Monitor, AI Search, OpenAI, and Well-Architected Framework best practices.
- **Authentication**: Azure CLI (`az login`), Azure Developer CLI (`azd auth login`), or `DefaultAzureCredential` environment variables.

### `aws-mcp.sh` (AWS Labs MCP Servers)
- **Runtime**: Python FastMCP via `uvx`.
- **Upstream**: [`awslabs/mcp`](https://github.com/awslabs/mcp).
- **Transport**: `stdio`.
- **Modes**:
  - `aws-api-mcp` (`./mcp/aws-mcp.sh api`): Universal AWS API execution (`call_aws`, `suggest_aws_commands`) across all AWS services.
  - `aws-docs-mcp` (`./mcp/aws-mcp.sh docs`): Search and retrieve official AWS documentation.
  - `aws-iac-mcp` (`./mcp/aws-mcp.sh iac`): CloudFormation, AWS CDK, and Terraform synthesis and validation.
- **Authentication**: Standard AWS credential chain (`~/.aws/credentials`, `AWS_PROFILE`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`).

### `ibm-mcp.sh` (IBM MCP Servers)
- **Runtime**: Python / Node.js via `uvx` and `npx`.
- **Upstream**: [`IBM/mcp`](https://github.com/IBM/mcp).
- **Transport**: `stdio`.
- **Modes**:
  - `ibm-docling-mcp` (`./mcp/ibm-mcp.sh docling`): IBM Docling document understanding, multi-format conversion (PDF, DOCX, PPTX to Markdown/JSON), and RAG extraction.
  - `ibm-watsonxdata-mcp` (`./mcp/ibm-mcp.sh watsonxdata`): IBM watsonx.data lakehouse engine management and queries.
  - `ibm-carbon-mcp` (`./mcp/ibm-mcp.sh carbon`): IBM Carbon Design System component exploration and tokens.

### `kaggle-mcp.sh` (Kaggle Remote MCP Bridge)
- **Runtime**: Node.js via `npx -y mcp-remote https://www.kaggle.com/mcp`.
- **Transport**: `stdio` wrapper over remote HTTP endpoint.
- **Authentication**: Bearer token loaded securely from `~/.config/kaggle-mcp/token` (file permission `600`).
- **Coverage**: Notebooks, datasets, competitions, models, and benchmarks.

### `mongodb-mcp.sh` (MongoDB MCP Server)
- **Runtime**: Node.js via `mongodb-mcp-server` (`@mongodb-js/mongodb-mcp-server`).
- **Upstream**: [`mongodb-js/mongodb-mcp-server`](https://github.com/mongodb-js/mongodb-mcp-server).
- **Transport**: `stdio`.
- **Authentication**: Authenticated via MongoDB Atlas CLI (`atlas`) Service Account OAuth 2.0 Client Credentials stored in `~/.config/mongodb-mcp/credentials` (file permission `600`).
- **Coverage**: 49 tools across MongoDB Database operations (`find`, `aggregate`, `collection-schema`, `create-index`, `insert-many`, `update-many`, `delete-many`) and MongoDB Atlas cluster/project management (`atlas-list-clusters`, `atlas-list-projects`, `atlas-inspect-cluster`, `atlas-create-access-list`, `atlas-list-db-users`, `atlas-get-performance-advisor`, etc.).

### `google-flow-mcp.sh` (Google Flow MCP Server)
- **Runtime**: Node.js v24 via [`integrations/google-flow-mcp`](../integrations/google-flow-mcp).
- **Upstream**: [`ParkSangGwon/google-flow-mcp`](https://github.com/ParkSangGwon/google-flow-mcp).
- **Transport**: `stdio`.
- **Authentication**: Reuses existing authenticated Google Chrome session and cookies from `~/.config/google-chrome/Default` synchronized into `~/.google-flow-chrome`.
- **CDP Port**: `9333` (auto-launches dedicated Chrome or attaches to existing instance).
- **Coverage**: 11 tools for Google Flow automation:
  - `flow_connect`: Attach to dedicated Chrome instance and verify login state.
  - `flow_status`: Query active session and running generation jobs.
  - `flow_screenshot`: Inspect current tab state via screenshot.
  - `flow_inspect`: Probe DOM elements and selectors.
  - `flow_project_open`: Open or switch to a Google Flow project.
  - `flow_generate_video`: Video generation via Google Veo.
  - `flow_generate_image`: Image generation via Nano Banana.
  - `flow_media_download`: Download generated assets to local disk.
  - `flow_scene_add`: Add scene to Scene Builder.
  - `flow_scene_status`: Check status of Scene Builder scenes.
  - `flow_scene_extend`: Extend existing video scene.

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
