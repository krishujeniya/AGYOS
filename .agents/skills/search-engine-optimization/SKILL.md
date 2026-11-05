---
name: search-engine-optimization
description: Inspect search visibility, metadata, crawlability, and eligible structured data using the rendered page and primary evidence.
---
@context": "https://schema.org",
  "@type": "Article",
  "headline": "Page Title Here",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand Name"
  }
}
```

### Audit output shape

```text
[HIGH] Duplicate title tags on product pages
Location: src/routes/products/[slug].tsx
Issue: Dynamic titles collapse to the same default string, which weakens relevance and creates duplicate signals.
Fix: Generate a unique title per product using the product name and primary category.
```

## Anti-Patterns

| Anti-pattern | Fix |
| --- | --- |
| keyword stuffing | write for users first |
| thin near-duplicate pages | consolidate or differentiate them |
| schema for content that is not actually present | match schema to reality |
| content advice without checking the actual page | read the real page first |
| generic “improve SEO” outputs | tie every recommendation to a page or asset |

## Related Skills

- `seo-specialist`
- `frontend-patterns`
- `brand-voice`
- `market-research`
