---
title: "06A: Finance & Invoicing"
description: "International payment methods, tax compliance, expense tracking, and cash-flow systems for solo freelancers."
module: "06-OPERATIONS"
---

# 06A: Finance & Invoicing

> **Principle:** Revenue is vanity, cash flow is sanity. A freelancer who cannot invoice professionally, collect promptly, and reserve for taxes is running a hobby, not a business.

## 1. Payment Infrastructure

### 1.1 Recommended Accounts (Global Solo Operator)

| Account Type | Recommended Providers | Purpose |
|-------------|----------------------|---------|
| **Multi-Currency Wallet** | Wise, Payoneer, EasyStaff Invoice | Receive USD, EUR, GBP with local account details; low FX fees (0.35–1%). |
| **Crypto/Stablecoin** | USDC via Coinbase Commerce, Request Network | Instant settlement, minimal cross-border friction. Treat as income at fair-market value upon receipt. |
| **Local Bank** | Your domestic bank (India: ICICI/HDFC; US: Mercury; UK: Starling) | Withdraw local currency, pay domestic taxes, maintain audit trail. |
| **Emergency Reserve** | High-yield savings or money-market fund | 3–6 months of operating expenses. Non-negotiable. |

### 1.2 Platform-Specific Fee Structures (2026)

| Platform | Freelancer Fee | Client Fee | Withdrawal | Best For |
|----------|---------------|------------|------------|----------|
| **Upwork** | 0–15% sliding | 5% payment processing | Wire, Payoneer, Wise | High-volume, escrow protection |
| **Contra** | $29 per contract (flat) | None | Stripe Connect, bank | Simple, transparent pricing |
| **Fiverr** | 20% flat | Service fee added at checkout | Payoneer, bank | Quick gigs, productized micro-services |
| **Direct Invoice** | None | None | Wise, Payoneer, crypto | Enterprise clients, retainers |

> **Rule:** For projects above $3,000, always invoice directly via Wise / Payoneer. Platform fees on a $5,000 project can exceed $750 on Upwork or $1,000 on Fiverr.

### 1.3 Payment Terms That Protect Cash Flow

| Term | Recommended Setting | Rationale |
|------|---------------------|-----------|
| **Upfront Deposit** | 30–50% before work begins | De-risks scope creep and client ghosting. |
| **Milestone Invoicing** | 25% kickoff / 25% mid / 50% delivery | Aligns cash flow with delivery risk. |
| **Net Due** | Net-7 for retainers; Net-15 for projects | EU Late Payment Directive mandates 60 days B2B max; 30 days for public sector. |
| **Late Fee** | 1.5% per month (18% annual) | Statutory interest in many jurisdictions; deterrent effect. |
| **Final Delivery** | Watermarked / staged until final payment | Leverage, not hostility. |

### 1.4 Invoice Template Structure

Every invoice must contain:

1. **Your legal name / business entity** and tax ID (PAN, VAT, EIN, etc.).
2. **Client legal name**, billing address, and purchase order (if required).
3. **Unique invoice number** (sequential: INV-2026-001).
4. **Issue date** and **due date**.
5. **Line items**: Description, quantity, unit price, subtotal.
   - Example: "ML Pipeline Development — Phase 1: Data Engineering" | 1 | $2,500.00
6. **Tax breakdown**: VAT/GST, withholding tax, or "tax reverse-charged" for B2B cross-border EU transactions.
7. **Payment instructions**: Wise account details, Payoneer link, or crypto wallet address.
8. **Late-payment policy** and interest clause (one sentence at footer).
9. **Thank-you note** and contact email for billing questions.

> **Tooling:** Use Wave (free), FreshBooks, or EasyStaff Invoice for automated compliant invoicing and multi-currency support.

---

## 2. Tax Compliance & Reserves

### 2.1 The 30% Rule

For every dollar/euro/pound received, allocate immediately:

| Bucket | Allocation | Purpose |
|--------|-----------|---------|
| **Operating** | 50% | Living expenses, tools, subcontractor payments. |
| **Tax Reserve** | 30% | Income tax, GST/VAT, professional tax. |
| **Growth / Emergency** | 20% | Courses, equipment, 3-month runway buffer. |

> **Action:** Create three virtual sub-accounts or envelopes. Transfer the 30% tax reserve the same day payment lands. Do not wait until quarter-end.

### 2.2 Jurisdiction-Specific Notes

