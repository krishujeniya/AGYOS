---
name: docker-hub-mcp
description: Discover container images, inspect repository metadata and tags, verify image architectures, create repositories, and query Docker Hardened Images using the official Docker Hub MCP server (docker/hub-mcp).
risk: low
source: official (github.com/docker/hub-mcp)
date_added: 2026-11-15
---
# Docker Hub MCP Server

Bridge Docker Hub directly into AI agent workflows using the official Docker Hub Model Context Protocol server (`docker/hub-mcp`). Enables agents to search public and private repositories, verify tag existence and multi-architecture platform variants, manage repository descriptions, and query certified Docker Hardened Images.

## Prerequisites and Authentication

The server supports both anonymous access (public repository discovery) and authenticated access (full repository management and private content inspection).

### 1. Credentials Configuration

The launcher script [`docker-hub-mcp.sh`](file:///home/ai/Documents/projects/Freelance/AGYOS/mcp/docker-hub-mcp.sh) resolves credentials in this order:

- **Personal Access Token (PAT):**
  1. `HUB_PAT_TOKEN`, `DOCKERHUB_PAT`, or `DOCKER_HUB_PAT` environment variable
  2. `~/.config/docker-hub-mcp/token` (file permission `600`)

- **Docker Hub Username:**
  1. `DOCKER_HUB_USERNAME` or `DOCKERHUB_USERNAME` environment variable
  2. `~/.config/docker-hub-mcp/username` (plain text)

To store credentials securely:

```bash
mkdir -p ~/.config/docker-hub-mcp
echo -n "dckr_pat_your_token_here" > ~/.config/docker-hub-mcp/token
chmod 600 ~/.config/docker-hub-mcp/token
echo -n "your_docker_username" > ~/.config/docker-hub-mcp/username
```

### 2. Runtime Execution

The server runs via either:
1. Containerized execution using the official Docker Hub image `mcp/dockerhub` (`docker run -i --rm mcp/dockerhub --transport=stdio`).
2. Local compiled Node.js build (`node integrations/hub-mcp/dist/index.js --transport=stdio`).

## Available Tools

| Tool | Purpose | Read/Write | Parameters |
| :--- | :--- | :--- | :--- |
| `search` | Search repositories on Docker Hub by keyword, filter by operating system and architecture | Read | `query` (string), `page` (number), `page_size` (number) |
| `checkRepository` | Verify whether a specific repository exists in a namespace | Read | `namespace` (string), `repository` (string) |
| `checkRepositoryTag` | Verify whether a specific tag exists for a repository | Read | `namespace` (string), `repository` (string), `tag` (string) |
| `getRepositoryInfo` | Retrieve repository metadata, description, pull count, and star count | Read | `namespace` (string), `repository` (string) |
| `listRepositoriesByNamespace` | List all repositories under an organization or user namespace | Read | `namespace` (string), `page` (number), `page_size` (number) |
| `listRepositoryTags` | List all tags, digest hashes, and supported architectures for a repository | Read | `namespace` (string), `repository` (string), `page` (number), `page_size` (number) |
| `createRepository` | Create a new repository in a namespace | Write | `namespace` (string), `repository` (string), `description` (string, optional), `is_private` (boolean) |
| `dockerHardenedImages` | Search and inspect Docker Hardened Images (DHI) with security attestations | Read | `query` (string), `page` (number), `page_size` (number) |

## Standard Agent Workflows

### 1. Base Image Verification for Dockerfile Scaffolding
Before selecting a base image for application containerization:
1. Search official or trusted repositories:
   `search(query="python", page=1, page_size=5)`
2. Inspect available tags and multi-arch platform support:
   `listRepositoryTags(namespace="library", repository="python", page=1, page_size=10)`
3. Check the exact immutable tag before writing `FROM` statements:
   `checkRepositoryTag(namespace="library", repository="python", tag="3.12-slim-bookworm")`

### 2. Production Security Hardening via Docker Hardened Images
When designing high-assurance production deployments:
1. Query available hardened images:
   `dockerHardenedImages(query="nginx")`
2. Retrieve image security attestations and minimal base layer specifications.
3. Compare against standard community images to select the lowest CVE footprint.

### 3. CI/CD Release Preflight Verification
Before triggering automated builds or publishing artifacts:
1. Verify namespace access and target repository status:
   `checkRepository(namespace="myorg", repository="core-service")`
2. If absent and automated provisioning is permitted, initialize the repository:
   `createRepository(namespace="myorg", repository="core-service", is_private=true, description="Production service image")`

## Security Invariants

- Never print Personal Access Tokens into session artifacts, commit history, or logs.
- Enforce least-privilege scoping: issue PATs with Read-only access for auditing and discovery agents, reserving Read/Write/Admin access strictly for verified deployment agents.
- Always verify image digest hashes and supported architectures (`linux/amd64`, `linux/arm64`) before proposing deployment configs.
