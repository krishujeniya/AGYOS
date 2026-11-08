# AGYOS Encryption Coverage & Key Lifecycle Analysis

**Document Status:** Live Security Specification  
**Assessment Date:** 2026-11-08  
**Audit Finding:** `PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE`  
**Governing Code:** `scripts/agyos-runtime/lib/private-vault.cjs`, `scripts/agyos-runtime/lib/e2ee.cjs`, `scripts/agyos-privacy-audit.py`

---

## 1. Executive Summary & Honest Security Boundary

AGYOS does **not** claim or provide universal, system-wide End-to-End Encryption (E2EE). In standard execution against cloud AI providers (Google Gemini, Anthropic Claude), prompts, system instructions, and tool schemas are transmitted in plaintext across TLS to the provider inference endpoint. Local operational files (`.agents/state/state.json`, `.agents/state/context-graph.json`, checkpoints) reside in standard filesystem storage.

AGYOS provides two verified, isolated cryptographic boundaries:
1. **At-Rest Private Memory Vault:** Authenticated AES-256-GCM encrypted key-value storage outside the repository with scrypt KDF and atomic writes (`private-vault.cjs`).
2. **Endpoint-to-Endpoint File Exchange Envelope:** Asymmetric X25519 key agreement, HKDF-SHA256 key derivation, AES-256-GCM AEAD payload encryption, and Ed25519 digital signature envelope for peer-to-peer file transfer (`e2ee.cjs`).

---

## 2. Subsystem Coverage Matrix

| Subsystem / Data Flow | Classification | Current Protection | Target Provider / Consumer | Verification Command |
|---|---|---|---|---|
| **MCP Private Memory Writes** | Confidential | `encrypted_at_rest` (AES-256-GCM, scrypt) | Local user process only | `node --test scripts/tests/test_private_vault.cjs` |
| **Legacy Memory Reads** | Internal/Confidential | `plaintext_local` (opt-out available via `AGYOS_MEMORY_PRIVATE_ONLY=1`) | MCP State Server | `python3 scripts/agyos-privacy-audit.py` |
| **File Exchange CLI (`bin/agyos secure`)** | Confidential | `encrypted_e2e` (X25519 + Ed25519 + AES-256-GCM) | Named peer endpoint | `node --test scripts/tests/test_secure_envelope.cjs` |
| **Agent Gate State (`state.json`)** | Operational metadata | `plaintext_local` (Git tracked) | AGYOS CLI, scripts | `python3 scripts/agyos-privacy-audit.py` |
| **Context Dependency Graph** | Code structure | `plaintext_local` (Git tracked) | AGYOS Graph skill, MCP | `python3 scripts/agyos-privacy-audit.py` |
| **Pre-Write File Snapshots** | Source code backup | `plaintext_local` (mode 0700 dir, mode 0600 file) | Authorizer hook | `python3 -m unittest scripts/tests/test_authorizer_hardening.py` |
| **Cloud Model Prompts / Responses** | Sensitive user intent | `encrypted_transport` (TLS 1.3), `provider_visible` | Google Gemini / Anthropic API | Host network inspect |
| **Local Stdio JSON-RPC (FastMCP)** | Command/Payload | Local OS pipe (IPC boundary) | AGY CLI host process | `node --test scripts/tests/test_mcp_protocol.cjs` |
| **Subprocess Decisions (`agyos-decision.py`)** | Task classification | Subprocess stdin/stdout pipe | Python runtime | `python3 -m unittest scripts/tests/test_skill_routing.py` |

---

## 3. Cryptographic Primitives & Specifications

