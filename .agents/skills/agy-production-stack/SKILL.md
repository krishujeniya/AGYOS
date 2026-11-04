---
name: agy-production-stack
description: Master runbook for production-grade, free-first AI engineering setups using AGY CLI exclusively. Covers environment audits, MCP server wiring, specialist skill catalog routing, Supabase/Vercel/Cloudflare integration, free-tier cost controls, and automated verification.
---

# AGY Global Production Engineering Setup

A discipline and runbook for establishing and maintaining a production-grade, free-first AI development environment using AGY CLI (Antigravity) exclusively as the coding agent.

## Non-Negotiable Invariants

1. **Free-First Priority**: Prioritize genuinely free and open-source solutions. Never create paid resources, enable automatic billing, or exceed free-tier boundaries without explicit authorization.
2. **AGY-Native**: Rely exclusively on Antigravity CLI (`agy`). Do not install, invoke, or depend on Codex or Claude Code.
3. **Idempotence & Safety**: Never overwrite existing configurations without backups. Never use blind `curl | bash`.
4. **Machine Evidence Required**: Every verification step must execute real commands and report actual exit codes (PASS, FAIL, SKIPPED, or AUTH REQUIRED).

---

## Phase 1: Environment Audit

Execute system discovery before applying any changes:
1. **OS & Kernel**: Check distribution (`cat /etc/os-release`), architecture (`uname -m`), kernel release.
2. **Resources**: Inspect CPU (`nproc`), RAM (`free -h`), disk space (`df -h /`), GPU availability (`nvidia-smi`).
3. **Toolchains**: Verify versions of Node.js (`node -v`), npm, Bun, Python (`python3 --version`), `uv`, Git, GitHub CLI (`gh`), Vercel CLI (`vercel`), Supabase CLI (`supabase`), and Wrangler (`wrangler`).
4. **AGY Configuration**: Inspect `agy --version`, `agy mcp list`, `agy plugin list`, and `~/.gemini/config/mcp_config.json`.

---

## Phase 2: Production Skill Routing

Route development tasks to the appropriate specialist runbooks within AGY:

### 2.1 Frontend & UI/UX
- **Next.js & React**: `nextjs-best-practices`, `nextjs-app-router-patterns`, `react-performance`.
- **Styling & Tokens**: `tailwind-design-system`, `design-system-architect`, `radix-ui-design-system`.
- **Animation & Polish**: `emil-design-eng` (concentric border radii, frequency-based timing, transform/opacity only), `high-end-visual-design`.
- **Accessibility**: `frontend-a11y`, `wcag-audit-patterns`.

### 2.2 Backend & APIs
- **FastAPI / Python**: `fastapi-pro`, `fastapi-router-py`, `pydantic-models-py`.
- **Node.js / Edge**: `nodejs-backend-patterns`, `hono`, `bun-development`.
- **API Contracts**: `api-design-principles`, `api-security-best-practices`, `auth-implementation-patterns`.
- **Queues & Jobs**: `bullmq-specialist`, `trigger-dev`.

### 2.3 Databases & Storage
- **Postgres & Supabase**: `postgres-best-practices`, `supabase-postgres-best-practices`, `nextjs-supabase-auth`.
- **Schema & Migrations**: `architecture-database-design`, `drizzle-orm-expert`, `prisma-expert`, `database-migrations-sql-migrations`.

### 2.4 DevOps & Cloud
- **Hosting & Edge**: `vercel-deployment`, `cloudflare-workers-expert`.
- **CI/CD & Workflows**: `github-actions-templates`, `github-workflow-automation`.
- **Secrets & Validation**: `secrets-management`, `varlock`, `deployment-validation-config-validate`.

### 2.5 Security & Vulnerability Analysis
- **Audits**: `security-review`, `top-web-vulnerabilities`, `differential-review`.
- **Threat Modeling**: `stride-analysis-patterns`, `skill-audit`.

### 2.6 Testing & Verification
- **Test-Driven Development**: `test-driven-development`, `tdd-workflows-tdd-cycle`, `verification-loop`.
- **Browser Automation**: `playwright-skill`, `browser-qa`.
- **Performance Profiling**: `benchmark-optimization-loop`, `k6-load-testing`.

### 2.7 AI Engineering & MLOps
- **Pipelines & Evaluation**: `agentic-engineering`, `eval-harness`, `mle-workflow`.
- **RAG & Search**: `rag-implementation`, `embedding-strategies`, `hugging-face-cli`.

---

## Phase 3: Model Context Protocol (MCP) Management

Manage MCP servers via the native AGY CLI:

1. **Global Core MCPs**:
   - `anchor`: AGYOS state daemon and skill discovery engine.
   - `context7`: Direct documentation lookup (`context7-mcp` via `@upstash/context7-mcp`).
2. **Project-Scoped MCPs**:
   - PostgreSQL: `agy mcp add postgres npx -y @modelcontextprotocol/server-postgres "<CONN_URI>"`
   - GitHub: `agy mcp add --env GITHUB_PERSONAL_ACCESS_TOKEN="<PAT>" github npx -y @modelcontextprotocol/server-github`
   - Supabase: `agy mcp add --env SUPABASE_ACCESS_TOKEN="<TOKEN>" supabase npx -y @supabase/mcp-server-supabase`
   - Cloudflare: `agy mcp add --env CLOUDFLARE_API_TOKEN="<TOKEN>" --env CLOUDFLARE_ACCOUNT_ID="<ID>" cloudflare npx -y @cloudflare/mcp-server-cloudflare`
   - Playwright: `agy mcp add playwright npx -y @executeautomation/playwright-mcp-server`
   - Vercel: `agy mcp add vercel https://mcp.vercel.com`

---

## Phase 4: Full-Stack Integration Workflows

### 4.1 Supabase Workflow
1. Initialize local configuration: `supabase init`.
2. Generate TypeScript types:
   ```bash
   supabase gen types typescript --local > types/supabase.ts
   ```
3. Create idempotent migrations: `supabase migration new <name>`.
4. Enforce Row-Level Security (RLS) on all exposed tables. Never expose `service_role` keys in client-side code.

### 4.2 Vercel Workflow
1. Run local dev server with Vercel environment: `vercel dev`.
2. Pull safe environment variables: `vercel env pull .env.local`.
3. Pre-build validation: `vercel build`.
4. Deploy preview builds: `vercel deploy --prebuilt`.

---

## Phase 5: Free-Tier Financial Governance

1. Never enable automatic plan upgrades or unmetered credit card billing.
2. Default to local test fixtures, SQLite, or ephemeral in-memory databases before calling metered cloud APIs.
3. Observe provider limits:
   - Vercel: 100 GB bandwidth / month (Hobby).
   - Supabase: 500 MB database, pauses after 7 days of inactivity.
   - Cloudflare: 100,000 Worker requests / day.
   - GitHub: 2,000 runner minutes / month.

---

## Phase 6: Automated Verification Loop

Before concluding any setup or milestone, execute the verification suite:
1. `agy --version` (AGY startup)
2. `agy mcp list` (MCP discovery)
3. `context7-mcp` handshake (JSON-RPC 2.0 initialize)
4. `NODE_PATH=$(npm root -g) node -e 'require("playwright").chromium.launch({ headless: true }).then(b => b.close())'` (Browser automation)
5. `gh auth status` (GitHub CLI auth)
6. `vercel whoami` (Vercel CLI auth)
7. `uvx ruff check . && uvx pytest && uvx mypy` (Python test suite)
