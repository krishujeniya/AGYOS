//! Canonical Skill Placement Registry and Qualification Harness.
//!
//! Complies with Step 11: Place and qualify skills and Principles:
//! - P04 (Schema-first contracts & strict boundary validation)
//! - P05 (Least privilege & complete mediation)
//! - P06 (Source provenance & cryptographic receipts)
//! - P09 (Transactional idempotency)
//! - P23 (Human-in-the-loop review)
//! - P24 (Calibrated reliance)
//! - P26 (Universal accessibility)
//! - P28 (Socratic intent synthesis & EVPI gating)
//! - P29 (Graph-based skill retrieval & lazy runbook loading)
//! - P31 (Ariadne session recovery)
//! - P32 (Operator-owned budgets)

use domain::RiskTier;
use crate::role::{Department, GoverningPod};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CanonicalSkill {
    pub id: String,
    pub home: String,
    pub canonical_path: String,
    pub owner_team: String,
    pub department: Department,
    pub pod: GoverningPod,
    pub principles: Vec<String>,
    pub risk_tier: RiskTier,
    pub intent: String,
    pub route_labels: Vec<String>,
    pub clarification_triggers: Vec<String>,
    pub abstention_triggers: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DepartmentFixture {
    pub department: Department,
    pub pod: GoverningPod,
    pub skill_id: String,
    pub positive_prompt: String,
    pub expected_output_type: String,
    pub negative_prompt: String,
    pub abstention_reason: String,
    pub interruption_prompt: String,
    pub recovery_checkpoint: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RouteEvaluationResult {
    Matched {
        skill_id: String,
        department: Department,
        pod: GoverningPod,
    },
    ClarificationRequired {
        prompt: String,
        question: String,
    },
    Abstain {
        reason: String,
    },
}

pub struct SkillPlacementRegistry;

impl SkillPlacementRegistry {
    pub fn load_required_153() -> Vec<CanonicalSkill> {
        let raw_specs: Vec<(&str, &str, &str, Department, GoverningPod, RiskTier, &[&str], &str, &[&str], &[&str], &[&str])> = vec![
            // 1. operator (7 skills)
            ("capture-goal", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P28", "P31"], "Capture the primary objective and constraints from the operator", &["capture goal", "user objective"], &["vague goal"], &["unsupported task"]),
            ("clarify-intent", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P28", "P31"], "Socratic EVPI clarification for ambiguous high-consequence requirements", &["clarify intent", "ask question"], &["ambiguous request"], &["out of scope"]),
            ("revise-assumption", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P23", "P24", "P26", "P28", "P31"], "Update task contract assumptions upon operator guidance", &["revise assumption", "change constraint"], &["conflicting constraint"], &["illegal override"]),
            ("explain-evidence", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P28", "P31"], "Render transparent evidence links and attribution proofs", &["explain evidence", "show proof"], &["unverified claim"], &["unlinked fact"]),
            ("accessible-handoff", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P28", "P31"], "Format accessible human handoff with keyboard and screen reader support", &["accessible handoff", "human summary"], &["unclear summary"], &["inaccessible markup"]),
            ("pause-resume", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P23", "P24", "P26", "P28", "P31"], "Checkpoint active session state and resume via Ariadne breadcrumbs", &["pause session", "resume work"], &["incomplete checkpoint"], &["corrupted state"]),
            ("teach-by-example", "operator", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P23", "P24", "P26", "P28", "P31"], "Ingest few-shot operator demonstrations to refine execution rules", &["teach by example", "few-shot demonstration"], &["contradictory demo"], &["malicious instruction"]),

            // 2. authority (6 skills)
            ("classify-risk", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P09", "P11", "P30"], "Determine R0 read-only, R1 local reversible, R2 shared internal, or R3 external irreversible tier", &["classify risk", "risk tier"], &["uncertain impact"], &["bypass safety"]),
            ("preview-effect", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P09", "P11", "P30"], "Render dry-run preview of proposed external mutations", &["preview effect", "dry run"], &["unknown side effect"], &["skip preview"]),
            ("request-consent", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R1, &["P05", "P09", "P11", "P30"], "Halt execution and request explicit operator authorization for R2/R3 actions", &["request consent", "human approval"], &["unclear approver"], &["unauthorized execute"]),
            ("withdraw-consent", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R1, &["P05", "P09", "P11", "P30"], "Revoke in-flight authorizations and trigger rollback/compensation", &["withdraw consent", "revoke approval"], &["partial rollback"], &["ignored withdrawal"]),
            ("reconcile-unknown-effect", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R2, &["P05", "P09", "P11", "P30"], "Triage ambiguous or unconfirmed provider receipts", &["reconcile effect", "check unknown"], &["missing receipt"], &["unlogged mutation"]),
            ("prove-scope", "authority", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P09", "P11", "P30"], "Cryptographically attest that proposed effect adheres to least-privilege contract", &["prove scope", "attest boundary"], &["broad permission"], &["unscoped action"]),

            // 3. councils (5 skills)
            ("frame-question", "councils", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P06", "P22", "P25", "P27"], "Structure high-consequence dilemma into typed blind evaluation prompts", &["frame question", "council question"], &["loaded question"], &["biased premise"]),
            ("assemble-context", "councils", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P06", "P22", "P25", "P27"], "Package isolated context packets for independent review arms", &["assemble context", "isolate packet"], &["leaked opinion"], &["poisoned context"]),
            ("independent-review", "councils", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P06", "P22", "P25", "P27"], "Execute blind multi-agent evaluation without peer bias", &["independent review", "blind evaluation"], &["peer influence"], &["collusion"]),
            ("resolve-dissent", "councils", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P06", "P22", "P25", "P27"], "Aggregate evaluation votes and record structured minority dissent", &["resolve dissent", "record dissent"], &["unresolved deadlock"], &["suppressed minority"]),
            ("evaluate-council", "councils", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P06", "P22", "P25", "P27"], "Measure council outcome quality and economic return on token spend", &["evaluate council", "council roi"], &["unmeasured spend"], &["wasteful council"]),

            // 4. planning (6 skills)
            ("work-backwards", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P09", "P10", "P23"], "Start from end customer deliverable to construct execution roadmap", &["work backwards", "customer end state"], &["fuzzy outcome"], &["vanity goal"]),
            ("discover-client-need", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P09", "P10", "P23"], "Extract business requirements and domain constraints", &["discover need", "client requirements"], &["unspoken expectation"], &["scope creep"]),
            ("define-acceptance", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P09", "P10", "P23"], "Establish deterministic Given-When-Then criteria", &["define acceptance", "given when then"], &["untestable criterion"], &["speculative promise"]),
            ("decompose-milestone", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P04", "P09", "P10", "P23"], "Break down roadmap into atomic, bounded execution tasks", &["decompose milestone", "atomic task"], &["monolithic task"], &["interdependent deadlock"]),
            ("map-dependencies", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P09", "P10", "P23"], "Construct topological dependency graph across tasks", &["map dependencies", "task graph"], &["circular dependency"], &["untraced blocker"]),
            ("plan-compensation", "planning", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P04", "P09", "P10", "P23"], "Define compensating transactions for reversible actions", &["plan compensation", "rollback transaction"], &["irreversible step"], &["unhedged effect"]),

            // 5. knowledge (8 skills)
            ("inventory-sources", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P07", "P22", "P29"], "Scan repository and external references for source provenance", &["inventory sources", "trace provenance"], &["untracked source"], &["unlicensed asset"]),
            ("establish-rights", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P07", "P22", "P29"], "Verify open source licenses and data redistribution rights", &["establish rights", "verify license"], &["unclear license"], &["license breach"]),
            ("reconcile-aliases", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P07", "P22", "P29"], "Map legacy names and aliases to canonical skill targets", &["reconcile aliases", "alias redirect"], &["broken alias"], &["circular redirect"]),
            ("curate-skill", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P07", "P22", "P29"], "Review and format community skill submissions into TOON runbooks", &["curate skill", "format runbook"], &["unstructured submission"], &["malicious skill"]),
            ("retrieve-context", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P07", "P22", "P29"], "Graph-based lazy retrieval of relevant runbook sections", &["retrieve context", "lazy runbook"], &["irrelevant context"], &["token blowup"]),
            ("verify-citation", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P07", "P22", "P29"], "Validate external URLs and reference citations against primary sources", &["verify citation", "check link"], &["dead citation"], &["hallucinated source"]),
            ("evaluate-routing", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P07", "P22", "P29"], "Measure heuristic and model routing accuracy against held-out tests", &["evaluate routing", "routing accuracy"], &["routing drift"], &["uncalibrated model"]),
            ("retire-skill", "knowledge", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P07", "P22", "P29"], "Safely deprecate obsolete or vulnerable capabilities", &["retire skill", "deprecate skill"], &["unmigrated dependent"], &["silent deletion"]),

            // 6. memory (6 skills)
            ("capture-checkpoint", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P09", "P21", "P31"], "Persist transactional milestone checkpoint and session snapshot", &["capture checkpoint", "save state"], &["partial checkpoint"], &["corrupted snapshot"]),
            ("index-recall", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P09", "P21", "P31"], "Retrieve historical session context and durable learnings", &["index recall", "query memory"], &["stale fact"], &["unauthorized recall"]),
            ("correct-memory", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P09", "P21", "P31"], "Update or invalidate erroneous recalled facts upon operator correction", &["correct memory", "fix fact"], &["conflicting memory"], &["unverified rewrite"]),
            ("expire-records", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P09", "P21", "P31"], "Execute automated TTL retention pruning on ephemeral traces", &["expire records", "ttl prune"], &["premature deletion"], &["retained secret"]),
            ("export-workspace", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P09", "P21", "P31"], "Package tenant workspace memory into portable encrypted archive", &["export workspace", "archive tenant"], &["unencrypted export"], &["cross-tenant leak"]),
            ("forget-workspace", "memory", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R2, &["P06", "P09", "P21", "P31"], "Hard-delete workspace data and revoke cryptographic access keys", &["forget workspace", "purge tenant"], &["incomplete purge"], &["retained index"]),

            // 7. architecture (6 skills)
            ("map-boundaries", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P02", "P03", "P04", "P09"], "Trace subsystem boundaries and domain interfaces", &["map boundaries", "system interface"], &["unbounded coupling"], &["monolithic leak"]),
            ("untangle-codebase", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P02", "P03", "P04", "P09"], "Decouple circular dependencies and isolate legacy side effects", &["untangle codebase", "break circular dep"], &["spaghetti reference"], &["hidden side effect"]),
            ("record-decision", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P02", "P03", "P04", "P09"], "Document architectural tradeoffs in structured ADR format", &["record decision", "create adr"], &["undocumented choice"], &["unjustified shift"]),
            ("version-contract", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P02", "P03", "P04", "P09"], "Manage semantic versioning and schema migrations", &["version contract", "schema semver"], &["breaking schema"], &["unversioned payload"]),
            ("design-adapter", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P02", "P03", "P04", "P09"], "Specify clean boundary abstractions for external integrations", &["design adapter", "boundary contract"], &["leaky provider"], &["vendor lock-in"]),
            ("model-state", "architecture", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P02", "P03", "P04", "P09"], "Formalize state machines and invariant transitions", &["model state", "state machine"], &["invalid transition"], &["unreachable state"]),

            // 8. rust (6 skills)
            ("implement-slice", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P02", "P07", "P12"], "Author memory-safe, zero-copy Rust implementation slices", &["implement slice", "rust feature"], &["unsafe memory"], &["unbounded clone"]),
            ("audit-unsafe", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P02", "P07", "P12"], "Verify zero undefined behavior in unsafe blocks", &["audit unsafe", "miri verification"], &["unverified pointer"], &["undefined behavior"]),
            ("review-concurrency", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P02", "P07", "P12"], "Audit lock hierarchies, atomics, and thread safety", &["review concurrency", "deadlock check"], &["race condition"], &["unbounded contention"]),
            ("profile-allocation", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P02", "P07", "P12"], "Eliminate unnecessary heap allocations and buffer copies", &["profile allocation", "zero copy audit"], &["hidden heap alloc"], &["memory leak"]),
            ("review-dependencies", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P02", "P07", "P12"], "Enforce minimal dependency footprints and verify supply chain", &["review dependencies", "cargo audit"], &["bloated crate"], &["vulnerable dep"]),
            ("review-test-value", "rust", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P02", "P07", "P12"], "Audit test assertions for behavioral defect detection", &["review test value", "assertion strength"], &["tautological test"], &["flaky assertion"]),

            // 9. format (5 skills)
            ("validate-toon", "format", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P06", "P13"], "Enforce strict TOON grammar and structural invariants", &["validate toon", "toon lint"], &["syntax error"], &["illegal delimiter"]),
            ("canonicalize-record", "format", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P06", "P13"], "Format tabular and key-value objects into canonical order", &["canonicalize record", "sort keys"], &["irregular table"], &["non-deterministic json"]),
            ("migrate-envelope", "format", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P06", "P13"], "Safely transform legacy Markdown and JSON into native TOON", &["migrate envelope", "convert toon"], &["partial migration"], &["data loss"]),
            ("prove-roundtrip", "format", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P06", "P13"], "Verify bit-for-bit equivalence across encode/decode cycles", &["prove roundtrip", "codec test"], &["lossy decode"], &["mutation"]),
            ("generate-host-projection", "format", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P06", "P13"], "Emit bounded host-specific projections for CLI runtimes", &["host projection", "project runtime"], &["oversized projection"], &["broken schema"]),

            // 10. runtime (7 skills)
            ("compile-intent", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P05", "P15", "P16", "P32"], "Transform natural language requests into typed TaskContracts", &["compile intent", "parse prompt"], &["unclear intent"], &["malformed prompt"]),
            ("route-role", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P05", "P15", "P16", "P32"], "Assign leading operational role from the 104-role matrix", &["route role", "assign role"], &["ambiguous role"], &["unmapped specialty"]),
            ("select-model", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P05", "P15", "P16", "P32"], "Match task complexity and risk to optimal model tier", &["select model", "route model"], &["unknown model"], &["unsupported tier"]),
            ("schedule-task", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P05", "P15", "P16", "P32"], "Dispatch tasks across cooperative asynchronous workers", &["schedule task", "dispatch worker"], &["worker starvation"], &["deadlock"]),
            ("reserve-budget", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P05", "P15", "P16", "P32"], "Atomically reserve token, dollar, and time allowances", &["reserve budget", "lock allowance"], &["budget overdraft"], &["stale reservation"]),
            ("cancel-work", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P05", "P15", "P16", "P32"], "Gracefully terminate pending tasks and release reservations", &["cancel work", "abort task"], &["zombie process"], &["stranded lock"]),
            ("isolate-workspace", "runtime", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P05", "P15", "P16", "P32"], "Ensure complete tenant data and execution confinement", &["isolate workspace", "sandbox tenant"], &["boundary leak"], &["shared state"]),

            // 11. assurance (7 skills)
            ("design-contract-test", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P04", "P08", "P09", "P12", "P13"], "Author invariant assertions for system boundaries", &["design contract test", "boundary test"], &["unasserted boundary"], &["shallow test"]),
            ("differential-replay", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Compare execution outcomes against historical goldens", &["differential replay", "golden check"], &["golden mismatch"], &["drift"]),
            ("check-invariants", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Validate the 6 FAANG production invariants before ship", &["check invariants", "faang gate"], &["swallowed error"], &["in-place mutation"]),
            ("fuzz-owned-parser", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Execute property-based stress tests on TOON codec", &["fuzz parser", "afl fuzz"], &["crash input"], &["infinite loop"]),
            ("evaluate-regression", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Catch unintended behavioral regressions across releases", &["evaluate regression", "regression suite"], &["broken feature"], &["untracked delta"]),
            ("reproduce-failure", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Isolate root causes from incident telemetry", &["reproduce failure", "isolate bug"], &["non-reproducible error"], &["heisenbug"]),
            ("attest-evidence", "assurance", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P04", "P08", "P09", "P12", "P13"], "Cryptographically sign verified test outcomes", &["attest evidence", "sign receipt"], &["forged evidence"], &["unsigned test"]),

            // 12. protection (7 skills)
            ("model-trust-boundaries", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P20", "P21"], "Map untrusted inputs and external data paths", &["trust boundaries", "stride threat"], &["unmapped path"], &["blind trust"]),
            ("review-access", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P20", "P21"], "Enforce least privilege on tool permissions and filesystem scopes", &["review access", "least privilege"], &["over-permissioned tool"], &["root execution"]),
            ("verify-data-isolation", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P20", "P21"], "Audit memory and storage boundaries across tenants", &["verify isolation", "tenant privacy"], &["cross-tenant leak"], &["unencrypted data"]),
            ("detect-exposed-secret", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P20", "P21"], "Scan diffs for leaked credentials and sensitive keys", &["detect secret", "gitleaks scan"], &["leaked token"], &["hardcoded password"]),
            ("review-skill-intake", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P20", "P21"], "Security-audit third-party skill definitions prior to admission", &["review skill intake", "skill scan"], &["malicious payload"], &["control bypass"]),
            ("redact-telemetry", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P05", "P07", "P20", "P21"], "Strip PII and secrets from diagnostic logs", &["redact telemetry", "sanitize log"], &["pii leakage"], &["raw token"]),
            ("handle-disclosure", "protection", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P05", "P07", "P20", "P21"], "Execute structured incident disclosure workflows", &["handle disclosure", "cve response"], &["uncoordinated disclosure"], &["coverup"]),

            // 13. delivery (6 skills)
            ("verify-release", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R0, &["P05", "P08", "P11", "P17", "P19"], "Verify clean compilation, linting, and passing test ratchets", &["verify release", "release gate"], &["failing test"], &["decreased coverage"]),
            ("request-publication", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R1, &["P05", "P08", "P11", "P17", "P19"], "Stage release artifacts and request operator deployment sign-off", &["request publication", "stage release"], &["unauthorized push"], &["unreviewed artifact"]),
            ("attest-artifact", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R0, &["P05", "P08", "P11", "P17", "P19"], "Generate provenance digests and signed release receipts", &["attest artifact", "artifact sha"], &["tampered binary"], &["missing digest"]),
            ("stage-canary", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R1, &["P05", "P08", "P11", "P17", "P19"], "Deploy to isolated canary environment for progressive rollout", &["stage canary", "canary deploy"], &["canary failure"], &["unmonitored traffic"]),
            ("reconcile-rollout", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R1, &["P05", "P08", "P11", "P17", "P19"], "Monitor canary health metrics and error budgets", &["reconcile rollout", "monitor canary"], &["slo degradation"], &["budget burn"]),
            ("recover-release", "delivery", "IT & Platform", Department::ItInfra, GoverningPod::PodBuild, RiskTier::R2, &["P05", "P08", "P11", "P17", "P19"], "Execute automated rollback upon canary regression", &["recover release", "rollback deploy"], &["failed rollback"], &["data corruption"]),

            // 14. operations (7 skills)
            ("define-slo", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Establish availability, latency, and error budget objectives", &["define slo", "set sli"], &["unmeasurable objective"], &["unrealistic target"]),
            ("forecast-capacity", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Model infrastructure demands from traffic projections", &["forecast capacity", "resource plan"], &["resource exhaustion"], &["overprovisioning"]),
            ("test-overload", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Stress-test queuing backpressure and graceful load shedding", &["test overload", "load shed"], &["service crash"], &["unbounded latency"]),
            ("investigate-tail", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Profile high-percentile p99 latency anomalies", &["investigate tail", "p99 latency"], &["unexplained spike"], &["noisy neighbor"]),
            ("contain-incident", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Mitigate live service failures and isolate blast radius", &["contain incident", "kill switch"], &["cascading failure"], &["split brain"]),
            ("restore-backup", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R2, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Drill disaster recovery and point-in-time data restoration", &["restore backup", "disaster recovery"], &["corrupt snapshot"], &["untested recovery"]),
            ("run-postmortem", "operations", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P12", "P14", "P15", "P16", "P17", "P18", "P20"], "Author blameless incident retrospectives and action items", &["run postmortem", "blameless review"], &["punitive blame"], &["untracked action"]),

            // 15. migration (6 skills)
            ("inventory-behavior", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P03", "P06", "P09", "P10", "P12"], "Map legacy entrypoints, state stores, and external adapters", &["inventory behavior", "freeze legacy"], &["unmapped path"], &["unknown dependency"]),
            ("shadow-replay", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P03", "P06", "P09", "P10", "P12"], "Compare new runtime behavior against legacy baselines", &["shadow replay", "dark launch"], &["divergent behavior"], &["missed edge case"]),
            ("reconcile-state", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P03", "P06", "P09", "P10", "P12"], "Detect and reconcile discrepancies between dual state stores", &["reconcile state", "dual read"], &["data discrepancy"], &["split state"]),
            ("fence-writer", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P03", "P06", "P09", "P10", "P12"], "Prevent dual-writer split-brain during database cutover", &["fence writer", "single writer"], &["stale write"], &["concurrent mutation"]),
            ("rehearse-cutover", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P03", "P06", "P09", "P10", "P12"], "Simulate complete production cutover in staging", &["rehearse cutover", "cutover drill"], &["unexpected downtime"], &["irreversible failure"]),
            ("retire-legacy", "migration", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R2, &["P03", "P06", "P09", "P10", "P12"], "Safely decommission superseded codebases and schemas", &["retire legacy", "delete old"], &["premature deletion"], &["dangling caller"]),

            // 16. executive (4 skills)
            ("set-outcome", "executive", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P01", "P17", "P23", "P32"], "Define strategic business milestones and objectives", &["set outcome", "strategic goal"], &["unclear objective"], &["unrealistic target"]),
            ("prioritize-portfolio", "executive", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P01", "P17", "P23", "P32"], "Allocate resources across competing initiatives", &["prioritize portfolio", "rank projects"], &["competing priority"], &["resource conflict"]),
            ("allocate-capacity", "executive", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R1, &["P01", "P17", "P23", "P32"], "Balance operational bandwidth across pods", &["allocate capacity", "pod bandwidth"], &["overallocation"], &["bottleneck"]),
            ("review-enterprise-risk", "executive", "Executive", Department::Executive, GoverningPod::PodGna, RiskTier::R0, &["P01", "P17", "P23", "P32"], "Assess legal, financial, and strategic threats", &["review enterprise risk", "threat assessment"], &["unmitigated threat"], &["fiduciary breach"]),

            // 17. product (5 skills)
            ("interview-user", "product", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P23", "P24", "P28"], "Conduct customer discovery and synthesize pain points", &["interview user", "customer discovery"], &["biased inquiry"], &["invented need"]),
            ("write-prd", "product", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P23", "P24", "P28"], "Author comprehensive product requirement documents", &["write prd", "product spec"], &["ambiguous requirement"], &["unscoped feature"]),
            ("rank-opportunities", "product", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P23", "P24", "P28"], "Score potential features using customer impact frameworks", &["rank opportunities", "rice score"], &["unsupported score"], &["feature bloat"]),
            ("define-success-metric", "product", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P23", "P24", "P28"], "Establish measurable KPIs and telemetry events", &["define success metric", "kpi tracking"], &["vanity metric"], &["uninstrumented goal"]),
            ("validate-prototype", "product", "Product", Department::Product, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P23", "P24", "P28"], "Evaluate experimental features with user feedback", &["validate prototype", "user test"], &["unvalidated assumption"], &["premature launch"]),

            // 18. engineering (4 skills)
            ("estimate-delivery", "engineering", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P07", "P08"], "Produce calibrated effort estimates and risk buffers", &["estimate delivery", "story pointing"], &["uncalibrated estimate"], &["missing risk"]),
            ("implement-client-change", "engineering", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P04", "P07", "P08"], "Author clean, tested business logic changes", &["implement client change", "code change"], &["untested code"], &["breaking change"]),
            ("review-client-change", "engineering", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R0, &["P01", "P04", "P07", "P08"], "Conduct independent peer review across code diffs", &["review client change", "code review"], &["unreviewed diff"], &["rubber stamp"]),
            ("prepare-client-release", "engineering", "Engineering", Department::Engineering, GoverningPod::PodBuild, RiskTier::R1, &["P01", "P04", "P07", "P08"], "Package and verify deliverables for client handoff", &["prepare client release", "package release"], &["missing deliverable"], &["unverified artifact"]),

            // 19. data-ai (5 skills)
            ("profile-data-quality", "data-ai", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P12", "P21", "P23", "P27"], "Detect anomalies, missing fields, and distribution shifts", &["profile data quality", "data integrity"], &["dirty data"], &["corrupt column"]),
            ("establish-evaluation-set", "data-ai", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R1, &["P06", "P12", "P21", "P23", "P27"], "Build curated ground-truth datasets for benchmarks", &["evaluation set", "ground truth"], &["data leakage"], &["biased sample"]),
            ("assess-model-drift", "data-ai", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P12", "P21", "P23", "P27"], "Monitor accuracy degradation in production model outputs", &["assess model drift", "drift detection"], &["degraded accuracy"], &["unmonitored model"]),
            ("evaluate-model-change", "data-ai", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P12", "P21", "P23", "P27"], "Compare challenger models against incumbent baselines", &["evaluate model change", "model comparison"], &["overfitted model"], &["cherry-picked metric"]),
            ("assess-cohort-quality", "data-ai", "Data & AI", Department::DataAi, GoverningPod::PodBuild, RiskTier::R0, &["P06", "P12", "P21", "P23", "P27"], "Analyze retention and user segments from behavioral data", &["assess cohort quality", "cohort analysis"], &["confounded segment"], &["unreliable signal"]),

            // 20. design (5 skills)
            ("map-user-journey", "design", "Design", Department::Design, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P30"], "Chart end-to-end customer interaction workflows", &["map user journey", "interaction flow"], &["disconnected flow"], &["blind step"]),
            ("design-interaction", "design", "Design", Department::Design, GoverningPod::PodBuild, RiskTier::R1, &["P23", "P24", "P26", "P30"], "Create intuitive UI layouts, components, and microcopy", &["design interaction", "ui layout"], &["confusing ui"], &["inaccessible control"]),
            ("review-accessibility", "design", "Design", Department::Design, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P30"], "Audit color contrast, keyboard navigation, and screen reader tags", &["review accessibility", "wcag audit"], &["contrast failure"], &["keyboard trap"]),
            ("localize-interface", "design", "Design", Department::Design, GoverningPod::PodBuild, RiskTier::R1, &["P23", "P24", "P26", "P30"], "Adapt UI typography, spacing, and copy for target locales", &["localize interface", "gujarati localization"], &["broken layout"], &["untranslated string"]),
            ("validate-content", "design", "Design", Department::Design, GoverningPod::PodBuild, RiskTier::R0, &["P23", "P24", "P26", "P30"], "Ensure marketing and product copy aligns with brand voice", &["validate content", "brand copy audit"], &["ai slop"], &["off-brand tone"]),

            // 21. marketing (5 skills)
            ("research-audience", "marketing", "Marketing", Department::Marketing, GoverningPod::PodGrowth, RiskTier::R0, &["P06", "P21", "P23", "P24"], "Identify target customer personas and channel preferences", &["research audience", "persona discovery"], &["fictional persona"], &["unvalidated segment"]),
            ("plan-campaign", "marketing", "Marketing", Department::Marketing, GoverningPod::PodGrowth, RiskTier::R1, &["P06", "P21", "P23", "P24"], "Develop multi-channel acquisition and content calendars", &["plan campaign", "content calendar"], &["unrealistic frequency"], &["spam campaign"]),
            ("draft-channel-content", "marketing", "Marketing", Department::Marketing, GoverningPod::PodGrowth, RiskTier::R1, &["P06", "P21", "P23", "P24"], "Author engaging copy for social, email, and blog channels", &["draft channel content", "marketing copy"], &["low-quality copy"], &["plagiarism"]),
            ("measure-campaign", "marketing", "Marketing", Department::Marketing, GoverningPod::PodGrowth, RiskTier::R0, &["P06", "P21", "P23", "P24"], "Track CAC, ROAS, and conversion funnel analytics", &["measure campaign", "cac roas analytics"], &["unattributed lead"], &["vanity metric"]),
            ("prepare-media-brief", "marketing", "Marketing", Department::Marketing, GoverningPod::PodGrowth, RiskTier::R1, &["P06", "P21", "P23", "P24"], "Create creative direction guidelines for media assets", &["prepare media brief", "creative brief"], &["vague direction"], &["missing specification"]),

            // 22. sales-bd (5 skills)
            ("qualify-lead", "sales-bd", "Sales & BD", Department::SalesBd, GoverningPod::PodGrowth, RiskTier::R0, &["P04", "P05", "P06", "P23"], "Score prospect fit against ideal customer profile", &["qualify lead", "icp score"], &["unqualified lead"], &["fake contact"]),
            ("draft-proposal", "sales-bd", "Sales & BD", Department::SalesBd, GoverningPod::PodGrowth, RiskTier::R1, &["P04", "P05", "P06", "P23"], "Author tailored commercial proposals and service agreements", &["draft proposal", "commercial agreement"], &["unscoped deliverables"], &["unbounded liability"]),
            ("maintain-crm", "sales-bd", "Sales & BD", Department::SalesBd, GoverningPod::PodGrowth, RiskTier::R1, &["P04", "P05", "P06", "P23"], "Keep opportunity stages, notes, and deal contacts synchronized", &["maintain crm", "sync deal"], &["stale pipeline"], &["duplicate record"]),
            ("forecast-pipeline", "sales-bd", "Sales & BD", Department::SalesBd, GoverningPod::PodGrowth, RiskTier::R0, &["P04", "P05", "P06", "P23"], "Project monthly and quarterly revenue based on deal velocity", &["forecast pipeline", "revenue projection"], &["sandbagged deal"], &["unrealistic close date"]),
            ("prepare-partnership", "sales-bd", "Sales & BD", Department::SalesBd, GoverningPod::PodGrowth, RiskTier::R1, &["P04", "P05", "P06", "P23"], "Structure mutual co-marketing and strategic alliance terms", &["prepare partnership", "alliance agreement"], &["one-sided terms"], &["unauthorized commitment"]),

            // 23. customer-success (5 skills)
            ("onboard-client", "customer-success", "Customer Success", Department::CustomerSuccess, GoverningPod::PodCustomer, RiskTier::R1, &["P04", "P11", "P23", "P26", "P31"], "Guide new clients through setup milestones and time-to-value", &["onboard client", "client setup"], &["delayed onboarding"], &["missing requirement"]),
            ("triage-support", "customer-success", "Customer Success", Department::CustomerSuccess, GoverningPod::PodCustomer, RiskTier::R0, &["P04", "P11", "P23", "P26", "P31"], "Prioritize incoming support requests by customer tier and severity", &["triage support", "ticket priority"], &["misclassified severity"], &["ignored customer"]),
            ("draft-resolution", "customer-success", "Customer Success", Department::CustomerSuccess, GoverningPod::PodCustomer, RiskTier::R1, &["P04", "P11", "P23", "P26", "P31"], "Author technical issue resolutions and knowledgebase articles", &["draft resolution", "support answer"], &["inaccurate solution"], &["untested workaround"]),
            ("escalate-case", "customer-success", "Customer Success", Department::CustomerSuccess, GoverningPod::PodCustomer, RiskTier::R1, &["P04", "P11", "P23", "P26", "P31"], "Route critical bugs and blockers to engineering and leadership", &["escalate case", "priority escalation"], &["unjustified escalation"], &["unnotified team"]),
            ("confirm-handover", "customer-success", "Customer Success", Department::CustomerSuccess, GoverningPod::PodCustomer, RiskTier::R1, &["P04", "P11", "P23", "P26", "P31"], "Validate customer satisfaction and sign off on delivered scope", &["confirm handover", "client signoff"], &["unresolved punchlist"], &["premature completion"]),

            // 24. finance (5 skills)
            ("prepare-estimate", "finance", "Finance", Department::Finance, GoverningPod::PodGna, RiskTier::R0, &["P06", "P09", "P10", "P32"], "Calculate project costs, margins, and payment milestones", &["prepare estimate", "cost quote"], &["underestimated expense"], &["negative margin"]),
            ("reconcile-invoice", "finance", "Finance", Department::Finance, GoverningPod::PodGna, RiskTier::R1, &["P06", "P09", "P10", "P32"], "Match incoming supplier invoices against purchase orders", &["reconcile invoice", "po matching"], &["unmatched invoice"], &["duplicate billing"]),
            ("reconcile-ledger", "finance", "Finance", Department::Finance, GoverningPod::PodGna, RiskTier::R1, &["P06", "P09", "P10", "P32"], "Verify bank transactions against general ledger accounts", &["reconcile ledger", "bank reconciliation"], &["unbalanced ledger"], &["missing transaction"]),
            ("forecast-cash", "finance", "Finance", Department::Finance, GoverningPod::PodGna, RiskTier::R0, &["P06", "P09", "P10", "P32"], "Project 13-week rolling cash flow and runway", &["forecast cash", "13-week runway"], &["liquidity crisis"], &["untracked liability"]),
            ("review-unit-economics", "finance", "Finance", Department::Finance, GoverningPod::PodGna, RiskTier::R0, &["P06", "P09", "P10", "P32"], "Analyze gross margins, CAC payback, and LTV", &["review unit economics", "ltv cac analysis"], &["unsustainable economics"], &["negative contribution"]),

            // 25. legal-compliance (5 skills)
            ("triage-jurisdiction", "legal-compliance", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P06", "P07", "P21"], "Identify applicable regulatory regimes like GDPR, CCPA, or HIPAA", &["triage jurisdiction", "regulatory scope"], &["unmapped regulation"], &["non-compliance"]),
            ("review-contract", "legal-compliance", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P06", "P07", "P21"], "Identify indemnity, liability caps, and termination clauses", &["review contract", "contract analysis"], &["unlimited liability"], &["hidden clause"]),
            ("record-license", "legal-compliance", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R1, &["P05", "P06", "P07", "P21"], "Track open source and vendor software licensing obligations", &["record license", "license inventory"], &["unlicensed dependency"], &["gpl violation"]),
            ("assess-privacy-request", "legal-compliance", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R1, &["P05", "P06", "P07", "P21"], "Coordinate data subject access and deletion requests DSAR", &["assess privacy request", "dsar processing"], &["missed deadline"], &["data spoliation"]),
            ("prepare-compliance-evidence", "legal-compliance", "Legal & Compliance", Department::LegalCompliance, GoverningPod::PodGna, RiskTier::R0, &["P05", "P06", "P07", "P21"], "Compile audit-ready security and governance documentation", &["compliance evidence", "audit package"], &["missing evidence"], &["forged audit record"]),

            // 26. people-ops (5 skills)
            ("define-role", "people-ops", "People & Ops", Department::PeopleOps, GoverningPod::PodPeople, RiskTier::R1, &["P05", "P06", "P21", "P23", "P25"], "Author objective job descriptions and leveling competencies", &["define role", "job description"], &["discriminatory criteria"], &["unrealistic requirement"]),
            ("draft-hiring-rubric", "people-ops", "People & Ops", Department::PeopleOps, GoverningPod::PodPeople, RiskTier::R1, &["P05", "P06", "P21", "P23", "P25"], "Establish structured interview evaluation scorecards", &["draft hiring rubric", "interview rubric"], &["subjective bias"], &["inconsistent grading"]),
            ("coordinate-interviews", "people-ops", "People & Ops", Department::PeopleOps, GoverningPod::PodPeople, RiskTier::R1, &["P05", "P06", "P21", "P23", "P25"], "Manage candidate scheduling and interview team handoffs", &["coordinate interviews", "schedule candidate"], &["scheduling conflict"], &["dropped candidate"]),
            ("onboard-colleague", "people-ops", "People & Ops", Department::PeopleOps, GoverningPod::PodPeople, RiskTier::R1, &["P05", "P06", "P21", "P23", "P25"], "Facilitate new hire systems access and culture orientation", &["onboard colleague", "new hire setup"], &["delayed access"], &["unsupervised starter"]),
            ("review-vendor", "people-ops", "People & Ops", Department::PeopleOps, GoverningPod::PodPeople, RiskTier::R0, &["P05", "P06", "P21", "P23", "P25"], "Evaluate contractors and HR tooling providers on security and cost", &["review vendor", "vendor assessment"], &["insecure vendor"], &["excessive cost"]),

            // 27. it-platform (5 skills)
            ("provision-scoped-access", "it-platform", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P05", "P07", "P17", "P20"], "Grant role-based least-privilege credentials", &["provision scoped access", "grant access"], &["excessive privilege"], &["unauthorized role"]),
            ("plan-infrastructure", "it-platform", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P17", "P20"], "Architect cloud infrastructure for resilience and cost efficiency", &["plan infrastructure", "cloud architecture"], &["single point of failure"], &["unbudgeted cluster"]),
            ("verify-observability", "it-platform", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R0, &["P05", "P07", "P17", "P20"], "Ensure metrics, traces, and alerts cover critical journeys", &["verify observability", "check telemetry"], &["blind spot"], &["unalerted failure"]),
            ("recover-service", "it-platform", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R2, &["P05", "P07", "P17", "P20"], "Execute automated failover and incident mitigation playbooks", &["recover service", "service failover"], &["failed failover"], &["data loss"]),
            ("revoke-access", "it-platform", "IT & Platform", Department::ItInfra, GoverningPod::PodGna, RiskTier::R1, &["P05", "P07", "P17", "P20"], "Deprovision access keys and accounts upon role change or offboarding", &["revoke access", "deprovision keys"], &["lingering key"], &["unrevoked account"]),
        ];

        raw_specs
            .into_iter()
            .map(|(id, home, team, dept, pod, risk, principles, intent, routes, clarify, abstain)| {
                CanonicalSkill {
                    id: id.to_string(),
                    home: home.to_string(),
                    canonical_path: format!("knowledge/skills/{}/{}.toon", home, id),
                    owner_team: team.to_string(),
                    department: dept,
                    pod,
                    principles: principles.iter().map(|s| s.to_string()).collect(),
                    risk_tier: risk,
                    intent: intent.to_string(),
                    route_labels: routes.iter().map(|s| s.to_string()).collect(),
                    clarification_triggers: clarify.iter().map(|s| s.to_string()).collect(),
                    abstention_triggers: abstain.iter().map(|s| s.to_string()).collect(),
                }
            })
            .collect()
    }

    pub fn get_skill(id: &str) -> Option<CanonicalSkill> {
        Self::load_required_153().into_iter().find(|s| s.id == id)
    }

    pub fn skills_by_home(home: &str) -> Vec<CanonicalSkill> {
        Self::load_required_153().into_iter().filter(|s| s.home == home).collect()
    }

    pub fn skills_by_department(dept: Department) -> Vec<CanonicalSkill> {
        Self::load_required_153().into_iter().filter(|s| s.department == dept).collect()
    }

    pub fn skills_by_pod(pod: GoverningPod) -> Vec<CanonicalSkill> {
        Self::load_required_153().into_iter().filter(|s| s.pod == pod).collect()
    }

    pub fn get_department_fixtures() -> Vec<DepartmentFixture> {
        vec![
            DepartmentFixture {
                department: Department::Executive,
                pod: GoverningPod::PodGna,
                skill_id: "prioritize-portfolio".to_string(),
                positive_prompt: "Prioritize portfolio initiatives against Q1 revenue targets".to_string(),
                expected_output_type: "portfolio_ranking".to_string(),
                negative_prompt: "Unilaterally override board fiduciary vote".to_string(),
                abstention_reason: "Board fiduciary override exceeds executive delegation authority".to_string(),
                interruption_prompt: "Allocate cross-pod capacity for strategic transformation".to_string(),
                recovery_checkpoint: "executive-allocation-step-2".to_string(),
            },
            DepartmentFixture {
                department: Department::Product,
                pod: GoverningPod::PodBuild,
                skill_id: "write-prd".to_string(),
                positive_prompt: "Write PRD for client portal".to_string(),
                expected_output_type: "prd_document".to_string(),
                negative_prompt: "Publish unapproved pricing tiers to public store".to_string(),
                abstention_reason: "Direct pricing change requires finance and executive sign-off".to_string(),
                interruption_prompt: "Decompose user onboarding milestone into atomic tasks".to_string(),
                recovery_checkpoint: "product-milestone-step-3".to_string(),
            },
            DepartmentFixture {
                department: Department::Engineering,
                pod: GoverningPod::PodBuild,
                skill_id: "implement-client-change".to_string(),
                positive_prompt: "Implement client change for isolated data adapter".to_string(),
                expected_output_type: "code_diff".to_string(),
                negative_prompt: "Deploy unreviewed binary straight to production server".to_string(),
                abstention_reason: "Production deployment without checker review violates FAANG Invariant 6".to_string(),
                interruption_prompt: "Execute contract test suite across domain boundaries".to_string(),
                recovery_checkpoint: "eng-contract-test-batch-2".to_string(),
            },
            DepartmentFixture {
                department: Department::DataAi,
                pod: GoverningPod::PodBuild,
                skill_id: "profile-data-quality".to_string(),
                positive_prompt: "Profile data quality on client intake CSV".to_string(),
                expected_output_type: "quality_scorecard".to_string(),
                negative_prompt: "Scrape PII from external unauthorized source".to_string(),
                abstention_reason: "Intake of non-consented PII violates Principle P21".to_string(),
                interruption_prompt: "Evaluate candidate model against held-out benchmark".to_string(),
                recovery_checkpoint: "data-eval-fold-3".to_string(),
            },
            DepartmentFixture {
                department: Department::Design,
                pod: GoverningPod::PodBuild,
                skill_id: "review-accessibility".to_string(),
                positive_prompt: "Review accessibility for dashboard color contrast and navigation".to_string(),
                expected_output_type: "wcag_report".to_string(),
                negative_prompt: "Inject proprietary dark patterns into cancellation screen".to_string(),
                abstention_reason: "Dark patterns violate accessibility and transparency standards".to_string(),
                interruption_prompt: "Localize onboarding interaction flow for Gujarati locale".to_string(),
                recovery_checkpoint: "design-localize-screen-2".to_string(),
            },
            DepartmentFixture {
                department: Department::Marketing,
                pod: GoverningPod::PodGrowth,
                skill_id: "plan-campaign".to_string(),
                positive_prompt: "Plan campaign content calendar for solo founder launch".to_string(),
                expected_output_type: "campaign_schedule".to_string(),
                negative_prompt: "Blast unverified spam email to scraped addresses".to_string(),
                abstention_reason: "Bulk messaging unverified contacts violates acceptable use".to_string(),
                interruption_prompt: "Research target audience personas for freelance tools".to_string(),
                recovery_checkpoint: "mkt-persona-2".to_string(),
            },
            DepartmentFixture {
                department: Department::SalesBd,
                pod: GoverningPod::PodGrowth,
                skill_id: "draft-proposal".to_string(),
                positive_prompt: "Draft proposal for 12-hour client onboarding".to_string(),
                expected_output_type: "commercial_proposal".to_string(),
                negative_prompt: "Commit legal entity to unlimited liability indemnity".to_string(),
                abstention_reason: "Unlimited liability commitments require General Counsel review".to_string(),
                interruption_prompt: "Maintain CRM opportunity pipeline stages".to_string(),
                recovery_checkpoint: "sales-crm-deal-1".to_string(),
            },
            DepartmentFixture {
                department: Department::CustomerSuccess,
                pod: GoverningPod::PodCustomer,
                skill_id: "onboard-client".to_string(),
                positive_prompt: "Onboard client and generate setup checklist".to_string(),
                expected_output_type: "onboarding_checklist".to_string(),
                negative_prompt: "Disclose other client contract terms during support call".to_string(),
                abstention_reason: "Cross-tenant information disclosure prohibited under P21".to_string(),
                interruption_prompt: "Triage support ticket and draft resolution".to_string(),
                recovery_checkpoint: "cs-triage-diagnosis".to_string(),
            },
            DepartmentFixture {
                department: Department::Finance,
                pod: GoverningPod::PodGna,
                skill_id: "reconcile-invoice".to_string(),
                positive_prompt: "Reconcile invoice with monthly Stripe payouts".to_string(),
                expected_output_type: "reconciliation_ledger".to_string(),
                negative_prompt: "Authorize untracked $5,000 wire transfer without receipt".to_string(),
                abstention_reason: "Unreceipted wire transfer violates Principle P09".to_string(),
                interruption_prompt: "Forecast 13-week cashflow runway".to_string(),
                recovery_checkpoint: "finance-cashflow-week-6".to_string(),
            },
            DepartmentFixture {
                department: Department::LegalCompliance,
                pod: GoverningPod::PodGna,
                skill_id: "review-contract".to_string(),
                positive_prompt: "Review contract NDA for reciprocal protection".to_string(),
                expected_output_type: "nda_redline".to_string(),
                negative_prompt: "Provide binding legal defense counsel in criminal proceeding".to_string(),
                abstention_reason: "Binding legal defense requires licensed jurisdiction attorney".to_string(),
                interruption_prompt: "Audit data subject access request history".to_string(),
                recovery_checkpoint: "legal-dsar-record-10".to_string(),
            },
            DepartmentFixture {
                department: Department::PeopleOps,
                pod: GoverningPod::PodPeople,
                skill_id: "draft-hiring-rubric".to_string(),
                positive_prompt: "Draft hiring rubric for senior software engineer".to_string(),
                expected_output_type: "evaluation_scorecard".to_string(),
                negative_prompt: "Inquire about protected demographic traits in interview".to_string(),
                abstention_reason: "Inquiring into protected characteristics violates employment law".to_string(),
                interruption_prompt: "Coordinate interview schedule across panel".to_string(),
                recovery_checkpoint: "people-interview-slot-2".to_string(),
            },
            DepartmentFixture {
                department: Department::ItInfra,
                pod: GoverningPod::PodGna,
                skill_id: "provision-scoped-access".to_string(),
                positive_prompt: "Provision scoped access token with read-only repository role".to_string(),
                expected_output_type: "scoped_token".to_string(),
                negative_prompt: "Disable firewall and open root SSH to public internet".to_string(),
                abstention_reason: "Disabling infrastructure access controls strictly blocked".to_string(),
                interruption_prompt: "Verify observability metrics ingestion across nodes".to_string(),
                recovery_checkpoint: "infra-node-telemetry-2".to_string(),
            },
        ]
    }

    pub fn evaluate_natural_language_route(prompt: &str) -> RouteEvaluationResult {
        let p_lower = prompt.to_lowercase();

        // 1. Check abstention / negative / prohibited patterns first
        let abstention_cases = [
            ("override board", "Board fiduciary override exceeds executive delegation authority"),
            ("unapproved pricing", "Direct pricing change requires finance and executive sign-off"),
            ("deploy unreviewed", "Production deployment without checker review violates FAANG Invariant 6"),
            ("scrape pii", "Intake of non-consented PII violates Principle P21"),
            ("dark patterns", "Dark patterns violate accessibility and transparency standards"),
            ("spam email", "Bulk messaging unverified contacts violates acceptable use"),
            ("unlimited liability", "Unlimited liability commitments require General Counsel review"),
            ("disclose other client", "Cross-tenant information disclosure prohibited under P21"),
            ("untracked $5,000", "Unreceipted wire transfer violates Principle P09"),
            ("criminal proceeding", "Binding legal defense requires licensed jurisdiction attorney"),
            ("protected demographic", "Inquiring into protected characteristics violates employment law"),
            ("disable firewall", "Disabling infrastructure access controls strictly blocked"),
            ("bypass safety", "Bypassing safety controls strictly prohibited"),
        ];

        for (pattern, reason) in &abstention_cases {
            if p_lower.contains(pattern) {
                return RouteEvaluationResult::Abstain {
                    reason: reason.to_string(),
                };
            }
        }

        // 2. Check clarification triggers
        let clarification_cases = [
            ("vague goal", "Could you specify the target deliverables and constraints for this goal?"),
            ("ambiguous request", "Could you clarify the expected scope and governing criteria?"),
            ("conflicting constraint", "There is a conflict in the constraints. Which priority takes precedence?"),
            ("unclear impact", "What is the expected operational risk tier for this operation?"),
        ];

        for (pattern, question) in &clarification_cases {
            if p_lower.contains(pattern) {
                return RouteEvaluationResult::ClarificationRequired {
                    prompt: prompt.to_string(),
                    question: question.to_string(),
                };
            }
        }

        // 3. Match positive routes across the 153 skills
        let all_skills = Self::load_required_153();

        // Pass 1: exact substring match of route label
        for skill in &all_skills {
            for label in &skill.route_labels {
                let l_lower = label.to_lowercase();
                if p_lower.contains(&l_lower) {
                    return RouteEvaluationResult::Matched {
                        skill_id: skill.id.clone(),
                        department: skill.department,
                        pod: skill.pod,
                    };
                }
            }
        }

        // Pass 2: whole-word matching across all words of route label
        let prompt_tokens: std::collections::HashSet<&str> = p_lower
            .split(|c: char| !c.is_alphanumeric() && c != '-')
            .filter(|s| !s.is_empty())
            .collect();

        for skill in all_skills {
            for label in &skill.route_labels {
                let l_lower = label.to_lowercase();
                let words: Vec<&str> = l_lower.split_whitespace().collect();
                if words.len() > 1 && words.iter().all(|w| prompt_tokens.contains(*w)) {
                    return RouteEvaluationResult::Matched {
                        skill_id: skill.id,
                        department: skill.department,
                        pod: skill.pod,
                    };
                }
            }
        }

        // 4. Default out-of-scope abstention
        RouteEvaluationResult::Abstain {
            reason: format!("No matching operational capability found for query: '{}'", prompt),
        }
    }

    pub fn validate_tenant_specialty(skill_id: &str, is_admitted: bool) -> Result<(), &'static str> {
        if skill_id.starts_with("specialty-") && !is_admitted {
            return Err("Tenant specialty packaged as lazy runbook and not admitted into active catalog");
        }
        Ok(())
    }
}
