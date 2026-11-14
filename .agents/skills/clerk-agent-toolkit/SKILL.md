---
name: clerk-agent-toolkit
description: Integrate Clerk user management, organizations, sessions, and invitations directly into AI agent workflows using @clerk/agent-toolkit. Covers the local MCP server, Vercel AI SDK integration, LangChain integration, session context injection, and scoped tool helpers for multi-tenant agentic apps.
risk: medium
source: official (clerk.com/changelog/2025-03-7-clerk-agent-toolkit)
date_added: 2026-11-13
---
# Clerk Agent Toolkit

Bring Clerk's authentication and user management primitives into AI agent workflows via `@clerk/agent-toolkit`. Ships with a local MCP server, first-class Vercel AI SDK and LangChain helpers, session context injection, and scoped tool access for multi-tenant safety.

> [!IMPORTANT]
> This skill covers the **agentic** surface of Clerk (`@clerk/agent-toolkit`). For general Clerk auth patterns (middleware, webhooks, `<ClerkProvider>`) use the `clerk-auth` skill instead.

## Package

```bash
npm install @clerk/agent-toolkit
```

**Secret key:** Store as `CLERK_SECRET_KEY` in your environment (`.env.local` / hosting secrets). Never commit to source.

## MCP Server (Local)

The toolkit ships a built-in local MCP server for use with Claude Desktop, Cursor, and similar MCP clients:

```bash
npx -y @clerk/agent-toolkit -p local-mcp --secret-key sk_live_...
```

The AGYOS `mcp_config.json` registers this as `clerk-agent-toolkit` using `${CLERK_SECRET_KEY}` from the environment. Set the variable before starting Antigravity:

```bash
export CLERK_SECRET_KEY="sk_live_..."
```

## Tool Domains

| Domain | Tools Available |
|--------|----------------|
| **Users** | `users_list`, `users_get`, `users_create`, `users_update`, `users_delete` |
| **Organizations** | `organizations_list`, `organizations_get`, `organizations_create` |
| **Memberships** | `organization_memberships_list`, `organization_memberships_update`, `organization_memberships_delete` |
| **Invitations** | `invitations_create`, `invitations_list`, `invitations_revoke` |
| **Sessions** | `sessions_list`, `sessions_revoke` |

## Framework Integration

### Vercel AI SDK

```typescript
import { createClerkToolkit } from '@clerk/agent-toolkit/ai-sdk'
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'
import { auth } from '@clerk/nextjs/server'

export async function POST(req: Request) {
  const { messages } = await req.json()
  const { userId } = await auth()

  // Scoped to the authenticated user — cannot access other users' data
  const toolkit = await createClerkToolkit({ userId })

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    system: 'You are a helpful assistant with access to the user account.',
    tools: {
      ...toolkit.users(),
      ...toolkit.organizations(),
    },
  })

  return result.toDataStreamResponse()
}
```

### LangChain

```typescript
import { createClerkToolkit } from '@clerk/agent-toolkit/langchain'

const toolkit = await createClerkToolkit()
const tools = [
  ...toolkit.users(),
  ...toolkit.organizations(),
  ...toolkit.invitations(),
]
// Pass tools to your LangChain agent executor
```

### Session Context Injection

Inject the authenticated user's session claims into the model system prompt so the agent always knows *who* it's acting on behalf of:

```typescript
const toolkit = await createClerkToolkit()
const sessionContext = toolkit.injectSessionClaims({
  userId: 'user_2abc',
  sessionId: 'sess_xyz',
  orgId: 'org_abc',
})
// sessionContext is a string — prepend to your system prompt
```

## Scoping Rules

Always scope tools to the minimum necessary surface:

| Situation | Scope to pass |
|-----------|--------------|
| User managing their own account | `toolkit.users()` with `userId` restriction |
| Org admin managing their org | `toolkit.organizations()` + `toolkit.invitations()` |
| Super-admin agentic workflow | All domains (require explicit confirmation before destructive ops) |

## Workflow

1. **Confirm scope** — verify the task is Clerk user/org/session management inside an AI agent workflow.
2. **Check secret key** — confirm `CLERK_SECRET_KEY` is set in the environment and matches the target Clerk instance (`sk_test_` for development, `sk_live_` for production).
3. **Choose integration surface**:
   - Standalone MCP → use the `clerk-agent-toolkit` MCP server already registered.
   - Vercel AI SDK route → use `@clerk/agent-toolkit/ai-sdk`.
   - LangChain agent → use `@clerk/agent-toolkit/langchain`.
4. **Scope tools** — only expose the minimum domain set needed. Wrap with `userId` or `orgId` context when acting on behalf of a specific user.
5. **Inject session context** — call `toolkit.injectSessionClaims()` and prepend to the system prompt so the model has user context.
6. **Execute the task** — call tools via the agent. For destructive operations (`users_delete`, `sessions_revoke`, `invitations_revoke`), require explicit user confirmation before invoking.
7. **Verify** — confirm the operation succeeded by calling the corresponding `_get` or `_list` tool and checking the returned state.

## Security Constraints

- Never store `CLERK_SECRET_KEY` in a file tracked by git or in any artifact.
- Always prefer `sk_test_` keys during development; use `sk_live_` only in production environments.
- Scope tool access to the authenticated user's context — do not expose all-user admin tools to untrusted agents.
- Confirm before calling `users_delete`, `sessions_revoke`, or `invitations_revoke` — these are irreversible or immediately disruptive.
- If a session token lacks required scopes (`user:org:read` etc.), surface the error to the user and prompt re-authentication; do not silently retry.

## Related Skills

- `clerk-auth` — general Clerk auth (middleware, webhooks, `<ClerkProvider>`, `useAuth`)
- `nextjs-supabase-auth` — Supabase-based auth alternative
- `api-patterns` — API design patterns when wrapping Clerk in a backend route
