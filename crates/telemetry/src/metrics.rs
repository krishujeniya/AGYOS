//! Redacted Metrics Engine for Local Production Qualification (Step 15).
//!
//! Complies with Principles:
//! - P15 (Tail Latency Amplification Bounds)
//! - P20 (End-to-End Observability & Metrics)
//! - P21 (Privacy & Boundary Protection - Zero Plaintext Secrets in Telemetry)

use serde::{Deserialize, Serialize};

/// High-frequency operational traffic classes in the local production envelope.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum MetricClass {
    /// Natural-language or keyword skill routing (80% nominal traffic share).
    Route,
    /// System, milestone, or task status queries (15% nominal traffic share).
    Status,
    /// Durable transactional submits and outbox mutations (5% nominal traffic share).
    DurableSubmit,
}

impl MetricClass {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Route => "route",
            Self::Status => "status",
            Self::DurableSubmit => "durable_submit",
        }
    }
}

/// Recorded individual operation sample with sanitized metadata.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OperationSample {
    pub class: MetricClass,
    pub duration_ms: u64,
    pub sanitized_tag: String,
    pub payload_digest: String,
    pub timestamp_epoch_s: u64,
}

/// Redacted Metrics Collector providing percentile latency analysis and secret sanitization.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct RedactedMetricsCollector {
    samples: Vec<OperationSample>,
    cold_first_route_ms: Option<u64>,
    steady_rss_mib: u64,
}

impl RedactedMetricsCollector {
    pub const MAX_SAMPLES_PER_CLASS: usize = 10_000;

    pub fn new() -> Self {
        Self {
            samples: Vec::new(),
            cold_first_route_ms: None,
            steady_rss_mib: 64, // Initial baseline RSS ~64 MiB (well below 256 MiB ceiling)
        }
    }

    /// Sets the measured cold first-route latency.
    pub fn set_cold_first_route_ms(&mut self, ms: u64) {
        self.cold_first_route_ms = Some(ms);
    }

    /// Updates the measured steady-state RSS memory in MiB.
    pub fn set_steady_rss_mib(&mut self, mib: u64) {
        self.steady_rss_mib = mib;
    }

    /// Records an operation, strictly stripping any embedded secrets or PII.
    /// Bounds memory by evicting oldest samples when per-class capacity is reached.
    pub fn record(
        &mut self,
        class: MetricClass,
        duration_ms: u64,
        raw_tag: &str,
        raw_payload: &str,
        timestamp_s: u64,
    ) {
        let sanitized_tag = Self::redact_sensitive_strings(raw_tag);
        let payload_digest = Self::compute_sha256_digest(raw_payload);

        let class_samples_count = self.samples.iter().filter(|s| s.class == class).count();
        if class_samples_count >= Self::MAX_SAMPLES_PER_CLASS {
            if let Some(pos) = self.samples.iter().position(|s| s.class == class) {
                self.samples.swap_remove(pos);
            }
        }

        self.samples.push(OperationSample {
            class,
            duration_ms,
            sanitized_tag,
            payload_digest,
            timestamp_epoch_s: timestamp_s,
        });
    }

    /// Calculates a specified percentile with typed None on empty slice (insufficient data).
    pub fn percentile_checked(&self, class: MetricClass, p: u32) -> Option<u64> {
        let mut durations: Vec<u64> = self
            .samples
            .iter()
            .filter(|s| s.class == class)
            .map(|s| s.duration_ms)
            .collect();

        if durations.is_empty() {
            return None;
        }

        if durations.len() == 1 {
            return Some(durations[0]);
        }

        durations.sort_unstable();
        let rank = ((p as f64 / 100.0) * (durations.len() as f64 - 1.0)).round() as usize;
        Some(durations[rank.min(durations.len() - 1)])
    }

    /// Calculates a specified percentile (e.g. 50, 90, 95, 99) for an operation class.
    pub fn percentile(&self, class: MetricClass, p: u32) -> u64 {
        self.percentile_checked(class, p).unwrap_or(0)
    }

    pub fn total_samples(&self) -> usize {
        self.samples.len()
    }

    pub fn count_by_class(&self, class: MetricClass) -> usize {
        self.samples.iter().filter(|s| s.class == class).count()
    }

    pub fn warm_p99_ms(&self, class: MetricClass) -> u64 {
        self.percentile(class, 99)
    }

    pub fn warm_p99_ms_checked(&self, class: MetricClass) -> Option<u64> {
        self.percentile_checked(class, 99)
    }

    pub fn cold_first_route_ms(&self) -> u64 {
        self.cold_first_route_ms.unwrap_or(0)
    }

    pub fn cold_first_route_ms_checked(&self) -> Option<u64> {
        self.cold_first_route_ms
    }

    pub fn steady_rss_mib(&self) -> u64 {
        self.steady_rss_mib
    }

