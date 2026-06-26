#!/usr/bin/env python3
"""Generate deterministic R-009 observer-commitment validation artifacts."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ash_model.observer_commitment import (
    ObserverCommitmentConfig,
    commitment_distribution,
    decoherence_entry,
    decoherence_summary,
    demo_expand_tree,
    frontier,
    record_to_row,
    verify_r009,
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".")
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--pair-sample-limit", type=int, default=5000)
    args = parser.parse_args()

    root = Path(args.out_root)
    cfg = ObserverCommitmentConfig()
    records = demo_expand_tree(max_depth=args.depth)
    leaves = frontier(records, args.depth)

    data_root = root / "data" / "ash-cosmology" / "observer-commitment" / "v0.1"
    validation_root = root / "validation" / "observer-commitment" / "roadmap-009" / "outputs"

    write_csv(data_root / "r009_frontier.csv", [record_to_row(record) for record in leaves])
    write_csv(data_root / "r009_commitment_distribution.csv", commitment_distribution(leaves))

    pair_rows: list[dict[str, object]] = []
    for i, a in enumerate(leaves):
        for b in leaves[i + 1 :]:
            if len(pair_rows) >= args.pair_sample_limit:
                break
            pair_rows.append(decoherence_entry(a, b, cfg))
        if len(pair_rows) >= args.pair_sample_limit:
            break
    write_csv(data_root / "r009_decoherence_pair_sample.csv", pair_rows)

    depth_rows = []
    for depth in range(1, args.depth + 1):
        depth_rows.append({"depth": depth, **decoherence_summary(frontier(records, depth), cfg)})
    write_csv(data_root / "r009_decoherence_summary_by_depth.csv", depth_rows)

    verification = verify_r009(max_depth=args.depth, config=cfg)
    validation_root.mkdir(parents=True, exist_ok=True)
    (validation_root / "verification.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
