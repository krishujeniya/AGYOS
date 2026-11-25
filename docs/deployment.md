# Deployment Guide — AGYOS

> Operational Runbook for Production Deployment, Health Verification, and Rollbacks.
> Standardized across the project suite in conformance with deployment engineering patterns.

---

## 1. Architecture & Production Topology

**Application Type**: Autonomous Agent Operating System & Skills Knowledge Engine

### Declared Service Topology
- **`agyos_engine`**: Multi-stage Python `3.12.9-slim-bookworm` container that builds the static documentation and skill catalog portal via `build_docs_site.py` and serves it on port `8080` as a non-root user (`agyos`, uid `1001`).

All container services are orchestrated via `deploy/docker/docker-compose.yml` with isolated bridge networking (`agyos-net`), health checks, and layer-cached multi-stage builds (`deploy/docker/Dockerfile`).

### Automated CI/CD Pipelines
- **Cloudflare Pages (`.github/workflows/deploy.yml`)**: Automatically builds `_site/` with `mistune` and deploys to `agyos.pages.dev` on pushes to `main` (when `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets are configured).
- **Container Registry (`.github/workflows/docker-publish.yml`)**: Builds and publishes container images to GitHub Container Registry (`ghcr.io/krishujeniya/agyos`).

---

## 2. Environment Configuration

Supply environment variables via a secure `.env` file (or CI/CD secrets manager). Never commit plaintext credentials to Git.

### Key Environment Variables
- `PORT (default 8080)`

---

## 3. Deployment Procedures

### Method A: Single-Host / VPS Deployment (Docker Compose)

1. **Clone repository on host**:
   ```bash
   git clone https://github.com/krishujeniya/AGYOS.git
   cd AGYOS
   ```

2. **Start stack in detached mode**:
   ```bash
   docker compose -f deploy/docker/docker-compose.yml up -d --build
   ```

3. **Verify container health and logs**:
   ```bash
   docker compose -f deploy/docker/docker-compose.yml ps
   docker compose -f deploy/docker/docker-compose.yml logs -f
   ```

### Method B: Pre-built Container Registry Deployment (GHCR)

Pre-built multi-stage production images are published automatically via GitHub Actions:
```bash
docker pull ghcr.io/krishujeniya/agyos:latest
docker run -d --restart unless-stopped -p 8080:8080 ghcr.io/krishujeniya/agyos:latest
```

### Method C: Cloudflare Free Stack Deployment (CLI)

Deploy static documentation to Cloudflare Pages and configure edge bindings via Wrangler CLI:
```bash
# Build and deploy _site directory to Cloudflare Pages
uv run --with mistune python gemini/antigravity-cli/builtin/scripts/build_docs_site.py --out _site --base /
wrangler pages deploy _site --project-name=agyos

# Verify D1 and KV bindings status
wrangler d1 info shared-production-db
wrangler kv namespace list
```

---

## 4. Health Check & Readiness Probes

### Verification Command
Run the designated health check probe to confirm operational readiness:
```bash
curl -f https://agyos.pages.dev/
```

Expected HTTP Response: `200 OK`

---

## 5. Rollback Procedures

If an anomaly, regression, or service failure is detected:

### Step 1: Immediate Container Rollback
Roll back immediately to the previous immutable release tag or SHA:
```bash
# Pull previous known healthy SHA tag
docker pull ghcr.io/krishujeniya/agyos:sha-<previous-commit-sha>

# Or revert compose to previous git revision
git checkout <previous-stable-tag>
docker compose -f deploy/docker/docker-compose.yml up -d
```

### Step 2: Verification
Re-run the health probe to confirm traffic restoration:
```bash
curl -f http://localhost:8080/
```

---

## 6. Pre-Flight & Post-Flight Quality Gates

Follow the 4-phase verification protocol before declaring a release complete:

- [ ] **Code Quality**: Static inspection passed; zero lint or AST warnings.
- [ ] **Build Reproducibility**: Container builds cleanly via multi-stage isolation without dev dependencies.
- [ ] **Environment Validation**: All required environment variables present; secrets injected via secrets manager.
- [ ] **Safety & Probes**: Healthcheck endpoints respond with `200 OK`; rollback target verified.
