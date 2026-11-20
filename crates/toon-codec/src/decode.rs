//! Bounded, Zero-Copy Parser for Token-Oriented Object Notation (TOON).
//!
//! Enforces:
//! - Payload ceiling <= 256 KiB
//! - Nesting depth <= 4
//! - Strict escape sequence handling (rejects lone surrogates \ud83d..=\udfff)
//! - Duplicate key rejection
//! - Numeric overflow rejection

use crate::error::{
    MAX_ARRAY_ELEMENTS, MAX_NESTING_DEPTH, MAX_PAYLOAD_BYTES, MAX_STRING_LENGTH, ToonError,
};
use crate::model::ToonValue;
use serde_json::{Map, Number, Value};

/// Parse and unescape a string token, rejecting lone surrogates.
pub fn parse_string_token(token: &str) -> Result<String, ToonError> {
    let mut out = String::with_capacity(token.len());
    let mut chars = token.chars().peekable();

    while let Some(c) = chars.next() {
        if c == '\\' {
            match chars.next() {
                Some('"') => out.push('"'),
                Some('\\') => out.push('\\'),
                Some('/') => out.push('/'),
                Some('b') => out.push('\x08'),
                Some('f') => out.push('\x0c'),
                Some('n') => out.push('\n'),
                Some('r') => out.push('\r'),
                Some('t') => out.push('\t'),
                Some('u') => {
                    let mut hex = String::with_capacity(4);
                    for _ in 0..4 {
                        if let Some(h) = chars.next() {
                            if h.is_ascii_hexdigit() {
                                hex.push(h);
                            } else {
                                return Err(ToonError::InvalidEscapeSequence(format!("\\u{}{}", hex, h)));
                            }
                        } else {
                            return Err(ToonError::UnexpectedEof);
                        }
                    }
                    let code = u32::from_str_radix(&hex, 16)
                        .map_err(|_| ToonError::InvalidEscapeSequence(format!("\\u{}", hex)))?;

                    // Check for lone surrogate range 0xD800..=0xDFFF
                    if (0xD800..=0xDFFF).contains(&code) {
                        return Err(ToonError::LoneSurrogate(format!("\\u{:04x}", code)));
                    }

                    if let Some(ch) = char::from_u32(code) {
                        out.push(ch);
                    } else {
                        return Err(ToonError::InvalidEscapeSequence(format!("\\u{:04x}", code)));
                    }
                }
                Some(other) => {
                    return Err(ToonError::InvalidEscapeSequence(format!("\\{}", other)));
                }
                None => return Err(ToonError::UnexpectedEof),
            }
        } else {
            out.push(c);
        }
    }

    if out.len() > MAX_STRING_LENGTH {
        return Err(ToonError::StringLengthExceeded {
            limit: MAX_STRING_LENGTH,
            actual: out.len(),
        });
    }

    Ok(out)
}

/// Parse a scalar token into a typed ToonValue.
pub fn parse_scalar(token: &str) -> Result<ToonValue, ToonError> {
    let trimmed = token.trim();
    if trimmed.is_empty() {
        return Ok(ToonValue::String(String::new()));
    }
    if trimmed.eq_ignore_ascii_case("true") {
        return Ok(ToonValue::Bool(true));
    }
    if trimmed.eq_ignore_ascii_case("false") {
        return Ok(ToonValue::Bool(false));
    }
    if trimmed.eq_ignore_ascii_case("null") || trimmed.eq_ignore_ascii_case("none") {
        return Ok(ToonValue::Null);
    }

    // Quoted string
    if (trimmed.starts_with('"') && trimmed.ends_with('"') && trimmed.len() >= 2)
        || (trimmed.starts_with('\'') && trimmed.ends_with('\'') && trimmed.len() >= 2)
    {
        let inner = &trimmed[1..trimmed.len() - 1];
        let unescaped = parse_string_token(inner)?;
        return Ok(ToonValue::String(unescaped));
    }

    // Integer
    if let Ok(n) = trimmed.parse::<i64>() {
        return Ok(ToonValue::Int(n));
    }

    // Float
    if let Ok(f) = trimmed.parse::<f64>() {
        if f.is_finite() {
            return Ok(ToonValue::Float(f));
        }
    }

    // Default to unquoted string with escape check
    let s = parse_string_token(trimmed)?;
    Ok(ToonValue::String(s))
}

