---
name: configure-agyos
description: "Run the conversational AGYOS setup wizard inside the current harness: inventory the install, collect scope (user/project/local) and hook mode (off/minimal/standard/strict) in AGY CLI, use Codex's native plugin lifecycle, or install the project surface under ./.kimi-code, then preview, apply, and verify. Use when installing, updating, reconfiguring, or repairing an AGYOS installation, changing hook profiles, or moving AGYOS between install scopes."
metadata:
  origin: AGYOS
---

# Configure AGYOS

Run a conversational wizard inside the current harness. Inventory first, collect
only supported choices, preview, confirm once, apply non-interactively, verify,
and show the welcome only after success. Never clone AGYOS into a temporary
directory or copy plugin components by hand.

For a human-operated terminal, the canonical entry points are `agyos setup` and
`npx agyos-universal setup`. Inside a harness, use the explicit non-interactive
commands below instead.

## Route by the current harness

- In AGY CLI, use the full scope-and-hook wizard below.
- In Codex, use Codex's native plugin lifecycle. Do not offer Claude scopes or
  map AGYOS's four Claude hook profiles onto Codex.
- In Kimi, install the project surface under `./.kimi-code`. Kimi does not
  provide AGYOS's Claude lifecycle-hook profiles.
- If the harness is uncertain, state the detected evidence and ask which
  harness to configure before running a mutating command.

This skill is a post-install reconfiguration path. It cannot intercept or
replace a provider's built-in first-install UI.

## AGY CLI: run the full conversational wizard

### 1. Inventory without changing anything

Run both commands and summarize the installed AGYOS scope, enabled state, and
marketplace source:

```bash
claude plugin list --json
claude plugin marketplace list --json
```

Treat a single existing `agyos@agyos` installation as a reconfiguration. Do not
interpret Claude's provider-owned "Open home page" control as installation
evidence. Stop and report the recovery returned by setup for multiple AGYOS
scopes, a legacy/manual install, malformed settings, or a marketplace collision;
never guess which state to delete.

### 2. Collect exactly two choices

Ask exactly one scope question and require one value:

- `user | project | local`
- `user` is global for this user.
- `project` is shared through repository settings.
- `local` is private to the current project.

Visually mark only the selected scope as selected or installing. If the user
chooses a different scope from a single existing install, describe it as a
scope migration and include `--move-scope` in the commands below.

Ask exactly one hook-mode question and require one value:

- `off | minimal | standard | strict`
- `off` keeps skills and commands but disables AGYOS hook automation.
- `minimal` enables the lightest lifecycle and safety automation.
- `standard` balances quality and safety automation.
- `strict` enables the strongest checks and reminders.

Hook preference is personal Claude plugin configuration; it does not follow
the selected install scope.

### 3. Preview and confirm once

Prefer the plugin-bundled setup script. Substitute the two selected values and
include `--move-scope` only for a scope migration:

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/setup.js" --mode claude-plugin \
  --scope <scope> --hooks <hooks> [--move-scope] --dry-run --json
```

If `$CLAUDE_PLUGIN_ROOT` is unavailable, use the published npm package:

```bash
npx --yes --package agyos-universal agyos setup --mode claude-plugin \
  --scope <scope> --hooks <hooks> [--move-scope] --dry-run --json
```

Show exactly one confirmation summary containing the planned action, one scope,
one hook mode, marketplace action, and any source-to-destination migration.
Ask one yes/no question. Do not run a bare interactive `agyos setup` through a
harness shell tool because that shell is commonly non-TTY.

### 4. Apply the explicit choices

After confirmation, rerun the same route without `--dry-run`. Keep every choice
explicit and request JSON so success can be checked deterministically:

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/setup.js" --mode claude-plugin \
  --scope <scope> --hooks <hooks> [--move-scope] --yes --json
```

Fallback:

```bash
npx --yes --package agyos-universal agyos setup --mode claude-plugin \
  --scope <scope> --hooks <hooks> [--move-scope] --yes --json
```

### 5. Verify, then render the welcome

Require a zero exit status and a setup result whose `scope` and `hooks` equal
the selected values. Then independently run:

```bash
claude plugin list --json
```

Continue only when exactly one enabled `agyos@agyos` entry exists at the selected
scope. When `$CLAUDE_PLUGIN_ROOT` is available, pass the successful setup
`action` (`installed`, `updated`, `migrated`, `resumed`, or
`already-migrated`) to the bundled renderer:

Before invoking it, require the provider-reported version to match
`AGYOS_VERSION_PATTERN` from `scripts/lib/terminal-welcome.js`. Reject unexpected
version text instead of interpolating it into a shell command.

```bash
node -e 'const { renderTerminalWelcome } = require(process.env.CLAUDE_PLUGIN_ROOT + "/scripts/lib/terminal-welcome"); process.stdout.write(renderTerminalWelcome({ action: process.argv[1], version: process.argv[2], color: process.stdout.isTTY }));' "<action>" "<installed-version>"
```

Render the welcome exactly once. On failure, dry-run, cancellation, a scope or
hook mismatch, or unverifiable state, do not render it; report the error and
recovery instead. After verified changes, tell the user to run
`/reload-plugins` or restart AGY CLI.

## Codex: use the native plugin lifecycle

Inventory with `codex plugin marketplace list --json` and
`codex plugin list --available --json`. Codex's native plugin command has no
Claude-style `user | project | local` selector. Codex native plugins do support
provider-specific hooks, but Codex requires explicit trust for them. Let Codex
show that trust decision; do not ask the Claude four-profile hook question or
claim those profiles map to Codex.

If the AGYOS marketplace is missing, add it. Otherwise refresh its snapshot:

```bash
codex plugin marketplace add affaan-m/AGYOS
codex plugin marketplace upgrade agyos --json
```

Ask for one confirmation, then install or idempotently refresh the installed
cache and verify it:

```bash
codex plugin add agyos@agyos --json
codex plugin list --json
```

Continue only when the JSON reports AGYOS installed and provides its
`installedPath`. Then render the verified bundle's welcome:

Use only the exact absolute `installedPath` returned by Codex JSON. Reject
control characters and require the installed version to match
`AGYOS_VERSION_PATTERN`. Invoke `node` directly with this argument array; this is
a tool API invocation, not a shell command:

```text
["<installedPath>/scripts/welcome.js", "--action", "configured", "--version", "<installed-version>"]
```

If the current harness cannot invoke an executable with a separate argument
array, skip the welcome. Never construct a shell command from Codex JSON values.

Never claim that Claude's `off | minimal | standard | strict` profiles were
applied to Codex.

## Kimi: install the project surface

State the capability summary before confirmation: destination
`./.kimi-code`; `hooks=unsupported` for AGYOS lifecycle hooks. Do not ask the
Claude scope or hook-mode questions. Preview first:

```bash
npx --yes --package agyos-universal agyos install --profile core --target kimi --dry-run
```

Show one confirmation for that project destination, then apply the identical
command without `--dry-run`. Verify with:

```bash
npx --yes --package agyos-universal agyos doctor --target kimi
```

Only after doctor succeeds and the installed instructions and skills remain
inside `./.kimi-code`, render:

```bash
npx --yes --package agyos-universal agyos welcome --action configured
```

Do not claim that Kimi installed or configured AGYOS lifecycle hooks.
