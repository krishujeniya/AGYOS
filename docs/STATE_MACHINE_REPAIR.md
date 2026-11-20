# AGYOS state machine repair queue

This document tracks the implicit workflow state machines found in the runtime
audit and their repair status. Statuses describe code changes only; checks remain
pending until GitHub Actions runs them.

## Repair order

| # | State machine | Main implementation | Audit finding | Status |
|---|---|---|---|---|
| 1 | AGYOS gate progression | `bin/agyos`, `bin/state.sh` | Arbitrary gate names and jumps were accepted; fast path overwrote complexity and skipped ANALYZE; the generic state setter could bypass the transition graph. | Implemented; CI pending |
| 2 | Outbox and Saga recovery | `agyos_decision/state_ledger.py` | Terminal outbox states could be overwritten; Saga accepted steps after rollback and could retry a failed compensation. | Implemented; CI pending |
| 3 | GitHub epic coordination | `scripts/agyos-runtime/lib/github-coordination/` | Status axes accepted arbitrary values; blocked/dependency paths could be bypassed; publication lacked source-state checks; concurrent callers sharing one store could double-claim. | Implemented with transition, dependency, publication, and same-host per-issue lock guards; CI pending |
| 4 | State-file repair | `bin/state-validate.sh` | Repair flag and destructive reinitialization had no validated state schema or explicit recovery result; jq execution errors could be mistaken for corrupt input. | Implemented with schema recovery and tool-error preservation; CI pending |
| 5 | Work-item lifecycle and GitHub sync | `scripts/agyos-runtime/work-items.js`, `lib/control-pane/work-item-mutations.js` | Statuses use a declared vocabulary; claims require an active result state; terminal records cannot be moved or upserted back into active states; stale pruning is skipped if a GitHub listing reaches its limit and local edits remain protected. | Implemented; CI pending |
| 6 | Installer, repair, update, and uninstall | `scripts/agyos-runtime/install-guided.js`, `lib/install-lifecycle.js`, `auto-update.js`, `lib/nasiko-release.js` | Guided install, repair, uninstall, and auto-update validate distinct result vocabularies; Nasiko lifecycle locking recovers dead local owners and publication removes its own partial receipt and binary on failure. CI cases cover rollback and lock behavior. | Implemented; CI pending |
| 7 | Plan Canvas session | `scripts/agyos-runtime/lib/plan-canvas/sessions.js` | Transitions are constrained to new/open/feedback/ended; ended sessions reject late agent replies at the store and return HTTP 409. User-ended attribution remains sticky and reopening requires the existing explicit flag. | Implemented; CI pending |
| 8 | Council dispatch | `scripts/council/src/council.ts` | Configured retry counts are honored; each stage persists complete, grace-expired, or quorum-failed status with quorum counts. | Implemented; CI pending |
| 9 | Hook dispatch | `scripts/agyos-runtime/hooks/bash-hook-dispatcher.js` and post-tool dispatcher | Bash reports skipped/continued/stopped/failed; PostToolUse reports skipped/dry-run/continued/failed. Existing fail-open and continue behavior is retained. | Implemented; CI pending |
| 10 | Observer and host session lifecycle | `scripts/agyos-runtime/lib/observer-sessions.js`, session hooks | Lease writes are atomic; lease registration/removal and shutdown serialize through an owner-tagged lock file. Dead local main-lock owners are reclaimed. A process killed during stale-lock recovery leaves a fail-closed guard for operator inspection. Session end explicitly selects skip/create/update and empty/mechanical/LLM summary outcomes. | Implemented with documented recovery boundary; CI pending |
| 11 | Release approval | `scripts/agyos-runtime/release-approval-gate.js` | Decision rows now accept a declared vocabulary; unknown states and conflicting duplicate rows fail closed. | Implemented; CI pending |

## Related explicit state or parser machines

These were found during the same scan and reviewed after the primary queue:

- Worktree lifecycle and shadow-trail replay have named states and validators;
  the CI suite now covers protection of dirty worktrees, stale/merged
  classification, and valid/duplicate shadow-trail acknowledgements.
- Hook input limits has an explicit character parser; CI covers chunk boundaries,
  top-level field selection, and nested-field exclusion.
- Orchestration session status is derived from Markdown and pane presence. It
  only reports observed state and does not drive worker lifecycle actions.

## Verification policy

Add regression cases to the repository CI suites. Do not run tests, builds,
linters, type checks, dependency resolution, setup, or rendering locally. Review
source and diffs locally, and report each Actions result against the exact
revision that CI executed. No push or deployment is implied by this queue.

## Remaining boundary

GitHub does not participate in the local issue lock. Mutations sharing a
persistent store path, or direct callers using the per-user temporary fallback,
are serialized on that host. Independent hosts using separate stores can still
race on the same issue. Cross-host mutations require a serialized operator or
job queue until coordination gains a server-side compare-and-set contract.
Process locks with a different hostname remain fail-closed because a local PID
cannot establish that a remote owner is dead. A process killed during the
short stale-lock recovery critical section can leave the `.reclaim` file. The
lock then fails closed until an operator inspects and removes that stale guard.
The independent review confirmed this as the remaining lock-recovery boundary;
it found no other transition or mutation-lock defect in the repair queue.
