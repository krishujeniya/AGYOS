---
name: wechat-summarizer
description: Summarizes WeChat group chat highlights into a structured digest using the local wx-cli binary (https://github.com/jackwener/wx-cli). Generates a normal digest by default; a roast (毒舌) version is opt-in. Maintains per-group history (history.json + history-digests.jsonl) and per-user profiles across runs, with privacy guardrails baked in. Use when the user asks to "总结群聊", "群聊精华", "群聊摘要", "summarize group chat", "group chat digest", mentions a WeChat group name with a time range, says "帮我看看 XX 群最近聊了什么", "XX 群有什么值得看的", or asks to "回溯画像" / "初始化画像" / "backfill profiles". Adds the roast version when the user says "毒舌版", "roast 版", "再来个毒舌的", or similar.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-wechat-summary
    requires:
      anyBins:
        - wx
---
# WeChat Group Summary

Summarizes WeChat group chat highlights into a structured digest using the local wx-cli binary (https://github.com/jackwener/wx-cli). Generates a normal digest by default; a roast (毒舌) version is opt-in. Maintains per-group history (history.json + history-digests.jsonl) and per-user profiles across runs, with privacy guardrails baked in. Use when the user asks to "总结群聊", "群聊精华", "群聊摘要", "summarize group chat", "group chat digest", mentions a WeChat group name with a time range, says "帮我看看 XX 群最近聊了什么", "XX 群有什么值得看的", or asks to "回溯画像" / "初始化画像" / "backfill profiles". Adds the roast version when the user says "毒舌版", "roast 版", "再来个毒舌的", or similar.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
