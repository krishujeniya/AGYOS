---
name: adversarial-red-team
description: "SOP for the Gate 5 Red Team audit. Actively attempts to break the code, exploit vulnerabilities, and bypass guardrails before HITL approval."
category: security
version: "1.0.0"
author: "Krish Ujeniya"
---

# Adversarial Red Team Audit

> **Author**: Krish Ujeniya
> 
> This skill defines the mandatory security and vulnerability audit for Gate 5. 
> The executing agent adopts an adversarial persona ("Red Team") to proactively exploit the system and uncover flaws before the code is presented for Human-In-The-Loop (HITL) deployment approval.

## 1. Dependency Vulnerability Scan
- **Action**: Run deep audits on all package manifests.
- **Tools**: Use native ecosystem tools (e.g., `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`).
- **Gate**: Any critical or high vulnerabilities constitute an immediate fail.

## 2. Active Logic Exploitation
- **Action**: The agent must attempt to conceptually or programmatically break the implementation.
- **Vectors**:
  - **Injection**: Can SQL/NoSQL/Command injection bypass inputs?
  - **Auth/Authz**: Are endpoints properly protected? Can privilege escalation occur?
  - **State Manipulation**: Can race conditions or improper state handling corrupt data?
  - **XSS/CSRF**: Are frontend inputs sanitized?

## 3. Static Analysis & SAST
- **Action**: Run Static Application Security Testing (SAST) tools if available.
- **Focus**: Hardcoded secrets, insecure random number generation, insecure cryptography.

## 4. Audit Reporting
- **Deliverable**: Append findings to `.sovereign/verification.md`.
- **Format**:
  - 🔴 **VULNERABILITY FOUND**: [Description, Impact, Remediation]
  - 🟢 **SECURE**: [Area tested and verified]
- **Enforcement**: If any 🔴 vulnerabilities exist, the code is sent back to Gate 4. The HITL gate CANNOT be initiated until the Red Team signs off.
