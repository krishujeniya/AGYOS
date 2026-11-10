#!/usr/bin/env bash
# IBM Cloud token helper
# Fetches a fresh IAM Bearer token from ibmcloud CLI and prints it.
# Used by IBM MCP wrappers to inject auth without hard-coding credentials.
set -euo pipefail

TOKEN=$(ibmcloud iam oauth-tokens --output json 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); t=d.get('iam_token',''); print(t.split('Bearer ')[-1].strip())" 2>/dev/null)

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: ibmcloud not authenticated. Run 'ibmcloud login' first." >&2
  exit 1
fi

echo "$TOKEN"
