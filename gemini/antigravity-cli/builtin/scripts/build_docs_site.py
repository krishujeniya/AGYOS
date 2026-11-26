#!/usr/bin/env python3
"""Build a public-only AGYOS documentation site from an explicit allowlist."""
from __future__ import annotations
import argparse
import html
import json
import posixpath
import re
import shutil
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import mistune

ROOT = Path(__file__).resolve().parents[4]
GITHUB = 'https://github.com/krishujeniya/AGYOS/blob/main/'
URL = 'https://agyos.pages.dev/'


def slugify(text: str) -> str:
    value = re.sub(r'<[^>]*>', '', text)
    value = re.sub(r'[^a-zA-Z0-9\s_-]', '', value).strip().lower()
    return re.sub(r'[\s_]+', '-', value) or 'section'


def plain(text: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', text))).strip()


def safe_path(path: str) -> str:
    p = Path(path)
    if p.is_absolute() or '..' in p.parts or not re.fullmatch(r'[\w./-]+', path):
        raise ValueError('Unsafe document path: ' + path)
    return p.as_posix()


def read_config() -> dict:
    config = json.loads((ROOT / 'frontend/public-docs.json').read_text(encoding='utf-8'))
    approved = list(config['documents'])
    used = {d['source'] for d in approved}
    public_root_cfg = config.get('public_root')
    if public_root_cfg:
        public_root = ROOT / safe_path(public_root_cfg)
        if public_root.exists():
            for md in sorted(public_root.rglob('*.md')):
                relative = md.relative_to(ROOT).as_posix()
                if relative in used:
                    continue
                slug = relative.removeprefix(public_root_cfg.rstrip('/') + '/').removesuffix('.md')
                if slug.casefold() == 'readme':
                    slug = 'readme'
                approved.append({'source': relative, 'slug': 'guides/' + slug, 'title': md.stem.replace('-', ' ').title(), 'category': 'Guides', 'description': 'Public AGYOS guide.'})
                used.add(relative)
    slugs = set()
    for doc in approved:
        source = safe_path(doc['source'])
        slug = safe_path(doc['slug']).strip('/')
        if slug in slugs or not slug:
            raise ValueError('Duplicate or invalid slug: ' + slug)
        slugs.add(slug)
        path = ROOT / source
        if not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise FileNotFoundError('Approved documentation missing: ' + source)
        if path.suffix.lower() not in ('.md', '.mdx'):
            raise ValueError('Only Markdown/MDX are supported: ' + source)
        doc['slug'] = slug
        doc['source'] = source
    config['documents'] = approved
    return config


def _arch_flowchart_html() -> str:
    """Return the monochrome 6-layer AGYOS architecture flowchart HTML."""
    return (
        '<div class="arch-flowchart doc-flowchart" aria-label="AGYOS System Architecture Flowchart">'
        '<div class="flow-trigger"><div class="flow-pill operator-node">'
        '<span class="flow-pill-tag">Operator Input</span>'
        '<strong>Operator / User Request</strong>'
        '<span class="flow-pill-sub">Natural Language Prompt</span>'
        '</div><div class="flow-arrow-down" aria-hidden="true">↓ <span>Routes via CLI &amp; MCP Syscall Bus</span></div></div>'
        '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">L0 / L2</span>'
        '<h3>Kernel Hooks &amp; Syscall Bus</h3>'
        '<span class="subgraph-sub">bin/agyos • state-server.cjs • hooks/</span></div>'
        '<div class="subgraph-cards double-grid">'
        '<div class="flow-card"><span class="card-kicker">Layer 2 • Syscall Bus</span><strong>CLI &amp; MCP Daemon</strong>'
        '<p><code>bin/agyos</code> dispatcher and zero-dependency stdio JSON-RPC 2.0 <code>state-server.cjs</code></p></div>'
        '<div class="flow-card"><span class="card-kicker">Layer 0 • Safety Interceptor</span><strong>Dual Hook Boundary</strong>'
        '<p>Fail-closed <code>authorizer.py</code> (R3 outbox blocking) and fail-open <code>agy_os_hook.py</code></p></div>'
        '</div></div>'
        '<div class="flow-connector" aria-hidden="true">↓ <span>Compiles Intent, EVPI &amp; Role Assignment</span></div>'
        '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">L4 / L5</span>'
        '<h3>Governance, 104-Role Matrix &amp; EVPI</h3>'
        '<span class="subgraph-sub">agyos_decision/ • 12 Departments • 5 Pods</span></div>'
        '<div class="subgraph-cards triple-grid">'
        '<div class="flow-card"><span class="card-kicker">Layer 5 • EVPI Gate</span><strong>Intent &amp; EVPI Compiler</strong>'
        '<p>Compiles prompt into typed <code>TaskContract</code> and computes Howard 1966 EVPI</p></div>'
        '<div class="flow-card"><span class="card-kicker">Layer 4 • Hierarchy</span><strong>104-Role Virtual Org</strong>'
        '<p>12 functional departments partitioned into 5 governing operational pods (<code>roles.py</code>)</p></div>'
        '<div class="flow-card"><span class="card-kicker">Layer 4 • Runbooks</span><strong>TOON Skill Catalog</strong>'
        '<p>2,289 TOON skills across 103 role packs with JIT on-demand runbook retrieval</p></div>'
        '</div></div>'
        '<div class="flow-connector" aria-hidden="true">↓ <span>Dispatches TaskContract to 5-Gate SOP &amp; 7-Step Cycle</span></div>'
        '<div class="flow-subgraph cycle-subgraph"><div class="subgraph-header"><span class="subgraph-num">L3</span>'
        '<h3>7-Step Autonomous Engineering Cycle</h3>'
        '<span class="subgraph-sub">5-Gate SOP Engine • UNDERSTAND → VERIFY</span></div>'
        '<div class="cycle-track">'
        '<div class="cycle-step"><span class="step-num">1</span><strong>Think</strong><small>Role Alignment</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">2</span><strong>Plan</strong><small>Checkpoints</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">3</span><strong>Build</strong><small>Maker TDD</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">4</span><strong>Review</strong><small>Checker Audit</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">5</span><strong>Test</strong><small>Static Gates</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">6</span><strong>Ship</strong><small>Commit &amp; Lock</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
        '<div class="cycle-step"><span class="step-num">7</span><strong>Reflect</strong><small>CURRENT.md</small></div>'
        '</div></div>'
        '<div class="flow-connector" aria-hidden="true">↓ <span>Atomic Persistence &amp; Runtime Compression</span></div>'
        '<div class="flow-dual-grid">'
        '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">L1</span>'
        '<h3>State, Memory &amp; Vault</h3><span class="subgraph-sub">SQLite • AES-256-GCM</span></div>'
        '<div class="subgraph-cards double-grid">'
        '<div class="flow-card"><span class="card-kicker">Persistence</span><strong>ACID SQLite State</strong><p>Monotonic revisions, CAS checks, and idempotent replay</p></div>'
        '<div class="flow-card"><span class="card-kicker">Safety</span><strong>R3 Outbox &amp; Snapshots</strong><p>Pre-write backups (<code>state_ledger.py</code>) and <code>PENDING_COMMIT</code> holds</p></div>'
        '<div class="flow-card"><span class="card-kicker">Memory Tiers</span><strong>3-Tier Virtual Memory</strong><p><code>memory.json</code> working set, <code>CURRENT.md</code> recall, and archival catalog</p></div>'
        '<div class="flow-card"><span class="card-kicker">Confidentiality</span><strong>Encrypted Private Vault</strong><p>AES-256-GCM vault &amp; X25519 endpoint-side envelopes</p></div>'
        '</div></div>'
        '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">CODEC</span>'
        '<h3>Model Router &amp; TOON</h3><span class="subgraph-sub">T0–T3 • Exact Encoding</span></div>'
        '<div class="subgraph-cards vertical-grid">'
        '<div class="flow-card"><span class="card-kicker">Routing Policy</span><strong>Skill &amp; Model Router</strong><p>T0–T3 complexity tiers with privacy gating and KV-cache prefixing</p></div>'
        '<div class="flow-card"><span class="card-kicker">Data Protocol</span><strong>TOON Codec Engine</strong><p>Typed Token-Oriented Object Notation parsing and compression</p></div>'
        '<div class="flow-card"><span class="card-kicker">Static Portal</span><strong>Docs &amp; Catalog Builder</strong><p>Allowlisted Markdown site generator (<code>build_docs_site.py</code>)</p></div>'
        '</div></div></div>'
        '<div class="flow-connector" aria-hidden="true">↓ <span>Monotonic Ratchet Verification &amp; Release</span></div>'
        '<div class="flow-subgraph delivery-subgraph"><div class="subgraph-header"><span class="subgraph-num">SHIP</span>'
        '<h3>Gated Verification &amp; Delivery</h3><span class="subgraph-sub">Single main Branch • Cloudflare Pages</span></div>'
        '<div class="subgraph-cards double-grid">'
        '<div class="flow-card highlight-card"><span class="card-kicker">CI/CD Pipeline</span><strong>GitHub Actions Verification</strong><p><code>ci.yml</code>, <code>deploy.yml</code>, and <code>codeql.yml</code> with monotonic test ratchets</p></div>'
        '<div class="flow-card highlight-card"><span class="card-kicker">Protected Deployment</span><strong>Single main Branch &amp; Edge</strong><p>Verified author lock (Krish Ujeniya) deploying to <code>agyos.pages.dev</code></p></div>'
        '</div></div></div>\n'
    )


def _render_ascii_diagram(code: str) -> str | None:
    """Render known ASCII architecture/pipeline blocks as monochrome flowcharts."""
    if '[GATE 1: UNDERSTAND]' in code:
        return (
            '<div class="arch-flowchart doc-flowchart" aria-label="AGYOS 5-Gate SOP Flow">'
            '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">SOP</span>'
            '<h3>5-Gate Deterministic Pipeline</h3><span class="subgraph-sub">Code = SOP(Team)</span></div>'
            '<div class="cycle-track">'
            '<div class="cycle-step"><span class="step-num">1</span><strong>Understand</strong><small>Gate 1</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">2</span><strong>Analyze</strong><small>Gate 2</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">3</span><strong>Plan</strong><small>Gate 3</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">4</span><strong>Implement</strong><small>Gate 4</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">5</span><strong>Verify</strong><small>Gate 5</small></div>'
            '</div>'
            '<div class="flow-connector" aria-hidden="true">↳ <span>Fast-Path Router (Complexity ≤ 2): Bypasses Gates 1–3 → IMPLEMENT → VERIFY</span></div>'
            '</div></div>\n'
        )
    if '[DISCOVERY]' in code and '[HANDOVER]' in code:
        return (
            '<div class="arch-flowchart doc-flowchart" aria-label="7-Phase Working Backwards SDLC Pipeline">'
            '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">SDLC</span>'
            '<h3>7-Phase Working Backwards Pipeline</h3><span class="subgraph-sub">sdlc.py</span></div>'
            '<div class="cycle-track">'
            '<div class="cycle-step"><span class="step-num">1</span><strong>Discovery</strong><small>PR / FAQ</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">2</span><strong>PRD</strong><small>Criteria</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">3</span><strong>Architecture</strong><small>C4 &amp; ADR</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">4</span><strong>TDD Build</strong><small>80%+ Cov</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">5</span><strong>Verify</strong><small>Static Proof</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">6</span><strong>Release</strong><small>Rollout</small></div><div class="cycle-arrow" aria-hidden="true">→</div>'
            '<div class="cycle-step"><span class="step-num">7</span><strong>Handover</strong><small>CURRENT.md</small></div>'
            '</div></div></div>\n'
        )
    if 'AGYOS Operational Kernel' in code:
        return (
            '<div class="arch-flowchart doc-flowchart" aria-label="AGYOS Operational Kernel Topology">'
            '<div class="flow-subgraph"><div class="subgraph-header"><span class="subgraph-num">KERNEL</span>'
            '<h3>AGYOS Operational Kernel</h3><span class="subgraph-sub">gemini/antigravity-cli/bin/agyos</span></div>'
            '<div class="subgraph-cards triple-grid">'
            '<div class="flow-card"><span class="card-kicker">Routing</span><strong>Decision Engine</strong><p><code>skills_router.py</code> &amp; <code>model_router.py</code></p></div>'
            '<div class="flow-card"><span class="card-kicker">Syscall Bus</span><strong>FastMCP Daemon</strong><p><code>state-server.cjs</code> (stdio JSON-RPC)</p></div>'
            '<div class="flow-card"><span class="card-kicker">Guardrails</span><strong>Security Hooks</strong><p><code>authorizer.py</code> &amp; <code>agy_os_hook.py</code></p></div>'
            '</div>'
            '<div class="flow-connector" aria-hidden="true">↓ <span>Persists Projections &amp; Secrets</span></div>'
            '<div class="subgraph-cards double-grid">'
            '<div class="flow-card highlight-card"><span class="card-kicker">State Machine</span><strong><code>state.json</code> &amp; SQLite</strong><p><code>gemini/antigravity-cli/builtin/state/state.json</code></p></div>'
            '<div class="flow-card highlight-card"><span class="card-kicker">Encrypted Store</span><strong>Private Vault</strong><p><code>~/.local/state/agyos/private-memory.vault.json</code></p></div>'
            '</div></div></div>\n'
        )
    return None


class Renderer(mistune.HTMLRenderer):
    def __init__(self, source: str, routes: dict, base: str):
        super().__init__(escape=True)
        self.source, self.routes, self.base = source, routes, base
        self.headings: list[dict] = []
        self.heading_counts: Counter = Counter()
        self.unsupported: list[str] = []

    def heading(self, text: str, level: int, **attrs) -> str:
        heading = plain(text)
        raw_id = slugify(heading)
        self.heading_counts[raw_id] += 1
        slug = raw_id if self.heading_counts[raw_id] == 1 else f'{raw_id}-{self.heading_counts[raw_id]}'
        self.headings.append({'id':slug,'title':heading,'level':level})
        return f'<h{level} id="{html.escape(slug)}"><a class="heading-anchor" href="#{html.escape(slug)}" aria-label="Link to {html.escape(heading)}">#</a>{text}</h{level}>\n'

    def block_code(self, code: str, info: str | None = None) -> str:
        lang = ((info or '').split() or [''])[0].lower()
        if lang == 'mermaid':
            return _arch_flowchart_html()
        ascii_html = _render_ascii_diagram(code) if not lang else None
        if ascii_html:
            return ascii_html
        if lang == 'plantuml':
            self.unsupported.append(lang + ' diagram rendered as source')
        return f'<div class="code-shell"><div class="code-toolbar"><span>{html.escape(lang or "text")}</span><button type="button" class="code-copy" aria-label="Copy code">Copy</button></div><pre><code class="language-{html.escape(lang)}">{html.escape(code)}</code></pre></div>\n'

    def link(self, text: str, url: str, title: str | None = None) -> str:
        href = self.resolve(url)
        safe = html.escape(href, quote=True)
        attr = f' title="{html.escape(title,quote=True)}"' if title else ''
        if href.startswith('https://'):
            attr += ' target="_blank" rel="noopener noreferrer"'
        return f'<a href="{safe}"{attr}>{text}</a>'

    def image(self, text: str, url: str, title: str | None = None) -> str:
        href = self.resolve(url, image=True)
        return f'<img loading="lazy" src="{html.escape(href, quote=True)}" alt="{html.escape(plain(text),quote=True)}">'

    def resolve(self, target: str, image: bool = False) -> str:
        if target.startswith('#'):
            return '#' + slugify(unquote(target[1:]))
        p = urlsplit(target)
        if p.scheme in ('https', 'http', 'mailto'):
            return target
        if p.scheme or target.startswith('//'):
            return '#'
        if target.startswith('/AGYOS/'):
            return target
        if not p.path:
            return '#'
        source_dir = posixpath.dirname(self.source)
        full = posixpath.normpath(posixpath.join(source_dir, unquote(p.path)))
        if full.startswith('../'):
            return '#'
        if not image and full in self.routes:
            suffix = ('#' + slugify(unquote(p.fragment))) if p.fragment else ''
            return self.base + 'docs/' + self.routes[full] + '/' + suffix
        if full == 'catalog' or full == 'catalog/':
            return self.base + 'catalog/'
        if full in ('assets/logo.svg', 'assets/logo-mark.svg', 'assets/agyos-logo.svg', 'assets/social-card.svg', 'assets/agyos-4k.png', 'assets/agyos-icon.png', 'docs/assets/logo.svg', 'docs/assets/logo-mark.svg', 'docs/assets/agyos-logo.svg'):
            return self.base + 'assets/' + posixpath.basename(full)
        # Source files that are not approved remain on GitHub and are not republished.
        if full.startswith(('http:', 'https:')):
            return '#'
        if full.lower().endswith('.md'):
            return GITHUB + quote(full, safe='/')
        suffix = ('#' + quote(p.fragment)) if p.fragment else ''
        return GITHUB + quote(full, safe='/') + suffix


def source_text(path: Path) -> str:
    source = path.read_text(encoding='utf-8')
    # The GitHub README uses HTML layout wrappers and badges; do not execute raw HTML.
    # Leave all Markdown and fenced code unchanged and omit only the decorative header.
    if path.name == 'README.md' and path.parent == ROOT:
        source = re.sub(r'\A(?:\s*<(?:p|h1)\b[^>]*>.*?</(?:p|h1)>)+', '', source, flags=re.S).lstrip()
    return source


def pages_sidebar(docs: list[dict], active: str, base: str) -> str:
    groups: dict[str, list[dict]] = {}
    for item in docs:
        groups.setdefault(item['category'], []).append(item)
    return ''.join('<section class="side-group"><p class="side-label">' + html.escape(category) + '</p>' + ''.join(
        '<a href="' + base + 'docs/' + doc['slug'] + '/" class="side-link' + (' active' if doc['slug']==active else '') + '"' + (' aria-current="page"' if doc['slug']==active else '') + '>' + html.escape(doc['title']) + '</a>' for doc in items) + '</section>' for category, items in groups.items())


def _json_ld(title: str, description: str, canonical: str, page_class: str) -> str:
    """Build Schema.org JSON-LD graph for SEO, AEO, and GEO."""
    author = {
        '@type': 'Person',
        '@id': f'{URL}#krish-ujeniya',
        'name': 'Krish Ujeniya',
        'alternateName': ['krishujeniya', '@krishujeniya'],
        'mainEntityOfPage': URL,
        'url': 'https://github.com/krishujeniya',
        'sameAs': [
            'https://github.com/krishujeniya',
            'https://github.com/sponsors/krishujeniya',
        ],
    }
    software = {
        '@type': 'SoftwareApplication',
        '@id': f'{URL}#agyos',
        'name': 'AGYOS',
        'alternateName': 'AGYOS Cognitive Operating System',
        'description': 'Autonomous Cognitive Operating System for AGY CLI with a 6-layer governance architecture, 104-role matrix, and 2,289 TOON skills.',
        'applicationCategory': 'DeveloperApplication',
        'operatingSystem': 'Linux, macOS',
        'url': URL,
        'downloadUrl': 'https://github.com/krishujeniya/AGYOS',
        'softwareVersion': '3.2.0',
        'license': 'https://opensource.org/licenses/Apache-2.0',
        'author': {'@id': f'{URL}#krish-ujeniya'},
        'creator': {'@id': f'{URL}#krish-ujeniya'},
    }
    website = {
        '@type': 'WebSite',
        '@id': f'{URL}#website',
        'name': 'AGYOS by Krish Ujeniya (krishujeniya)',
        'alternateName': ['AGYOS', 'krishujeniya'],
        'url': URL,
        'publisher': {'@id': f'{URL}#krish-ujeniya'},
        'potentialAction': {
            '@type': 'SearchAction',
            'target': f'{URL}catalog/?q={{search_term_string}}',
            'query-input': 'required name=search_term_string',
        },
    }
    page_type = 'TechArticle' if page_class == 'docs-page' else 'WebPage'
    webpage = {
        '@type': page_type,
        '@id': f'{canonical}#webpage',
        'url': canonical,
        'name': f'{title} | AGYOS',
        'description': description,
        'isPartOf': {'@id': f'{URL}#website'},
        'about': {'@id': f'{URL}#agyos'},
        'author': {'@id': f'{URL}#krish-ujeniya'},
    }
    if page_type == 'TechArticle':
        webpage['headline'] = title
    graph = [author, software, website, webpage]
    if page_class == 'home-page':
        graph.append({
            '@type': 'FAQPage',
            '@id': f'{URL}#faq',
            'mainEntity': [
                {
                    '@type': 'Question',
                    'name': 'What is AGYOS?',
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': 'AGYOS is an Autonomous Cognitive Operating System for AGY CLI created by Krish Ujeniya. It combines a 6-layer governance architecture, 104 enterprise roles across 5 pods, 2,289 TOON-native skills, and an automated 7-step engineering cycle.',
                    },
                },
                {
                    '@type': 'Question',
                    'name': 'Who created AGYOS?',
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': 'AGYOS is created and maintained by Krish Ujeniya (@krishujeniya) under the Apache 2.0 license at https://github.com/krishujeniya/AGYOS.',
                    },
                },
                {
                    '@type': 'Question',
                    'name': 'How do you install AGYOS?',
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': 'Run curl -fsSL https://raw.githubusercontent.com/krishujeniya/AGYOS/main/gemini/antigravity-cli/builtin/scripts/install.sh | bash or clone the repository and run make install.',
                    },
                },
            ],
        })
    payload = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    return payload.replace('</', '<\\/')


