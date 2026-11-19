---
name: carto-mcp
description: Execute spatial SQL queries, analyze geospatial data across cloud data warehouses (Snowflake, BigQuery, Redshift, PostgreSQL), create and publish CARTO Builder maps, and orchestrate spatial analytics workflows via CARTO MCP.
risk: medium
source: official (docs.carto.com/carto-for-agents/mcp-server)
date_added: 2026-11-13
prompt-source: prompt.toon
---
skill: "carto-mcp"
sections[8]:
  - "# CARTO Spatial MCP Server\n\nInteract with the CARTO Location Intelligence platform and underlying cloud data warehouses directly through the CARTO Model Context Protocol (`carto`) server. Supports spatial data discovery, executing CARTO Analytics Toolbox geospatial SQL, creating and updating CARTO Builder maps, and managing spatial workflows.\n\n"
  - "## Configuration & Authentication\n\n- **Server URL**: Organization specific endpoint from your CARTO Workspace (`Developers > Workflow API & MCP Server`):\n  `https://<region>.api.carto.com/mcp/<account_id>`\n- **Environment Variable Fallback**: `CARTO_MCP_URL`\n- **Authentication**:\n  - **Browser OAuth**: Native SSO / OAuth sign-in flow on first invocation.\n  - **API Access Token**: For automated pipelines, an API Access Token with `MCP Server` permissions enabled can be provisioned under `Developers > Credentials`.\n\n"
  - "## Core Spatial Tools\n\n| Category | Tools | Description |\n| :--- | :--- | :--- |\n| **Data Discovery** | `explore_data` | List warehouse connections, search tables, inspect schemas and geometry columns |\n| **Spatial Queries** | `execute_query`, `execute_async_query` | Run spatial SQL, H3/Quadbin indexing, spatial joins, and CARTO Analytics Toolbox routines |\n| **Map Authoring** | `read_maps`, `create_map`, `update_map`, `validate_map` | Complete CARTO Builder map lifecycle with layer styling, SQL sources, and dry-run validation |\n| **Workspace Ops** | `manage_api_access_tokens` | Create and revoke scoped API credentials for agent pipelines |\n\n"
  - "## Standard Workflow\n\n"
  - "### 1. Spatial Data Discovery\n1. Discover connected data warehouses:\n   `explore_data(method=\"list_connections\")`\n2. Search for spatial tables or datasets:\n   `explore_data(method=\"search\", query=\"boundaries\")`\n3. Inspect geometry format and column names:\n   `explore_data(method=\"describe\", connection_name=\"snowflake\", resource_name=\"PUBLIC.RETAIL_STORES\")`\n\n"
  - "### 2. Spatial SQL Analysis\n1. For quick queries (< 1 minute), run:\n   `execute_query(connection_name=\"bigquery\", query=\"SELECT carto.H3_FROMGEOGPOINT(geom, 8) as h3, count(*) FROM dataset.stores GROUP BY 1\")`\n2. For heavy spatial aggregations, spatial clustering, or enrichment routines, trigger `execute_async_query`.\n\n"
  - "### 3. Builder Map Generation\n1. Formulate the JSON map bundle with layers, basemap, and SQL sources.\n2. Validate the configuration and dry-run SQL:\n   `validate_map(map_bundle={...})`\n3. Create the map:\n   `create_map(title=\"Store Density Analysis\", map_bundle={...}, privacy=\"private\")`\n4. Publish when ready:\n   `update_map(method=\"publish\", map_id=\"map-uuid\")`\n\n"
  - "## Invariants & Safety\n\n- Use `validate_map` prior to persisting changes to existing maps to prevent visual or data-binding breaks.\n- Use `execute_async_query` for intensive spatial joins or massive spatial tables to prevent timeout aborts.\n- Never hardcode warehouse service keys into spatial SQL queries.\n"
