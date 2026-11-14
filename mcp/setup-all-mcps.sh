#!/usr/bin/env bash
# AGYOS MCP Interactive Setup & Token Assistant
# Walks through credentials for all configured local MCP servers.
set -euo pipefail

mkdir -p ~/.config/clerk-mcp ~/.config/deepnote-mcp ~/.config/travis-mcp ~/.config/carto-mcp
chmod 700 ~/.config/*mcp* 2>/dev/null || true

echo "=================================================="
echo "    AGYOS MCP Services & Credentials Setup        "
echo "=================================================="
echo ""

prompt_token() {
  local service_name="$1"
  local token_file="$2"
  local instructions="$3"

  echo "--------------------------------------------------"
  echo "[$service_name Setup]"
  echo "Instructions: $instructions"
  if [[ -s "$token_file" ]]; then
    echo "Status: Configured in $token_file"
    read -r -p "Do you want to update/overwrite it? (y/N): " update_choice
    if [[ ! "$update_choice" =~ ^[Yy]$ ]]; then
      echo "Kept existing credential."
      return 0
    fi
  else
    echo "Status: Not yet set"
  fi

  read -r -s -p "Enter $service_name credential/token (or press ENTER to skip): " input_val
  echo ""
  if [[ -n "$input_val" ]]; then
    echo -n "$input_val" > "$token_file"
    chmod 600 "$token_file"
    echo "Saved and secured: $token_file"
  else
    echo "Skipped for now."
  fi
}

# 1. Clerk
prompt_token "Clerk Agent Toolkit" "$HOME/.config/clerk-mcp/token" "Get your secret key (sk_live_... or sk_test_...) from Clerk Dashboard -> API Keys"

# 2. Deepnote
prompt_token "Deepnote" "$HOME/.config/deepnote-mcp/token" "Generate API key in Deepnote -> Workspace Settings -> Security -> API keys"

# 3. Travis CI
prompt_token "Travis CI" "$HOME/.config/travis-mcp/token" "Generate API token from your Travis CI User Settings -> Settings -> API authentication"

# 4. CARTO (Optional API token for automated pipelines)
prompt_token "CARTO API Token" "$HOME/.config/carto-mcp/token" "Optional: Developers -> Credentials -> Create API Access Token with MCP Server permissions"

echo ""
echo "=================================================="
echo "OAuth-based Remote Servers (Browser-based):"
echo "  • Camber Cloud (camber-mcp) -> https://camber-mcp.cambercloud.com/mcp"
echo "  • IconScout (iconscout-mcp) -> https://mcp.iconscout.com/mcp"
echo "  • TestMu AI / LambdaTest (mcp-lambdatest) -> https://mcp.lambdatest.com/mcp"
echo "  • CARTO (carto) -> Direct browser SSO upon first call"
echo "These will launch an OAuth browser verification prompt automatically when invoked."
echo "=================================================="
echo "Setup assistant complete."