def template(base: str, title: str, description: str, canonical: str, content: str, page_class: str = '') -> str:
    content = content.replace('{{BASE}}', base)
    full_title = f'{title} | AGYOS' if 'AGYOS' not in title else title
    keywords = 'AGYOS, Krish Ujeniya, krishujeniya, Autonomous Cognitive Operating System, AGY CLI, AI agent operating system, TOON skills, multi-agent governance'
    return (f'<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(full_title)}</title><meta name="description" content="{html.escape(description,quote=True)}">'
        f'<meta name="author" content="Krish Ujeniya"><meta name="keywords" content="{keywords}">'
        f'<meta name="theme-color" content="#000000"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
        f'<link rel="canonical" href="{html.escape(canonical)}"><link rel="alternate" type="text/plain" title="LLMs.txt" href="{base}llms.txt">'
        f'<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="AGYOS by Krish Ujeniya">'
        f'<meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(description,quote=True)}">'
        f'<meta property="og:url" content="{html.escape(canonical)}"><meta property="og:image" content="{URL}assets/social-card.svg">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:creator" content="@krishujeniya">'
        f'<meta name="twitter:title" content="{html.escape(full_title)}"><meta name="twitter:description" content="{html.escape(description,quote=True)}">'
        f'<meta name="twitter:image" content="{URL}assets/social-card.svg"><link rel="icon" type="image/svg+xml" href="{base}assets/logo-mark.svg">'
        f'<script type="application/ld+json">{_json_ld(title, description, canonical, page_class)}</script>'
        f'<link rel="stylesheet" href="{base}site.css"><script defer src="{base}site.js"></script></head><body class="{html.escape(page_class)}">'
        + content + '</body></html>')


