#!/usr/bin/env bash
# IBM MCP Server launcher (docling, watsonxdata, carbon)
# Auth: fetches a fresh IAM token from `ibmcloud` CLI at startup.
# Requires `ibmcloud login` to have been run once. Tokens are injected as env vars.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Inject IBM Cloud credentials from CLI session
export IBMCLOUD_REGION="${IBMCLOUD_REGION:-in-mum}"
export IBMCLOUD_ACCOUNT_ID="${IBMCLOUD_ACCOUNT_ID:-9b8df9c9897a405b95d55653bb400ace}"

# Fetch a fresh IAM token from the authenticated ibmcloud CLI
IBM_IAM_TOKEN="$("$SCRIPT_DIR/ibm-token-helper.sh" 2>/dev/null || true)"
if [[ -n "$IBM_IAM_TOKEN" ]]; then
  export IBMCLOUD_IAM_TOKEN="$IBM_IAM_TOKEN"
fi

SERVER="${1:-docling}"
shift || true

case "$SERVER" in
  docling)
    exec uvx --from docling-mcp docling-mcp-server --transport stdio "$@"
    ;;
  watsonx)
    exec uvx --from git+https://github.com/IBM/ibm-watsonxdata-mcp-server \
      ibm-watsonxdata-mcp-server "$@"
    ;;
  carbon)
    exec npx -y @carbon/mcp "$@"
    ;;
  *)
    echo "Usage: $0 [docling|watsonx|carbon]" >&2
    exit 1
    ;;
esac
