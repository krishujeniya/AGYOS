#!/usr/bin/env bash
# AGYOS MCP Interactive Setup & Token Assistant
# Walks through credentials for all configured local MCP servers.
set -euo pipefail

mkdir -p ~/.config/clerk-mcp ~/.config/deepnote-mcp ~/.config/travis-mcp ~/.config/carto-mcp ~/.config/docker-hub-mcp ~/.config/1password-mcp ~/.config/cloudflare ~/.config/ibmcloud ~/.aws
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

# 5. Docker Hub
prompt_token "Docker Hub PAT" "$HOME/.config/docker-hub-mcp/token" "Generate Personal Access Token in Docker Hub -> Account Settings -> Personal access tokens"
prompt_token "Docker Hub Username" "$HOME/.config/docker-hub-mcp/username" "Your Docker Hub account or organization namespace handle"

# 6. 1Password Service Account
prompt_token "1Password Service Account" "$HOME/.config/1password-mcp/token" "Service account token (ops_...) from 1Password -> Developer -> Service Accounts"

# 7. Cloudflare API Token
prompt_token "Cloudflare API Token" "$HOME/.config/cloudflare/api_token" "API token from Cloudflare Dashboard -> My Profile -> API Tokens"

# 8. IBM Cloud API Key
prompt_token "IBM Cloud API Key" "$HOME/.config/ibmcloud/api_key" "API key from IBM Cloud -> Manage -> Access (IAM) -> API keys"

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