def site_header(base: str, docs: bool = False) -> str:
    return (f'<a href="#main" class="skip-link">Skip to content</a><header class="topbar"><div class="topbar-inner"><a class="wordmark" href="{base}" aria-label="AGYOS home">'
        f'<img src="{base}assets/logo-mark.svg" width="30" height="30" alt=""><span>AGYOS</span></a>'
        f'<nav class="toplinks" aria-label="Primary"><a href="{base}#capabilities">Platform</a><a href="{base}#architecture">Architecture</a><a href="{base}docs/overview/" {"aria-current=\"page\"" if docs else ""}>Documentation</a><a href="{base}catalog/">Skill catalog</a></nav>'
        f'<div class="header-actions"><button class="search-trigger" type="button" data-search-open aria-label="Search documentation"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/></svg><span>Search docs</span><kbd>⌘ K</kbd></button>'
        f'<button type="button" class="theme-button" data-theme-toggle aria-label="Toggle black and white theme" title="Toggle theme"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3v18a9 9 0 0 0 0-18Z" fill="currentColor" stroke="none"/></svg></button>'
        f'<a class="sponsor-pill" href="https://github.com/sponsors/krishujeniya" target="_blank" rel="noopener noreferrer" aria-label="Sponsor on GitHub">'
        f'<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6.5 5.5 5.5 0 0 1 21.5 12C19 16.5 12 21 12 21Z"/></svg>'
        f'<span>Sponsor</span></a>'
        f'<a class="sponsor-pill header-github" href="https://github.com/krishujeniya/AGYOS" target="_blank" rel="noopener noreferrer">GitHub ↗</a>'
        f'<button class="menu-button" type="button" data-menu aria-label="Open navigation" aria-expanded="false"><span></span><span></span></button></div></div></header>')


