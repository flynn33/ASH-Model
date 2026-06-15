#!/usr/bin/env bash
set -euo pipefail

echo "== branch =="
git branch --show-current

echo "== required files =="
python tools/verify_branch.py --required-only

echo "== tests =="
python -m pytest

echo "== claim audit =="
python tools/audit_claims.py

echo "== simulation controls =="
python tools/run_simulation_controls.py --quick

echo "Local precheck passed."
