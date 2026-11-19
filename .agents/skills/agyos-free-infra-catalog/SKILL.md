---
name: agyos-free-infra-catalog
description: Curated architectural guide to zero-cost developer infrastructure. Covers free tiers for hosting, serverless Postgres, vector databases, authentication, object storage, and background queues.
prompt-source: prompt.toon
---
skill: "agyos-free-infra-catalog"
sections[13]:
  - "\n"
  - "# AGYOS Free Tier Developer Infrastructure Guide\n\nAn architectural decision playbook for selecting and composing zero-cost developer infrastructure for early-stage software, MVPs, and production side-projects.\n\n"
  - "## 1. Zero-Cost Infrastructure Directory\n\nCurated providers offering reliable free-tier allowances without requiring upfront credit card lock-in:\n\n"
  - "### Compute & Hosting\n- Cloudflare Pages / Workers: Unlimited static requests, 100k free worker invocations/day, global edge network.\n- Vercel: Free tier for personal Next.js and frontend projects with serverless API functions.\n- Fly.io / Railway / Render: Starter instances suitable for lightweight API services and background workers.\n\n"
  - "### Databases & State\n- Neon Postgres: Serverless PostgreSQL with 0.5 GB storage, instant branching, and connection pooling.\n- Supabase: Managed Postgres with 500 MB database, built-in Auth, Row Level Security, and realtime websockets.\n- Cloudflare D1: Serverless SQLite with 5M reads/day and 100k writes/day.\n- Upstash Redis: Serverless Redis with 10k commands/day, ideal for rate-limiting and session caches.\n\n"
  - "### Object Storage & CDN\n- Cloudflare R2: 10 GB free storage/month with 0 egress fees (S3-compatible API).\n- Supabase Storage: 1 GB free bucket storage for user uploads and media.\n\n"
  - "### Authentication & Identity\n- Clerk: Generous free tier for modern React/Next.js authentication and user management.\n- Supabase Auth: Complete email/password and OAuth provider integration out of the box.\n\n"
  - "### Transactional Email & Messaging\n- Resend: 3,000 emails/month free for transactional authentication and notifications.\n- Postmark / SendGrid: 100 emails/day developer tier.\n- Upstash QStash: Serverless HTTP-based message queue and cron scheduler for async task dispatch.\n- Inngest: Event-driven background functions with automatic retries and step execution.\n\n"
  - "### Search & Vector Indices\n- Pinecone: 1 free serverless index with 2GB storage for vector embeddings.\n- Algolia: 10,000 search requests/month free tier.\n\n"
  - "### Code Quality, Security & DNS\n- Cloudflare DNS: Free global authoritative DNS with DDoS mitigation and automatic TLS.\n- Semgrep: Free CLI and community rules for SAST scanning in GitHub Actions.\n- Sentry: Developer plan with 5,000 free error events/month for exception telemetry.\n- Axiom: Free tier for centralized JSON log ingestion and query analytics.\n- GitHub Actions: 2,000 free runner minutes/month for automated tests and build validation.\n\n"
  - "## 2. Recommended Zero-Cost Stacks\n\n"
  - "### Stack A: Next.js SaaS MVP\n- Frontend & Hosting: Vercel or Cloudflare Pages.\n- Database: Neon Serverless Postgres (Prisma / Drizzle ORM).\n- Authentication: Clerk or Supabase Auth.\n- Storage: Cloudflare R2.\n- Total Monthly Cost: $0.00.\n\n"
  - "### Stack B: Python / FastAPI Microservice\n- Backend Hosting: Render / Fly.io free tier.\n- Database: Supabase managed Postgres.\n- Caching & Rate Limiting: Upstash Redis.\n- Monitoring: Sentry free tier.\n- Total Monthly Cost: $0.00.\n"
