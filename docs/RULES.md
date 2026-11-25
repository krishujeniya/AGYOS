# Rules and Standards

## Structure

AGYOS stores `148` modular rules directly under `gemini/antigravity-cli/builtin/rules/` using Token-Oriented Object Notation (`.toon`) envelopes alongside the priority baseline `00-priority-rules.md`:

```text
gemini/antigravity-cli/builtin/rules/
├── 00-priority-rules.md             # Global invariants (single main branch, uv-only, security)
├── agyos-*.toon                     # AGYOS lifecycle, handoff, legal/DSAR gates, memory & prompt principles
├── common-*.toon                    # Language-agnostic defaults (coding-style, git-workflow, testing, security, skill-routing)
├── python-*.toon                    # Python conventions & testing
├── golang-*.toon                    # Go conventions & testing
├── typescript-*.toon                # TypeScript / JavaScript conventions
├── angular-*.toon                   # Angular conventions
├── swift-*.toon                     # Swift conventions
├── php-*.toon                       # PHP conventions
└── ...                              # Framework & domain rule packs (148 total files)
```

- **`00-priority-rules.md` and `common-*.toon`** define repository-wide invariants and universal engineering defaults.
- **Subsystem rules (`agyos-*.toon`)** govern autonomous cycles, gate verdicts, handoffs, security boundaries, and prompt hygiene.
- **Language and framework rules (`<lang>-*.toon`)** extend or specialize the common rules for specific tech stacks.

## Rules vs Skills

- **Rules** (`gemini/antigravity-cli/builtin/rules/`) define standing standards, constraints, and checklists that apply across tasks (for example `common-skill-routing.toon`, `agyos-git-workflow.toon`, `agyos-security.toon`).
- **Skills** (`gemini/antigravity-cli/builtin/skills/<skill-name>/SKILL.toon` + `prompt.toon`) provide task-specific runbooks discovered on demand via `gemini/antigravity-cli/bin/agyos decide "<task>" --json --runbook` or `gemini/antigravity-cli/bin/agyos find "<query>"`.

Rules state *what invariants and standards must hold*; skills provide *how to execute a specific task*.

## Rule Priority

1. Global priority invariants (`gemini/antigravity-cli/builtin/rules/00-priority-rules.md`) and explicit user instructions take highest precedence.
2. Language- or framework-specific rules override generic `common-*.toon` defaults when language idioms differ.
3. Domain runbooks in `gemini/antigravity-cli/builtin/skills/` never override higher-priority authorization, scope, or repository safety rules.
