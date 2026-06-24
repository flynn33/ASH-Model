"""Controlled Markov-chain simulations and ablations."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from math import comb
from typing import Literal

import numpy as np

from .code import CODEWORDS

TransformMode = Literal["none", "ash", "random_weight4"]
InitialMode = Literal["uniform", "zero", "one", "integrity_uniform"]


@dataclass(frozen=True)
class SimulationResult:
    agents: np.ndarray
    occupancy: np.ndarray
    tv_to_binomial: float
    seed: int
    initial_mode: InitialMode
    transform_mode: TransformMode
    noise_probability: float
    ticks: int


def binomial_distribution() -> np.ndarray:
    return np.asarray([comb(9, weight) / 512.0 for weight in range(10)], dtype=float)


def total_variation(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left, dtype=float)
    b = np.asarray(right, dtype=float)
    if a.shape != b.shape:
        raise ValueError("distributions must have equal shape")
    return float(0.5 * np.sum(np.abs(a - b)))


def initialize_agents(count: int, mode: InitialMode, rng: np.random.Generator) -> np.ndarray:
    if count <= 0:
        raise ValueError("count must be positive")
    if mode == "uniform":
        return rng.integers(0, 2, size=(count, 9), dtype=np.uint8)
    if mode == "zero":
        return np.zeros((count, 9), dtype=np.uint8)
    if mode == "one":
        return np.ones((count, 9), dtype=np.uint8)
    if mode == "integrity_uniform":
        payload = rng.integers(0, 2, size=(count, 8), dtype=np.uint8)
        parity = np.bitwise_xor.reduce(payload, axis=1, keepdims=True)
        return np.concatenate([payload, parity], axis=1)
    raise ValueError(f"unsupported initial mode {mode!r}")


@lru_cache(maxsize=1)
def _weight4_mask_table() -> np.ndarray:
    table = np.zeros((126, 9), dtype=np.uint8)
    for row, indices in enumerate(combinations(range(9), 4)):
        table[row, list(indices)] = 1
    return table


def _random_weight4_masks(count: int, rng: np.random.Generator) -> np.ndarray:
    table = _weight4_mask_table()
    choices = rng.integers(0, len(table), size=count)
    return table[choices].copy()


def step_agents(
    agents: np.ndarray,
    *,
    transform_mode: TransformMode,
    noise_probability: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if agents.ndim != 2 or agents.shape[1] != 9:
        raise ValueError("agents must have shape Nx9")
    if noise_probability < 0.0 or noise_probability > 1.0:
        raise ValueError("noise_probability must lie in [0,1]")
    output = np.asarray(agents, dtype=np.uint8).copy()
    count = output.shape[0]
    if transform_mode == "ash":
        code_array = np.asarray(CODEWORDS, dtype=np.uint8)
        choices = rng.integers(0, len(code_array), size=count)
        output ^= code_array[choices]
    elif transform_mode == "random_weight4":
        output ^= _random_weight4_masks(count, rng)
    elif transform_mode != "none":
        raise ValueError(f"unsupported transform mode {transform_mode!r}")

    noisy = rng.random(count) < noise_probability
    rows = np.flatnonzero(noisy)
    if rows.size:
        coordinates = rng.integers(0, 9, size=rows.size)
        output[rows, coordinates] ^= 1
    return output


def occupancy_distribution(agents: np.ndarray) -> np.ndarray:
    weights = np.sum(agents, axis=1).astype(int)
    counts = np.bincount(weights, minlength=10).astype(float)
    return counts / float(len(agents))


def run_simulation(
    *,
    agent_count: int = 10_000,
    ticks: int = 250,
    initial_mode: InitialMode = "uniform",
    transform_mode: TransformMode = "ash",
    noise_probability: float = 0.01,
    seed: int = 20260624,
) -> SimulationResult:
    if ticks < 0:
        raise ValueError("ticks may not be negative")
    rng = np.random.default_rng(seed)
    agents = initialize_agents(agent_count, initial_mode, rng)
    for _ in range(ticks):
        agents = step_agents(
            agents,
            transform_mode=transform_mode,
            noise_probability=noise_probability,
            rng=rng,
        )
    occupancy = occupancy_distribution(agents)
    return SimulationResult(
        agents=agents,
        occupancy=occupancy,
        tv_to_binomial=total_variation(occupancy, binomial_distribution()),
        seed=seed,
        initial_mode=initial_mode,
        transform_mode=transform_mode,
        noise_probability=noise_probability,
        ticks=ticks,
    )


def run_ablation_suite(
    *,
    agent_count: int = 20_000,
    ticks: int = 400,
    noise_probability: float = 0.02,
    seed: int = 20260624,
) -> tuple[SimulationResult, ...]:
    specifications = (
        ("uniform", "none", 0.0),
        ("uniform", "ash", noise_probability),
        ("uniform", "none", noise_probability),
        ("zero", "ash", 0.0),
        ("zero", "ash", noise_probability),
        ("zero", "none", noise_probability),
        ("zero", "random_weight4", noise_probability),
    )
    results = []
    for offset, (initial_mode, transform_mode, noise) in enumerate(specifications):
        results.append(
            run_simulation(
                agent_count=agent_count,
                ticks=ticks,
                initial_mode=initial_mode,  # type: ignore[arg-type]
                transform_mode=transform_mode,  # type: ignore[arg-type]
                noise_probability=noise,
                seed=seed + offset,
            )
        )
    return tuple(results)


def noise_kernel(noise_probability: float) -> np.ndarray:
    """Return the exact 512x512 lazy single-bit-flip transition matrix."""

    if not 0.0 <= noise_probability <= 1.0:
        raise ValueError("noise_probability must lie in [0,1]")
    state_count = 512
    kernel = np.zeros((state_count, state_count), dtype=float)
    for state in range(state_count):
        kernel[state, state] += 1.0 - noise_probability
        for bit in range(9):
            # State integers use the same XOR operation regardless of display order.
            neighbor = state ^ (1 << bit)
            kernel[state, neighbor] += noise_probability / 9.0
    return kernel
