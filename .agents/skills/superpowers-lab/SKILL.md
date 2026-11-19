---
name: superpowers-lab
description: "Evaluate experimental Claude Code Superpowers Lab skills for duplicate-function discovery, on-demand MCP use, tmux interaction, or a Windows VM. Use only when the matching extension and prerequisites are installed."
risk: safe
source: "https://github.com/obra/superpowers-lab"
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "superpowers-lab"
sections[5]:
  - "\n"
  - "# Superpowers Lab\n\nThe upstream project contains experimental skills for Claude Code. This catalog entry does not make those extensions available in AGYOS by itself.\n\n"
  - "## Choose the relevant experiment\n\n- `finding-duplicate-functions`: investigate semantic code duplication; verify each proposed match before changing code.\n- `mcp-cli`: discover and invoke an MCP tool for a bounded task; inspect the server and tool schema before sending data.\n- `using-tmux-for-interactive-commands`: control an interactive CLI only when the host supports it and `tmux` is installed. Avoid unattended commands that can change repositories or remote state.\n- `windows-vm`: create or manage a Windows VM only with explicit permission, a known Docker/KVM setup, and a clear cleanup plan.\n\n"
  - "## Workflow\n\n1. Check the current [upstream skill list](https://github.com/obra/superpowers-lab) and confirm the requested experiment still exists.\n2. Verify the host plugin, tools, and prerequisites. If unavailable, do not imply that the capability is active or install it automatically.\n3. Define the files, servers, or VM resources the experiment may touch. Keep review read-only unless changes are authorized.\n4. Run a small, reversible task first. Inspect all tool output and changes before relying on the result.\n5. Report the experiment used, prerequisites met, changes made, and checks performed. The upstream project labels these skills experimental and subject to change.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
