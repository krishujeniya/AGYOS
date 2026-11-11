---
name: agyos-self-improvement
description: >-
  Use when maintaining the AGYOS skill catalog or improving a skill's correctness, discovery, references, or quality gates. Captures corrections, source checks, cross-skill dependencies, and test ratchets.
metadata:
  version: 1.0.1
license: MIT
---

# AGYOS Self-Improvement

Systematic protocol for keeping every skill in the AGYOS catalog accurate, current, and internally consistent. Triggered whenever a user correction arrives, new industry data surfaces, or a skill change ripples into dependents.

## When to Use This Skill

- A user corrects, refines, or extends any existing AGYOS skill
- Research reveals new techniques, deprecations, or industry shifts relevant to a skill
- A skill update creates stale cross-references in dependent skills
- End-of-session reconciliation of all changes applied during the conversation

---

## 1. Correction Capture Protocol

When a user provides a correction, addition, or refinement to any skill, execute every step in order.

### 1.1 Log the Correction

Append an entry to `.agents/state/corrections/CORRECTIONS_LOG.md` with this structure:

```markdown
## [YYYY-MM-DDTHH:MM:SSZ] <skill-name>

- **Category**: <category>
- **Section**: <section heading or "frontmatter">
- **Before**:
  ```
  <verbatim text replaced>
  ```
- **After**:
  ```
  <verbatim replacement text>
  ```
- **Rationale**: <one-line reason for the change>
```

### 1.2 Categorize the Change

Assign exactly one category per correction entry:

| Category | Use When |
|---|---|
| `factual_fix` | Incorrect information replaced with verified data |
| `principle_addition` | New principle, pattern, or technique added |
| `principle_removal` | Existing principle removed (requires explicit rationale) |
| `restructure` | Section reordering, heading changes, or layout refactoring |
| `cross_reference` | Adding, updating, or removing links to other skills |
| `workflow_update` | Changes to procedural steps, commands, or tool invocations |

### 1.3 Apply the Correction

1. Read the target `SKILL.md` file in full.
2. Apply the change using `edit_file` with exact `Target` matching.
3. Verify the edit landed correctly by re-reading the affected region.

### 1.4 Bump the Version

Increment the `metadata.version` patch number in the target skill's YAML frontmatter.

- `1.0.0` becomes `1.0.1` for a single correction.
- `1.0.1` becomes `1.0.2` for the next correction in the same session.
- Minor version bumps (`1.0.x` to `1.1.0`) require structural changes or 5+ corrections in one session.

### 1.5 Rebuild the Manifest

Run:

```bash
python3 scripts/build_tiered_skills_manifest.py
```

Verify the modified skill appears in the updated index output. If the script exits non-zero, diagnose and fix before continuing.

---

## 2. Trend Integration Protocol

When research or web search results reveal new industry developments relevant to an existing skill.

### 2.1 Cross-Check Existing Content

Read the target skill's full content. Compare new information against what is already documented. Skip if the skill already covers the development accurately.

### 2.2 Add New Principles or Techniques

- Insert new entries with an inline annotation: `[Added YYYY-MM-DD]`
- Place the addition in the most contextually appropriate section.
- If no section fits, create a new one and note it in the correction log.

### 2.3 Deprecate Outdated Techniques

- Do not silently remove any principle or technique.
- Annotate with: `[Deprecated YYYY-MM-DD: <reason>]`
- The annotated content stays in the skill for at least one version cycle.
- Removal happens in the next version bump, with an explicit `principle_removal` log entry.

### 2.4 Source Attribution

When adding information from research, include a brief source reference:

```markdown
- Use structured concurrency for goroutine lifecycle management [Added 2025-01-15] (ref: Go 1.24 release notes)
```

---

## 3. Cross-Skill Dependency Updates

When a skill changes, downstream skills that reference it may become stale.

### 3.1 Identify Dependents

1. Read the changed skill's "Related Skills", "Where This Connects", "See Also", or equivalent section.
2. Search the skills directory for files that reference the changed skill by name:

```bash
rg -l "<skill-name>" .agents/skills/ --glob "*.md"
```

### 3.2 Verify Each Cross-Reference

For every file returned:

1. Read the referencing section.
2. Confirm the reference still accurately describes the changed skill's purpose and content.
3. If stale, update the reference text.
4. Log the update as a `cross_reference` category correction.

### 3.3 Cascade Version Bumps

