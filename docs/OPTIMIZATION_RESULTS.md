# Applied AGYOS optimization results

Date: 2026-11-11. Branch: `main`. Baseline revision: `190e8eac09cb17675442c3740a983b5f28b81ede`. Changes are local and uncommitted.

Delivered: [14-paper research review and 16 principles](research/OPTIMIZATION_RESEARCH.md), [one reusable prompt](OPTIMIZATION_PROMPT.md), [implementation plan](research/OPTIMIZATION_PLAN.md), regression fixes, benchmark evidence, and [ADR 0002](adr/0002-budget-and-routing-contracts.md).

## What changed

| Area | Before | After | Evidence |
|---|---|---|---|
| USD accounting | 1,000 charges of $0.001 recorded $0.00; cent rounding lost each charge | Exact rational accounting from decimal input retains small charges and enforces the actual cap | `scripts/tests/test_budget_hardening.py`: cumulative charges and boundary regressions |
| Numeric inputs | Negative tokens/USD/calls could reduce usage; NaN could bypass comparisons | Invalid, boolean/fractional counts and negative/nonfinite amounts reject before state changes | Invalid configuration/usage and atomic-charge tests |
| Arithmetic isolation | Initial repair depended on the caller's Decimal precision | Fraction arithmetic preserves cap checks even with precision 1/4/28 and Decimal rounding traps | Reviewer reproduction, precision and sub-float tests; ADR records the tradeoff |
| Recovery allowance | Reserve purpose ignored; elapsed time and tool reserve unenforced | Only verification/rollback labels accepted; monotonic deadline and reserved tool capacity checked on consumption | Fake-clock deadline and recovery-capacity tests; no sleeps |
| Graph updates | Failed insertion could leave a child attached to an earlier parent; duplicate task IDs overwrote entries | Validate before replacing maps; reject duplicate IDs and invalid depths; preserve forward references | `test_state_recovery.py`: failure leaves both maps unchanged |
| Routing transport | Fallback/integration candidate dictionaries exposed cached sets and failed JSON encoding | Explicit public candidate fields serialize through Python, CLI, and MCP | `test_routing_contract.py`; repeated workload JSON failures drop from 90 to zero |
| Test isolation | Patched manifest paths could be bypassed by a populated cache | Clear cache for source-patching tests; assert that fallback actually executes | `test_skill_routing.py`; all existing assertions retained |
| Verification liveness | Installed `agy agents` call could hang indefinitely | Existing host-discovery test has a 30-second timeout and still asserts all five pods | Full run now reports the host timeout as an error instead of hanging |

Accounting is still a single-owner, in-process primitive. Callers must check before dispatch; this patch does not implement authenticated authorization, persistent distributed reservations, provider billing settlement, or cancellation of an already-running tool. Recovery purpose labels classify usage; they do not grant permission. Public float views can round below float resolution; internal money comparisons remain exact. Integer token/tool reserves round down to whole units.

## Measured routing experiment

Command: `python3 scripts/benchmark_decision.py --repeats 30 --output <path>`.

Each run executes ten fixed development cases 30 times against 1,979 skills. Warm-up precedes measurement; JSON checks occur outside the timed routing call. The report includes raw samples, Python/platform/revision, router source hash, selected skills, ranking hash, and error categories. There are zero model/provider calls. These are microbenchmarks and regression fixtures, not held-out agent-quality evaluations.

| Run | Warm p50 (ms) | Warm p95 (ms) | JSON errors / 300 calls | Ranking |
|---|---:|---:|---:|---|
| [Baseline 1](research/evidence/optimization-baseline-1.json) | 8.352 | 11.947 | 90 | Reference |
| [Baseline 2](research/evidence/optimization-baseline-2.json) | 8.358 | 11.954 | 90 | Identical |
| [Candidate 1: bounded top-k](research/evidence/optimization-candidate-1.json) | 8.383 | 11.983 | 0 | Identical |
| [Candidate 2: bounded top-k](research/evidence/optimization-candidate-2.json) | 8.065 | 11.410 | 0 | Identical |
| [Final 1: original sort, concurrent validation load](research/evidence/optimization-final.json) | 9.204 | 17.049 | 0 | Identical |
| [Final 2: original sort, isolated rerun](research/evidence/optimization-final-2.json) | 8.352 | 11.982 | 0 | Identical |

All runs have ranking SHA-256 `2df456a40aec233055cc19b9edd77599d701fe9b38658f86a02f6100cd1df5ad`. Bounded top-k was faster in an isolated sorting microbenchmark, but its complete-routing benefit was inconsistent. It was rejected; final source retains the original sort. No overall latency improvement is established. The supported improvement is correct JSON transport without changed fixed-case rankings. Cold catalog load and warm routing are separate metrics; neither includes CLI startup, transport, external tools, or model inference.

## Executed verification

