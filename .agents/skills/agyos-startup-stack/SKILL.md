---
name: agyos-startup-stack
description: The 9-tool operational stack for solo founders and technical builders using AGYOS. Coordinates agent orchestration, literature research, zero-cost infra, automated lead generation, launch distribution, binary inspection, code protection, and release verification.
---

# AGYOS 9-Tool Production Startup Stack

An integrated operational stack designed for technical founders and solo builders using the AGY CLI and AGYOS cognitive architecture. It combines 9 core engineering capabilities into a cohesive, zero-speculation workflow.

## 1. The 9 Operational Subsystems

1. Agent Orchestration Engine:
   - Tooling: AGY CLI (`agy`), AGYOS 5-Gate Workflow (`bin/agyos gate`), and FastMCP State Daemon.
   - Purpose: Enforces 5-Gate lifecycle governance (UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY) and context-separated Maker/Checker execution.

2. Academic & Market Intelligence:
   - Tooling: `agyos-academic-research`, Semantic Scholar, arXiv, and SciSpace workflows.
   - Purpose: Synthesizes empirical literature, evaluates competitor claims, isolates defensible problem statements, and avoids duplicated research.

3. Zero-Cost Infrastructure Directory:
   - Tooling: `agyos-free-infra-catalog` (Neon Postgres, Supabase, Cloudflare Pages/R2, Upstash Redis).
   - Purpose: Provisions serverless compute, relational databases, object storage, and session caches without upfront infrastructure costs.

4. Content & Visual Identity System:
   - Tooling: `agyos-anti-ai-design`, tokenized CSS, vector icon suites (Lucide/Phosphor), and typography pairings.
   - Purpose: Generates high-contrast, production-grade web interfaces and social marketing cards without generic AI templates.

5. Multi-Channel Distribution & Directory Syndication:
   - Tooling: `agyos-startup-distribution`, Hacker News Show HN protocol, Product Hunt launch checklist, and targeted Subreddit engagement.
   - Purpose: Orchestrates product launches across 100+ software indexes and developer communities.

6. Headless Lead & Market Scraping:
   - Tooling: `agyos-lead-scraper`, containerized Playwright, coordinate grid traversal.
   - Purpose: Collects verified local business leads, directory contacts, and market signals with rate-limiting and deduplication.

7. Binary Analysis & Reverse Engineering:
   - Tooling: `agyos-binary-analysis`, Ghidra, Hopper, radare2, and dynamic runtime tracing.
   - Purpose: Analyzes third-party client protocols, inspects compiled binaries, and isolates technical implementation patterns.

8. Software Protection & Counter-Analysis:
   - Tooling: `agyos-software-protection`, symbol stripping, control-flow flattening, and decoy resource traps.
   - Purpose: Hardens production builds against automated decompilers and resource-exhausting AI reverse engineering.

9. Pre-Launch Verification & Telemetry:
   - Tooling: `agyos-app-launch-checklist`, Sentry exception tracking, OpenGraph metadata validation, and Lighthouse audits.
   - Purpose: Verifies production readiness, social preview cards, security headers, and search indexability before public release.

## 2. Integrated Execution Pipeline

To launch a feature or venture with the 9-tool stack:

```text
[Research & Intelligence] ──► [Architecture & Free Infra] ──► [Autonomous TDD Build]
           │                                │                              │
           ▼                                ▼                              ▼
   Literature Review              Database & Storage Setup          5-Gate Implementation
           │                                │                              │
           ▼                                ▼                              ▼
[Hardening & Protection]  ──► [Pre-Launch Verification]   ──► [Distribution & Syndication]
```
