# AGYOS References & Knowledge Repository

This directory contains external reference specifications, production prompt engineering playbooks, and architecture guides utilized across the AGYOS cognitive operating system.

## Directory Contents

| File | Type | Description |
| :--- | :--- | :--- |
| [`prompts.md`](prompts.md) | Markdown | Production prompt engineering library with CRISPE + Invariant framework prompts. |
| [`github-profile-playbook.pdf`](github-profile-playbook.pdf) | PDF Guide | Portfolio and open-source profile architecture guide for technical engineering. |
| [`Motion_Graphics_Google_Flow_Master_Guide.pdf`](Motion_Graphics_Google_Flow_Master_Guide.pdf) | PDF Guide | Google Flow and cinematic animation timing guide for ScrollHeart components. |
| [`video/`](video/README.md) | Source toolkits and prompt references | Local talking-head editor, faceless-shorts renderer, and provenance notes for supplied prompt material. |
| [`industry/`](industry/README.md) | User-supplied PDFs and searchable text | AI accounts watchlist, DevOps career roadmap, first-customer playbook, and Harvey/Sellbird setup reference with freshness notes. |
| [`upstream-skills/`](upstream-skills/README.md) | Pinned skill source inventory | License-aware imports from Jakeschincariol and the individually MIT-licensed Benji Taylor Stageshow skill. |

## Usage Standard

All skills and subagents access reference materials through Just-In-Time (JIT) retrieval via `read_file` rather than loading heavy manuals into always-on prompt contexts.
