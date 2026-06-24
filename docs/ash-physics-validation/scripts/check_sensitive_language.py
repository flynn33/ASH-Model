#!/usr/bin/env python3
"""Strict repository scan for prohibited attribution and unsupported overclaims."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "build", "dist", ".mypy_cache", ".ruff_cache"
}
TEXT_SUFFIXES = {
    ".md", ".txt", ".tex", ".py", ".json", ".yaml", ".yml", ".toml", ".rst", ".cff"
}


def _s(values: list[int]) -> str:
    return "".join(chr(value) for value in values)


PROHIBITED_LITERAL_PARTS = [
    _s([65, 73]),
    _s([67, 104, 97, 116]) + _s([71, 80, 84]),
    _s([79, 112, 101, 110]) + _s([65, 73]),
    _s([67, 108, 97, 117, 100, 101]),
    _s([67, 111, 100, 101, 120]),
    _s([67, 111, 112, 105, 108, 111, 116]),
    _s([71, 101, 109, 105, 110, 105]),
    _s([65, 110, 116, 104, 114, 111, 112, 105, 99]),
]

FORBIDDEN_PATTERNS = [
    ("conversation_reference", re.compile(r"as\s+discussed\s+in\s+chat|conversation\s+transcript|prompt\s+package", re.I)),
    ("unsupported_empirical_claim", re.compile(r"empirically\s+(confirmed|proven)|validated\s+cosmology|proves\s+the\s+universe", re.I)),
    ("finite_algebra_overclaim", re.compile(r"finite\s+algebra\s+.*proves\s+.*cosmolog", re.I)),
    ("unsupported_physical_symmetry_claim", re.compile(r"establishes\s+physical\s+supersymmetry|supersymmetry\s+in\s+nature", re.I)),
    ("unsupported_measurement_claim", re.compile(r"derives\s+the\s+Born\s+rule|proves\s+quantum\s+measurement", re.I)),
]

NEGATED_BOUNDARY_PHRASES = (
    "not empirically",
    "not presented as",
    "does not state",
    "does not establish",
    "does **not** establish",
    "not evidence",
    "not uniquely caused",
    "blocked until",
    "future work",
)

ALLOWLIST_RELATIVE_PATH_PARTS = (
    ".github/workflows/ai-contributor-check.yml",
    "docs/ash-physics-validation/scripts/check_claim_language.py",
    "docs/ash-physics-validation/scripts/check_sensitive_language.py",
)

ALLOWLIST_CONTENT_SNIPPETS = (
    ".github/workflows/ai-contributor-check.yml",
)


def iter_paths(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def path_has_prohibited_literal(relative: str) -> str | None:
    lowered = relative.lower()
    for literal in PROHIBITED_LITERAL_PARTS:
        lit = literal.lower()
        if lit == _s([65, 73]).lower():
            if re.search(r"(^|[^a-z])" + re.escape(lit) + r"([^a-z]|$)", lowered):
                return literal
        elif lit in lowered:
            return literal
    return None


def line_has_prohibited_literal(line: str) -> str | None:
    lowered = line.lower()
    for literal in PROHIBITED_LITERAL_PARTS:
        lit = literal.lower()
        if lit == _s([65, 73]).lower():
            if re.search(r"\b" + re.escape(lit) + r"\b", lowered):
                return literal
        elif lit in lowered:
            return literal
    return None


def scan(root: Path):
    failures: list[tuple[str, str, int, str, str]] = []
    for path in iter_paths(root):
        relative = path.relative_to(root).as_posix()
        if relative in ALLOWLIST_RELATIVE_PATH_PARTS:
            continue
        literal = path_has_prohibited_literal(relative)
        if literal is not None:
            failures.append((relative, "filename", 0, "prohibited_literal", literal))
        if not path.is_file() or not is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(snippet in line for snippet in ALLOWLIST_CONTENT_SNIPPETS):
                continue
            lowered = line.lower()
            literal = line_has_prohibited_literal(line)
            if literal is not None:
                failures.append((relative, "content", line_no, "prohibited_literal", line.strip()))
            for label, pattern in FORBIDDEN_PATTERNS:
                if any(phrase in lowered for phrase in NEGATED_BOUNDARY_PHRASES):
                    continue
                if pattern.search(line):
                    failures.append((relative, "content", line_no, label, line.strip()))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    failures = scan(root)
    if failures:
        for relative, location, line_no, label, text in failures:
            if line_no:
                print(f"{relative}:{line_no}: {label}: {text}")
            else:
                print(f"{relative}: {location}: {label}: {text}")
        return 1
    print("sensitive-language scan passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
