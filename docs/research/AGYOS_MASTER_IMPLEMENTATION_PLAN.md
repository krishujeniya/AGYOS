# AGYOS Master Implementation Plan & Resumable Execution Architecture

**Document Version:** 1.0.0  
**Target Architecture:** AGYOS v3.1 on Ubuntu 25.04 (3.3GB RAM ceiling, Python 3.13, Node 24, Bun 1.3)  
**Governing Standard:** Top 1% FAANG/Research Lab Staff Engineering Discipline  
**Baseline Git SHA:** `35903ad9125607daf89ca2f189864136dbe18a67`  
**Working Branch:** `main` (Strict Single-Branch Invariant)

---

## 1. Executive Strategy & Prioritization Matrix

This plan translates the 45 audited principles from ten reference platforms and 41 FAANG/SRE standards into atomic, test-driven implementations for AGYOS. Work proceeds strictly under the AGYOS 5-Gate Spine (`UNDERSTAND` -> `ANALYZE` -> `PLAN` -> `IMPLEMENT` -> `VERIFY`).

```
[Phase 0: Safe Baseline Sync] (COMPLETED: 35903ad)
         │
         ▼
[Phase 1 & 2: Platform Audits & Standards] (COMPLETED: 10 Platforms + 9 Standards)
         │
         ▼
[Phase 3: Cryptographic Boundaries & Threat Modeling] (COMPLETED: Vault + E2EE + Threat Model)
         │
         ▼
[Phase 4: Model Registry, Routing Policy & Context Economics] (COMPLETED: model_router.py + tests)
         │
         ▼
[Phase 5: Core Platform, DevOps & Observability Runbook] (IN PROGRESS)
         │
         ▼
[Phase 6: Adversarial Verification & Golden Task Suite] (PENDING)
```

### Workstream Priority Ranking:
- **P0 (Security & Data Integrity):** Fail-closed tool execution, honest encryption boundaries, zero plaintext secret leakage, pre-write snapshots.
- **P1 (Core Platform & Routing):** Model capability routing, T0-T3 complexity mapping, context economics, privacy gating for confidential data.
- **P2 (DevOps & Observability):** Traceability, local OTel JSONL spans, SLO verification, 4GB RAM performance baselines.
- **P3 (Operational Tooling):** CLI helpers, runbook documentation, migration and rollback procedures.

---

## 2. Dependency Graph & Architecture Decision Records (ADRs)

### ADR-0002: Model Registry & Privacy-Gated Routing
- **Status:** IMPLEMENTED
- **Context:** Cloud LLM providers (Google, Anthropic) process prompts in plaintext over TLS. Highly sensitive or confidential code must not be transmitted without explicit operator consent or local inference.
- **Decision:** Implement `agyos_decision/model_router.py` with strict `DataSensitivity` classification (`public`, `internal`, `confidential`, `secret`). If sensitivity is `confidential` or `secret` and no local attested endpoint exists, the router fails closed with `LOCAL_INFERENCE_UNAVAILABLE`.
- **Consequences:** Protects proprietary data; prevents silent cloud exfiltration; routes standard tasks based on complexity (T0 low-risk Flash Low to T3 deep reasoning).

### ADR-0003: Memory Vault Isolation vs Global E2EE
- **Status:** IMPLEMENTED
- **Context:** Previous documentation occasionally claimed system-wide E2EE, which is technically inaccurate because model prompts and local JSON files reside outside the envelope.
- **Decision:** Restrict cryptographic claims to two explicitly tested boundaries: (1) At-Rest Memory Vault (`private-vault.cjs`), and (2) Endpoint-to-Endpoint Secure Envelope (`e2ee.cjs`). All public and internal documentation reflects `PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE`.
- **Consequences:** Unimpeachable security honesty; zero false assurances for end-users.

### ADR-0004: Resource Boundedness on 4GB Ubuntu
- **Status:** IMPLEMENTED
- **Context:** Target host runs Ubuntu 25.04 with 3.3GB available RAM. Spawning persistent Docker daemons, browser automation instances, or unbounded concurrent skill work can exhaust available memory.
- **Decision:** Mandate lazy catalog search (`agyos_find_skill`), single-agent execution by default, subprocess timeouts (15s), and memory-efficient Python/Node scripting.
- **Consequences:** System executes reliably under 1.0GB active RAM without swap thrashing.

---

## 3. Resumable Execution Matrix & Milestone Roadmap

| Milestone ID | Scope & Deliverable | Priority | Status | Verification Evidence |
|---|---|---|---|---|
| **M0-BASELINE** | Safe Git sync to remote `origin/main` (`35903ad`), host environment audit | P0 | **DONE** | Local `main` fast-forwarded cleanly; 98 Python tests pass |
| **M1-AUDIT-10** | 10 Reference agent platform deep audit (`docs/research/TEN_AGENT_PLATFORMS.md`) | P1 | **DONE** | 45 principles mapped with file/line evidence |
| **M2-STANDARDS** | FAANG/SRE/OWASP/SLSA crosswalk (`docs/research/FAANG_SRE_DEVOPS_PRINCIPLES.md`) | P1 | **DONE** | 41 standards cross-referenced to AGYOS files |
| **M3-THREAT-SEC** | Threat Model (`THREAT_MODEL.md`), Data Flow Inventory (`DATA_FLOW_INVENTORY.md`), Encryption Coverage (`ENCRYPTION_COVERAGE.md`) | P0 | **DONE** | Honest trust boundaries; Node tests (17/17 pass) |
| **M4-MODEL-ROUTER**| AGYOS Model Registry, Routing Policy & Context Economics (`model_router.py`) | P1 | **DONE** | 12/12 unit tests pass (`test_model_router.py`) |
| **M5-CLI-INTEG** | Integrate `model-route` into `bin/agyos` and wire into intent compiler | P1 | **IN PROGRESS** | Shell syntax checks + CLI execution tests |
| **M6-RUNBOOK** | Operations Runbook (`docs/OPERATIONS_RUNBOOK.md`) covering SLOs, incidents, safe rollbacks | P2 | **PENDING** | Markdown documentation + verified commands |
| **M7-VERIFY-REPORT**| Full verification suite (`agyos-verify.sh`), 4GB RAM benchmark, Master Report (`docs/IMPLEMENTATION_REPORT.md`) | P0 | **PENDING** | Clean exit codes across all test runners |

---

## 4. Rollback & Migration Safety Strategy

1. **Non-Destructive Reversibility:** All changes reside in clean, modular files. Never execute `git reset --hard` or `git clean -fd` on shared branches.
2. **Safe Rollback Tooling:** `bin/rollback.sh` creates clean inverse git commits on `main` without creating secondary branches or discarding untracked files.
3. **Pre-Write Snapshots:** `scripts/hooks/authorizer.py` automatically captures SHA-256 identified backups in `.agents/state/snapshots/` before any file write tool executes.
4. **Passphrase FD Protection:** Cryptographic keys and passphrases are never passed via command-line arguments or environment variables where process tables or shell logs can inspect them.
