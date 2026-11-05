#!/usr/bin/env python3
"""Basic zero-browser documentation build validation."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse, unquote


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default='_site')
    parser.add_argument('--base', default='/AGYOS/')
    args = parser.parse_args()
    site = Path(args.site)
    assert (site / 'index.html').is_file(), 'No landing page'
    assert (site / 'catalog/index.html').is_file(), 'Existing catalog not preserved'
    assert (site / 'catalog/skills-data.json').is_file(), 'Skill catalog index missing'
    assert (site / 'site.js').is_file(), 'Interaction JS missing'
    assert (site / 'site.css').is_file(), 'Site styles missing'
    inventory = json.loads((site / 'content-inventory.json').read_text())
    index = json.loads((site / 'search-index.json').read_text())
    assert len(index) == len(inventory['published']) >= 8, 'Public content inventory is incomplete'
    all_routes = {x['url'] for x in index}
    assert len(all_routes) == len(index), 'Duplicate documentation URLs'
    assert any('architecture' in x['content'].lower() for x in index), 'Index does not contain document content'
    for item in inventory['published']:
        source = item['source']
        assert not source.startswith(('.agents/', 'skills/', 'docs/references/')), source
        assert source not in inventory['excluded'], 'Excluded source published: '+source
        url = item['url']
        assert url.startswith(args.base+'docs/')
        relative = url.removeprefix(args.base)
        page = site / relative / 'index.html'
        assert page.exists(), 'Missing ' + str(page)
        content = page.read_text(encoding='utf-8')
        assert 'id="doc-content"' in content and '<article' in content, 'Missing actual rendered documentation'
        assert 'data-search-open' in content and 'docs-sidebar' in content, 'Missing reader navigation/search'
        assert '<script' in content and 'site.js' in content
        assert '<script>alert(' not in content, 'Suspicious unsanitized HTML'
        for href in re.findall(r'href="([^"]+)"',content):
            if href.startswith((args.base+'docs/', args.base+'catalog/', args.base+'assets/')):
                u = urlparse(href)
                path = unquote(u.path).removeprefix(args.base)
                if path.endswith('/'):
                    target = site / path / 'index.html'
                else:
                    target = site / path
                assert target.exists(), 'Broken internal link: '+href+' in '+source
    assert not (site/'RESEARCH_PLAN.md').exists()
    assert not (site/'AGENTS.md').exists()
    assert not (site/'.agents').exists()
    assert 'prefers-reduced-motion' in (site/'site.css').read_text(), 'No reduced-motion CSS'
    assert 'reduceMotion.matches' in (site/'site.js').read_text(), 'No reduced-motion JS'
    print(f'PASS: {len(index)} searchable documentation pages, safe publication allowlist, catalog, internal links, reduced motion and assets')


if __name__ == '__main__':
    main()
