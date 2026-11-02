# SKILL ⚡

> **The Unified AI Agent Skills, Frameworks, and Tooling Monorepo**  
> Curated and maintained by [@krishujeniya](https://github.com/krishujeniya).

A consolidated, production-grade repository combining state-of-the-art AI agent skills, autonomous workflows, multi-agent deliberation systems, and cinematic web animation frameworks for modern coding agents (Antigravity, Gemini CLI, Claude Code, Codex, Cursor, and Windsurf).

---

## 📦 What's Inside

```
SKILL/
├── Aegis/                     # Massive skill framework & verification library (1,500+ skills)
├── Anchor/                    # Agent orchestration, scoping, verification & MCP server
├── ScrollHeart/               # Cinematic scroll-driven web animation & storytelling skill
├── agentic-freelance-skills/  # End-to-end freelance agency skills (acquisition to delivery)
├── agent-council/             # Multi-agent deliberation council CLI (Codex, Gemini, Claude, Antigravity)
├── Motion_Graphics_Google_Flow_Master_Guide.pdf  # Motion graphics master guide
└── github-profile-playbook.pdf                   # Developer positioning playbook
```

---

## 🛡️ 1. Aegis — Security, Verification & Skill Library

`Aegis` provides a robust, defense-in-depth skill library and verification runtime for AI agents.

- **1,445+ Community Skills**: Covers algorithms, API integrations, DevOps, security, data science, and web frameworks.
- **83 Core Skills**: Critical foundational skills for code review, refactoring, debugging, and architecture.
- **Expert Domain Skills**: Specialized suites for deep security audits, performance profiling, and SEO analysis.
- **Engine & Specs**: Standardized schema, manifests, and documentation for consistent agent tool calling.

👉 Explore: [`Aegis/`](./Aegis)

---

## ⚓ 2. Anchor — Agent Orchestrator & Execution Runtime

`Anchor` is a scoped, verifiable agent orchestration system that prevents hallucinations, bounds blast radius, and enforces strict preflight and post-execution verification.

- **Anchor Skills**:
  - `anchor-scout`: Reconnaissance and safe codebase exploration.
  - `anchor-scope`: Scope boundary enforcement.
  - `anchor-orchestrator`: Multi-step plan execution.
  - `anchor-draft-commit`: Atomic, reversible git checkpointing.
  - `anchor-verify`: Evidence-backed test and lint validation.
  - `anchor-graph`: Dependency and call-path analysis.
- **MCP Server**: Lazily-loaded MCP server exposing Anchor primitives to any MCP-compliant client.
- **Dashboard**: Live terminal monitoring and telemetry dashboard.

👉 Explore: [`Anchor/`](./Anchor)

---

## 📜 3. ScrollHeart — Cinematic Motion & Visual Storytelling

`ScrollHeart` is a dedicated skill for building cinematic, video-like scroll-driven animations and narrative web experiences using HTML, CSS, and GSAP.

- **Kinetic Typography & Storytelling**: Replaces boring slide decks with fluid, video-grade web experiences.
- **GSAP & Native CSS Scroll Timelines**: Production-optimized scroll-driven animation presets.
- **Examples & Resources**: Ready-to-use templates, interactive demos, and component blueprints.

👉 Explore: [`ScrollHeart/`](./ScrollHeart)

---

## 💼 4. Agentic Freelance Skills — Autonomous Agency Suite

A complete suite of operational and client-facing skills designed for autonomous freelance software engineering and consulting.

- **`freelancer-client-acquisition`**: Lead prospecting, proposal crafting, and outreach.
- **`freelancer-sales-closing`**: Objection handling, scoping, and contract negotiation.
- **`freelancer-project-delivery`**: Milestone structuring, deliverables tracking, and client updates.
- **`freelancer-operations`**: Invoicing, time management, and agency SOPs.
- **`freelancer-post-delivery`**: Handover packages, upsells, and testimonial gathering.
- **`freelancer-emergency-kit`**: Urgent production bug fixes, client de-escalation, and outage playbooks.

👉 Explore: [`agentic-freelance-skills/`](./agentic-freelance-skills)

---

## 🏛️ 5. Agent Council — Multi-Agent Deliberation Panel

`agent-council` convenes a panel of CLI-based AI agents (Codex, Gemini, Claude, and Antigravity) to independently deliberate on complex architectural decisions, debug hard bugs, and synthesize high-confidence consensus verdicts.

- **Multi-Model Consensus**: Runs diverse models against the same problem in isolated subprocesses.
- **Antigravity Native Integration**: Seamlessly integrates Antigravity / Gemini CLI / Claude / Codex as chairmen or panel members.
- **Interactive HTML Viewer**: Generates clean, tabbed deliberation logs and side-by-side opinions.

👉 Explore: [`agent-council/`](./agent-council)

---

## 📚 6. Guides & Reference Playbooks

- **`Motion_Graphics_Google_Flow_Master_Guide.pdf`**: Comprehensive manual for mastering cinematic web animations, Google Flow, and browser video workflows.
- **`github-profile-playbook.pdf`**: The definitive playbook for architecting standout GitHub profiles and showcasing open-source authority.

---

## 🚀 Quickstart & Skill Installation

### Symlink into Antigravity or Gemini CLI
```bash
# Add any skill directly to your personal agent environment
mkdir -p ~/.agents/skills
ln -s "$(pwd)/ScrollHeart" ~/.agents/skills/scrollheart
ln -s "$(pwd)/agentic-freelance-skills/skills/freelancer-help" ~/.agents/skills/freelancer-help
```

### Running Agent Council
```bash
cd agent-council
bun install
bun run start --question "Should we use Redis or PostgreSQL for session caching?"
```

---

## 📄 License

This monorepo consolidates tools and skills under their respective open-source licenses (MIT / Apache-2.0). See individual subdirectories for details.

Developed with ❤️ by **[Krish Ujeniya](https://github.com/krishujeniya)**.
