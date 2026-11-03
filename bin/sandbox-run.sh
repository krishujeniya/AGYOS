#!/usr/bin/env bash
# sandbox-run.sh — Wrapper for executing untrusted code or tests
set -euo pipefail
# This is a stub for a sandbox wrapper. In a production environment,
# this should wrap the execution in bubblewrap (bwrap), firejail, or docker.

if [ "$#" -eq 0 ]; then
  echo "Usage: sandbox-run.sh <command...>"
  exit 1
fi

if command -v bwrap >/dev/null 2>&1; then
  echo "🛡️ ANCHOR SANDBOX: Executing command in bwrap isolated environment..."
  exec bwrap --unshare-all --tmpfs /tmp --ro-bind / / --dev /dev --proc /proc --ro-bind "$PWD" "$PWD" --new-session --cap-drop all -- "$@"
elif command -v firejail >/dev/null 2>&1; then
  echo "🛡️ ANCHOR SANDBOX: Executing command in firejail isolated environment..."
  exec firejail --quiet --net=none --private=. "$@"
elif command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  echo "🛡️ ANCHOR SANDBOX: Executing command in docker isolated environment..."
  exec docker run --rm -v "$PWD":"$PWD":ro -w "$PWD" --network none --read-only --cpus=1 --memory=512m --security-opt no-new-privileges:true ubuntu:22.04 "$@"
else
  if [ "${ANCHOR_ALLOW_UNSANDBOXED:-0}" != "1" ]; then
    echo "⚠️ NO SANDBOX AVAILABLE — execution blocked."
    echo "ANCHOR requires bwrap, firejail, or docker for sandbox isolation."
    echo "To execute directly on the host, set ANCHOR_ALLOW_UNSANDBOXED=1"
    exit 1
  fi
  echo "⚠️ NO SANDBOX AVAILABLE — ANCHOR_ALLOW_UNSANDBOXED=1 set. Executing directly."
  mkdir -p "$PWD/.agents/state"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) UNSANDBOXED EXECUTION: $*" >> "$PWD/.agents/state/audit.log"
  exec "$@"
fi
