# ANCHOR ⚓

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
[![npm version](https://img.shields.io/npm/v/anchor-agent.svg)](https://www.npmjs.com/package/anchor-agent)
[![CI](https://github.com/krishujeniya/Anchor/actions/workflows/anchor-verify.yml/badge.svg)](https://github.com/krishujeniya/Anchor/actions/workflows/anchor-verify.yml)
[![Nightly Chaos](https://github.com/krishujeniya/Anchor/actions/workflows/anchor-nightly-chaos.yml/badge.svg)](https://github.com/krishujeniya/Anchor/actions/workflows/anchor-nightly-chaos.yml)

**100% planning precision on a 50k-LOC codebase. Automated test suite & evaluation harness. 0 verify failures. Measured, not claimed.**

![ANCHOR Preview](social_preview.png)

ANCHOR is a production-grade agentic development spine for agent-first IDEs (Antigravity, Cursor, Claude Code). It acts as the "weight" that keeps AI autonomy grounded in verifiable state and computed gates.

## Quick Install

Scaffold ANCHOR into any existing repository in under 60 seconds:

```bash
npx anchor-agent init
```

This installs the framework into `.agents/`, generates IDE bridges (`.cursor/rules` and `.claude.json`), and sets up git hooks. Zero third-party host dependencies required (pure bash/jq).

## Why ANCHOR?

AI coding agents often drift, rubber-stamp their own work, or get lost in long-running tasks. ANCHOR's moat is **enforced, measured discipline**:

1. **Enforced gates with computed verdicts** — Pre-commit hooks guarantee that code isn't merged until deterministic checks pass.
2. **Durable state machine + audit trail** — `state.json` survives context resets, with append-only iteration logs.
3. **Automated rollback** — Rescue branches and drift detection catch bad agent decisions instantly.
4. **Chaos Trials methodology** — A formal, falsifiable validation method proving resilience.
5. **Maker/checker separation** — No agent grades its own work.

## Comparison

| Feature | ANCHOR | Spec Kit | Claude Code Hooks | Cursor Rules | Kiro |
|---|---|---|---|---|---|
| **Enforcement** | **Strict (Git Hooks & Assertions)** | Advisory (Slash Commands) | Native Hooks | Advisory Prompting | Full IDE |
| **State** | **Durable JSON/Markdown** | Conversational | Session-based | Ephemeral | Database |
| **Portability** | **Universal (Bash spine)** | GitHub-native | Anthropic-only | Cursor-only | AWS-only |
| **Best For** | **Zero-defect engineering & Trust** | Rapid greenfield planning | Ad-hoc scripting | Quick guardrails | Enterprise IDE |

*Read our [Detailed Comparison](COMPARISON.md) and [Spec Kit Interop Guide](SPEC_KIT_INTEROP.md).*

## The 5-Gate Workflow

ANCHOR routes every multi-step development task through a strict pipeline:
1. **UNDERSTAND**: Explores intent and gathers requirements. (Outputs an artifact, requires human approval).
2. **ANALYZE**: Evaluates feasibility, risk, and scope. (Requires human approval).
3. **PLAN**: Builds architecture and the implementation plan. (Requires human approval).
4. **IMPLEMENT**: Writes code and tests autonomously. No human in the loop.
5. **VERIFY**: Proves the work is correct via deterministic checks (tests, linting) and a human Quiz-Me gate.

## IDE Adapters

ANCHOR is tool-agnostic and maps directly to native features in major agent-first IDEs:

| Feature | Google Antigravity | Claude Code | Cursor |
|---------|---------------------|-------------|--------|
| **Task List** | Native Artifact | `PLAN.md` file | `TODO.md` file |
| **Plan Artifact** | Native Artifact | `DESIGN.md` file | `DESIGN.md` file |
| **Browser Check** | Native browser subagent | N/A (Manual only) | N/A (Manual only) |
| **Walkthrough** | Native Artifact | `README.md` diff | Chat summary |

## Chaos Trials & Evidence

ANCHOR is validated via adversarial **Chaos Trials**. Our [CT-002 (Papermill)](CHAOS_TRIALS.md) benchmark demonstrated 100% planning precision across automated trials with zero unhandled failures. Nightly cron jobs actively sabotage the framework to ensure automatic recovery works every time.

## Architecture

ANCHOR lives entirely inside the `.agents/` folder of your project:
- `AGENTS.md` - The strict constitutional rules.
- `.agents/state/` - Where the active JSON and Markdown state lives.
- `.agents/skills/` - The isolated, targeted skills that enforce the gates.
- `bin/` - Pure bash executables (eval, init, verify, rollback, gate-check).

## GitHub Action

Enforce ANCHOR gates in your CI:
```yaml
uses: krishujeniya/Anchor@main
```

## Contributing

See our [Contributing Guide](../CONTRIBUTING.md) and [Code of Conduct](../CODE_OF_CONDUCT.md).

## License
MIT
