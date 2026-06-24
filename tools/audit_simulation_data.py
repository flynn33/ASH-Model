#!/usr/bin/env python3
"""Audit generated ASH data against version-1.1.0 invariants."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "simulation-results.csv"
METADATA_PATH = REPO_ROOT / "data" / "simulation-metadata.json"
REFERENCE_PATH = REPO_ROOT / "data" / "ash-state-reference.csv"
CODEWORDS_PATH = REPO_ROOT / "data" / "codewords.csv"


def read_binary_csv(path: Path) -> list[tuple[int, ...]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = [tuple(int(value) for value in row) for row in reader]
    if len(header) != 9 or any(len(row) != 9 for row in rows):
        raise AssertionError(f"{path} does not contain nine columns")
    if any(value not in (0, 1) for row in rows for value in row):
        raise AssertionError(f"{path} contains non-binary values")
    return rows


def main() -> int:
    states = read_binary_csv(DATA_PATH)
    if len(states) != 1000:
        raise AssertionError("simulation-results.csv must contain 1,000 rows")
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if metadata["agent_count"] != len(states):
        raise AssertionError("metadata agent count mismatch")

    with REFERENCE_PATH.open(newline="", encoding="utf-8") as handle:
        reference_count = sum(1 for _ in csv.DictReader(handle))
    if reference_count != 512:
        raise AssertionError("state reference must contain 512 rows")

    with CODEWORDS_PATH.open(newline="", encoding="utf-8") as handle:
        code_rows = list(csv.DictReader(handle))
    weights = Counter(int(row["weight"]) for row in code_rows)
    if len(code_rows) != 16 or weights != Counter({4: 14, 0: 1, 8: 1}):
        raise AssertionError("codeword table invariant mismatch")
    if any(row["syndrome"] != "00000" for row in code_rows):
        raise AssertionError("nonzero codeword syndrome")

    summary = {
        "simulation_rows": len(states),
        "simulation_unique_states": len(set(states)),
        "mean_hamming_weight": sum(sum(row) for row in states) / len(states),
        "reference_rows": reference_count,
        "codeword_weight_distribution": dict(sorted(weights.items())),
        "metadata": metadata,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
