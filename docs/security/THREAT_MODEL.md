# AGYOS Threat Model

**Version:** 1.0
**Date:** 2026-11-08
**Baseline commit:** `35903ad9125607daf89ca2f189864136dbe18a67`
**Methodology:** STRIDE per data flow, adapted for local-first agent OS

Catalog inventory note (2026-11-12): the physical catalog now contains 2,180 skills, including pinned third-party source adapters. This note updates the inventory count only; the threat model remains the 2026-11-08 baseline and has not been re-audited for these imports.

## 1. Protected Assets

| Asset | Classification | Storage | Current Protection |
|-------|---------------|---------|-------------------|
| User source code | Confidential | Git worktree | File permissions, Git ACL |
| Agent state (milestones, gates) | Internal | `.agents/state/state.json` | Plaintext JSON, file permissions |
| Memory tiers (tier0/1/2) | Confidential | `.agents/state/memory.json` + encrypted vault | Plaintext legacy + AES-256-GCM vault (opt-in) |
| Decision receipts | Internal | `.agents/state/decisions/` | Plaintext JSON |
| Checkpoint history | Internal | `.agents/state/checkpoints/` | Plaintext |
| Context graph | Internal | `.agents/state/context-graph.json` | Plaintext |
| Encrypted envelope keys | Secret | `~/.config/agyos/identity.json` | scrypt + AES-256-GCM, mode 0600, dir mode 0700 |
| Private vault data | Confidential | `~/.local/state/agyos/private-memory.vault.json` | AES-256-GCM, scrypt KDF, mode 0600 |
| Model API keys | Secret | Environment variables | Not stored in repo; env-only |
| Skill catalog (1,862 skills at this threat-model baseline) | Public | `.agents/skills/` | Git-tracked, read-only usage |
| E2EE envelope messages | Confidential | User-specified paths | X25519+AES-256-GCM+Ed25519 |

## 2. Trust Boundaries

```
┌─────────────────────────────────────────────────────┐
│ AGYOS Local Process (Trusted)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ CLI (bin/agyos)│  │ MCP Server   │  │ Hooks     │  │
│  │ Shell process │  │ stdio JSON-RPC│  │ authorizer│  │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │
│         │                 │                │         │
│  ┌──────┴─────────────────┴────────────────┴──────┐  │
│  │ Local Filesystem (.agents/, scripts/, mcp/)     │  │
│  └─────────────────────┬──────────────────────────┘  │
│                        │                             │
│  ┌─────────────────────┴──────────────────────────┐  │
│  │ Encrypted Vault (outside repo, mode 0600)       │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ TRUST BOUNDARY
┌──────────────────────┴──────────────────────────────┐
│ External (Untrusted / Partially Trusted)             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ AI Provider   │  │ GitHub API   │  │ Network   │  │
│  │ (Gemini/Claude)│  │ (push/fetch) │  │ (general) │  │
│  └──────────────┘  └──────────────┘  └───────────┘  │
│  ┌──────────────┐  ┌──────────────┐                  │
│  │ Browser Tools │  │ External MCP │                  │
│  │ (if enabled)  │  │ Servers      │                  │
│  └──────────────┘  └──────────────┘                  │
└──────────────────────────────────────────────────────┘
```

## 3. STRIDE Analysis

### 3.1 Spoofing

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| S1: Forged authorization in tool payloads | `authorized=true` or `outbox_token` in model-generated tool args | Authorizer ignores payload auth flags; all R3 blocked until external verifier | MITIGATED |
| S2: Forged MCP tool responses | Model fabricates tool results | MCP server validates JSON-RPC protocol; no model-writable control plane | MITIGATED |
| S3: Impersonated E2EE sender | Wrong public key used | Manual fingerprint verification required; no PKI/TOFU | MITIGATED (manual) |
| S4: Spoofed skill identity | Malicious skill YAML claims different provenance | Pinned third-party source paths, SHA-256 catalog digests, and automated preflight checks in scripts/audit_skill_catalog.py | MITIGATED |

