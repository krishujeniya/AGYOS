#!/usr/bin/env python3
"""
Compile comprehensive skills database and SEO assets for SKILL GitHub Pages documentation site.
Applies unslop rules to remove AI buzzwords, decorative symbols, and fluff.
"""

import os
import json
import re

REPO_ROOT = "/home/ai/Documents/projects/SKILL"
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

AI_WORDS_MAP = {
    r"\bleverage\b": "use",
    r"\bleveraging\b": "using",
    r"\butilize\b": "use",
    r"\butilizing\b": "using",
    r"\bdelve\b": "explore",
    r"\bdelving\b": "exploring",
    r"\bseamless\b": "direct",
    r"\bseamlessly\b": "directly",
    r"\brobust\b": "reliable",
    r"\brobustness\b": "reliability",
    r"\bcrucial\b": "essential",
    r"\bparamount\b": "primary",
    r"\btestament\b": "proof",
    r"\btapestry\b": "collection",
    r"\bfoster\b": "support",
    r"\bfostering\b": "supporting",
    r"\belevate\b": "improve",
    r"\belevating\b": "improving",
    r"\bgame-changer\b": "major advance",
    r"\bgame changer\b": "major advance",
    r"\bdive deep\b": "inspect thoroughly",
    r"\bdive into\b": "inspect",
    r"\bmultifaceted\b": "broad",
    r"\bplethora\b": "wide range",
    r"\bfurthermore\b": "also",
    r"\bmoreover\b": "also",
    r"\bholistic\b": "complete",
    r"\bsynergy\b": "coordination",
    r"\bunleash\b": "enable",
    r"\bnavigating\b": "handling",
    r"\bintricate\b": "complex",
    r"\bvibrant\b": "active",
    r"\bpivotal\b": "critical",
    r"\benduring\b": "lasting",
    r"\bgroundbreaking\b": "practical",
    r"\btransformative\b": "effective",
    r"\brevolutionary\b": "novel"
}

