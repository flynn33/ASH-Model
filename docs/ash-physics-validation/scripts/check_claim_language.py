#!/usr/bin/env python3
"""Scan repository text for unsupported overclaim language."""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

DEFAULT_EXCLUDE = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    "dist", "build", ".mypy_cache", ".pytest_cache"
}

FORBIDDEN_PATTERNS = [
    ("unsupported_empirical_claim", re.compile(r"empirically\s+(confirmed|proven)|validated\s+cosmology|proves\s+the\s+universe", re.I)),
    ("finite_algebra_overclaim", re.compile(r"finite\s+algebra\s+.*proves\s+.*cosmolog", re.I)),
    ("unsupported_supersymmetry_claim", re.compile(r"establishes\s+physical\s+supersymmetry|supersymmetry\s+in\s+nature", re.I)),
]

NEGATED_BOUNDARY_PHRASES = (
    "not empirically",
    "not presented as",
    "does not state",
    "does not establish",
)

TEXT_SUFFIXES = {
    ".md", ".txt", ".tex", ".py", ".json", ".yaml", ".yml", ".toml", ".rst"
}


def should_scan(path: pathlib.Path) -> bool:
    return path.is_file() and path.suffix.lower() in TEXT_SUFFIXES


def iter_files(root: pathlib.Path):
    for path in root.rglob("*"):
        if any(part in DEFAULT_EXCLUDE for part in path.parts):
            continue
        if should_scan(path):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    failures = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            for label, pattern in FORBIDDEN_PATTERNS:
                # Ignore scanner source literals that define the check itself.
                if path.name == "check_claim_language.py" and "re.compile" in line:
                    continue
                if label == "unsupported_empirical_claim" and any(phrase in lowered for phrase in NEGATED_BOUNDARY_PHRASES):
                    continue
                if label == "unsupported_empirical_claim" and "not" in lowered and "empirically confirmed" in lowered:
                    continue
                if pattern.search(line):
                    failures.append((path, line_no, label, line.strip()))
    if failures:
        for path, line_no, label, line in failures:
            print(f"{path}:{line_no}: {label}: {line}")
        return 1
    print("claim-language scan passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
