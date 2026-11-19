---
name: azure-keyvault-secrets-ts
description: "Manage secrets using Azure Key Vault Secrets SDK for JavaScript (@azure/keyvault-secrets). Use when storing and retrieving application secrets or configuration values."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "azure-keyvault-secrets-ts"
sections[17]:
  - "\n"
  - "# Azure Key Vault Secrets SDK for TypeScript\n\nManage secrets with Azure Key Vault.\n\n"
  - "## Installation\n\n```bash\n# Secrets SDK\nnpm install @azure/keyvault-secrets @azure/identity\n```\n\n"
  - "## Environment Variables\n\n```bash\nKEY_VAULT_URL=https://<vault-name>.vault.azure.net\n# Or\nAZURE_KEYVAULT_NAME=<vault-name>\n```\n\n"
  - "## Authentication\n\n```typescript\nimport { DefaultAzureCredential } from \"@azure/identity\";\nimport { SecretClient } from \"@azure/keyvault-secrets\";\n\nconst credential = new DefaultAzureCredential();\nconst vaultUrl = `https://${process.env.AZURE_KEYVAULT_NAME}.vault.azure.net`;\n\nconst secretClient = new SecretClient(vaultUrl, credential);\n```\n\n"
  - "## Secrets Operations\n\n"
  - "### Create/Set Secret\n\n```typescript\nconst secret = await secretClient.setSecret(\"MySecret\", \"secret-value\");\n\n// With attributes\nconst secretWithAttrs = await secretClient.setSecret(\"MySecret\", \"value\", {\n  enabled: true,\n  expiresOn: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),\n  contentType: \"application/json\",\n  tags: { environment: \"production\" }\n});\n```\n\n"
  - "### Get Secret\n\n```typescript\n// Get latest version\nconst secret = await secretClient.getSecret(\"MySecret\");\nconsole.log(secret.value);\n\n// Get specific version\nconst specificSecret = await secretClient.getSecret(\"MySecret\", {\n  version: secret.properties.version\n});\n```\n\n"
  - "### List Secrets\n\n```typescript\nfor await (const secretProperties of secretClient.listPropertiesOfSecrets()) {\n  console.log(secretProperties.name);\n}\n\n// List versions\nfor await (const version of secretClient.listPropertiesOfSecretVersions(\"MySecret\")) {\n  console.log(version.version);\n}\n```\n\n"
  - "### Delete Secret\n\n```typescript\n// Soft delete\nconst deletePoller = await secretClient.beginDeleteSecret(\"MySecret\");\nawait deletePoller.pollUntilDone();\n\n// Purge (permanent)\nawait secretClient.purgeDeletedSecret(\"MySecret\");\n\n// Recover\nconst recoverPoller = await secretClient.beginRecoverDeletedSecret(\"MySecret\");\nawait recoverPoller.pollUntilDone();\n```\n\n"
  - "## Key management\n\nFor cryptographic keys and key operations, use the [Azure Key Vault Keys skill](../azure-keyvault-keys-ts/SKILL.md).\n\n"
  - "## Backup and Restore\n\n```typescript\nconst secretBackup = await secretClient.backupSecret(\"MySecret\");\nconst restoredSecret = await secretClient.restoreSecretBackup(secretBackup!);\n```\n\n"
  - "## Error Handling\n\n```typescript\ntry {\n  const secret = await secretClient.getSecret(\"NonExistent\");\n} catch (error: any) {\n  if (error.code === \"SecretNotFound\") {\n    console.log(\"Secret does not exist\");\n  } else {\n    throw error;\n  }\n}\n```\n\n"
  - "## Official SDK reference\n\nSee the [Microsoft Key Vault Secrets JavaScript SDK documentation](https://learn.microsoft.com/en-us/javascript/api/overview/azure/keyvault-secrets-readme?view=azure-node-latest) for the installed package version.\n\n"
  - "## Best Practices\n\n1. **Use DefaultAzureCredential** - Works across dev and production\n2. **Enable soft-delete** - Required for production vaults\n3. **Set expiration dates** - On both keys and secrets\n4. **Use key rotation policies** - Automate key rotation\n5. **Limit key operations** - Only grant needed operations (encrypt, sign, etc.)\n6. **Browser not supported** - These SDKs are Node.js only\n\n"
  - "## When to Use\nThis skill is applicable to execute the workflow or actions described in the overview.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
