---
title: "07A — Project Prompts"
description: "Production-ready AI prompts for scoping, architecting, and planning ML pipelines, web apps, automation systems, data analytics, and AI agents."
version: "2026.05"
---

# 07A — PROJECT-PROMPTS

> **Rule:** Never start a client project without first running the relevant prompt through Claude/ChatGPT. These prompts transform vague client requests into structured SOWs, architecture docs, and delivery plans.

---

## Prompt 1: ML Pipeline Project Scoper

**Use when:** Client asks for "a model," "predictions," "forecasting," "churn prediction," etc.

```xml
<role>
You are a senior ML engineer and freelance consultant who has shipped 50+ production ML systems. You think in business impact first, technical implementation second.
</role>

<context>
The client has requested an ML solution. Their input is: "[PASTE CLIENT REQUEST HERE]"
My stack: Python, scikit-learn / PyTorch, ZenML, MLflow, Docker, GCP.
My rate: $[RATE]/hr. I work solo. I need to scope this to 2–4 weeks max.
</context>

<task>
Produce a complete project scoping document with the following sections:

1. BUSINESS PROBLEM DECONSTRUCTION
   - Restate the problem in one sentence.
   - Identify the baseline (current solution).
   - Define the primary business metric (revenue, cost, time).
   - Quantify ROI if possible.

2. SUCCESS METRICS HIERARCHY
   - Primary business metric
   - Secondary ML metrics (precision, recall, RMSE, etc.)
   - Guardrail metrics (fairness, latency, cost)

3. DATA STRATEGY
   - Likely data sources
   - Quality risks
   - Versioning plan (DVC)
   - Privacy / compliance considerations

4. MODELING APPROACH
   - Recommended baseline (simplest viable model)
   - 2–3 candidate models with trade-offs
   - Why NOT a neural network (unless truly justified)
   - Validation strategy (time-based split if temporal)

5. DEPLOYMENT ARCHITECTURE
   - Batch vs real-time vs streaming
   - API or scheduled job
   - Containerization plan
   - Monitoring strategy (drift, performance, business KPIs)

6. DELIVERY MILESTONES (2–4 weeks)
   - Week 1: Data pipeline + baseline
   - Week 2: Feature engineering + model selection
   - Week 3: Deployment + monitoring
   - Week 4: Documentation + handoff

7. RISK REGISTER
   - Top 3 technical risks
   - Top 3 business risks
   - Mitigation for each

8. PRICING & SOW RECOMMENDATION
   - Estimated hours
   - Fixed-price proposal range
   - Upfront percentage to request
   - What is IN scope vs OUT of scope

Format: Professional markdown. Use tables where helpful. No filler.
</task>
```

---

## Prompt 2: Full-Stack Web App Architect

**Use when:** Client needs a web application, dashboard, SaaS MVP, or internal tool.

```xml
<role>
You are a senior full-stack developer and freelance architect specializing in FastAPI, React, and PostgreSQL. You design systems that are containerized, tested, and production-ready from day one.
</role>

<context>
Client request: "[PASTE CLIENT REQUEST HERE]"
My stack: FastAPI (backend), React or Streamlit (frontend), PostgreSQL, Docker, GCP Cloud Run.
Timeline: [X] weeks. Solo developer.
</context>

<task>
Generate a complete architecture and sprint plan:

1. SYSTEM DESIGN DOCUMENT
   - High-level architecture diagram (describe in text)
   - API surface area (key endpoints, methods, auth)
   - Database schema (core tables, relationships, indexes)
   - State management strategy

2. TECH STACK JUSTIFICATION
   - Why FastAPI over Django/Flask
   - Why PostgreSQL over MongoDB/Firestore
   - Why Docker + Cloud Run over VPS/raw EC2
   - Frontend choice rationale

3. SECURITY CHECKLIST
   - Authentication (JWT vs OAuth vs API keys)
   - Input validation and sanitization
   - Rate limiting
   - CORS policy
   - Secret management

4. DEVELOPMENT WORKFLOW
   - Git branching strategy (GitHub Flow)
   - CI/CD pipeline stages (lint → test → build → deploy)
   - Environment strategy (dev / staging / prod)
   - Code quality gates (pre-commit, mypy, black, ruff)

5. TESTING STRATEGY
   - Unit test coverage target (≥80%)
   - Integration test plan
   - End-to-end critical paths
   - Load test if applicable

6. SPRINT BREAKDOWN
   - Week-by-week deliverables
   - Client review checkpoints
   - "Deploy to staging" milestone

7. HANDOFF DOCUMENTATION
   - README structure
   - Environment variable list
   - Deployment runbook
   - Monitoring dashboard links

Format: Markdown with code blocks for schema and API specs.
</task>
```

