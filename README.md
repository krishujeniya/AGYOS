# SKILL

The unified repository of AI agent skills, autonomous workflows, multi-agent deliberation systems, and engineering verification runtimes. Maintained by [Krish Ujeniya](https://github.com/krishujeniya).

## Documentation and live catalog

The full documentation site and interactive skill catalog is hosted on GitHub Pages:

**Live documentation:** [https://krishujeniya.github.io/SKILL/](https://krishujeniya.github.io/SKILL/)

- Zero backend dependencies: 100% static HTML, CSS, and client-side JavaScript.
- Strict monochrome design: Swiss typography, high contrast, responsive layout, dark and light modes.
- Instant search and filtering across all 1,580+ skills by module, runtime, or keyword.
- Machine-readable discovery files: [llms.txt](https://krishujeniya.github.io/SKILL/llms.txt), [ai-catalog.json](https://krishujeniya.github.io/SKILL/ai-catalog.json), and [sitemap.xml](https://krishujeniya.github.io/SKILL/sitemap.xml).

---

## Directory layout

```
SKILL/
├── Aegis/                     # Security, verification library, and 1,500+ skills
├── Anchor/                    # Scoped orchestrator, contract manager, and MCP server
├── agent-council/             # Multi-agent deliberation panel CLI
├── agentic-freelance-skills/  # End-to-end consulting and client delivery suite
├── ScrollHeart/               # Scroll-driven web animations and storytelling
├── docs/                      # Pure static documentation and explorer site
├── scripts/                   # Data compilation and runtime linking utilities
├── Motion_Graphics_Google_Flow_Master_Guide.pdf  # Motion graphics master guide
└── github-profile-playbook.pdf                   # Developer positioning playbook
```

---

## Core modules

### 1. Aegis: Security, verification and skill library
Aegis provides a defense-in-depth skill library and verification runtime for AI agents.

- **1,450+ community skills**: Covers cloud providers, scrapers, databases, web frameworks, and programming languages.
- **79 core skills**: Foundational skills for automated evaluation, refactoring, context restoration, and test runners.
- **50 expert skills**: Specialized suites for deep security audits, performance profiling, and architecture reviews.

Explore: [`Aegis/`](./Aegis)

---

### 2. Anchor: Scoped orchestrator and execution runtime
Anchor is an execution system that bounds blast radius and enforces five mandatory gates for multi-step tasks.

- `anchor-scout`: Read-only reconnaissance and codebase exploration.
- `anchor-scope`: Scope boundary enforcement in `contract.json`.
- `anchor-orchestrator`: Multi-step plan execution through understand, analyze, plan, implement, and verify gates.
- `anchor-draft-commit`: Atomic, reversible git checkpointing.
- `anchor-verify`: Evidence-backed test and lint validation.
- `anchor-graph`: Dependency and call-path analysis.
- `anchor-preflight`: Preflight environment and tool verification.
- **MCP server**: Lazily-loaded MCP server exposing Anchor primitives.

Explore: [`Anchor/`](./Anchor)

---

### 3. Agent Council: Multi-agent deliberation panel
Agent Council runs multiple AI models (Codex, Gemini, Claude, Antigravity) in isolated subprocesses to deliberate on architectural decisions and synthesize consensus verdicts.

- **Multi-model consensus**: Queries diverse models independently against the same problem.
- **Chairman synthesis**: Summarizes common points, disagreements, and final recommendations.
- **Audit trail**: Saves deliberation logs and replayable HTML transcripts.

Explore: [`agent-council/`](./agent-council)

---

### 4. Agentic freelance skills: Autonomous agency suite
An operational suite for freelance software engineers and consultants:

- `freelancer-client-acquisition`: Outbound prospecting, cold email sequences, and referral loops.
- `freelancer-sales-closing`: Discovery calls, objection handling, pricing models, and contract signing.
- `freelancer-project-delivery`: Milestone roadmaps, client sprint updates, and demo walkthroughs.
- `freelancer-operations`: Invoicing, payment tracking, and standard operating procedures.
- `freelancer-post-delivery`: Handover documentation packages and maintenance retainer agreements.
- `freelancer-emergency-kit`: Incident runbooks and client communication playbooks for outages.

Explore: [`agentic-freelance-skills/`](./agentic-freelance-skills)

---

### 5. ScrollHeart: Cinematic motion and storytelling
ScrollHeart builds scroll-driven web experiences using HTML, CSS, and GSAP ScrollTrigger. It generates lightweight static pages deployable directly on GitHub Pages without video rendering pipelines.

Explore: [`ScrollHeart/`](./ScrollHeart)

---

### 6. Reliability and quality standards
- **Gravitas**: Enforces six engineering invariants: ground before mutating, stay in declared scope, require evidence for completion, avoid identical retries, satisfy contract gates, and state unverifiable claims.
- **Unslop**: Strips synthetic AI vocabulary, superficial clauses, and robotic formatting from documentation.

---

## Installation in AGY and Codex

To install and verify all skills across your local AI environments:

```bash
# Link all monorepo skills into AGY (~/.gemini/skills) and Codex (~/.codex/skills)
python3 scripts/build_docs_data.py
```

The script verifies that all skills from Anchor, Agent Council, Freelance Suite, ScrollHeart, SEO Suite, and Founder Suite are symlinked into both `~/.gemini/skills/` and `~/.codex/skills/`.

---

## Local preview of documentation site

To preview the documentation locally with any static web server:

```bash
# Using Python
python3 -m http.server 8080 --directory docs

# Open in browser
xdg-open http://localhost:8080
```

---

## License

This repository consolidates tools and skills under their respective open-source licenses (MIT / Apache-2.0).
