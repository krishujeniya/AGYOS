# Hosted agents with Azure AI Projects (Python)

This guide covers container-based agents hosted by Microsoft Foundry Agent Service. API names and requirements change; check the current [Foundry deployment guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent) and [Azure AI Projects Python reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme) before applying it.

## 1. Confirm the project contract

Before editing code, establish:

- Python version and the locked `azure-ai-projects` / `azure-identity` versions.
- Foundry project endpoint and model deployment, without printing credentials.
- Container image, registry, deployment protocol, and expected endpoint behavior.
- Whether the task is local development, image build, resource provisioning, or cloud deployment.

Current Microsoft quickstarts document Python SDK deployment with `azure-ai-projects` 2.3.0 or later; the library reference is versioned and newer releases may change supported fields. Keep the project's lockfile authoritative unless an upgrade was requested.

## 2. Model a container-based definition

Current SDK examples use `HostedAgentDefinition` with `ContainerConfiguration` for an image-based deployment. The definition also carries CPU, memory, environment variables, and protocol versions. Do not copy older preview examples using `ImageBasedHostedAgentDefinition` without checking the installed SDK.

```python
from azure.ai.projects.models import (
    ContainerConfiguration,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)

definition = HostedAgentDefinition(
    cpu="1",
    memory="2Gi",
    container_configuration=ContainerConfiguration(
        image="<registry>/<image>:<immutable-tag>"
    ),
    environment_variables={"PYTHONNOUSERSITE": "1"},
    protocol_versions=[ProtocolVersionRecord(protocol="responses", version="2.0.0")],
)
```

Treat the example as a shape to compare with the installed SDK, not a copy-paste deployment. Supply the required project-specific identity, image, protocol, model, and resource settings from verified configuration. Keep secrets out of source files and logs.

## 3. Validate locally

1. Build using the repository's existing container workflow and dependency lockfile.
2. Check that the image architecture matches the hosting requirements documented for the selected deployment path.
3. Start the agent with the documented local host and send a non-sensitive test request to the expected protocol endpoint.
4. Check successful, invalid, and incomplete responses. Record the actual output; do not infer cloud readiness from a local response.

## 4. Deploy only with explicit authorization

Image pushes, Azure provisioning, and hosted-agent deployments change external resources and may incur cost. Confirm the target subscription, project, registry, image tag, identity, expected charges, and rollback plan before performing them. Prefer immutable image tags. Review the resource and file diff before applying changes.

After an authorized deployment, verify the created agent version, endpoint, protocol, and a test invocation. Report the exact resource changes and checks performed. If no cloud deployment was run, say so.

## Compatibility ID

The older `agents-v2-py` ID remains as a compatibility pointer to this canonical hosted-agent runbook.
