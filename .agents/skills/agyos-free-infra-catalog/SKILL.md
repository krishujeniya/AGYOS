---
name: agyos-free-infra-catalog
description: Curated architectural guide to zero-cost developer infrastructure. Covers free tiers for hosting, serverless Postgres, vector databases, authentication, object storage, and background queues.
---

# AGYOS Free Tier Developer Infrastructure Guide

An architectural decision playbook for selecting and composing zero-cost developer infrastructure for early-stage software, MVPs, and production side-projects.

## 1. Zero-Cost Infrastructure Directory

Curated providers offering reliable free-tier allowances without requiring upfront credit card lock-in:

### Compute & Hosting
- Cloudflare Pages / Workers: Unlimited static requests, 100k free worker invocations/day, global edge network.
- Vercel: Free tier for personal Next.js and frontend projects with serverless API functions.
- Fly.io / Railway / Render: Starter instances suitable for lightweight API services and background workers.

### Databases & State
- Neon Postgres: Serverless PostgreSQL with 0.5 GB storage, instant branching, and connection pooling.
- Supabase: Managed Postgres with 500 MB database, built-in Auth, Row Level Security, and realtime websockets.
- Cloudflare D1: Serverless SQLite with 5M reads/day and 100k writes/day.
- Upstash Redis: Serverless Redis with 10k commands/day, ideal for rate-limiting and session caches.

### Object Storage & CDN
- Cloudflare R2: 10 GB free storage/month with 0 egress fees (S3-compatible API).
- Supabase Storage: 1 GB free bucket storage for user uploads and media.

### Authentication & Identity
- Clerk: Generous free tier for modern React/Next.js authentication and user management.
- Supabase Auth: Complete email/password and OAuth provider integration out of the box.

### Messaging & Background Jobs
- Upstash QStash: Serverless HTTP-based message queue and cron scheduler for async task dispatch.
- Inngest: Event-driven background functions with automatic retries and step execution.

### CI/CD & Observability
- GitHub Actions: 2,000 free runner minutes/month for automated tests, linting, and build validation.
- Sentry: Developer plan with 5,000 free error events/month for exception telemetry.
- Axiom: Free tier for centralized JSON log ingestion and query analytics.

## 2. Recommended Zero-Cost Stacks

### Stack A: Next.js SaaS MVP
- Frontend & Hosting: Vercel or Cloudflare Pages.
- Database: Neon Serverless Postgres (Prisma / Drizzle ORM).
- Authentication: Clerk or Supabase Auth.
- Storage: Cloudflare R2.
- Total Monthly Cost: $0.00.

### Stack B: Python / FastAPI Microservice
- Backend Hosting: Render / Fly.io free tier.
- Database: Supabase managed Postgres.
- Caching & Rate Limiting: Upstash Redis.
- Monitoring: Sentry free tier.
- Total Monthly Cost: $0.00.