| Region | Key Compliance Point |
|--------|---------------------|
| **United States** | Clients issue Form 1099-NEC for payments ≥$600/year. Report all income; deduct home-office, software, and professional-development expenses. |
| **European Union** | B2B invoices require VAT ID; reverse-charge applies cross-border. Late-payment interest is statutory (EU Directive 2011/7/EU). |
| **United Kingdom** | Self-assessment due 31 January. CGT on crypto gains (10–20%). Maintain 6-year records. |
| **India** | GST registration mandatory if turnover exceeds ₹20 lakh. Export of services with payment in foreign exchange is zero-rated GST. File GSTR-1 and GSTR-3B monthly/quarterly. |

### 2.3 Deductible Expenses (Common for AI/ML Freelancers)

- Cloud compute (GCP, AWS, Azure) and API costs (OpenAI, Anthropic)
- Software subscriptions (GitHub Copilot, Notion, Figma, Adobe, JetBrains)
- Hardware (laptop, GPU, monitors, ergonomic equipment) — depreciate or Section 179
- Professional development (courses, certifications, conferences)
- Co-working space or home-office percentage of rent/utilities
- Legal and accounting fees
- Internet and phone (business-use percentage)

> **Record-keeping:** Snap receipts immediately into Expensify, Wave, or a dedicated Google Drive folder. Categorize weekly, not annually.

---

## 3. Cash-Flow Forecasting

### 3.1 Simple 90-Day Cash-Flow Sheet

Maintain a rolling spreadsheet with these columns:

| Month | Expected Invoices | Probable Receipts | Fixed Costs | Variable Costs | Net Cash Flow | Cumulative |
|-------|-------------------|-------------------|-------------|----------------|---------------|------------|
| May | $8,000 | $6,400 (80%) | $1,200 | $400 | +$4,800 | $4,800 |
| June | $12,000 | $9,600 (80%) | $1,200 | $600 | +$7,800 | $12,600 |
| July | $5,000 | $4,000 (80%) | $1,200 | $200 | +$2,600 | $15,200 |

> **Assumption:** Assume only 80% of invoiced amounts arrive on time. The remaining 20% arrives 15–30 days late or requires follow-up.

### 3.2 Red-Flag Triggers

- Cumulative cash drops below 1.5× monthly fixed costs → Pause non-essential spending; accelerate outreach.
- Two consecutive months of negative net cash flow → Emergency client acquisition mode (refer to Module 02).
- Client payment delayed >30 days past due → Stop all non-essential work for that client; enforce late fees.

---

## 4. AI Prompts

### Prompt 1: Invoice Line-Item Generator
```
I am a [specialty, e.g., ML Engineer / Full-Stack Developer / Data Scientist].
I need to invoice a client for the following scope:
[ paste project scope or SOW here ]

Break this into 3–5 professional line items with:
- Clear deliverable names
- Quantities (hours, sprints, models, pages)
- Unit prices that reflect value, not just hours
- Subtotals and a grand total

Format as a markdown table suitable for an invoice.
```

### Prompt 2: Tax Deduction Auditor
```
Here is a list of my expenses this quarter:
[ paste expenses ]

For each item, classify it as:
- Fully deductible business expense
- Partially deductible (explain %)
- Personal / non-deductible
- Requires receipt / documentation

Summarize total deductible amount and flag any items that may raise audit risk.
```

### Prompt 3: Cash-Flow Scenario Planner
```
My current monthly fixed costs are $[X].
My average project size is $[Y] with a [Z]-week delivery cycle.
I have [N] active prospects in my pipeline.

Generate a 90-day cash-flow scenario with:
- Conservative (40% close rate)
- Base case (60% close rate)
- Optimistic (80% close rate)

Show monthly net cash flow and cumulative runway for each scenario.
```

---

## 5. Action Checklist

### This Week
- [ ] Open a Wise or Payoneer business account.
- [ ] Create invoice template with sequential numbering and late-fee clause.
- [ ] Set up three virtual accounts: Operating / Tax / Growth.
- [ ] Log all Q2 expenses and categorize them.

### This Month
- [ ] Send every invoice with Net-15 terms and 40% upfront on new projects.
- [ ] Review 90-day cash-flow forecast; adjust outreach if pipeline is thin.
- [ ] Schedule 30 minutes with a tax professional to verify jurisdiction-specific obligations.

### Ongoing
- [ ] Reconcile accounts weekly (Friday afternoon).
- [ ] Follow up on unpaid invoices at Net+7, Net+14, and Net+21.
- [ ] Review and raise rates every 6 months or after every 3 successful projects.

---

*Next: `06B-LEGAL-CONTRACTS.md` — Build your legal shield.*
