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


## Encrypted local memory vault (added security layer)

The standard AGYOS MCP \`agyos_memory\` tool now writes only to a separately configured encrypted vault. Its old plaintext write path to \`.agents/state/memory.json\` has been disabled. Data written through the MCP memory API is encrypted at rest using AES-256-GCM and a passphrase-derived key (scrypt N=32768, r=8, p=1, random salt). Each update rotates the salt and nonce, holds a cooperative lock, and atomically replaces the encrypted file. No encryption key is stored in Git or generated by the model.

**Initialize an encrypted private vault on the Ubuntu endpoint** (run from your local AGYOS checkout, never inside a model-hosted shell with recorded secrets):

\`\`\`bash
bin/agyos secure vault-status
read -r -s -p "Enter a strong private memory vault passphrase: " AGY_SECRET; printf '\n'
printf '%s' "$AGY_SECRET" | bin/agyos secure vault-init --passphrase-fd 0
unset AGY_SECRET
bin/agyos secure vault-status
\`\`\`

The default vault location is \`~/.local/state/agyos/private-memory.vault.json\` (or \`$XDG_STATE_HOME/agyos/private-memory.vault.json\`). Keep the vault outside the repository and back up the encrypted file and passphrase separately. Vault files must be owned by the current user with mode \`0600\` in a mode-\`0700\` directory.

**Unlock at MCP server startup** by supplying the passphrase over a private inherited descriptor \`3\`, and setting only \`AGYOS_VAULT_PASSPHRASE_FD=3\` in the MCP server environment. A securely configured launch supervisor, not the model prompt, must provide the descriptor. The passphrase must not appear in a command argument, environment variable, Git commit, config file, shell trace, or telemetry. Example pseudocode for a supervisor:

\`\`\`text
open private pipe FD 3 containing vault passphrase (not a regular file on disk)
spawn: node mcp/state-server.cjs
env: AGYOS_VAULT_PASSPHRASE_FD=3
inherit: only required private FD 3 plus MCP stdin/stdout
\`\`\`

A configured vault with no private descriptor **fails closed** on MCP memory reads or writes. Without an initialized vault, existing public baseline memory reads remain compatible, but **all writes are rejected**. On successful unlock, private fields override the public baseline; read operations still return plaintext to the authorized local MCP client because it must consume the data. **Any model or plugin allowed to call this tool can see its returned plaintext**, so restrict tool grants accordingly.

This vault is **at-rest encryption, not true multi-party E2EE**. It does not transparently encrypt \`.agents/state/state.json\`, checkpoint Markdown, telemetry JSONL, documentation, skill runbooks, Git history, third-party ECC memory stores, or model-provider traffic. Those paths need separate audited migrations and access controls. Current AGYOS public state data may already exist in Git history; no new encryption layer can revoke previously cloned content. Rotate any compromised credentials.

### Evidence and verification

\`\`\`bash
node --test scripts/tests/test_private_vault.cjs scripts/tests/test_secure_envelope.cjs
python3 -m unittest discover -s scripts/tests -v
\`\`\`

The vault test suite checks authenticated writes, ciphertext secrecy, tamper detection, restrictive file permissions, safe file paths, mismatched passphrases, no plaintext fallback, MCP reads after authentication, and protected CLI initialization. CI evidence should always be checked on the actual main commit.

### Coverage map: do not represent AGYOS as fully end-to-end encrypted

| Data path | Current protection | Remaining requirement |
| --- | --- | --- |
| Opt-in endpoint-to-endpoint file exchange | X25519 + AES-256-GCM + Ed25519 | Independent identity verification, replay protection, long-term key rotation |
| MCP memory writes after vault setup | Encrypted at rest; key held by local MCP endpoint | Host tool authorization, key rotation, backup/restore, sensitive metadata classification |
| Legacy committed memory and state | Plaintext baseline | Inventory, history exposure assessment, explicit migration of each consumer |
| AGYOS workflow state, checkpoints and telemetry | Existing plaintext flows | Encrypted storage integration with transactional state machinery |
| ECC memory vault | Existing independent plaintext implementation | Separate compatibility-preserving encryption migration |
| Agent-to-agent remote messages | No universal E2EE transport | Key identities, authenticated endpoints, replay controls, session key updates |
| AGY CLI and MCP stdio traffic | Local IPC; not sealed by new envelope | Tool access controls, privileged process isolation, encrypted remote transport |
| Remote AI providers | Provider receives readable prompts | Locally hosted trusted inference or independently attested confidential execution |
| Source code and public skills on GitHub | Intentionally public | Never treat public source as a secret; protect credentials and private runtime data |

**Security outcome:** partial encrypted infrastructure, not entire-OS E2EE. This distinction is required for accurate security claims.
