---
name: agyos-lead-scraper
description: Local and headless web scraping playbook for Google Maps, directories, and business leads. Covers query generation, rate limiting, proxy handling, data normalization, and CSV/JSON export.
---

# AGYOS Lead & Directory Scraper Kit

Autonomous operational playbook for extracting verified business leads, local service listings, and directory data using containerized scrapers and headless browser automation.

## 1. Query Planning & Coordinate Grid Mapping

To scrape local business directories or Google Maps without truncation:

1. Query Structuring:
   - Combine target industry keyword with granular geographic tokens:
     - `"<niche> in <suburb>, <city>"`
     - Example: `"pediatric dentists in North Denver, CO"`
2. Bounding Box & Grid Traversal:
   - High-density metros return capped result counts (typically 120-200 listings max per viewport).
   - Divide metropolitan areas into a 3x3 or 4x4 coordinate grid using latitude/longitude bounding steps.
   - Run localized queries per cell to extract full directory depth.

## 2. Data Extraction Schema

Normalize all extracted lead records to this typed schema:

```json
{
  "business_name": "string (required)",
  "phone": "string (E.164 formatted)",
  "website": "string (URL with https:// prefix)",
  "category": "string (primary business category)",
  "address": "string (street, city, state, postal code)",
  "latitude": "number (float)",
  "longitude": "number (float)",
  "rating": "number (float, 1.0 - 5.0)",
  "review_count": "integer",
  "verified": "boolean",
  "opening_hours": "object",
  "scraped_at": "string (ISO 8601 timestamp)"
}
```

## 3. Anti-Detection & Rate-Limiting Controls

When executing headless browser scrapers (Playwright / Puppeteer):

- Jittered Delays: Insert randomized execution delays between actions (e.g., 800ms - 2200ms) rather than static sleep intervals.
- User-Agent Rotation: Cycle authentic modern browser user-agents across desktop Chrome, Edge, and Safari profiles.
- Headless Masking: Disable navigator automation flags (`navigator.webdriver = undefined`) and pass valid WebGL vendor/renderer parameters.
- Respect Rate Boundaries: If HTTP 429 or CAPTCHA challenge is encountered, trigger exponential backoff and alert operator per AGYOS guidelines.

## 4. Normalization & Deduplication Pipeline

1. Deduplication Key:
   - Primary key: Normalized phone number or clean domain name (`example.com`).
   - Secondary key: Lowercase string match on `(business_name, postal_code)`.
2. Clean Export:
   - Output normalized records to CSV and JSON formats:
     ```bash
     python3 scripts/normalize_leads.py input_raw.json --out verified_leads.csv
     ```
   - Strip tracking query parameters (`utm_*`, `fbclid`, `gclid`) from extracted URLs.
