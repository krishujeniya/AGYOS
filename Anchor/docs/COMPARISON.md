# Agent Governance Comparison

The ecosystem for guiding and restraining AI coding agents has exploded. Here is an honest, technical comparison of the major tools, and when you should use each.

## The Contenders

1. **ANCHOR**: A lightweight, zero-dependency bash spine that enforces a 5-gate workflow, maintains durable JSON state, and uses git hooks to block unverified commits.
2. **GitHub Spec Kit**: A CLI tool that structures conversational planning into `/specify`, `/plan`, and `/tasks` commands.
3. **Claude Code Hooks**: Native pre/post-tool execution scripts built into Anthropic's CLI.
4. **Cursor Rules**: Glob-scoped markdown files (`.cursor/rules/`) that append context to the agent's prompt.
5. **AWS Kiro**: A full, heavy-weight agentic IDE with built-in requirements modeling and enterprise SSO.

---

## Feature Matrix

| Feature | ANCHOR | Spec Kit | Claude Hooks | Cursor Rules | AWS Kiro |
|---|---|---|---|---|---|
| **Enforced Verification** | ✅ (Git Hooks & Bash) | ❌ (Advisory) | ✅ (Native) | ❌ (Prompting) | ✅ (IDE Native) |
| **Durable State** | ✅ (JSON/Markdown) | ❌ (Conversational) | ❌ (Session) | ❌ (Ephemeral) | ✅ (Database) |
| **Rollback & Recovery** | ✅ (Rescue Branches) | ❌ | ❌ | ❌ | ✅ |
| **Maker/Checker Split** | ✅ (Strict) | ❌ | ❌ | ❌ | ✅ |
| **Portability** | ✅ (Universal CLI) | ✅ (GitHub native) | ❌ (Claude only) | ❌ (Cursor only)| ❌ (AWS only) |
| **Installation** | 60s (`npx`) | 60s (`uvx`) | Built-in | Built-in | Account required |

## When to use which?

### Use Cursor Rules when...
You just need lightweight guardrails (e.g., "Always use `React.FC`", "Don't use `var`"). Rules are great for stylistic alignment but cannot stop a hallucinating agent from committing broken code.

### Use Claude Code Hooks when...
You are building custom, highly-specific workflows that only need to run in Claude Code and you want to write them in TypeScript/Bash.

### Use GitHub Spec Kit when...
You are doing rapid, greenfield development and want the best UX for converting a conversational idea into a markdown specification.

### Use ANCHOR when...
You are working on a mature, production-grade codebase where **defect prevention** is more important than speed. ANCHOR is for teams that need absolute proof (via tests and linters) that the agent didn't hallucinate a fix. (Note: ANCHOR [pairs perfectly with Spec Kit](SPEC_KIT_INTEROP.md)).

### Use AWS Kiro when...
You are a massive enterprise that requires full IDE-level control, SSO integrations, and you don't mind locking your engineering org into a specific vendor's ecosystem.
