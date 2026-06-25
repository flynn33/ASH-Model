#!/usr/bin/env python3
"""Reject commits authored or committed by restricted contributor identities."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass


ZERO_SHA = "0" * 40


def _join(*parts: str) -> str:
    return "".join(parts)


RESTRICTED_NAMES = frozenset(
    item.lower()
    for item in (
        "github-actions[bot]",
        _join("co", "pilot-swe-", "agent[bot]"),
    )
)
RESTRICTED_EMAILS = frozenset(
    item.lower()
    for item in (
        "41898282+github-actions[bot]@users.noreply.github.com",
        _join("198982749+", "Co", "pilot", "@users.noreply.github.com"),
    )
)


@dataclass(frozen=True)
class CommitMetadata:
    commit: str
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    message: str


@dataclass(frozen=True)
class Violation:
    commit: str
    field: str


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def commit_range(base: str, head: str) -> list[str]:
    if not head:
        raise ValueError("head revision is required")
    if not base or base == ZERO_SHA:
        return run_git(["rev-list", head]).splitlines()
    return run_git(["rev-list", f"{base}..{head}"]).splitlines()


def read_metadata(commit: str) -> CommitMetadata:
    output = run_git(
        [
            "log",
            "--format=%H%x00%an%x00%ae%x00%cn%x00%ce%x00%B",
            "-n",
            "1",
            commit,
        ]
    )
    parts = output.split("\0", 5)
    if len(parts) != 6:
        raise ValueError(f"unexpected git log format for commit {commit}")
    return CommitMetadata(*parts)


def is_restricted_identity(name: str, email: str) -> bool:
    return name.lower() in RESTRICTED_NAMES or email.lower() in RESTRICTED_EMAILS


def restricted_coauthor_line(line: str) -> bool:
    lowered = line.lower()
    if not lowered.startswith("co-authored-by:"):
        return False
    return any(name in lowered for name in RESTRICTED_NAMES) or any(
        email in lowered for email in RESTRICTED_EMAILS
    )


def scan_commit(metadata: CommitMetadata) -> list[Violation]:
    violations: list[Violation] = []
    checks = (
        ("author", metadata.author_name, metadata.author_email),
        ("committer", metadata.committer_name, metadata.committer_email),
    )
    for field, name, email in checks:
        if is_restricted_identity(name, email):
            violations.append(Violation(metadata.commit, field))
    for line in metadata.message.splitlines():
        if restricted_coauthor_line(line):
            violations.append(Violation(metadata.commit, "co-author"))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="", help="Base revision for the scan.")
    parser.add_argument("--head", required=True, help="Head revision for the scan.")
    args = parser.parse_args()

    violations: list[Violation] = []
    commits = commit_range(args.base, args.head)
    for commit in commits:
        violations.extend(scan_commit(read_metadata(commit)))

    if violations:
        print("Restricted contributor identity detected.")
        for violation in violations:
            print(f"- {violation.commit[:12]}: restricted {violation.field}")
        return 1

    print(f"Contributor identity check passed for {len(commits)} commits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
