---
name: agyos-founder-guide
description: Operational guide for startup founders navigating skill stacking, customer discovery, pricing psychology, MVP scoping, and investor narrative construction within the AGYOS ecosystem.
---

# AGYOS Founder Operational Guide

A tactical handbook for technical founders, operators, and solo builders developing early-stage software products with AGYOS.

## 1. Founder Skill-Stacking Model

Sustainable software ventures require four interlocking competencies:

1. Technical Execution:
   - Deep familiarity with contract-first API design, 5-Gate lifecycle governance, and monotonic test coverage.
   - Using AI agents as leveraged junior engineers rather than autonomous decision-makers without review.

2. Positioning & Direct Distribution:
   - Defining a specific audience niche with clear, jargon-free problem statements.
   - Establishing early distribution channels (communities, niche directories, Show HN) before writing backend code.

3. Pricing Psychology & Unit Economics:
   - Anchoring prices to customer outcome value rather than server cost or development hours.
   - Designing unambiguous billing tiers with straightforward usage limits.

4. Empirical Validation Loops:
   - Structured user interviews focused on historical user behaviors rather than hypothetical future interest.

## 2. Customer Discovery & Problem Validation

Apply these interview invariants during discovery:

- Inquire About Past Actions: Ask "When was the last time you encountered this problem?" instead of "Would you pay for a tool that solves this?".
- Quantify Current Workarounds: Determine how the user currently handles the issue (spreadsheets, manual labor, competing software). If no workaround exists, the problem is rarely acute.
- Identify Willingness-to-Pay: If an interview subject affirms a problem is critical, request a concrete commitment (pre-order, deposit, or scheduled onboarding session).

## 3. High-Velocity MVP Scoping

When scoping an initial release:

1. Identify the Single Load-Bearing Feature:
   - Strip away secondary admin dashboards, multi-tenant billing permutations, and advanced configuration toggles.
   - Retain only the singular workflow that delivers the core value proposition.

2. Enforce the 48-Hour Build Rule:
   - An MVP implementation plan must be executable within 48 engineering hours using proven boilerplate templates and free-tier infrastructure (`agyos-free-infra-catalog`).

## 4. Value-Based Pricing Architecture

- Tier 1 (Free / Starter): Restricted by usage volume (e.g., 50 operations/month) or features, sufficient for individual evaluation without generating continuous operational loss.
- Tier 2 (Professional): Positioned for commercial operators and growing teams; captures direct economic value.
- Tier 3 (Enterprise): Includes SSO/SAML, dedicated SLAs, custom data residency, and audit logging.
- Pricing Rule: Avoid charging micro-transactions ($1-3/mo) that fail to cover Stripe transaction minimums and customer support overhead.

## 5. Narrative & Communications Discipline

- Ban AI Jargon: Eliminate buzzwords ("seamless", "game-changing", "revolutionary") in pitch decks, landing pages, and documentation.
- Lead with Metrics: Replace subjective claims with concrete technical baselines (latency numbers, uptime figures, test counts).
