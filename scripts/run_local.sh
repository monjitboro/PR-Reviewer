#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Please export OPENAI_API_KEY"
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Tip: export GITHUB_TOKEN if you want to post comments. Otherwise use --dry-run."
fi

python -m pr_reviewer.main "$@"