def footer(base: str) -> str:
    return (f'<footer class="site-footer"><div class="footer-shell"><div class="footer-top">'
        '<div class="footer-tagline">© 2026 · AUTONOMOUS AGENT ENGINEERING WITH GOVERNANCE BUILT IN</div>'
        f'<nav class="footer-links" aria-label="Footer"><a href="{base}docs/overview/">Docs</a><a href="{base}catalog/">Catalog</a><a href="{base}docs/security/">Security</a><a href="https://github.com/sponsors/krishujeniya" target="_blank" rel="noopener noreferrer">Sponsor</a><a href="https://github.com/krishujeniya/AGYOS" target="_blank" rel="noopener noreferrer">Source</a></nav></div>'
        '<div class="footer-banner"><div class="footer-wordmark" aria-label="AGYOS">'
        '<span class="footer-letter">A</span><span class="footer-letter">G</span><span class="footer-letter footer-float-1">Y</span><span class="footer-letter footer-float-2">O</span><span class="footer-letter footer-float-3">S</span>'
        '</div></div>'
        '<div class="footer-bottom"><div class="footer-meta"><span>AGYOS</span><span class="footer-sep">/</span><span>BY KRISH UJENIYA</span></div>'
        '<a href="#" class="back-top" aria-label="Back to top">Back to Top</a>'
        '</div></div></footer>')