def unslop(text: str) -> str:
    if not text:
        return ""
    # Remove emoji and high unicode AI icons
    clean = re.sub(r"[\U00010000-\U0010ffff]", "", text)
    clean = re.sub(r"[\u2600-\u27bf]", "", clean)
    clean = re.sub(r"[\u2300-\u23ff]", "", clean)
    # Replace em dash and en dash with comma or period
    clean = clean.replace("—", ", ").replace("–", "-")
    # Clean AI words
    for pattern, replacement in AI_WORDS_MAP.items():
        clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
    # Normalize spaces
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def build_data():
    skills = []
    seen_ids = set()

    def add_skill(s):
        sid = s["id"]
        if sid in seen_ids:
            return
        seen_ids.add(sid)
        s["description"] = unslop(s.get("description", ""))
        skills.append(s)

    # 1. Anchor Skills
    anchor_items = [
        {
            "id": "anchor-orchestrator",
            "name": "Anchor Orchestrator",
            "module": "Anchor",
            "category": "Orchestration",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor orchestrator",
            "path": "Anchor/.agents/skills/anchor-orchestrator",
            "risk": "safe",
            "description": "Routes multi-step coding tasks through five explicit gates: understand, analyze, plan, implement, and verify. Blocks skipping validation."
        },
        {
            "id": "anchor-scout",
            "name": "Anchor Scout",
            "module": "Anchor",
            "category": "Reconnaissance",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor scout",
            "path": "Anchor/.agents/skills/anchor-scout",
            "risk": "safe",
            "description": "Performs read-only inspection of target files, package manifests, and project layouts before any code change."
        },
        {
            "id": "anchor-scope",
            "name": "Anchor Scope",
            "module": "Anchor",
            "category": "Safety",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor scope",
            "path": "Anchor/.agents/skills/anchor-scope",
            "risk": "safe",
            "description": "Restricts agent file writes to explicitly declared path boundaries. Denies out-of-scope edits automatically."
        },
        {
            "id": "anchor-verify",
            "name": "Anchor Verify",
            "module": "Anchor",
            "category": "Verification",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor verify",
            "path": "Anchor/.agents/skills/anchor-verify",
            "risk": "safe",
            "description": "Executes test suites, linters, and type checkers after mutations. Rejects completion claims without fresh validator output."
        },
        {
            "id": "anchor-draft-commit",
            "name": "Anchor Draft Commit",
            "module": "Anchor",
            "category": "Version Control",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor draft-commit",
            "path": "Anchor/.agents/skills/anchor-draft-commit",
            "risk": "safe",
            "description": "Saves reversible git checkpoints before high-risk changes. Enables immediate recovery if an approach fails."
        },
        {
            "id": "anchor-graph",
            "name": "Anchor Graph",
            "module": "Anchor",
            "category": "Architecture",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor graph",
            "path": "Anchor/.agents/skills/anchor-graph",
            "risk": "safe",
            "description": "Analyzes call hierarchies, cross-module dependencies, and imports across the project before refactoring."
        },
        {
            "id": "anchor-preflight",
            "name": "Anchor Preflight",
            "module": "Anchor",
            "category": "Environment",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "anchor preflight",
            "path": "Anchor/.agents/skills/anchor-preflight",
            "risk": "safe",
            "description": "Validates workspace preconditions including clean git status, compiler tools, test runners, and API keys."
        }
    ]
    for s in anchor_items:
        add_skill(s)

    # 2. Agent Council
    council_items = [
        {
            "id": "agent-council",
            "name": "Agent Council",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "agent-council \"<question>\"",
            "path": "agent-council/skills/claude-code/agent-council",
            "risk": "safe",
            "description": "Convenes multiple AI models in isolated CLI subprocesses to independently deliberate on architecture decisions and synthesize consensus."
        },
        {
            "id": "council-list",
            "name": "Council List",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "council-list",
            "path": "agent-council/skills/claude-code/council-list",
            "risk": "safe",
            "description": "Lists recorded council deliberation sessions for the current project with question summaries and timestamp logs."
        },
        {
            "id": "council-outcome",
            "name": "Council Outcome",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "council-outcome <session_id>",
            "path": "agent-council/skills/claude-code/council-outcome",
            "risk": "safe",
            "description": "Logs post-implementation outcomes for council decisions to build empirical model calibration metrics over time."
        },
        {
            "id": "council-replay",
            "name": "Council Replay",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "council-replay <session_id>",
            "path": "agent-council/skills/claude-code/council-replay",
            "risk": "safe",
            "description": "Replays complete debate transcripts in the terminal or browser, showing raw model votes and chairman reasoning."
        },
        {
            "id": "council-revisit",
            "name": "Council Revisit",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "council-revisit <session_id>",
            "path": "agent-council/skills/claude-code/council-revisit",
            "risk": "safe",
            "description": "Re-evaluates a prior architectural decision using updated codebase context, highlighting what assumptions changed."
        },
        {
            "id": "council-nudge",
            "name": "Council Nudge",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "council-nudge",
            "path": "agent-council/skills/claude-code/council-nudge",
            "risk": "safe",
            "description": "Notifies the developer when a high-impact architectural choice or complex bug could benefit from a multi-model panel."
        },
        {
            "id": "agent-council-nudge",
            "name": "Agent Council Ambient Nudge",
            "module": "Agent Council",
            "category": "Deliberation",
            "runtime": ["Bun", "AGY", "Codex", "Claude Code"],
            "command": "agent-council-nudge",
            "path": "agent-council/skills/claude-code/agent-council-nudge",
            "risk": "safe",
            "description": "Passive background monitor that detects cross-file refactors or conflicting design approaches and suggests a council check."
        }
    ]
    for s in council_items:
        add_skill(s)

    # 3. Agentic Freelance Skills
    freelance_items = [
        {
            "id": "freelancer-client-acquisition",
            "name": "Freelancer Client Acquisition",
            "module": "Freelance Suite",
            "category": "Business",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-client-acquisition",
            "path": "agentic-freelance-skills/skills/freelancer-client-acquisition",
            "risk": "safe",
            "description": "Designs and executes outbound client prospecting, cold outreach sequences, platform profile positioning, and inbound referral loops."
        },
        {
            "id": "freelancer-sales-closing",
            "name": "Freelancer Sales Closing",
            "module": "Freelance Suite",
            "category": "Business",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-sales-closing",
            "path": "agentic-freelance-skills/skills/freelancer-sales-closing",
            "risk": "safe",
            "description": "Structures discovery calls, proposals, scope documents, objection handling, pricing models, and contract signing."
        },
        {
            "id": "freelancer-project-delivery",
            "name": "Freelancer Project Delivery",
            "module": "Freelance Suite",
            "category": "Delivery",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-project-delivery",
            "path": "agentic-freelance-skills/skills/freelancer-project-delivery",
            "risk": "safe",
            "description": "Manages milestone roadmaps, client sprint updates, acceptance testing, scope creep boundaries, and demo walkthroughs."
        },
        {
            "id": "freelancer-operations",
            "name": "Freelancer Operations",
            "module": "Freelance Suite",
            "category": "Operations",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-operations",
            "path": "agentic-freelance-skills/skills/freelancer-operations",
            "risk": "safe",
            "description": "Handles invoicing schedules, payment chasing, contract agreements, tax bookkeeping, and standard operating procedures."
        },
        {
            "id": "freelancer-post-delivery",
            "name": "Freelancer Post Delivery",
            "module": "Freelance Suite",
            "category": "Delivery",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-post-delivery",
            "path": "agentic-freelance-skills/skills/freelancer-post-delivery",
            "risk": "safe",
            "description": "Packages documentation handovers, maintenance retainer contracts, client testimonials, and case study writeups."
        },
        {
            "id": "freelancer-emergency-kit",
            "name": "Freelancer Emergency Kit",
            "module": "Freelance Suite",
            "category": "Emergency",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-emergency-kit",
            "path": "agentic-freelance-skills/skills/freelancer-emergency-kit",
            "risk": "safe",
            "description": "Provides incident runbooks for live production bugs, client communication templates during outages, and rapid rollback steps."
        },
        {
            "id": "freelancer-developer-resources",
            "name": "Freelancer Developer Resources",
            "module": "Freelance Suite",
            "category": "Tooling",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-developer-resources",
            "path": "agentic-freelance-skills/skills/freelancer-developer-resources",
            "risk": "safe",
            "description": "Curated collection of developer toolchains, boilerplates, contract templates, and deployment scripts for client work."
        },
        {
            "id": "freelancer-help",
            "name": "Freelancer Help Desk",
            "module": "Freelance Suite",
            "category": "Guidance",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-help",
            "path": "agentic-freelance-skills/skills/freelancer-help",
            "risk": "safe",
            "description": "Interactive diagnostic assistant that identifies bottlenecks in client pipeline, project delivery, or pricing strategy."
        },
        {
            "id": "freelancer-identity",
            "name": "Freelancer Identity & Positioning",
            "module": "Freelance Suite",
            "category": "Business",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": "freelancer-identity",
            "path": "agentic-freelance-skills/skills/freelancer-identity",
            "risk": "safe",
            "description": "Refines professional positioning, niche specialization, developer bio, GitHub presentation, and service offerings."
        }
    ]
    for s in freelance_items:
        add_skill(s)

    # 4. ScrollHeart
    add_skill({
        "id": "scrollheart",
        "name": "ScrollHeart Motion Engine",
        "module": "ScrollHeart",
        "category": "Frontend Motion",
        "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
        "command": "scrollheart",
        "path": "ScrollHeart/.agents/skills/scrollheart",
        "risk": "safe",
        "description": "Builds cinematic, scroll-driven web experiences using HTML, CSS, and GSAP ScrollTrigger. Produces single-page static sites deployable on GitHub Pages."
    })

    # 5. Gravitas & Unslop
    add_skill({
        "id": "gravitas",
        "name": "Gravitas Engineering Runtime",
        "module": "Engineering & Reliability",
        "category": "Verification",
        "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
        "command": "gravitas decide",
        "path": "skills/gravitas",
        "risk": "safe",
        "description": "Engineering reliability runtime enforcing six invariants: ground before mutating, stay in scope, require evidence, avoid identical retries, satisfy contract gates, and state unverifiable claims."
    })
    add_skill({
        "id": "unslop",
        "name": "Unslop Writing Standard",
        "module": "Engineering & Reliability",
        "category": "Quality",
        "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
        "command": "unslop",
        "path": "skills/unslop",
        "risk": "safe",
        "description": "Enforces natural human language in technical docs. Strips AI buzzwords, decorative symbols, superficial clauses, and false ranges."
    })

    # 6. SEO & AEO Suite
    seo_items = [
        ("seo", "SEO Hub", "Universal SEO and AEO analysis hub coordinating 25 specialized audit modules and subagents."),
        ("seo-audit", "SEO Full Audit", "Runs complete technical, content, and on-page audits across entire domains with prioritized issue matrices."),
        ("seo-page", "SEO Single Page", "Performs deep inspection of one target URL including tags, schema, speed, and content depth."),
        ("seo-technical", "SEO Technical Audit", "Evaluates crawlability, indexability, status codes, canonical tags, redirects, and rendering speed."),
        ("seo-geo", "Generative Engine Optimization", "Optimizes site content for AI answer engines (AI Overviews, ChatGPT, Perplexity, Gemini) citations."),
        ("seo-agentic", "Agentic SEO Readiness", "Audits website accessibility for autonomous AI browsing agents, llms.txt, and structured catalogs."),
        ("seo-content", "SEO Content & E-E-A-T", "Scores content for usefulness, author experience, topic depth, and freedom from AI phrasing."),
        ("seo-content-brief", "SEO Content Brief", "Generates detailed keyword-targeted outlines, competitor section counts, and semantic target entities."),
        ("seo-schema", "SEO Schema Markup", "Generates and validates Schema.org JSON-LD structured data for products, articles, organizations, and FAQ."),
        ("seo-sitemap", "SEO Sitemap Suite", "Generates, validates, and audits XML sitemaps to prevent index bloat and dead URL crawls."),
        ("seo-images", "SEO Image Optimization", "Checks image dimensions, formats, alt descriptions, Core Web Vitals impact, and WebP compression."),
        ("seo-local", "Local SEO & Map Pack", "Audits Google Business Profile consistency, regional citations, NAP data, and local search rankings."),
        ("seo-maps", "SEO Maps Intelligence", "Provides geo-grid ranking tracking, competitor service radius checks, and local review velocity analysis."),
        ("seo-competitor-pages", "SEO Competitor Comparison Pages", "Generates high-intent comparison and alternative pages with objective feature matrices."),
        ("seo-programmatic", "Programmatic SEO", "Architects scalable page templates, database-driven URL paths, and internal link trees for large catalogs."),
        ("seo-plan", "Strategic SEO Planning", "Develops custom multi-month SEO roadmaps based on site niche, search demand, and competitor gaps."),
        ("seo-cluster", "SEO Keyword Clustering", "Groups search keywords by SERP result overlap into hub-and-spoke topic structures."),
        ("seo-backlinks", "SEO Backlink Profile", "Analyzes referring domains, anchor text ratios, link velocity, toxic spam signals, and competitors."),
        ("seo-drift", "SEO Drift Monitoring", "Captures baseline snapshots of meta titles and tags to detect accidental regressions after deployments."),
        ("seo-ecommerce", "E-commerce SEO", "Optimizes product detail pages, merchant feeds, faceted navigation, and shopping schema."),
        ("seo-sxo", "Search Experience Optimization", "Diagnoses search intent mismatches by comparing SERP page layouts to user search expectations."),
        ("seo-google", "Google Search APIs", "Interfaces with Search Console, URL Inspection, PageSpeed Insights, and CrUX field metrics."),
        ("seo-hreflang", "International SEO & Hreflang", "Audits and generates correct language and regional alternate link tags for global audiences."),
        ("seo-dataforseo", "DataForSEO Live Data", "Pulls live SERP rankings, search volumes, and backlink data through DataForSEO APIs."),
        ("seo-image-gen", "SEO Asset Image Gen", "Builds search-optimized OpenGraph cards, social preview headers, and article hero visuals."),
        ("seo-flow", "FLOW SEO Framework", "Applies the Find, Leverage, Optimize, and Win framework across search research workflows.")
    ]
    for sid, name, desc in seo_items:
        add_skill({
            "id": sid,
            "name": name,
            "module": "SEO & AEO Suite",
            "category": "SEO",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": f"/{sid.replace('-', ' ')} <url>",
            "path": f"skills/{sid}",
            "risk": "safe",
            "description": desc
        })

    # 7. Founder Suite
    founder_items = [
        ("founder-board", "Founder Board of Directors", "Scores business concepts through three frameworks: $100M Offers, Zero to One, and product focus."),
        ("founder-brand", "Founder Brand Designer", "Develops brand names, one-line promises, taglines, visual palettes, and trademark checks."),
        ("founder-cfo", "Founder CFO", "Calculates unit economics, gross margins, break-even unit volumes, and year-one cash runway."),
        ("founder-competitors", "Founder Competitor Mapping", "Identifies direct competitors and market substitutes from public review complaints to find market gaps."),
        ("founder-consumer", "Founder Consumer Panel", "Simulates 100 diverse buyer profiles against your pitch to surface objections and purchase rates."),
        ("founder-launch", "Founder Launch Lead", "Builds staged launch plans: cheap demand test, opening day countdown checklist, and 30-day KPI tracker."),
        ("founder-marketing", "Founder Marketing Director", "Translates customer objections into positioning, channel distribution, and 30-day launch copy."),
        ("founder-offer", "Founder Offer Architect", "Creates high-value offers with clear guarantees, bonuses, and low delivery costs."),
        ("founder-ops", "Founder Operations Manager", "Specifies day-one operating routines, supplier costs, staffing plans, and risk registers."),
        ("founder-plan", "Founder Business Planner", "Assembles board votes, unit margins, and launch steps into an investor-ready business plan."),
        ("founder-pricing", "Founder Pricing Strategy", "Calculates Van Westendorp price sensitivity ranges to recommend tiered price ladders.")
    ]
    for sid, name, desc in founder_items:
        add_skill({
            "id": sid,
            "name": name,
            "module": "Founder Suite",
            "category": "Business",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": sid,
            "path": f"skills/{sid}",
            "risk": "safe",
            "description": desc
        })

    # 8. Engineering & Developer Tools
    dev_tools = [
        ("reverse-engineer-anything", "Reverse Engineer Anything (REA)", "Disassembles and analyzes native binaries, Electron applications, .NET code, APKs, and web bundles."),
        ("graphify", "Graphify Codebase Knowledge", "Transforms source repositories into persistent graph structures with god nodes and dependency maps."),
        ("bang-motion", "Bang Motion Web Graphics", "Builds cinematic web animations and video-style kinetic typography using HTML, CSS, and GSAP."),
        ("voice-notifier", "Voice Notifier & Phone Alert", "Speaks a concise completion message and triggers a KDE Connect phone ping when tasks finish."),
        ("ui-ux-pro-max", "UI/UX Pro Max Design Intelligence", "Design database covering 79 UI styles, 192 product palettes, 74 font pairings, and 119 UX rules."),
        ("ui-styling", "UI Styling & Components", "Builds accessible UI components with Tailwind CSS and accessible primitive component patterns."),
        ("slides", "Strategic HTML Presentations", "Creates presentation slides in static HTML using responsive design tokens and charts."),
        ("banner-design", "Multi-Platform Banner Design", "Designs social, ad, and website hero banners across 12 layout styles."),
        ("design-system", "Token Architecture Design System", "Defines primitive, semantic, and component design tokens in CSS custom properties."),
        ("upstash", "Upstash Serverless Integration", "Integrates serverless Redis caching, rate limiting, QStash queues, Vector search, and sandboxed containers.")
    ]
    for sid, name, desc in dev_tools:
        add_skill({
            "id": sid,
            "name": name,
            "module": "Engineering & Developer Tools",
            "category": "Engineering",
            "runtime": ["AGY", "Codex", "Claude Code", "Antigravity"],
            "command": sid,
            "path": f"skills/{sid}",
            "risk": "safe",
            "description": desc
        })

    # 9. Aegis Core Skills
    aegis_core_path = os.path.join(REPO_ROOT, "Aegis/library/core/skills_index.json")
    if os.path.exists(aegis_core_path):
        with open(aegis_core_path) as f:
            core_raw = json.load(f)
            for item in core_raw:
                cid = item.get("id") or item.get("name")
                add_skill({
                    "id": cid,
                    "name": cid.replace("-", " ").title(),
                    "module": "Aegis Core",
                    "category": "Core Engineering",
                    "runtime": ["Codex", "AGY", "Claude Code"],
                    "command": f"aegis use {cid}",
                    "path": f"Aegis/library/core/{item.get('path', 'skills/' + cid)}",
                    "risk": "safe",
                    "description": item.get("description", "Core engineering skill.")
                })

    # 10. Aegis Experts Skills
    aegis_exp_path = os.path.join(REPO_ROOT, "Aegis/library/experts/skills_index.json")
    if os.path.exists(aegis_exp_path):
        with open(aegis_exp_path) as f:
            exp_data = json.load(f).get("skills", [])
            for item in exp_data:
                cid = item.get("name")
                add_skill({
                    "id": cid,
                    "name": cid.replace("-", " ").title(),
                    "module": "Aegis Experts",
                    "category": "Specialized Audit",
                    "runtime": ["Codex", "AGY", "Claude Code"],
                    "command": f"aegis use {cid}",
                    "path": f"Aegis/{item.get('path', 'library/experts/' + cid)}",
                    "risk": "safe",
                    "description": item.get("description", "Domain expert skill.")
                })

    # 11. Aegis Community Skills
    aegis_comm_path = os.path.join(REPO_ROOT, "Aegis/library/community/skills_index.json")
    if os.path.exists(aegis_comm_path):
        with open(aegis_comm_path) as f:
            comm_raw = json.load(f)
            for item in comm_raw:
                cid = item.get("id") or item.get("name")
                desc = item.get("description", "")
                cat = item.get("category", "Community")
                add_skill({
                    "id": cid,
                    "name": cid.replace("-", " ").title(),
                    "module": "Aegis Community",
                    "category": cat.capitalize(),
                    "runtime": ["Codex", "Claude Code", "AGY"],
                    "command": f"aegis use {cid}",
                    "path": f"Aegis/library/community/{item.get('path', 'skills/' + cid)}",
                    "risk": item.get("risk", "safe"),
                    "description": desc
                })

    print(f"Total compiled unique skills: {len(skills)}")

    # Write skills-data.json
    data_out = os.path.join(DOCS_DIR, "skills-data.json")
    with open(data_out, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2, ensure_ascii=False)
    print(f"Saved: {data_out}")

    # Generate sitemap.xml
    sitemap_out = os.path.join(DOCS_DIR, "sitemap.xml")
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://krishujeniya.github.io/SKILL/</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#anchor</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#council</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#freelance</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#scrollheart</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#aegis</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#gravitas</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#unslop</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#seo</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#founder</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://krishujeniya.github.io/SKILL/#explorer</loc>
    <lastmod>2026-11-02</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    with open(sitemap_out, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"Saved: {sitemap_out}")

    # Generate robots.txt
    robots_out = os.path.join(DOCS_DIR, "robots.txt")
    robots_content = """User-agent: *
Allow: /

Sitemap: https://krishujeniya.github.io/SKILL/sitemap.xml
"""
    with open(robots_out, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print(f"Saved: {robots_out}")

    # Generate llms.txt (per llms.txt standard)
    llms_out = os.path.join(DOCS_DIR, "llms.txt")
    llms_content = f"""# SKILL Documentation

> The unified AI agent skills, frameworks, and tooling monorepo.
> Maintained by krishujeniya.
> Total skills documented: {len(skills)}

## Core Frameworks

- Anchor: Scoped, verifiable agent orchestration system with five gates (understand, analyze, plan, implement, verify), contract enforcement, and MCP server.
- Agent Council: Multi-agent CLI deliberation panel running Codex, Gemini, Claude, and Antigravity in parallel subprocesses for architecture consensus.
- Agentic Freelance Skills: End-to-end autonomous freelance consulting lifecycle from lead prospecting to contract delivery and operations.
- ScrollHeart: Cinematic scroll-driven web animations using GSAP and native CSS timelines for GitHub Pages.
- Aegis: Verification library and skill repository with 1,500+ community, core, and expert skills.

## Reliability and Quality Standards

- Gravitas: Six engineering invariants: ground before mutating, stay in declared scope, require evidence for completion, avoid identical retries, satisfy contract gates, and state unverifiable claims explicitly.
- Unslop: Writing standard prohibiting AI tells, filler vocabulary, decorative emojis, superficial clauses, and false ranges.

## Specialized Suites

- SEO Suite: 25 modules covering technical audits, single-page inspection, E-E-A-T analysis, generative engine optimization, schema, sitemaps, and programmatic SEO.
- Founder Suite: 11 business modeling skills including board reviews, CFO unit economics, buyer simulations, and launch checklists.

## Full Skill Catalog

Access the complete structured JSON catalog at https://krishujeniya.github.io/SKILL/skills-data.json
"""
    with open(llms_out, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"Saved: {llms_out}")

    # Generate ai-catalog.json
    catalog_out = os.path.join(DOCS_DIR, "ai-catalog.json")
    catalog_data = {
        "name": "SKILL Monorepo",
        "description": "Unified AI agent skills, frameworks, and tooling monorepo.",
        "url": "https://krishujeniya.github.io/SKILL/",
        "version": "2.5.0",
        "total_skills": len(skills),
        "modules": [
            "Anchor",
            "Agent Council",
            "Freelance Suite",
            "ScrollHeart",
            "Aegis Core",
            "Aegis Experts",
            "Aegis Community",
            "SEO & AEO Suite",
            "Founder Suite",
            "Engineering & Reliability"
        ],
        "runtimes_supported": ["AGY", "Codex", "Claude Code", "Antigravity", "Bun"]
    }
    with open(catalog_out, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Saved: {catalog_out}")

    # Write .nojekyll
    nojekyll_out = os.path.join(DOCS_DIR, ".nojekyll")
    with open(nojekyll_out, "w", encoding="utf-8") as f:
        f.write("")
    print(f"Saved: {nojekyll_out}")

    # Synchronize skills into AGY and Codex runtimes
    sync_skills_to_runtimes()

def sync_skills_to_runtimes():
    print("\n--- Synchronizing skills to AGY and Codex runtimes ---")
    gemini_skills_dir = os.path.expanduser("~/.gemini/skills")
    gemini_config_skills_dir = os.path.expanduser("~/.gemini/config/skills")
    codex_skills_dir = os.path.expanduser("~/.codex/skills")
    agents_skills_dir = os.path.expanduser("~/.agents/skills")

    repo_skills = {}

    anchor_path = os.path.join(REPO_ROOT, "Anchor/.agents/skills")
    if os.path.exists(anchor_path):
        for s in os.listdir(anchor_path):
            sp = os.path.join(anchor_path, s)
            if os.path.isdir(sp) and os.path.exists(os.path.join(sp, "SKILL.md")):
                repo_skills[s] = sp

    freelance_path = os.path.join(REPO_ROOT, "agentic-freelance-skills/skills")
    if os.path.exists(freelance_path):
        for s in os.listdir(freelance_path):
            sp = os.path.join(freelance_path, s)
            if os.path.isdir(sp) and os.path.exists(os.path.join(sp, "SKILL.md")):
                repo_skills[s] = sp

    scrollheart_path = os.path.join(REPO_ROOT, "ScrollHeart/.agents/skills/scrollheart")
    if os.path.exists(os.path.join(scrollheart_path, "SKILL.md")):
        repo_skills["scrollheart"] = scrollheart_path

    council_path = os.path.join(REPO_ROOT, "agent-council/skills/claude-code")
    if os.path.exists(council_path):
        for s in os.listdir(council_path):
            sp = os.path.join(council_path, s)
            if os.path.isdir(sp) and os.path.exists(os.path.join(sp, "SKILL.md")):
                repo_skills[s] = sp

    all_to_sync = dict(repo_skills)
    for src_dir in [agents_skills_dir, gemini_config_skills_dir, gemini_skills_dir]:
        if os.path.exists(src_dir):
            for s in os.listdir(src_dir):
                if s.startswith("."): continue
                sp = os.path.join(src_dir, s)
                if os.path.isdir(sp) and os.path.exists(os.path.join(sp, "SKILL.md")):
                    if s not in all_to_sync:
                        all_to_sync[s] = sp

    def link_skill(target_dir, name, src):
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, name)
        if os.path.islink(dest):
            curr = os.readlink(dest)
            if curr != src:
                os.unlink(dest)
                os.symlink(src, dest)
                return "updated"
            return "ok"
        elif os.path.exists(dest):
            return "exists"
        else:
            os.symlink(src, dest)
            return "created"

    for target_dir, label in [
        (gemini_skills_dir, "AGY (~/.gemini/skills)"),
        (gemini_config_skills_dir, "AGY config (~/.gemini/config/skills)"),
        (codex_skills_dir, "Codex (~/.codex/skills)"),
        (agents_skills_dir, "Agents (~/.agents/skills)"),
    ]:
        count = 0
        for name, sp in all_to_sync.items():
            res = link_skill(target_dir, name, sp)
            if res in ("ok", "created", "updated", "exists"):
                count += 1
        print(f"Verified {label}: {count} skills available.")

if __name__ == "__main__":
    build_data()
