# AGYOS Role-Wise Skills Directory (`skills-by-role/`)

> Canonical enterprise mapping of all 2,247 skills across 104 FAANG/MANGO corporate roles.
> Maintained By Krish Ujeniya (@krishujeniya).

## Subsystem Architecture

In AGYOS, physical skill runbooks are canonically authored in `.agents/skills/<skill-name>/SKILL.md`.
This directory (`.agents/skills-by-role/` and its root symlink `skills-by-role/`) organizes skills
into dedicated per-role workspaces via relative symlinks.

## Department Matrix & Skill Allocations

| Department | Role ID | Role Title | Seniority | Mapped Skills | Primary Skills |
|------------|---------|------------|-----------|---------------|----------------|
| customer_success | [`role-churn-analyst`](role-churn-analyst/) | Churn & Retention Analyst | L4 | 7 | 5 |
| customer_success | [`role-docs-technical-writer`](role-docs-technical-writer/) | Technical Writer | L4 | 44 | 5 |
| customer_success | [`role-onboarding-specialist`](role-onboarding-specialist/) | Onboarding Specialist | L4 | 34 | 5 |
| customer_success | [`role-support-engineer`](role-support-engineer/) | Support Engineer | L4 | 37 | 5 |
| customer_success | [`role-implementation-consultant`](role-implementation-consultant/) | Implementation Consultant | L5 | 57 | 5 |
| customer_success | [`role-technical-account-manager`](role-technical-account-manager/) | Technical Account Manager | L6 | 25 | 5 |
| data_ai | [`role-data-analyst`](role-data-analyst/) | Data Analyst | L4 | 53 | 5 |
| data_ai | [`role-ai-product-engineer`](role-ai-product-engineer/) | AI Product Engineer | L5 | 157 | 5 |
| data_ai | [`role-computer-vision-eng`](role-computer-vision-eng/) | Computer Vision Engineer | L5 | 14 | 5 |
| data_ai | [`role-data-engineer`](role-data-engineer/) | Data Engineer | L5 | 55 | 5 |
| data_ai | [`role-data-scientist`](role-data-scientist/) | Data Scientist | L5 | 40 | 5 |
| data_ai | [`role-ml-engineer`](role-ml-engineer/) | ML Engineer | L5 | 61 | 5 |
| data_ai | [`role-mlops-engineer`](role-mlops-engineer/) | MLOps Engineer | L5 | 24 | 5 |
| data_ai | [`role-speech-audio-ai-eng`](role-speech-audio-ai-eng/) | Speech & Audio AI Engineer | L5 | 35 | 6 |
| data_ai | [`role-privacy-engineer`](role-privacy-engineer/) | Privacy Engineer | L6 | 8 | 5 |
| data_ai | [`role-research-scientist`](role-research-scientist/) | Research Scientist | L7 | 34 | 5 |
| design | [`role-ux-copywriter`](role-ux-copywriter/) | UX Copywriter | L4 | 7 | 5 |
| design | [`role-3d-visual-designer`](role-3d-visual-designer/) | 3D Visual Designer | L5 | 26 | 5 |
| design | [`role-brand-designer`](role-brand-designer/) | Brand Designer | L5 | 51 | 5 |
| design | [`role-design-system-engineer`](role-design-system-engineer/) | Design System Engineer | L5 | 62 | 5 |
| design | [`role-motion-designer`](role-motion-designer/) | Motion Designer | L5 | 68 | 5 |
| design | [`role-product-designer`](role-product-designer/) | Product Designer | L5 | 45 | 5 |
| design | [`role-ux-ui-designer`](role-ux-ui-designer/) | UX / UI Designer | L5 | 95 | 5 |
| design | [`role-design-director`](role-design-director/) | Design Director | L7 | 45 | 5 |
| engineering | [`role-backend-engineer`](role-backend-engineer/) | Backend Engineer | L5 | 218 | 6 |
| engineering | [`role-desktop-app-eng`](role-desktop-app-eng/) | Desktop Application Engineer | L5 | 57 | 4 |
| engineering | [`role-devops-engineer`](role-devops-engineer/) | DevOps / Platform Engineer | L5 | 82 | 5 |
| engineering | [`role-frontend-engineer`](role-frontend-engineer/) | Frontend Engineer | L5 | 214 | 6 |
| engineering | [`role-mobile-engineer`](role-mobile-engineer/) | Mobile Engineer | L5 | 97 | 5 |
| engineering | [`role-network-infra-eng`](role-network-infra-eng/) | Network Infrastructure Engineer | L5 | 26 | 5 |
| engineering | [`role-qa-engineer`](role-qa-engineer/) | QA / Test Engineer | L5 | 53 | 5 |
| engineering | [`role-swe`](role-swe/) | Software Engineer | L5 | 134 | 5 |
| engineering | [`role-web3-blockchain-eng`](role-web3-blockchain-eng/) | Web3 / Blockchain Engineer | L5 | 21 | 5 |
| engineering | [`role-database-reliability-eng`](role-database-reliability-eng/) | Database Reliability Engineer | L6 | 39 | 5 |
| engineering | [`role-incident-commander`](role-incident-commander/) | Incident Commander | L6 | 14 | 5 |
| engineering | [`role-security-engineer`](role-security-engineer/) | Security Engineer | L6 | 85 | 5 |
| engineering | [`role-senior-swe`](role-senior-swe/) | Senior Software Engineer | L6 | 174 | 6 |
| engineering | [`role-site-reliability-engineer`](role-site-reliability-engineer/) | Site Reliability Engineer | L6 | 43 | 5 |
| engineering | [`role-agentic-workflow-architect`](role-agentic-workflow-architect/) | Agentic Workflow Architect | L7 | 269 | 5 |
| engineering | [`role-staff-engineer`](role-staff-engineer/) | Staff Software Engineer | L7 | 77 | 5 |
| executive | [`role-ceo`](role-ceo/) | Chief Executive Officer | L8 | 37 | 5 |
| executive | [`role-cfo`](role-cfo/) | Chief Financial Officer | L8 | 7 | 4 |
| executive | [`role-cmo`](role-cmo/) | Chief Marketing Officer | L8 | 26 | 5 |
| executive | [`role-coo`](role-coo/) | Chief Operating Officer | L8 | 40 | 5 |
| executive | [`role-cpo`](role-cpo/) | Chief Product Officer | L8 | 31 | 5 |
| executive | [`role-cso`](role-cso/) | Chief Security Officer | L8 | 42 | 5 |
| executive | [`role-cto`](role-cto/) | Chief Technology Officer | L8 | 40 | 5 |
| executive | [`role-vp-engineering`](role-vp-engineering/) | VP Engineering | L8 | 30 | 5 |
| finance | [`role-accounts-manager`](role-accounts-manager/) | Accounts Manager | L4 | 7 | 4 |
| finance | [`role-cost-optimization-analyst`](role-cost-optimization-analyst/) | Cost Optimization Analyst | L4 | 28 | 5 |
| finance | [`role-billing-payments-eng`](role-billing-payments-eng/) | Billing & Payments Engineer | L5 | 15 | 5 |
| finance | [`role-fp-and-a-analyst`](role-fp-and-a-analyst/) | FP&A Analyst | L5 | 84 | 4 |
| finance | [`role-tax-compliance-spec`](role-tax-compliance-spec/) | Tax & Compliance Specialist | L5 | 12 | 4 |
| finance | [`role-treasury-banking-spec`](role-treasury-banking-spec/) | Treasury & Banking Specialist | L5 | 4 | 4 |
| finance | [`role-corporate-controller`](role-corporate-controller/) | Corporate Controller | L7 | 13 | 4 |
| finance | [`role-startup-cfo-advisor`](role-startup-cfo-advisor/) | Startup CFO Advisor | L7 | 47 | 4 |
| it_infra | [`role-it-systems-admin`](role-it-systems-admin/) | IT Systems Administrator | L4 | 30 | 5 |
| it_infra | [`role-cybersecurity-analyst`](role-cybersecurity-analyst/) | Cybersecurity Analyst | L5 | 28 | 5 |
| it_infra | [`role-finops-cloud-cost`](role-finops-cloud-cost/) | FinOps / Cloud Cost Engineer | L5 | 20 | 5 |
| it_infra | [`role-observability-engineer`](role-observability-engineer/) | Observability Engineer | L5 | 31 | 5 |
| it_infra | [`role-platform-engineer`](role-platform-engineer/) | Platform Engineer | L5 | 20 | 5 |
| it_infra | [`role-cloud-architect`](role-cloud-architect/) | Cloud Architect | L7 | 83 | 5 |
| legal_compliance | [`role-contract-manager`](role-contract-manager/) | Contract Manager | L5 | 8 | 4 |
| legal_compliance | [`role-compliance-officer`](role-compliance-officer/) | Compliance Officer | L6 | 28 | 5 |
| legal_compliance | [`role-data-protection-officer`](role-data-protection-officer/) | Data Protection Officer | L6 | 29 | 5 |
| legal_compliance | [`role-risk-manager`](role-risk-manager/) | Risk Manager | L6 | 16 | 4 |
| legal_compliance | [`role-ip-patent-attorney`](role-ip-patent-attorney/) | IP & Patent Attorney | L7 | 7 | 4 |
| legal_compliance | [`role-general-counsel`](role-general-counsel/) | General Counsel | L8 | 9 | 4 |
| marketing | [`role-brand-copywriter`](role-brand-copywriter/) | Brand Copywriter | L4 | 23 | 5 |
| marketing | [`role-community-manager`](role-community-manager/) | Community Manager | L4 | 9 | 5 |
| marketing | [`role-seo-specialist`](role-seo-specialist/) | SEO Specialist | L4 | 60 | 5 |
| marketing | [`role-social-media-manager`](role-social-media-manager/) | Social Media Manager | L4 | 118 | 5 |
| marketing | [`role-content-strategist`](role-content-strategist/) | Content Strategist | L5 | 190 | 5 |
| marketing | [`role-conversion-optimizer`](role-conversion-optimizer/) | Conversion Rate Optimizer | L5 | 19 | 5 |
| marketing | [`role-email-lifecycle-marketer`](role-email-lifecycle-marketer/) | Email & Lifecycle Marketer | L5 | 49 | 5 |
| marketing | [`role-partnership-bd-manager`](role-partnership-bd-manager/) | Partnership & BD Manager | L5 | 6 | 4 |
| marketing | [`role-performance-marketer`](role-performance-marketer/) | Performance Marketer | L5 | 18 | 5 |
| marketing | [`role-pr-comms-manager`](role-pr-comms-manager/) | PR & Communications Manager | L5 | 20 | 5 |
| people_ops | [`role-executive-assistant`](role-executive-assistant/) | Executive Assistant | L4 | 13 | 5 |
| people_ops | [`role-hr-ops-specialist`](role-hr-ops-specialist/) | HR Operations Specialist | L4 | 6 | 4 |
| people_ops | [`role-learning-development`](role-learning-development/) | L&D Specialist | L4 | 30 | 5 |
| people_ops | [`role-office-facilities-manager`](role-office-facilities-manager/) | Office & Facilities Manager | L4 | 13 | 4 |
| people_ops | [`role-recruiter`](role-recruiter/) | Talent Recruiter | L4 | 21 | 5 |
| people_ops | [`role-hr-business-partner`](role-hr-business-partner/) | HR Business Partner | L5 | 24 | 5 |
| people_ops | [`role-procurement-vendor-manager`](role-procurement-vendor-manager/) | Procurement & Vendor Manager | L5 | 6 | 4 |
| people_ops | [`role-chief-of-staff`](role-chief-of-staff/) | Chief of Staff | L6 | 26 | 5 |
| people_ops | [`role-solopreneur-operator`](role-solopreneur-operator/) | Solopreneur Operator | L6 | 68 | 5 |
| people_ops | [`role-vp-people`](role-vp-people/) | VP People | L8 | 22 | 5 |
| product | [`role-product-analyst`](role-product-analyst/) | Product Analyst | L4 | 24 | 5 |
| product | [`role-growth-pm`](role-growth-pm/) | Growth Product Manager | L5 | 20 | 5 |
| product | [`role-pm`](role-pm/) | Product Manager | L5 | 11 | 4 |
| product | [`role-scrum-agile-coach`](role-scrum-agile-coach/) | Scrum / Agile Coach | L5 | 5 | 4 |
| product | [`role-ux-researcher`](role-ux-researcher/) | UX Researcher | L5 | 26 | 4 |
| product | [`role-senior-pm`](role-senior-pm/) | Senior Product Manager | L6 | 27 | 5 |
| product | [`role-technical-pm`](role-technical-pm/) | Technical Product Manager | L6 | 33 | 5 |
| product | [`role-product-director`](role-product-director/) | Product Director | L7 | 26 | 4 |
| sales_bd | [`role-sales-development-rep`](role-sales-development-rep/) | Sales Development Representative | L4 | 24 | 5 |
| sales_bd | [`role-account-executive`](role-account-executive/) | Account Executive | L5 | 47 | 5 |
| sales_bd | [`role-customer-success-manager`](role-customer-success-manager/) | Customer Success Manager | L5 | 12 | 5 |
| sales_bd | [`role-freelancer-sales`](role-freelancer-sales/) | Freelancer Business Development | L5 | 25 | 5 |
| sales_bd | [`role-revenue-operations`](role-revenue-operations/) | Revenue Operations Analyst | L5 | 16 | 5 |
| sales_bd | [`role-solutions-engineer`](role-solutions-engineer/) | Solutions Engineer | L5 | 24 | 5 |
| sales_bd | [`role-enterprise-ae`](role-enterprise-ae/) | Enterprise Account Executive | L6 | 38 | 5 |
| sales_bd | [`role-vp-sales`](role-vp-sales/) | VP Sales | L8 | 32 | 5 |

## CLI Inspection

Inspect role skills directly via the `agyos` kernel CLI:
```bash
# List all roles with skill counts
bin/agyos roles --skills

# Inspect a specific role's full skill roster
bin/agyos role role-frontend-engineer --skills
```
