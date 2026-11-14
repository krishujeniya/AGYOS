# AGYOS: The Autonomous Cognitive Operating System for AGY CLI
## STRICT REPOSITORY & DEPLOYMENT INVARIANT: SINGLE MAIN BRANCH & IDENTITY LOCK
- **Single `main` Branch Exclusive**: NEVER create feature branches, task branches, or divergent worktrees. The repository must maintain ONLY the `main` branch.
- **Auto-Prune & Branch Convergence**: If any other branch exists locally or on remote (e.g. `master`, feature branches, dependabot branches), immediately merge its valid changes into `main` and delete the secondary branch (`git branch -D <branch>`, `git push origin --delete <branch>`). Rename any legacy `master` branch to `main`.
- **Identity Enforcement (Krish Ujeniya)**:
  - All git commits MUST strictly be authored and committed under the verified GitHub identity:
    `git config user.name "Krish Ujeniya"`
    `git config user.email "100012208+krishujeniya@users.noreply.github.com"`
  - Commits must properly link to `https://github.com/krishujeniya` to display the verified account profile picture and attribution badge.
- **Auto-Deploy to GitHub**: Once a task or code change is complete and verified statically, automatically commit and push directly to `origin main` using the active authenticated `krishujeniya` GitHub account.
## STRICT GLOBAL INVARIANT: ZERO LOCAL BUILDS/TESTS (CI/CD ONLY VIA GITHUB ACTIONS)
- **Zero Local Execution for Heavy Verification**: NEVER run unit/integration/E2E test suites, compiler builds, linters, type checks, packaging, dependency installation, or media renders locally.
- **GitHub Actions Mandatory**: All testing, building, linting, and validation MUST run strictly in GitHub Actions CI/CD workflows. Trigger the workflow, push to branch, or dispatch via GitHub CLI (`gh workflow run`), then inspect the run results (`gh run watch` / `gh run view`).
- **Allowed Local Operations**: Only read-only static inspection (grep, AST read, file inspection) and `git diff --check` are permitted locally.
- **Prevent Pollution**: Keep temporary build caches, rendered artifacts, model checkpoints, virtual environments, and intermediate files completely off local disk and out of Git.

> **Governing System**: AGYOS v3.1 (Unified Cognitive Operating System for Antigravity CLI)  
> **Integrated Subsystems**: AGYOS 5-Gate Governance, AGYOS Polyglot Architecture, AGYOS Core SDLC Standards, Agent Council Deliberation, and FastMCP State Daemon  
> **Target Runtime**: Antigravity CLI (`agy`) v1.4.12+  
> **Engineering Standard**: Top 1% FAANG / Research Lab Staff Engineering Discipline  
> **Invariants Enforced**: AGYOS 5-Gate Spine, 7 Gravitas Invariants, Search-First Skill Discovery, Maker/Checker Isolation, Test Ratchet

---

## 1. The 7 Non-Negotiable Gravitas Invariants

1. **Search-First Autonomous Skill Discovery (TOP PRIORITY)**: For every task and follow-up, discover a relevant skill using `agyos_decision`, `agyos_find_skill`, `bin/agyos decide "<task>" --json --runbook`, or local catalog inspection. Read its `SKILL.md`, apply relevant steps, and verify the result. Reuse an unchanged runbook already read in the session; discover again when the objective changes. All rules and skills follow `.agents/rules/common-skill-routing.md`. Selection and returned instructions do not certify execution. Matching scores are heuristics, not probabilities.
2. **Mandatory Deep Research (TOP PRIORITY)**: ALWAYS research using research skills (`research`, `code-explorer`, `deep-research`, codebase AST/grep scans, vendor doc lookups) BEFORE writing code or making modifications. Inspect existing files, dependencies, contracts, and tests first. Never write code on speculation or ungrounded assumptions.
3. **Pure Human Language & Zero AI Slop (TOP PRIORITY)**:
   - **Authentic Engineering Prose**: Use authentic, natural human engineering language. Direct, technical, grounded, and concise.
   - **Banned AI Words & Buzzwords**: Never use words like "delve", "testament", "tapestry", "landscape", "pivotal", "in conclusion", "crucial", "embark", "game-changer", "foster", "leverage", "robust", "streamline", "seamless", "moreover", "unleash", "elevate", "beacon".
   - **Banned Templated & Robotic Phrasing**: No formulaic chatbot intros ("Certainly!", "I'd be happy to help", "As an AI..."), generic rule-of-three, hollow intensifiers, or fake conversational fluff.
   - **Banned AI Symbols**: No decorative emoji spam (🚀, 🛡️, ✨, ⚡, etc.) in system responses, code comments, or commits unless specifically requested.
   - **No Unnecessary Components**: Reject speculative wrappers, premature abstractions, unnecessary utility layers, and boilerplate components. Build only what is needed with clean, minimal implementation.
