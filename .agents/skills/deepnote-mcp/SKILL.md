---
name: deepnote-mcp
description: Interact with Deepnote collaborative notebooks via its MCP server. Create, edit, and execute Python and SQL notebooks; manage projects, folders, integrations (Snowflake, BigQuery, Postgres), Streamlit apps, and compute machines programmatically from any AI agent or coding assistant.
risk: medium
source: official (deepnote.com/docs/deepnote-mcp)
date_added: 2026-11-13
---
# Deepnote MCP

Drive the full Deepnote collaborative data science platform through its MCP server (`@deepnote/mcp`). Create notebooks, run Python and SQL blocks, inspect outputs, manage integrations, and deploy Streamlit apps — all from an AI agent.

## MCP Server

**Package:** `@deepnote/mcp` (official, run via `npx`)  
**Auth options:**
- **API key** (recommended for agents): Generate under *Workspace → Settings & members → Security → API keys*. Store as `DEEPNOTE_API_KEY`.
- **OAuth**: For interactive clients (Claude Desktop, Cursor) pointing to `https://deepnote.com/mcp` — triggers browser sign-in automatically.

The AGYOS `mcp_config.json` registers this as `deepnote-mcp` using `${DEEPNOTE_API_KEY}`. Set before starting Antigravity:

```bash
export DEEPNOTE_API_KEY="your_api_key_here"
```

## Tool Domains

| Domain | Tools | Mode |
|--------|-------|------|
| **Account & workspace** | `get_me`, `search`, `list_projects`, `list_folders`, `create_folder` | Read / Write |
| **Projects** | `get_project`, `create_project`, `update_project`, `delete_project`, `generate_project_url` | Read / Write |
| **Notebooks** | `get_notebook`, `create_notebook`, `update_notebook`, `duplicate_notebook`, `delete_notebook` | Read / Write |
| **Blocks** | `get_block`, `create_block`, `update_block`, `delete_block`, `reorder_notebook_blocks` | Read / Write |
| **Runs (execution)** | `create_run`, `get_run`, `list_notebook_runs` | Write |
| **Integrations** | `list_integrations`, `get_integration`, `attach_integration`, `detach_integration` | Read / Write |
| **Apps** | `create_streamlit_app`, `list_streamlit_apps`, `get_streamlit_app_status`, `create_data_app_token` | Write |
| **Machines** | `restart_machine`, `update_machine`, `list_machine_types`, `list_environments` | Write |

> [!NOTE]
> Read-only tools (`get_*`, `list_*`, `search`) require only viewer access. Write and execution tools require editor access or an API key with edit permissions.

## Workflow

### Standard agentic notebook task
1. **Confirm auth** — call `get_me` to verify the API key is valid and check permission level.
2. **Locate resources** — use `list_projects` or `search` to find the target project and notebook. Note the IDs.
3. **Inspect the notebook** — call `get_notebook` to understand existing block structure before making changes.
4. **Make changes** — use `create_block` / `update_block` / `reorder_notebook_blocks` as needed. Keep changes minimal and scoped.
5. **Execute** — call `create_run` on the notebook, then poll `get_run` until status is `completed` or `failed`.
6. **Inspect outputs** — call `get_run` with `include_outputs: true` or `get_block` with `include_outputs: true` to retrieve results.
7. **Report** — summarise what ran, what blocks were added/changed, and any errors from outputs.

### Create a new analysis from scratch
```text
1. list_projects                          → find or create a project
2. create_project name="Q4 Analysis"     → new project
3. create_notebook project_id=... name="EDA"
4. create_block notebook_id=... type="python" content="import pandas as pd\ndf = pd.read_csv('data.csv')\ndf.head()"
5. create_block notebook_id=... type="python" content="df.describe()"
6. create_run notebook_id=...
7. get_run run_id=... include_outputs=true
```

### SQL analysis against a data warehouse
```text
1. list_integrations type="snowflake"     → find integration ID
2. attach_integration project_id=... integration_id=...
3. create_block notebook_id=... type="sql" integration_id=... content="SELECT * FROM orders LIMIT 100"
4. create_run notebook_id=...
5. get_run run_id=... include_outputs=true
```

### Deploy a Streamlit app
```text
1. create_block notebook_id=... type="python" content="<streamlit app code>"
   # or upload app.py as a project file
2. create_streamlit_app project_id=... file_path="app.py"
3. get_streamlit_app_status app_id=...   → wait for "running"
4. Return the app URL to the user
```

## Block Types Reference

| Type | Use for |
|------|---------|
| `python` | General code, data processing, ML, visualisations |
| `sql` | Queries against attached integrations (Snowflake, BigQuery, Postgres, etc.) |
| `text` | Markdown documentation, section headings, report narrative |
| `input` | User-facing input variables that parameterise the notebook |

## Security Constraints

- Never store `DEEPNOTE_API_KEY` in any file tracked by git.
- Confirm before calling `delete_project`, `delete_notebook`, or `delete_block` — deletions move to trash but confirm the user intends it.
- Do not call `restart_machine` without confirming the user understands it clears all in-memory kernel state.
- When a run fails, call `get_run` with `include_outputs: true` and report the error verbatim before proposing a fix.
- Use `create_data_app_token` only for preview purposes; tokens are short-lived and scoped to viewer access.

## Related Skills

- `data-storytelling` — narrative structure for Deepnote reports and data apps
- `matplotlib` / `seaborn` / `plotly` — visualisation code for Python blocks
- `database-design` — schema planning before writing SQL blocks
- `elite-python-architect` — Python code quality within notebook blocks
