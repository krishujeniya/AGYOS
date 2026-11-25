# AGYOS Operations, SRE & Incident Response Runbook

**System:** AGYOS v3.2.0 Autonomous Agent Operating System
**Target Environment:** Local Linux / macOS Workstation (Node 22+, Python 3.12+ via `uv`)
**Standard:** Google SRE Principles, SLSA Level 1-2 Provenance, Monotonic Test Ratchets
**Document Revision:** 2026-11-25

---

## 1. System Architecture & Component Inventory

AGYOS operates strictly as a local-first single-operator CLI execution environment. It does not spawn background HTTP server daemons, multi-tenant databases, or unmonitored cloud services.

```
┌────────────────────────────────────────────────────────┐
│ AGYOS Operational Kernel (gemini/antigravity-cli/bin/agyos)            │
├───────────────────┬───────────────────┬────────────────┤
│ Decision Engine   │ FastMCP Daemon    │ Security Hooks │
│ skills_router.py  │ state-server.cjs  │ authorizer.py  │
│ model_router.py   │ stdio JSON-RPC    │ agy_os_hook.py │
├───────────────────┴───────────────────┴────────────────┤
│ State Machine: gemini/antigravity-cli/builtin/state/state.json                 │
│ Private Vault: ~/.local/state/agyos/private-memory...  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Service Level Objectives (SLOs) & Error Budgets

AGYOS enforces local Service Level Indicators (SLIs) and deterministic launch gates evaluated via `gemini/antigravity-cli/builtin/scripts/canary_launch_gate.py`:

| Service / Capability | SLI (Metric) | Target SLO | Measurement Method | Error Budget Policy |
|---|---|---|---|---|
| **Skill Selection** | Top-1 Skill Relevance | >= 95% | Frozen corpus in `gemini/antigravity-cli/builtin/scripts/tests/fixtures/` | If test fails, block deployment |
| **Model Routing** | Privacy Compliance | 100% | `test_model_router.py` | Zero confidential leaks permitted |
| **Tool Execution** | Command Authorization | 100% fail-closed | `test_authorizer_hardening.py` | Untrusted auth tokens rejected |
| **Fast-Path Latency** | Command-to-Execution | < 250ms | `gemini/antigravity-cli/bin/agyos fast` execution time | Optimize if startup > 500ms |
| **Memory Footprint** | Peak Process RSS | < 500MB | `/proc/self/statm` on Ubuntu | Kill agent if RSS > 1.5GB |
| **Test Monotonicity**| Total Test Assertions | Monotonic | `gemini/antigravity-cli/bin/gate-check.sh` pre-commit | Total assertions must never decrease |

---

## 3. Routine Operations & Setup Procedures

### 3.1 Initial Workspace Verification
```bash
# Verify system dependencies and git status
git status --short --branch
node --version && uv --version

# Run full baseline verification
bash gemini/antigravity-cli/builtin/scripts/agyos-verify.sh
```

### 3.2 Initializing the Private Encrypted Vault
The encrypted memory vault is stored outside the repository at `~/.local/state/agyos/private-memory.vault.json`. Passphrases must never appear in command-line arguments.
```bash
# Initialize vault via non-echoing file descriptor
read -rs -p "Enter 16+ char vault passphrase: " VAULT_PASS; printf '\n'
printf '%s' "$VAULT_PASS" | gemini/antigravity-cli/bin/agyos secure vault-init --passphrase-fd 0
unset VAULT_PASS
```

### 3.3 Executing Model Routing & Context Checks
```bash
# Check autonomous model selection and context economics
gemini/antigravity-cli/bin/agyos model-route "implement user authentication with JWT"

