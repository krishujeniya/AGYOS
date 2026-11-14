---
name: carto-mcp
description: Execute spatial SQL queries, analyze geospatial data across cloud data warehouses (Snowflake, BigQuery, Redshift, PostgreSQL), create and publish CARTO Builder maps, and orchestrate spatial analytics workflows via CARTO MCP.
risk: medium
source: official (docs.carto.com/carto-for-agents/mcp-server)
date_added: 2026-11-13
---
# CARTO Spatial MCP Server

Interact with the CARTO Location Intelligence platform and underlying cloud data warehouses directly through the CARTO Model Context Protocol (`carto`) server. Supports spatial data discovery, executing CARTO Analytics Toolbox geospatial SQL, creating and updating CARTO Builder maps, and managing spatial workflows.

## Configuration & Authentication

- **Server URL**: Organization specific endpoint from your CARTO Workspace (`Developers > Workflow API & MCP Server`):
  `https://<region>.api.carto.com/mcp/<account_id>`
- **Environment Variable Fallback**: `CARTO_MCP_URL`
- **Authentication**:
  - **Browser OAuth**: Native SSO / OAuth sign-in flow on first invocation.
  - **API Access Token**: For automated pipelines, an API Access Token with `MCP Server` permissions enabled can be provisioned under `Developers > Credentials`.

## Core Spatial Tools

| Category | Tools | Description |
| :--- | :--- | :--- |
| **Data Discovery** | `explore_data` | List warehouse connections, search tables, inspect schemas and geometry columns |
| **Spatial Queries** | `execute_query`, `execute_async_query` | Run spatial SQL, H3/Quadbin indexing, spatial joins, and CARTO Analytics Toolbox routines |
| **Map Authoring** | `read_maps`, `create_map`, `update_map`, `validate_map` | Complete CARTO Builder map lifecycle with layer styling, SQL sources, and dry-run validation |
| **Workspace Ops** | `manage_api_access_tokens` | Create and revoke scoped API credentials for agent pipelines |

## Standard Workflow

### 1. Spatial Data Discovery
1. Discover connected data warehouses:
   `explore_data(method="list_connections")`
2. Search for spatial tables or datasets:
   `explore_data(method="search", query="boundaries")`
3. Inspect geometry format and column names:
   `explore_data(method="describe", connection_name="snowflake", resource_name="PUBLIC.RETAIL_STORES")`

### 2. Spatial SQL Analysis
1. For quick queries (< 1 minute), run:
   `execute_query(connection_name="bigquery", query="SELECT carto.H3_FROMGEOGPOINT(geom, 8) as h3, count(*) FROM dataset.stores GROUP BY 1")`
2. For heavy spatial aggregations, spatial clustering, or enrichment routines, trigger `execute_async_query`.

### 3. Builder Map Generation
1. Formulate the JSON map bundle with layers, basemap, and SQL sources.
2. Validate the configuration and dry-run SQL:
   `validate_map(map_bundle={...})`
3. Create the map:
   `create_map(title="Store Density Analysis", map_bundle={...}, privacy="private")`
4. Publish when ready:
   `update_map(method="publish", map_id="map-uuid")`

## Invariants & Safety

- Use `validate_map` prior to persisting changes to existing maps to prevent visual or data-binding breaks.
- Use `execute_async_query` for intensive spatial joins or massive spatial tables to prevent timeout aborts.
- Never hardcode warehouse service keys into spatial SQL queries.
