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

ROOT = Path(__file__).resolve().parents[1]
GITHUB = 'https://github.com/krishujeniya/AGYOS/blob/main/'
URL = 'https://krishujeniya.github.io/AGYOS/'


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
    config = json.loads((ROOT / 'site/public-docs.json').read_text(encoding='utf-8'))
    approved = list(config['documents'])
    used = {d['source'] for d in approved}
    public_root = ROOT / safe_path(config['public_root'])
    if public_root.exists():
        for md in sorted(public_root.rglob('*.md')):
            relative = md.relative_to(ROOT).as_posix()
            if relative in used:
                continue
            slug = relative.removeprefix(config['public_root'].rstrip('/') + '/').removesuffix('.md')
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
        if lang in ('mermaid', 'plantuml'):
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
        if full in ('docs/assets/logo.svg', 'docs/assets/logo-mark.svg', 'docs/assets/agyos-logo.svg', 'assets/logo.svg'):
            return self.base + 'assets/' + posixpath.basename(full)
        # Source files that are not approved remain on GitHub and are not republished.
        if full.startswith(('http:', 'https:')):
            return '#'
        suffix = ('#' + quote(p.fragment)) if p.fragment else ''
        return GITHUB + quote(full, safe='/') + suffix


def source_text(path: Path) -> str:
    source = path.read_text(encoding='utf-8')
    # The GitHub README uses HTML layout wrappers and badges; do not execute raw HTML.
    # Leave all Markdown and fenced code unchanged and omit only the decorative header.
    if path.name == 'README.md' and path.parent == ROOT:
        source = re.sub(r'\A\s*<p align="center">.*?</p>\s*<h1 align="center">.*?</h1>\s*<p align="center">.*?</p>\s*<p align="center">.*?</p>\s*---', '# AGYOS\n', source, flags=re.S)
    return source


def pages_sidebar(docs: list[dict], active: str, base: str) -> str:
    groups: dict[str, list[dict]] = {}
    for item in docs:
        groups.setdefault(item['category'], []).append(item)
    return ''.join('<section class="side-group"><p class="side-label">' + html.escape(category) + '</p>' + ''.join(
        '<a href="' + base + 'docs/' + doc['slug'] + '/" class="side-link' + (' active' if doc['slug']==active else '') + '"' + (' aria-current="page"' if doc['slug']==active else '') + '>' + html.escape(doc['title']) + '</a>' for doc in items) + '</section>' for category, items in groups.items())


def template(base: str, title: str, description: str, canonical: str, content: str, page_class: str = '') -> str:
    origin = URL.rstrip('/') if base == '/AGYOS/' else ''
    content = content.replace('{{BASE}}', base)
    return (f'<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(title)} | AGYOS</title><meta name="description" content="{html.escape(description,quote=True)}">'
        f'<meta name="theme-color" content="#f6f7f9"><meta name="robots" content="index,follow"><link rel="canonical" href="{html.escape(canonical)}">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="AGYOS"><meta property="og:title" content="{html.escape(title)} | AGYOS">'
        f'<meta property="og:description" content="{html.escape(description,quote=True)}"><meta property="og:url" content="{html.escape(canonical)}">'
        f'<meta property="og:image" content="{URL}assets/social-card.svg"><link rel="icon" type="image/svg+xml" href="{base}assets/logo-mark.svg">'
        f'<link rel="stylesheet" href="{base}site.css"><script defer src="{base}site.js"></script></head><body class="{html.escape(page_class)}">'
        + content + '</body></html>')


def site_header(base: str, docs: bool = False) -> str:
    return (f'<a href="#main" class="skip-link">Skip to content</a><header class="topbar"><div class="topbar-inner"><a class="wordmark" href="{base}" aria-label="AGYOS home">'
        f'<img src="{base}assets/logo-mark.svg" width="30" height="30" alt=""><span>AGYOS</span></a>'
        f'<nav class="toplinks" aria-label="Primary"><a href="{base}#capabilities">Platform</a><a href="{base}#architecture">Architecture</a><a href="{base}docs/overview/" {"aria-current=\"page\"" if docs else ""}>Documentation</a><a href="{base}catalog/">Skill catalog</a></nav>'
        f'<div class="header-actions"><button class="search-trigger" type="button" data-search-open aria-label="Search documentation"><span>Search docs</span><kbd>⌘ K</kbd></button>'
        f'<button type="button" class="theme-button" data-theme-toggle aria-label="Change theme"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.4 1.4m11.34 11.34 1.4 1.4M2 12h2m16 0h2M4.93 19.07l1.4-1.4M17.67 6.33l1.4-1.4"/></svg></button>'
        f'<a class="header-github" href="https://github.com/krishujeniya/AGYOS" target="_blank" rel="noopener noreferrer">GitHub ↗</a>'
        f'<button class="menu-button" type="button" data-menu aria-label="Open navigation" aria-expanded="false"><span></span><span></span></button></div></div></header>')