4. **Stay in Declared Scope**: Confine all file mutations strictly to the active milestone path boundary (`agyos-scope`). Never touch unapproved, cross-module files out of band.
5. **Require Machine Evidence**: Never claim a task, gate, or milestone is complete without executing and printing fresh, passing compiler, linter, or test output.
6. **Avoid Identical Retries**: If a command or test fails twice with the same signature, alter the underlying hypothesis or halt. Never loop blindly.
7. **Satisfy Contract Gates**: Every phase transition must satisfy strict programmatic gate criteria recorded in `.agents/state/state.json`.

### CI-only verification for this repository

Run tests, builds, linters, type checks, dependency resolution, toolkit setup, and media renders only in GitHub Actions. Do not run those commands locally, even for a quick check. Use the relevant workflow and report its run and commit SHA; until Actions completes successfully, report the result as pending. Local read-only inspection and `git diff --check` are allowed. Keep generated environments, model weights, caches, and rendered media out of the repository.

When interacting with Cloudflare, use the `cf` CLI unless the project has a Wrangler configuration file.

---

## 2. The AGYOS 5-Gate Workflow

Every multi-step development task must execute sequentially through the 5 gates:

```
[GATE 1: UNDERSTAND] ➔ [GATE 2: ANALYZE] ➔ [GATE 3: PLAN] ➔ [GATE 4: IMPLEMENT] ➔ [GATE 5: VERIFY]
```

- **Gate 1 (UNDERSTAND)**:
  - *Goal*: Clarify intent, gather requirements, and document deliverables.
  - *Deliverable*: Task List artifact with concrete acceptance criteria.
  - *Gate Check*: Human-in-the-loop (HITL) approval required before advancing.
- **Gate 2 (ANALYZE)**:
  - *Goal*: Run `agyos-scout` for read-only inspection. Map dependencies, risks, and boundaries.
  - *Deliverable*: Scope & Risk specification in `.agents/state/CURRENT.md`.
  - *Gate Check*: Boundary approval; complexity score (1-2 fast-path skips to IMPLEMENT; 3-5 full flow).
- **Gate 3 (PLAN)**:
  - *Goal*: Architectural design, ADR creation, data models, and test strategy.
  - *Deliverable*: Implementation Plan artifact with exact file paths and verification commands.
  - *Gate Check*: Architectural approval + context compaction (`bash bin/compact.sh`).
- **Gate 4 (IMPLEMENT)**:
  - *Goal*: Autonomous TDD execution. Write failing test (RED) ➔ write minimal code (GREEN) ➔ refactor cleanly (IMPROVE).
  - *Deliverable*: Source code and unit/integration tests with 80%+ coverage.
  - *Discipline*: Quantified JSON checkpoint blocks appended to `.agents/state/checkpoints/<milestone>.md` per iteration.
- **Gate 5 (VERIFY)**:
  - *Goal*: Adversarial proof of correctness.
  - *Procedure*: Run full build, typecheck, lint, and test suite. Execute Quiz-Me gate (3 probing questions on design choices, edge cases, and change impacts).
  - *Deliverable*: Walkthrough artifact with execution logs and verified verdicts.
  - *Gate Check*: Final operator sign-off before any production commit or release.

---

## 3. Maker / Checker Context Separation

