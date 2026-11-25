#!/usr/bin/env bash
# ast_packer.sh — Pure bash AST-like codebase indexer
# Produces a compact project skeleton for token-efficient understanding
# Usage: ./ast_packer.sh /path/to/project > .sovereign/ast_index.md
#
# Zero dependencies — pure bash + standard POSIX utilities

set -euo pipefail

PROJECT_ROOT="${1:-.}"
PROJECT_NAME=$(basename "$(cd "$PROJECT_ROOT" && pwd)")

# Configuration
MAX_DEPTH=6
IGNORE_DIRS=".git|node_modules|__pycache__|.venv|venv|dist|build|.next|coverage|.sovereign"
CODE_EXTENSIONS="py|ts|tsx|js|jsx|go|rs|java|rb|sh|sql|yaml|yml|json|toml|md"

echo "# AST Index: ${PROJECT_NAME}"
echo ""
echo "> Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "> Source: ${PROJECT_ROOT}"
echo ""

# ─── Section 1: File Tree ────────────────────────────────────────────
echo "## File Tree"
echo '```'
find "$PROJECT_ROOT" -maxdepth "$MAX_DEPTH" \
  -not -path '*/.git/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.venv/*' \
  -not -path '*/venv/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/.next/*' \
  -not -path '*/coverage/*' \
  -not -path '*/.sovereign/*' \
  -type f \
  | sed "s|^$PROJECT_ROOT/||" \
  | sort \
  | head -200
echo '```'
echo ""

# ─── Section 2: Size Summary ─────────────────────────────────────────
echo "## Size Summary"
echo '```'
echo "Total files: $(find "$PROJECT_ROOT" -type f -not -path '*/.git/*' -not -path '*/node_modules/*' | wc -l)"
echo "Total size: $(du -sh "$PROJECT_ROOT" 2>/dev/null | cut -f1)"
echo ""
echo "By extension:"
find "$PROJECT_ROOT" -type f -not -path '*/.git/*' -not -path '*/node_modules/*' \
  | sed 's/.*\.//' \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -15
echo '```'
echo ""

# ─── Section 3: Function/Class Signatures ────────────────────────────
echo "## Code Signatures"

# Python signatures
PY_FILES=$(find "$PROJECT_ROOT" -name "*.py" -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' 2>/dev/null)
if [ -n "$PY_FILES" ]; then
  echo ""
  echo "### Python"
  echo '```python'
  echo "$PY_FILES" | while read -r f; do
    rel=$(echo "$f" | sed "s|^$PROJECT_ROOT/||")
    sigs=$(grep -nE '^\s*(def |class |async def )' "$f" 2>/dev/null || true)
    if [ -n "$sigs" ]; then
      echo "# --- $rel ---"
      echo "$sigs" | head -20
    fi
  done
  echo '```'
fi

# TypeScript/JavaScript signatures
TS_FILES=$(find "$PROJECT_ROOT" \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/dist/*' 2>/dev/null)
if [ -n "$TS_FILES" ]; then
  echo ""
  echo "### TypeScript/JavaScript"
  echo '```typescript'
  echo "$TS_FILES" | while read -r f; do
    rel=$(echo "$f" | sed "s|^$PROJECT_ROOT/||")
    sigs=$(grep -nE '^\s*(export |function |const |class |interface |type |async function |enum )' "$f" 2>/dev/null | grep -vE '^\s*//' || true)
    if [ -n "$sigs" ]; then
      echo "// --- $rel ---"
      echo "$sigs" | head -20
    fi
  done
  echo '```'
fi

# Go signatures
GO_FILES=$(find "$PROJECT_ROOT" -name "*.go" -not -path '*/.git/*' -not -path '*/vendor/*' 2>/dev/null)
if [ -n "$GO_FILES" ]; then
  echo ""
  echo "### Go"
  echo '```go'
  echo "$GO_FILES" | while read -r f; do
    rel=$(echo "$f" | sed "s|^$PROJECT_ROOT/||")
    sigs=$(grep -nE '^\s*(func |type |var |const )' "$f" 2>/dev/null || true)
    if [ -n "$sigs" ]; then
      echo "// --- $rel ---"
      echo "$sigs" | head -20
    fi
  done
  echo '```'
fi

# Rust signatures
RS_FILES=$(find "$PROJECT_ROOT" -name "*.rs" -not -path '*/.git/*' -not -path '*/target/*' 2>/dev/null)
if [ -n "$RS_FILES" ]; then
  echo ""
  echo "### Rust"
  echo '```rust'
  echo "$RS_FILES" | while read -r f; do
    rel=$(echo "$f" | sed "s|^$PROJECT_ROOT/||")
    sigs=$(grep -nE '^\s*(pub |fn |struct |enum |trait |impl |mod |use )' "$f" 2>/dev/null || true)
    if [ -n "$sigs" ]; then
      echo "// --- $rel ---"
      echo "$sigs" | head -20
    fi
  done
  echo '```'
fi

echo ""

# ─── Section 4: Dependencies ─────────────────────────────────────────
echo "## Dependencies"

# package.json
if [ -f "$PROJECT_ROOT/package.json" ]; then
  echo ""
  echo "### Node.js (package.json)"
  echo '```json'
  grep -A 50 '"dependencies"' "$PROJECT_ROOT/package.json" 2>/dev/null | head -30 || echo "No dependencies found"
  echo '```'
fi

# requirements.txt
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  echo ""
  echo "### Python (requirements.txt)"
  echo '```'
  cat "$PROJECT_ROOT/requirements.txt" | head -30
  echo '```'
fi

# pyproject.toml
if [ -f "$PROJECT_ROOT/pyproject.toml" ]; then
  echo ""
  echo "### Python (pyproject.toml)"
  echo '```toml'
  grep -A 20 '\[project\]' "$PROJECT_ROOT/pyproject.toml" 2>/dev/null | head -25 || echo "No project section"
  echo '```'
fi

# go.mod
if [ -f "$PROJECT_ROOT/go.mod" ]; then
  echo ""
  echo "### Go (go.mod)"
  echo '```'
  cat "$PROJECT_ROOT/go.mod" | head -20
  echo '```'
fi

# Cargo.toml
if [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
  echo ""
  echo "### Rust (Cargo.toml)"
  echo '```toml'
  grep -A 20 '\[dependencies\]' "$PROJECT_ROOT/Cargo.toml" 2>/dev/null | head -25 || echo "No dependencies section"
  echo '```'
fi

echo ""

# ─── Section 5: TODOs and FIXMEs ─────────────────────────────────────
echo "## TODOs / FIXMEs"
echo '```'
grep -rn "TODO\|FIXME\|HACK\|XXX\|WORKAROUND" "$PROJECT_ROOT" \
  --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --include="*.go" --include="*.rs" --include="*.java" \
  2>/dev/null \
  | grep -v 'node_modules\|.git\|__pycache__\|venv\|dist' \
  | sed "s|^$PROJECT_ROOT/||" \
  | head -20 \
  || echo "None found"
echo '```'

echo ""
echo "---"
echo "> Token-efficient index. ~2KB per 1000 LOC. Use instead of reading full files."