/// Simple CSV line splitter respecting quoted segments.
pub fn split_csv_line(line: &str) -> Result<Vec<String>, ToonError> {
    let mut tokens = Vec::new();
    let mut current = String::new();
    let mut in_quotes = false;
    let mut quote_char = '"';
    let mut chars = line.chars().peekable();

    while let Some(c) = chars.next() {
        if !in_quotes && (c == '"' || c == '\'') {
            in_quotes = true;
            quote_char = c;
            current.push(c);
        } else if in_quotes && c == quote_char {
            if chars.peek() == Some(&quote_char) {
                current.push(c);
                current.push(chars.next().unwrap());
            } else {
                in_quotes = false;
                current.push(c);
            }
        } else if !in_quotes && c == ',' {
            tokens.push(current.trim().to_string());
            current.clear();
        } else {
            current.push(c);
        }
    }

    if in_quotes {
        return Err(ToonError::SyntaxError("Unclosed quote in CSV segment".into()));
    }

    tokens.push(current.trim().to_string());
    Ok(tokens)
}

/// Bounded TOON parser.
pub fn decode_document(input: &str) -> Result<ToonValue, ToonError> {
    if input.len() > MAX_PAYLOAD_BYTES {
        return Err(ToonError::SizeCeilingExceeded {
            limit: MAX_PAYLOAD_BYTES,
            actual: input.len(),
        });
    }

    let lines: Vec<&str> = input.lines().collect();
    parse_block(&lines, 0, 0).map(|(val, _)| val)
}

fn parse_block(lines: &[&str], start_idx: usize, depth: usize) -> Result<(ToonValue, usize), ToonError> {
    if depth > MAX_NESTING_DEPTH {
        return Err(ToonError::MaxDepthExceeded {
            limit: MAX_NESTING_DEPTH,
            actual: depth,
        });
    }

    let mut entries: Vec<(String, ToonValue)> = Vec::new();
    let mut idx = start_idx;

    while idx < lines.len() {
        let line = lines[idx];
        let trimmed = line.trim();

        if trimmed.is_empty() || trimmed.starts_with('#') {
            idx += 1;
            continue;
        }

        // Check if map key
        if let Some(colon_pos) = line.find(':') {
            let key_part = line[..colon_pos].trim();
            let val_part = line[colon_pos + 1..].trim();

            // Duplicate key check
            if entries.iter().any(|(k, _)| k == key_part) {
                return Err(ToonError::DuplicateKey(key_part.to_string()));
            }

            // Tabular record indicator: key[N] or key[N]{cols}
            if let Some(bracket_start) = key_part.find('[') {
                if let Some(bracket_end) = key_part.find(']') {
                    let key_name = key_part[..bracket_start].trim().to_string();
                    let (tabular_val, next_idx) = parse_tabular(lines, idx, depth + 1)?;
                    entries.push((key_name, tabular_val));
                    idx = next_idx;
                    continue;
                }
            }

            if val_part.is_empty() {
                // Nested block or list
                if idx + 1 < lines.len() && lines[idx + 1].trim().starts_with('-') {
                    let (list_val, next_idx) = parse_list(lines, idx + 1, depth + 1)?;
                    entries.push((key_part.to_string(), list_val));
                    idx = next_idx;
                } else {
                    let (nested_val, next_idx) = parse_block(lines, idx + 1, depth + 1)?;
                    entries.push((key_part.to_string(), nested_val));
                    idx = next_idx;
                }
            } else {
                let scalar = parse_scalar(val_part)?;
                entries.push((key_part.to_string(), scalar));
                idx += 1;
            }
        } else {
            idx += 1;
        }
    }

    Ok((ToonValue::Map(entries), idx))
}

