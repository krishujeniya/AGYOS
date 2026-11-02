#!/usr/bin/env bash
# test-env.sh — Installs necessary dependencies for local ANCHOR testing
set -euo pipefail

echo "🔧 Installing ANCHOR test dependencies..."

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y jq bats shellcheck
  echo "✅ Dependencies installed via apt."
elif command -v brew >/dev/null 2>&1; then
  brew install jq bats-core shellcheck
  echo "✅ Dependencies installed via Homebrew."
else
  echo "❌ Unsupported package manager. Please manually install: jq, bats, shellcheck."
  exit 1
fi
