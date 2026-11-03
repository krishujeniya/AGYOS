---
name: cloud-sandbox-execution
description: "SOP for executing Gate 4 tasks safely using ephemeral, containerized sandboxes (Docker/Cloud VMs)."
category: devops
version: "1.0.0"
author: "Krish Ujeniya"
---

# Cloud Sandbox Execution

> **Author**: Krish Ujeniya
> 
> This skill defines the mandatory protocol for isolating autonomous code execution during Gate 4. 
> To prevent host system contamination, all agent-driven execution (compilation, testing, package installation) MUST occur within a disposable sandbox.

## 1. Sandbox Initialization
- **Action**: Spin up an ephemeral Docker container mimicking the production target environment.
- **Base Image**: Select an appropriate minimal base (e.g., `node:20-alpine`, `python:3.11-slim`, `golang:1.21`).
- **Command Example**: `docker run -it -d --name aegis-sandbox-$(date +%s) <image>`

## 2. Secure Worktree Mounting
- **Action**: Mount the active Git worktree as a volume into the sandbox.
- **Restriction**: The mount MUST be restricted to the project root. Never mount `/home`, `/`, or sensitive directories like `~/.ssh`.

## 3. Sandbox Execution Protocol
When performing Gate 4 actions, the agent must route commands through the sandbox:
- **Testing**: `docker exec aegis-sandbox <test-command>`
- **Compilation**: `docker exec aegis-sandbox <build-command>`
- **Dependencies**: `docker exec aegis-sandbox <install-command>`

## 4. Teardown and Cleanup
- **Action**: Upon task completion or session end, the sandbox MUST be forcefully destroyed.
- **Command**: `docker rm -f aegis-sandbox-xyz`
- **Verification**: Ensure no dangling containers or orphaned volumes remain.
