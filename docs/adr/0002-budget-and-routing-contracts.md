# ADR 0002: Preserve accounting precision and public routing contracts

Date: 2026-11-11. Status: accepted for the operator-authorized local optimization.

## Context

`RunBudgetTracker` rounded every charge to cents and accepted negative usage; 1,000 charges of $0.001 left a $0.00 ledger. Its reserve-purpose argument and elapsed-time budget were unenforced. Routing cached sets for performance, then exposed them in fallback and integration candidates, breaking JSON transport. Failed graph insertion could partially update a parent's child list.

## Decision

Parse USD through `Decimal(str(value))`, then use standard-library `Fraction` arithmetic for exact accounting. This preserves small decimal charges without inheriting caller decimal precision or rounding traps. Expose float read views for existing callers while enforcing money limits using the exact ledger; those views may round amounts below float resolution. Require nonnegative integer counts and finite nonnegative amounts. Check a monotonic clock on each charge; reserve time and tool capacity alongside tokens and USD. Preserve the reserve call's positional arguments and add optional keyword tool usage. Only verification/rollback purpose labels are valid; they are not authenticated authorization.

Construct public candidates from explicit fields. Validate all graph dependencies before publishing replacement maps, rejecting duplicate task IDs and invalid depths. Keep explicit cycle validation and forward dependency registration.

## Alternatives and consequences

- Cent rounding loses small model charges. Binary float accumulation introduces boundary drift. Decimal arithmetic alone depends on the active precision context and can silently discard tiny charges. Exact rational arithmetic adds small accounting overhead and no package dependency. No accounting speedup is claimed.
- A persistent concurrent reservation service could enforce shared budgets across workers, but no inspected dispatch caller requires that architecture here. This tracker remains single-owner and in-process, and cannot stop an already-running tool.
- A JSON encoder that converts sets would hide the interface leak and expose unnecessary metadata. Explicit response fields preserve the existing public structure.
- Deep-copying the whole graph on every insert is unnecessary for these changes. Replace top-level maps and only the changed child lists after validation; existing entries are preserved.
- Valid counts and existing calls remain compatible. Fractional/boolean/negative counts, nonfinite amounts, unrecognized reserve purposes, duplicate task IDs, and charges after deadlines now fail intentionally. `used_usd` is a read-only numeric view; direct writes to accounting internals are unsupported.

## Verification

`scripts/tests/test_budget_hardening.py`, `scripts/tests/test_routing_contract.py`, and the added graph regressions exercise these boundaries. See [executed results](../OPTIMIZATION_RESULTS.md) for measurements, independent review, and limitations. No host-enforcement claim follows from these unit tests.
