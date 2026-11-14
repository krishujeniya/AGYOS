---
name: testmu-ai
description: Run cross-browser automation, diagnose test failures, perform SmartUI visual regression audits, conduct WCAG accessibility evaluations, and orchestrate tests via HyperExecute on TestMu AI (formerly LambdaTest).
risk: low
source: official (testmuai.com/support/docs/testmu-mcp-server)
date_added: 2026-11-13
---
# TestMu AI MCP (LambdaTest)

Connect and drive end-to-end testing, visual regression comparisons, accessibility audits, and test orchestration on the TestMu AI (LambdaTest) platform via Model Context Protocol (`mcp-lambdatest`).

## Configuration & Authentication

- **Server URL**: `https://mcp.lambdatest.com/mcp`
- **Transport**: Remote HTTP (OAuth).
- **Authentication**: On first invocation, Antigravity prompts a browser authentication flow to pair your TestMu AI / LambdaTest credentials. No manual API tokens need to be committed.

## Core Capabilities

| Capability Suite | Description | Key Tools |
| :--- | :--- | :--- |
| **HyperExecute** | Generate test runner configurations and track distributed test jobs | `generateHyperExecuteConfig`, `getHyperExecuteJobStatus` |
| **Automation Cloud** | Retrieve execution sessions, command logs, HAR files, and console logs | `getAutomationTestDetails`, `getAutomationLogs` |
| **SmartUI** | Inspect visual diffs across pixel, layout, DOM, and perceptual dimensions | `analyzeSmartUIRun`, `summarizeSmartUILayoutDiff`, `summarizeSmartUIDomDiff` |
| **Accessibility** | Audit web applications for WCAG 2.1/2.2 violations on public URLs or local tunnels | `getAccessibilityReport`, `analyseAppViaTunnel` |
| **Test Manager** | Organize test cases, link execution statuses, and track milestone coverage | `manageTestCase` |

## Standard Workflow

### 1. Diagnosing Test Failures
1. Identify the failing `test_id` from continuous integration logs.
2. Call `getAutomationTestDetails` to inspect device, browser, OS, and status metadata.
3. Call `getAutomationLogs` with `log_type="all"` or `log_type="console"` to retrieve command-level failures and browser console errors.
4. Synthesize root cause and suggest code fixes.

### 2. SmartUI Visual Regression Debugging
1. Given a `build_id`, run `analyzeSmartUIRun` for a complete breakdown of visual variations.
2. For layout or structural regressions, execute `summarizeSmartUILayoutDiff` and `summarizeSmartUIDomDiff`.
3. Separate intentional style changes from unintended layout shifts.

### 3. Accessibility (a11y) Auditing
1. For production/staging URLs, run `getAccessibilityReport` with `standard="WCAG21AA"`.
2. For local dev applications, establish a secure tunnel and run `analyseAppViaTunnel`.
3. Provide remediation suggestions with exact HTML/CSS and ARIA attribute repairs.

### 4. HyperExecute Orchestration
1. Call `generateHyperExecuteConfig` specifying test framework (`playwright`, `cypress`, `selenium`), language, and desired parallel concurrency.
2. Review and save the generated `.hyperexecute.yaml` in the target project.
3. Track running executions via `getHyperExecuteJobStatus`.

## Constraints & Invariants

- Respect Antigravity tool ceilings; only enable the required tool domains if hitting context quotas.
- Always perform root-cause log inspection before proposing code or assertion modifications.
- Do not bypass accessibility violations by loosening assertions without clear rationale.
