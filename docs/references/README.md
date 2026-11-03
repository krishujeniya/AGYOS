# AGYOS References & Knowledge Repository

This directory contains external reference specifications, production prompt engineering playbooks, and architecture guides utilized across the AGYOS cognitive operating system.

## Directory Contents

| File | Type | Description |
| :--- | :--- | :--- |
| [`prompts.md`](prompts.md) | Markdown | Production prompt engineering library with CRISPE + Invariant framework prompts. |
| [`github-profile-playbook.pdf`](github-profile-playbook.pdf) | PDF Guide | Portfolio and open-source profile architecture guide for technical engineering. |
| [`Motion_Graphics_Google_Flow_Master_Guide.pdf`](Motion_Graphics_Google_Flow_Master_Guide.pdf) | PDF Guide | Google Flow and cinematic animation timing guide for ScrollHeart components. |

## Usage Standard

All skills and subagents access reference materials through Just-In-Time (JIT) retrieval via `read_file` rather than loading heavy manuals into always-on prompt contexts.
