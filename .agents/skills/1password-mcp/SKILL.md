---
name: 1password-mcp
description: Manage and inject secrets, list vaults, search vault items, and resolve op:// secret reference URIs programmatically using the 1Password CLI and 1Password Model Context Protocol (MCP) server.
risk: medium
source: official (developer.1password.com)
date_added: 2026-11-14
---
# 1Password MCP Server

Bridge 1Password's vault storage directly into AI agent workflows using the official 1Password CLI (`op`) and the `1password-mcp` stdio server. Allows agents to resolve secret references (`op://`), list available vaults, inspect item metadata, and authenticate environments safely without hardcoding secrets in configuration files.

## Prerequisites & Authentication

The server supports two authentication modes:

### 1. Service Account (Recommended for Agents / Headless)
Create a Service Account in your 1Password console (*Developer > Service Accounts*), grant read permissions to the necessary vaults, and configure the token:

```bash
# Save to secure config file
echo -n "opsa_your_service_account_token" > ~/.config/1password-mcp/token
chmod 600 ~/.config/1password-mcp/token

# Or set via environment variable
export OP_SERVICE_ACCOUNT_TOKEN="opsa_..."
```

### 2. User Account (Interactive Desktop Sign-in)
If signed into the 1Password desktop app or interactive terminal via `op signin`, the CLI will automatically inherit session authorization.

## Available Tools

| Tool | Purpose | Parameters |
| :--- | :--- | :--- |
| `op_whoami` | Verify authentication status and account details | None |
| `op_list_vaults` | List accessible vaults (returns names and IDs) | None |
| `op_list_items` | List items within a vault or across vaults | `vault` (optional), `categories` (optional) |
| `op_get_item` | Fetch item details, field layouts, and metadata | `item` (required), `vault` (optional) |
| `op_read_reference` | Resolve a secret reference (`op://Vault/Item/field`) | `reference` (required) |

## Standard Agent Workflows

### 1. Secret Injection via `op://` URIs
Instead of pasting API keys into prompt instructions:
1. Store the secret in 1Password (e.g. Vault `Production`, Item `Stripe`, Field `api_key`).
2. Instruct the agent using the reference URI:
   `op_read_reference(reference="op://Production/Stripe/api_key")`
3. Pass the resolved token directly into ephemeral tool runtime invocations.

### 2. Discovering Vault Contents
1. Verify access:
   `op_whoami()`
2. List available vaults:
   `op_list_vaults()`
3. List credentials in a target vault:
   `op_list_items(vault="Engineering", categories="API Credential")`

## Security Invariants

- **Least Privilege**: Only assign your Service Account access to the specific vaults required for the active workspace.
- **No Disk Leakage**: Never dump resolved secret values into markdown notes, chat artifacts, or committed repository files.
- **Reference Over Plaintext**: Always prefer passing `op://` reference syntax in code and CI templates over storing raw strings.
