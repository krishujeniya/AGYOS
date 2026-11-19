---
name: architecture-c4-model
description: "Generate comprehensive C4 architecture documentation for a system. Focuses on Context, Container, and Component levels."
prompt-source: prompt.toon
---
skill: "architecture-c4-model"
sections[8]:
  - "\n"
  - "# C4 Architecture Documentation\n\nUse this skill to design or document the architecture of a software system following the C4 Model.\n\n"
  - "## Overview\n\nThe C4 model consists of 4 levels of diagrams:\n1. **Context Level**: High-level system context with personas and user journeys (focuses on people and external software systems, not technologies).\n2. **Container Level**: Maps applications and data stores. Shows high-level technology choices, deployment containers with API documentation.\n3. **Component Level**: Defines the components within a container.\n4. **Code (Optional)**: Deep code-level implementation details.\n\n"
  - "## How to Apply During Project Planning\n\nWhen asked to design the system architecture, always walk through the levels:\n\n"
  - "### 1. Context Diagram & Documentation\n- Define the user personas (Who is using this system?)\n- Define external systems (What APIs or platforms does it interact with?)\n- Create a `C4Context` Mermaid diagram showing the system in the center.\n\n"
  - "### 2. Container Diagram & Documentation\n- Break the system down into Deployable Units (e.g., PostgreSQL Database, Next.js Frontend, Python FastAPI Backend).\n- Define the exact technologies chosen for each container.\n- Create a `C4Container` Mermaid diagram detailing how these containers interact.\n\n"
  - "### 3. Component Definition\n- Inside the backend, what are the core modules? (e.g., Auth Module, Billing Module, Search Service).\n- Detail boundaries, API contracts, and bounded contexts (DDD).\n\n"
  - "## Deliverables to Generate\n\nWhen using this skill to plan architecture, output:\n1. **System Context Overview** (`c4-context.md`)\n2. **Container Deployments** (`c4-container.md` or a detailed README section)\n3. **Mermaid Architecture Flow** using `C4Context` or `C4Container` notation.\n"
