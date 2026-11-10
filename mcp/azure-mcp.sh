#!/usr/bin/env bash
# Azure MCP Server launcher
# Auth: inherits from `az login` — credentials live in ~/.azure, the SDK picks them up automatically.
# No tokens are hard-coded here. Run `az login` once; this launcher needs no extra steps.
set -euo pipefail

export AZURE_SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:-60da109a-8501-4d1d-8c58-12f62c231164}"

exec npx -y @azure/mcp@latest server start "$@"
