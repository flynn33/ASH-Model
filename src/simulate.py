#!/usr/bin/env python3
"""Seeded ASH data generator with nontrivial, auditable dynamics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from ash_model.simulation import run_simulation

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=1000)
    parser.add_argument("--ticks", type=int, default=250)
    parser.add_argument("--noise", type=float, default=0.01)
    parser.add_argument("--seed", type=int, default=20260624)
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "data" / "simulation-results.csv")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_simulation(
        agent_count=args.agents,
        ticks=args.ticks,
        initial_mode="uniform",
        transform_mode="ash",
        noise_probability=args.noise,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(
        args.output,
        result.agents,
        fmt="%d",
        delimiter=",",
        header="dim1,dim2,dim3,dim4,dim5,dim6,dim7,dim8,dim9",
        comments="",
    )
    metadata = {
        "seed": result.seed,
        "agent_count": len(result.agents),
        "ticks": result.ticks,
        "initial_mode": result.initial_mode,
        "transform_mode": result.transform_mode,
        "noise_probability": result.noise_probability,
        "tv_to_binomial": result.tv_to_binomial,
    }
    metadata_path = args.output.with_name("simulation-metadata.json")
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
