"""
Visualization-focused noisy hypercube mixing demo for ASH.

This script applies parity-explicit canonical ASH code masks and optional
random bit-flip noise to agents in F2^9. It visualizes Hamming-weight
occupancy. It does not by itself demonstrate runtime error correction;
decoder behavior is tested in src/ash_code.py and tests/test_ash_code.py.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from src.ash_code import CANONICAL_TRANSFORMS, DIM

NUM_AGENTS = 2000
TICKS = 2000
NOISE_PROB = 0.01
DEFAULT_SEED = 20260613
OUTPUT_PATH = Path("figures") / "simulation-histogram-generated.png"


def run_simulation(
    *,
    num_agents: int = NUM_AGENTS,
    ticks: int = TICKS,
    noise_prob: float = NOISE_PROB,
    seed: int = DEFAULT_SEED,
) -> tuple[np.ndarray, np.ndarray]:
    """Run the visualization demo and return final occupancy plus history."""
    rng = np.random.default_rng(seed)
    codewords = [np.array(codeword, dtype=np.int8) for codeword in CANONICAL_TRANSFORMS]
    agents = rng.integers(0, 2, size=(num_agents, DIM), dtype=np.int8)
    occupancy_history = np.zeros((ticks + 1, DIM + 1), dtype=int)

    initial_weights = agents.sum(axis=1)
    for weight in initial_weights:
        occupancy_history[0, int(weight)] += 1

    for tick in range(1, ticks + 1):
        code = codewords[int(rng.integers(0, len(codewords)))]
        agents ^= code

        if noise_prob > 0:
            flips = rng.random(size=(num_agents, DIM)) < noise_prob
            agents ^= flips.astype(np.int8)

        weights = agents.sum(axis=1)
        for weight in weights:
            occupancy_history[tick, int(weight)] += 1

    return occupancy_history[-1], occupancy_history


def save_histogram(final_occupancy: np.ndarray, *, output_path: Path, num_agents: int, ticks: int, noise_prob: float) -> None:
    """Write a Hamming-weight occupancy histogram."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    planes = np.arange(DIM + 1)

    plt.figure(figsize=(10, 6))
    plt.bar(planes, final_occupancy, color="teal", alpha=0.8, edgecolor="black")
    plt.title(
        "ASH Model Simulation: Hamming-Weight Occupancy Distribution\n"
        f"({num_agents} agents after {ticks} ticks, noise p={noise_prob})"
    )
    plt.xlabel("Hamming Weight Plane")
    plt.ylabel("Number of Agents")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--ticks", type=int, default=TICKS)
    parser.add_argument("--agents", type=int, default=NUM_AGENTS)
    parser.add_argument("--noise-prob", type=float, default=NOISE_PROB)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    final_occupancy, _ = run_simulation(
        num_agents=args.agents,
        ticks=args.ticks,
        noise_prob=args.noise_prob,
        seed=args.seed,
    )
    save_histogram(
        final_occupancy,
        output_path=args.output,
        num_agents=args.agents,
        ticks=args.ticks,
        noise_prob=args.noise_prob,
    )

    print("Simulation demo complete.")
    print(f"Histogram saved to {args.output}")
    print("Final occupancy per plane:")
    for plane, count in enumerate(final_occupancy):
        print(f"Plane {plane}: {count} agents ({100 * count / args.agents:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
