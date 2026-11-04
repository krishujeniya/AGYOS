---
name: pentagi-orchestrator
description: "Autonomous multi-agent penetration testing orchestrator. Coordinates target reconnaissance, vulnerability analysis, exploit planning, and remediation reporting."
risk: offensive
source: community
author: "Krish Ujeniya"
---

# Autonomous Penetration Testing Orchestrator (PentAGI Pattern)

> **⚠️ AUTHORIZED USE ONLY**
> This skill is strictly for authorized security assessments, penetration tests, and defensive verification with written approval from system owners.

## Overview

The `pentagi-orchestrator` skill automates the full penetration testing lifecycle through coordinated multi-agent roles:
1. **Scoping & Rules of Engagement (RoE)**: Enforce boundary validation, target domain/IP lists, and forbidden targets.
2. **Reconnaissance & Surface Mapping**: Surface enumeration (subdomains, open ports, web frameworks, technology stacks).
3. **Vulnerability Assessment**: Automated CVE intelligence, configuration auditing, and exposed endpoint probing.
4. **Exploitation & Verification**: Controlled exploit execution in isolated sandboxes to verify impact without collateral damage.
5. **Remediation & Executive Reporting**: Generating executive summaries, technical findings with CVSS 3.1 / 4.0 scores, and reproduction steps.

---

## Architecture & Agent Roles

```
[TARGET SCOPE] ➔ [ORCHESTRATOR]
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
[RECON AGENT]   [RESEARCH AGENT]  [EXPLOIT AGENT]
  (Nmap/Gobuster)   (CVE/OSINT)     (Sandbox Runner)
       │                │                │
       └────────────────┼────────────────┘
                        ▼
               [REPORTING AGENT]
         (CVSS Metrics, Remediations)
```

### Agent Roles
- **The Orchestrator**: Maintains global task state, validates scope boundaries, and sequences test iterations.
- **The Reconnaissance Lead**: Executes passive OSINT, DNS resolution, port scans, and web technology identification.
- **The Vulnerability Researcher**: Cross-references service versions with known CVEs, public advisories, and Exploit-DB entries.
- **The Exploit Specialist**: Formulates exploit hypotheses, prepares tailored payloads, and tests them safely inside isolated environments.
- **The Remediation Analyst**: Verifies exploitability, rates business impact, and compiles clear developer remediation steps.

---

## Step-by-Step Workflow

### Phase 1: Target Definition and Boundary Enforcement
```bash
# Define target scope JSON
cat << 'EOF' > target-scope.json
{
  "target": "staging.example.com",
  "allowed_hosts": ["staging.example.com", "10.0.1.50"],
  "forbidden_hosts": ["prod.example.com", "auth.prod.example.com"],
  "test_window": "2026-11-04T00:00:00Z to 2026-11-04T23:59:59Z",
  "safe_mode": true
}
EOF
```

### Phase 2: Autonomous Reconnaissance Loop
1. Run non-intrusive DNS resolution and subdomain discovery:
   ```bash
   dig +short staging.example.com
   sublist3r -d staging.example.com -o subdomains.txt 2>/dev/null || true
   ```
2. Execute service and port discovery:
   ```bash
   nmap -sV -sC -T4 -p 80,443,8080,8443 staging.example.com -oN recon-ports.txt
   ```
3. Map web application routes and assets:
   ```bash
   gobuster dir -u https://staging.example.com -w /usr/share/wordlists/dirb/common.txt -q -o recon-dirs.txt
   ```

### Phase 3: Vulnerability Analysis & Exploit Verification
- Feed discovered services to `cve-vulnerability-intelligence`.
- Test input vectors with `ssrf-oob-interaction-testing` and `xxe-xml-injection-testing`.
- Execute tests inside the container using `security-sandbox-runner`.

### Phase 4: Finding Verification & Reporting
Every finding must include:
- **Title**: Clear vulnerability identification (e.g., *Blind SSRF in Webhook Registration Endpoint*).
- **Severity**: CVSS 3.1 score with vector string.
- **Affected Asset**: Specific URL, parameter, or port.
- **Proof of Concept (PoC)**: Minimal, non-destructive curl or script reproduction.
- **Remediation**: Concrete code-level or infrastructure mitigation.
