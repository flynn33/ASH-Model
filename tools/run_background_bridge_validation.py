#!/usr/bin/env python3
"""Run Pass 003 ASH background-bridge synthetic validation."""

from __future__ import annotations

import json
from pathlib import Path

from ash_model.background_bridge import run_validation


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "validation" / "background_bridge" / "pass_003" / "outputs"
    summary = run_validation(output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
