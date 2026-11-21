//! AGYOS 104-Role Matrix and Pod Alignment.
//!
//! Complies with Principle P04 (Behavioral Contracts), P09 (Explicit State),
//! and Baseline Invariant:
//! 104 Operational Roles, 12 Departments, 5 Seniority Tiers (L4-L8),
//! 5 Governing Pods (Build: 43, Growth: 21, Customer: 8, People: 5, GNA: 27).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Department {
    Executive,
    Product,
    Engineering,
    DataAi,
    Design,
    Marketing,
    SalesBd,
    CustomerSuccess,
    Finance,
    LegalCompliance,
    PeopleOps,
    ItInfra,
}

impl Department {
    pub fn as_str(&self) -> &'static str {
        match self {
            Department::Executive => "executive",
            Department::Product => "product",
            Department::Engineering => "engineering",
            Department::DataAi => "data_ai",
            Department::Design => "design",
            Department::Marketing => "marketing",
            Department::SalesBd => "sales_bd",
            Department::CustomerSuccess => "customer_success",
            Department::Finance => "finance",
            Department::LegalCompliance => "legal_compliance",
            Department::PeopleOps => "people_ops",
            Department::ItInfra => "it_infra",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum GoverningPod {
    PodBuild,
    PodGrowth,
    PodCustomer,
    PodPeople,
    PodGna,
}

impl GoverningPod {
    pub fn as_str(&self) -> &'static str {
        match self {
            GoverningPod::PodBuild => "pod-build",
            GoverningPod::PodGrowth => "pod-growth",
            GoverningPod::PodCustomer => "pod-customer",
            GoverningPod::PodPeople => "pod-people",
            GoverningPod::PodGna => "pod-gna",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum SeniorityTier {
    L4,
    L5,
    L6,
    L7,
    L8,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RoleDefinition {
    pub role_id: String,
    pub title: String,
    pub department: Department,
    pub seniority: SeniorityTier,
    pub governing_pod: GoverningPod,
    pub primary_skills: Vec<String>,
    pub secondary_skills: Vec<String>,
}

pub struct RoleRegistry;

impl RoleRegistry {
    /// Return the canonical 104 operational roles matching baseline roles.py.
    pub fn load_roles() -> Vec<RoleDefinition> {
        let mut roles = Vec::with_capacity(104);

        // Helper macro to insert roles cleanly
        macro_rules! add_role {
            ($id:expr, $title:expr, $dept:expr, $sen:expr, $pod:expr) => {
                roles.push(RoleDefinition {
                    role_id: $id.to_string(),
                    title: $title.to_string(),
                    department: $dept,
                    seniority: $sen,
                    governing_pod: $pod,
                    primary_skills: Vec::new(),
                    secondary_skills: Vec::new(),
                });
            };
        }

        // --- POD-BUILD (43 roles) ---
        add_role!("role-agentic-workflow-architect", "Agentic Workflow Architect", Department::Engineering, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-ai-product-engineer", "AI Product Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-backend-engineer", "Backend Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-cloud-architect", "Cloud Architect", Department::ItInfra, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-computer-vision-eng", "Computer Vision Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-cpo", "Chief Product Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodBuild);
        add_role!("role-cto", "Chief Technology Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodBuild);
        add_role!("role-data-analyst", "Data Analyst", Department::DataAi, SeniorityTier::L4, GoverningPod::PodBuild);
        add_role!("role-data-engineer", "Data Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-data-scientist", "Data Scientist", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-database-reliability-eng", "Database Reliability Engineer", Department::Engineering, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-design-director", "Design Director", Department::Design, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-design-system-engineer", "Design System Engineer", Department::Design, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-desktop-app-eng", "Desktop Application Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-devops-engineer", "DevOps / Platform Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-frontend-engineer", "Frontend Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-incident-commander", "Incident Commander", Department::Engineering, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-it-systems-admin", "IT Systems Administrator", Department::ItInfra, SeniorityTier::L4, GoverningPod::PodBuild);
        add_role!("role-ml-engineer", "ML Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-mlops-engineer", "MLOps Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-mobile-engineer", "Mobile Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-network-infra-eng", "Network Infrastructure Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-observability-engineer", "Observability Engineer", Department::ItInfra, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-platform-engineer", "Platform Engineer", Department::ItInfra, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-pm", "Product Manager", Department::Product, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-product-analyst", "Product Analyst", Department::Product, SeniorityTier::L4, GoverningPod::PodBuild);
        add_role!("role-product-designer", "Product Designer", Department::Design, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-product-director", "Product Director", Department::Product, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-qa-engineer", "QA / Test Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-research-scientist", "Research Scientist", Department::DataAi, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-scrum-agile-coach", "Scrum / Agile Coach", Department::Product, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-senior-pm", "Senior Product Manager", Department::Product, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-senior-swe", "Senior Software Engineer", Department::Engineering, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-site-reliability-engineer", "Site Reliability Engineer", Department::Engineering, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-speech-audio-ai-eng", "Speech & Audio AI Engineer", Department::DataAi, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-staff-engineer", "Staff Software Engineer", Department::Engineering, SeniorityTier::L7, GoverningPod::PodBuild);
        add_role!("role-swe", "Software Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-technical-pm", "Technical Product Manager", Department::Product, SeniorityTier::L6, GoverningPod::PodBuild);
        add_role!("role-ux-copywriter", "UX Copywriter", Department::Design, SeniorityTier::L4, GoverningPod::PodBuild);
        add_role!("role-ux-researcher", "UX Researcher", Department::Product, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-ux-ui-designer", "UX / UI Designer", Department::Design, SeniorityTier::L5, GoverningPod::PodBuild);
        add_role!("role-vp-engineering", "VP Engineering", Department::Executive, SeniorityTier::L8, GoverningPod::PodBuild);
        add_role!("role-web3-blockchain-eng", "Web3 / Blockchain Engineer", Department::Engineering, SeniorityTier::L5, GoverningPod::PodBuild);
        // --- POD-GROWTH (21 roles) ---
        add_role!("role-3d-visual-designer", "3D Visual Designer", Department::Design, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-account-executive", "Account Executive", Department::SalesBd, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-brand-copywriter", "Brand Copywriter", Department::Marketing, SeniorityTier::L4, GoverningPod::PodGrowth);
        add_role!("role-brand-designer", "Brand Designer", Department::Design, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-cmo", "Chief Marketing Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodGrowth);
        add_role!("role-content-strategist", "Content Strategist", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-conversion-optimizer", "Conversion Rate Optimizer", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-email-lifecycle-marketer", "Email & Lifecycle Marketer", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-enterprise-ae", "Enterprise Account Executive", Department::SalesBd, SeniorityTier::L6, GoverningPod::PodGrowth);
        add_role!("role-freelancer-sales", "Freelancer Business Development", Department::SalesBd, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-growth-pm", "Growth Product Manager", Department::Product, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-motion-designer", "Motion Designer", Department::Design, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-partnership-bd-manager", "Partnership & BD Manager", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-performance-marketer", "Performance Marketer", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-pr-comms-manager", "PR & Communications Manager", Department::Marketing, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-revenue-operations", "Revenue Operations Analyst", Department::SalesBd, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-sales-development-rep", "Sales Development Representative", Department::SalesBd, SeniorityTier::L4, GoverningPod::PodGrowth);
        add_role!("role-seo-specialist", "SEO Specialist", Department::Marketing, SeniorityTier::L4, GoverningPod::PodGrowth);
        add_role!("role-social-media-manager", "Social Media Manager", Department::Marketing, SeniorityTier::L4, GoverningPod::PodGrowth);
        add_role!("role-solutions-engineer", "Solutions Engineer", Department::SalesBd, SeniorityTier::L5, GoverningPod::PodGrowth);
        add_role!("role-vp-sales", "VP Sales", Department::SalesBd, SeniorityTier::L8, GoverningPod::PodGrowth);
        // --- POD-CUSTOMER (8 roles) ---
        add_role!("role-churn-analyst", "Churn & Retention Analyst", Department::CustomerSuccess, SeniorityTier::L4, GoverningPod::PodCustomer);
        add_role!("role-community-manager", "Community Manager", Department::Marketing, SeniorityTier::L4, GoverningPod::PodCustomer);
        add_role!("role-customer-success-manager", "Customer Success Manager", Department::SalesBd, SeniorityTier::L5, GoverningPod::PodCustomer);
        add_role!("role-docs-technical-writer", "Technical Writer", Department::CustomerSuccess, SeniorityTier::L4, GoverningPod::PodCustomer);
        add_role!("role-implementation-consultant", "Implementation Consultant", Department::CustomerSuccess, SeniorityTier::L5, GoverningPod::PodCustomer);
        add_role!("role-onboarding-specialist", "Onboarding Specialist", Department::CustomerSuccess, SeniorityTier::L4, GoverningPod::PodCustomer);
        add_role!("role-support-engineer", "Support Engineer", Department::CustomerSuccess, SeniorityTier::L4, GoverningPod::PodCustomer);
        add_role!("role-technical-account-manager", "Technical Account Manager", Department::CustomerSuccess, SeniorityTier::L6, GoverningPod::PodCustomer);
        // --- POD-PEOPLE (5 roles) ---
        add_role!("role-hr-business-partner", "HR Business Partner", Department::PeopleOps, SeniorityTier::L5, GoverningPod::PodPeople);
        add_role!("role-hr-ops-specialist", "HR Operations Specialist", Department::PeopleOps, SeniorityTier::L4, GoverningPod::PodPeople);
        add_role!("role-learning-development", "L&D Specialist", Department::PeopleOps, SeniorityTier::L4, GoverningPod::PodPeople);
        add_role!("role-recruiter", "Talent Recruiter", Department::PeopleOps, SeniorityTier::L4, GoverningPod::PodPeople);
        add_role!("role-vp-people", "VP People", Department::PeopleOps, SeniorityTier::L8, GoverningPod::PodPeople);
        // --- POD-GNA (27 roles) ---
        add_role!("role-accounts-manager", "Accounts Manager", Department::Finance, SeniorityTier::L4, GoverningPod::PodGna);
        add_role!("role-billing-payments-eng", "Billing & Payments Engineer", Department::Finance, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-ceo", "Chief Executive Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodGna);
        add_role!("role-cfo", "Chief Financial Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodGna);
        add_role!("role-chief-of-staff", "Chief of Staff", Department::PeopleOps, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-compliance-officer", "Compliance Officer", Department::LegalCompliance, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-contract-manager", "Contract Manager", Department::LegalCompliance, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-coo", "Chief Operating Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodGna);
        add_role!("role-corporate-controller", "Corporate Controller", Department::Finance, SeniorityTier::L7, GoverningPod::PodGna);
        add_role!("role-cost-optimization-analyst", "Cost Optimization Analyst", Department::Finance, SeniorityTier::L4, GoverningPod::PodGna);
        add_role!("role-cso", "Chief Security Officer", Department::Executive, SeniorityTier::L8, GoverningPod::PodGna);
        add_role!("role-cybersecurity-analyst", "Cybersecurity Analyst", Department::ItInfra, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-data-protection-officer", "Data Protection Officer", Department::LegalCompliance, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-executive-assistant", "Executive Assistant", Department::PeopleOps, SeniorityTier::L4, GoverningPod::PodGna);
        add_role!("role-finops-cloud-cost", "FinOps / Cloud Cost Engineer", Department::ItInfra, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-fp-and-a-analyst", "FP&A Analyst", Department::Finance, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-general-counsel", "General Counsel", Department::LegalCompliance, SeniorityTier::L8, GoverningPod::PodGna);
        add_role!("role-ip-patent-attorney", "IP & Patent Attorney", Department::LegalCompliance, SeniorityTier::L7, GoverningPod::PodGna);
        add_role!("role-office-facilities-manager", "Office & Facilities Manager", Department::PeopleOps, SeniorityTier::L4, GoverningPod::PodGna);
        add_role!("role-privacy-engineer", "Privacy Engineer", Department::DataAi, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-procurement-vendor-manager", "Procurement & Vendor Manager", Department::PeopleOps, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-risk-manager", "Risk Manager", Department::LegalCompliance, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-security-engineer", "Security Engineer", Department::Engineering, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-solopreneur-operator", "Solopreneur Operator", Department::PeopleOps, SeniorityTier::L6, GoverningPod::PodGna);
        add_role!("role-startup-cfo-advisor", "Startup CFO Advisor", Department::Finance, SeniorityTier::L7, GoverningPod::PodGna);
        add_role!("role-tax-compliance-spec", "Tax & Compliance Specialist", Department::Finance, SeniorityTier::L5, GoverningPod::PodGna);
        add_role!("role-treasury-banking-spec", "Treasury & Banking Specialist", Department::Finance, SeniorityTier::L5, GoverningPod::PodGna);

        roles
    }
}
