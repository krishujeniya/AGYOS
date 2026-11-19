---
name: tcm-constitution-analyzer
description: 分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。
allowed-tools: Read, Grep, Glob, Write
risk: unknown
source: community
prompt-source: prompt.toon
---
skill: "tcm-constitution-analyzer"
sections[2]:
  - "# 中医体质辨识分析器技能\n\n分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
