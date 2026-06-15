#!/usr/bin/env bash
set -euo pipefail

branch="$(git branch --show-current)"
if [[ "$branch" != "Skir" ]]; then
  echo "Expected branch Skir, got $branch"
  exit 1
fi

if [[ -z "$(git log --oneline main..Skir)" ]]; then
  echo "Skir has no commits ahead of main"
  exit 1
fi

if [[ -z "$(git diff --stat main...Skir)" ]]; then
  echo "Skir diff against main is empty"
  exit 1
fi

python tools/verify_branch.py --required-only
python -m pytest
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/verify_branch.py

if [[ ! -f reports/skir-completion-report.md ]]; then
  echo "Missing reports/skir-completion-report.md"
  exit 1
fi

echo "Final gate passed."
