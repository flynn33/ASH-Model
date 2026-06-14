#!/usr/bin/env python3
"""Verify that the Skir branch contains a complete implementation."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATHS = [
    "src/ash_code.py",
    "tests/test_ash_code.py",
    "tools/audit_claims.py",
    "tools/run_simulation_controls.py",
    "tools/verify_branch.py",
    "docs/skir-code-validation.md",
    "docs/falsification-and-controls.md",
    "reports/skir-completion-report.md",
    "scripts/local_precheck.sh",
    "scripts/final_gate.sh",
    ".github/pull_request_template.md",
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def verify_required_paths(failures: list[str]) -> None:
    for rel_path in REQUIRED_PATHS:
        require((REPO_ROOT / rel_path).exists(), f"missing required path: {rel_path}", failures)


def verify_branch_state(failures: list[str]) -> None:
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    require(branch == "Skir", f"expected branch Skir, got {branch!r}", failures)

    log = run(["git", "log", "--oneline", "main..Skir"])
    if log.returncode != 0:
        failures.append("could not compare Skir to main:\n" + log.stdout[-4000:])
    else:
        require(bool(log.stdout.strip()), "Skir has no commits ahead of main", failures)

    diff = run(["git", "diff", "--stat", "main...Skir"])
    if diff.returncode != 0:
        failures.append("could not compute Skir diff against main:\n" + diff.stdout[-4000:])
    else:
        require(bool(diff.stdout.strip()), "Skir diff against main is empty", failures)


def verify_commands(failures: list[str]) -> None:
    commands = [
        [sys.executable, "-m", "pytest"],
        [sys.executable, "tools/audit_claims.py"],
        [sys.executable, "tools/run_simulation_controls.py", "--quick"],
    ]

    for command in commands:
        result = run(command)
        if result.returncode != 0:
            failures.append(
                "command failed: "
                + " ".join(command)
                + "\n"
                + result.stdout[-4000:]
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--required-only", action="store_true")
    args = parser.parse_args(argv)

    failures: list[str] = []
    verify_required_paths(failures)

    if not args.required_only:
        verify_branch_state(failures)
        verify_commands(failures)

    if failures:
        print("Skir verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Skir verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