### 3.2 Tampering

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| T1: Modified encrypted vault | Attacker edits vault file | AES-256-GCM authentication tag; tamper = decryption failure | MITIGATED |
| T2: Modified E2EE envelope | Attacker modifies ciphertext/header | AEAD + Ed25519 signature verification | MITIGATED |
| T3: Modified agent state | Direct edit of `.agents/state/` | Git branch tracking; sequence numbers, fence tokens, and dedup log in crates/store | MITIGATED |
| T4: Modified hook scripts | Attacker alters authorizer.py | File permissions; Git tracking; pre-commit verification gates | MITIGATED |

### 3.3 Repudiation

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| R1: Unattributed agent actions | No audit trail for tool executions | W3C PROV receipts in crates/adapters; decision ledgers in `.agents/state/decisions/` | MITIGATED |
| R2: Denied approval | Operator denies authorizing action | Explicit HITL state transitions in `.agents/state/state.json`; immutable checkpoint blocks | MITIGATED |

### 3.4 Information Disclosure

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| I1: Secrets in model prompts | Confidential data sent to cloud inference | Privacy audit scanner (scripts/agyos-privacy-audit.py) and zero-secrets invariant | PARTIAL (hosted model boundary) |
| I2: Secrets in Git history | Historical commits contain sensitive data | agy_security_scanner AST pattern scans; pre-commit hook checks | MITIGATED |
| I3: Plaintext state files | `.agents/state/` readable | Mode 0600 file permissions; private memory stored in AES-256-GCM vault | MITIGATED |
| I4: MCP error stack traces | Internal paths in error responses | Errors redacted in JSON-RPC responses | MITIGATED |
| I5: Secrets in logs/telemetry | Structured logging may capture prompts | Redacted metrics engine in crates/telemetry; no plaintext key logging | MITIGATED |

### 3.5 Denial of Service

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| D1: Oversized MCP input | Large JSON-RPC payload | Input size bounded (1MB); subprocess timeout (15s) | MITIGATED |
| D2: Recursive agent spawning | Unbounded fan-out/depth | Iteration cap in state.json; worker lease enforcement in apps/worker | MITIGATED |
| D3: Memory exhaustion (4GB) | Loading all skills/agents | Lazy loading; search-first discovery; memory budgets | MITIGATED |

### 3.6 Elevation of Privilege

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| E1: Tool permission escalation | Agent requests tools beyond scope | R0-R3 risk tier gating in crates/domain; broker confinement in crates/agy | MITIGATED |
| E2: Prompt injection | Untrusted content in skill/tool output | Pre-install scanning via skill-audit; static instruction-override pattern checks | MITIGATED |
| E3: Unauthorized file write | Agent writes to protected paths | Pre-write snapshots; path boundary enforcement in authorizer hooks | MITIGATED |

## 4. Risk Priority Matrix

| Risk ID | Priority | Impact | Likelihood | Current Status |
|---------|----------|--------|------------|----------------|
| I1 | P0 | High | High | PARTIAL — hosted inference boundary |
| E2 | P1 | High | Low | MITIGATED — pre-install scanner and pattern filtering |
| R2 | P1 | Medium | Low | MITIGATED — state.json HITL blocks |
| S4 | P1 | Medium | Low | MITIGATED — catalog audit script |
| T3 | P1 | Medium | Low | MITIGATED — fence tokens and Git index |
| I3 | P2 | Low | Low | MITIGATED — private vault separation |

## 5. Residual Risks

1. **Cloud provider inference**: Hosted models process prompt text sent over TLS. This remains an external trust boundary. Sensitive memory must stay in the local AES-256-GCM vault via `AGYOS_MEMORY_PRIVATE_ONLY=1`.
2. **Local root access**: A compromised local user shell can read local files. File mode protections (0600 for vault, 0700 for directories) protect against cross-user local access on multi-user systems.
3. **Skill third-party revisions**: External skill repositories can introduce regressions if pulled unpinned. All skills must remain pinned in the catalog and validated with `scripts/audit_skill_catalog.py`.

## 6. Recommended Next Actions

1. Implement prompt injection detection at the input boundary (P0)
2. Build cryptographic approval verifier for R3 operations (P0)
3. Add data classification labels to tool request schema (P0)
4. Encrypt `.agents/state/` at rest with vault integration (P1)
5. Add skill provenance verification (P1)
6. Implement runtime fan-out/depth limits (P2)
7. Commission independent cryptographic review (P1)