### 3.1 At-Rest Memory Vault (`private-vault.cjs`)
- **Cipher:** `aes-256-gcm`
- **Key Derivation Function (KDF):** `scrypt` with parameters `N=32768, r=8, p=1`, random 32-byte salt per write.
- **Nonce:** 12-byte cryptographically secure random bytes generated per write.
- **Associated Authenticated Data (AAD):** `agyos-local-memory-vault-v1`
- **File System Permissions:** Enforcement of mode `0700` on parent directory and mode `0600` on vault file. Symlinks and paths within the repository boundary are strictly forbidden.
- **Passphrase Delivery:** Required via private file descriptor (FD 3–9) using `AGYOS_VAULT_PASSPHRASE_FD`. Zero-allocation memory clearing (`Buffer.fill(0)`) on passphrase buffer after key derivation.
- **Write Semantics:** Atomic replacement via temporary sibling file followed by `fs.renameSync` with cooperative locking.

### 3.2 Endpoint-to-Endpoint Secure Envelope (`e2ee.cjs`)
- **Key Agreement:** Elliptic Curve Diffie-Hellman over Curve25519 (X25519).
- **Digital Signatures:** Edwards-curve Digital Signature Algorithm over Ed25519.
- **Payload Cipher:** `aes-256-gcm` using a fresh ephemeral X25519 sender key per message.
- **Key Derivation:** HKDF-SHA256 (`info: agyos-secure-envelope-v1`) with random 32-byte salt.
- **Authentication Header:** AEAD Authenticated Data covers version, sender fingerprint, recipient fingerprint, sender public key, ephemeral public key, salt, nonce, and algorithm tag.
- **Identity Storage:** Encrypted private identity file using scrypt (`N=32768, r=8, p=1`) and `aes-256-gcm`.

---

## 4. Key Lifecycle & Recovery Runbook

### 4.1 Key Generation
1. Endpoints execute `bin/agyos secure keygen --passphrase-fd <FD>`.
2. Master identity is saved to `~/.config/agyos/identity.json` (or `$XDG_CONFIG_HOME`).
3. Permissions must be verified as user-only: `0600` (file) and `0700` (directory).

### 4.2 Key Distribution & Trust Establishment
- Only **public identity files** (`alice.pub.json`) may be transmitted.
- Fingerprints (SHA-256 of public key) must be validated out-of-band via an authenticated human channel (e.g., in-person or verified voice).
- Automated Trust-On-First-Use (TOFU) is disallowed by policy to prevent man-in-the-middle attacks.

### 4.3 Key Rotation
- **Vault Passphrase Rotation:** Read current vault via FD, re-encrypt under new passphrase via fresh FD, write atomically, destroy old passphrase memory.
- **Envelope Identity Rotation:** Generate new identity pair, issue signed transition advisory to authorized peers, decommission previous public key after message grace period.

### 4.4 Failure Modes & Fail-Closed Invariants
1. **Missing or Invalid Passphrase FD:** MCP server returns JSON-RPC error `-32000` (`Vault authentication required`). Plaintext fallback is forbidden.
2. **Ciphertext Tampering or Tag Mismatch:** Throws authentication error immediately; zero partial plaintext is returned or written.
3. **Corrupted Identity File:** Returns non-zero exit code without revealing filesystem internals or stack traces.
4. **Key Loss:** No backdoor, escrow, or administrative recovery key exists. Loss of passphrase/identity renders all historical ciphertexts permanently unrecoverable.

---

## 5. Remaining Security Gaps & Research Roadmap

1. **Host-Model Plaintext Exposure:** Inherent in remote LLM architectures. Solution requires confidential computing with hardware remote attestation (e.g., AMD SEV-SNP / Intel SGX) or localized small language models (SLM) executing entirely on-premise.
2. **Replay Resistance & Forward Secrecy:** The envelope format uses ephemeral sender keys but static recipient keys; compromise of recipient private key exposes past captured ciphertexts. Roadmap requires full Double Ratchet (Signal protocol) or MLS (RFC 9420) session management.
3. **Automated Plaintext Migration:** Transitioning existing legacy `.agents/state/memory.json` entries into the vault without breaking backward compatibility for older AGYOS components.
