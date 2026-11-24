# Changelog

All notable changes to the **AGYOS** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.0] - 2026-11-24

### Added
- Standardized monorepo layout conforming strictly to global engineering standards (`backend/`, `frontend/`, `deploy/`, `docs/`, `scripts/`, `assets/`, `.github/`).
- Modern FastAPI backend powered strictly by `uv` exposing `/health`, `/v1/skills`, `/v1/roles`, `/v1/decide`, and `/v1/intent`.
- Next.js 15+ App Router frontend with React 19 and Tailwind CSS v4 for Cloudflare Pages deployment at `agyos.pages.dev`.
- GitHub community and governance templates: `bug_report.yml`, `feature_request.yml`, `config.yml`, `PULL_REQUEST_TEMPLATE.md`, `CODEOWNERS`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `FUNDING.yml`, and `copilot-instructions.md`.
- Automated CodeQL static security analysis workflow (`.github/workflows/codeql.yml`).
- Root unified `Makefile` for developer commands (`make dev`, `make test`, `make build`, `make lint`, `make typecheck`, `make clean`).
- Cross-IDE configuration in `.editorconfig`.

### Changed
- Standardized Cloudflare deployment workflow to `.github/workflows/deploy.yml`.
- Relocated deployment manifests (`Dockerfile`, `docker-compose.yml`, `.dockerignore`) into `deploy/docker/`.
- Consolidated root documentation (`DEPLOYMENT.md`, `CITATION.cff`, `AI_HANDOFF.md`) into `docs/`.
- Relocated `SECURITY.md` to `.github/SECURITY.md`.
- Consolidated Python dependencies into `backend/pyproject.toml` managed by `uv`.

### Removed
- Retired legacy root `requirements.txt`.
- Closed and deleted remote Dependabot branches on `origin`, enforcing strict single-branch (`main`) discipline.

## [3.1.0] - 2026-11-22

### Added
- Native Cloudflare deployment pipeline for documentation and edge routing.
- Adversarial security scanning via Strix runner and gitleaks integration.
- Expanded enterprise 104-role organization across 12 departments and 5 seniority tiers (L4-L8).
- Multi-model deliberation panel with Agent Council (`agyos council`).

### Changed
- Refactored skill definitions to Token-Oriented Object Notation (TOON) format.
- Optimized query compiler and KV-cache prompt alignment in `agyos_decision`.

## [3.0.0] - 2026-11-20

### Added
- Initial release of 13-crate Rust ACID storage engine (`crates/store`) with write-ahead log (WAL), transactional outbox, and disk fence.
- Hosted worker pool (`apps/worker`) with fair admission and lease management.
- 5-Gate autonomous engineering lifecycle (`UNDERSTAND`, `ANALYZE`, `PLAN`, `IMPLEMENT`, `VERIFY`).
- 2,289-skill catalog with on-demand runbook retrieval.

[3.2.0]: https://github.com/krishujeniya/AGYOS/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/krishujeniya/AGYOS/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/krishujeniya/AGYOS/releases/tag/v3.0.0
