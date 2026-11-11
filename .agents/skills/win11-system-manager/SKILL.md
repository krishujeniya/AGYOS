---
name: win11-system-manager
description: "Update GitHub Spec Kit templates and manifests in a project. Legacy catalog ID: win11-system-manager; this skill does not manage Windows settings."
risk: safe
source: "https://github.com/NotMyself/claude-win11-speckit-update-skill"
date_added: "2026-02-27"
---

# GitHub Spec Kit updates

Despite its legacy catalog ID, this skill covers updating GitHub Spec Kit files in a project; it does not provide general Windows 11 system administration.

## Workflow

1. Inspect the project for Spec Kit files, its update manifest, local customizations, and existing backups. Record the current revision and worktree status.
2. Treat the upstream project as archived and read-only since 2026-02-01. Its documented environment is Windows 11, PowerShell 7+, Git, Claude Code, and Internet access for GitHub API requests; do not assume it supports AGYOS or has maintained current documentation.
3. Run a check-only or dry-run mode first when the installed updater supports it. Review the full file list and diff before any update.
4. Before writing, confirm the requested version and obtain explicit approval for the update. Preserve customized files and keep a recoverable backup; do not use force or skip-backup options by default.
5. Apply the update only to the approved project paths. Verify the manifest, changed templates, and project tests. If verification fails, restore from the recorded backup and report the result.

The [archived upstream updater](https://github.com/NotMyself/claude-win11-speckit-update-skill) documents check-only, version selection, approval, and rollback flows. Validate the installed version and its actual interface before use.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
