# Agentic Freelance Skills

An agent-native, professional-grade skill repository for solo AI/ML/Data Science freelancers. This repository is structured to be dynamically discovered, loaded, and executed by AI coding agents (such as Claude Code, Claude AI, and Antigravity) to assist with the entire freelance lifecycle.

---

## Agentic Skill Architecture

This repository adopts a **Progressive Disclosure Skill Design** optimized for LLM token efficiency:

1. **Discovery Indexes (`skills/*/SKILL.md`)**: The root of each skill directory contains a lean `SKILL.md` file. It features a standardized YAML frontmatter trigger description indicating precisely *when* the agent should load this skill. It deliberately omits long workflows to prevent token bloat and AI shortcuts.
2. **Detailed References (`skills/*/references/*`)**: Heavy playbooks, copy-paste prompts, code boilerplates, and templates are isolated in `references/` directories. The agent only loads these files when actively executing a specific sub-task, saving context window space.

```
agentic-freelance-skills/
├── README.md                                 ← You are here (Master Repository Guide)
└── skills/
    ├── freelancer-identity/
    │   ├── SKILL.md                          ← Entrypoint & triggers
    │   └── references/                       ← Progressive disclosure docs
    │       ├── 01A-PERSONAL-BRAND.md
    │       ├── 01B-LINKEDIN-OPTIMIZATION.md
    │       └── 01C-PORTFOLIO-POSITIONING.md
    ├── freelancer-client-acquisition/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 02A-PROSPECTING-SYSTEM.md
    │       ├── 02B-COLD-OUTREACH.md
    │       ├── 02C-PLATFORM-STRATEGY.md
    │       ├── 02D-CONTENT-MARKETING.md
    │       └── 02E-REFERRAL-ENGINE.md
    ├── freelancer-sales-closing/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 03A-DISCOVERY-CALL.md
    │       ├── 03B-PRICING-STRATEGY.md
    │       ├── 03C-PROPOSAL-TEMPLATES.md
    │       ├── 03D-NEGOTIATION-PLAYBOOK.md
    │       └── 03E-CLOSING-RITUALS.md
    ├── freelancer-project-delivery/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 04A-KICKOFF-SYSTEM.md
    │       ├── 04B-PROJECT-MANAGEMENT.md
    │       ├── 04C-DEVELOPMENT-WORKFLOW.md
    │       ├── 04D-ML-OPS-PIPELINE.md
    │       ├── 04E-TESTING-QA.md
    │       └── 04F-DELIVERY-HANDOFF.md
    ├── freelancer-post-delivery/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 05A-TESTIMONIALS-REVIEWS.md
    │       ├── 05B-MAINTAINERS-RETAINERS.md
    │       ├── 05C-UPSELL-CROSS-SELL.md
    │       └── 05D-OFFBOARDING.md
    ├── freelancer-operations/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 06A-FINANCE-TRACKING.md
    │       ├── 06B-LEGAL-CONTRACTS.md
    │       ├── 06C-AUTOMATION-STACK.md
    │       ├── 06D-TIME-MANAGEMENT.md
    │       └── 06E-SCALING-SYSTEMS.md
    ├── freelancer-developer-resources/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 07A-PROJECT-PROMPTS.md
    │       ├── 07B-ARCHITECTURE-TEMPLATES.md
    │       ├── 07C-CODE-SNIPPETS.md
    │       ├── 07D-MONITORING-PLAYBOOKS.md
    │       └── 07E-INTERVIEW-PREP.md
    ├── freelancer-emergency-kit/
    │   ├── SKILL.md
    │   └── references/
    │       ├── 08A-SCOPE-CREEP-DEFENSE.md
    │       ├── 08B-DIFFICULT-CLIENTS.md
    │       ├── 08C-BURNOUT-PREVENTION.md
    │       └── 08D-PIVOT-STRATEGIES.md
    └── freelancer-help/
        ├── SKILL.md
        └── references/
            ├── 09A-ECOSYSTEM-GUIDE.md
            ├── 09B-END-TO-END-EXAMPLE.md
            └── 09C-FREELANCE-LIFE-IMPACT.md
```

---

## How to Install and Load Skills in AI Agents

