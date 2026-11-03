---
title: "06C: Automation Stack"
description: "Zapier, Make, n8n selection criteria, AI agent workflows, and CRM architecture for solo freelancers."
module: "06-OPERATIONS"
---

# 06C: Automation Stack

> **Principle:** Every repetitive task you perform twice per week should be automated by the third week. The solo freelancer's competitive advantage is not working more hours — it is systematizing everything that does not require judgment.

## 1. Platform Selection Framework

### 1.1 The 2026 Automation Landscape

| Platform | Best For | Pricing (2026) | Key Strength | Key Weakness |
|----------|----------|---------------|--------------|--------------|
| **Zapier** | Beginners, quick integrations, 7,000+ apps | Free: 100 tasks/mo; Starter: ~$20/mo (750 tasks); Pro: ~$49/mo (2,000 tasks) | Fastest time-to-automation; largest app library; AI natural-language workflow creation | Expensive at scale; limited branching logic; no self-hosting |
| **Make (Integromat)** | Complex multi-step workflows, visual routing, cost efficiency | Free: 1,000 ops/mo; Core: ~$9/mo (10,000 ops); Pro: ~$16/mo (10,000 ops + advanced) | Visual canvas builder; 60% cheaper than Zapier; native routers, iterators, data stores | Steeper learning curve; 1,500+ integrations (vs 7,000+); cloud-only |
| **n8n** | Technical freelancers, AI agent workflows, data sovereignty, cost control at scale | Free cloud: 2,500 runs/mo; Pro cloud: ~$20/mo; Self-hosted: $0 license (server costs only) | Self-hosted option; unlimited executions; native LangChain + AI agents; custom JS/Python nodes; direct DB connections | Requires DevOps knowledge; 400+ native integrations; steeper onboarding |
| **HubSpot Workflows** | CRM-native automation, email sequences, deal-stage triggers | Included in HubSpot CRM free tier; paid plans from $20/mo | Zero setup friction if already using HubSpot CRM | Locked to HubSpot ecosystem; limited external integrations |
| **Airtable Automations** | Database-heavy operations, inventory, project portfolios | Included in Airtable free tier; paid from $20/mo/user | Native automations remove third-party dependency; structured data + automation in one | Smaller trigger library; limited for cross-app workflows |

### 1.2 Decision Matrix

Answer these three questions to select your primary platform:

| Question | If Yes → | If No → |
|----------|----------|---------|
| **Do you need self-hosting or data sovereignty?** | n8n (self-hosted) | Zapier or Make |
| **Are your workflows simple (2–3 steps, linear)?** | Zapier | Make or n8n |
| **Do you build AI agents or need custom code nodes?** | n8n | Make or Zapier |
| **Is cost-per-operation your primary constraint?** | n8n self-hosted or Make | Zapier |
| **Do you need the largest possible app library?** | Zapier (7,000+) | Make (1,500+) or n8n (400+) |
| **Are you non-technical and need speed?** | Zapier | Make (moderate learning curve) |

> **Solo Freelancer Recommendation:** Start with **Make** for operational workflows (prospecting, invoicing, project updates) and **n8n self-hosted** for AI agent experiments and custom API integrations. Use **Zapier** only for quick one-off integrations that Make does not support.

---

## 2. Core Automation Workflows

### 2.1 Lead Capture & Triage

**Trigger:** New lead enters system (LinkedIn DM, website form, Apollo.io list, email).

**Workflow:**

```
[Lead Source]
    → [Data Enrichment] (Apollo.io / Hunter.io / Clearbit)
    → [Scoring] (Assign 1–5 star rating based on company size, budget signals, urgency)
    → [CRM Entry] (HubSpot / Notion / Airtable)
    → [Slack Alert] ("New 4-star lead: [Name] at [Company] — [URL]")
    → [Auto-Reply] (Personalized email/DM acknowledging inquiry within 5 minutes)
    → [Calendar Link] (If 4–5 star, send Calendly/TidyCal booking link)
    → [Task Creation] (Add to follow-up queue: Day 1, Day 3, Day 7, Day 10, Day 14)
```

**Platform:** Make or n8n (for conditional routing and data stores).

### 2.2 Client Onboarding Sequence

**Trigger:** Contract signed + deposit received.

**Workflow:**

```
[Payment Confirmation] (Stripe / Wise / Payoneer webhook)
    → [Welcome Email] (Project timeline, communication rules, access requests)
    → [Slack/Discord Channel Creation] (Auto-create private client channel)
    → [Project Board Setup] (Notion / Linear / GitHub Projects — auto-populate milestones)
    → [Calendar Invites] (Kickoff call, weekly check-ins, milestone review dates)
    → [File Structure] (Auto-create Google Drive / Dropbox folder with template subfolders)
    → [Access Requests] (Generate list: repo access, API keys, database credentials, analytics logins)
    → [Internal Alert] (Slack: "New client onboarded — [Name]. Kickoff: [Date]. PM: [You].")
```

