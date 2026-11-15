#!/usr/bin/env bash
# Docker Hub MCP Server launcher
# Bridges local AI agents with Docker Hub APIs for container discovery, repository management, and hardened images.
# Upstream repository: https://github.com/docker/hub-mcp
# Distributed container image: mcp/dockerhub
# Auth: Reads PAT from HUB_PAT_TOKEN / DOCKERHUB_PAT / DOCKER_HUB_PAT or ~/.config/docker-hub-mcp/token (chmod 600)
# Username: Reads from DOCKER_HUB_USERNAME / DOCKERHUB_USERNAME or ~/.config/docker-hub-mcp/username
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOKEN_FILE="${DOCKER_HUB_MCP_TOKEN_FILE:-$HOME/.config/docker-hub-mcp/token}"
USER_FILE="${DOCKER_HUB_MCP_USER_FILE:-$HOME/.config/docker-hub-mcp/username}"

# 1. Resolve Personal Access Token (PAT)
TOKEN="${HUB_PAT_TOKEN:-${DOCKERHUB_PAT:-${DOCKER_HUB_PAT:-}}}"
if [[ -z "$TOKEN" && -f "$TOKEN_FILE" ]]; then
  PERMS=$(stat -c "%a" "$TOKEN_FILE" 2>/dev/null || stat -f "%Op" "$TOKEN_FILE" 2>/dev/null || echo "600")
  if [[ "$PERMS" != "600" && "$PERMS" != "400" ]]; then
    echo "ERROR: $TOKEN_FILE has insecure permissions ($PERMS). Run: chmod 600 $TOKEN_FILE" >&2
    exit 1
  fi
  TOKEN=$(cat "$TOKEN_FILE")
fi

if [[ -n "$TOKEN" ]]; then
  export HUB_PAT_TOKEN="$TOKEN"
fi

# 2. Resolve Docker Hub Username
USERNAME="${DOCKER_HUB_USERNAME:-${DOCKERHUB_USERNAME:-}}"
if [[ -z "$USERNAME" && -f "$USER_FILE" ]]; then
  USERNAME=$(cat "$USER_FILE")
fi

# 3. Execution Strategy:
# Preferred 1: Local compiled Node.js build if available
for candidate in \
  "${PROJECT_ROOT}/mcp/hub-mcp/dist/index.js" \
  "${PROJECT_ROOT}/integrations/hub-mcp/dist/index.js" \
  "${PROJECT_ROOT}/integrations/docker-hub-mcp/dist/index.js"; do
  if [[ -f "$candidate" ]]; then
    NODE_ARGS=("$candidate" "--transport=stdio")
    if [[ -n "$USERNAME" ]]; then
      NODE_ARGS+=("--username=$USERNAME")
    fi
    exec node "${NODE_ARGS[@]}" "$@"
  fi
done

# Preferred 2: Containerized runtime via official Docker image (mcp/dockerhub)
if command -v docker >/dev/null 2>&1; then
  DOCKER_ARGS=("run" "-i" "--rm")
  if [[ -n "${HUB_PAT_TOKEN:-}" ]]; then
    DOCKER_ARGS+=("-e" "HUB_PAT_TOKEN")
  fi
  DOCKER_ARGS+=("mcp/dockerhub" "--transport=stdio")
  if [[ -n "$USERNAME" ]]; then
    DOCKER_ARGS+=("--username=$USERNAME")
  fi
  exec docker "${DOCKER_ARGS[@]}" "$@"
fi

echo "ERROR: Neither a compiled Node.js build of docker/hub-mcp nor a functioning Docker runtime was found." >&2
echo "To configure:" >&2
echo "  1. Install Docker and pull the image: docker pull mcp/dockerhub" >&2
echo "  2. Or clone and build https://github.com/docker/hub-mcp into integrations/hub-mcp" >&2
exit 1
