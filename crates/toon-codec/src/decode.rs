//! Zero-copy parser for Token-Oriented Object Notation (TOON) tabular streams.

use serde_json::{Map, Number, Value};

/// Parse a scalar string token into a typed serde_json::Value.
pub fn parse_scalar(token: &str) -> Value {
    let trimmed = token.trim();
    if trimmed.is_empty() {
        return Value::String(String::new());
    }
    if trimmed.eq_ignore_ascii_case("true") {
        return Value::Bool(true);
    }
    if trimmed.eq_ignore_ascii_case("false") {
        return Value::Bool(false);
    }
    if trimmed.eq_ignore_ascii_case("null") || trimmed.eq_ignore_ascii_case("none") {
        return Value::Null;
    }
    // Check if JSON-quoted string
    if (trimmed.starts_with('"') && trimmed.ends_with('"') && trimmed.len() >= 2)
        || (trimmed.starts_with('\'') && trimmed.ends_with('\'') && trimmed.len() >= 2)
    {
        if let Ok(parsed) = serde_json::from_str::<Value>(trimmed) {
            return parsed;
        }
        return Value::String(trimmed[1..trimmed.len() - 1].to_string());
    }
    // Integer
    if let Ok(n) = trimmed.parse::<i64>() {
        return Value::Number(Number::from(n));
    }
    // Float
    if let Ok(f) = trimmed.parse::<f64>() {
        if let Some(num) = Number::from_f64(f) {
            return Value::Number(num);
        }
    }
    // Default to string
    Value::String(trimmed.to_string())
}

/// Simple CSV line splitter that respects quoted strings.
pub fn split_csv_line(line: &str) -> Vec<String> {
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
            // Check for escaped quote ""
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
    tokens.push(current.trim().to_string());
    tokens
}

/// Decode a TOON tabular manifest block into a vector of JSON objects.
pub fn decode_records(input: &str) -> Result<Vec<Map<String, Value>>, String> {
    let lines: Vec<&str> = input.lines().map(|l| l.trim_end()).collect();
    if lines.is_empty() {
        return Ok(Vec::new());
    }

    let mut idx = 0;
    while idx < lines.len() && (lines[idx].trim().is_empty() || lines[idx].trim().starts_with('#')) {
        idx += 1;
    }
    if idx >= lines.len() {
        return Ok(Vec::new());
    }

    let header_line = lines[idx].trim();
    idx += 1;

    let mut columns: Vec<String> = Vec::new();

    // Check if inline columns exist: e.g. skills[N]{col1, col2}:
    if let Some(brace_start) = header_line.find('{') {
        if let Some(brace_end) = header_line.find('}') {
            if brace_end > brace_start {
                let cols_substr = &header_line[brace_start + 1..brace_end];
                columns = split_csv_line(cols_substr);
            }
        }
    }

    // If no inline columns, look at the next line starting with "  - "
    if columns.is_empty() {
        while idx < lines.len() {
            let line = lines[idx].trim();
            if line.is_empty() || line.starts_with('#') {
                idx += 1;
                continue;
            }
            if let Some(stripped) = line.strip_prefix("- ") {
                columns = split_csv_line(stripped);
                idx += 1;
                break;
            } else {
                return Err(format!("Expected column definition line, got: {}", line));
            }
        }
    }

    if columns.is_empty() {
        return Err("No columns found in TOON tabular definition".to_string());
    }

    let mut records: Vec<Map<String, Value>> = Vec::new();

    while idx < lines.len() {
        let line = lines[idx].trim();
        idx += 1;

        if line.is_empty() || line.starts_with('#') {
            continue;
        }

        if let Some(stripped) = line.strip_prefix("- ") {
            let tokens = split_csv_line(stripped);
            let mut map = Map::new();
            for (i, col) in columns.iter().enumerate() {
                let val = if i < tokens.len() {
                    parse_scalar(&tokens[i])
                } else {
                    Value::Null
                };
                map.insert(col.clone(), val);
            }
            records.push(map);
        } else {
            // Reached end of array rows
            break;
        }
    }

    Ok(records)
}
