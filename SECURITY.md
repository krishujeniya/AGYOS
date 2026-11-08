# Security Policy

## Supported Versions
We release patches and security fixes for the latest release on the  branch.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability
We take the security of our software and autonomous agent systems seriously. If you believe you have discovered a vulnerability, please report it responsibly.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities directly to the maintainer via:
- GitHub Private Vulnerability Reporting / Security Advisory
- Contact: Krish Ujeniya (@krishujeniya)

Include detailed reproduction steps, proof of concept, and affected environment. We will acknowledge receipt within 48 hours and work with you to remediate the issue prior to public disclosure.

## Endpoint-Side Encrypted File Exchange

The optional encrypted-envelope CLI is described in [docs/security/END_TO_END_ENCRYPTION.md](docs/security/END_TO_END_ENCRYPTION.md). No system-wide end-to-end encryption guarantee is made: AGYOS memory, model requests and external tools remain outside this envelope. Verify peer fingerprints out-of-band. Keep private identities and passphrases off Git, AGYOS chat, remote models and logs. A compromised endpoint can still reveal plaintext, and long-lived X25519 recipient keys do not supply full post-compromise forward secrecy. Report cryptographic findings using private vulnerability reporting.
