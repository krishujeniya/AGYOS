# AGYOS Operations, SRE & Incident Response Runbook

**System:** AGYOS v3.1 Autonomous Agent Operating System  
**Target Environment:** Local Ubuntu Workstation (2–4 GB RAM, Node 24, Python 3.13, Bun 1.3)  
**Standard:** Google SRE Principles, SLSA Level 1-2 Provenance, Monotonic Test Ratchets  
**Document Revision:** 2026-11-08

---

## 1. System Architecture & Component Inventory

AGYOS operates strictly as a local-first single-operator CLI execution environment. It does not spawn background HTTP server daemons, multi-tenant databases, or unmonitored cloud services.

```
┌────────────────────────────────────────────────────────┐
│ AGYOS Operational Kernel (bin/agyos)                   │
├───────────────────┬───────────────────┬────────────────┤
│ Decision Engine   │ FastMCP Daemon    │ Security Hooks │
│ skills_router.py  │ state-server.cjs  │ authorizer.py  │
│ model_router.py   │ stdio JSON-RPC    │ agy_os_hook.py │
├───────────────────┴───────────────────┴────────────────┤
│ State Machine: .agents/state/state.json                │
│ Private Vault: ~/.local/state/agyos/private-memory...  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Service Level Objectives (SLOs) & Error Budgets

AGYOS enforces local Service Level Indicators (SLIs) and deterministic launch gates evaluated via `scripts/canary_launch_gate.py`:

| Service / Capability | SLI (Metric) | Target SLO | Measurement Method | Error Budget Policy |
|---|---|---|---|---|
| **Skill Selection** | Top-1 Skill Relevance | >= 95% | Frozen corpus in `scripts/tests/fixtures/` | If test fails, block deployment |
| **Model Routing** | Privacy Compliance | 100% | `test_model_router.py` | Zero confidential leaks permitted |
| **Tool Execution** | Command Authorization | 100% fail-closed | `test_authorizer_hardening.py` | Untrusted auth tokens rejected |
| **Fast-Path Latency** | Command-to-Execution | < 250ms | `bin/agyos fast` execution time | Optimize if startup > 500ms |
| **Memory Footprint** | Peak Process RSS | < 500MB | `/proc/self/statm` on Ubuntu | Kill agent if RSS > 1.5GB |
| **Test Monotonicity**| Total Test Assertions | Monotonic | `bin/gate-check.sh` pre-commit | Total assertions must never decrease |

---

## 3. Routine Operations & Setup Procedures

### 3.1 Initial Workspace Verification
```bash
# Verify system dependencies and git status
git status --short --branch
node --version && python3 --version && bun --version

# Run full baseline verification
bash scripts/agyos-verify.sh
```

### 3.2 Initializing the Private Encrypted Vault
The encrypted memory vault is stored outside the repository at `~/.local/state/agyos/private-memory.vault.json`. Passphrases must never appear in command-line arguments.
```bash
# Initialize vault via non-echoing file descriptor
read -rs -p "Enter 16+ char vault passphrase: " VAULT_PASS; printf '\n'
printf '%s' "$VAULT_PASS" | bin/agyos secure vault-init --passphrase-fd 0
unset VAULT_PASS
```

### 3.3 Executing Model Routing & Context Checks
```bash
# Check autonomous model selection and context economics
bin/agyos model-route "implement user authentication with JWT"

# Verify privacy enforcement for confidential data
bin/agyos model-route "process customer PII and card records" --sensitivity confidential
```

### 3.4 Context Window Compaction
When active conversational context exceeds 65% of the effective window (~83,200 tokens for Gemini Flash), execute compaction:
```bash
bin/agyos compact
```

---

## 4. Incident Response & Emergency Procedures

### 4.1 Severity 1 (SEV-1): Runaway Agent Loop / High Token Burn
- **Symptoms:** Agent repeating identical failing commands, `no_progress_strikes >= 3`, or unexpected token expenditure.
- **Immediate Mitigation:**
  1. Terminate running subagent processes (`manage_subagents` kill action or `kill -9`).
  2. Inspect `.agents/state/state.json` to verify `iteration_cap` (default 10) was not overridden.
  3. Reset gate to `IDLE`:
     ```bash
     source bin/state.sh && set_gate IDLE
     ```

### 4.2 SEV-2: Corrupted Working Tree or Erroneous Code Mutations
- **Symptoms:** Broken builds, unintended file modifications, or syntax regressions across multiple files.
- **Immediate Mitigation:**
  1. Execute safe single-branch rollback:
     ```bash
     bin/agyos rollback
     ```
  2. Verify working tree cleanliness:
     ```bash
     git status --short
     ```
  3. Pre-write snapshots are preserved in `.agents/state/snapshots/` and can be inspected if individual files need manual recovery.

### 4.3 SEV-3: Memory Exhaustion (OOM) on 4GB Ubuntu
- **Symptoms:** Host system responsiveness degrades, swap thrashing, Python/Node process killed by Linux OOM killer.
- **Immediate Mitigation:**
  1. Clear temporary bytecode caches:
     ```bash
     rm -rf /tmp/agyos-bytecode /tmp/agyos-check.*
     ```
  2. Ensure background council processes or dangling subagents are terminated:
     ```bash
     pkill -f "state-server.cjs" || true
     pkill -f "council.ts" || true
     ```
  3. Bound subagent memory limit using Linux `prlimit`:
     ```bash
     prlimit --as=2147483648 <command>
     ```

---

## 5. Safe Upgrade & Release Gate Runbook

Before tagging or pushing any release to `origin/main`:

1. **Syntax Integrity:**
   ```bash
   bash -n bin/agyos bin/rollback.sh scripts/agyos-verify.sh
   node --check mcp/state-server.cjs
   python3 -m compileall -q .
   ```

2. **Automated Unit & Hardening Suite:**
   ```bash
   python3 -m unittest discover -s scripts/tests -q
   node --test scripts/tests/test_secure_envelope.cjs
   node --test scripts/tests/test_private_vault.cjs
   node --test scripts/tests/test_mcp_protocol.cjs
   ```

3. **Privacy Audit:**
   ```bash
   python3 scripts/agyos-privacy-audit.py
   ```

4. **Canary Launch Gate Evaluation:**
   ```bash
   python3 scripts/canary_launch_gate.py
   ```

5. **Monotonic Test Ratchet:**
   ```bash
   bash bin/gate-check.sh
   ```
