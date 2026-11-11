# AGYOS Threat Model

**Version:** 1.0
**Date:** 2026-11-08
**Baseline commit:** `35903ad9125607daf89ca2f189864136dbe18a67`
**Methodology:** STRIDE per data flow, adapted for local-first agent OS

Catalog inventory note (2026-11-11): the physical catalog now contains 1,983 skills. This note updates the inventory count only; the threat model remains the 2026-11-08 baseline and has not been re-audited by the catalog milestone.

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
| S2: Forged MCP tool responses | Model fabricates tool results | MCP server validates JSON-RPC protocol; no model-writable control plane | PARTIAL |
| S3: Impersonated E2EE sender | Wrong public key used | Manual fingerprint verification required; no PKI/TOFU | MITIGATED (manual) |
| S4: Spoofed skill identity | Malicious skill YAML claims different provenance | Skill provenance not cryptographically verified | OPEN (P1) |

### 3.2 Tampering

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| T1: Modified encrypted vault | Attacker edits vault file | AES-256-GCM authentication tag; tamper = decryption failure | MITIGATED |
| T2: Modified E2EE envelope | Attacker modifies ciphertext/header | AEAD + Ed25519 signature verification | MITIGATED |
| T3: Modified agent state | Direct edit of `.agents/state/` | Plaintext; no integrity protection beyond Git | OPEN (P1) |
| T4: Modified hook scripts | Attacker alters authorizer.py | File permissions; Git tracking; no runtime integrity check | PARTIAL |

### 3.3 Repudiation

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| R1: Unattributed agent actions | No audit trail for tool executions | Decision receipts in `.agents/state/decisions/`; no signed log | PARTIAL |
| R2: Denied approval | Operator denies authorizing action | No cryptographic approval receipt system | OPEN (P0) |

### 3.4 Information Disclosure

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| I1: Secrets in model prompts | Confidential data sent to cloud inference | Privacy audit warns; no automatic blocking | PARTIAL |
| I2: Secrets in Git history | Historical commits contain sensitive data | Gitleaks scanning; no history rewrite | PARTIAL |
| I3: Plaintext state files | `.agents/state/` readable | File permissions only | OPEN (P1) |
| I4: MCP error stack traces | Internal paths in error responses | Errors redacted in JSON-RPC responses | MITIGATED |
| I5: Secrets in logs/telemetry | Structured logging may capture prompts | No PII/key logging policy; partial enforcement | PARTIAL |

### 3.5 Denial of Service

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| D1: Oversized MCP input | Large JSON-RPC payload | Input size bounded (1MB); subprocess timeout (15s) | MITIGATED |
| D2: Recursive agent spawning | Unbounded fan-out/depth | Iteration cap in state.json; no runtime enforcement | PARTIAL |
| D3: Memory exhaustion (4GB) | Loading all skills/agents | Lazy loading; search-first discovery | PARTIAL |

### 3.6 Elevation of Privilege

| Threat | Vector | Mitigation | Status |
|--------|--------|------------|--------|
| E1: Tool permission escalation | Agent requests tools beyond scope | Capability allowlist in authorizer; heuristic matching | PARTIAL |
| E2: Prompt injection | Untrusted content in skill/tool output | No runtime prompt injection defense | OPEN (P0) |
| E3: Unauthorized file write | Agent writes to protected paths | Pre-write snapshot; path validation in authorizer | MITIGATED |

## 4. Risk Priority Matrix

| Risk ID | Priority | Impact | Likelihood | Current Status |
|---------|----------|--------|------------|----------------|
| E2 | P0 | Critical | Medium | OPEN — prompt injection defense needed |
| R2 | P0 | Critical | Low | OPEN — no trusted approval verifier |
| I1 | P0 | High | High | PARTIAL — audit warns, no enforcement |
| I3 | P1 | Medium | Medium | OPEN — state files plaintext |
| S4 | P1 | Medium | Low | OPEN — skill provenance unsigned |
| T3 | P1 | Medium | Low | OPEN — state integrity unprotected |
| D2 | P2 | Medium | Low | PARTIAL — cap exists, not enforced |

## 5. Residual Risks

1. **Cloud provider inference**: Google/Anthropic hosted models must see plaintext prompts. This is an inherent trust boundary, not a fixable vulnerability. Mitigation: data classification + consent gating.
2. **No independent cryptographic audit**: Vault and E2EE implementations use Node.js crypto primitives (well-reviewed) but the protocol design has not been independently audited.
3. **Single-user local system**: Many enterprise threats (multi-tenant isolation, network attacks) are lower priority for a single-user CLI tool, but local compromise defeats all protections.
4. **Skill supply chain at this threat-model baseline**: 1,862 skills from various sources; no signature verification or sandboxed execution of skill-recommended commands.

## 6. Recommended Next Actions

1. Implement prompt injection detection at the input boundary (P0)
2. Build cryptographic approval verifier for R3 operations (P0)
3. Add data classification labels to tool request schema (P0)
4. Encrypt `.agents/state/` at rest with vault integration (P1)
5. Add skill provenance verification (P1)
6. Implement runtime fan-out/depth limits (P2)
7. Commission independent cryptographic review (P1)
