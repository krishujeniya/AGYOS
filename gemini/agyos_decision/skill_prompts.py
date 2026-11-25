"""One-time migration of Markdown skill sections into TOON string fields."""
import json
from pathlib import Path
import re

from .catalog import FRONTMATTER

# These active prompts are unavailable. Preserve discovery metadata and attribution.
UNAVAILABLE = frozenset("""
broken-authentication network-101 security-audit
adversarial-red-team agyos-binary-analysis agyos-software-protection
api-security-testing application-security-testing ci-security-scanning-with-strix
ethical-hacking-methodology ffuf-web-fuzzing firmware-analyst
fix-security-vulnerabilities-with-strix managed-pentesting-with-strix malware-analyst
owasp-top-10-testing penetration-testing-with-strix pentagi-orchestrator
privilege-escalation-methods protocol-reverse-engineering scanning-tools
security-bounty-hunter shodan-reconnaissance sqlmap-database-pentesting
strix-api-security-testing top-web-vulnerabilities vulnerability-scanner
web-app-penetration-testing web-fuzzing-ffuf web-security-testing
jake-console-console-reverse jake-replica-replica-recon
""".split())


def quoted(text):
    return json.dumps(text, ensure_ascii=False)


def sections(body):
    """Split on Markdown headings outside fenced code, preserving every character."""
    parts = []
    start = 0
    fence = ""
    offset = 0
    for line in body.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if not fence:
                fence = token
            elif token.startswith(fence) and not line[marker.end():].strip():
                fence = ""
        elif not fence and re.match(r"^#{1,6}\s", line) and offset > start:
            parts.append(body[start:offset])
            start = offset
        offset += len(line)
    if start < len(body):
        parts.append(body[start:])
    return parts


def migrate_skill(manifest: Path, text: str):
    header = FRONTMATTER.match(text)
    if not header:
        raise ValueError(f"Missing frontmatter in {manifest}")
    name = manifest.parent.name
    body = text[header.end():]
    fields = [f"skill: {quoted(name)}"]
    if name in UNAVAILABLE or re.search(r"^risk:\s*offensive\s*$", header[1], re.M):
        fields.extend(["status: unavailable", "instruction: This entry has no operational instructions or tools. Refer defensive findings to the owner within written scope."])
    else:
        parts = sections(body)
        fields.append(f"sections[{len(parts)}]:")
        fields.extend("  - " + quoted(part) for part in parts)
    source = "\n".join(fields) + "\n"
    return f"---\n{header[1]}\nprompt-source: prompt.toon\n---\n{source}", source
