# AGYOS Endpoint-Side Encrypted Exchange (v1)

## Security goal and exact scope

This feature protects **files deliberately encrypted at the sender endpoint and decrypted by a named trusted recipient endpoint**. It is a standalone, optional transport-independent envelope system. It does **not** turn the whole AGYOS agent runtime, AGY CLI, MCP state daemon, logging, cloud model requests, browser integrations, or existing plaintext session memory into E2EE. Do not describe AGYOS itself as fully end-to-end encrypted.

**Protocol design:** X25519 ephemeral sender key to X25519 recipient identity, HKDF-SHA256 with a per-message salt and versioned context, AES-256-GCM encryption with authenticated header metadata, and Ed25519 sender signature verified against a previously trusted public identity. Identity private keys use scrypt (N=32768, r=8, p=1) and AES-256-GCM at rest. Nonces, ephemeral keys and salts are randomly generated per message.

**Trust boundary:** Only two endpoints holding authorized private keys can decrypt a correctly addressed envelope, assuming those endpoints and private keys are not compromised, the peer public keys are independently authenticated, and the cryptographic primitives remain secure. A message created after a future compromise of a recipient's long-term private key may be at risk; this format has **no double ratchet, no post-compromise recovery, no replay protection, no key revocation infrastructure, and no forward secrecy against later compromise of the recipient's static private key**. The sender signature authenticates origin but does not prevent a previously observed envelope from being replayed.

**Threats not covered:** local malware, unlocked process memory, user-typed prompts given to cloud AI services, clipboard or shell history exposure, private data already committed to Git, external tools, and plaintext captured before encryption or after decryption. File names, sizes, identity fingerprints and envelope metadata are not hidden. Do not feed decrypted contents to a remote model unless separately authorized.

## Ubuntu / AGYOS use

Keep private keys under a user-owned directory such as `~/.config/agyos` (mode 0700). All outputs must be new file names; the CLI refuses to overwrite files.

1. Use a local password manager or a non-echoing prompt plus a private file descriptor. **Do not put the passphrase directly in command arguments, terminal history, environment variables, Git, or AI agent prompts.**
2. Create a separate identity on each machine:

```bash
# Run locally on each endpoint; input below is an interactive, non-echoing shell prompt.
read -rs -p "New AGYOS identity passphrase: " AGYOS_PASSPHRASE
printf '\n'
printf '%s' "$AGYOS_PASSPHRASE" | bin/agyos secure keygen --passphrase-fd 0
unset AGYOS_PASSPHRASE

bin/agyos secure public --out "$HOME/agyos-public.json"
```

3. Exchange **only public identity files** using a trusted communication channel. Compare the full SHA-256 public-identity fingerprint with your intended contact through a separate authenticated channel (for example, an in-person comparison). The CLI cannot establish peer trust automatically.
4. Encrypt at the sender endpoint:

```bash
read -rs -p "Identity passphrase: " AGYOS_PASSPHRASE
printf '\n'
printf '%s' "$AGYOS_PASSPHRASE" | bin/agyos secure encrypt --recipient /path/to/verified-recipient-public.json --in /path/to/private-data.txt --out /path/to/message.e2ee.json --passphrase-fd 0
unset AGYOS_PASSPHRASE
```

5. Only transfer `message.e2ee.json`. The receiving endpoint must have the **verified sender public key** before decrypting:

```bash
read -rs -p "Identity passphrase: " AGYOS_PASSPHRASE
printf '\n'
printf '%s' "$AGYOS_PASSPHRASE" | bin/agyos secure decrypt --sender /path/to/verified-sender-public.json --in /path/to/message.e2ee.json --out /path/to/recovered.txt --passphrase-fd 0
unset AGYOS_PASSPHRASE
```

A shell variable briefly contains the passphrase; prefer a password-manager pipe where available. The secret is never transmitted to the intended recipient or written to the repository by this CLI. Never run these examples through an AI tool that logs stdin or full shell requests.

## Verification

```bash
node --test scripts/tests/test_secure_envelope.cjs
bin/agyos secure help
```

Security cases: correct sender/recipient authenticated round-trip; wrong recipient, forged key, corrupted ciphertext/nonce/tag/signature, invalid identity password, key-file permissions, symlink rejection, overwrite refusal, and fresh ephemeral key/nonce generation.

These tests validate important implementation properties; they are not a formal cryptographic audit or proof of system-wide E2EE.

## Required work before any system-wide E2EE claim

- Classify every AGYOS data flow, including `.agents/state/memory.json`, checkpoints, `mcp/state-server.cjs`, the separate ECC memory vault, telemetry, council transcripts and model-provider prompts.
- Define which entities truly need plaintext. Remote AI inference inherently exposes plaintext to the inference endpoint unless confidential-computing or other separately verified techniques are used; encryption of the transport alone is not E2EE.
- Design authenticated device enrollment, multi-device key management, recovery, rotation, replay protection, revocation, and message ratcheting; independently review the protocol.
- For local-at-rest confidentiality, design a separate encrypted memory vault and migration of existing plaintext files, including backups, rollback and per-tool authorization. Do not silently encrypt tracked state files or break AGYOS verification.
- Red-team log leaks, model/tool prompt exfiltration, ciphertext parsing, malicious MCPs and key substitution. Perform an independent security review and test on the user's actual Ubuntu / AGY environment.

## Recovery

A lost identity passphrase or key makes previously encrypted messages unrecoverable by the CLI. Back up the encrypted identity file and passphrase safely and separately. Never publish the backup or recovery secrets. Existing AGYOS data and memory remain unchanged by this optional tool.
