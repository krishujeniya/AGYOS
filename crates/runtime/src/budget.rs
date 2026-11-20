//! Context Token and Financial Budget Ledger with 20% Recovery Reserve.
//!
//! Complies with Principle P32 (Operator-Owned Budgets) and P22 (Measured Context Retrieval).
//!
//! Production Ceilings per TaskContract:
//! - Tokens: 30,000 max (6,000 reserved for verification/recovery, 24,000 spendable)
//! - Money: $1.50 max ($0.30 reserved for verification/recovery, $1.20 spendable)
//! - Duration: 600s max (120s reserved, 480s spendable)
//! - Tool Calls: 40 max (8 reserved, 32 spendable)
//! - Retries: 2 max

use domain::{DomainError, FixedMoney};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContextBudget {
    pub max_tokens: u32,
    pub allocated_tokens: u32,
    pub max_money: FixedMoney,
    pub spent_money: FixedMoney,
    pub max_duration_s: u64,
    pub max_tool_calls: u32,
    pub used_tool_calls: u32,
    pub max_retries: u32,
    pub used_retries: u32,
    pub recovery_reserve_pct: u32, // Default 20
}

impl ContextBudget {
    /// Create standard TaskContract ceiling budget with 20% mandatory reserve.
    pub fn default_contract_ceiling() -> Self {
        Self {
            max_tokens: 30_000,
            allocated_tokens: 0,
            max_money: FixedMoney::from_micros(1_500_000), // $1.50
            spent_money: FixedMoney::ZERO,
            max_duration_s: 600,
            max_tool_calls: 40,
            used_tool_calls: 0,
            max_retries: 2,
            used_retries: 0,
            recovery_reserve_pct: 20,
        }
    }

    /// Untouchable recovery token reserve (20% of max tokens = 6,000).
    pub fn token_recovery_reserve(&self) -> u32 {
        (self.max_tokens * self.recovery_reserve_pct) / 100
    }

    /// Spendable token limit before eating into recovery reserve.
    pub fn spendable_token_limit(&self) -> u32 {
        self.max_tokens.saturating_sub(self.token_recovery_reserve())
    }

    /// Remaining available spendable tokens.
    pub fn available_tokens(&self) -> u32 {
        self.spendable_token_limit().saturating_sub(self.allocated_tokens)
    }

    /// Attempt to allocate tokens for LLM generation or context injection.
    /// Fails immediately if attempting to breach the 20% recovery reserve.
    pub fn allocate_tokens(&mut self, tokens: u32) -> Result<(), DomainError> {
        let available = self.available_tokens();
        if tokens > available {
            return Err(DomainError::BudgetExceeded {
                requested: FixedMoney::from_micros(tokens as i64),
                available: FixedMoney::from_micros(available as i64),
            });
        }
        self.allocated_tokens += tokens;
        Ok(())
    }

    /// Untouchable recovery money reserve (20% of $1.50 = $0.30).
    pub fn money_recovery_reserve(&self) -> FixedMoney {
        FixedMoney::from_micros((self.max_money.as_micros() * self.recovery_reserve_pct as i64) / 100)
    }

    /// Spendable money limit.
    pub fn spendable_money_limit(&self) -> FixedMoney {
        self.max_money - self.money_recovery_reserve()
    }

    /// Spendable tool call limit (32 calls).
    pub fn spendable_tool_call_limit(&self) -> u32 {
        self.max_tool_calls - (self.max_tool_calls * self.recovery_reserve_pct / 100)
    }

    /// Increment tool call count.
    pub fn record_tool_call(&mut self) -> Result<(), DomainError> {
        let limit = self.spendable_tool_call_limit();
        if self.used_tool_calls >= limit {
            return Err(DomainError::BudgetExceeded {
                requested: FixedMoney::from_micros(self.used_tool_calls as i64 + 1),
                available: FixedMoney::from_micros(limit as i64),
            });
        }
        self.used_tool_calls += 1;
        Ok(())
    }
}

pub struct TokenSavingsEvaluator;

impl TokenSavingsEvaluator {
    /// Calculate percentage token savings of progressive TOON retrieval vs raw monolithic context.
    /// Formula: (raw - toon) / raw * 100%
    pub fn calculate_savings_percentage(raw_context_tokens: usize, toon_shortlist_tokens: usize) -> f64 {
        if raw_context_tokens == 0 {
            return 0.0;
        }
        if toon_shortlist_tokens >= raw_context_tokens {
            return 0.0;
        }
        let saved = raw_context_tokens - toon_shortlist_tokens;
        (saved as f64 / raw_context_tokens as f64) * 100.0
    }

    /// Verify whether a run satisfies the minimum 20% token savings threshold (Principle P22).
    pub fn satisfies_p22_threshold(raw_context_tokens: usize, toon_shortlist_tokens: usize) -> bool {
        Self::calculate_savings_percentage(raw_context_tokens, toon_shortlist_tokens) >= 20.0
    }
}
