---
name: council-replay
description: |
  Replay a past Agent Council session in the terminal. Shows the full
  deliberation: question, each agent's opinion, and the chairman's synthesis.
allowed-tools:
  - Bash
prompt-source: prompt.toon
---
skill: "council-replay"
sections[4]:
  - "\n"
  - "# Council Replay\n\nReplay a past council deliberation session in the terminal.\n\n"
  - "## Usage\n\nThe user invokes `/council-replay <session-id>`.\n\n"
  - "## Run\n\nReplace `{SESSION_ID}` with the session ID the user provided.\n\n```bash\nCOUNCIL_BIN=\"\"; for _d in \"$HOME/.claude/skills/agent-council\" \"$HOME/.agents/skills/agent-council\" \"$HOME/.gemini/skills/agent-council\" \"$(git rev-parse --show-toplevel 2>/dev/null)\"; do [ -x \"$_d/bin/council\" ] && COUNCIL_BIN=\"$_d/bin/council\" && break; [ -x \"$_d/council\" ] && COUNCIL_BIN=\"$_d/council\" && break; done; [ -z \"$COUNCIL_BIN\" ] && COUNCIL_BIN=\"$(which council 2>/dev/null || echo \"bin/council\")\"\nSLUG=$(basename \"$(git rev-parse --show-toplevel 2>/dev/null || pwd)\")\n$COUNCIL_BIN replay {SESSION_ID} --project \"$SLUG\"\n```\n\nAfter the replay, tell the user:\n\n> **Next steps:**\n> - Re-run with current context: `/council-revisit <session-id>`\n> - Record outcome: `/council-outcome <session-id> \"what happened\"`\n> - Open viewer: `open ~/.council/{project}/{session-id}/viewer.html`\n"
