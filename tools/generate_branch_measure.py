#!/usr/bin/env python3
"""Generate Roadmap 008 finite branch-measure artifacts.

Outputs are deterministic finite-observer ASH branch-measure artifacts. They do
not define empirical cosmological probabilities, a Born-rule derivation, a
decoherence law, or a physical bridge to observables.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable, Mapping

from ash_model.branch_measure import (
    BranchMeasure,
    BranchMeasureConfig,
    demo_branch_frontier,
    frontier_entropy,
    law_summary,
    shell_demo_children,
    transfer_penalty,
    verify_branch_measure,
)

DATA_RELATIVE = Path("data/ash-cosmology/branch-measure/v0.1")
VALIDATION_RELATIVE = Path("validation/branch-measure/roadmap-008/outputs")


def _write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _frontier_rows(rows: Iterable[BranchMeasure]) -> list[dict[str, object]]:
    return [
        {
            "branch_id": row.branch_id,
            "parent_id": row.parent_id,
            "shell_q": row.shell_q,
            "score": row.score,
            "local_probability": row.local_probability,
            "measure": row.measure,
            "amplitude_real": row.amplitude_real,
            "amplitude_imag": row.amplitude_imag,
            "amplitude_norm_squared": row.amplitude_norm_squared,
        }
        for row in rows
    ]


def _shell_score_rows(config: BranchMeasureConfig) -> list[dict[str, object]]:
    return [
        {
            "shell_q": q,
            "transfer_probability": config.transfer_probability,
            "transfer_penalty": transfer_penalty(q, config.transfer_probability, config.epsilon),
        }
        for q in range(5)
    ]


def _entropy_rows(config: BranchMeasureConfig, max_depth: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for depth in range(1, max_depth + 1):
        frontier = demo_branch_frontier(depth=depth, config=config)
        rows.append(
            {
                "depth": depth,
                "frontier_size": len(frontier),
                "frontier_entropy_bits": frontier_entropy(frontier),
                "total_measure": sum(row.measure for row in frontier),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".", help="repository root for generated outputs")
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--beta", type=float, default=1.0)
    parser.add_argument("--transfer-probability", type=float, default=0.05)
    args = parser.parse_args()

    config = BranchMeasureConfig(beta=args.beta, transfer_probability=args.transfer_probability)
    root = Path(args.out_root)
    data_dir = root / DATA_RELATIVE
    validation_dir = root / VALIDATION_RELATIVE
    data_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    frontier = demo_branch_frontier(depth=args.depth, config=config)
    _write_csv(data_dir / "branch_measure_frontier.csv", _frontier_rows(frontier))
    _write_csv(data_dir / "shell_transfer_penalties.csv", _shell_score_rows(config))
    _write_csv(data_dir / "branch_entropy_by_depth.csv", _entropy_rows(config, args.depth))
    _write_csv(
        data_dir / "root_child_candidates.csv",
        [
            {
                "branch_id": child.branch_id,
                "parent_id": child.parent_id,
                "shell_q": child.shell_q,
                "action": child.action,
                "defect_count": child.defect_count,
                "memory_delta": child.memory_delta,
                "coherence_penalty": child.coherence_penalty,
            }
            for child in shell_demo_children("root", depth=1, probability=config.transfer_probability)
        ],
    )

    verification = {
        "classification": {
            "layer_1": "finite branch normalization law over finite sibling sets",
            "layer_2": "deterministic branch-frontier artifact generation and normalization checks",
            "layer_3_boundary": "interpretive branch-cosmology scaffolding only; no empirical cosmology or Born-rule proof",
        },
        "boundary": "Finite ASH branch measure only; no Hilbert-space dynamics, no physical probability calibration, no decoherence rule, no bridge to observables, and no empirical validation.",
        "law_summary": law_summary(config),
        "frontier_depth": args.depth,
        "normalization_check": verify_branch_measure(frontier),
        "entropy_bits": frontier_entropy(frontier),
    }
    (validation_dir / "verification.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote finite branch-measure data to {data_dir}")
    print(f"wrote verification JSON to {validation_dir / 'verification.json'}")


if __name__ == "__main__":
    main()