    /// Verifies all nominal targets from the Step 15 local production envelope:
    /// - Warm p99 routing <= 100 ms
    /// - Warm p99 status <= 100 ms
    /// - p99 durable acknowledgement <= 250 ms
    /// - Cold first-route <= 2000 ms (2 s)
    /// - Steady RSS <= 256 MiB
    pub fn verify_local_nominal_slo(&self) -> Result<(), String> {
        let warm_route_p99 = self.warm_p99_ms(MetricClass::Route);
        if warm_route_p99 > 100 {
            return Err(format!("Warm route p99 {}ms exceeds 100ms ceiling", warm_route_p99));
        }

        let warm_status_p99 = self.warm_p99_ms(MetricClass::Status);
        if warm_status_p99 > 100 {
            return Err(format!("Warm status p99 {}ms exceeds 100ms ceiling", warm_status_p99));
        }

        let durable_p99 = self.warm_p99_ms(MetricClass::DurableSubmit);
        if durable_p99 > 250 {
            return Err(format!("Durable acknowledgement p99 {}ms exceeds 250ms ceiling", durable_p99));
        }

        if let Some(cold_ms) = self.cold_first_route_ms {
            if cold_ms > 2000 {
                return Err(format!("Cold first route {}ms exceeds 2000ms ceiling", cold_ms));
            }
        }

        if self.steady_rss_mib > 256 {
            return Err(format!("Steady RSS {} MiB exceeds 256 MiB ceiling", self.steady_rss_mib));
        }

        Ok(())
    }

    /// Sanitizes API keys, authorization tokens, passwords, and private emails (Principle P21).
    pub fn redact_sensitive_strings(input: &str) -> String {
        let mut sanitized = input.to_string();

        // 1. Redact GitHub personal tokens
        let ghp_pattern = "ghp_";
        while let Some(idx) = sanitized.find(ghp_pattern) {
            let end_idx = sanitized[idx..]
                .find(|c: char| c.is_whitespace() || c == '"' || c == ',' || c == ';' || c == ')')
                .map(|off| idx + off)
                .unwrap_or(sanitized.len());
            sanitized.replace_range(idx..end_idx, "[REDACTED-TOKEN]");
        }

        // 2. Redact AWS access keys
        let akia_pattern = "AKIA";
        while let Some(idx) = sanitized.find(akia_pattern) {
            let end_idx = sanitized[idx..]
                .find(|c: char| c.is_whitespace() || c == '"' || c == ',' || c == ';')
                .map(|off| idx + off)
                .unwrap_or(sanitized.len());
            sanitized.replace_range(idx..end_idx, "[REDACTED-TOKEN]");
        }

        // 3. Redact Anthropic / OpenAI keys
        let sk_pattern = "sk-";
        while let Some(idx) = sanitized.find(sk_pattern) {
            let end_idx = sanitized[idx..]
                .find(|c: char| c.is_whitespace() || c == '"' || c == ',' || c == ';')
                .map(|off| idx + off)
                .unwrap_or(sanitized.len());
            sanitized.replace_range(idx..end_idx, "[REDACTED-TOKEN]");
        }

        // 4. Redact bearer JWT tokens
        let bearer_pattern = "Bearer ey";
        while let Some(idx) = sanitized.find(bearer_pattern) {
            let end_idx = sanitized[idx..]
                .find(|c: char| c.is_whitespace() || c == '"' || c == ',')
                .map(|off| idx + off)
                .unwrap_or(sanitized.len());
            sanitized.replace_range(idx..end_idx, "Bearer [REDACTED-JWT]");
        }

        // 5. Redact raw email addresses
        if sanitized.contains('@') && sanitized.contains('.') {
            let parts: Vec<&str> = sanitized.split_whitespace().collect();
            let mut rebuilt = Vec::new();
            for word in parts {
                if word.contains('@') && word.contains('.') {
                    rebuilt.push("[REDACTED-EMAIL]");
                } else {
                    rebuilt.push(word);
                }
            }
            sanitized = rebuilt.join(" ");
        }

        sanitized
    }

    /// Computes deterministic standard SHA-256 digest of payload for traceable provenance (P06, P20).
    pub fn compute_sha256_digest(content: &str) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        format!("sha256:{}", hex::encode(hasher.finalize()))
    }

    /// Exports redacted metrics in structured JSON format.
    pub fn export_redacted_json(&self) -> String {
        serde_json::to_string_pretty(self).unwrap_or_else(|_| "{}".to_string())
    }

    /// Exports redacted metrics in canonical TOON format.
    pub fn export_redacted_toon(&self) -> String {
        let mut out = String::new();
        out.push_str("metrics:\n");
        out.push_str(&format!("  total_samples: {}\n", self.total_samples()));
        out.push_str(&format!("  route_samples: {}\n", self.count_by_class(MetricClass::Route)));
        out.push_str(&format!("  status_samples: {}\n", self.count_by_class(MetricClass::Status)));
        out.push_str(&format!("  durable_samples: {}\n", self.count_by_class(MetricClass::DurableSubmit)));
        out.push_str(&format!("  warm_route_p99_ms: {}\n", self.warm_p99_ms(MetricClass::Route)));
        out.push_str(&format!("  warm_status_p99_ms: {}\n", self.warm_p99_ms(MetricClass::Status)));
        out.push_str(&format!("  durable_ack_p99_ms: {}\n", self.warm_p99_ms(MetricClass::DurableSubmit)));
        out.push_str(&format!("  cold_first_route_ms: {}\n", self.cold_first_route_ms()));
        out.push_str(&format!("  steady_rss_mib: {}\n", self.steady_rss_mib()));
        out
    }
}
