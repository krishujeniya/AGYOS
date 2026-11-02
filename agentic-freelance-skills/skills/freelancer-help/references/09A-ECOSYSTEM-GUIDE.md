---
title: "09A: Skill Ecosystem & Prompting Guide"
description: "How to navigate the 9 freelance modules, identify trigger keywords, and query/prompt AI agents for maximum efficiency."
module: "09-HELP"
---

# 09A: Skill Ecosystem & Prompting Guide

> **Principle:** Having access to professional-grade playbooks is only 20% of the battle. The other 80% is knowing exactly *how* and *when* to activate them. An AI agent is a force multiplier, but it requires precise steering.

---

## 1. Navigating the 9-Module Ecosystem

This repository covers the entire lifecycle of a freelancer. Use the lookup table below to quickly map your business challenges to the correct skill namespace and reference files:

| Business Phase | Typical Challenges / Questions | Target Skill | Reference Files to Load |
|:---|:---|:---|:---|
| **Identity & Brand** | "How do I price myself?", "My LinkedIn is getting no views", "How should I write my resume/case studies?" | `freelancer-identity` | `01A-PERSONAL-BRAND.md`<br>`01B-LINKEDIN-OPTIMIZATION.md`<br>`01C-PORTFOLIO-POSITIONING.md` |
| **Acquisition & Leads** | "Where do I find clients?", "How do I write a cold email?", "How can I stand out on Upwork?" | `freelancer-client-acquisition` | `02A-PROSPECTING-SYSTEM.md`<br>`02B-COLD-OUTREACH.md`<br>`02C-PLATFORM-STRATEGY.md`<br>`02D-CONTENT-MARKETING.md` |
| **Sales & Closing** | "What do I say on a discovery call?", "How do I pitch value-based pricing?", "How do I write a proposal?" | `freelancer-sales-closing` | `03A-DISCOVERY-CALL.md`<br>`03B-PRICING-STRATEGY.md`<br>`03C-PROPOSAL-TEMPLATES.md`<br>`03D-NEGOTIATION-PLAYBOOK.md` |
| **Project Delivery** | "How do I manage client expectations?", "What tools should I use for ML pipelines?", "How do I do handoffs?" | `freelancer-project-delivery` | `04A-KICKOFF-SYSTEM.md`<br>`04C-DEVELOPMENT-WORKFLOW.md`<br>`04D-ML-OPS-PIPELINE.md`<br>`04F-DELIVERY-HANDOFF.md` |
| **Post-Delivery / Retention** | "How do I get client testimonials?", "How do I sell a monthly retainer?", "How do I transition support?" | `freelancer-post-delivery` | `05A-TESTIMONIALS-REVIEWS.md`<br>`05B-MAINTAINERS-RETAINERS.md`<br>`05C-UPSELL-CROSS-SELL.md` |
| **Business Operations** | "What goes into a contract?", "How do I automate invoicing?", "How do I manage my daily schedule?" | `freelancer-operations` | `06A-FINANCE-TRACKING.md`<br>`06B-LEGAL-CONTRACTS.md`<br>`06C-AUTOMATION-STACK.md`<br>`06D-TIME-MANAGEMENT.md` |
| **Developer Assets** | "Give me a FastAPI skeleton", "How do I structure a system design doc?", "How do I set up drift alerts?" | `freelancer-developer-resources` | `07A-PROJECT-PROMPTS.md`<br>`07B-ARCHITECTURE-TEMPLATES.md`<br>`07C-CODE-SNIPPETS.md`<br>`07D-MONITORING-PLAYBOOKS.md` |
| **Crisis Management** | "My client wants to add features for free", "The client isn't paying", "I am working 14-hour days" | `freelancer-emergency-kit` | `08A-SCOPE-CREEP-DEFENSE.md`<br>`08B-DIFFICULT-CLIENTS.md`<br>`08C-BURNOUT-PREVENTION.md`<br>`08D-PIVOT-STRATEGIES.md` |
| **Ecosystem Help** | "How do these skills relate?", "Give me an example of the full flow", "How do I use this repository?" | `freelancer-help` | `09A-ECOSYSTEM-GUIDE.md`<br>`09B-END-TO-END-EXAMPLE.md`<br>`09C-FREELANCE-LIFE-IMPACT.md` |

