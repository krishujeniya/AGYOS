---
name: cloud-sandbox-execution
description: "SOP for executing Gate 4 tasks safely using ephemeral, containerized sandboxes (Docker/Cloud VMs)."
category: devops
version: "1.0.0"
author: "Krish Ujeniya"
prompt-source: prompt.toon
---
skill: "cloud-sandbox-execution"
sections[6]:
  - "\n"
  - "# Cloud Sandbox Execution\n\n> **Author**: Krish Ujeniya\n> \n> This skill defines the mandatory protocol for isolating autonomous code execution during Gate 4. \n> To prevent host system contamination, all agent-driven execution (compilation, testing, package installation) MUST occur within a disposable sandbox.\n\n"
  - "## 1. Sandbox Initialization\n- **Action**: Spin up an ephemeral Docker container mimicking the production target environment.\n- **Base Image**: Select an appropriate minimal base (e.g., `node:20-alpine`, `python:3.11-slim`, `golang:1.21`).\n- **Command Example**: `docker run -it -d --name aegis-sandbox-$(date +%s) <image>`\n\n"
  - "## 2. Secure Worktree Mounting\n- **Action**: Mount the active Git worktree as a volume into the sandbox.\n- **Restriction**: The mount MUST be restricted to the project root. Never mount `/home`, `/`, or sensitive directories like `~/.ssh`.\n\n"
  - "## 3. Sandbox Execution Protocol\nWhen performing Gate 4 actions, the agent must route commands through the sandbox:\n- **Testing**: `docker exec aegis-sandbox <test-command>`\n- **Compilation**: `docker exec aegis-sandbox <build-command>`\n- **Dependencies**: `docker exec aegis-sandbox <install-command>`\n\n"
  - "## 4. Teardown and Cleanup\n- **Action**: Upon task completion or session end, the sandbox MUST be forcefully destroyed.\n- **Command**: `docker rm -f aegis-sandbox-xyz`\n- **Verification**: Ensure no dangling containers or orphaned volumes remain.\n"
