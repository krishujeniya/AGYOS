# AGYOS documentation website

A dependency-light, statically generated documentation site for GitHub Pages. It reads only explicitly permitted Markdown files, generates a searchable index and one HTML page per approved document, and preserves the pre-existing skills explorer under `/catalog/`.

## Build

Requires Python 3.10+ and `mistune>=3,<4` (installed by GitHub Actions):

```bash
python -m pip install 'mistune>=3,<4'
python scripts/build_docs_site.py --out _site --base /AGYOS/
python -m http.server 8000 --directory _site
```

For local previews at `http://localhost:8000/`, pass `--base /` instead.

## Publication policy

`site/public-docs.json` explicitly lists public documents. Newly approved Markdown under `docs/public/` is included automatically. Other repository Markdown, tracked state files, prompt libraries, PDFs, private files, and agent instructions are not copied into `_site`. Exclusions are listed in the generated `content-inventory.json`. Keep `docs/public/` strictly public, and review every newly committed file before publication. Do not place credentials in docs or image assets.

Source code for the original interactive catalog is preserved at `docs/`; the build copies its public HTML, JS, CSS, logo assets, and skills metadata into the isolated `/catalog/` route. It does not export any other repository content.

## Checks

```bash
python scripts/build_docs_site.py --out _site --base /
python scripts/test_docs_site.py
```

These checks validate output paths, document ingestion, generated links and security exclusions. Lighthouse and real-browser audits should be run against the deployed site; no unmeasured score is claimed.
