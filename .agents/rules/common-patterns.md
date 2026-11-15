---
trigger: always_on
---
# Common Patterns

## Skeleton Projects

When implementing new functionality:
1. Search for battle-tested skeleton projects
2. Use parallel agents to evaluate options:
   - Security assessment
   - Extensibility analysis
   - Relevance scoring
   - Implementation planning
3. Clone best match as foundation
4. Iterate within proven structure

## Design Patterns

### Repository Pattern

Encapsulate data access behind a consistent interface:
- Define standard operations: findAll, findById, create, update, delete
- Concrete implementations handle storage details (database, API, file, etc.)
- Business logic depends on the abstract interface, not the storage mechanism
- Enables easy swapping of data sources and simplifies testing with mocks

### API Response Format

Use a consistent envelope for all API responses:
- Include a success/status indicator
- Include the data payload (nullable on error)
- Include an error message field (nullable on success)
- Include metadata for paginated responses (total, page, limit)

### OpenDots Coworker Pattern (Persistent Dots & Living Workspaces)

Structure autonomous multi-agent systems following OpenDots principles without external code:
- **Persistent Dots**: Treat agents as persistent coworkers with defined roles, bounded scopes, and durable memory across turns.
- **Spaces & Pages**: Record deliverables in living markdown documents (pages within domain spaces) rather than ephemeral chat streams.
- **Sandboxed Execution**: Keep agent execution contained within designated paths and headless browser environments.
- **Human-in-the-Loop Review**: Enforce explicit review checkpoints before executing destructive actions, database mutations, or external tool commits.
- **Least-Privilege Tool Allowlists**: Scope tool and MCP permissions strictly to each worker's defined mandate.
