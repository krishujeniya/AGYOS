---
name: service-mesh-expert
description: "Design or troubleshoot Kubernetes service-mesh traffic, mTLS, policy, and service discovery. Use for zero-trust service communication or mesh connectivity issues."
risk: safe
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "service-mesh-expert"
sections[9]:
  - "\n"
  - "# Service Mesh Expert\n\nDesign or troubleshoot Kubernetes service-mesh traffic, mTLS, policy, and service discovery. Use for zero-trust service communication or mesh connectivity issues.\n\n"
  - "## Do not use this skill when\n\n- The task is unrelated to service mesh expert\n- You need a different domain or tool outside this scope\n\n"
  - "## Instructions\n\n- Clarify goals, constraints, and required inputs.\n- Apply relevant best practices and validate outcomes.\n- Provide actionable steps and verification.\n- If detailed examples are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Capabilities\n\n- Istio and Linkerd installation, configuration, and optimization\n- Traffic management: routing, load balancing, circuit breaking, retries\n- mTLS configuration and certificate management\n- Service mesh observability with distributed tracing\n- Multi-cluster and multi-cloud mesh federation\n- Progressive delivery with canary and blue-green deployments\n- Security policies and authorization rules\n\n"
  - "## Use this skill when\n\n- Implementing service-to-service communication in Kubernetes\n- Setting up zero-trust networking with mTLS\n- Configuring traffic splitting for canary deployments\n- Debugging service mesh connectivity issues\n- Implementing rate limiting and circuit breakers\n- Setting up cross-cluster service discovery\n\n"
  - "## Workflow\n\n1. Assess current infrastructure and requirements\n2. Design mesh topology and traffic policies\n3. Implement security policies (mTLS, AuthorizationPolicy)\n4. Configure observability (metrics, traces, logs)\n5. Set up traffic management rules\n6. Test failover and resilience patterns\n7. Document operational runbooks\n\n"
  - "## Best Practices\n\n- Start with permissive mode, gradually enforce strict mTLS\n- Use namespaces for policy isolation\n- Implement circuit breakers before they're needed\n- Monitor mesh overhead (latency, resource usage)\n- Keep sidecar resources appropriately sized\n- Use destination rules for consistent load balancing\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
