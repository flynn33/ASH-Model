#!/usr/bin/env python3
"""Reproduce finite sector-mixing workbench CSV artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
from math import comb
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from ash_model.bits import bits_to_int, hamming_weight, int_to_bits, integrity_bit
from ash_model.physics import (
    mixed_sector_eigenvalue,
    mixed_sector_transition,
    payload_pair_flip_transition,
    payload_state_space,
)


SPECTRAL_EPSILONS = (0.0, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5)
TIME_SERIES_EPSILONS = (0.0, 0.001, 0.01, 0.05, 0.1)
LUMPED_EPSILONS = (0.01, 0.05, 0.1)
DEFAULT_PAIR_PROBABILITY = 0.5
FIGURE_HASHES = {
    "gap_vs_epsilon.png": "250c76f73a8394702e46ae7e6da93c4574b4dae104b7898e1066422e111d9000",
    "sector_mass_vs_time.png": "3c316bab6fe9146c0b3b215573e5c71a6469fed595ddd6bf89106b47b37b2679",
    "tv_convergence.png": "c11714e8ec6cd1acf43c0e7009287758d7e9a69e09540aa729b9707a06e8b892",
}


def write_rows(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(fieldnames), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reachable_count(kernel: np.ndarray, start: int = 0) -> int:
    seen = {start}
    frontier = [start]
    while frontier:
        row = frontier.pop()
        for column in np.flatnonzero(kernel[row] > 0.0):
            column = int(column)
            if column not in seen:
                seen.add(column)
                frontier.append(column)
    return len(seen)


def write_state_metadata(data_dir: Path) -> None:
    rows = []
    for index, payload in enumerate(payload_state_space()):
        rows.append(
            {
                "state_index": index,
                "x1_to_x8": "".join(str(bit) for bit in payload),
                "x9_parity": integrity_bit(payload),
                "hamming_weight_8": hamming_weight(payload),
                "weight_sector": hamming_weight(payload) % 2,
            }
        )
    write_rows(
        data_dir / "admissible_state_metadata_256.csv",
        ("state_index", "x1_to_x8", "x9_parity", "hamming_weight_8", "weight_sector"),
        rows,
    )


def spectral_formula(epsilon: float) -> list[float]:
    values: list[float] = []
    for mode_weight in range(9):
        values.extend(
            [mixed_sector_eigenvalue(mode_weight, epsilon, pair_probability=DEFAULT_PAIR_PROBABILITY)]
            * comb(8, mode_weight)
        )
    return values


def write_spectral_scan(data_dir: Path) -> None:
    rows = []
    for epsilon in SPECTRAL_EPSILONS:
        kernel = mixed_sector_transition(epsilon, pair_probability=DEFAULT_PAIR_PROBABILITY)
        values = np.sort(np.linalg.eigvalsh(kernel))[::-1]
        formula = spectral_formula(epsilon)
        rows.append(
            {
                "epsilon": epsilon,
                "connected": reachable_count(kernel) == 256,
                "reachable": reachable_count(kernel),
                "gap": 1.0 - max(abs(value) for value in values[1:]),
                "lambda2": float(values[1]),
                "max_formula_error": float(np.max(np.abs(np.sort(values) - np.sort(formula)))),
                "min_eigen": float(values[-1]),
            }
        )
    write_rows(
        data_dir / "sector_mixing_spectral_scan.csv",
        ("epsilon", "connected", "reachable", "gap", "lambda2", "max_formula_error", "min_eigen"),
        rows,
    )


def write_time_series(data_dir: Path) -> None:
    payloads = payload_state_space()
    payload_weights = np.asarray([hamming_weight(payload) for payload in payloads], dtype=float)
    odd_indicator = np.asarray([hamming_weight(payload) % 2 for payload in payloads], dtype=float)
    uniform = np.full(256, 1.0 / 256.0, dtype=float)
    rows = []
    for epsilon in TIME_SERIES_EPSILONS:
        kernel = mixed_sector_transition(epsilon, pair_probability=DEFAULT_PAIR_PROBABILITY)
        law = np.zeros(256, dtype=float)
        law[0] = 1.0
        for step in range(501):
            rows.append(
                {
                    "epsilon": epsilon,
                    "t": step,
                    "odd_sector_mass": float(law @ odd_indicator),
                    "mean_weight_8": float(law @ payload_weights),
                    "tv_to_uniform": float(0.5 * np.sum(np.abs(law - uniform))),
                }
            )
            law = law @ kernel
    write_rows(
        data_dir / "sector_mixing_time_series.csv",
        ("epsilon", "t", "odd_sector_mass", "mean_weight_8", "tv_to_uniform"),
        rows,
    )


def lumped_weight_row(epsilon: float, weight: int) -> dict[str, object]:
    pair = payload_pair_flip_transition(DEFAULT_PAIR_PROBABILITY)
    refresh = mixed_sector_transition(1.0, pair_probability=DEFAULT_PAIR_PROBABILITY)
    kernel = (1.0 - epsilon) * pair + epsilon * refresh
    law = np.zeros(256, dtype=float)
    states = [bits_to_int(int_to_bits(index, length=8)) for index in range(256)]
    matching = [index for index in states if hamming_weight(int_to_bits(index, length=8)) == weight]
    for index in matching:
        law[index] = 1.0 / len(matching)
    next_law = law @ kernel
    row: dict[str, object] = {f"to_w{target_weight}": 0.0 for target_weight in range(9)}
    for index, probability in enumerate(next_law):
        target_weight = hamming_weight(int_to_bits(index, length=8))
        row[f"to_w{target_weight}"] = float(row[f"to_w{target_weight}"]) + float(probability)
    row["from_weight"] = weight
    return row


def write_lumped_weight_transitions(data_dir: Path) -> None:
    fields = tuple(f"to_w{weight}" for weight in range(9)) + ("from_weight",)
    for epsilon in LUMPED_EPSILONS:
        rows = [lumped_weight_row(epsilon, weight) for weight in range(9)]
        write_rows(data_dir / f"lumped_weight_transition_epsilon_{epsilon:g}.csv", fields, rows)


def generate_figures(data_dir: Path, figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    spectral = np.genfromtxt(data_dir / "sector_mixing_spectral_scan.csv", delimiter=",", names=True)
    time_series = np.genfromtxt(data_dir / "sector_mixing_time_series.csv", delimiter=",", names=True)

    plt.figure()
    plt.plot(spectral["epsilon"], spectral["gap"], marker="o")
    plt.xlabel("epsilon")
    plt.ylabel("spectral gap")
    plt.tight_layout()
    plt.savefig(figures_dir / "gap_vs_epsilon.png")
    plt.close()

    plt.figure()
    for epsilon in TIME_SERIES_EPSILONS:
        mask = time_series["epsilon"] == epsilon
        plt.plot(time_series["t"][mask], time_series["odd_sector_mass"][mask], label=f"{epsilon:g}")
    plt.xlabel("step")
    plt.ylabel("odd sector mass")
    plt.legend(title="epsilon")
    plt.tight_layout()
    plt.savefig(figures_dir / "sector_mass_vs_time.png")
    plt.close()

    plt.figure()
    for epsilon in TIME_SERIES_EPSILONS:
        mask = time_series["epsilon"] == epsilon
        plt.plot(time_series["t"][mask], time_series["tv_to_uniform"][mask], label=f"{epsilon:g}")
    plt.xlabel("step")
    plt.ylabel("total variation to uniform")
    plt.legend(title="epsilon")
    plt.tight_layout()
    plt.savefig(figures_dir / "tv_convergence.png")
    plt.close()


def verify_figures(figures_dir: Path) -> None:
    missing = []
    mismatched = []
    for filename, expected in FIGURE_HASHES.items():
        path = figures_dir / filename
        if not path.exists():
            missing.append(filename)
            continue
        actual = sha256_file(path)
        if actual != expected:
            mismatched.append((filename, expected, actual))
    if missing or mismatched:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if mismatched:
            details.extend(f"{name}: expected {expected}, actual {actual}" for name, expected, actual in mismatched)
        raise SystemExit("Figure verification failed: " + "; ".join(details))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=".", help="Repository root or output root.")
    parser.add_argument("--refresh-figures", action="store_true", help="Regenerate figure PNGs intentionally.")
    args = parser.parse_args()

    root = Path(args.output_dir)
    data_dir = root / "data" / "ash-physics-sector-mixing"
    figures_dir = root / "figures" / "ash-physics-sector-mixing"

    write_state_metadata(data_dir)
    write_spectral_scan(data_dir)
    write_time_series(data_dir)
    write_lumped_weight_transitions(data_dir)

    if args.refresh_figures or not all((figures_dir / filename).exists() for filename in FIGURE_HASHES):
        generate_figures(data_dir, figures_dir)
    else:
        verify_figures(figures_dir)

    print("sector-mixing reproduction complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
