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

### 2. Python Runtime & Dependencies (`uv` Only)
```bash
# Install pinned script dependencies via uv
uv pip install --system -r gemini/scripts/requirements.txt
# Verify syntax
uv run python -m py_compile gemini/agyos_decision/catalog.py
```

### 3. Static Frontend & Docs Verification
```bash
# Check frontend script syntax
node --check frontend/site.js
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

AGYOS deploys its static documentation and skill catalog portal to Cloudflare Pages:
- **Frontend Portal**: Cloudflare Pages (`agyos.pages.dev`, configured via `wrangler.jsonc` and `.github/workflows/deploy.yml`).
See [the deployment guide](deployment.md) for full deployment details.
