# AGYOS encrypted envelope exchange — security boundary

**Scope: encrypted files exchanged between two independently keyed AGYOS endpoints.** This is *not* blanket end-to-end encryption for the AGYOS operating system. Existing FastMCP stdio, memory JSON, task state, model-provider prompts/responses, shell arguments, telemetry, browser plugins, GitHub, and cloud tools are not transported through this envelope. Never describe the whole system as E2EE until each data flow has an endpoint/key architecture and dedicated verification.

## Cryptographic construction

- Each endpoint generates an X25519 agreement private/public key pair and an Ed25519 signing private/public pair using Node.js crypto. Private key DER material is encrypted in an on-disk identity file with scrypt (N=32768, r=8, p=1, random 32-byte salt) and AES-256-GCM with a fresh 96-bit nonce. The key is not committed.
- Every message creates a fresh ephemeral X25519 key pair and random 32-byte HKDF salt, derives a new 256-bit AES-GCM key using X25519 shared secret and HKDF-SHA-256 with protocol domain separation, and uses a random 96-bit nonce.
- The version, sender and recipient fingerprints, sender public key, ephemeral public key, salt, nonce and algorithm identifier are included in the authenticated header (AEAD AAD). The header, ciphertext and authentication tag are signed with Ed25519. Decryption requires the pretrusted sender public key and a matching recipient private identity, verifies the signature, then authenticates the ciphertext.
- Identities are generated locally, never sent to a host. Private identity files are created with mode 0600 in mode-0700 directories and require the same restrictions when opened. The recipient must compare the sender's SHA-256 fingerprint through an independent authenticated channel before accepting a key.
- Envelopes are JSON blobs and can traverse an untrusted file transfer or storage service. This implementation provides **message confidentiality, authentication, and integrity**, not key transparency, automatic identity discovery, or a secure messaging transport.

## Usage — two independently controlled endpoints

Requires Node.js supporting crypto X25519, Ed25519, HKDF and AES-256-GCM. The example uses interactive terminal prompts so the passphrase does not appear in shell history; the passphrase is passed through a private file descriptor, not a command-line argument. Never pipe secrets through a model prompt or a logged command. Paths below are examples.

At sender endpoint (Alice):

```bash
read -r -s -p "Alice key passphrase (12+ chars): " AGY_PASS; printf '\n'
printf '%s' "$AGY_PASS" | bin/agyos secure keygen --passphrase-fd 0
unset AGY_PASS
bin/agyos secure public --out alice.pub.json
```

At recipient endpoint (Bob), independently generate a key pair and export `bob.pub.json` using the same two commands. Exchange **public identity files only** and verify displayed fingerprints through a trusted channel. Do not trust a public identity delivered together with an unverified encrypted message.

Alice encrypts a local private file *after verifying Bob's fingerprint*:

```bash
read -r -s -p "Alice key passphrase: " AGY_PASS; printf '\n'
printf '%s' "$AGY_PASS" | bin/agyos secure encrypt --recipient bob.pub.json --in notes.txt --out notes.agyos.enc.json --passphrase-fd 0
unset AGY_PASS
```

Alice sends only `notes.agyos.enc.json` to Bob, using a suitable file transfer. Bob decrypts after verifying Alice's fingerprint:

```bash
read -r -s -p "Bob key passphrase: " AGY_PASS; printf '\n'
printf '%s' "$AGY_PASS" | bin/agyos secure decrypt --sender alice.pub.json --in notes.agyos.enc.json --out notes.recovered.txt --passphrase-fd 0
unset AGY_PASS
```

To use a nondefault private identity, pass `--identity /private/location/identity.json` to every command. Default private identity: `~/.config/agyos/identity.json`, or `$XDG_CONFIG_HOME/agyos/identity.json`. Never generate it inside the AGYOS repository. Explicit output paths are create-only and refuse overwrites.

**Shell note:** a shell variable containing the passphrase lives briefly in that shell's memory; do not use the commands under `set -x` or in audited terminal sessions. For higher assurance use a local secret agent that supplies a private file descriptor. Back up the encrypted private identity and remember the passphrase; loss means the associated ciphertext is unrecoverable.

## Important limitations and unresolved security work

1. **Existing state and memory remain plaintext.** `.agents/state/memory.json`, `state.json`, context graphs, checkpoint files, logs, previous Git commits and numerous runtime data flows are not encrypted or migrated. Do not put secrets into the tracked state directory. This new module neither rewrites nor encrypts them.
2. **AI provider can read prompts** submitted in ordinary AGYOS execution. The provider/model is an endpoint for those prompts. Client encryption without model-accessible keys would prevent model inference.
3. **No post-compromise forward secrecy.** If a recipient long-term agreement private key is later stolen, old captured envelopes can be decrypted. Per-message ephemeral sender keys alone do not provide Double Ratchet or Signal-style forward secrecy. Replays are not rejected by this stateless file exchange.
4. **Sender fingerprint verification is manual**; there is no PKI, automatic trust-on-first-use, signed identity directory, revocation, multi-device group management, or key rotation protocol.
5. **Host compromise defeats endpoint confidentiality.** While endpoints process plaintext, compromised local machines, memory dumps, shell tracing, logs, or untrusted agent tools can expose it. Node.js memory cannot be guaranteed to be securely erased. Header metadata (public identities and fingerprints) is not confidential.
6. **No independent cryptographic audit.** A passing regression suite does not prove resistance to all adversaries. Do not market as audited or ready for high-value secrets before an external design and implementation review.
7. **No transport integration.** The new CLI is an opt-in file exchange tool. MCP, Agent Reach, gstack, cloud adapters, customer and agent-to-model messages do not automatically use it. No secret should be stored in public Git history.
8. **No authenticated streaming or compression**; files larger than 8 MiB are refused. Outbound encryption uses create-only files, and no automatic key escrow is provided.

## Verification

```bash
node --test scripts/tests/test_secure_envelope.cjs
node --check scripts/agyos-runtime/lib/e2ee.cjs
node --check scripts/agyos-runtime/secure-envelope.cjs
bin/agyos secure help
```

Tests cover two-endpoint round trips, different recipients, mismatched senders, tampered header/ciphertext/tag/signature, wrong passphrases, fresh per-message keys/nonces, file permissions, symlink rejection, output overwrite denial and CLI plaintext boundaries. Existing Python routing tests and CI must remain passing.

## Next architecture stage for system-wide protection

Map and classify every AGYOS data flow (local memories, state, MCP, multi-agent messages, inference provider, network retrieval, audit trails and backups). For **at-rest** privacy, introduce an authenticated encrypted vault with migration/rollback and key rotation, without altering immutable governance checks. For genuine **agent-to-agent E2EE**, define participating endpoints, identity enrollment, revocation, replay protection, session ratcheting and transport authentication, while keeping decryption keys outside the relay. For hosted AI, either explicitly trust the provider as an endpoint or use a verified local/attested confidential-computing inference boundary. Each step needs independent tests and a threat model; no blanket E2EE claim is defensible today.
