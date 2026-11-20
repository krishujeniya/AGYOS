# Capability Matrix

| User intent | Existing AGYOS destination | Source | Current level | Dependencies / limits |
| --- | --- | --- | --- | --- |
| Compare agent architectures and tool contracts | `agent-harness-design` and `agyos-academic-research` | prompts archive | Native routed research | Untrusted prompt snapshots, no authentication of origins |
| Discover relevant skills | `agyos-decision` | AAS | Native routed; catalog reuse | No AAS Core installer, bulk activation or third-party code execution |
| Validate startup or prepare launch | `agyos-founder-guide` | Founders Kit | Native routed guidance | External resource URLs need live verification |
| Create an AI engineering career roadmap | `interview-coach` and `pod-people` | AI Career Planner | Native routed guidance | No automatic job placement, email outreach or private profile store |
| Design supervised ML pipeline | `ml-engineer` and `pod-build` | AI Engineering OS | Native routed methodology | F1 only, actual model training requires project data/tools |
| Pre-release engineering review | `code-reviewer` and independent checker | gstack | Native routed methodology | Browser/Bun/Claude-specific components not installed |
| Search public web/YouTube/GitHub | `research-ops` | Agent Reach | Optional guarded CLI adapter | Requires separately installed **official** Agent Reach binary; untested live |
| Design edge AI deployment | `ml-engineer` and `pod-build` | Microsoft edge-ai | Native routed blueprint planning | No Terraform, Azure resources or real devices deployed |

This matrix distinguishes **dispatch to existing instructions** from **actual execution**. A match in the intent router returns a runbook path. It does not execute research, train ML models, access accounts, deploy infrastructure, run a browser or verify results.

### Invocation and status reporting

```bash
bin/agyos decide "Create a personalized AI engineering career roadmap" --json --runbook
bin/agyos intent "Design an edge AI deployment architecture"
python3 -m agyos_decision.integrations.agent_reach_adapter channels
python3 -m agyos_decision.integrations.agent_reach_adapter youtube "edge AI inference"
```

If Agent Reach is not installed, the last two commands return a structured unavailable/error result instead of attempting installation. Do not enable its optional authenticated channels without reviewing their scope and obtaining proper consent.