If a dependent skill's content changed (not just a reference URL), bump its patch version and rebuild the manifest.

---

## 4. Quality Gates

Run every gate before finalizing any self-improvement change. All gates must pass.

### 4.1 Banned-Word Lint

Scan the modified file for these 18 prohibited words (case-insensitive):

```
delve, testament, tapestry, landscape, pivotal, in conclusion, crucial,
embark, game-changer, foster, leverage, robust, streamline, seamless,
moreover, unleash, elevate, beacon
```

Command:

```bash
rg -i -c "(delve|testament|tapestry|landscape|pivotal|in conclusion|crucial|embark|game-changer|foster|leverage|robust|streamline|seamless|moreover|unleash|elevate|beacon)" <file>
```

Gate passes when the command returns no matches (exit code 1).

### 4.2 Decorative Emoji Check

Scan for decorative emoji usage. Emoji in code examples, Unicode references, or user-facing UI strings are acceptable. Decorative emoji in prose headings, bullet points, or descriptions are not.

```bash
rg -P "[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]" <file>
```

Review each match manually. Remove decorative instances.

### 4.3 YAML Frontmatter Validation

```bash
python3 -c "
import yaml, sys
with open(sys.argv[1]) as f:
    content = f.read()
if not content.startswith('---'):
    sys.exit('No frontmatter found')
fm = content.split('---', 2)[1]
data = yaml.safe_load(fm)
assert 'name' in data, 'Missing name'
assert 'description' in data, 'Missing description'
print('Frontmatter valid:', data.get('name'))
" <file>
```

### 4.4 Test Ratchet — Principle Count

Count the number of actionable principles, techniques, or rules in the skill before and after the change.

```bash
# Count lines starting with "- " under instruction sections
rg -c "^- " <file>
```

If the count decreased, the change requires an explicit written rationale in the correction log entry under `Rationale`. Without it, the gate fails and the change must be reverted.

### 4.5 Manifest Rebuild Verification

After running the manifest builder, verify:

1. The script exited with code 0.
2. The modified skill name appears in the output manifest.
3. No previously indexed skills disappeared from the manifest.

---

## 5. Session Learning Capture

At the end of any session where corrections were applied, write a summary.

### 5.1 Write the Session Summary

Create or append to `.agents/state/corrections/SESSION_SUMMARY.md`:

```markdown
## Session: YYYY-MM-DDTHH:MM:SSZ

### Skills Modified
| Skill | Version Before | Version After | Changes |
|---|---|---|---|
| <skill-name> | 1.0.0 | 1.0.1 | <brief description> |

### Principles Added
- <skill-name>: <principle text> [Added YYYY-MM-DD]

### Principles Deprecated
- <skill-name>: <principle text> [Deprecated YYYY-MM-DD: <reason>]

### Principles Removed
- <skill-name>: <principle text> (rationale: <reason>)

### Manifest Status
- Rebuild: SUCCESS / FAILURE
- Skills indexed: <count>
- Delta: +<added> / -<removed>

### Quality Gate Results
| Gate | Result |
|---|---|
| Banned-word lint | PASS / FAIL |
| Emoji check | PASS / FAIL |
| YAML validation | PASS / FAIL |
| Test ratchet | PASS / FAIL |
| Manifest rebuild | PASS / FAIL |
```

### 5.2 Summary Rules

- One summary per session, appended chronologically.
- If no corrections were applied, do not write a summary.
- Keep each summary under 50 lines.

---

## File Locations

| File | Purpose |
|---|---|
| `.agents/state/corrections/CORRECTIONS_LOG.md` | Append-only log of every correction applied |
| `.agents/state/corrections/SESSION_SUMMARY.md` | Per-session rollup of changes and gate results |
| `scripts/build_tiered_skills_manifest.py` | Manifest builder — re-run after every skill change |
| `.agents/skills/<name>/SKILL.md` | Individual skill files — targets of correction |

---

## Decision Record

| Decision | Rationale |
|---|---|
| Append-only correction log | Full audit trail; no silent rewrites of history |
| Deprecation before removal | Prevents accidental loss of valid techniques |
| Test ratchet on principle count | Guards against silent content erosion |
| Per-session summary cap of 50 lines | Keeps summaries scannable without losing signal |
| Single category per correction | Forces precise classification; avoids ambiguous multi-labels |
| Mandatory manifest rebuild | Ensures index consistency after every change |
