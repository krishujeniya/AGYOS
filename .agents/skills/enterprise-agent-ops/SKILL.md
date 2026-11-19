---
name: enterprise-agent-ops
description: Operational controls for long-lived or cloud-hosted agent systems — runtime lifecycle (start, pause, stop, restart), observability (logs, metrics, traces), least-privilege safety scopes and kill switches, and rollout/rollback change management with audit logs and success/cost metrics. Use when running production agent fleets on PM2, systemd, or containers that need monitoring, incident response, or deployment gates.
metadata:
  origin: ECC
prompt-source: prompt.toon
---
skill: "enterprise-agent-ops"
sections[7]:
  - "\n"
  - "# Enterprise Agent Ops\n\nUse this skill for cloud-hosted or continuously running agent systems that need operational controls beyond single CLI sessions.\n\n"
  - "## Operational Domains\n\n1. runtime lifecycle (start, pause, stop, restart)\n2. observability (logs, metrics, traces)\n3. safety controls (scopes, permissions, kill switches)\n4. change management (rollout, rollback, audit)\n\n"
  - "## Baseline Controls\n\n- immutable deployment artifacts\n- least-privilege credentials\n- environment-level secret injection\n- hard timeout and retry budgets\n- audit log for high-risk actions\n\n"
  - "## Metrics to Track\n\n- success rate\n- mean retries per task\n- time to recovery\n- cost per successful task\n- failure class distribution\n\n"
  - "## Incident Pattern\n\nWhen failure spikes:\n1. freeze new rollout\n2. capture representative traces\n3. isolate failing route\n4. patch with smallest safe change\n5. run regression + security checks\n6. resume gradually\n\n"
  - "## Deployment Integrations\n\nThis skill pairs with:\n- PM2 workflows\n- systemd services\n- container orchestrators\n- CI/CD gates\n"
