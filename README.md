<p align="center">
  <img src="assets/agyos-logo.svg" alt="AGYOS" width="180" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Agent workflow tools, skill catalog, and local runtime</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" alt="Apache 2.0 license" /></a>
  <a href="https://github.com/krishujeniya/AGYOS/actions/workflows/ci.yml"><img src="https://github.com/krishujeniya/AGYOS/actions/workflows/ci.yml/badge.svg" alt="GitHub Actions CI" /></a>
  <a href="https://krishujeniya.github.io/AGYOS/"><img src="https://img.shields.io/badge/Docs-GitHub_Pages-blue.svg" alt="Documentation site" /></a>
</p>

AGYOS is a Python-centered repository for discovering agent runbooks and coordinating work through a command-line interface, workflow rules, state tracking, and optional MCP integrations. The main host target listed in [`AGENTS.md`](AGENTS.md) is the Antigravity CLI (`agy`).

Skill runbooks live under `.agents/skills/`. Generated manifests and the published search index are maintained separately; a runbook may not appear in search until the generated files are synchronized through CI.

AGYOS returns instructions and exposes workflow utilities. A selected skill is not proof that an agent followed it, that a host enforces every rule, or that an external action is authorized. Check the actual host tools, permissions, and verification evidence for each task.

## Get started

Clone the repository and inspect the CLI:

```bash
git clone https://github.com/krishujeniya/AGYOS.git
cd AGYOS
bin/agyos help
```

Find and read a runbook:

```bash
bin/agyos decide "fix a Python error" --json --runbook
bin/agyos find "database schema migration"
bin/agyos skill technical-documentation-writer
```

`decide` ranks candidate skills and can return the selected runbook. Matching scores are heuristics, not calibrated probabilities. Read the runbook and its linked references before applying it; respect the task scope, user instructions, and host permissions.

`bin/agyos intent "<task>"` compiles a prompt into a task contract and clarification decision. It does not implement the task or perform external actions. Commands such as `gate`, `fast`, `init`, `rollback`, and `verify` can change state, configure a host, or execute checks; review their behavior before use.

## How the system is organized

```text
Task description
      │
      ├── CLI or MCP entry point
      │       └── skill discovery and task-contract utilities
      │
      ├── applicable runbook, rules, and host permissions
      │       └── scoped implementation or operator workflow
      │
      └── repository changes
              └── GitHub Actions verification
```

For multi-step engineering work, the governance model uses five gates:

| Gate | Purpose |
| --- | --- |
| Understand | Record the objective, deliverables, and acceptance criteria. |
| Analyze | Inspect the code, dependencies, scope, and risks. |
| Plan | Set the implementation boundary and verification approach. |
| Implement | Make the smallest complete change while preserving project invariants. |
| Verify | Review evidence from the required GitHub Actions workflows. |

The repository instructions require human approval at defined gate boundaries. Complexity scores guide the fast path, but do not override risk, scope, or approval requirements. See [`AGENTS.md`](AGENTS.md) for the operating contract.

## Main components

| Path | Contents |
| --- | --- |
| `.agents/skills/` | Skill runbooks, references, and examples. Some entries are adapters to pinned upstream sources. |
| `.agents/rules/` | Shared and language-specific engineering and operating rules. |
| `.agents/agents/`, `.agents/workflows/`, `.agents/plugins/` | Agent definitions, workflow descriptions, and host plugin configuration. |
| `agyos_decision/` | Skill catalog loading, intent routing, task contracts, and state-ledger code. |
| `bin/agyos`, `bin/state.sh` | CLI entry point and gate/state operations. |
| `scripts/agyos-runtime/`, `scripts/hooks/` | Runtime lifecycle code, host hooks, and stateful integrations. Hook effectiveness depends on host registration and behavior. |
| `scripts/council/` | Optional multi-agent deliberation CLI and tests. |
| `mcp/` | Local stdio MCP state server and optional service launchers. |
| `integrations/` | Optional adapters; external services may require separate installation, credentials, and authorization. |
| `tools/video/` | Bundled video-editing and faceless-shorts toolkits with their own setup and license notes. |
| `docs/`, `.github/workflows/` | Project references, generated documentation, and CI workflows. |

### Five operating pods

AGYOS includes five pod definitions and corresponding SOP runbooks. They organize task guidance; they do not imply that an external service or specialist agent is running.

| Pod | Focus |
| --- | --- |
| `pod-build` | Engineering, architecture, QA, and operations |
| `pod-customer` | Support, onboarding, and customer success |
| `pod-growth` | Marketing, growth, sales, and outreach drafts |
| `pod-gna` | Finance, legal, compliance, and executive operations |
| `pod-people` | Recruiting, HR, and team operations |

## Command reference

