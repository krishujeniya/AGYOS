# Research-led AGYOS optimization

Date: 2026-11-11. Baseline: `190e8eac09cb17675442c3740a983b5f28b81ede`, branch `main`, initially clean.

## Task and acceptance

The operator requested relevant principles, primary-source papers, one reusable optimization prompt, and application to this project. That request authorizes the local research, implementation, and verification below. Publication, deployment, spending, and live customer actions require separate authorization.

1. Produce a ranked, attributable principle and paper review, separating published results from AGYOS measurements.
2. Write one reusable prompt covering architecture, correctness, security, cost, performance, context, evaluation, reliability, developer experience, documentation, and delivery.
3. Apply fixes to reproduced defects; measure any performance variant against identical cases. Preserve existing assertions and public routing semantics.
4. Run local regression and integration checks; obtain an independent checker verdict. Record unavailable or failed checks explicitly.

## Inspection and risk

- Existing plans: `docs/RESEARCH_PLAN.md`, `docs/research/AGYOS_MASTER_IMPLEMENTATION_PLAN.md`. Existing handoff performance numbers are historical, not current baselines.
- `RunBudgetTracker` accepts negative accounting increments, rounds each USD charge to cents, does not enforce its deadline, and ignores the reserve purpose. Reproduction: 1,000 charges of $0.001 record $0.00; negative tokens/calls reduce usage.
- Integration routing expands cached internal fields into the public decision. `json.dumps(decide_skill('Review code and find problems before release'))` raises `TypeError: Object of type set is not JSON serializable`.
- Catalog tests patch manifest paths without clearing the process cache. They can pass without executing the fallback they describe.
- `DAGTaskGraph.add_task` mutates earlier dependency child lists before rejecting a later full parent. Failed insertion can leave partial state. Duplicate IDs can overwrite existing tasks.
- Full baseline: restricted run executed 110 tests with one failure and four errors involving state writes/host subprocesses. Two unrestricted attempts stalled in installed AGY discovery and were terminated; neither is a pass.
- Python dependencies: `requirements.txt`; CI uses unittest and Node tests. No project Python lint/type configuration or installed coverage tool was found. There are no linked repositories.

Complexity: 4/5. One writer. Independent checker has read/test access only. No new runtime dependencies or provider calls. The budget tracker remains an in-process primitive; repairing it does not prove complete host mediation or cancellation of running tools.

## File boundary

- Runtime: `agyos_decision/state_ledger.py`, `agyos_decision/skills_router.py`.
- Tests: `scripts/tests/test_budget_hardening.py`, `scripts/tests/test_routing_contract.py`, `scripts/tests/test_state_recovery.py`, `scripts/tests/test_skill_routing.py`, `scripts/tests/test_hooks_authorizer.py`.
- Measurement: `scripts/benchmark_decision.py`, `docs/research/evidence/optimization-*.json`.
- Documentation: this plan, `docs/research/OPTIMIZATION_RESEARCH.md`, `docs/OPTIMIZATION_PROMPT.md`, `docs/OPTIMIZATION_RESULTS.md`, `docs/adr/0002-budget-and-routing-contracts.md`, `docs/adr/README.md`, `README.md`, `AI_HANDOFF.md`.
- Governance: `.agents/state/state.json`, `.agents/state/CURRENT.md`, `.agents/state/checkpoints/research-led-optimization.md`.

## Implementation and verification

1. Freeze small failing cases for budget integrity, failed graph insertion, JSON transport, and real manifest fallback. Establish routing timing and output baselines.
2. Validate finite, nonnegative numeric inputs; preserve decimal USD charges with exact accounting; enforce elapsed monotonic time and reserved tool capacity. Preserve public numeric read access and existing call signatures. Accept only verification/rollback reserve purposes. These labels are not authentication. Independent review identified ambient decimal precision as a bypass, so the final arithmetic uses Fraction after Decimal parsing; see ADR 0002.
3. Validate graph insertions before replacing maps. Reject duplicate IDs and negative/noninteger depths without partial mutation; preserve forward dependency registration and explicit cycle validation.
4. Keep internal routing indexes out of public candidate dictionaries. Trial bounded top-k selection only if repeated measurements support it and ranking stays identical.
5. Bound the existing installed-host subprocess test so a stalled host reports failure. Do not remove or skip its assertions.
6. Run targeted unittest regressions, full unittest discovery, Node crypto/MCP suites, Bun council tests, Python syntax, generated-catalog reproducibility, shell/state checks, secret scan, and diff review. Use bounded timeouts for host-dependent checks. Run an independent review of contracts and measurements.

Commands:

```bash
python3 -m unittest scripts.tests.test_budget_hardening scripts.tests.test_routing_contract scripts.tests.test_state_recovery scripts.tests.test_skill_routing -v
python3 scripts/benchmark_decision.py --repeats 30 --output /tmp/agyos-routing.json
timeout 180s python3 -m unittest discover -s scripts/tests -v
node --test scripts/tests/test_secure_envelope.cjs scripts/tests/test_private_vault.cjs scripts/tests/test_mcp_protocol.cjs
bun test --cwd scripts/council
python3 -X pycache_prefix=/tmp/agyos-optimization-bytecode -m compileall -q agyos_decision scripts/tests scripts/benchmark_decision.py
git diff --check
```

Stop after two identical failures; inspect the cause instead of repeating. Limit performance search to baseline plus one top-k variant, two repetitions, zero provider spend. No timing thresholds in CI. Revert only this task's rejected variant. Changes to documented budget rejection behavior are intentional; valid existing requests must keep working.
