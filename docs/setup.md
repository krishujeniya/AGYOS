# AGYOS Developer Setup Guide

This guide details setting up the AGYOS development environment and local commands.

---

## One-Line Install (`~/.gemini`)

Sync `AGYOS/gemini/` (`config/` and `antigravity-cli/`) directly into `~/.gemini/` (with automatic timestamped backup):

```bash
curl -fsSL https://raw.githubusercontent.com/krishujeniya/AGYOS/main/gemini/antigravity-cli/builtin/scripts/install.sh | bash
```

Or from a local clone:

```bash
make install
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
# Verify Python syntax across decision kernel and scripts
uv run --with-requirements gemini/antigravity-cli/builtin/scripts/requirements.txt python -m compileall gemini/antigravity-cli/builtin/agyos_decision gemini/antigravity-cli/builtin/scripts
```

### 3. Static Frontend & Docs Verification
```bash
# Check frontend script syntax
node --check frontend/site.js
```

---

## Unified Makefile Targets

```bash
# Build static frontend and serve locally on http://127.0.0.1:8000
make dev

# Fast test suite
make test

# Syntax and bytecode checks across Python and frontend JS
make typecheck

# Git whitespace hygiene and JS syntax checks
make lint

# Build static frontend bundle into frontend/
make build

# Install AGYOS/gemini into ~/.gemini (with timestamped backup)
make install

# Clean temporary caches and generated frontend/ artifacts
make clean
```

---

## Cloudflare Deployment

AGYOS deploys its static documentation and skill catalog portal to Cloudflare Pages:
- **Frontend Portal**: Cloudflare Pages (`agyos.pages.dev`, configured via `wrangler.jsonc` and `.github/workflows/deploy.yml`).
See [the deployment guide](deployment.md) for full deployment details.
