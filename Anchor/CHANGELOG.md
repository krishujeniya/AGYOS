# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-25

### Added
- One-command initialization via `npx anchor-agent init` (D2).
- GitHub Action (`uses: krishujeniya/Anchor@main`) for CI pipelines (D2).
- Native bridge generation for Cursor (`.cursor/rules/anchor.mdc`) and Claude Code (`.claude.json`) (D3).
- MCP Server implementation finished with `anchor_state`, `anchor_checkpoint`, and `anchor_verify` tools (D3).
- `tests/eval.bats` meta-verification test for `eval.sh` (D1).
- Nightly Chaos GitHub Action pipeline (`anchor-nightly-chaos.yml`) (D1).
- Spec Kit interop guide (`SPEC_KIT_INTEROP.md`) and Feature Comparison guide (`COMPARISON.md`) (D4).
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and GitHub Issue/PR templates (D5).

### Changed
- Complete rewrite of `README.md` as a landing page with headline metrics and comparison table (D4).
- CI is now strict: removed `|| true` suppressions from lint steps in `anchor-verify.yml` (D1).

### Fixed
- Fixed silent failures in `eval.sh` Phase 2 (Checkpoint Regression) by replacing process substitution (D1).
- Added explicit archive directory creation (`checkpoints/archive/`) to `init.sh` to prevent fresh clone failures (D1).

## [1.1.1] - 2026-07-25

### Fixed
- Fixed `eval.sh` reporting false positives by properly handling `null` default asserts in `state-validate.sh` (N-1).
- Fixed `verify.sh` fail-open behavior caused by process substitution in restricted environments (N-2).
- Fixed `.github/workflows/anchor-verify.yml` to enforce CI failures by removing `|| true` and ensuring `jq` is installed (N-4, N-12).
- Fixed `rollback.sh` to safely stash and commit WIP changes to a rescue branch before executing destructive commands (N-3).
- Added `bwrap`/`firejail`/`docker` checking to `sandbox-run.sh` to prevent false confidence in isolation (N-9).
- Standardized `token_budget` to `50000` across `init.sh` and `state-validate.sh` (N-7).
- Documented `last_known_commit_COMPACT` as the target for `IMPLEMENT` gate rollbacks (N-10).
- Fixed the Test Ratchet rule to calculate assertion counts instead of blocking simple code refactoring (N-6).
- Added an `ANCHOR_HUMAN=1` bypass for the `gate-check.sh` pre-commit hook (N-5).
- Restored repo hygiene by removing `Need.md` from the root, untracking `telemetry.jsonl`, and deduplicating `TRIAL_REGISTRY.md` (N-8).
- Added a `golden_checkpoint.md` fixture and `tests/state.bats` MCP smoke test (N-13, N-14).
- Normalized the "5-gate workflow" taxonomy across all files (N-11).

## [1.1.0] - 2026-07-25

### Added
- Phase 1: Rollback rescue hooks, drift detection, and dashboard security.
- Phase 2: Unified 5-Gate terminology, updated documentation, and CI badges.
- Phase 3: Added Agent Skills spec fields to SKILL.md and automated AGENTS.md linking.
- Phase 4: Deterministic git pre-commit hook (`gate-check.sh`), test ratchet, TDD gate, state file locking, and `sandbox-run.sh`.
- Phase 5: CI hardening (`shellcheck`, `bats`), and Chaos Trial CT-004.
- Phase 6: Subagent isolation contracts, IDE-agnostic adapters, granular checkpoints, structured COMPACT handoffs, and MCP Server.

### Fixed
- Fixed drift-check blind spot for untracked files.
- Fixed dashboard binding to expose only on `127.0.0.1`.
- Purged stale `.agents/state/decisions/drafts` files.
