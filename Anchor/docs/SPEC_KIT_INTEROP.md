# Spec Kit Interop Guide

## "Spec Kit plans it; ANCHOR proves it."

GitHub's [Spec Kit](https://github.com/github/spec-kit) is a fantastic tool for driving agentic development via a structured `/specify`, `/plan`, and `/tasks` command workflow. It excels at greenfield planning and breaking down large problems into conversational sub-tasks.

However, Spec Kit relies on **convention** rather than **enforcement**. Agents can still hallucinate tests passing, skip verification, or push uncompilable code.

ANCHOR perfectly complements Spec Kit by wrapping its conversational planning with **hard verification gates and durable state.** 

## How to use them together

1. **Initialize both in your repo:**
   ```bash
   uvx specify init
   npx anchor-agent init
   ```

2. **The Combined Workflow:**
   
   | Step | Tool | Action |
   |---|---|---|
   | **1. Ideation** | Spec Kit | Use `/specify` and `/plan` to gather requirements and generate a `DESIGN.md` |
   | **2. Scoping** | ANCHOR | ANCHOR's `UNDERSTAND` and `ANALYZE` gates automatically validate the Spec Kit `DESIGN.md` for risks and invariants. |
   | **3. Implementation** | Spec Kit | Run `/tasks` to let the agent implement the spec. |
   | **4. Verification** | ANCHOR | The git pre-commit hook automatically fires `gate-check.sh`, intercepting the agent's commit until tests and linters pass deterministically. |

## Why this works
By layering ANCHOR under Spec Kit, you get the best of both worlds: Spec Kit's brilliant UX and workflow commands, backed by ANCHOR's zero-trust audit trail and rollback guarantees.
