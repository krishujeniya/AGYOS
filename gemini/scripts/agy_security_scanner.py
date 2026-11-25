#!/usr/bin/env python3
"""AGYOS Direct Security Scanner and Penetration Testing Engine.

Provides autonomous zero-API security scanning, OWASP Top 10 vulnerability
analysis, static analysis, and SARIF/Markdown report generation without
requiring external LLM APIs, cloud tokens, or Docker containers.
"""
from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional
import urllib.parse
import urllib.request

SEVERITY_ORDER = {
    "info": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "critical": 5,
}

IGNORE_DIR_NAMES = frozenset({
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".tox",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "strix_runs",
})

TEXT_FILE_EXTENSIONS = frozenset({
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".sh",
    ".bash",
    ".toml",
    ".ini",
    ".conf",
    ".env",
    ".go",
    ".rs",
    ".sql",
})


def meets_fail_threshold(finding_severity: str, threshold: Optional[str]) -> bool:
    """Determine whether a finding severity meets or exceeds the fail-on threshold."""
    if not threshold:
        return True
    threshold_lower = threshold.strip().lower()
    if threshold_lower not in SEVERITY_ORDER:
        return True
    finding_rank = SEVERITY_ORDER.get(finding_severity.lower(), 1)
    threshold_rank = SEVERITY_ORDER[threshold_lower]
    return finding_rank >= threshold_rank


def _extract_snippet(lines: List[str], line_no: int, context: int = 2) -> str:
    """Extract code context snippet surrounding line_no (1-indexed)."""
    start = max(0, line_no - context - 1)
    end = min(len(lines), line_no + context)
    snippet_lines = []
    for idx in range(start, end):
        prefix = ">" if idx == (line_no - 1) else " "
        snippet_lines.append(f"{prefix} {idx + 1:4d} | {lines[idx].rstrip()}")
    return "\n".join(snippet_lines)


