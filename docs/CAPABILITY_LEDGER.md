# Capability ledger

Baseline source revision: `0ad85cdb1179941cccfe5f9113dcef64e826b49c`
Implementation worktree: later than the baseline; see the current Git revision and Actions run before treating this ledger as release evidence.
Assessment date: 2026-11-15

This ledger distinguishes code presence from verified operational behavior. No test run is claimed here.

| Capability | Evidence | Status | Boundary |
|---|---|---|---|
| Natural-language task planning | `scripts/agyos_e2e.py`; `agyos_decision/intent_compiler.py`; `agyos_decision/skills_router.py` | Implemented; runtime outcome unverified | Planning and routing do not prove task execution |
| Typed task contracts | `agyos_decision/contracts.py`; `agyos_decision/contracts.schema.json` | Implemented; compatibility suite pending | Contract validity does not grant permission |
| Skill discovery | `agyos_decision/skills_router.py`; `mcp/state-server.cjs` | Implemented; retrieved runbook execution is unverified | Selection status is not completion evidence |
| Tool interception | `.agents/hooks.json`; `scripts/hooks/authorizer.py`; `scripts/hooks/agy_os_hook.py` | Partial; host mediation unverified | Do not enable unattended privileged effects |
| Irreversible action approval | `scripts/hooks/authorizer.py`; `docs/HOST_COMPATIBILITY.md` | Missing trusted verifier | Matched high-impact shell commands remain denied |
| Durable Python task/outbox state | `agyos_decision/state_ledger.py` | Missing | Snapshot and outbox objects are process-local |
| Durable runtime state primitives | `scripts/agyos-runtime/lib/state-store/` | Implemented; suitability for task lifecycle unverified | Candidate for reuse; not yet task-state owner |
| Business role adapters | `agyos_decision/company_adapters.py` | Partial | Adapter methods do not establish live integration or production permission |
| CI regression suites | `.github/workflows/ci.yml`; `scripts/tests/` | Configured; current worktree run pending | Only the exact revision's completed Actions result is verification |
| Production release | `docs/HOST_COMPATIBILITY.md`; `scripts/agyos_e2e.py` | Unverified | Require host-bound authorization, durable recovery and exact-SHA CI |

## Baseline evaluation

No token, latency, cost, routing-accuracy, or task-success measurements are recorded. Establish them with frozen representative cases and matched model/tool configurations before accepting optimization claims. Targets are not measurements.
