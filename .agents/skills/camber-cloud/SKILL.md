---
name: camber-cloud
description: Interact with the Camber data science and agentic platform via its MCP server. Create, discover, and chat with Camber agents; manage team and personal workspaces; and orchestrate multi-agent data workflows.
risk: low
source: official (cambercloud.com)
date_added: 2026-11-13
---
# Camber Cloud

Interact with the [Camber](https://cambercloud.com) agentic data science platform through its hosted MCP server (`camber-mcp`). Camber lets you build, deploy, and compose AI agents that share data, collaborate on tasks, and integrate with your existing toolchain.

## MCP Server

**Endpoint:** `https://camber-mcp.cambercloud.com/mcp`  
**Auth:** OAuth (browser-based, no manual API key required). On first use the client will open an OAuth flow mapped to your Camber account.

## Available Tools

| Tool | Purpose |
|------|---------|
| `usage_guide` | Onboarding instructions for the active session |
| `user_info` | Authenticated user profile and team associations |
| `teams_list` | List personal and team workspaces |
| `teams_select` | Switch the active workspace (`team_name` or `personal=true`) |
| `agents_list` | List agents filtered by scope (`personal` / `team` / `all`) |
| `agents_create` | Create a new agent in the active workspace |
| `agents_chat` | Chat with an agent via its `@owner.alias` tag |

## Workflow

1. **Confirm scope** — verify the task involves Camber agent management, workspace selection, or agent-to-agent orchestration.
2. **Check session** — call `user_info` to confirm the OAuth session is active. If not, follow the OAuth prompt before proceeding.
3. **Select workspace** — call `teams_list` to discover available workspaces, then `teams_select` to activate the correct one.
4. **Discover agents** — call `agents_list` with the appropriate scope to find existing agents before creating new ones.
5. **Execute the task**:
   - To chat with an existing agent: call `agents_chat` with the full `@owner.alias` tag and your message.
   - To create an agent: call `agents_create` with `name`, `alias`, and optionally `description` and `system_prompt`.
6. **Report results** — summarise what workspace is active, which agents were involved, and the agent's response or the created agent's details.

## Usage Patterns

### Chat with an existing agent
```text
# 1. Discover the agent tag
agents_list scope="all"

# 2. Chat
agents_chat agent_tag="@alice.researcher" message="Summarise last quarter's sales data"
```

### Create an agent in a team workspace
```text
# 1. Switch to the team workspace
teams_select team_name="data-science"

# 2. Create the agent
agents_create name="Pipeline Monitor" alias="pipeline-monitor" description="Monitors ETL pipeline health and alerts on anomalies"
```

### Orchestrate multi-agent workflow
```text
# Chain agents: send output from one as input to another
agents_chat agent_tag="@team.cleaner" message="Clean the uploaded CSV and return a summary"
# → take the summary
agents_chat agent_tag="@team.analyst" message="Given this summary: <output>, produce a trend report"
```

## Constraints

- Always call `user_info` first if the OAuth session state is unknown.
- Do not store OAuth tokens or session credentials in any file or repository.
- Workspace selection (`teams_select`) is required before creating team agents.
- Agent aliases must be unique within the workspace — call `agents_list` to verify before `agents_create`.
- Do not invoke destructive or billing-impacting actions without explicit user confirmation.
