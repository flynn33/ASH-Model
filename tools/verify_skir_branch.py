#!/usr/bin/env python3
"""Verify that the Skir branch is substantively implemented."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

REQUIRED_FILES = [
    "src/ash_code.py",
    "tests/test_ash_code.py",
    "tools/audit_claims.py",
    "tools/run_simulation_controls.py",
    "tools/verify_skir_branch.py",
    "docs/canonical-code.md",
    "docs/falsification-and-controls.md",
    "docs/claim-language-policy.md",
    "docs/python-smoke-validation.md",
    ".github/workflows/skir-validation.yml",
    ".github/pull_request_template.md",
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--head", default="Skir")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    root = args.root.resolve()
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    if missing:
        return fail("missing required files: " + ", ".join(missing))

    log = run(["git", "log", "--oneline", f"{args.base}..{args.head}"])
    if log.returncode != 0:
        return fail("could not compare branch log:\n" + log.stdout)
    if not log.stdout.strip():
        return fail(f"{args.head} has no commits beyond {args.base}")

    diff = run(["git", "diff", "--stat", f"{args.base}...{args.head}"])
    if diff.returncode != 0:
        return fail("could not compute diff stat:\n" + diff.stdout)
    if not diff.stdout.strip():
        return fail(f"{args.head} diff against {args.base} is empty")

    print("PASS: Skir branch has required files and non-empty diff")
    print("Commits:")
    print(log.stdout.strip())
    print("Diff stat:")
    print(diff.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