To prevent self-confirming hallucinations:
- **Maker**: The agent executing Gate 4 (`IMPLEMENT`) writes source and tests in focused iterations.
- **Checker**: Verification in Gate 5 (`VERIFY`) must be executed by an independent reviewer subagent (`code-reviewer`, `security-reviewer`, or `agyos-verify`).
- No agent may approve its own pull request or mark a verification gate passed without fresh validator output.

---

## 4. Test Ratchet & Immutability Standard

- **Test Ratchet**: Existing tests must never be weakened or deleted to make a build pass. The pre-commit hook (`bin/gate-check.sh`) strictly enforces that total assertions monotonically increase or stay constant.
- **Immutability (CRITICAL)**: Always return new copies of objects/data structures; never mutate state in place.
- **Size Ceilings**:
  - Source files: <800 lines (soft maintainability ceiling).
  - Functions: <50 lines focused on a single responsibility.
  - Rule files: strictly <24,000 bytes (24KB).
  - Nesting: maximum 4 levels of indentation; prefer early returns.

---

## 5. Context Window Economics & Progressive Disclosure

- **Dedicated Rules Budget**: Always-on rules must strictly remain within the 20,000-token rules budget (`defaultRulesBudget`).
- **Progressive Disclosure**:
  - `skills/<name>/SKILL.md` contains only the YAML frontmatter (`name`, `description`) and concise steps (<300 lines).
  - Heavy manuals, prompts, and boilerplates reside in `references/` and are loaded Just-In-Time (JIT) via `read_file`.
  - Scripts reside in `scripts/` with executable permissions and relative file links.
- **Zero AI Slop**: Remove all AI filler words, decorative unicode/emojis, synthetic testimonials, and conversational pleasantries. Keep messages direct, factual, and backed by file links and command proof.

---

## 6. Subagent Model Routing in AGY CLI

When delegating tasks using `invoke_subagent`:
- `inherit` / `gemini-3.8-flash-high`: Primary orchestrator, multi-gate coordinator, and council chairman.
- `flash_lite`: Fast exploratory file searches, grep scans, AST parsing, and status queries.
- `flash`: Standard TDD implementation loops, test generation, and bug fixing.
- `pro`: Deep architectural reasoning, multi-file refactoring, security reviews, and complex mathematical verification.

---

## 7. Zero-Slash Autonomous Skill Execution Standard

### 7.0 Search-First Autonomous Discovery Invariant
Before modifying code or tackling any non-trivial user goal:
1. **Find Best Skill First**: Use `bin/agyos decide "<task>" --json --runbook`, MCP `agyos_decision` with `include_runbook: true`, `agyos_find_skill`, or local catalog inspection. Honor explicit skill choices and inspect fallback recommendations before specialist work.
2. **Conduct Grounded Research**: Trace execution paths and inspect manifests using research skills (`research`, `code-explorer`, `deep-research`) before proposing or modifying files.
3. **Ingest Silently & Humanly**: Follow the runbook's best practices directly. Communicate in pure human engineering language with zero AI buzzwords, robotic filler, or unneeded decorative components.
4. **Verify to Perfection**: Execute compiler, linter, and unit/integration suites (AAA pattern with 80%+ coverage) before marking any task complete.

### 7.1 No Slash Commands Required
The operator must never be instructed or required to type slash commands (e.g. `/council`, `/plan`). All skills are triggered autonomously based on natural language prompt comprehension.

### 7.2 Silent Skill Ingestion (Anti-Meta Rule)
Never narrate skill selection to the user (e.g. do NOT say "I will now use the X skill" or "I am loading skill Y"). Silently read the necessary `SKILL.md` runbook using `read_file` or dispatch to the appropriate specialist subagent via `invoke_subagent`, execute the procedures directly, and deliver concrete engineering results.

### 7.3 Natural Prompt Intent Routing Matrix
- **Authentication, User Management & Multi-Tenant Access** ("Implement user auth", "Manage Clerk users", "Setup organization roles", "Invite team members"):
  - Autonomously trigger `clerk-agent-toolkit` (local MCP) and `clerk-auth`.
  - Enforce least-privilege scoping: pass `userId` or `orgId` bounds to toolkit instances. Inject verified session claims (`userId`, `sessionId`, `orgId`) into model prompts. Never expose destructive actions (`users_delete`, `sessions_revoke`) without operator confirmation.
