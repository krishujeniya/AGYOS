---
name: hosted-agents-v2-py
description: "Create container-based Microsoft Foundry hosted agents with the Azure AI Projects Python SDK. Use when configuring or deploying hosted agents; verify the installed SDK version and current documentation."
risk: unknown
source: community
date_added: "2026-02-27"
---
# Azure AI Hosted Agents (Python)

Create container-based hosted agents in Microsoft Foundry with the Azure AI Projects Python SDK. Use when defining, testing, or deploying an agent image; use current SDK references because the API has changed since early v2 previews.

## Workflow

1. Read [the hosted-agent runbook](references/FULL_RUNBOOK.md) and the project's existing dependency lockfile.
2. Confirm Python and Azure SDK versions, project endpoint, container registry, deployment protocol, and test/deploy scope.
3. Check the current Microsoft Foundry documentation before changing SDK calls or resource configuration.
4. Obtain explicit authorization before installing packages, pushing an image, provisioning resources, deploying, or incurring cloud cost.
5. Verify the image, protocol, identity, environment configuration, and local tests; report exact checks and any cloud behavior not exercised.
