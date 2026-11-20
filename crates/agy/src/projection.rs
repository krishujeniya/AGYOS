//! Canonical TOON to AGY Workspace Projection Engine.
//!
//! Complies with Principle P29 (Progressive Disclosure) and
//! Build Rule (Strictly zero tracked .md in git; runtime projections live outside git).

use std::collections::HashSet;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ProjectionError {
    InvalidToon(String),
    MissingField(String),
    SlugCollision(String),
}

impl fmt::Display for ProjectionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ProjectionError::InvalidToon(msg) => write!(f, "Invalid TOON for projection: {}", msg),
            ProjectionError::MissingField(msg) => write!(f, "Missing field in TOON: {}", msg),
            ProjectionError::SlugCollision(slug) => write!(f, "Flat slug collision detected: {}", slug),
        }
    }
}

impl std::error::Error for ProjectionError {}

pub struct ProjectionEngine {
    registered_slugs: HashSet<String>,
}

impl ProjectionEngine {
    pub fn new() -> Self {
        Self {
            registered_slugs: HashSet::new(),
        }
    }

    /// Register slug with flat collision detection.
    pub fn register_slug(&mut self, slug: &str) -> Result<(), ProjectionError> {
        if self.registered_slugs.contains(slug) {
            return Err(ProjectionError::SlugCollision(slug.to_string()));
        }
        self.registered_slugs.insert(slug.to_string());
        Ok(())
    }

    /// Project a canonical TOON skill into markdown for AGY consumption.
    pub fn project_skill_markdown(&mut self, toon_content: &str) -> Result<(String, String), ProjectionError> {
        let mut id = String::new();
        let mut intent = String::new();
        let mut risk = "R0".to_string();

        for line in toon_content.lines() {
            let trimmed = line.trim();
            if let Some(val) = trimmed.strip_prefix("id:") {
                id = val.trim().trim_matches('"').to_string();
            } else if let Some(val) = trimmed.strip_prefix("intent:") {
                intent = val.trim().trim_matches('"').to_string();
            } else if let Some(val) = trimmed.strip_prefix("risk_level:") {
                risk = val.trim().trim_matches('"').to_string();
            }
        }

        if id.is_empty() {
            return Err(ProjectionError::MissingField("id".to_string()));
        }

        self.register_slug(&id)?;

        let markdown = format!(
            "---\nname: {}\ndescription: {}\nrisk_level: {}\n---\n\n# {}\n\n{}\n",
            id, intent, risk, id, intent
        );

        Ok((id, markdown))
    }

    /// Project a canonical TOON rule into markdown rule for AGY consumption.
    pub fn project_rule_markdown(&self, toon_content: &str) -> Result<String, ProjectionError> {
        let mut title = "Operating Policy".to_string();
        for line in toon_content.lines() {
            let trimmed = line.trim();
            if let Some(val) = trimmed.strip_prefix("name:") {
                title = val.trim().trim_matches('"').to_string();
                break;
            }
        }

        let mut body = String::new();
        body.push_str(&format!("# {}\n\n", title));
        for line in toon_content.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with('-') {
                body.push_str(&format!("* {}\n", trimmed.trim_start_matches('-').trim().trim_matches('"')));
            }
        }

        Ok(body)
    }

    /// Project canonical TOON hooks manifest to hooks.json.
    pub fn project_hooks_json(&self, toon_content: &str) -> Result<String, ProjectionError> {
        let mut hooks = Vec::new();
        let mut current_name = String::new();
        let mut current_type = String::new();

        for line in toon_content.lines() {
            let trimmed = line.trim();
            if let Some(val) = trimmed.strip_prefix("- name:") {
                if !current_name.is_empty() {
                    hooks.push(serde_json::json!({
                        "name": current_name,
                        "type": current_type,
                    }));
                }
                current_name = val.trim().trim_matches('"').to_string();
            } else if let Some(val) = trimmed.strip_prefix("type:") {
                current_type = val.trim().trim_matches('"').to_string();
            }
        }

        if !current_name.is_empty() {
            hooks.push(serde_json::json!({
                "name": current_name,
                "type": current_type,
            }));
        }

        serde_json::to_string_pretty(&serde_json::json!({ "hooks": hooks }))
            .map_err(|e| ProjectionError::InvalidToon(e.to_string()))
    }

    /// Project canonical TOON MCP manifest to mcp_config.json.
    pub fn project_mcp_json(&self, toon_content: &str) -> Result<String, ProjectionError> {
        let mut server_name = "agyos-kernel".to_string();
        for line in toon_content.lines() {
            let trimmed = line.trim();
            if let Some(val) = trimmed.strip_prefix("- name:") {
                server_name = val.trim().trim_matches('"').to_string();
                break;
            }
        }

        let config = serde_json::json!({
            "mcpServers": {
                server_name: {
                    "command": "target/release/agyos",
                    "args": ["mcp-server"],
                    "env": {
                        "AGYOS_CONFINED": "true"
                    }
                }
            }
        });

        serde_json::to_string_pretty(&config)
            .map_err(|e| ProjectionError::InvalidToon(e.to_string()))
    }
}

impl Default for ProjectionEngine {
    fn default() -> Self {
        Self::new()
    }
}