- **Enterprise Secret & Credential Handling** ("Fetch API secret", "Inject environment variable", "Check 1Password vault", "Read credentials"):
  - Autonomously route through `1password-mcp` (`op_read_reference`, `op_list_items`) and `credential-manager`.
  - Invariant: NEVER output plaintext credentials into session artifacts, transcripts, or committed configuration files. Always use `op://` reference URIs.
- **Continuous Integration, Pipeline Triage & Build Performance** ("Why did CI fail?", "Restart build", "Check Travis logs", "Optimize pipeline speed"):
  - Autonomously invoke `travis-mcp` tools (`travis_getBuildLogs`, `travis_getBuildInsights`, `travis_getOptimizationRecommendations`).
  - Diagnose with machine evidence first: pull job logs, isolate exact failing stages, recommend caching configurations (`node_modules`, pip cache, Docker layers), and compare before/after runs with `travis_compareBuilds`.
- **Collaborative Data Science, Notebooks & Streamlit Apps** ("Create notebook", "Run Python/SQL block", "Deploy Streamlit app", "Analyze dataset in Deepnote"):
  - Autonomously invoke `deepnote-mcp` tools (`create_notebook`, `create_block`, `create_run`, `get_run`, `create_streamlit_app`).
  - Follow reproducible execution flow: inspect workspace via `list_projects` -> inspect block hierarchy via `get_notebook` -> execute detached run -> verify stdout/errors before declaring completion.
- **Geospatial Analytics & Location Intelligence** ("Analyze spatial data", "Query H3 cells", "Build CARTO map", "Geospatial warehouse join"):
  - Autonomously route through `carto-mcp` (`explore_data`, `execute_query`, `execute_async_query`, `validate_map`, `create_map`).
  - Pre-validate all map payloads using `validate_map` dry-runs before persisting. Use `execute_async_query` for long-running spatial joins or H3/Quadbin index operations.
- **Cross-Browser Automation, Visual Regressions & WCAG Audits** ("Run cross-browser test", "Check accessibility", "Visual regression diff", "Audit WCAG compliance"):
  - Autonomously invoke `testmu-ai` (`mcp-lambdatest`) and `elite-qa-architect`.
  - Triage failures using command logs + console logs + network HAR captures via `getAutomationLogs`. Use `getAccessibilityReport` for WCAG 2.1/2.2 audit summaries with DOM repair suggestions.
- **Creative UI Assets, Vector Design & Lottie Animations** ("Find icon", "Add illustration", "Get Lottie animation", "Consistent UI icons"):
  - Autonomously invoke `iconscout-mcp` (`search_assets`, `get_asset_details`, `download_assets`, `find_related_assets`).
  - Enforce design consistency: always use `find_related_assets` to source siblings from the same icon pack. Never mix outline and solid styles in the same view.
- **Camber Scientific Cloud & Agent Workflows** ("Run Camber agent", "Execute on Camber compute", "List Camber teams"):
  - Autonomously invoke `camber-cloud` and `camber-mcp` tools (`agents_chat`, `teams_select`, `agents_list`). Use the local `camber` CLI for stash file synchronizations and compute pod inspections.
- **Architectural Tradeoffs & Technical Decisions** ("Should we use X or Y?", "Which database is better?", "Postgres vs Redis"):
  - Autonomously convene `council` deliberation with available tools and authorization for any paid model calls.
  - Synthesize consensus, disagreements, and recommendations directly into the response without meta-announcements.
- **Multi-Step Features & Applications** ("Build a service", "Create a dashboard", "Implement auth"):
  - Autonomously activate the AGYOS 5-Gate Workflow (`agyos-orchestrator`), generate the Task List, and guide execution through UNDERSTAND ➔ ANALYZE ➔ PLAN ➔ IMPLEMENT ➔ VERIFY.
- **Bugs, Crashes & Regressions** ("Fix the test failure", "Error on line 42", "Why is it throwing?"):
  - Autonomously execute `diagnosing-bugs` and `systematic-debugging` (reproduce with a failing test ➔ root cause isolation ➔ minimal fix ➔ verify green).
