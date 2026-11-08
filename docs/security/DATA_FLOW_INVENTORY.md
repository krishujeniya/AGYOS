# AGYOS Data Flow Inventory

**Version:** 1.0
**Date:** 2026-11-08
**Baseline commit:** `35903ad`

## 1. Data Flow Classification

| Protection Level | Definition |
|-----------------|------------|
| `encrypted_at_rest` | AES-256-GCM with passphrase-derived key, mode 0600 |
| `encrypted_transport` | TLS 1.2+ to provider endpoints |
| `encrypted_e2e` | X25519+AES-256-GCM envelope between keyed endpoints |
| `plaintext_local` | Unencrypted files with filesystem permissions only |
| `provider_visible` | Data necessarily visible to cloud inference provider |
| `git_tracked` | Committed to repository history (public or private) |

## 2. Data Flow Matrix

### 2.1 Agent State & Memory

| Data Flow | Source | Destination | Classification | Protection | Notes |
|-----------|--------|-------------|----------------|------------|-------|
| Gate/milestone state | CLI/MCP | `.agents/state/state.json` | Internal | `plaintext_local` + `git_tracked` | No secrets; operational metadata |
| Memory tier0/1/2 (legacy) | MCP `agyos_memory` | `.agents/state/memory.json` | Confidential | `plaintext_local` + `git_tracked` | **Risk**: may contain user context |
| Memory (private vault) | MCP `agyos_memory` | `~/.local/state/agyos/private-memory.vault.json` | Confidential | `encrypted_at_rest` | scrypt+AES-256-GCM, mode 0600 |
| Decision receipts | Decision engine | `.agents/state/decisions/rcpt_*.json` | Internal | `plaintext_local` + `git_tracked` | Task classification metadata |
| Context graph | MCP | `.agents/state/context-graph.json` | Internal | `plaintext_local` + `git_tracked` | Dependency index |
| Checkpoints | State engine | `.agents/state/checkpoints/` | Internal | `plaintext_local` | Milestone history |
| CURRENT.md | Session state | `.agents/state/CURRENT.md` | Internal | `plaintext_local` | Human-readable summary |

### 2.2 Encryption & Identity

| Data Flow | Source | Destination | Classification | Protection | Notes |
|-----------|--------|-------------|----------------|------------|-------|
| E2EE identity (private) | `bin/agyos secure keygen` | `~/.config/agyos/identity.json` | Secret | `encrypted_at_rest` (scrypt+AES-256-GCM), mode 0600 | Never committed |
| E2EE identity (public) | `bin/agyos secure public` | User-specified export | Public | N/A | Fingerprint verification required |
| E2EE envelope | `bin/agyos secure encrypt` | User-specified output | Confidential | `encrypted_e2e` | X25519+HKDF+AES-256-GCM+Ed25519 |
| Vault passphrase | User terminal | File descriptor 3-9 | Secret | In-process only | Never in shell history or args |

### 2.3 External Communications

| Data Flow | Source | Destination | Classification | Protection | Notes |
|-----------|--------|-------------|----------------|------------|-------|
| Model inference prompts | CLI/MCP | Gemini/Claude API | Confidential | `encrypted_transport` + `provider_visible` | **Provider sees plaintext**; inherent to inference |
| Model responses | Gemini/Claude API | CLI/MCP | Varies | `encrypted_transport` + `provider_visible` | Content depends on prompt |
| Git push/fetch | Local repo | GitHub | Public/Internal | `encrypted_transport` | HTTPS; repo visibility controls access |
| Skill discovery | Decision engine | Local catalog | Public | `plaintext_local` | No network; local file search |
| AGY CLI telemetry | AGY host | Unknown | Unknown | `unknown` | Host-dependent; needs investigation |

### 2.4 MCP Protocol

| Data Flow | Source | Destination | Classification | Protection | Notes |
|-----------|--------|-------------|----------------|------------|-------|
| JSON-RPC requests | AGY host | `mcp/state-server.cjs` via stdio | Internal | Process isolation | Bounded input (1MB), 15s timeout |
| JSON-RPC responses | MCP server | AGY host | Internal | Process isolation | Errors redacted; no stack traces |
| Subprocess calls | MCP `agyos_decision` | `scripts/agyos-decision.py` | Internal | Subprocess isolation | Input/output bounded |

### 2.5 Hook System

| Data Flow | Source | Destination | Classification | Protection | Notes |
|-----------|--------|-------------|----------------|------------|-------|
| PreToolUse events | AGY host | `scripts/hooks/authorizer.py` | Internal | Process isolation | Fail-closed on error/malformed input |
| Pre-write snapshots | Authorizer | `.agents/state/snapshots/` | Internal | `plaintext_local` | Bounded size (16MB), private permissions |
| OS hook events | AGY host | `scripts/hooks/agy_os_hook.py` | Internal | Process isolation | Rejects malformed/oversized events |

## 3. Unprotected Data Paths (Action Required)

| Path | Risk | Recommended Action | Priority |
|------|------|-------------------|----------|
| `.agents/state/memory.json` | May contain user context in plaintext Git | Migrate to encrypted vault; disable plaintext writes | P1 |
| `.agents/state/state.json` | Operational metadata; low sensitivity | Accept risk or add integrity signing | P2 |
| `.agents/state/decisions/` | Task metadata; could contain prompt fragments | Sanitize content; consider encryption | P2 |
| `.agents/state/checkpoints/` | Historical milestone data | Review for sensitive content | P2 |
| AGY CLI telemetry channel | Unknown data sent to host | Investigate and document; disable if possible | P1 |

## 4. Provider Trust Summary

| Provider | What They See | Mitigation |
|----------|--------------|------------|
| Google (Gemini) | All prompts, tool schemas, responses in cleartext | Data classification; consent gating; local inference for secrets |
| Anthropic (Claude) | All prompts, tool schemas, responses in cleartext | Same as above |
| GitHub | Repository contents (public); Git operations | Repo access controls; no secrets in commits |
| AGY Host Runtime | All tool calls, file operations, hook events | Host-level trust; investigate telemetry |
