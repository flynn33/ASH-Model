#!/usr/bin/env python3
"""Audit ASH simulation CSV data against repository expectations."""

from __future__ import annotations

import ast
import csv
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SIM_PATH = REPO_ROOT / "src" / "simulate.py"
DATA_PATH = REPO_ROOT / "data" / "simulation-results.csv"


def read_constants(path: Path) -> dict[str, int]:
    constants: dict[str, int] = {}
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {"NUM_AGENTS", "DIM", "TICKS"} and isinstance(node.value, ast.Constant):
                constants[name] = int(node.value.value)
    return constants


def read_csv_rows(path: Path) -> tuple[list[str], list[list[float]], list[tuple[int, list[str]]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows: list[list[float]] = []
        malformed: list[tuple[int, list[str]]] = []
        for line_no, row in enumerate(reader, start=2):
            if not row:
                continue
            if len(row) != 9:
                malformed.append((line_no, row))
                continue
            try:
                rows.append([float(v) for v in row])
            except ValueError:
                malformed.append((line_no, row))
        return header, rows, malformed


def main() -> int:
    constants = read_constants(SIM_PATH)
    header, rows, malformed = read_csv_rows(DATA_PATH)

    expected_agents = constants.get("NUM_AGENTS")
    expected_dim = constants.get("DIM")

    print("ASH data audit")
    print(f"- Source constants: NUM_AGENTS={expected_agents}, DIM={expected_dim}, TICKS={constants.get('TICKS')}")
    print(f"- CSV header columns: {len(header)}")
    print(f"- Valid rows: {len(rows)}")

    if malformed:
        print(f"- Malformed rows: {len(malformed)}")
        for line_no, row in malformed[:5]:
            preview = ",".join(row[:3])
            print(f"  - line {line_no}: {len(row)} columns (starts with: {preview})")

    if rows:
        dims = len(rows[0])
        unique_states = len({tuple(int(v) for v in r) for r in rows})
        weights = [sum(int(v) for v in r) for r in rows]
        print(f"- Inferred row width: {dims}")
        print(f"- Unique binary states: {unique_states}")
        print(f"- Hamming weight distribution: {dict(sorted(Counter(weights).items()))}")

    failures: list[str] = []
    if expected_dim is not None and len(header) != expected_dim:
        failures.append(f"header has {len(header)} columns but DIM={expected_dim}")
    if expected_dim is not None and rows and len(rows[0]) != expected_dim:
        failures.append(f"row width {len(rows[0])} does not match DIM={expected_dim}")
    if expected_agents is not None and len(rows) != expected_agents:
        failures.append(f"valid row count {len(rows)} does not match NUM_AGENTS={expected_agents}")
    if malformed:
        failures.append(f"CSV contains {len(malformed)} malformed row(s)")

    # Deterministic parity check from the implementation: same codeword is applied every tick.
    ticks = constants.get("TICKS")
    if ticks is not None:
        parity = "identity" if ticks % 2 == 0 else "single XOR flip"
        print(f"- Transform parity after TICKS: {parity} (because same codeword is used every tick)")

    if failures:
        print("\nRESULT: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
