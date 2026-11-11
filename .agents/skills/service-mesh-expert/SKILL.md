---
name: service-mesh-expert
description: "Design or troubleshoot Kubernetes service-mesh traffic, mTLS, policy, and service discovery. Use for zero-trust service communication or mesh connectivity issues."
risk: safe
source: community
date_added: "2026-02-27"
---

# Service Mesh Expert

Design or troubleshoot Kubernetes service-mesh traffic, mTLS, policy, and service discovery. Use for zero-trust service communication or mesh connectivity issues.

## Do not use this skill when

- The task is unrelated to service mesh expert
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Capabilities

- Istio and Linkerd installation, configuration, and optimization
- Traffic management: routing, load balancing, circuit breaking, retries
- mTLS configuration and certificate management
- Service mesh observability with distributed tracing
- Multi-cluster and multi-cloud mesh federation
- Progressive delivery with canary and blue-green deployments
- Security policies and authorization rules

## Use this skill when

- Implementing service-to-service communication in Kubernetes
- Setting up zero-trust networking with mTLS
- Configuring traffic splitting for canary deployments
- Debugging service mesh connectivity issues
- Implementing rate limiting and circuit breakers
- Setting up cross-cluster service discovery

## Workflow

1. Assess current infrastructure and requirements
2. Design mesh topology and traffic policies
3. Implement security policies (mTLS, AuthorizationPolicy)
4. Configure observability (metrics, traces, logs)
5. Set up traffic management rules
6. Test failover and resilience patterns
7. Document operational runbooks

## Best Practices

- Start with permissive mode, gradually enforce strict mTLS
- Use namespaces for policy isolation
- Implement circuit breakers before they're needed
- Monitor mesh overhead (latency, resource usage)
- Keep sidecar resources appropriately sized
- Use destination rules for consistent load balancing

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
