---
trigger: always_on
---

Be direct and concise. Avoid conversational filler, unnecessary preambles, and postambles.

# PRIORITY RULES & INVARIANTS (GLOBAL)
1. **Single Git Branch Discipline (main only)**:
   - On GitHub and locally, exclusively use the `main` branch.
   - Always display and maintain exactly ONE branch (`main`).
   - If multiple branches, stale branches, or legacy `master` branches exist, merge them into `main` and delete all other branches immediately.
   - Ensure the repository strictly works on and exposes only `main`.
2. **GitHub Profile & Push Discipline**:
   - Commits and pushes to GitHub must always be made with the profile:
     - Name: `Krish Ujeniya`
     - Email: `100012208+krishujeniya@users.noreply.github.com`
     - GitHub URL: `https://github.com/krishujeniya`
   - Ensure the git author, committer, and avatar/profile match `github.com/krishujeniya` accurately.
   - After completing work, commit and push to remote using this profile.
3. **Local Loadless Verification & GitHub Actions CI/CD Execution**:
   - Locally, perform ONLY fast type checks and simple, loadless validations (e.g. `tsc --noEmit`, syntax/type verification).
   - Do NOT run heavy builds, large test suites, container builds, or long-running tasks locally.
   - All full builds, comprehensive test suites, container builds, and deployment verifications MUST run in GitHub Actions CI/CD (`.github/workflows/ci.yml`).
   - **Continuous CI/CD Watch**: After pushing, actively monitor remote CI/CD workflow runs (`gh run list` / `gh run watch`) until ALL checks have succeeded (PASS / green). If any check fails, diagnose and push a fix immediately until all workflow runs succeed.
4. **Python Tooling (uv Only)**:
   - For all Python operations, dependency management, package installations, virtual environments, and script executions, exclusively use `uv` and official uv tools (`uv pip`, `uv run`, `uv add`, `uv venv`, `uv lock`, etc.). Never use legacy `pip` or unmanaged `python` commands directly.
5. **Human, Concrete & Direct Communication (Anti-Slop / Anti-AI Discipline)**:
   - Do NOT use generic AI filler words, templated jargon, buzzwords, boilerplate preambles/postambles, plagiarism phrases, watermark phrases, or unnecessary filler words.
   - Write cleanly, directly, concretely, and concisely with maximum factual density.
6. **Research & Apply Latest Proven Principles to Every Query**:
   - Continuously research and identify the latest working, real-world principles, standards, and canonical patterns for every query and task.
   - Apply state-of-the-art, validated, best-practice methodologies across all architecture, code, and decision workflows.
7. **Production Deployment & Cloudflare Tech Stack**:
   - For production deployment, exclusively use the **Cloudflare tech stack** (Cloudflare Pages & Cloudflare Workers).
   - Domain conventions:
     - Frontend: `<projectname>.pages.dev`
     - Backend: `api.<projectname>.workers.dev` (or `<projectname>.workers.dev` / `api-<projectname>.pages.dev`)

# AGYOS Operating System Integration
You are operating within the AGYOS (Antigravity Operating System) ecosystem by default.
- AGYOS Core Workspace: `/home/ai/Documents/projects/Freelance/AGYOS`
- AGYOS CLI: `/home/ai/Documents/projects/Freelance/AGYOS/bin/agyos`
- Catalog & Decision Engine: Whenever taking on non-trivial workflows, engineering tasks, audits, design, or architecture, follow AGYOS standards.
- Skills: The complete AGYOS skill catalog is available in `~/.agents/skills/` and registered in Pi. Leverage the relevant skills (e.g. `agyos-orchestrator`, `agyos-decision`, `agyos-scout`, `agyos-verify`, etc.) according to task requirements.
- State & Telemetry: Respect the 5-Gate architecture (UNDERSTAND, ANALYZE, PLAN, IMPLEMENT, VERIFY) when coordinating complex multi-step development.

# CODING AGENTS & AGENT FILES REPOSITORY HYGIENE (GLOBAL INVARIANT)
- Never commit agent instructions, harness configs, or coding agent workspace metadata to git repositories.
- Always ignore agent instruction files and directories across projects, including:
  - `AGENTS.md`, `agent.md`, `agents.md`, `CLAUDE.md`, `claude.md`, `GEMINI.md`, `gemini.md`, `COPILOT.md`, `copilot.md`
  - `.agents/`, `.pi/`, `.claude/`, `.codex/`, `.cursor/`, `.cursorrules`, `.windsurfrules`, `.roo/`, `.cline/`, `.hermes/`, `.aider*`, `skills-lock.json`
- Ensure all repository `.gitignore` files include these patterns.

# MANDATORY GLOBAL FILE STRUCTURE (STRICT INVARIANT ACROSS ALL PROJECTS)
Always enforce and maintain exactly this clean, minimal, production-grade monorepo file structure across ALL projects (new and existing) locally and on GitHub. All files and directories (including optional items) MUST follow this exact layout without any extra files/folders:

```text
<repo-name>/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     # Lint, typecheck & test (frontend + backend)
│   │   ├── deploy.yml                 # Auto-deploy on push to main
│   │   └── codeql.yml                 # Automated security scanning (optional)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml             # Structured bug report form
│   │   ├── feature_request.yml        # Structured feature request form
│   │   └── config.yml                 # Disables blank issues / links to Discussions
│   ├── PULL_REQUEST_TEMPLATE.md       # Checklist for every PR
│   ├── CODEOWNERS                     # Auto-assigns reviewers per folder
│   ├── dependabot.yml                 # Auto-updates npm, pip, and GitHub Actions
│   ├── CONTRIBUTING.md                # How to set up & contribute
│   ├── CODE_OF_CONDUCT.md             # Community standards
│   ├── SECURITY.md                    # How to report vulnerabilities privately
│   ├── SUPPORT.md                     # Where to ask for help (optional)
│   ├── FUNDING.yml                    # Enables the GitHub Sponsor button (optional)
│   └── copilot-instructions.md        # Custom rules for GitHub Copilot (optional)
├── assets/                            # Brand logos, screenshots, diagrams
├── backend/                           # FastAPI (app/, tests/, pyproject.toml, .env.example)
├── deploy/                            # docker/ (Dockerfiles, compose) & hosting configs
├── docs/                              # architecture.md, setup.md, deployment.md
├── frontend/                          # Next.js (src/app, src/features, package.json, .env.example)
├── scripts/                           # DB seed, typegen, automation scripts
├── .editorconfig                      # Consistent indentation/line-endings across IDEs
├── .gitignore                         # Combined Node/Next.js + Python/FastAPI + OS rules
├── CHANGELOG.md                       # Version history & release notes (optional)
├── LICENSE                            # MUST stay in root for GitHub auto-detection
├── Makefile                           # Unified commands (make dev, make test, make build)
└── README.md                          # Project overview, badges, architecture, quickstart
```

- **Strict Root Discipline**: Root files MUST ONLY be: `.editorconfig`, `.gitignore`, `CHANGELOG.md`, `LICENSE`, `Makefile`, `README.md` (and any single config strictly required at root by the hosting provider). No other files or folders in root.
- **Latest Tech Stack**: Always use the latest stable versions of all tech stacks and dependencies (Next.js, React, Tailwind CSS, TypeScript, FastAPI, Python, Pydantic, etc.).
- **Docker & Deployment**: All Dockerfiles, compose files, and hosting configs MUST reside in `deploy/`.
- **Documentation**: All Markdown documentation (except root `README.md`, `LICENSE`, `CHANGELOG.md`, and community templates in `.github/`) MUST reside in `docs/`.