---

## 2. Prompting Formulas for Maximum Precision

To get the absolute best results from your AI agent (whether using Antigravity, Claude Code, or a web chat interface), construct your requests using this three-part formula:

$$\text{Context} + \text{Reference Document} + \text{Input Data} = \text{Actionable Output}$$

### 2.1 The Formula Broken Down
1. **Context:** Describe your specific freelancing niche, target client type, and immediate business objective.
2. **Reference Document:** Direct the agent to read a specific markdown file from this repository. (e.g. *"Read skills/freelancer-operations/references/06B-LEGAL-CONTRACTS.md"*).
3. **Input Data:** Paste the current email, draft proposal, client description, or pricing requirements.
4. **Actionable Output:** Specify the format of the output you need (e.g., email reply, redlined contract, Google Sheets formula).

### 2.2 Good vs. Poor Prompting Examples

> [!WARNING]
> **Poor Prompt:**
> *"Help me reply to a client who wants to add more features to our project."*
> *Why it fails:* It lacks context, doesn't point to a reference skill, and forces the agent to guess the pricing model, current relationship health, and specific additions.

> [!TIP]
> **Superb Prompt (Using the Formula):**
> *"I am a freelance ML engineer. I have a client who just emailed asking to add drift monitoring to our current regression model pipeline, which is not in our original Statement of Work (SOW). We have a fixed-price contract of \$8,000. 
> Please read `skills/freelancer-emergency-kit/references/08A-SCOPE-CREEP-DEFENSE.md` (Scope Creep Defense).
> Based on Section 2 (Change Request responses), draft a professional email reply presenting two options:
> 1. An add-on scope for \$1,500 to build the drift pipeline.
> 2. Scheduling the drift pipeline as a separate Phase 2 project after we deliver the core model.
> Keep the tone collaborative, firm, and helpful."*

---

## 3. The Master Agent Trigger Prompt

If you are starting a new session with an AI coding agent or creating a Custom GPT/Claude Project, copy-paste the prompt below into the system instructions or initial prompt. This forces the agent to use this repository as its source-of-truth business operating system:

```text
You are Antigravity, my AI Freelancer Operations Officer. Your job is to help me run, scale, and protect my freelance solo agency using the local "agentic-freelance-skills" repository.

Whenever I ask a business-related question, you must follow these operational rules:
1. Identify which skill module matches my situation by consulting `skills/freelancer-help/references/09A-ECOSYSTEM-GUIDE.md`.
2. Locate and read the relevant reference markdown files in that skill's subdirectory.
3. Apply the exact frameworks, pricing math, legal terms, or scripts outlined in those reference documents. Do not improvise generic internet advice.
4. Present outputs in clean, copy-pasteable markdown, highlighting the exact reference document (e.g., [08A-SCOPE-CREEP-DEFENSE.md]) that guided your advice.

Let me know you are ready by outputting a summary of the 9 available skill areas and asking me what stage of my freelance lifecycle we are tackling today.
```

---

## 4. Action Checklist

### Implementation Steps
- [ ] Symlink or copy the `skills/` folders to your agent's config path (e.g., `~/.gemini/antigravity/skills/`).
- [ ] Create a shortcut command in your terminal (`alias agentops="claude"`) to spin up your agent-assisted operations center in one keystroke.
- [ ] Keep this file open in your IDE whenever you are doing freelance administrative tasks for quick cross-referencing.

---

*Next: `09B-END-TO-END-EXAMPLE.md` — The skills ecosystem in action.*
