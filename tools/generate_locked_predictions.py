#!/usr/bin/env python
"""Verify and emit R-015 locked prediction validation artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ash_model.locked_predictions import write_verification  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root", default=".", help="repository root containing R-015 locked artifacts")
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="exit nonzero if lock verification fails",
    )
    args = parser.parse_args()

    result = write_verification(args.out_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.require_pass and not result["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
