---
name: quarkus-security
description: "Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators, parameterized Panache queries, BCrypt password hashing, CORS and security headers, rate limiting, audit logging, Vault or environment-variable secrets, and dependency CVE scanning. Use when adding authentication or authorization, validating input, managing secrets, or hardening a Quarkus application."
metadata:
  origin: ECC
---
# Quarkus Security Review

Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation and custom validators, parameterized Panache queries, BCrypt password hashing, CORS and security headers, rate limiting, audit logging, Vault or environment-variable secrets, and dependency CVE scanning. Use when adding authentication or authorization, validating input, managing secrets, or hardening a Quarkus application.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
