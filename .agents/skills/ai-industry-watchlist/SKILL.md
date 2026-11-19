---
name: ai-industry-watchlist
description: Maintain a useful, source-checked watchlist of AI companies, labs, researchers, and leaders from the supplied AI Accounts to Follow reference. Use when organizing AI news sources, building a daily reading list, checking official social profiles, or refreshing the supplied 79-account directory.
metadata:
  origin: user-supplied-reference
prompt-source: prompt.toon
---
skill: "ai-industry-watchlist"
sections[4]:
  - "\n"
  - "# AI industry watchlist\n\nUse the supplied directory as a starting list, not as proof that an account is current or official.\n\n"
  - "## Workflow\n\n1. Read `docs/references/industry/AI_Accounts_To_Follow.txt` and keep the original PDF at `docs/references/industry/AI_Accounts_To_Follow.pdf` as the source record.\n2. Ask which platforms and topics matter if the user wants a personalized list. Keep the initial list small enough to follow consistently.\n3. Verify each selected organization or person's identity from an official site or another first-party source. Link that evidence and record the checked date; do not guess handles from display names.\n4. Separate first-party announcements from community discussion. Label unaffiliated Reddit communities as community sources.\n5. Present a compact table with organization/person, topic, platform, verified profile link, source, and checked date. Mark unavailable profiles as unknown rather than inventing one.\n6. Refresh unstable account links and organizational roles before recommending them as current.\n\n"
  - "## Boundaries\n\n- Do not sign into accounts, follow profiles, enable notifications, or change a feed without the user's explicit request.\n- Do not claim that a small watchlist is comprehensive or that a source is unbiased.\n- Keep the PDF's statements and handles attributed to that supplied edition; newer claims need current first-party evidence.\n"
