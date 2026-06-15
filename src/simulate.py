"""
Data-focused ASH simulation demo.

Generates CSV data for 1000 agents over 1000 ticks in a 9D binary state
space. The script applies parity-explicit canonical code masks and records
the resulting state matrix. It is a data/demo script, not standalone proof of
runtime error correction.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

NUM_AGENTS = 1000
TICKS = 1000
DIM = 9
DEFAULT_SEED = 20260613

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.ash_code import CANONICAL_TRANSFORMS

OUTPUT_PATH = REPO_ROOT / "data" / "simulation-results.csv"


def adinkra_transform(state: np.ndarray, codeword: np.ndarray) -> np.ndarray:
    """Apply a canonical GF(2) codeword transform."""
    return state ^ codeword


def lsystem_branch(branches: list[str]) -> list[str]:
    """Apply cumulative L-system branching for a lightweight demo trace."""
    new = []
    for branch in branches:
        new.append(branch)
        new.append(branch + "+")
        new.append(branch + "-")
    return new


def run_simulation(*, num_agents: int = NUM_AGENTS, ticks: int = TICKS, seed: int = DEFAULT_SEED) -> np.ndarray:
    """Run the data-focused simulation and return final agent states."""
    rng = np.random.default_rng(seed)
    codewords = [np.array(codeword, dtype=np.int8) for codeword in CANONICAL_TRANSFORMS]
    agents = rng.integers(0, 2, (num_agents, DIM), dtype=np.int8)
    branches = ["F"]

    for tick in range(ticks):
        codeword = codewords[tick % len(codewords)]
        for index in range(num_agents):
            agents[index] = adinkra_transform(agents[index], codeword)

        if tick % 100 == 0:
            branches = lsystem_branch(branches)
            print(f"Tick {tick}: Branch count = {len(branches)}")

    return agents


def write_results(agents: np.ndarray, output_path: Path = OUTPUT_PATH) -> None:
    """Write final agent states as CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(
        output_path,
        agents,
        delimiter=",",
        header="dim1,dim2,dim3,dim4,dim5,dim6,dim7,dim8,dim9",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--ticks", type=int, default=TICKS)
    parser.add_argument("--agents", type=int, default=NUM_AGENTS)
    args = parser.parse_args()

    agents = run_simulation(num_agents=args.agents, ticks=args.ticks, seed=args.seed)
    weights = agents.sum(axis=1)
    unique, counts = np.unique(weights, return_counts=True)

    print("Hamming-weight occupancy distribution:")
    for weight, count in zip(unique, counts):
        print(f"Weight {int(weight)}: {int(count)} agents")

    write_results(agents)
    print(f"Simulation demo complete. Results saved to {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