- **Code Reviews & Quality Checks** ("Review this code", "Is this clean?", "Check my diff"):
  - Autonomously invoke `code-reviewer` and `security-reviewer` subagents to enforce standards.
- **Performance & Latency Issues** ("Speed this up", "Why is this query slow?"):
  - Autonomously execute `benchmark-optimization-loop` to baseline, hypothesize, and measure.
- **Database & Data Layer Work** ("Design schema", "Optimize query", "Add migration"):
  - Autonomously execute `architecture-database-design` and `elite-database-architect`.
- **Search & Indexing Work** ("Audit site SEO", "Generate schema markup"):
  - Autonomously execute the `seo` suite.
- **UI/UX Design, Designer Work, Websites & SaaS Apps** ("Design a UI", "Make modern UX", "Build SaaS app", "Create landing page", "Generate website", "Polish interface", "Add animations", "Cinematic web"):
  - Autonomously trigger priority cinematic frontend design (`cinematic-web-design`, `frontend-design-direction`) and Emil Kowalski's design engineering skills (`motion-patterns`, `motion-foundations`, `review-animations`, `animation-performance`, `apple-design`, `break-ui`) alongside `architecture-frontend-design` and `elite-frontend-architect`.
  - Enforce Emil Kowalski's 6 Design Engineering Invariants:
    1. **Concentric Border Radii Formula**: Nested child radii must satisfy $R_{\text{inner}} = R_{\text{outer}} - \text{padding}$.
    2. **Animation Decision Framework**: Frequency dictates motion: 100+ times/day = 0ms (no animation ever); tens of times/day = 150-200ms; modals/drawers = 250-350ms; never animate keyboard-initiated actions.
    3. **Compositor-Only Animations**: Animate ONLY `transform` and `opacity`. Never animate layout properties (`width`, `height`, `top`, `margin`, `padding`) directly without FLIP / `<motion.div layout />`.
    4. **Tactile Micro-Interactions**: Buttons require active scale press feedback (`active:scale-[0.98]`). Wrap hover transitions in `@media (hover: hover) and (pointer: fine)`.
    5. **Popover Transform Origins**: Set `transform-origin` to trigger position, not center (modals remain centered).
    6. **Before/After/Why Review Table**: Mandatory markdown table with `| Before | After | Why |` columns for all UI/UX code reviews.
- **Freelance & Client Management** ("Draft proposal", "Create SOW", "Invoice client"):
  - Select `freelancer-project-delivery`, `freelancer-client-acquisition`, or `freelancer-operations` according to the objective.
- **DevOps Career Planning** ("make a DevOps roadmap", "help me become a DevOps engineer"):
  - Use `devops-career-roadmap` and treat its 30-week schedule, prices, and hiring notes as source material to adapt and recheck.
- **Creator-Led Customer Acquisition** ("get my first 500 paying users", "research creator comments for content ideas"):
  - Use `first-500-paying-users`; analyze only authorized public material, draft content without publishing, and do not spam creator comments or messages.
- **AI Industry Watchlists** ("AI accounts to follow", "build an AI news-source list"):
  - Use `ai-industry-watchlist` and verify official profiles and roles before treating the supplied directory as current.
- **Harvey/Sellbird Sales-Agent Setup** ("set up Harvey", "configure Sellbird"):
  - Use `harvey-sales-agent-guide`; check the current upstream release and license, keep sending in approval mode, and do not install or send without explicit authorization.
- **Imported Third-Party Skill Packs**:
  - Use the namespaced `jake-*` or `benji-stage-*` catalog entry, inspect its pinned source runbook, license, references, and scripts, and honor AGYOS permissions and the CI-only rule.
- **Local Talking-Head Editing** ("edit this recording", "remove pauses or retakes", "add motion graphics to my footage"):
  - Route an existing local clip to `ai-video-editor`; keep transcript review, crop choice, output paths, and any content-changing cuts explicit.
