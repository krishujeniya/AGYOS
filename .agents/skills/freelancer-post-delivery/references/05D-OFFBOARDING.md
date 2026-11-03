---
module: "05-POST-DELIVERY"
part: "D"
title: "Offboarding"
version: "2026.05"
status: "Production-Ready"
---

# 05D: Offboarding

> **Core Principle:** How you end a project is as important as how you start it. A professional offboarding leaves the door open for future work, referrals, and testimonials.
>
> *"Even if this is the end, make it feel like a beginning."*

---

## Table of Contents

1. [The Offboarding Checklist](#1-the-offboarding-checklist)
2. [Asset Transfer Protocol](#2-asset-transfer-protocol)
3. [Knowledge Transfer](#3-knowledge-transfer)
4. [The Final Invoice](#4-the-final-invoice)
5. [Relationship Preservation](#5-relationship-preservation)
6. [AI Prompts](#6-ai-prompts)
7. [Action Checklist](#7-action-checklist)

---

## 1. The Offboarding Checklist

### The 48-Hour Offboarding Sprint

| Hour | Action | Owner | Status |
|------|--------|-------|--------|
| **0** | Confirm final deliverable acceptance | Client | ☐ |
| **0** | Send final invoice | You | ☐ |
| **2** | Transfer all source code and assets | You | ☐ |
| **2** | Transfer credentials and access | You | ☐ |
| **4** | Send documentation package | You | ☐ |
| **4** | Schedule knowledge transfer call | You | ☐ |
| **8** | Revoke your access to client systems | You | ☐ |
| **24** | Send thank-you + testimonial request | You | ☐ |
| **48** | Confirm payment received | You | ☐ |

### The Offboarding Email

```
Subject: [Project Name] — Final Handoff Complete

Hi [Name],

[Project] is officially wrapped up! Here's everything you need:

📦 DELIVERABLES
• Source code: [GitHub/GitLab link]
• Documentation: [Notion/Google Drive link]
• API credentials: [Secure method]
• Deployment details: [Infrastructure info]

📚 KNOWLEDGE TRANSFER
• Training session recording: [Loom/Zoom link]
• Runbook / troubleshooting guide: [Link]
• Architecture diagram: [Link]

🔐 ACCESS
• I've revoked my access to [systems]
• Your team admin [Name] now has full control
• Backup credentials are in [secure location]

📋 NEXT STEPS
• Review all deliverables within 5 business days
• Confirm acceptance by replying to this email
• Final invoice attached — due within 7 days

🤝 STAYING IN TOUCH
• I'll check in at 30 days to see how things are running
• For urgent issues, email [your email] or call [phone]
• For maintenance, see the retainer options we discussed

It's been a pleasure working with you and the [Company] team. 
I'm proud of what we built together.

Best,
[Your name]

P.S. — If you know anyone who might benefit from similar work, 
I'd love an intro. And if you're open to a quick testimonial, 
just reply with a few sentences about your experience.
```

---

## 2. Asset Transfer Protocol

### The Asset Inventory

| Category | Items | Format | Location |
|----------|-------|--------|----------|
| **Source Code** | All repositories | GitHub/GitLab | Transfer ownership or add admin |
| **Models** | Trained models, weights | .pkl, .h5, ONNX | Cloud storage + local backup |
| **Data** | Processed datasets, features | CSV, Parquet | Secure cloud transfer |
| **Documentation** | README, API docs, runbooks | Markdown, PDF | Shared drive |
| **Credentials** | API keys, DB passwords | Encrypted | Password manager or secure email |
| **Infrastructure** | Dockerfiles, K8s configs, Terraform | YAML, JSON | Repository |
| **Monitoring** | Dashboard configs, alert rules | JSON, YAML | Export + instructions |

### The Transfer Checklist

- [ ] All code committed and pushed to client-owned repo
- [ ] Client added as admin/owner on all repositories
- [ ] Model artifacts uploaded to client cloud storage
- [ ] Documentation complete and reviewed
- [ ] Credentials transferred via secure method (1Password, Bitwarden)
- [ ] Deployment instructions tested on clean environment
- [ ] Monitoring dashboards exported and documented
- [ ] Backup/recovery procedures documented
- [ ] All third-party accounts transferred or recreated

### Security Protocol

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Transfer ownership of all repos | Day 0 |
| 2 | Remove yourself from client Slack/Teams | Day 1 |
| 3 | Revoke API keys you created | Day 1 |
| 4 | Remove your SSH keys from servers | Day 1 |
| 5 | Delete local copies of sensitive data | Day 2 |
| 6 | Confirm no lingering access | Day 3 |

---

## 3. Knowledge Transfer

### The Training Session (1 Hour)

| Time | Topic | Format |
|------|-------|--------|
| **0-10 min** | System overview | Slide deck |
| **10-25 min** | Architecture walkthrough | Live diagram |
| **25-40 min** | Common operations demo | Screen share |
| **40-50 min** | Troubleshooting scenarios | Q&A |
| **50-60 min** | Questions + next steps | Discussion |

### The Runbook Template

```markdown
# [System Name] — Operations Runbook

## Quick Reference
- **System URL:** [Link]
- **Repository:** [GitHub link]
- **Documentation:** [Link]
- **On-call contact:** [Name, email, phone]

## Daily Checks
- [ ] Check monitoring dashboard: [Link]
- [ ] Review overnight alerts (if any)
- [ ] Verify data pipeline ran successfully

## Weekly Checks
- [ ] Review model performance metrics
- [ ] Check for data drift
- [ ] Verify backup completion

## Common Issues

### Issue 1: [Symptom]
**Symptoms:** [What you see]
**Cause:** [Why it happens]
**Fix:** [Step-by-step]
**Prevention:** [How to avoid]

### Issue 2: [Symptom]
[Same structure]

## Emergency Procedures

### System Down
1. Check [monitoring link]
2. Restart [service] via [method]
3. If still down, contact [escalation contact]

### Data Pipeline Failure
1. Check [Airflow/Dagster link]
2. Review error logs: [location]
3. Re-run failed task
4. If persistent, check [dependency]

## Contact
- **Primary:** [Your name, email] (available for retainer clients)
- **Secondary:** [Alternative contact]
```

---

## 4. The Final Invoice

### Final Invoice Checklist

| Item | Specification |
|------|--------------|
| **Invoice number** | Sequential, professional |
| **Date** | Date of delivery |
| **Due date** | Net 7 (shorter than deposit) |
| **Description** | "[Project Name] — Final Payment (25%)" |
| **Amount** | Per SOW |
| **Payment methods** | Same as deposit |
| **Late fee notice** | 1.5% per month |
| **Thank you note** | Personalized, appreciative |

### The Payment Follow-Up

**Day 3 (Friendly):**
```
"Hi [Name], just checking in — wanted to make sure the final 
invoice arrived okay. Let me know if you have any questions!"
```

**Day 7 (Firm):**
```
"Hi [Name], following up on the final invoice (attached again). 
Payment was due [date]. Please let me know if there's an issue 
— happy to discuss."
```

**Day 14 (Formal):**
```
"Hi [Name], this is a formal reminder that invoice #[Number] 
for $[Amount] is 14 days past due. Per our SOW, a 1.5% monthly 
late fee applies. Please arrange payment by [date]."
```

---

## 5. Relationship Preservation

### The 30-Day Check-In

```
Subject: How's [System] running?

Hi [Name],

It's been 30 days since we handed off [project]. Quick check-in:

1. How is the system performing?
2. Any issues or questions come up?
3. Is the team finding it useful?
4. Anything you'd want to improve?

If anything needs attention, I'm here. And if you're open to 
a quick testimonial about your experience, I'd be grateful.

Hope all is well!

Best,
[Your name]
```

### The Quarterly Touch

```
"Hi [Name],

Saw [Company] [recent news/achievement] — congrats!

Also came across this [article/tool/resource] on [topic] and 
thought of you: [Link]

No agenda — just staying in touch. If you ever need [type of 
help], my door's open.

Best,
[Your name]"
```

### The "Door Always Open" Close

```
"Working with [Company] was a highlight of my year. Even though 
this project is complete, I hope we stay in touch.

If you ever need:
• Quick advice on [topic]
• An intro to someone in my network
• Help with a future project

Just reach out. No project too small.

Wishing you and the team continued success.

[Your name]"
```

---

## 6. AI Prompts

### Prompt 1: Offboarding Email Writer

```
Act as a client offboarding specialist.

Project details:
- Client: [COMPANY]
- Project: [NAME]
- Duration: [WEEKS]
- Deliverables: [LIST]
- Systems involved: [TECH STACK]

Write a comprehensive offboarding email that includes:
1. Deliverables summary with links
2. Knowledge transfer resources
3. Access revocation confirmation
4. Next steps for client
5. Maintenance retainer mention
6. Testimonial request
7. Referral request

Tone: Professional, warm, forward-looking.
```

### Prompt 2: Runbook Generator

```
Act as a technical writer for operations documentation.

System details:
- Name: [SYSTEM]
- Tech stack: [TOOLS]
- Deployment: [METHOD]
- Monitoring: [TOOLS]
- Common issues: [LIST]

Generate an operations runbook with:
1. Quick reference section
2. Daily/weekly checklists
3. 3 common issues with troubleshooting
4. Emergency procedures
5. Contact information
6. Architecture overview

Make it usable by a non-technical person.
```

### Prompt 3: Relationship Preservation Plan

```
Act as a client relationship manager.

Client details:
- Company: [COMPANY]
- Project: [WHAT YOU BUILT]
- Relationship quality: [EXCELLENT/GOOD/OKAY]
- Future potential: [HIGH/MEDIUM/LOW]

Create a 12-month relationship preservation plan:
1. 30-day check-in (email draft)
2. 90-day touch (topic + resource)
3. 6-month review (call or email)
4. Holiday message (template)
5. Quarterly value-add (articles, tools, intros)
6. Annual check-in (full relationship review)

Make each touch feel personal, not automated.
```

---

## 7. Action Checklist

### Day 0 (Delivery Day)

- [ ] Confirm final deliverable acceptance
- [ ] Send final invoice
- [ ] Transfer all assets
- [ ] Transfer credentials securely
- [ ] Send documentation package
- [ ] Schedule knowledge transfer call

### Day 1-2

- [ ] Conduct knowledge transfer session
- [ ] Revoke your access to all client systems
- [ ] Delete local copies of sensitive data
- [ ] Send offboarding email
- [ ] Update project status to "Complete"

### Day 3-7

- [ ] Follow up on invoice payment
- [ ] Confirm no lingering access
- [ ] Archive project files (your records)
- [ ] Update portfolio with project details

### Day 30

- [ ] Send 30-day check-in email
- [ ] Request testimonial
- [ ] Identify upsell opportunities
- [ ] Update case study with results

### Ongoing

- [ ] Quarterly relationship touch
- [ ] Annual check-in call
- [ ] Holiday/birthday messages
- [ ] Share relevant resources

---

> **Next Module:** [06-OPERATIONS →](../06-OPERATIONS/)
>
> *"A good goodbye is a good hello to the next opportunity."*

---

*Module 05D | Offboarding | Version 2026.05*