# Verify privacy enforcement for confidential data
gemini/antigravity-cli/bin/agyos model-route "process customer PII and card records" --sensitivity confidential
```

### 3.4 Context Window Compaction
When active conversational context exceeds 65% of the effective window (~83,200 tokens for Gemini Flash), execute compaction:
```bash
gemini/antigravity-cli/bin/agyos compact
```

---

## 4. Incident Response & Emergency Procedures

### 4.1 Severity 1 (SEV-1): Runaway Agent Loop / High Token Burn
- **Symptoms:** Agent repeating identical failing commands, `no_progress_strikes >= 3`, or unexpected token expenditure.
- **Immediate Mitigation:**
  1. Terminate running subagent processes (`manage_subagents` kill action or `kill -9`).
  2. Inspect `gemini/antigravity-cli/builtin/state/state.json` to verify `iteration_cap` (default 10) was not overridden.
  3. Reset gate to `IDLE`:
     ```bash
     gemini/antigravity-cli/bin/agyos gate IDLE
     ```

### 4.2 SEV-2: Corrupted Working Tree or Erroneous Code Mutations
- **Symptoms:** Broken builds, unintended file modifications, or syntax regressions across multiple files.
- **Immediate Mitigation:**
  1. Execute safe single-branch rollback:
     ```bash
     gemini/antigravity-cli/bin/agyos rollback
     ```
  2. Verify working tree cleanliness:
     ```bash
     git status --short
     ```
  3. Pre-write snapshots are preserved in `gemini/antigravity-cli/builtin/state/snapshots/` and can be inspected if individual files need manual recovery.

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

1. **Syntax Integrity (Fast Local Checks):**
   ```bash
   make typecheck
   make lint
   bash -n gemini/antigravity-cli/bin/agyos gemini/antigravity-cli/bin/rollback.sh gemini/antigravity-cli/builtin/scripts/agyos-verify.sh
   node --check gemini/antigravity-cli/mcp/state-server.cjs
   ```

2. **Automated Unit & Hardening Suite (Executed in GitHub Actions `.github/workflows/ci.yml`):**
   ```bash
   cd gemini/antigravity-cli/builtin && uv run --with-requirements scripts/requirements.txt python -m unittest discover -s scripts/tests -q
   node --test gemini/antigravity-cli/builtin/scripts/tests/test_secure_envelope.cjs
   node --test gemini/antigravity-cli/builtin/scripts/tests/test_private_vault.cjs
   node --test gemini/antigravity-cli/builtin/scripts/tests/test_mcp_protocol.cjs
   ```

3. **Privacy Audit:**
   ```bash
   uv run python gemini/antigravity-cli/builtin/scripts/agyos-privacy-audit.py
   ```

4. **Canary Launch Gate Evaluation:**
   ```bash
   uv run python gemini/antigravity-cli/builtin/scripts/canary_launch_gate.py
   ```

5. **Monotonic Test Ratchet:**
   ```bash
   bash gemini/antigravity-cli/bin/gate-check.sh
   ```

---

## 6. Disaster Recovery, Restore Drill & Retention Limits

### 6.1 Workspace State Machine Architecture & Authoritative Storage
AGYOS uses a dual-layer state architecture:
1. **Primary Authoritative Store (`workspace-state.db` via `gemini/antigravity-cli/builtin/scripts/agyos-runtime/`):** ACID transactional store managing `workspace_milestones` and `workspace_operations` tables with monotonically increasing revision counters, CAS conflict detection, and deterministic replay.
2. **Projections (`gemini/antigravity-cli/builtin/state/state.json`, `gemini/antigravity-cli/builtin/state/CURRENT.md`):** Derived read-only summaries reconstructed from the authoritative database.

### 6.2 Disaster Recovery Drill: Reconstructing Corrupted State (<5 min MTTR)
If `gemini/antigravity-cli/builtin/state/state.json` is corrupted, truncated, or removed:
```bash
# 1. Inspect SQLite workspace status to identify the authoritative milestone and latest revision
gemini/antigravity-cli/bin/agyos workspace status

# 2. Re-project the authoritative state directly from SQLite
gemini/antigravity-cli/bin/agyos workspace project <milestone_id>

# 3. If an explicit revision rollback is required:
gemini/antigravity-cli/bin/agyos workspace restore <milestone_id> <target_revision>

# 4. Verify working state integrity
gemini/antigravity-cli/bin/agyos state
```

### 6.3 Transactional Replay & In-Flight Crash Recovery
If an operation process was terminated in mid-flight (power outage, kill -9):
```bash
# Replay the operation idempotently; if already committed, returns existing result without mutation
gemini/antigravity-cli/bin/agyos workspace replay <milestone_id> <operation_id>
```

### 6.4 Redacted Diagnostics Export
To share system state or file an issue without disclosing user paths or secrets:
```bash
# Export redacted diagnostic bundle
gemini/antigravity-cli/bin/agyos diagnostics --output /tmp/agyos-diagnostic-bundle.json

# Preview redacted diagnostic bundle
gemini/antigravity-cli/bin/agyos diagnostics --preview
```
The export engine guarantees:
- All `/home/*` and `/Users/*` paths are sanitized to `~`.
- All tokens (`ghp_*`, `AKIA*`, Bearer tokens, private keys) are replaced with redacted markers.
- All internal sentinel markers are stripped.

### 6.5 Storage Retention & Deletion Policy
- **Disposable Diagnostics & CI Artifacts:** Retained for 7 days, then automatically purged.
- **Pre-write Snapshots (`gemini/antigravity-cli/builtin/state/snapshots/`):** Retained for the duration of the active milestone, pruned upon milestone completion.
- **Authoritative Milestones & Audit Trails:** Retained locally until explicitly archived by the operator.

---

## 7. Documentation release candidates

A successful push-triggered CI run produces `pages-candidate` and
`documentation-image-candidate`. Record the run URL and full commit SHA.
The candidates are retained for 14 days. Dispatch the corresponding
publication workflow on `main` only after approving that revision for the
destination. The workflow verifies the candidate's checksums before publishing.
If the candidate has expired, generate and verify a new candidate.

Verify the expected Pages route and container digest after publication. Record
the previously approved image digest before moving `latest`. If a release
must be rolled back, restore the previous approved image digest and use
the retained, verified Pages bundle through an authorized publication job.
Keep publication paused if the previous artifact cannot be verified.
