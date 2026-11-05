---
name: agyos-app-launch-checklist
description: Production pre-launch verification checklist for web and mobile apps. Covers Open Graph previews, Twitter Cards, favicons, meta tags, canonical URLs, error tracking, and release gates.
---

# AGYOS Production App Launch Checklist

A deterministic pre-launch audit checklist to verify frontend assets, metadata, security headers, search indexing, and error monitoring prior to production deployment.

## 1. Social Sharing & Open Graph Metadata

Ensure app previews render accurately on WhatsApp, Twitter/X, LinkedIn, Discord, and Slack:

1. Preview Image Specifications:
   - Dimensions: 1200 x 630 px (1.91:1 aspect ratio).
   - Format: PNG or optimized JPG (<1 MB).
   - Path: Hosted on an absolute HTTPS URL (e.g., `https://example.com/og-image.png`).

2. Next.js App Router Implementation (`app/layout.tsx`):
```typescript
export const metadata = {
  title: "Application Name — Core Proposition",
  description: "Direct, technical description of product value and features.",
  metadataBase: new URL("https://example.com"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Application Name — Core Proposition",
    description: "Direct, technical description of product value and features.",
    url: "https://example.com",
    siteName: "Application Name",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Application preview",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Application Name — Core Proposition",
    description: "Direct, technical description of product value and features.",
    images: ["/og-image.png"],
  },
};
```

## 2. Favicon & App Icon Matrix

Verify browser tab icons across all device resolutions:

- `favicon.ico`: 32 x 32 px multi-layer icon in web root.
- `icon.svg`: Scalable vector icon for modern browsers.
- `apple-touch-icon.png`: 180 x 180 px square for iOS home screen shortcuts.
- `site.webmanifest`: PWA manifest declaring app name, icons (192x192, 512x512), and background theme colors.

## 3. Search Engine Indexing & Discovery

1. Canonical Tags:
   - Ensure every public page declares `<link rel="canonical" href="https://example.com/path">` to prevent duplicate content indexing.
2. `robots.txt`:
   - Permit public crawling while protecting internal APIs and admin routes:
     ```text
     User-agent: *
     Allow: /
     Disallow: /api/
     Disallow: /dashboard/
     Sitemap: https://example.com/sitemap.xml
     ```
3. `sitemap.xml`:
   - Generate valid XML with prioritized public routes, clean changefreq, and lastmod timestamps.

## 4. Observability & Error Handling

- Custom Error Pages: Confirm `/404` and `/500` handle user errors with clear recovery options and brand styling.
- Client Error Boundary: Catch unhandled runtime exceptions in UI components without crashing entire views.
- Error Tracking: Configure telemetry (Sentry, Axiom, or OpenTelemetry) with environment tagging and sourcemap uploads.

## 5. Security & Performance Release Gates

- CSP & Security Headers: Configure `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`.
- Lighthouse Audit: Verify Performance >= 90, Accessibility >= 95, Best Practices >= 95, SEO >= 95 on mobile and desktop profiles.