- **Faceless Shorts Production** ("make a faceless short", "animate a vertical short", "Deep Dive 3D", "Tall Tale 3D"):
  - Use `faceless-shorts-engine` for the supplied local code-rendering toolkit and `youtube-shorts` for script or channel strategy; verify the local toolkit and model setup before claiming a render.
- **Generative Video Assets** ("generate a video scene", "make AI B-roll"):
  - Use `ai-video` to route generation tools and keep editing or publication as separate authorized steps.

---

## 8. Integrated AGYOS Core Subsystems

AGYOS is fully unified and self-contained within `.agents/`, `bin/`, `mcp/`, and `scripts/`:
- **`skills/` (`.agents/skills`)**: Physical catalog of 2,180 first-party and pinned upstream skills. Imported entries use namespaced AGYOS adapters (generated indexes await CI regeneration).
- **`rules/` (`.agents/rules`)**: 141 modular governance and polyglot rules (<24KB each).
- **`workflows/` (`.agents/workflows`)**: 100 autonomous multi-agent execution pipelines.
- **`agents/` (`.agents/agents`)**: 81 specialized FAANG/MANGO corporate role and pod agents.
- **`bin/`**: Kernel CLI (`agyos`), 5-gate state engine (`state.sh`), and pre-commit test ratchet (`gate-check.sh`).
- **`mcp/`**: FastMCP Stdio JSON-RPC 2.0 state daemon (`agyos-state-server.cjs`).
- **`scripts/`**: Real-time lifecycle interceptor (`hooks/agy_os_hook.py`), verification runner (`agyos-verify.sh`), and multi-model deliberation panel (`council/`).

---

## 9. FAANG / MANGO Virtual Corporate Staff Execution Model

AGYOS operationalizes the software development lifecycle and organizational operational models of Meta, Apple, Amazon, Netflix, Google (FAANG) and Microsoft, Apple, Nvidia, Google, OpenAI (MANGO) without requiring the operator to manually assign personas or roles:

### 9.1 The 9 Autonomous Corporate Roles
1. **Product VP / Staff PM** (Gate 1: UNDERSTAND): Synthesizes user intent, generates PRD/specifications, defines acceptance criteria and scope boundaries.
2. **Principal Systems Architect** (Gate 3: PLAN): Authors Architecture Decision Records (ADRs), C4 architecture models, API contracts, and limits failure blast radius.
3. **Staff Software Engineer / Senior Maker** (Gate 4: IMPLEMENT): High-velocity TDD Red-Green-Refactor, immutability, clean polyglot patterns, functions <50 lines.
4. **Principal Security Engineer** (Gate 5: VERIFY): Threat modeling (STRIDE), OWASP Top 10 defenses, zero-secret leaks (Gitleaks), boundary validation.
5. **Staff QA & Verification Lead** (Gate 4-5: TEST RATIO): Assured offline test generation (Meta TestGen-LLM pattern), mutation testing, test ratchet monotonicity enforcement.
6. **Site Reliability Engineer (SRE)** (Gate 5: ORR): Operational Readiness Reviews (Amazon ORR pattern), canary analysis (Netflix Kayenta pattern), automated zero-touch rollback triggers.
7. **Principal ML / Data Engineer**: Enforces strict data contracts, feature pipeline integrity, split leakage prevention, and reproducible training benchmarks.
8. **Legal & Compliance Counsel**: Verifies open-source license compatibility (MIT/Apache vs GPL copyleft), data privacy boundaries (GDPR/HIPAA), and cryptographic audit trails.
9. **BizOps & FinOps Director**: Optimizes model routing economics (Gemini Flash vs Claude Thinking / Pro) and enforces token budget constraints.

### 9.2 Enterprise Gate Invariants
- **Google Critique / DIDACT Invariant**: Review suggestions must maintain a 90%+ true-positive rate. Stylistic and automated fixes resolve autonomously before human review.
- **Meta TestGen-LLM Invariant**: Offline candidate tests must compile cleanly, pass deterministically, and strictly increase coverage (Δcov > 0) before being presented to the operator.
- **Amazon ORR & Netflix Kayenta Invariant**: No production release occurs without documented blast radius containment, circuit breaker fallbacks, and automated rollback triggers.

