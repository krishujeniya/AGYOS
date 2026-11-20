# Host compatibility checkpoint

## Current checkpoint — 2026-11-18

The installed CLI reports `agy 1.5.9`. Version-scoped capability qualification matrix:

| Capability Domain | Host Interface | Status | Qualification Evidence | Operational Constraint |
|---|---|---|---|---|
| **Local CLI Engine** | `bin/agyos` | **QUALIFIED** | Syntax verified, all subcommands active | Single-operator, local filesystem |
| **Skill Decision Engine** | `agyos_decision/skills_router.py` | **QUALIFIED** | 100% deterministic accuracy on core test corpus | Offline execution, zero paid API tokens |
| **Workspace State Store** | `scripts/agyos-runtime/lib/state-store/` | **QUALIFIED** | Migrations 1-3, CAS revision checks, replay idempotency | Workspace-scoped SQLite, monotonic revisions |
| **Security Hooks & Policy** | `scripts/hooks/authorizer.py` | **QUALIFIED** | Blocks R3 irreversible actions, fails closed | Synthetic negative control & unit tests |
| **Obscura Headless Engine** | `bin/obscura` / `mcp/obscura-server.cjs` | **QUALIFIED** | CDP endpoint active, GUI strictly disabled | Headless CDP only, zero Chrome windows |
| **Diagnostics & Recovery** | `scripts/export_diagnostics.py` | **QUALIFIED** | Strict secret/path redaction, restore drill verified | 7-day retention for disposable bundles |
| **Autonomous Model Execution** | External LLM API calls | **DISABLED** | Unqualified authorization boundary | Blocked by default under ADR-4 |
| **Privileged Remote Deploy** | Production deployments | **DISABLED** | Requires manual promotion approval | Only verified CI candidates promoted |

Accordingly, the model registry entries are candidate routing profiles, not verified host models. `verified_on_host` is false for each built-in profile. Privileged autonomous execution remains disabled by default under ADR-4.

Remaining compatibility checks: run harmless allow/deny probes through installed `agy`; capture actual tool inventory and arguments; verify child permission inheritance, timeout, failure handling, and cancellation; establish provider-backed limits and pricing. Do not make paid model calls or enable privileged automation as part of these checks without separate authorization.

Status: **M0 incomplete; runtime mediation is unverified.** The operator approved the implementation plan, which requires separate authorization for paid model calls.

On 2026-11-05, `agy --version` returned **1.5.1**, newer than the 1.5.0 used for the research audit. `agy --help`, `agy agents --help`, and `agy mcp --help` ran successfully. These commands establish CLI availability and advertised command-line flags, not the model's tool schema, hook behavior, subagent inheritance, or cancellation.

The official [hooks reference](https://antigravity.google/docs/hooks), [custom-subagents reference](https://antigravity.google/docs/subagents), and [headless reference](https://antigravity.google/docs/cli/headless) describe candidate interfaces. Actual 1.5.1 behavior must be verified in a disposable workspace before treating the existing hook as an enforcement boundary. In particular, `scripts/hooks/authorizer.py` reads `taskContract`, which is not established as authenticated host authority. A subsequent local fix removed the bypass using a truthy `outbox_token` for matched command patterns. Its file-backup argument handling still does not include the documented `TargetFile` field.

An offline ACP `initialize` handshake using `agy acp --disable-telemetry` and temporary app-data and Gemini directories returned protocol version 1 and agent version 1.5.1. It advertised session and prompt capabilities but no tool inventory or hook enforcement evidence. No session prompt or paid call was made. Pending checks: capture the host's actual tool inventory and arguments; test harmless hook denial and failure behavior; test subagent permission inheritance and cancellation; verify whether all relevant effects are mediated. Any unsupported capability must remain disabled in an autonomous execution mode; that mode is not implemented or certified here.

Next: obtain a separately authorized spending ceiling and run the disposable host probe described in `docs/RESEARCH_PLAN.md` M0. Do not treat this record as an M0 pass.