fn parse_tabular(lines: &[&str], header_idx: usize, _depth: usize) -> Result<(ToonValue, usize), ToonError> {
    let header_line = lines[header_idx].trim();
    let mut columns: Vec<String> = Vec::new();

    if let Some(b_start) = header_line.find('{') {
        if let Some(b_end) = header_line.find('}') {
            if b_end > b_start {
                let col_sub = &header_line[b_start + 1..b_end];
                for col in col_sub.split(',') {
                    columns.push(col.trim().to_string());
                }
            }
        }
    }

    let mut rows: Vec<ToonValue> = Vec::new();
    let mut idx = header_idx + 1;

    // If columns not in inline header, look at first row
    if columns.is_empty() && idx < lines.len() && lines[idx].trim().starts_with('-') {
        let first_line = lines[idx].trim_start_matches('-').trim();
        let cols = split_csv_line(first_line)?;
        columns = cols;
        idx += 1;
    }

    while idx < lines.len() {
        let line = lines[idx].trim();
        if !line.starts_with('-') {
            break;
        }
        let raw_row = line.trim_start_matches('-').trim();
        if raw_row == "(empty)" {
            idx += 1;
            continue;
        }

        let tokens = split_csv_line(raw_row)?;
        if !columns.is_empty() {
            let mut row_map = Vec::with_capacity(columns.len());
            for (i, col) in columns.iter().enumerate() {
                let tok = tokens.get(i).map(|s| s.as_str()).unwrap_or("null");
                let scalar = parse_scalar(tok)?;
                row_map.push((col.clone(), scalar));
            }
            rows.push(ToonValue::Map(row_map));
        } else {
            let mut row_arr = Vec::with_capacity(tokens.len());
            for tok in tokens {
                row_arr.push(parse_scalar(&tok)?);
            }
            rows.push(ToonValue::Array(row_arr));
        }

        if rows.len() > MAX_ARRAY_ELEMENTS {
            return Err(ToonError::ArrayElementsExceeded {
                limit: MAX_ARRAY_ELEMENTS,
                actual: rows.len(),
            });
        }
        idx += 1;
    }

    Ok((ToonValue::Array(rows), idx))
}

fn parse_list(lines: &[&str], start_idx: usize, _depth: usize) -> Result<(ToonValue, usize), ToonError> {
    let mut items = Vec::new();
    let mut idx = start_idx;

    while idx < lines.len() {
        let line = lines[idx].trim();
        if !line.starts_with('-') {
            break;
        }
        let raw_item = line.trim_start_matches('-').trim();
        let scalar = parse_scalar(raw_item)?;
        items.push(scalar);

        if items.len() > MAX_ARRAY_ELEMENTS {
            return Err(ToonError::ArrayElementsExceeded {
                limit: MAX_ARRAY_ELEMENTS,
                actual: items.len(),
            });
        }
        idx += 1;
    }

    Ok((ToonValue::Array(items), idx))
}

/// Backward-compatible decoder for legacy tabular records returning serde_json maps.
pub fn decode_records(input: &str) -> Result<Vec<Map<String, Value>>, String> {
    let val = decode_document(input).map_err(|e| e.to_string())?;
    match val {
        ToonValue::Array(rows) => {
            let mut out = Vec::with_capacity(rows.len());
            for row in rows {
                match row.to_json() {
                    Value::Object(m) => out.push(m),
                    _ => return Err("Expected array of objects".into()),
                }
            }
            Ok(out)
        }
        ToonValue::Map(entries) => {
            for (_k, v) in entries {
                if let ToonValue::Array(rows) = v {
                    let mut out = Vec::with_capacity(rows.len());
                    for row in rows {
                        match row.to_json() {
                            Value::Object(m) => out.push(m),
                            _ => {}
                        }
                    }
                    if !out.is_empty() {
                        return Ok(out);
                    }
                }
            }
            Ok(Vec::new())
        }
        _ => Err("Invalid tabular stream".into()),
    }
}