**Platform:** Zapier or Make (for Google Workspace / Slack / Notion native integrations).

### 2.3 Invoice & Payment Automation

**Trigger:** Milestone marked "Complete" in project board OR calendar date (1st of month for retainers).

**Workflow:**

```
[Milestone Complete / Calendar Trigger]
    → [Invoice Generation] (Wave / FreshBooks / EasyStaff — auto-populate from project data)
    → [PDF Attachment] (Auto-attach SOW excerpt and timesheet if hourly)
    → [Email Send] (Professional invoice email with payment link)
    → [CRM Update] (Deal stage: "Invoiced")
    → [Follow-Up Sequence] 
        Day 7: Gentle reminder
        Day 14: Second reminder + late-fee notice
        Day 21: Final notice + work suspension warning
        Day 30: Escalation to collections or legal review
    → [Payment Receipt] (Webhook from payment platform)
        → [CRM Update] (Deal stage: "Paid")
        → [Slack Alert] ("[Client] paid $[Amount] — next milestone: [Date]")
        → [Tax Log] (Auto-log to expense/income tracker)
```

**Platform:** Make or n8n (for conditional branching and multi-step logic).

### 2.4 Content Marketing Engine

**Trigger:** Weekly (scheduled) or RSS feed (new blog post / case study published).

**Workflow:**

```
[Content Published]
    → [Social Media Drafts] (AI generates LinkedIn, Twitter/X, Reddit post variants)
    → [Image Generation] (DALL-E / Midjourney API for featured image)
    → [Scheduling] (Buffer / Hootsuite / native API — queue for optimal times)
    → [Newsletter Draft] (Convert post to email format; queue in Mailchimp / Brevo)
    → [SEO Ping] (IndexNow / Google Indexing API — notify search engines)
    → [Analytics Log] (Track publish date, platform, expected engagement baseline)
```

**Platform:** n8n (for AI node integration and custom API calls) or Make.

### 2.5 AI Agent Workflow (Advanced)

**Trigger:** New support email or Slack message from client.

**Workflow (n8n with LangChain):**

```
[Incoming Message]
    → [Intent Classification] (LLM node: "Is this urgent, question, or routine update?")
    → [Knowledge Retrieval] (RAG pipeline: query vector DB of project docs, past decisions, SOW)
    → [Draft Response] (LLM generates response with citations from project context)
    → [Human Review Gate] (If confidence < 0.8 or "urgent" intent, pause for your approval)
    → [Auto-Send] (If confidence ≥ 0.8 and "routine", send immediately)
    → [Log & Learn] (Store thread in vector DB; flag misclassifications for retraining)
```

**Platform:** n8n (native LangChain integration, vector DB support, custom AI agents).

---

## 3. CRM Architecture for Solo Freelancers

### 3.1 Minimal Viable CRM (Free Tier)

| Component | Tool | Purpose |
|-----------|------|---------|
| **Contact Database** | Notion or Airtable | Companies, contacts, interaction history, deal stages |
| **Pipeline** | Kanban view: Prospect → Qualified → Proposal → Contract → Active → Delivery → Retainer | Visual deal flow |
| **Activity Log** | Relation property: Last contact, next action, meeting notes | No leads fall through cracks |
| **Revenue Tracker** | Roll-up formula: Sum of deal values by month/quarter | Cash-flow visibility |
| **Automation** | Notion automations or Zapier/Make | Status changes trigger emails, tasks, Slack alerts |

### 3.2 Growth-Stage CRM ($20–50/month)

| Component | Tool | Purpose |
|-----------|------|---------|
| **CRM Core** | HubSpot Free or Pipedrive | Deal stages, email tracking, meeting scheduler |
| **Email Sequences** | HubSpot Workflows or Brevo | Automated follow-ups, nurture campaigns |
| **Task Management** | Linear or Todoist | Engineering tasks integrated with CRM deals |
| **Document Hub** | Google Drive + Notion | SOWs, contracts, deliverables, meeting notes |
| **Analytics** | HubSpot Reports or Google Data Studio | Pipeline velocity, conversion rates, LTV |

### 3.3 CRM Data Model (Notion/Airtable Template)

**Companies Table:**
- Name, Industry, Size, Website, LinkedIn URL
- ICP Fit Score (1–5)
- Source (LinkedIn, Referral, Upwork, Content)
- Status (Target → Engaged → Client → Alumni)
- Lifetime Value (roll-up from Deals)