def search_dialog(base: str) -> str:
    return (f'<dialog class="search-dialog" id="search-dialog" aria-label="Search documentation"><div class="search-dialog-head"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/></svg>'
        '<input id="search-input" aria-label="Search documentation" type="search" placeholder="Search documentation…" autocomplete="off"><button type="button" id="search-close" aria-label="Close search">Esc</button></div>'
        '<div id="search-results" class="search-results" role="listbox" aria-label="Search results"><p class="search-hint">Type to search real documentation content.</p></div><div class="search-dialog-footer">'
        '<span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span><span><kbd>↵</kbd> Open</span></div></dialog>')


def build(out: Path, base: str) -> dict:
    config = read_config()
    routes = {doc['source']: doc['slug'] for doc in config['documents']}
    out.mkdir(parents=True, exist_ok=True)
    for asset in ('site.css', 'site.js'):
        shutil.copy2(ROOT / 'frontend' / asset, out / asset)
    if (ROOT / 'frontend/_headers').exists():
        shutil.copy2(ROOT / 'frontend/_headers', out / '_headers')
    shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
    catalog = out / 'catalog'
    catalog.mkdir(parents=True, exist_ok=True)
    for asset in ('skills-data.json', 'skills-data.toon'):
        src = ROOT / 'docs' / asset
        if src.exists():
            shutil.copy2(src, catalog / asset)
    shutil.copytree(ROOT / 'assets', catalog / 'assets', dirs_exist_ok=True)
    catalog_template = (ROOT / 'frontend/catalog.html').read_text(encoding='utf-8').replace('{{BASE}}', base)
    catalog_template = catalog_template.replace('<!-- SITE-HEADER -->', site_header(base, False)).replace('<!-- SITE-FOOTER -->', footer(base)).replace('<!-- SITE-SEARCH -->', search_dialog(base))
    (catalog / 'index.html').write_text(template(base, 'Skill catalog', 'Search and explore 2,289 modular engineering skills in AGYOS.', URL+'catalog/', catalog_template, 'catalog-page'), encoding='utf-8')
    docs = config['documents']
    search_index = []
    inventory = []
    for i, doc in enumerate(docs):
        source = ROOT / doc['source']
        tracked_source = doc['source']
        raw = source_text(source)
        renderer = Renderer(doc['source'], routes, base)
        md = mistune.create_markdown(renderer=renderer, plugins=['table', 'strikethrough', 'url', 'task_lists'])
        rendered = md(raw)
        if '<script' in rendered.lower():
            raise ValueError('Unexpected script in rendered Markdown ' + doc['source'])
        headings = [h for h in renderer.headings if h['level'] in (2,3)]
        toc = ''.join(f'<a class="toc-level-{h["level"]}" href="#{html.escape(h["id"])}">{html.escape(h["title"])}</a>' for h in headings)
        prev = docs[i-1] if i else None
        nxt = docs[i+1] if i+1<len(docs) else None
        pager = '<div class="doc-pager">' + (f'<a href="{base}docs/{prev["slug"]}/"><span>← Previous</span><strong>{html.escape(prev["title"])}</strong></a>' if prev else '<span></span>') + (f'<a href="{base}docs/{nxt["slug"]}/"><span>Next →</span><strong>{html.escape(nxt["title"])}</strong></a>' if nxt else '<span></span>') + '</div>'
        main = (site_header(base, True) + '<div class="docs-layout"><button type="button" class="mobile-docs-toggle" data-docs-menu aria-expanded="false">Browse documentation <span>☰</span></button>'
            + f'<aside class="docs-sidebar" id="docs-sidebar" aria-label="Documentation navigation"><div class="sidebar-head">Documentation <span>{len(docs)} guides</span></div>{pages_sidebar(docs,doc["slug"],base)}</aside>'
            + f'<main id="main" class="docs-article"><div class="doc-breadcrumb"><a href="{base}docs/overview/">Documentation</a><span>/</span><span>{html.escape(doc["category"])}</span></div>'
            + f'<div class="doc-heading"><p class="eyebrow">{html.escape(doc["category"])}</p><h1>{html.escape(doc["title"])}</h1><p>{html.escape(doc["description"])}</p></div>'
            + f'<article class="prose" id="doc-content">{rendered}</article>{pager}<div class="source-link"><a href="{GITHUB+quote(tracked_source,safe="/")}" target="_blank" rel="noopener noreferrer">View source on GitHub ↗</a></div></main>'
            + f'<aside class="docs-toc" aria-label="On this page"><div class="toc-title">On this page</div>{toc or "<p>No subsections</p>"}</aside></div>' + footer(base) + search_dialog(base))
        dest = out / 'docs' / doc['slug'] / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(template(base, doc['title'], doc['description'], URL+'docs/'+doc['slug']+'/', main, 'docs-page'), encoding='utf-8')
        search_index.append({'title':doc['title'],'category':doc['category'],'description':doc['description'],'url':base+'docs/'+doc['slug']+'/', 'content': re.sub(r'\s+', ' ', re.sub(r'```[\s\S]*?```',' ',raw))[:24000]})
        inventory.append({'source':doc['source'],'url':base+'docs/'+doc['slug']+'/', 'title':doc['title'],'category':doc['category'],'visibility':'public','imported':True,'headings':len(renderer.headings),'notes':renderer.unsupported})
    home = (ROOT / 'frontend/index.html').read_text(encoding='utf-8').replace('{{BASE}}', base).replace('{{DOCS_COUNT}}', str(len(docs)))
    home = home.replace('<!-- SITE-HEADER -->',site_header(base)).replace('<!-- SITE-FOOTER -->',footer(base)).replace('<!-- SITE-SEARCH -->',search_dialog(base))
    (out / 'index.html').write_text(template(base,'AGYOS by Krish Ujeniya (krishujeniya) — Autonomous Cognitive Operating System','AGYOS by Krish Ujeniya (krishujeniya): 6-layer hierarchical agent operating system, 104 enterprise roles across 5 pods, and 2,289 TOON engineering skills.', URL, home, 'home-page'),encoding='utf-8')
    (out / 'docs/index.html').write_text('<!doctype html><meta http-equiv="refresh" content="0;url='+base+'docs/overview/"><a href="'+base+'docs/overview/">Open documentation</a>',encoding='utf-8')
    (out / 'search-index.json').write_text(json.dumps(search_index,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (out / 'content-inventory.json').write_text(json.dumps({'published':inventory,'excluded':config['exclude'],'policy':'Explicit allowlist'},indent=2),encoding='utf-8')
    sitemap_entries = [(URL, '1.0', 'weekly'), (URL+'catalog/', '0.9', 'weekly')] + [(URL+'docs/'+doc['slug']+'/', '0.8', 'weekly') for doc in docs]
    (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{html.escape(u)}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>' for u, prio, freq in sitemap_entries)+'</urlset>',encoding='utf-8')
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: '+URL+'sitemap.xml\nLlms-txt: '+URL+'llms.txt\n',encoding='utf-8')
    if (ROOT / 'frontend/llms.txt').exists():
        shutil.copy2(ROOT / 'frontend/llms.txt', out / 'llms.txt')
    (out / '.nojekyll').touch()
    return {'pages':len(docs),'source_paths':[d['source'] for d in docs],'destination':str(out)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',default='_site')
    parser.add_argument('--base',default='/AGYOS/')
    args = parser.parse_args()
    base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
    out = Path(args.out).resolve()
    if out == ROOT or out == ROOT / 'docs' or out == ROOT / 'frontend' or out == ROOT / 'gemini':
        raise ValueError('Do not overwrite source directories')
    if out.exists():
        shutil.rmtree(out)
    print(json.dumps(build(out,base),indent=2))


if __name__ == '__main__':
    main()
