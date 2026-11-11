---
name: azure-keyvault-secrets-ts
description: "Manage secrets using Azure Key Vault Secrets SDK for JavaScript (@azure/keyvault-secrets). Use when storing and retrieving application secrets or configuration values."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Key Vault Secrets SDK for TypeScript

Manage secrets with Azure Key Vault.

## Installation

```bash
# Secrets SDK
npm install @azure/keyvault-secrets @azure/identity
```

## Environment Variables

```bash
KEY_VAULT_URL=https://<vault-name>.vault.azure.net
# Or
AZURE_KEYVAULT_NAME=<vault-name>
```

## Authentication

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { SecretClient } from "@azure/keyvault-secrets";

const credential = new DefaultAzureCredential();
const vaultUrl = `https://${process.env.AZURE_KEYVAULT_NAME}.vault.azure.net`;

const secretClient = new SecretClient(vaultUrl, credential);
```

## Secrets Operations

### Create/Set Secret

```typescript
const secret = await secretClient.setSecret("MySecret", "secret-value");

// With attributes
const secretWithAttrs = await secretClient.setSecret("MySecret", "value", {
  enabled: true,
  expiresOn: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
  contentType: "application/json",
  tags: { environment: "production" }
});
```

### Get Secret

```typescript
// Get latest version
const secret = await secretClient.getSecret("MySecret");
console.log(secret.value);

// Get specific version
const specificSecret = await secretClient.getSecret("MySecret", {
  version: secret.properties.version
});
```

### List Secrets

```typescript
for await (const secretProperties of secretClient.listPropertiesOfSecrets()) {
  console.log(secretProperties.name);
}

// List versions
for await (const version of secretClient.listPropertiesOfSecretVersions("MySecret")) {
  console.log(version.version);
}
```

### Delete Secret

```typescript
// Soft delete
const deletePoller = await secretClient.beginDeleteSecret("MySecret");
await deletePoller.pollUntilDone();

// Purge (permanent)
await secretClient.purgeDeletedSecret("MySecret");

// Recover
const recoverPoller = await secretClient.beginRecoverDeletedSecret("MySecret");
await recoverPoller.pollUntilDone();
```

## Key management

For cryptographic keys and key operations, use the [Azure Key Vault Keys skill](../azure-keyvault-keys-ts/SKILL.md).

## Backup and Restore

```typescript
const secretBackup = await secretClient.backupSecret("MySecret");
const restoredSecret = await secretClient.restoreSecretBackup(secretBackup!);
```

## Error Handling

```typescript
try {
  const secret = await secretClient.getSecret("NonExistent");
} catch (error: any) {
  if (error.code === "SecretNotFound") {
    console.log("Secret does not exist");
  } else {
    throw error;
  }
}
```

## Official SDK reference

See the [Microsoft Key Vault Secrets JavaScript SDK documentation](https://learn.microsoft.com/en-us/javascript/api/overview/azure/keyvault-secrets-readme?view=azure-node-latest) for the installed package version.

## Best Practices

1. **Use DefaultAzureCredential** - Works across dev and production
2. **Enable soft-delete** - Required for production vaults
3. **Set expiration dates** - On both keys and secrets
4. **Use key rotation policies** - Automate key rotation
5. **Limit key operations** - Only grant needed operations (encrypt, sign, etc.)
6. **Browser not supported** - These SDKs are Node.js only

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