**Contacts Table:**
- Name, Role, Email, Phone, LinkedIn
- Company (relation)
- Last Contact Date, Next Action Date
- Warmth (Cold → Warm → Hot)

**Deals Table:**
- Deal Name, Company (relation), Contact (relation)
- Value, Currency, Probability (%)
- Stage (Prospect → Discovery → Proposal → Negotiation → Closed-Won / Closed-Lost)
- Expected Close Date, Actual Close Date
- Source, Campaign

**Activities Table:**
- Type (Email, Call, Meeting, LinkedIn DM, Content View)
- Contact (relation), Deal (relation)
- Date, Notes, Outcome
- Follow-Up Required (checkbox)

---

## 4. The 2026 Tech Stack for Solo AI Freelancers

| Layer | Primary Tool | Backup / Alternative | Monthly Cost |
|-------|-------------|---------------------|--------------|
| **Automation Engine** | Make (Core plan) | n8n self-hosted | $9–20 |
| **CRM** | Notion (Free) | HubSpot Free | $0–20 |
| **Email** | Gmail + Brevo (Free) | Mailchimp | $0–15 |
| **Calendar** | Google Calendar + Calendly (Free) | TidyCal | $0–10 |
| **Invoicing** | Wave (Free) | FreshBooks | $0–17 |
| **Storage** | Google Drive (15GB free) | Dropbox | $0–12 |
| **Communication** | Slack (Free) | Discord | $0 |
| **AI Agent** | n8n self-hosted + OpenAI API | Make + GPT integration | $10–50 |
| **Passwords** | Bitwarden (Free) | 1Password | $0–3 |
| **Total** | | | **$19–147/month** |

> **Target:** Keep operational tooling under $100/month until you consistently invoice $5,000+/month. Then upgrade selectively.

---

## 5. AI Prompts

### Prompt 1: Automation Workflow Designer
```
I am a solo freelance [specialty].
I currently waste time on these repetitive tasks:
[ list 3–5 tasks, e.g., "manually copying LinkedIn leads to a spreadsheet", "sending follow-up emails", "creating project folders" ]

For each task, design an automation workflow including:
- Trigger (what starts it)
- Steps (in order)
- Tools recommended (Zapier / Make / n8n / native)
- Estimated time saved per week
- Setup complexity (Low / Medium / High)

Format as a markdown table.
```

### Prompt 2: n8n AI Agent Builder
```
I want to build an n8n workflow that acts as a [purpose, e.g., "client support assistant" / "lead qualification agent" / "project status reporter"].

The agent should:
- Receive input from: [source, e.g., "Slack DM" / "email" / "webhook"]
- Query knowledge from: [source, e.g., "Notion project docs" / "vector DB of past emails"]
- Use LLM: [OpenAI GPT-4 / Claude / local model]
- Output to: [destination, e.g., "draft Slack reply" / "CRM update" / "email send"]
- Human approval required when: [condition, e.g., "confidence < 0.8" / "contains pricing question"]

Generate the complete n8n node sequence with:
- Node names and types
- Configuration parameters
- Error handling logic
- Testing checklist
```

### Prompt 3: CRM Health Audit
```
Here is my current CRM data export:
[ paste CSV or describe structure ]

Audit this CRM for:
1. Data quality issues (duplicates, missing fields, stale contacts)
2. Pipeline bottlenecks (deals stuck >30 days in one stage)
3. Conversion rate by source (which channel delivers best clients?)
4. Revenue concentration risk (% from top 3 clients)
5. Recommended automation to fix the top 3 issues

Output a prioritized action plan with quick wins this week.
```

---

## 6. Action Checklist

### This Week
- [ ] Map your top 5 time-wasting repetitive tasks.
- [ ] Sign up for Make (free tier) and build your first workflow: "New LinkedIn lead → Notion database entry."
- [ ] Set up Notion or Airtable as your CRM with Companies, Contacts, Deals, and Activities tables.
- [ ] Connect your invoicing tool to a payment gateway (Stripe, Wise, Payoneer).

### This Month
- [ ] Build the Lead Capture & Triage workflow (Section 2.1).
- [ ] Build the Invoice & Payment Automation workflow (Section 2.3).
- [ ] Set up the Client Onboarding Sequence (Section 2.2).
- [ ] Test an n8n AI agent for one use case (e.g., email drafting or FAQ response).

### Ongoing
- [ ] Review automation logs weekly for failures and optimize.
- [ ] Add one new automation per month as your practice grows.
- [ ] Maintain a "Automation Runbook" documenting every workflow, its purpose, and how to debug it.

---

*Next: `06D-TIME-MANAGEMENT.md` — Defend your deep work.*
