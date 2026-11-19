---
name: testmu-ai
description: Run cross-browser automation, diagnose test failures, perform SmartUI visual regression audits, conduct WCAG accessibility evaluations, and orchestrate tests via HyperExecute on TestMu AI (formerly LambdaTest).
risk: low
source: official (testmuai.com/support/docs/testmu-mcp-server)
date_added: 2026-11-13
prompt-source: prompt.toon
---
skill: "testmu-ai"
sections[9]:
  - "# TestMu AI MCP (LambdaTest)\n\nConnect and drive end-to-end testing, visual regression comparisons, accessibility audits, and test orchestration on the TestMu AI (LambdaTest) platform via Model Context Protocol (`mcp-lambdatest`).\n\n"
  - "## Configuration & Authentication\n\n- **Server URL**: `https://mcp.lambdatest.com/mcp`\n- **Transport**: Remote HTTP (OAuth).\n- **Authentication**: On first invocation, Antigravity prompts a browser authentication flow to pair your TestMu AI / LambdaTest credentials. No manual API tokens need to be committed.\n\n"
  - "## Core Capabilities\n\n| Capability Suite | Description | Key Tools |\n| :--- | :--- | :--- |\n| **HyperExecute** | Generate test runner configurations and track distributed test jobs | `generateHyperExecuteConfig`, `getHyperExecuteJobStatus` |\n| **Automation Cloud** | Retrieve execution sessions, command logs, HAR files, and console logs | `getAutomationTestDetails`, `getAutomationLogs` |\n| **SmartUI** | Inspect visual diffs across pixel, layout, DOM, and perceptual dimensions | `analyzeSmartUIRun`, `summarizeSmartUILayoutDiff`, `summarizeSmartUIDomDiff` |\n| **Accessibility** | Audit web applications for WCAG 2.1/2.2 violations on public URLs or local tunnels | `getAccessibilityReport`, `analyseAppViaTunnel` |\n| **Test Manager** | Organize test cases, link execution statuses, and track milestone coverage | `manageTestCase` |\n\n"
  - "## Standard Workflow\n\n"
  - "### 1. Diagnosing Test Failures\n1. Identify the failing `test_id` from continuous integration logs.\n2. Call `getAutomationTestDetails` to inspect device, browser, OS, and status metadata.\n3. Call `getAutomationLogs` with `log_type=\"all\"` or `log_type=\"console\"` to retrieve command-level failures and browser console errors.\n4. Synthesize root cause and suggest code fixes.\n\n"
  - "### 2. SmartUI Visual Regression Debugging\n1. Given a `build_id`, run `analyzeSmartUIRun` for a complete breakdown of visual variations.\n2. For layout or structural regressions, execute `summarizeSmartUILayoutDiff` and `summarizeSmartUIDomDiff`.\n3. Separate intentional style changes from unintended layout shifts.\n\n"
  - "### 3. Accessibility (a11y) Auditing\n1. For production/staging URLs, run `getAccessibilityReport` with `standard=\"WCAG21AA\"`.\n2. For local dev applications, establish a secure tunnel and run `analyseAppViaTunnel`.\n3. Provide remediation suggestions with exact HTML/CSS and ARIA attribute repairs.\n\n"
  - "### 4. HyperExecute Orchestration\n1. Call `generateHyperExecuteConfig` specifying test framework (`playwright`, `cypress`, `selenium`), language, and desired parallel concurrency.\n2. Review and save the generated `.hyperexecute.yaml` in the target project.\n3. Track running executions via `getHyperExecuteJobStatus`.\n\n"
  - "## Constraints & Invariants\n\n- Respect Antigravity tool ceilings; only enable the required tool domains if hitting context quotas.\n- Always perform root-cause log inspection before proposing code or assertion modifications.\n- Do not bypass accessibility violations by loosening assertions without clear rationale.\n"