You can import these skills directly into your favorite agentic coding interfaces to automate lead generation, legal drafting, or MLOps setup.

### 1. Claude Code CLI
To load these skills into the Claude Code terminal CLI:
1. Copy the desired skill folders into your local Claude configuration directory:
   ```bash
   cp -r skills/* ~/.claude/skills/
   ```
2. Restart your Claude Code terminal.
3. Claude will automatically scan the frontmatter descriptions in the `SKILL.md` files and load them into context whenever you ask it a relevant question.

### 2. Antigravity Agent CLI
To load these skills into Antigravity:
1. Copy or symlink the skill folders into the Antigravity skill path:
   ```bash
   mkdir -p ~/.gemini/antigravity/skills/
   cp -r skills/* ~/.gemini/antigravity/skills/
   ```
2. The agent will discover them automatically on startup and execute them on demand.

### 3. Claude AI (Web Interface - Projects)
To use these skills in the Claude.ai Web UI:
1. Create a new **Project** in Claude.ai.
2. Upload the `SKILL.md` files and specific reference files you need for your task as project documents.
3. Add the following instruction to the Project's Custom Instructions:
   > *"You are an AI freelance operations assistant. Access the uploaded SKILL.md files to locate triggering instructions, then reference the sub-documents in the references directory to execute the requested freelance business workflow."*

---

## Overview of the 9 Skills

| Skill Namespace | Focus | Purpose |
|-----------------|-------|---------|
| [**freelancer-identity**](skills/freelancer-identity/SKILL.md) | Identity System | Personal branding, Trust Triangle, LinkedIn optimization, case studies. |
| [**freelancer-client-acquisition**](skills/freelancer-client-acquisition/SKILL.md) | Acquisition Engine | Cold outreach campaigns, signal-based prospecting, platform profiles (Upwork/Contra). |
| [**freelancer-sales-closing**](skills/freelancer-sales-closing/SKILL.md) | Closing & Pricing | Discovery scripts, value-based pricing, SOW proposals, rate negotiations. |
| [**freelancer-project-delivery**](skills/freelancer-project-delivery/SKILL.md) | Operations & MLOps | Kickoff rituals, sprint updates, Git branch setups, ZenML/MLflow pipeline integrations. |
| [**freelancer-post-delivery**](skills/freelancer-post-delivery/SKILL.md) | Retainers & Loops | Testimonial acquisition, support SLAs, quarterly upselling, clean offboarding. |
| [**freelancer-operations**](skills/freelancer-operations/SKILL.md) | Backoffice & Admin | Wise/banking setups, contract terms (late fees, IP transfer), Zapier/n8n pipelines. |
| [**freelancer-developer-resources**](skills/freelancer-developer-resources/SKILL.md) | Templates & Prompts | System design templates, ADR sheets, FastAPI boilerplate, Grafana drift alerts. |
| [**freelancer-emergency-kit**](skills/freelancer-emergency-kit/SKILL.md) | Crisis Management | Scope creep defenses, late payment collections, burnout recovery, rate pivots. |
| [**freelancer-help**](skills/freelancer-help/SKILL.md) | Ecosystem Help | Navigator, end-to-end walkthrough example, career & lifestyle impact analysis. |

---

## Design Principles

- **Modular**: Separate `.md` files per sub-topic. Never one giant file.
- **Generic**: No personal names or private details. Any freelancer worldwide can use this.
- **Tone**: Formal, professional, trustworthy.
- **AI-Ready**: Every reference file contains copy-paste prompts for ChatGPT/Claude.
- **Actionable**: Includes templates, checklists, scripts, and week-by-week sprints.

---

## Key Research Sources

- **Him Singh's Free Freelancing Course**: Profile optimization, 15-15-15 ritual, cold outreach templates.
- **Ayush Singh's Production-Grade ML Projects**: MLOps, drift detection, Prometheus/Grafana alerts, ADR templates.
- **2026 Platform Analytics**: Upwork algorithm tracking, Contra flat-fee contracts, Apollo.io prospecting.
- **StopScopeCreep 2026**: Scope creep defense, change request workflows.
- **Jobbers.io Burnout Index 2025**: Burnout prevention, financial stability, energy management.

---

## License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
