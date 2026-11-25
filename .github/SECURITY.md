# Security Policy

## Supported Versions

We release patches and security fixes for the latest release on the `main` branch.

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

## Endpoint-Side Encrypted File Exchange & Boundaries

AGYOS provides optional endpoint-side file encryption (`gemini/antigravity-cli/bin/agyos secure`, implemented in `gemini/antigravity-cli/scripts/agyos-runtime/lib/e2ee.cjs`) and an optional encrypted local memory vault (`~/.local/state/agyos/private-memory.vault.json`, implemented in `gemini/antigravity-cli/scripts/agyos-runtime/lib/private-vault.cjs`).

- **Cryptographic Construction:** X25519 ephemeral key agreement, HKDF-SHA256 with per-message random salt, AES-256-GCM authenticated encryption, Ed25519 sender signature, and scrypt (`N=32768, r=8, p=1`) key derivation for private identity files (mode `0600`).
- **Explicit Trust Boundary (`PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE`):** AGYOS is **not** system-wide end-to-end encrypted. Checked-in operational state (`gemini/antigravity-cli/state/state.json`, checkpoints, decision receipts), FastMCP stdio traffic, shell arguments, and prompts submitted to cloud LLM providers remain plaintext. Never store credentials, tokens, or private keys in repository files.
- **No Post-Compromise Forward Secrecy or PKI:** Verify peer SHA-256 identity fingerprints out-of-band before encrypting or decrypting. No independent external cryptographic audit has been performed.

### Encrypted Envelope CLI Usage

```bash
# Generate local identity and export public key
read -rs -p "Identity passphrase: " AGYOS_PASSPHRASE; printf '\n'
printf '%s' "$AGYOS_PASSPHRASE" | gemini/antigravity-cli/bin/agyos secure keygen --passphrase-fd 0
unset AGYOS_PASSPHRASE
gemini/antigravity-cli/bin/agyos secure public --out "$HOME/agyos-public.json"

# Verify implementation in CI or inspect CLI help
node --test gemini/antigravity-cli/scripts/tests/test_secure_envelope.cjs
node --test gemini/antigravity-cli/scripts/tests/test_private_vault.cjs
gemini/antigravity-cli/bin/agyos secure help
uv run python gemini/antigravity-cli/scripts/agyos-privacy-audit.py
```
