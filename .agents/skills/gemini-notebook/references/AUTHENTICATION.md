# Authentication and Credential Management for Gemini Notebook

This document details credential extraction, storage modes, and session management for `notebooklm-mcp-cli` and `gemini-notebook-mcp`.

## Overview

Gemini Notebook (notebook.google.com) requires an active authenticated Google session. The integration automatically handles CSRF tokens and build labels when provided with session cookies.

## Extraction Methods

### Method 1: Chrome DevTools Network Tab (Recommended)

1. Open Google Chrome and navigate to `https://notebook.google.com/`.
2. Open Developer Tools (F12 or Ctrl+Shift+I / Cmd+Option+I) and select the **Network** tab.
3. Click any notebook or action to trigger an internal `batchexecute` request.
4. Select the `batchexecute` request in the Network list.
5. In Request Headers, copy the entire value of the `Cookie:` header.
6. Store the cookies in the AGYOS credential path:
   ```bash
   mkdir -p ~/.config/gemini-notebook-mcp
   echo -n "<PASTED_COOKIE_STRING>" > ~/.config/gemini-notebook-mcp/cookies
   chmod 600 ~/.config/gemini-notebook-mcp/cookies
   ```

### Method 2: Automated Login via nlm CLI

The `nlm` CLI provides interactive browser-assisted authentication:

```bash
bin/agyos nlm login
```

This launches a headless/CDP connection to extract cookies directly into your configuration profile.

### Method 3: Environment Variable

For non-interactive container or headless agent environments:

```bash
export NOTEBOOKLM_COOKIES="<PASTED_COOKIE_STRING>"
```

The launcher script [mcp/gemini-notebook-mcp.sh](file:///home/ai/Documents/projects/Freelance/AGYOS/mcp/gemini-notebook-mcp.sh) checks `NOTEBOOKLM_COOKIES` first, falling back to `~/.config/gemini-notebook-mcp/cookies`.

## Credential Storage Modes

`nlm` supports two local storage modes:

1. **Protected Storage (Recommended for personal workstations)**:
   Encrypts stored tokens using AES-GCM with keys maintained in the OS keychain:
   ```bash
   bin/agyos nlm auth storage set protected
   ```

2. **Plain Storage (Default for headless/server/container environments)**:
   Stores tokens with strict file permissions (`600`) in configuration directories:
   ```bash
   bin/agyos nlm auth storage set plain
   ```

## Multi-Account Profiles

Manage multiple Google accounts using profiles:

- List profiles: `bin/agyos nlm profile list`
- Switch active profile: `bin/agyos nlm profile switch <profile_name>`
- Create named profile: `bin/agyos nlm login --profile <profile_name>`
