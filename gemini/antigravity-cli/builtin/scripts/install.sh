#!/usr/bin/env bash
# install.sh — One-line installer & ~/.gemini sync for AGYOS
set -euo pipefail

REPO_URL="${AGYOS_REPO_URL:-https://github.com/krishujeniya/AGYOS.git}"
BRANCH="${AGYOS_BRANCH:-main}"
TARGET_DIR="${AGYOS_GEMINI_DIR:-$HOME/.gemini}"
DRY_RUN=false
BACKUP=true

usage() {
  cat <<'EOF'
Usage: install.sh [--target DIR] [--dry-run] [--no-backup] [--yes]

Replaces/syncs ~/.gemini/{config,antigravity-cli} with AGYOS/gemini/.
Creates a timestamped backup of existing ~/.gemini unless --no-backup is set.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --no-backup)
      BACKUP=false
      shift
      ;;
    -y|--yes)
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

TMP_CLONE=""
cleanup() {
  if [[ -n "$TMP_CLONE" && -d "$TMP_CLONE" ]]; then
    rm -rf -- "$TMP_CLONE"
  fi
}
trap cleanup EXIT

SOURCE_GEMINI=""
if [[ -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  CANDIDATE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
  if [[ -d "$CANDIDATE/config" && -d "$CANDIDATE/antigravity-cli" ]]; then
    SOURCE_GEMINI="$CANDIDATE"
  fi
fi

if [[ -z "$SOURCE_GEMINI" ]]; then
  command -v git >/dev/null 2>&1 || { echo "Error: git is required for remote install" >&2; exit 1; }
  TMP_CLONE="$(mktemp -d "${TMPDIR:-/tmp}/agyos-install.XXXXXXXX")"
  echo "Cloning AGYOS ($BRANCH)..."
  git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TMP_CLONE" >/dev/null 2>&1
  SOURCE_GEMINI="$TMP_CLONE/gemini"
fi

echo "Source: $SOURCE_GEMINI"
echo "Target: $TARGET_DIR"

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] Would back up existing $TARGET_DIR (backup=$BACKUP) and sync config/ + antigravity-cli/."
  exit 0
fi

if [[ -e "$TARGET_DIR" && "$BACKUP" == "true" ]]; then
  BACKUP_DIR="${TARGET_DIR}.bak.$(date +%Y%m%d_%H%M%S)"
  echo "Backing up existing $TARGET_DIR -> $BACKUP_DIR"
  cp -a "$TARGET_DIR" "$BACKUP_DIR"
fi

mkdir -p "$TARGET_DIR/config" "$TARGET_DIR/antigravity-cli"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$SOURCE_GEMINI/config/" "$TARGET_DIR/config/"
  rsync -a --delete \
    --exclude 'brain/*' \
    --exclude 'conversations/*' \
    --exclude 'scratch/*' \
    --exclude 'cache/' \
    --exclude 'log/' \
    --exclude 'crashes/' \
    --exclude 'conversation_summaries.db*' \
    --exclude 'history.jsonl' \
    "$SOURCE_GEMINI/antigravity-cli/" "$TARGET_DIR/antigravity-cli/"
else
  rm -rf "$TARGET_DIR/config"
  cp -a "$SOURCE_GEMINI/config" "$TARGET_DIR/config"
  rm -rf "$TARGET_DIR/antigravity-cli/builtin" "$TARGET_DIR/antigravity-cli/bin" "$TARGET_DIR/antigravity-cli/mcp"
  cp -a "$SOURCE_GEMINI/antigravity-cli/." "$TARGET_DIR/antigravity-cli/"
fi

chmod +x "$TARGET_DIR/antigravity-cli/bin/"* 2>/dev/null || true
chmod +x "$TARGET_DIR/antigravity-cli/builtin/scripts/hooks/"*.py 2>/dev/null || true

if command -v agy >/dev/null 2>&1; then
  echo "Validating plugins with agy $(agy --version)..."
  for p in "$TARGET_DIR/config/plugins/"*; do
    agy plugin validate "$p" >/dev/null
  done
  echo "All plugins validated."
fi

echo "AGYOS installed into $TARGET_DIR"
