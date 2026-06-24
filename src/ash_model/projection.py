"""Exact code-orbit averaging operator T."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .bits import BIT_COUNT, bits_to_int, int_to_bits
from .code import CODEWORDS

STATE_COUNT = 1 << BIT_COUNT
CODEWORD_INDICES = tuple(bits_to_int(word) for word in CODEWORDS)


def orbit_average(values: Sequence[float] | np.ndarray) -> np.ndarray:
    """Compute (T f)(x) = |C|^-1 sum_c f(x xor c) for all x."""

    data = np.asarray(values, dtype=float)
    if data.shape != (STATE_COUNT,):
        raise ValueError(f"expected a vector of length {STATE_COUNT}")
    output = np.empty_like(data)
    for index in range(STATE_COUNT):
        output[index] = sum(data[index ^ code_index] for code_index in CODEWORD_INDICES) / len(CODEWORD_INDICES)
    return output


def monte_carlo_orbit_average(
    values: Sequence[float] | np.ndarray,
    *,
    samples_per_state: int,
    seed: int = 0,
) -> np.ndarray:
    """Unbiased Monte Carlo approximation of T using sampled codewords."""

    if samples_per_state <= 0:
        raise ValueError("samples_per_state must be positive")
    data = np.asarray(values, dtype=float)
    if data.shape != (STATE_COUNT,):
        raise ValueError(f"expected a vector of length {STATE_COUNT}")
    rng = np.random.default_rng(seed)
    output = np.empty_like(data)
    for index in range(STATE_COUNT):
        sampled = rng.choice(CODEWORD_INDICES, size=samples_per_state, replace=True)
        output[index] = float(np.mean([data[index ^ int(code_index)] for code_index in sampled]))
    return output


def is_code_invariant(values: Sequence[float] | np.ndarray, *, atol: float = 1e-12) -> bool:
    data = np.asarray(values, dtype=float)
    if data.shape != (STATE_COUNT,):
        return False
    for code_index in CODEWORD_INDICES:
        if not np.allclose(data, data[np.arange(STATE_COUNT) ^ code_index], atol=atol, rtol=0.0):
            return False
    return True


def projection_certificate() -> dict[str, object]:
    """Finite checks supplementing the algebraic proof of T^2=T."""

    probe = np.asarray([index * index - 7 * index + 3 for index in range(STATE_COUNT)], dtype=float)
    once = orbit_average(probe)
    twice = orbit_average(once)
    return {
        "state_count": STATE_COUNT,
        "codeword_count": len(CODEWORD_INDICES),
        "idempotence_max_abs_error": float(np.max(np.abs(twice - once))),
        "output_is_code_invariant": is_code_invariant(once),
        "constant_preserved": bool(np.array_equal(orbit_average(np.ones(STATE_COUNT)), np.ones(STATE_COUNT))),
    }