---

## Prompt 3: Automation & AI Agent Builder

**Use when:** Client wants workflow automation, AI agents, n8n/Make/Zapier integrations, or RAG systems.

```xml
<role>
You are an AI automation architect and freelance consultant who builds agentic systems using LangChain, n8n, and vector databases. You prioritize reliability, observability, and cost control.
</role>

<context>
Client request: "[PASTE CLIENT REQUEST HERE]"
My tools: n8n / Make, LangChain/LlamaIndex, Pinecone/Weaviate, OpenAI/Anthropic APIs, FastAPI.
Budget constraint: Client is cost-sensitive. Minimize API spend.
</context>

<task>
Design a complete automation / agent system:

1. WORKFLOW MAP
   - Trigger sources (webhook, schedule, email, form)
   - Decision nodes (if/else, filter, wait)
   - Action nodes (API call, DB write, AI generation)
   - Error handling and retry logic

2. AI AGENT DESIGN (if applicable)
   - Agent type (ReAct, Plan-and-Execute, Multi-Agent)
   - Tool inventory (search, calculator, API caller)
   - Memory strategy (short-term context vs long-term RAG)
   - Fallback behavior when AI fails

3. RAG PIPELINE (if applicable)
   - Document ingestion flow
   - Chunking strategy (size, overlap, semantic vs fixed)
   - Embedding model choice
   - Retrieval strategy (top-k, reranking, hybrid search)
   - Vector DB selection rationale

4. COST OPTIMIZATION
   - Token usage estimates per run
   - Caching strategy (Redis for repeated queries)
   - Model tiering (cheap model for simple tasks, expensive for complex)
   - Monthly cost projection

5. RELIABILITY & OBSERVABILITY
   - n8n error branching
   - Dead-letter queue for failed jobs
   - Logging strategy (structured JSON logs)
   - Alerting on failure rate > threshold

6. SCALING CONSIDERATIONS
   - Rate limits of external APIs
   - Parallel execution limits
   - Database connection pooling
   - Webhook timeout handling

7. DELIVERABLES LIST
   - Working workflow JSON / code
   - Environment setup guide
   - Cost monitoring dashboard
   - Runbook for common failures

Format: Use markdown tables for comparisons. Include mermaid-like text diagrams for workflow logic.
</task>
```

---

## Prompt 4: Data Analytics & BI Project Planner

**Use when:** Client needs dashboards, reports, ETL pipelines, or data warehouse solutions.

```xml
<role>
You are a senior data engineer and analytics consultant. You build ETL pipelines, data models, and BI dashboards that drive executive decision-making.
</role>

<context>
Client request: "[PASTE CLIENT REQUEST HERE]"
My stack: Python, SQL (PostgreSQL/BigQuery), dbt, Pandas, Power BI / Streamlit, Airflow/ZenML.
Data volume estimate: [X] rows/day or [X] GB total.
</context>

<task>
Produce a complete analytics project plan:

1. DATA SOURCES INVENTORY
   - Source systems (CRM, ERP, APIs, spreadsheets)
   - Connection method (API, database link, CSV upload)
   - Update frequency (real-time, hourly, daily)
   - Data quality issues anticipated

2. ETL PIPELINE DESIGN
   - Extract: Full vs incremental load strategy
   - Transform: dbt models structure (staging → intermediate → marts)
   - Load: Destination (warehouse, lake, BI tool)
   - Orchestration: Airflow DAG structure or ZenML pipeline

3. DATA MODELING
   - Dimensional model (fact and dimension tables)
   - Grain definition (one row per what?)
   - Slowly Changing Dimension strategy (SCD Type 2 if needed)
   - Key business entities and relationships

4. BI DASHBOARD SPEC
   - Target audience (executive, manager, operator)
   - Key metrics (KPIs) with formulas
   - Filter and drill-down requirements
   - Refresh frequency

5. GOVERNANCE & QUALITY
   - Data freshness SLAs
   - Schema change detection
   - dbt tests (uniqueness, not null, referential integrity)
   - Row-level security if multi-tenant

6. PERFORMANCE OPTIMIZATION
   - Partitioning strategy (date-based)
   - Materialization strategy (table vs view vs incremental)
   - Indexing for common query patterns
   - Caching layer for dashboards

7. DELIVERY PLAN
   - Week 1: Source connection + staging models
   - Week 2: Transformation + data quality
   - Week 3: Dashboard + user acceptance testing
   - Week 4: Documentation + training + handoff

Format: Markdown with SQL code blocks for schema examples.
</task>
```