| Command | Use |
| --- | --- |
| `bin/agyos help` | Show available CLI commands. |
| `bin/agyos decide "<task>" --json --runbook` | Rank skills and optionally return a runbook. |
| `bin/agyos find "<query>"` | Search the local skill catalog. |
| `bin/agyos skill <id>` | Print a skill's `SKILL.md`. |
| `bin/agyos intent "<task>"` | Produce a task contract and clarification decision. |
| `bin/agyos state` | Read the current workflow state. |
| `bin/agyos gate <name>` | Request a state transition; this changes workspace state. |

The CLI also has setup, verification, security, model-routing, and Council commands. Use `bin/agyos help` and inspect the relevant implementation before relying on a command's side effects.

## MCP and integrations

`mcp/state-server.cjs` is the local stdio MCP entry point for AGYOS state and skill-discovery tools. Register it with a compatible host using that host's documented MCP configuration. The service-specific launchers in `mcp/` and `integrations/` have separate runtime, authentication, and permission requirements; their presence does not mean they are installed or connected.

The intent router, MCP server, and host hooks are distinct entry points. A runbook returned by one entry point is not evidence that another component enforced it. Host compatibility and actual tool mediation must be checked on the target host.

## Security and data boundaries

- Treat imported skills and external references as instructions to review, not code to execute automatically. Preserve each source's license and attribution; inspect the pinned source before updating an adapter.
- Hook scripts provide checks, but complete enforcement depends on the host registering and honoring them. AGYOS is not a general-purpose sandbox for arbitrary agent code.
- Optional encrypted-envelope support protects files exchanged between separately keyed endpoints. It does not encrypt all AGYOS state, model-provider requests, or external tool traffic, and it has not received an independent cryptographic audit.
- The Apache-2.0 [`LICENSE`](LICENSE) applies to project files covered by that license. Imported toolkits, upstream skills, PDFs, and other third-party materials may have separate rights and notices. See the provenance references before redistribution.
- Do not place credentials, private keys, or sensitive customer data in the repository, prompts, logs, or untrusted tools. Follow [`SECURITY.md`](SECURITY.md) and the relevant security design documents.

## CI and verification

This repository's policy is to run tests, builds, linters, type checks, dependency resolution, toolkit setup, and media renders in GitHub Actions only. Local work is limited to source inspection and `git diff --check`; do not run those checks or setup commands on the workstation.

The workflows are configured as follows:

- [`ci.yml`](.github/workflows/ci.yml) runs on pushes and pull requests targeting `main`. It checks shell and Python syntax, runs Python and Node regression suites, runs the Council suite with Bun, generates catalog files, uploads the `agyos-skill-catalog-generated` artifact, and checks generated-file parity.
- [`video-toolkits.yml`](.github/workflows/video-toolkits.yml) runs for video-toolkit changes and by manual dispatch. It checks the bundled packages and performs six faceless-render smoke cases without downloading speech models.

When catalog source changes, review and sync the generated artifact from the matching Actions run before treating the catalog parity gate as passing. Report verification against the exact commit SHA; a workflow badge or a returned runbook alone is not proof that the current changes passed.

## Documentation map

| Topic | Reference |
| --- | --- |
| Repository rules and approval boundaries | [`AGENTS.md`](AGENTS.md) |
| Skill routing behavior, fallbacks, and limits | [`docs/SKILL_ROUTING.md`](docs/SKILL_ROUTING.md) |
| Architecture model and component notes | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| State-machine repair inventory | [`docs/STATE_MACHINE_REPAIR.md`](docs/STATE_MACHINE_REPAIR.md) |
| Security risks and residual limits | [`docs/security/THREAT_MODEL.md`](docs/security/THREAT_MODEL.md), [`docs/security/END_TO_END_ENCRYPTION.md`](docs/security/END_TO_END_ENCRYPTION.md) |
| Optional integrations and capability boundaries | [`docs/integrations/CAPABILITY_MATRIX.md`](docs/integrations/CAPABILITY_MATRIX.md) |
| Upstream skill sources and notices | [`docs/references/upstream-skills/README.md`](docs/references/upstream-skills/README.md) |
| Supplied industry PDFs and provenance | [`docs/references/industry/README.md`](docs/references/industry/README.md) |
| Video toolkits and prompt provenance | [`tools/video/README.md`](tools/video/README.md), [`docs/references/video/README.md`](docs/references/video/README.md) |
| Research, decisions, and optimization records | [`docs/research/`](docs/research/), [`docs/adr/`](docs/adr/), [`docs/OPTIMIZATION_RESULTS.md`](docs/OPTIMIZATION_RESULTS.md) |
| MCP server entry points | [`mcp/README.md`](mcp/README.md) |
| Current task handoff and verification status | [`AI_HANDOFF.md`](AI_HANDOFF.md) |

The project website is published at [krishujeniya.github.io/AGYOS](https://krishujeniya.github.io/AGYOS/). Generated pages and catalog data can differ from source until the CI catalog artifact has been synchronized.

## License and citation

Project-level licensing is described in [`LICENSE`](LICENSE); third-party files retain their own licenses and notices. For research citation metadata, see [`CITATION.cff`](CITATION.cff). For security issues, use the private reporting channel described in [`SECURITY.md`](SECURITY.md).