| Check | Result | Scope or limitation |
|---|---|---|
| Initial failing regression run | 28 tests, 37 reported failures and 9 errors | Captured before fixes; includes subtests, so counts are not distinct test methods |
| Full Python discovery after initial repairs | 125 passed, 1 error, 126 total; 54.363 s | Installed host `agy agents` exceeded 30 seconds. Two precision regressions were added afterward |
| Final local Python discovery | **127 passed**, 11.016 s | Exactly one previously failed installed-host case excluded explicitly; not a full-suite pass |
| Independent checker targeted suite | **49 passed**, 4.944 s | Budget, routing, CLI/MCP, state, and catalog cases after final precision repair |
| Independent accounting probes | Passed | Original precision bypass now rejects; precision 1/4/28 and rounding traps tested |
| Node crypto/vault/MCP tests | **17 passed**, 0 skipped | Local tampering, permission, round-trip, and malformed-payload tests |
| Bun council tests | **59 passed**, 134 expectations | Deterministic local tests; no council model invocation |
| Generated catalogs and docs | **7/7 byte-identical** | Generated into a temporary directory; no generated production assets changed |
| Standard-library trace coverage | **95% ledger, 97% router** | 49 tests, with missing executable lines included; line coverage only |
| Python compile, Bash syntax, state schema, diff whitespace | Passed | Syntax/state checks are not type analysis |
| Existing test assertion ratchet | Passed | Modified files: 18 -> 18, 42 -> 43, 38 -> 42 assertions; new regressions are additional |
| Repository secret scanner | Passed, zero matches | Built-in pattern fallback with output redacted; Gitleaks is not installed, so no Gitleaks claim |
| Python Ruff/type checker | Not run | Neither installed nor configured for this project; no passing claim |
| Live model/host mediation, deployment, UI | Not performed | No paid calls, publication, deployment, or UI changes |

Coverage and durable verification metadata are recorded in [verification evidence](research/evidence/optimization-verification.json). Coverage is a line-execution metric, not a safety or branch-completeness certificate.

Reproduction commands:

```bash
python3 -m unittest scripts.tests.test_budget_hardening scripts.tests.test_routing_contract scripts.tests.test_state_recovery scripts.tests.test_skill_routing -v
python3 scripts/benchmark_decision.py --repeats 30 --output /tmp/agyos-routing.json
timeout 150s python3 -m unittest discover -s scripts/tests -v
node --test scripts/tests/test_secure_envelope.cjs scripts/tests/test_private_vault.cjs scripts/tests/test_mcp_protocol.cjs
(cd scripts/council && bun test)
python3 -X pycache_prefix=/tmp/agyos-optimization-bytecode -m compileall -q agyos_decision scripts/tests scripts/benchmark_decision.py
git diff --check
```

The full command intentionally retains the installed-host check and may report its timeout. The final local run used unittest discovery and excluded only `test_hooks_authorizer.PodDefinitionsTests.test_agy_cli_lists_all_5_pods`; all other cases ran. This exclusion does not resolve host acceptance.

## Independent review and remaining acceptance

Independent checker `optimization_checker` returned **scoped technical PASS** after the precision repair. It ran fresh checks and made no source changes. It did not certify host mediation, production readiness, or human acceptance.

Maker review questions and answers:

1. **Where must authorization live if reserve purposes are labels?** At the trusted host/dispatch boundary for each effect. A caller-provided string cannot establish authority.
2. **What happens when Decimal precision changes or charges are tiny?** Validated decimal input converts to exact rational arithmetic, independent of ambient precision. Float display rounding cannot weaken cap comparisons.
3. **What compatibility and evidence limits matter?** Invalid counts/amounts, unknown reserve labels, duplicate IDs, and deadline/cap violations now reject intentionally. JSON/ranking tests establish transport and fixed-case compatibility, not real task success or a latency gain.

The installed host reports **AGY CLI 1.5.5**. Its `agents` discovery stalled during unrestricted baseline and failed the bounded final test; MCP processes were observed during startup. The specific host cause is not established. Task-owned orphan subprocesses were cleaned up. No host configuration was modified. The complete host verifier was not run because it repeats these stalled host calls without individual timeouts.

The governance record remains at VERIFY with local scoped verification passed and host/human acceptance unresolved. No production sign-off is recorded. Remaining experiments and dependencies are listed in the [research review](research/OPTIMIZATION_RESEARCH.md#follow-up-experiments-with-acceptance-criteria).

Next permitted check, after inspecting/isolation of the installed host configuration:

```bash
timeout 40s python3 -m unittest scripts.tests.test_hooks_authorizer.PodDefinitionsTests.test_agy_cli_lists_all_5_pods -v
```

Do not repeat that failing probe unchanged. A real agent-quality evaluation of the prompt remains separate work requiring a task dataset and explicit provider-spend authorization.
