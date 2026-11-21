//! Fast Canonical Encoder for Token-Oriented Object Notation (TOON).
//!
//! Enforces:
//! - Deterministic alphabetical key ordering in maps
//! - Minimal escaping with literal UTF-8 preservation
//! - Consistent tabular encoding for arrays of uniform records

use std::fmt::Write;
use crate::error::ToonError;
use crate::model::ToonValue;
use serde_json::Value;

fn string_needs_quotes(s: &str) -> bool {
    if s.is_empty()
        || s.starts_with(' ')
        || s.ends_with(' ')
        || s.starts_with('-')
        || s.starts_with('+')
        || s.starts_with('.')
        || s.contains(',')
        || s.contains(':')
        || s.contains('"')
        || s.contains('\'')
        || s.contains('\n')
        || s.contains('\r')
        || s.contains('\t')
        || s.contains('[')
        || s.contains(']')
        || s.contains('{')
        || s.contains('}')
        || s.contains('#')
        || s.contains('\\')
    {
        return true;
    }

    if s.eq_ignore_ascii_case("true")
        || s.eq_ignore_ascii_case("false")
        || s.eq_ignore_ascii_case("null")
        || s.eq_ignore_ascii_case("none")
        || s.eq_ignore_ascii_case("nan")
        || s.eq_ignore_ascii_case("inf")
        || s.eq_ignore_ascii_case("-inf")
        || s.eq_ignore_ascii_case("infinity")
        || s.eq_ignore_ascii_case("-infinity")
    {
        return true;
    }

    if s.parse::<i64>().is_ok() || s.parse::<f64>().is_ok() {
        return true;
    }

    if s.chars().all(|c| c.is_ascii_digit() || c == '-' || c == '.' || c == '+' || c == 'e' || c == 'E') {
        return true;
    }

    false
}

/// Format a single scalar value.
pub fn format_scalar(val: &ToonValue) -> String {
    match val {
        ToonValue::Null => "null".to_string(),
        ToonValue::Bool(b) => if *b { "true".to_string() } else { "false".to_string() },
        ToonValue::Int(i) => i.to_string(),
        ToonValue::Float(f) => {
            if f.fract() == 0.0 {
                format!("{:.1}", f)
            } else {
                f.to_string()
            }
        }
        ToonValue::String(s) => {
            if string_needs_quotes(s) {
                serde_json::to_string(s).unwrap_or_else(|_| format!("\"{}\"", s))
            } else {
                s.clone()
            }
        }
        _ => "".to_string(),
    }
}

/// Canonical TOON encoder.
pub fn encode(val: &ToonValue) -> Result<String, ToonError> {
    let mut out = String::new();
    encode_value(val, 0, &mut out)?;
    if out.ends_with('\n') {
        out.pop();
    }
    Ok(out)
}

fn encode_value(val: &ToonValue, depth: usize, out: &mut String) -> Result<(), ToonError> {
    let indent = "  ".repeat(depth);

    match val {
        ToonValue::Null | ToonValue::Bool(_) | ToonValue::Int(_) | ToonValue::Float(_) | ToonValue::String(_) => {
            let _ = writeln!(out, "{}{}", indent, format_scalar(val));
        }
        ToonValue::Array(items) => {
            for item in items {
                match item {
                    ToonValue::Map(_) => {
                        let _ = write!(out, "{}- ", indent);
                        encode_value(item, depth + 1, out)?;
                    }
                    _ => {
                        let _ = writeln!(out, "{}- {}", indent, format_scalar(item));
                    }
                }
            }
        }
        ToonValue::Map(entries) => {
            // Sort keys alphabetically for canonical determinism
            let mut sorted = entries.clone();
            sorted.sort_by(|a, b| a.0.cmp(&b.0));

            for (k, v) in &sorted {
                match v {
                    ToonValue::Map(sub_entries) => {
                        let _ = writeln!(out, "{}{}:", indent, k);
                        let sub_val = ToonValue::Map(sub_entries.clone());
                        encode_value(&sub_val, depth + 1, out)?;
                    }
                    ToonValue::Array(items) => {
                        let count = items.len();
                        let _ = writeln!(out, "{}{}[{}]:", indent, k, count);
                        let sub_arr = ToonValue::Array(items.clone());
                        encode_value(&sub_arr, depth + 1, out)?;
                    }
                    _ => {
                        let _ = writeln!(out, "{}{}: {}", indent, k, format_scalar(v));
                    }
                }
            }
        }
    }
    Ok(())
}

/// Backward-compatible tabular records encoder.
pub fn encode_records(
    records: &[serde_json::Map<String, Value>],
    key_name: &str,
    inline_schema: bool,
) -> String {
    if records.is_empty() {
        return format!("{}[0]:\n  - (empty)", key_name);
    }

    let mut columns: Vec<String> = Vec::new();
    for rec in records {
        for key in rec.keys() {
            if !columns.contains(key) {
                columns.push(key.clone());
            }
        }
    }
    columns.sort();

    let mut out = String::with_capacity(records.len() * columns.len() * 16);
    let count = records.len();

    if inline_schema {
        let _ = writeln!(out, "{}[{}]{{{}}}:", key_name, count, columns.join(", "));
    } else {
        let _ = writeln!(out, "{}[{}]:", key_name, count);
        let _ = writeln!(out, "  - {}", columns.join(", "));
    }

    for rec in records {
        let mut row_vals: Vec<String> = Vec::with_capacity(columns.len());
        for col in &columns {
            let val = rec.get(col).unwrap_or(&Value::Null);
            let toon_val = ToonValue::from_json(val);
            row_vals.push(format_scalar(&toon_val));
        }
        let _ = writeln!(out, "  - {}", row_vals.join(", "));
    }

    if out.ends_with('\n') {
        out.pop();
    }
    out
}

pub fn encode_json_array(array: &[Value], key_name: &str) -> Result<String, String> {
    let mut maps: Vec<serde_json::Map<String, Value>> = Vec::with_capacity(array.len());
    for item in array {
        match item {
            Value::Object(m) => maps.push(m.clone()),
            _ => return Err("TOON tabular encoding requires an array of objects".to_string()),
        }
    }
    Ok(encode_records(&maps, key_name, false))
}
