#!/usr/bin/env bash
# AWS MCP Server launcher (api, docs, iac)
# Auth: inherits from `aws sso login` — credentials live in ~/.aws/login, SDK picks them up automatically.
# AWS_PROFILE and AWS_DEFAULT_REGION are set here for explicitness; the SDK also reads ~/.aws/config.
set -euo pipefail

export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-us-east-1}"
# AWS_PROFILE is not set because the CLI uses login-session auth, not a named profile.

SERVER="${1:-api}"
shift || true

case "$SERVER" in
  api)
    exec uvx awslabs.aws-api-mcp-server@latest "$@"
    ;;
  docs)
    exec uvx awslabs.aws-documentation-mcp-server@latest "$@"
    ;;
  iac)
    exec uvx awslabs.aws-iac-mcp-server@latest "$@"
    ;;
  *)
    echo "Usage: $0 [api|docs|iac]" >&2
    exit 1
    ;;
esac
