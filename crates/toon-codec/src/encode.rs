//! Fast streaming encoder for Token-Oriented Object Notation (TOON).

use std::fmt::Write;
use serde_json::Value;

/// Format a single scalar value according to TOON rules.
pub fn format_scalar(val: &Value) -> String {
    match val {
        Value::Null => "null".to_string(),
        Value::Bool(b) => if *b { "true".to_string() } else { "false".to_string() },
        Value::Number(n) => n.to_string(),
        Value::String(s) => {
            // Quote string if it contains delimiter characters, newlines, or looks like a number/boolean
            if s.is_empty()
                || s.contains(',')
                || s.contains(':')
                || s.contains('"')
                || s.contains('\n')
                || s.contains('\r')
                || s.contains('\t')
                || s.contains('[')
                || s.contains(']')
                || s.contains('{')
                || s.contains('}')
                || s == "true"
                || s == "false"
                || s == "null"
                || s.chars().all(|c| c.is_ascii_digit() || c == '-' || c == '.')
            {
                serde_json::to_string(s).unwrap_or_else(|_| format!("\"{}\"", s))
            } else {
                s.clone()
            }
        }
        _ => serde_json::to_string(val).unwrap_or_default(),
    }
}

/// Encode a slice of JSON map records into canonical TOON tabular text.
pub fn encode_records(
    records: &[serde_json::Map<String, Value>],
    key_name: &str,
    inline_schema: bool,
) -> String {
    if records.is_empty() {
        return format!("{}[0]:\n  - (empty)", key_name);
    }

    // Determine deterministic columns from the keys of the first record (or union)
    let mut columns: Vec<String> = Vec::new();
    for rec in records {
        for key in rec.keys() {
            if !columns.contains(key) {
                columns.push(key.clone());
            }
        }
    }

    let mut out = String::with_capacity(records.len() * columns.len() * 16);
    let count = records.len();

    if inline_schema {
        // e.g. skills[2]{name, tier}:
        let _ = writeln!(out, "{}[{}]{{{}}}:", key_name, count, columns.join(", "));
    } else {
        // e.g. skills[2]:\n  - name, tier
        let _ = writeln!(out, "{}[{}]:", key_name, count);
        let _ = writeln!(out, "  - {}", columns.join(", "));
    }

    for rec in records {
        let mut row_vals: Vec<String> = Vec::with_capacity(columns.len());
        for col in &columns {
            let val = rec.get(col).unwrap_or(&Value::Null);
            row_vals.push(format_scalar(val));
        }
        let _ = writeln!(out, "  - {}", row_vals.join(", "));
    }

    // Strip trailing newline to return clean block
    if out.ends_with('\n') {
        out.pop();
    }
    out
}

/// Encode arbitrary JSON array of objects to TOON text.
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
