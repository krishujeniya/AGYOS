---
name: security-sandbox-runner
description: "Containerized security tool execution runner. Safely executes security scanners (Nmap, Metasploit, SQLmap) in isolated environments with error recovery."
risk: safe
source: community
author: "Krish Ujeniya"
prompt-source: prompt.toon
---
skill: "security-sandbox-runner"
sections[6]:
  - "\n"
  - "# Security Tool Sandbox Runner (Isolated Container Execution)\n\n"
  - "## Overview\n\nThe `security-sandbox-runner` provides an execution loop for running offensive and defensive security utilities (e.g. `nmap`, `sqlmap`, `nikto`, `gobuster`, `ffuf`) within isolated Docker or sandboxed environments. It captures stdout/stderr streams, filters sensitive credentials, interprets tool errors, and enables autonomous agents to pivot commands without crashing the host.\n\n---\n\n"
  - "## Safety & Isolation Guarantees\n\n1. **Non-Root Execution**: Tools execute with limited user permissions inside ephemeral containers.\n2. **Resource Constraints**: CPU, memory, and timeout caps prevent runaway scans.\n3. **Network Boundary**: Scans are restricted to user-approved target IP ranges.\n4. **Structured JSON Output**: Translates tool logs into machine-readable findings.\n\n---\n\n"
  - "## Execution Workflow\n\n```bash\n# Run a scoped nmap scan inside an ephemeral container\ndocker run --rm   --network none   --memory 512m   --cpus 1.0   sec-sandbox-image   nmap -sV -p 80,443 target.local -oX /tmp/output.xml\n```\n\n"
  - "### Dynamic Error Recovery Loop\nWhen a command fails inside the sandbox:\n1. **Analyze Return Code**: Identify connection refusal, timeout, SSL error, or WAF block.\n2. **Adjust Technique**:\n   - Connection timeout ➔ Lower rate limit (`-T2` or `--delay 200ms`).\n   - WAF rate-limiting ➔ Add random user-agent and header rotation.\n   - SSL handshake failure ➔ Specify `--insecure` or alternate TLS version.\n3. **Re-execute**: Safely retry once with updated parameters. Never loop indefinitely.\n"
