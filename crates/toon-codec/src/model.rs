//! TOON Canonical Data Model.

use serde_json::{Map, Number, Value};

#[derive(Debug, Clone, PartialEq)]
pub enum ToonValue {
    Null,
    Bool(bool),
    Int(i64),
    Float(f64),
    String(String),
    Array(Vec<ToonValue>),
    Map(Vec<(String, ToonValue)>),
}

impl ToonValue {
    pub fn is_null(&self) -> bool {
        matches!(self, ToonValue::Null)
    }

    pub fn as_str(&self) -> Option<&str> {
        match self {
            ToonValue::String(s) => Some(s),
            _ => None,
        }
    }

    pub fn as_i64(&self) -> Option<i64> {
        match self {
            ToonValue::Int(i) => Some(*i),
            _ => None,
        }
    }

    pub fn as_bool(&self) -> Option<bool> {
        match self {
            ToonValue::Bool(b) => Some(*b),
            _ => None,
        }
    }

    pub fn to_json(&self) -> Value {
        match self {
            ToonValue::Null => Value::Null,
            ToonValue::Bool(b) => Value::Bool(*b),
            ToonValue::Int(i) => Value::Number(Number::from(*i)),
            ToonValue::Float(f) => Number::from_f64(*f).map(Value::Number).unwrap_or(Value::Null),
            ToonValue::String(s) => Value::String(s.clone()),
            ToonValue::Array(arr) => Value::Array(arr.iter().map(|v| v.to_json()).collect()),
            ToonValue::Map(entries) => {
                let mut map = Map::with_capacity(entries.len());
                for (k, v) in entries {
                    map.insert(k.clone(), v.to_json());
                }
                Value::Object(map)
            }
        }
    }

    pub fn from_json(val: &Value) -> Self {
        match val {
            Value::Null => ToonValue::Null,
            Value::Bool(b) => ToonValue::Bool(*b),
            Value::Number(n) => {
                if let Some(i) = n.as_i64() {
                    ToonValue::Int(i)
                } else if let Some(f) = n.as_f64() {
                    ToonValue::Float(f)
                } else {
                    ToonValue::Null
                }
            }
            Value::String(s) => ToonValue::String(s.clone()),
            Value::Array(arr) => ToonValue::Array(arr.iter().map(Self::from_json).collect()),
            Value::Object(obj) => {
                let mut entries = Vec::with_capacity(obj.len());
                for (k, v) in obj {
                    entries.push((k.clone(), Self::from_json(v)));
                }
                ToonValue::Map(entries)
            }
        }
    }
}
