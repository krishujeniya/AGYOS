# Pinned Source Registry

The machine-readable registry is `integrations/registry/sources.json`. Each of the eight entries records the exact repository, pinned commit SHA, license caveat, high-level disposition, AGYOS pod, existing native skill, route patterns, evidence paths, and limitations.

| ID | Source repository | Primary native skill | Active implementation |
| --- | --- | --- | --- |
| agent-architecture-intelligence | [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | `agent-harness-design` | Research reference and AGYOS architecture comparison only |
| agentic-awesome-skills | [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | `agyos-decision` | Native catalog retained; upstream catalog reference only |
| founders-kit | [avinash201199/founders-kit](https://github.com/avinash201199/founders-kit) | `agyos-founder-guide` | Native startup guidance |
| ai-career-planner | [ayush488-glitch/ai-career-planner-skill](https://github.com/ayush488-glitch/ai-career-planner-skill) | `interview-coach` | Existing coaching + planning methodology |
| ai-engineering-os | [ayush488-glitch/ai-engineering-os](https://github.com/ayush488-glitch/ai-engineering-os) | `ml-engineer` | Existing ML runbook + F1 stages |
| gstack | [garrytan/gstack](https://github.com/garrytan/gstack) | `code-reviewer` | Existing review runbook + verification discipline |
| agent-reach | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | `research-ops` | Optional, restricted Python adapter |
| microsoft-edge-ai | [microsoft/edge-ai](https://github.com/microsoft/edge-ai) | `ml-engineer` | Deployment architecture guidance only |

## License and security constraints

- The **system-prompts** archive uses a GPL-3.0 repository license; its third-party prompt dumps may have other restrictions or disputed provenance. We copy none into executable files.
- **AAS** has an MIT code license and CC BY 4.0 content license, with additional source-level attribution and exceptions. Installing a skill is a separate per-file review decision.
- **Founders Kit**, **career planner**, **gstack**, **Agent Reach**, and **microsoft/edge-ai** have MIT repository licenses as inspected. External links, trademarks, browser credentials and third-party dependencies have their own terms.
- **AI Engineering OS** had no root `LICENSE` at the inspected commit. The AGYOS code is independently written and references architecture concepts without copying its skill text.
- Every registry entry remains an untrusted source. Its metadata and text never override AGYOS policy, authorize tool calls, or grant new risk allowances.

The SHA values in `sources.json` are inspection pins, **not** proof that upstream downloads, release archives or dependencies were installed. No continuous upstream updater is enabled.
