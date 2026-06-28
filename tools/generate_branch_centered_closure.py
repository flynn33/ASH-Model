#!/usr/bin/env python
"""Generate/verify R-016 branch-centered closure validation artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ash_model.branch_centered_closure import (  # noqa: E402
    branch_centered_model_card,
    verify_branch_centered_closure,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".", help="Repository root")
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Exit nonzero if the formal closure verifier does not pass",
    )
    args = parser.parse_args()

    root = Path(args.out_root)
    result = {
        "closure": verify_branch_centered_closure(root),
        "model_card": branch_centered_model_card(root),
    }
    out_dir = (
        root
        / "validation"
        / "branch-centered-closure"
        / "roadmap-016"
        / "outputs"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "runtime_verification.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.require_pass and not result["closure"]["closed_formal_candidate"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
