//! Legacy Envelope Import and Unpacking.
//!
//! Handles historical formats and envelopes:
//! - `text: "..."` text envelopes
//! - `header:` metadata envelopes
//! - `target:` destination envelopes
//! - `archive:` base64/hex payload archives

use crate::error::ToonError;
use crate::model::ToonValue;

#[derive(Debug, Clone, PartialEq)]
pub struct LegacyEnvelope {
    pub header: Option<ToonValue>,
    pub target: Option<String>,
    pub text_body: Option<String>,
    pub archive: Option<String>,
    pub extra_fields: Vec<(String, ToonValue)>,
}

pub fn unpack_legacy_envelope(val: &ToonValue) -> Result<LegacyEnvelope, ToonError> {
    match val {
        ToonValue::Map(entries) => {
            let mut envelope = LegacyEnvelope {
                header: None,
                target: None,
                text_body: None,
                archive: None,
                extra_fields: Vec::new(),
            };

            for (k, v) in entries {
                match k.as_str() {
                    "text" => {
                        if let ToonValue::String(s) = v {
                            envelope.text_body = Some(s.clone());
                        }
                    }
                    "header" => {
                        envelope.header = Some(v.clone());
                    }
                    "target" => {
                        if let ToonValue::String(s) = v {
                            if s.contains("../") || s.contains("..\\") {
                                return Err(ToonError::PathTraversalDetected(s.clone()));
                            }
                            envelope.target = Some(s.clone());
                        }
                    }
                    "archive" => {
                        if let ToonValue::String(s) = v {
                            envelope.archive = Some(s.clone());
                        }
                    }
                    _ => {
                        envelope.extra_fields.push((k.clone(), v.clone()));
                    }
                }
            }
            Ok(envelope)
        }
        _ => Err(ToonError::SyntaxError("Expected map for legacy envelope".into())),
    }
}
