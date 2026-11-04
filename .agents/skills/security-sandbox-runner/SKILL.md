---
name: security-sandbox-runner
description: "Containerized security tool execution runner. Safely executes security scanners (Nmap, Metasploit, SQLmap) in isolated environments with error recovery."
risk: safe
source: community
author: "Krish Ujeniya"
---

# Security Tool Sandbox Runner (Isolated Container Execution)

## Overview

The `security-sandbox-runner` provides an execution loop for running offensive and defensive security utilities (e.g. `nmap`, `sqlmap`, `nikto`, `gobuster`, `ffuf`) within isolated Docker or sandboxed environments. It captures stdout/stderr streams, filters sensitive credentials, interprets tool errors, and enables autonomous agents to pivot commands without crashing the host.

---

## Safety & Isolation Guarantees

1. **Non-Root Execution**: Tools execute with limited user permissions inside ephemeral containers.
2. **Resource Constraints**: CPU, memory, and timeout caps prevent runaway scans.
3. **Network Boundary**: Scans are restricted to user-approved target IP ranges.
4. **Structured JSON Output**: Translates tool logs into machine-readable findings.

---

## Execution Workflow

```bash
# Run a scoped nmap scan inside an ephemeral container
docker run --rm   --network none   --memory 512m   --cpus 1.0   sec-sandbox-image   nmap -sV -p 80,443 target.local -oX /tmp/output.xml
```

### Dynamic Error Recovery Loop
When a command fails inside the sandbox:
1. **Analyze Return Code**: Identify connection refusal, timeout, SSL error, or WAF block.
2. **Adjust Technique**:
   - Connection timeout ➔ Lower rate limit (`-T2` or `--delay 200ms`).
   - WAF rate-limiting ➔ Add random user-agent and header rotation.
   - SSL handshake failure ➔ Specify `--insecure` or alternate TLS version.
3. **Re-execute**: Safely retry once with updated parameters. Never loop indefinitely.