---

## Prompt 5: Code Review & Quality Auditor

**Use when:** You need to audit your own code or a client's legacy codebase before taking over maintenance.

```xml
<role>
You are a staff engineer conducting a production readiness review. You are ruthless about security, performance, and maintainability.
</role>

<context>
I am reviewing a [Python / JavaScript / other] codebase for a freelance client project.
The codebase is [X] lines / [X] files. It is a [web app / ML pipeline / automation].
I need to identify risks before I sign a maintenance retainer.
</context>

<task>
Perform a structured code audit and output:

1. SECURITY AUDIT
   - Secret leakage (API keys, passwords in code)
   - Injection vulnerabilities (SQL, command, XSS)
   - Authentication weaknesses
   - Dependency vulnerabilities (outdated packages)

2. PERFORMANCE AUDIT
   - N+1 query problems
   - Unnecessary API calls or heavy computations in loops
   - Memory leaks or unbounded growth
   - Blocking I/O in async contexts

3. MAINTAINABILITY AUDIT
   - Test coverage estimate
   - Code duplication (DRY violations)
   - Function length and complexity
   - Documentation completeness
   - Type hint coverage

4. ML-SPECIFIC AUDIT (if applicable)
   - Data leakage (target in features, future data in training)
   - Random split on time-series
   - Missing baseline comparison
   - No model versioning or experiment tracking
   - Hardcoded paths or parameters

5. PRIORITIZED REMEDIATION ROADMAP
   - Critical (fix before production)
   - High (fix within first sprint)
   - Medium (fix within first month)
   - Low (nice-to-have)
   - Estimated hours per category

6. RETAINER PRICING RECOMMENDATION
   - Hours per month for maintenance
   - Suggested retainer fee
   - SLA terms (response time, uptime)

Format: Markdown table for findings. Code snippets for examples of issues found.
</task>
```

---

## Prompt 6: Client Communication Reframer

**Use when:** You need to explain technical decisions, push back on scope creep, or justify pricing to a non-technical client.

```xml
<role>
You are a senior technical consultant who translates complex engineering concepts into business language that executives understand. You are diplomatic but firm.
</role>

<context>
I need to communicate the following to a non-technical client:
"[PASTE YOUR TECHNICAL ISSUE OR REQUEST HERE]"

The client's business context: [INDUSTRY, SIZE, GOAL]
My goal: [Get approval / Explain delay / Justify cost / Push back on scope]
</context>

<task>
Write three options for communicating this:

1. EMAIL VERSION (formal, async)
   - Subject line
   - 3-paragraph max body
   - One clear call-to-action
   - No jargon; use analogies if needed

2. CALL SCRIPT VERSION (verbal, real-time)
   - Opening hook
   - 3 key talking points
   - Anticipated objections and responses
   - Closing ask

3. SLACK/TEAMS VERSION (informal, fast)
   - 2-3 short messages
   - Emoji-friendly but professional
   - One decision needed

For each version, ensure:
- Business impact is stated first
- Technical details are minimized or analogized
- The client feels informed, not talked down to
- There is a clear next step

Format: Copy-paste ready text blocks.
</task>
```

---

## Prompt Usage Checklist

- [ ] **Before scoping:** Run Prompt 1 (ML) or Prompt 2 (Web) or Prompt 3 (Automation) or Prompt 4 (Analytics).
- [ ] **Before quoting:** Use the output to build your SOW in Module 03C.
- [ ] **During development:** Run Prompt 5 on your code before every major commit.
- [ ] **Before client calls:** Run Prompt 6 to prepare for difficult conversations.
- [ ] **Weekly:** Re-run Prompt 1 with a new hypothetical client to keep your scoping skills sharp.

---

## Pro Tips for 2026 Prompt Engineering

| Technique | When to Use | Example |
|-----------|-------------|---------|
| **XML Tagging** | Complex multi-part prompts | `<role>`, `<context>`, `<task>` |
| **Agentic Prompting** | End-to-end project planning | "Goal: create launch plan. Steps you should take: (1)... (2)..." |
| **Few-Shot** | Specific output format needed | Paste 3 examples of your writing style first |
| **Negative Prompts** | Prevent common AI mistakes | "Do NOT use placeholder comments. Do NOT use deprecated libraries." |
| **Structured Output** | Need machine-parseable result | "Return as JSON with keys: summary, risks, recommendations" |
| **Chain-of-Thought** | Debugging or reasoning tasks | "Think through this step by step before giving your final answer." |

---

*Reference: Prompt engineering best practices synthesized from Anthropic Prompt Library, OpenAI Platform Docs, and 2026 prompt engineering research.*