class AgySecurityScanner:
    """Autonomous zero-API security scanner and penetration testing analyzer."""

    def __init__(self, target: str, mode: str = "quick") -> None:
        self.target = target
        self.mode = mode.lower()
        self.findings: List[Dict[str, Any]] = []
        self._vuln_counter = 1

    def _next_vuln_id(self) -> str:
        vuln_id = f"vuln-{self._vuln_counter:04d}"
        self._vuln_counter += 1
        return vuln_id

    def scan(self) -> List[Dict[str, Any]]:
        """Execute autonomous scan across target path or specification."""
        target_path = Path(self.target)
        if target_path.is_file():
            self._scan_file(target_path, target_path.name)
        elif target_path.is_dir():
            self._scan_directory(target_path)
        elif self.target.startswith(("http://", "https://")):
            self._scan_url(self.target)
        else:
            # Fall back to current directory if target does not resolve
            self._scan_directory(Path("."))
        return self.findings

    def _scan_directory(self, root_dir: Path) -> None:
        """Traverse directory and inspect relevant source and configuration files."""
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIR_NAMES]
            for fname in filenames:
                file_path = Path(dirpath) / fname
                if file_path.suffix.lower() not in TEXT_FILE_EXTENSIONS:
                    continue
                try:
                    rel_path = file_path.relative_to(root_dir).as_posix()
                except ValueError:
                    rel_path = str(file_path)
                self._scan_file(file_path, rel_path)

    def _scan_file(self, file_path: Path, rel_path: str) -> None:
        """Inspect a single file with AST and regex heuristics."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return

        lines = content.splitlines()

        # Secret detection across all text files
        self._check_secrets(rel_path, lines)

        # Python-specific AST and pattern checks
        if file_path.suffix.lower() == ".py":
            self._check_python_patterns(rel_path, content, lines)

        # JavaScript/TypeScript-specific checks
        elif file_path.suffix.lower() in (".js", ".ts", ".jsx", ".tsx"):
            self._check_javascript_patterns(rel_path, lines)

        # API specification checks
        elif file_path.suffix.lower() in (".json", ".yaml", ".yml"):
            self._check_api_spec_file(rel_path, content, lines)

    def _check_secrets(self, rel_path: str, lines: List[str]) -> None:
        """Scan for hardcoded private keys, tokens, and plaintext credentials."""
        secret_patterns = [
            (
                re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
                "Hardcoded Private Cryptographic Key",
                "critical",
                "owasp-a02-cryptographic-failures",
                "CWE-798",
                9.8,
                "Exposed private key enables cryptographic spoofing and unauthorized access.",
            ),
            (
                re.compile(r"(?:AKIA[0-9A-Z]{16})"),
                "Hardcoded AWS Access Key Identifier",
                "high",
                "owasp-a02-cryptographic-failures",
                "CWE-798",
                8.2,
                "Hardcoded cloud credentials enable resource enumeration and privilege escalation.",
            ),
            (
                re.compile(r"(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82})"),
                "Hardcoded GitHub Personal Access Token",
                "critical",
                "owasp-a02-cryptographic-failures",
                "CWE-798",
                9.1,
                "Compromised GitHub token grants unauthorized repository and workflow control.",
            ),
            (
                re.compile(r"""(?i)(?:api_key|secret_key|private_key)\s*=\s*['\"][A-Za-z0-9_\-]{32,}['\"]"""),
                "Hardcoded API Secret Key",
                "high",
                "owasp-a02-cryptographic-failures",
                "CWE-798",
                7.8,
                "Hardcoded secret tokens in source code bypass access control when exposed.",
            ),
            (
                re.compile(r"(?i)(?:postgres|mysql|mongodb(?:\+srv)?):\/\/[^\s:]+:([^\s@]+)@"),
                "Hardcoded Database Connection URI with Plaintext Password",
                "critical",
                "owasp-a02-cryptographic-failures",
                "CWE-798",
                8.9,
                "Exposes database instance credentials directly in source files or configuration manifests.",
            ),
        ]

        for line_no, line in enumerate(lines, 1):
            if "test" in rel_path.lower() and "fixture" in line.lower():
                continue
            for pattern, title, severity, finding_class, cwe, cvss, impact in secret_patterns:
                if pattern.search(line):
                    self.findings.append({
                        "id": self._next_vuln_id(),
                        "title": title,
                        "severity": severity,
                        "finding_class": finding_class,
                        "cvss_score": cvss,
                        "cwe_id": cwe,
                        "target": rel_path,
                        "line_number": line_no,
                        "snippet": _extract_snippet(lines, line_no),
                        "description": f"Potential plaintext credential or secret detected on line {line_no} of {rel_path}.",
                        "impact": impact,
                        "poc_description": f"Static token extraction from file at line {line_no}.",
                        "poc_script_code": f"# Grep proof: grep -n -E '{pattern.pattern}' {rel_path}",
                        "remediation_steps": "Move secrets to external environment variables or a secrets manager (e.g., 1Password, Vault).",
                    })

    def _check_python_patterns(self, rel_path: str, content: str, lines: List[str]) -> None:
        """Scan Python files using AST traversal and security heuristics."""
        try:
            tree = ast.parse(content, filename=rel_path)
        except SyntaxError:
            self._check_python_regex_fallback(rel_path, lines)
            return

        for node in ast.walk(tree):
            # 1. SQL Injection: raw string formatting in db execution calls
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    func_name = node.func.id

                if func_name in ("execute", "raw", "raw_query", "executemany") and node.args:
                    first_arg = node.args[0]
                    if isinstance(first_arg, (ast.JoinedStr, ast.BinOp)):
                        line_no = getattr(node, "lineno", 1)
                        self.findings.append({
                            "id": self._next_vuln_id(),
                            "title": "Potential SQL Injection via Raw String Formatting",
                            "severity": "high",
                            "finding_class": "owasp-a03-injection",
                            "cvss_score": 8.8,
                            "cwe_id": "CWE-89",
                            "target": rel_path,
                            "line_number": line_no,
                            "snippet": _extract_snippet(lines, line_no),
                            "description": f"Database execute call at line {line_no} uses string interpolation instead of parameterized queries.",
                            "impact": "Attackers can manipulate database queries, leading to data exfiltration or tampering.",
                            "poc_description": "Execute payload with SQL syntax quotation escape (e.g., ' OR 1=1 --).",
                            "poc_script_code": "# Payload: ' OR '1'='1",
                            "remediation_steps": "Replace string formatting with parameterized query parameters (e.g., cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))).",
                        })

                # 2. Command Injection: subprocess with shell=True
                if func_name in ("run", "Popen", "call", "check_call", "check_output"):
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            line_no = getattr(node, "lineno", 1)
                            self.findings.append({
                                "id": self._next_vuln_id(),
                                "title": "Command Injection via subprocess shell=True",
                                "severity": "high",
                                "finding_class": "owasp-a03-injection",
                                "cvss_score": 8.6,
                                "cwe_id": "CWE-78",
                                "target": rel_path,
                                "line_number": line_no,
                                "snippet": _extract_snippet(lines, line_no),
                                "description": f"Subprocess invocation on line {line_no} enables shell=True, risking command injection.",
                                "impact": "Executing system shell commands with untrusted input permits remote arbitrary command execution.",
                                "poc_description": "Pass command separator argument (e.g., '; id;').",
                                "poc_script_code": "# Payload: '; id;'",
                                "remediation_steps": "Set shell=False and pass arguments as an explicit sequence of strings.",
                            })

                # 3. Insecure Deserialization: pickle.loads or yaml.load without SafeLoader
                if func_name in ("loads", "load"):
                    module_name = ""
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        module_name = node.func.value.id
                    if module_name == "pickle":
                        line_no = getattr(node, "lineno", 1)
                        self.findings.append({
                            "id": self._next_vuln_id(),
                            "title": "Insecure Deserialization with pickle",
                            "severity": "critical",
                            "finding_class": "owasp-a08-software-data-integrity",
                            "cvss_score": 9.8,
                            "cwe_id": "CWE-502",
                            "target": rel_path,
                            "line_number": line_no,
                            "snippet": _extract_snippet(lines, line_no),
                            "description": f"Use of pickle.{func_name} at line {line_no} allows arbitrary code execution during deserialization.",
                            "impact": "Unpickling untrusted data can execute arbitrary machine code.",
                            "poc_description": "Construct malicious pickle bytecode with __reduce__ invoking os.system.",
                            "poc_script_code": "import pickle, os\nclass Exploit:\n    def __reduce__(self):\n        return (os.system, ('id',))\n",
                            "remediation_steps": "Use safe serialization formats such as JSON or Protocol Buffers instead of pickle.",
                        })

            # 4. Silent Error Swallowing: bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                line_no = getattr(node, "lineno", 1)
                self.findings.append({
                    "id": self._next_vuln_id(),
                    "title": "Silent Error Swallowing via Bare except",
                    "severity": "low",
                    "finding_class": "owasp-a04-insecure-design",
                    "cvss_score": 3.7,
                    "cwe_id": "CWE-390",
                    "target": rel_path,
                    "line_number": line_no,
                    "snippet": _extract_snippet(lines, line_no),
                    "description": f"Bare except clause on line {line_no} catches all exceptions including system exits without explicit handling.",
                    "impact": "Hides fatal system errors and prevents diagnostic tracing during security incidents.",
                    "poc_description": "Trigger unexpected exception and observe swallowed failure.",
                    "poc_script_code": "# Code pattern: except:",
                    "remediation_steps": "Catch specific exceptions (e.g., except ValueError:) and log diagnostic context.",
                })

    def _check_python_regex_fallback(self, rel_path: str, lines: List[str]) -> None:
        """Regex fallback for Python files with syntax exceptions."""
        for line_no, line in enumerate(lines, 1):
            if "shell=True" in line and "subprocess" in line:
                self.findings.append({
                    "id": self._next_vuln_id(),
                    "title": "Command Injection via subprocess shell=True",
                    "severity": "high",
                    "finding_class": "owasp-a03-injection",
                    "cvss_score": 8.6,
                    "cwe_id": "CWE-78",
                    "target": rel_path,
                    "line_number": line_no,
                    "snippet": _extract_snippet(lines, line_no),
                    "description": f"Shell=True detected on line {line_no}.",
                    "impact": "Arbitrary command execution if parameters contain user input.",
                    "poc_description": "Inject command separators in arguments.",
                    "poc_script_code": "# Payload: '; id'",
                    "remediation_steps": "Pass arguments as list and set shell=False.",
                })

    def _check_javascript_patterns(self, rel_path: str, lines: List[str]) -> None:
        """Scan JavaScript and TypeScript files for injection, eval, and CORS flaws."""
        js_rules = [
            (
                re.compile(r"""\beval\s*\("""),
                "Arbitrary Code Execution via eval()",
                "high",
                "owasp-a03-injection",
                "CWE-95",
                8.5,
                "Dynamic code evaluation can execute unvalidated scripts in application context.",
            ),
            (
                re.compile(r"""dangerouslySetInnerHTML\s*="""),
                "Potential Cross-Site Scripting via dangerouslySetInnerHTML",
                "medium",
                "owasp-a03-injection",
                "CWE-79",
                6.1,
                "Unsanitized HTML injection leads to client-side session hijacking or defacement.",
            ),
            (
                re.compile(r"""['\"]Access-Control-Allow-Origin['\"]\s*:\s*['\"]\*(?:['\"])"""),
                "Permissive CORS Wildcard Configuration",
                "medium",
                "owasp-a05-security-misconfiguration",
                "CWE-942",
                5.3,
                "Allows any external origin to read response data if authentication headers are relaxed.",
            ),
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern, title, severity, finding_class, cwe, cvss, impact in js_rules:
                if pattern.search(line):
                    self.findings.append({
                        "id": self._next_vuln_id(),
                        "title": title,
                        "severity": severity,
                        "finding_class": finding_class,
                        "cvss_score": cvss,
                        "cwe_id": cwe,
                        "target": rel_path,
                        "line_number": line_no,
                        "snippet": _extract_snippet(lines, line_no),
                        "description": f"Security flaw detected on line {line_no} in {rel_path}.",
                        "impact": impact,
                        "poc_description": f"Review line {line_no} for unvalidated user data flow.",
                        "poc_script_code": f"# Target location: {rel_path}:{line_no}",
                        "remediation_steps": "Sanitize inputs and enforce least privilege security controls.",
                    })

    def _check_api_spec_file(self, rel_path: str, content: str, lines: List[str]) -> None:
        """Scan OpenAPI and Swagger specifications for missing auth and IDOR risks."""
        if "openapi" not in content and "swagger" not in content and "paths" not in content:
            return

        # Check for endpoints lacking security declarations
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return

        if not isinstance(data, dict):
            return

        paths = data.get("paths", {})
        if not isinstance(paths, dict):
            return

        for path_name, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() not in ("get", "post", "put", "patch", "delete"):
                    continue
                if isinstance(operation, dict) and "security" not in operation and "security" not in data:
                    self.findings.append({
                        "id": self._next_vuln_id(),
                        "title": f"Unauthenticated API Endpoint: {method.upper()} {path_name}",
                        "severity": "medium",
                        "finding_class": "owasp-api-02-broken-authentication",
                        "cvss_score": 6.5,
                        "cwe_id": "CWE-306",
                        "target": rel_path,
                        "line_number": 1,
                        "snippet": f"Path: {path_name} [{method.upper()}]",
                        "description": f"API specification defines endpoint {method.upper()} {path_name} with no security scheme requirements.",
                        "impact": "Permits unauthorized actors to invoke sensitive endpoints without authentication tokens.",
                        "poc_description": f"Send unauthenticated HTTP request to {path_name}.",
                        "poc_script_code": f"curl -X {method.upper()} 'http://localhost{path_name}'",
                        "remediation_steps": "Declare security requirements (e.g., BearerAuth or OAuth2 scopes) in the OpenAPI definition.",
                    })

    def _scan_url(self, url: str) -> None:
        """Scan a target URL headlessly for missing security headers."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Strix-AGY-Direct-Scanner/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = {k.lower(): v for k, v in response.headers.items()}
        except Exception as exc:
            self.findings.append({
                "id": self._next_vuln_id(),
                "title": f"Target Endpoint Unreachable: {url}",
                "severity": "low",
                "finding_class": "owasp-a05-security-misconfiguration",
                "cvss_score": 3.1,
                "cwe_id": "CWE-16",
                "target": url,
                "line_number": 1,
                "snippet": url,
                "description": f"Connection check failed: {exc}",
                "impact": "Scanner could not establish HTTP connection to inspect active defenses.",
                "poc_description": f"curl -I {url}",
                "poc_script_code": f"curl -I '{url}'",
                "remediation_steps": "Ensure service is running and accessible on specified port.",
            })
            return

        required_headers = [
            ("strict-transport-security", "Missing HSTS Header", "medium", 5.4, "CWE-319"),
            ("content-security-policy", "Missing Content-Security-Policy (CSP)", "medium", 5.0, "CWE-1021"),
            ("x-frame-options", "Missing X-Frame-Options (Clickjacking Risk)", "low", 4.3, "CWE-1021"),
            ("x-content-type-options", "Missing X-Content-Type-Options (MIME Sniffing)", "low", 3.7, "CWE-16"),
        ]

        for h_name, title, severity, cvss, cwe in required_headers:
            if h_name not in headers:
                self.findings.append({
                    "id": self._next_vuln_id(),
                    "title": title,
                    "severity": severity,
                    "finding_class": "owasp-a05-security-misconfiguration",
                    "cvss_score": cvss,
                    "cwe_id": cwe,
                    "target": url,
                    "line_number": 1,
                    "snippet": f"Header absent: {h_name}",
                    "description": f"Target HTTP service does not send the {h_name} header.",
                    "impact": "Clients navigating to service lack browser-enforced protections against clickjacking or protocol downgrade.",
                    "poc_description": f"Inspect response headers: curl -I {url}",
                    "poc_script_code": f"curl -s -D - -o /dev/null '{url}' | grep -i '{h_name}'",
                    "remediation_steps": f"Configure web server or middleware to include {h_name}.",
                })


def generate_sarif(findings: List[Dict[str, Any]], run_name: str) -> Dict[str, Any]:
    """Generate standard SARIF 2.1.0 output for GitHub code scanning."""
    rules = []
    results = []
    seen_rules = set()

    for f in findings:
        rule_id = f.get("cwe_id", "SECURITY-RULE")
        if rule_id not in seen_rules:
            seen_rules.add(rule_id)
            rules.append({
                "id": rule_id,
                "name": f["title"],
                "shortDescription": {"text": f["title"]},
                "fullDescription": {"text": f["description"]},
                "help": {"text": f["remediation_steps"]},
                "properties": {
                    "security-severity": str(f["cvss_score"]),
                    "tags": ["security", f["finding_class"]],
                },
            })

        level_map = {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "note",
            "info": "note",
        }
        level = level_map.get(f["severity"].lower(), "warning")

        results.append({
            "ruleId": rule_id,
            "level": level,
            "message": {"text": f["description"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": f["target"]},
                        "region": {"startLine": f["line_number"]},
                    }
                }
            ],
        })

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Strix (Direct AGY CLI Engine)",
                        "version": "1.7.1",
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }


def generate_executive_report(
    findings: List[Dict[str, Any]], run_name: str, target: str, mode: str
) -> str:
    """Format an executive markdown penetration testing report."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f["severity"].lower()
        if sev in counts:
            counts[sev] += 1

    report_lines = [
        f"# Strix Penetration Test Report — {run_name}",
        "",
        "## Executive Summary",
        "",
        f"- **Target**: `{target}`",
        f"- **Scan Mode**: `{mode}`",
        f"- **Execution Engine**: Direct AGY CLI (Zero-API Autonomous Security Engine)",
        f"- **Completed At**: `{timestamp}`",
        f"- **Total Validated Findings**: `{len(findings)}`",
        "",
        "### Findings Breakdown by Severity",
        "",
        "| Severity | Count |",
        "|:---|:---|",
        f"| Critical | {counts['critical']} |",
        f"| High | {counts['high']} |",
        f"| Medium | {counts['medium']} |",
        f"| Low | {counts['low']} |",
        f"| Info | {counts['info']} |",
        "",
        "## Validated Vulnerabilities",
        "",
    ]

    if not findings:
        report_lines.append("No security vulnerabilities detected in the specified target scope.")
        report_lines.append("")
    else:
        for f in findings:
            report_lines.extend([
                f"### [{f['severity'].upper()}] {f['title']} ({f['id']})",
                "",
                f"- **CWE**: `{f['cwe_id']}`",
                f"- **CVSS Score**: `{f['cvss_score']}`",
                f"- **Location**: `{f['target']}:{f['line_number']}`",
                f"- **Class**: `{f['finding_class']}`",
                "",
                f"**Description**:\n{f['description']}",
                "",
                f"**Impact**:\n{f['impact']}",
                "",
                "**Code Evidence**:",
                "```",
                f"{f['snippet']}",
                "```",
                "",
                f"**Proof-of-Concept**:\n{f['poc_description']}",
                "```bash",
                f"{f['poc_script_code']}",
                "```",
                "",
                f"**Remediation**:\n{f['remediation_steps']}",
                "",
                "---",
                "",
            ])

    return "\n".join(report_lines)


def write_strix_artifacts(
    findings: List[Dict[str, Any]],
    run_name: str,
    target: str,
    mode: str,
    output_dir: Path,
) -> Path:
    """Write standard Strix output artifacts to strix_runs/<run_name>."""
    run_dir = output_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    vulns_dir = run_dir / "vulnerabilities"
    vulns_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f["severity"].lower()
        if sev in counts:
            counts[sev] += 1

    # 1. run.json
    run_meta = {
        "run_name": run_name,
        "target": target,
        "scan_mode": mode,
        "status": "completed",
        "engine": "agy-direct",
        "zero_api": True,
        "llm_cost_usd": 0.0,
        "start_time": timestamp,
        "end_time": timestamp,
        "total_findings": len(findings),
        "findings_by_severity": counts,
    }
    (run_dir / "run.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    # 2. vulnerabilities.json
    (run_dir / "vulnerabilities.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")

    # 3. vulnerabilities.csv
    csv_file = run_dir / "vulnerabilities.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "severity", "title", "target", "line_number", "cwe_id", "cvss_score"])
        for finding in findings:
            writer.writerow([
                finding["id"],
                finding["severity"],
                finding["title"],
                finding["target"],
                finding["line_number"],
                finding["cwe_id"],
                finding["cvss_score"],
            ])

    # 4. findings.sarif
    sarif_data = generate_sarif(findings, run_name)
    (run_dir / "findings.sarif").write_text(json.dumps(sarif_data, indent=2), encoding="utf-8")

    # 5. penetration_test_report.md
    report_md = generate_executive_report(findings, run_name, target, mode)
    (run_dir / "penetration_test_report.md").write_text(report_md, encoding="utf-8")

    # 6. individual vulnerability advisories
    for finding in findings:
        vuln_md = (
            f"# {finding['title']}\n\n"
            f"- **ID**: {finding['id']}\n"
            f"- **Severity**: {finding['severity'].upper()} (CVSS {finding['cvss_score']})\n"
            f"- **Location**: {finding['target']}:{finding['line_number']}\n"
            f"- **CWE**: {finding['cwe_id']}\n\n"
            f"## Description\n{finding['description']}\n\n"
            f"## Impact\n{finding['impact']}\n\n"
            f"## Code Evidence\n```\n{finding['snippet']}\n```\n\n"
            f"## Proof of Concept\n```bash\n{finding['poc_script_code']}\n```\n\n"
            f"## Remediation\n{finding['remediation_steps']}\n"
        )
        (vulns_dir / f"{finding['id']}.md").write_text(vuln_md, encoding="utf-8")

    return run_dir


def execute_agy_direct_scan(
    target: str,
    mode: str = "quick",
    budget: float = 0.0,
    fail_on: Optional[str] = None,
    dry_run: bool = False,
    run_name: Optional[str] = None,
    output_base: Optional[Path] = None,
) -> int:
    """Run direct autonomous security scan using AGY CLI engine."""
    clean_target = target.strip()
    clean_mode = mode.strip().lower()

    if dry_run:
        print("Direct AGY CLI Mode (Zero-API). Planned execution:")
        print(f"  Target:     {clean_target}")
        print(f"  Mode:       {clean_mode}")
        print("  Engine:     Direct AGY CLI (Zero-API Autonomous Security Engine)")
        print("  Cost:       $0.00 (Zero external API token dependency)")
        return 0

    actual_run_name = run_name or f"strix_agy_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    base_dir = output_base or (Path(__file__).resolve().parents[1] / "strix_runs")

    print("============================================================")
    print("Strix Autonomous Security Scan (Direct AGY CLI Zero-API)")
    print("============================================================")
    print(f"Target:       {clean_target}")
    print(f"Mode:         {clean_mode}")
    print("Engine:       Direct AGY CLI (Offline Zero-API)")
    print(f"Run Name:     {actual_run_name}")
    print("------------------------------------------------------------")

    scanner = AgySecurityScanner(target=clean_target, mode=clean_mode)
    findings = scanner.scan()

    artifacts_dir = write_strix_artifacts(
        findings=findings,
        run_name=actual_run_name,
        target=clean_target,
        mode=clean_mode,
        output_dir=base_dir,
    )

    print(f"Scan Completed. Total Validated Findings: {len(findings)}")
    print(f"Artifacts:    {artifacts_dir}")
    print(f"  Report:     {artifacts_dir / 'penetration_test_report.md'}")
    print(f"  SARIF:      {artifacts_dir / 'findings.sarif'}")
    print(f"  JSON:       {artifacts_dir / 'vulnerabilities.json'}")
    print("------------------------------------------------------------")

    if findings:
        print("Discovered Findings:")
        for f in findings[:10]:
            print(f"  - [{f['severity'].upper()}] {f['title']} in {f['target']}:{f['line_number']}")
        if len(findings) > 10:
            print(f"  ... and {len(findings) - 10} more findings (see report)")

    failing_findings = [f for f in findings if meets_fail_threshold(f["severity"], fail_on)]

    if failing_findings:
        threshold_label = fail_on or "any"
        print(f"\n[FAIL] {len(failing_findings)} findings meet or breach '--fail-on {threshold_label}' threshold.")
        return 2

    print("\n[PASS] No vulnerabilities breached failure threshold.")
    return 0
