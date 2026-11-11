---
name: openwhispr
description: >-
  Set up, use, troubleshoot, or integrate OpenWhispr desktop voice dictation,
  meeting transcription, notes, local/cloud speech models, or its MCP server.
  Use whenever the user mentions OpenWhispr, its desktop app, or connecting its
  notes and transcripts to an AI assistant.
source: https://github.com/OpenWhispr/openwhispr
license: MIT
metadata:
  version: 1.0.2
---

# OpenWhispr

Use this runbook for OpenWhispr desktop setup, privacy-aware transcription, and assistant integrations. Treat the [current product documentation](https://docs.openwhispr.com/) as authoritative for release formats, supported platforms, plans, model names, and client-specific configuration.

## Set up the desktop app

1. Ask which OS and whether the user wants the packaged app or a source checkout. Prefer the [official release](https://github.com/OpenWhispr/openwhispr/releases) for normal use.
2. Follow the [quickstart](https://docs.openwhispr.com/quickstart) and [platform requirements](https://docs.openwhispr.com/platform/system-requirements). Grant permissions only for features the user enables. On macOS, Microphone is needed for recording and Accessibility for automatic pasting. **System Audio** is needed to record other meeting participants; macOS lists this permission under Privacy & Security → Screen Recording, but OpenWhispr records meeting audio only and does not capture the screen. The separate **Screen Recording** permission is for optional voice-agent screen context, which sends a screenshot when enabled. See the [macOS permission guide](https://docs.openwhispr.com/platform/macos).
3. Choose the processing provider before handling private audio. Start with a short, non-sensitive test dictation in a scratch field; confirm the hotkey, microphone input, and paste destination.
4. If building the desktop app from source, re-check the current Node.js requirement, then follow the root README. It currently documents:

   ```bash
   git clone https://github.com/OpenWhispr/openwhispr.git
   cd openwhispr
   npm install
   npm run dev
   ```

   The Expo mobile app is a separate project under `openwhispr-mobile` with its own setup.

## Choose speech processing and check data flows

In Settings, inspect **AI Models → Speech-to-Text** separately for **Dictation**, **Note Recording**, and **Audio Upload**. Each activity has its own engine choice; a local setting for one does not make the others local.

- Choose a local model when audio must stay on the device. Downloading a model needs network access; transcription can run offline after download. Check disk and memory requirements in the [local-model guide](https://docs.openwhispr.com/guides/local-models).
- OpenWhispr Cloud sends audio to its service and model provider. Its privacy guide says it retains transcript text and metadata, not the cloud-processed recording. Check the current [data-flow guide](https://docs.openwhispr.com/help/privacy/where-your-data-goes) before handling sensitive material.
- OpenWhispr Cloud requests can also include the selected model, language, and custom dictionary terms. Check whether a dictionary contains client or project names before cloud transcription. The optional voice-agent screen-context feature sends a screenshot with that request to the configured model; confirm it is off unless requested.
- With a bring-your-own-key provider, requests go to the configured provider. Review that provider's data terms and billing. Do not describe this mode as offline or free.
- Self-hosted and managed enterprise modes have separate configuration and data paths; confirm the intended server or organization policy in the current documentation.
- The current privacy guide says notes and transcription history stay on-device by default and cloud backup is off; shared and team-space notes sync when shared. Review cloud backup, audio retention, and usage-analytics settings separately. A local transcription engine does not by itself mean every note or account feature stays local. Check all three speech-to-text tabs before recording or uploading.

## Connect an assistant through MCP

OpenWhispr documents a hosted Streamable HTTP MCP endpoint at `https://mcp.openwhispr.com/mcp`. Use its current [MCP setup guide](https://docs.openwhispr.com/integrations/mcp) and the selected client's supported configuration:

1. Claude and Claude Code use OAuth sign-in; review the permissions on the consent screen. The current MCP guide says Claude Connectors requests all documented scopes, so do not describe that flow as user-selectable least privilege.
2. Clients configured with API-key headers use a personal OpenWhispr API key. For those clients, grant only the scopes needed. Store the key in the MCP client's secret store or protected input mechanism; do not commit it, place it in a shared workspace file, or print it in logs.
3. Begin verification with read-only operations. For API-key clients, add write scopes only for requested note, dictionary, or snippet changes. Treat `delete_note` and other destructive actions as requiring explicit user authorization.
4. Confirm the endpoint and authentication method. For Claude Connectors OAuth, review the full permission request on the consent screen; a read-only smoke test does not limit the granted permissions. For API-key clients, verify the configured scope set. Start with a read-only request, such as listing recent notes; add API-key write scopes only when requested.

MCP exposes the user's notes, folders, transcripts, dictionary, snippets, and usage data; its audio transcription tool is documented as beta and subject to plan/scope limits. Confirm current scope names, limits, and response shape in the [MCP reference](https://docs.openwhispr.com/integrations/mcp). This skill does not imply that an MCP connection is already installed or authenticated.

## Troubleshoot and report accurately

- For a hotkey or paste issue, check platform-specific shortcuts and permissions in the [platform guides](https://docs.openwhispr.com/platform) and test in a plain text field.
- For poor recognition, confirm the selected speech-to-text tab, microphone, language, model download, and available disk/memory. Try another supported model only after checking current requirements.
- For meeting capture, verify the separate Note Recording engine and required OS permissions; test with consent from meeting participants.
- When reporting a fix, state which path was checked and what test actually succeeded. Do not claim private/local processing without verifying the setting for the specific activity.
- Before sharing logs, transcripts, screenshots, API responses, or recordings, remove credentials and personal or meeting data.

## Sources

- [OpenWhispr repository and MIT license](https://github.com/OpenWhispr/openwhispr)
- [Quickstart](https://docs.openwhispr.com/quickstart)
- [macOS permissions](https://docs.openwhispr.com/platform/macos)
- [Local models](https://docs.openwhispr.com/guides/local-models)
- [Voice and text data flows](https://docs.openwhispr.com/help/privacy/where-your-data-goes)
- [MCP server](https://docs.openwhispr.com/integrations/mcp)
