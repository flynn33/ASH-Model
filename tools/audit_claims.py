#!/usr/bin/env python3
"""Audit ASH documentation for Skir claim alignment."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

TEXT_EXTENSIONS = {".md", ".tex", ".txt", ".rst", ".json", ".py", ".yml", ".yaml"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "data", "figures"}

FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("positive doubly-even self-dual claim", re.compile(r"doubly[- ]even\s+self[- ]dual", re.I)),
    ("positive self-dual error-correcting claim", re.compile(r"self[- ]dual\s+error[- ]correct", re.I)),
    (
        "Hamming-bound simulation resilience claim",
        re.compile(
            r"resilien\w*\s+to\s+random\s+bit[- ]flip\s+noise\s+up\s+to\s+the\s+theoretical\s+Hamming\s+bound",
            re.I,
        ),
    ),
    (
        "embedded codes correct noise up to Hamming bound",
        re.compile(r"embedded\s+codes\s+correct\s+noise\s+up\s+to\s+the\s+theoretical\s+Hamming\s+bound", re.I),
    ),
    (
        "robust correction under random bit-flip noise without decoder",
        re.compile(r"robust\s+error\s+correction\s+under\s+random\s+bit[- ]flip\s+noise", re.I),
    ),
    ("unsupported rapid Gaussian convergence claim", re.compile(r"rapid\s+convergence\s+to\s+Gaussian", re.I)),
    ("unsupported ASH-specific Gaussian claim", re.compile(r"ASH[- ]specific\s+Gaussian", re.I)),
    (
        "overbroad all claims verified",
        re.compile(r"all\s+mathematical\s+and\s+computational\s+claims\s+are\s+verified", re.I),
    ),
]

FORBIDDEN_BASE_TERMS = ["Divine Core", "Void Realm", "WRW"]

ALLOWED_PATH_PARTS = {
    "docs/claim-language-policy.md",
    "tools/audit_claims.py",
    "tests/fixtures",
    "interpretations/wrw",
}


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    if path.suffix not in TEXT_EXTENSIONS:
        return True
    if any(rel.startswith(prefix) or rel == prefix for prefix in ALLOWED_PATH_PARTS):
        return True
    return False


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and not should_skip(path, root):
            yield path


def audit(root: Path) -> list[str]:
    violations: list[str] = []
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for label, pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                violations.append(f"{rel}:{line}: {label}: {match.group(0)!r}")

        for term in FORBIDDEN_BASE_TERMS:
            start = 0
            while True:
                index = text.find(term, start)
                if index == -1:
                    break
                line = text.count("\n", 0, index) + 1
                violations.append(f"{rel}:{line}: narrative term not allowed in ASH base docs: {term!r}")
                start = index + len(term)

    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    violations = audit(root)
    if violations:
        print("ASH Skir claim audit: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("ASH Skir claim audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
