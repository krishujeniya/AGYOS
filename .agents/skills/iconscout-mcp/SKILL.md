---
name: iconscout-mcp
description: Search, inspect, and download design assets from Iconscout's library of 15M+ icons, vector illustrations, 3D icons, and Lottie animations via its MCP server. Use natural language queries to find style-consistent assets and inject them directly into codebases and design files.
risk: low
source: official (iconscout.com/mcp)
date_added: 2026-11-13
---
# Iconscout MCP

Access Iconscout's 15M+ asset library — icons, vector illustrations, 3D icons, and Lottie animations — through its hosted MCP server. Search in natural language, inspect specs before committing, download in the right format, and find style-matched siblings to keep UI design consistent.

## MCP Server

**Endpoint:** `https://mcp.iconscout.com/mcp`  
**Auth:** OAuth browser sign-in (no manual API keys). Works with your existing Iconscout account — free and paid plan limits apply to downloads.  
**Clients:** Claude Desktop, Claude Code, Cursor, ChatGPT, Antigravity.

## Tools

| Tool | Purpose |
|------|---------|
| `search_assets` | Natural language search across all asset types with style/color/license filters |
| `get_asset_details` | Fetch formats, dimensions, license tier, pack name, and contributor for any asset |
| `download_assets` | Download a file in SVG, PNG, Lottie JSON, GIF, or MP4 to inject into the project |
| `find_related_assets` | Find assets from the same visual pack/family for style consistency |
| `browse_categories` | Navigate the category tree to refine broad concepts before searching |

## Asset Types

| Type | Formats | Best for |
|------|---------|---------|
| **Icons** | SVG, PNG | UI controls, navigation, status indicators |
| **Illustrations** | SVG, PNG | Hero sections, empty states, onboarding flows |
| **3D Icons** | PNG | Marketing pages, app store screenshots, landing pages |
| **Lottie Animations** | JSON, GIF, MP4 | Micro-interactions, loading states, success/error feedback |

## Workflow

1. **Clarify the need** — confirm asset type (icon vs illustration vs Lottie), style (outline / filled / flat / 3D), color palette, and license constraint (free vs premium).
2. **Browse first if vague** — call `browse_categories` with a broad concept to land in the right classification before searching.
3. **Search with specifics** — call `search_assets` with a descriptive natural language query. Include style, orientation, and color explicitly:
   - ✅ `"outline style shopping cart icon, blue stroke, free"`
   - ✅ `"flat 3D rocket facing right, premium"`
   - ❌ `"icon"` (too vague)
4. **Inspect before download** — call `get_asset_details` to confirm format availability and license tier. Never download premium assets without user confirmation they have an active plan.
5. **Find siblings for consistency** — if the user is building a UI set, call `find_related_assets` on the first chosen asset to pull matching icons from the same pack.
6. **Download** — call `download_assets` with the correct format for the target use case:
   - SVG → React/Vue components, CSS `background-image`
   - PNG → `<img>` tags, documentation, app store assets
   - JSON → Lottie player (`@lottiefiles/react-lottie-player`, `lottie-web`)
   - GIF/MP4 → Email templates, video embeds

## Usage Patterns

### Drop an SVG icon into a React component
```text
1. search_assets query="outline bell notification icon" asset_type="icon" license="free"
2. get_asset_details asset_id="<id>"
3. download_assets asset_id="<id>" format="svg"
4. Paste SVG inline or save to src/assets/icons/bell.svg
```

### Add a Lottie animation to a loading state
```text
1. search_assets query="spinning loader animation minimal" asset_type="lottie"
2. get_asset_details asset_id="<id>"        # confirm JSON format available
3. download_assets asset_id="<id>" format="json"
4. Use with <Lottie animationData={data} loop={true} />
```

### Build a consistent icon set for a navigation bar
```text
1. search_assets query="solid filled home icon dark" asset_type="icon"
2. find_related_assets asset_id="<chosen home icon id>"   # get the full pack
3. download_assets for each: home, search, profile, settings, notifications
```

## Constraints

- **Download credits apply** — free-plan accounts have monthly download limits. Always call `get_asset_details` to confirm license tier before downloading; surface premium restrictions to the user.
- **Style consistency is mandatory** — never mix outline + filled, or flat + 3D in the same UI view. Always use `find_related_assets` when sourcing multiple icons for the same screen.
- **No hotlinking** — always download and serve assets from your own CDN/bundle; Iconscout URLs are not stable for direct `<img src>` use in production.
- **Attribution** — free assets from Iconscout require attribution unless the account has a paid plan. Confirm with the user before shipping to production.

## Related Skills

- `iconsax-library` — predefined Iconsax React/Vue component library (use this when already locked in to the Iconsax set)
- `design-system-spec-generator` — generates a design system that this skill can populate with icons
- `animejs-animation` — pairs with Lottie downloads for layered animation composition
- `mobile-design` — HIG-aware icon sizing and touch-target guidelines
