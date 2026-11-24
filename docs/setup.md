# AGYOS Developer Setup Guide

This guide details setting up the AGYOS development environment, toolchain prerequisites, and local commands.

## Prerequisites

- **Linux / macOS**: Modern POSIX shell environment.
- **Node.js**: `v22+` (or `v24+`).
- **Python Tooling (`uv` Only)**: Install `uv` via `curl -LsSf https://astral.sh/uv/install.sh | sh`. Raw `python` and `pip` are prohibited by project invariants.
- **Git**: Configured for maintainer profile:
  ```bash
  git config user.name "Krish Ujeniya"
  git config user.email "100012208+krishujeniya@users.noreply.github.com"
  ```

---

## Quickstart

### 1. Clone & Verify Working Copy
```bash
git clone https://github.com/krishujeniya/AGYOS.git
cd AGYOS
git status
```

### 2. Backend Setup (`uv` Only)
```bash
cd backend
# Sync virtual environment and install dependencies
uv sync
# Verify syntax
uv run python -m py_compile app/main.py
cd ..
```

### 3. Frontend Setup (Next.js 15+)
```bash
cd frontend
npm install
npm run typecheck
cd ..
```

---

## Unified Makefile Targets

```bash
# Fast test suite
make test

# Type checking across frontend and backend
make typecheck

# Production builds
make build

# Clean temporary caches
make clean
```

---

## Cloudflare Deployment

AGYOS deploys natively to the Cloudflare ecosystem:
- **Frontend Portal**: Cloudflare Pages (`agyos.pages.dev`).
- **Backend API Gateway**: Cloudflare Workers (`api.agyos.workers.dev`).
See [`docs/deployment.md`](deployment.md) for full deployment details.
