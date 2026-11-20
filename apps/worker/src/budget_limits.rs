//! Hosted Spending Limits & Token Rate Governance (Step 16).
//!
//! Complies with Step 16 finish criteria and Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P32 (Operator-Owned Budgets & Verification Reserves)

use domain::FixedMoney;
use serde::{Deserialize, Serialize};

/// Spending limit and token throughput controller.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpendingLimitController {
    max_authorized_spend: FixedMoney,
    accumulated_spend: FixedMoney,
    input_price_per_million: FixedMoney,
    output_price_per_million: FixedMoney,
    max_rpm: u32,
    max_input_tpm: u32,
    max_output_tpm: u32,
    current_rpm: u32,
    current_input_tpm: u32,
    current_output_tpm: u32,
}

impl SpendingLimitController {
    pub fn new(
        max_authorized_spend: FixedMoney,
        input_price_per_m: FixedMoney,
        output_price_per_m: FixedMoney,
    ) -> Self {
        Self {
            max_authorized_spend,
            accumulated_spend: FixedMoney::zero(),
            input_price_per_million: input_price_per_m,
            output_price_per_million: output_price_per_m,
            max_rpm: 6_000,
            max_input_tpm: 9_000_000,
            max_output_tpm: 1_800_000,
            current_rpm: 0,
            current_input_tpm: 0,
            current_output_tpm: 0,
        }
    }

    pub fn accumulated_spend(&self) -> FixedMoney {
        self.accumulated_spend
    }

    pub fn max_authorized_spend(&self) -> FixedMoney {
        self.max_authorized_spend
    }

    /// Calculates hourly cost according to Tracker.md capacity math:
    /// cost/hour = 540 * input_price + 108 * output_price (per million tokens)
    pub fn calculate_hourly_cost_at_50_jobs_per_sec(&self) -> FixedMoney {
        let input_cost = self.input_price_per_million.times(540);
        let output_cost = self.output_price_per_million.times(108);
        input_cost + output_cost
    }

    /// Evaluates if an operation's token reservation is permitted under spending ceiling.
    pub fn reserve_call(
        &mut self,
        input_tokens: u32,
        output_tokens: u32,
    ) -> Result<FixedMoney, String> {
        // Enforce rate limits
        if self.current_rpm + 1 > self.max_rpm {
            return Err("Rate limit exceeded: RPM cap reached".to_string());
        }
        if self.current_input_tpm + input_tokens > self.max_input_tpm {
            return Err("Rate limit exceeded: Input TPM cap reached".to_string());
        }
        if self.current_output_tpm + output_tokens > self.max_output_tpm {
            return Err("Rate limit exceeded: Output TPM cap reached".to_string());
        }

        // Calculate call cost in micros
        let in_micros = (input_tokens as u64 * self.input_price_per_million.micros()) / 1_000_000;
        let out_micros = (output_tokens as u64 * self.output_price_per_million.micros()) / 1_000_000;
        let call_cost = FixedMoney::from_micros(in_micros + out_micros);

        if self.accumulated_spend + call_cost > self.max_authorized_spend {
            return Err(format!(
                "Spending limit reached: authorized ${:.2}, current ${:.2}, requested ${:.4}",
                self.max_authorized_spend.dollars(),
                self.accumulated_spend.dollars(),
                call_cost.dollars()
            ));
        }

        self.current_rpm += 1;
        self.current_input_tpm += input_tokens;
        self.current_output_tpm += output_tokens;
        self.accumulated_spend = self.accumulated_spend + call_cost;

        Ok(call_cost)
    }

    /// Resets minute-window throughput counters.
    pub fn reset_window(&mut self) {
        self.current_rpm = 0;
        self.current_input_tpm = 0;
        self.current_output_tpm = 0;
    }
}