def footer(base: str) -> str:
    return (f'<footer class="site-footer"><div class="footer-inner"><div><a href="{base}" class="footer-brand">AGYOS<span class="footer-dot">.</span></a><p>Autonomous agent engineering, with governance built in.</p></div><div class="footer-links">'
        f'<a href="{base}docs/overview/">Docs</a><a href="{base}catalog/">Catalog</a><a href="{base}docs/security/">Security</a><a href="https://github.com/krishujeniya/AGYOS" target="_blank" rel="noopener noreferrer">Source ↗</a></div></div><div class="footer-bottom">'
        '<span>Open-source project by Krish Ujeniya.</span><span>Designed for clarity. Built for builders.</span></div></footer>')


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
        shutil.copy2(ROOT / 'site' / asset, out / asset)
    shutil.copytree(ROOT / 'docs/assets', out / 'assets', dirs_exist_ok=True)
    for asset in ('social-card.svg', 'logo.svg', 'logo-mark.svg'):
        if (ROOT / 'docs/assets' / asset).exists():
            shutil.copy2(ROOT / 'docs/assets' / asset, out / 'assets' / asset)
    catalog = out / 'catalog'
    catalog.mkdir(parents=True, exist_ok=True)
    for asset in ('index.html','docs.js','docs.css','skills-data.json'):
        shutil.copy2(ROOT / 'docs' / asset, catalog / asset)
    shutil.copytree(ROOT / 'docs/assets', catalog / 'assets', dirs_exist_ok=True)
    docs = config['documents']
    search_index = []
    inventory = []
    for i, doc in enumerate(docs):
        source = ROOT / doc['source']
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
            + f'<article class="prose" id="doc-content">{rendered}</article>{pager}<div class="source-link"><a href="{GITHUB+quote(doc["source"],safe="/")}" target="_blank" rel="noopener noreferrer">View source on GitHub ↗</a></div></main>'
            + f'<aside class="docs-toc" aria-label="On this page"><div class="toc-title">On this page</div>{toc or "<p>No subsections</p>"}</aside></div>' + footer(base) + search_dialog(base))
        dest = out / 'docs' / doc['slug'] / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(template(base, doc['title'], doc['description'], URL+'docs/'+doc['slug']+'/', main, 'docs-page'), encoding='utf-8')
        search_index.append({'title':doc['title'],'category':doc['category'],'description':doc['description'],'url':base+'docs/'+doc['slug']+'/', 'content': re.sub(r'\s+', ' ', re.sub(r'```[\s\S]*?```',' ',raw))[:24000]})
        inventory.append({'source':doc['source'],'url':base+'docs/'+doc['slug']+'/', 'title':doc['title'],'category':doc['category'],'visibility':'public','imported':True,'headings':len(renderer.headings),'notes':renderer.unsupported})
    home = (ROOT / 'site/index.html').read_text(encoding='utf-8').replace('{{BASE}}', base).replace('{{DOCS_COUNT}}', str(len(docs)))
    home = home.replace('<!-- SITE-HEADER -->',site_header(base)).replace('<!-- SITE-FOOTER -->',footer(base)).replace('<!-- SITE-SEARCH -->',search_dialog(base))
    (out / 'index.html').write_text(template(base,'Autonomous agent operating system','Discover AGYOS: hierarchical governance, five execution pods, and a searchable engineering runbook catalog.', URL, home, 'home-page'),encoding='utf-8')
    (out / 'docs/index.html').write_text('<!doctype html><meta http-equiv="refresh" content="0;url='+base+'docs/overview/"><a href="'+base+'docs/overview/">Open documentation</a>',encoding='utf-8')
    (out / 'search-index.json').write_text(json.dumps(search_index,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (out / 'content-inventory.json').write_text(json.dumps({'published':inventory,'excluded':config['exclude'],'policy':'Explicit allowlist + docs/public opt-in'},indent=2),encoding='utf-8')
    urls = [URL, URL+'catalog/'] + [URL+'docs/'+doc['slug']+'/' for doc in docs]
    (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(url)+'</loc></url>' for url in urls)+'</urlset>',encoding='utf-8')
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+URL+'sitemap.xml\n',encoding='utf-8')
    (out / '.nojekyll').touch()
    return {'pages':len(docs),'source_paths':[d['source'] for d in docs],'destination':str(out)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',default='_site')
    parser.add_argument('--base',default='/AGYOS/')
    args = parser.parse_args()
    base = '/' + args.base.strip('/') + '/' if args.base.strip('/') else '/'
    out = Path(args.out).resolve()
    if out == ROOT or out == ROOT / 'docs' or out == ROOT / 'site':
        raise ValueError('Do not overwrite source directories')
    if out.exists():
        shutil.rmtree(out)
    print(json.dumps(build(out,base),indent=2))


if __name__ == '__main__':
    main()
