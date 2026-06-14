#!/usr/bin/env python3
"""Run reproducible simulation controls for the Skir branch."""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.ash_code import CANONICAL_TRANSFORMS, DIM

OUTPUT_PATH = REPO_ROOT / "data" / "simulation-controls.json"


def binomial_weights(dim: int = DIM) -> np.ndarray:
    probabilities = np.array([comb(dim, weight) for weight in range(dim + 1)], dtype=float)
    probabilities /= probabilities.sum()
    return probabilities


def tvd_to_binomial(weights: np.ndarray) -> float:
    observed = np.bincount(weights, minlength=DIM + 1).astype(float)
    observed /= observed.sum()
    expected = binomial_weights()
    return float(0.5 * np.abs(observed - expected).sum())


def random_codewords(rng: np.random.Generator, count: int = 6) -> np.ndarray:
    return rng.integers(0, 2, size=(count, DIM), dtype=np.int8)


def simulate(
    *,
    name: str,
    agents_count: int,
    ticks: int,
    noise_prob: float,
    start: str,
    codewords: np.ndarray | None,
    seed: int,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    if start == "random":
        agents = rng.integers(0, 2, size=(agents_count, DIM), dtype=np.int8)
    elif start == "zero":
        agents = np.zeros((agents_count, DIM), dtype=np.int8)
    else:
        raise ValueError(f"unknown start mode: {start}")

    for _ in range(ticks):
        if codewords is not None and len(codewords) > 0:
            code = codewords[int(rng.integers(0, len(codewords)))]
            agents ^= code
        if noise_prob > 0:
            flips = rng.random(size=(agents_count, DIM)) < noise_prob
            agents ^= flips.astype(np.int8)

    weights = agents.sum(axis=1)
    counts = np.bincount(weights, minlength=DIM + 1).astype(int).tolist()
    return {
        "name": name,
        "agents": agents_count,
        "ticks": ticks,
        "noise_prob": noise_prob,
        "start": start,
        "hamming_weight_counts": counts,
        "tvd_to_binomial": tvd_to_binomial(weights),
    }


def run_controls(*, quick: bool = False, seed: int = 20260613) -> dict[str, object]:
    agents_count = 500 if quick else 2000
    ticks = 200 if quick else 2000
    noise_prob = 0.01
    rng = np.random.default_rng(seed)
    ash = np.array(CANONICAL_TRANSFORMS, dtype=np.int8)
    random_codes = random_codewords(rng, count=len(CANONICAL_TRANSFORMS))

    runs = [
        simulate(
            name="random_start_ash_noise",
            agents_count=agents_count,
            ticks=ticks,
            noise_prob=noise_prob,
            start="random",
            codewords=ash,
            seed=seed + 1,
        ),
        simulate(
            name="random_start_no_transform_noise",
            agents_count=agents_count,
            ticks=ticks,
            noise_prob=noise_prob,
            start="random",
            codewords=None,
            seed=seed + 2,
        ),
        simulate(
            name="random_start_random_transform_noise",
            agents_count=agents_count,
            ticks=ticks,
            noise_prob=noise_prob,
            start="random",
            codewords=random_codes,
            seed=seed + 3,
        ),
        simulate(
            name="zero_start_ash_no_noise",
            agents_count=agents_count,
            ticks=ticks,
            noise_prob=0.0,
            start="zero",
            codewords=ash,
            seed=seed + 4,
        ),
        simulate(
            name="zero_start_ash_noise",
            agents_count=agents_count,
            ticks=ticks,
            noise_prob=noise_prob,
            start="zero",
            codewords=ash,
            seed=seed + 5,
        ),
    ]
    return {
        "schema": "ash.skir.controls.v1",
        "quick": quick,
        "seed": seed,
        "interpretation": (
            "Controls compare ASH codeword transforms with no-codeword and random-codeword "
            "baselines. They support conservative language about noisy hypercube mixing and "
            "do not by themselves prove runtime error correction."
        ),
        "scenarios": runs,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="run small controls")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args(argv)

    result = run_controls(quick=args.quick)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    for run in result["scenarios"]:
        print(f"{run['name']}: TVD={run['tvd_to_binomial']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
