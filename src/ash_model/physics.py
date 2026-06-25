"""Finite-observer physics layer for ASH.

This module defines a conservative physical interpretation that stays inside
the verified finite ASH kernel.  It is a finite stochastic model over the
parity-valid ASH state space, not an empirical cosmology.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb, log2
from typing import Sequence

import numpy as np

from .bits import BIT_COUNT, BitTuple, bits_to_int, hamming_distance, hamming_weight, int_to_bits, integrity_bit, is_integrity_valid, normalize_bits, xor_bits
from .hypercube import integrity_states

PAIR_FLIP_COUNT = comb(BIT_COUNT, 2)
PAYLOAD_BIT_COUNT = BIT_COUNT - 1
PAYLOAD_PAIR_FLIP_COUNT = comb(PAYLOAD_BIT_COUNT, 2)


@dataclass(frozen=True)
class PhysicsObservables:
    """Dimensionless finite-observer observables derived from a state law."""

    mean_hamming_weight: float
    order_parameter: float
    shannon_entropy_bits: float
    parity_valid_probability: float


@dataclass(frozen=True)
class BackgroundMoments:
    """Dimensionless Hamming-background moments over parity-valid shells."""

    mean_hamming_weight: float
    variance_hamming_weight: float
    order_parameter: float


def physical_state_space() -> tuple[BitTuple, ...]:
    """Return the admissible ASH finite-observer state space.

    The current physical layer interprets admissible states as the 256
    parity-valid ASH bit strings.  This is the even-parity hyperplane of
    ``F_2^9`` under the repository coordinate convention.
    """

    return tuple(integrity_states())


def pair_flip_masks() -> tuple[BitTuple, ...]:
    """Return all weight-two masks over the nine ASH coordinates."""

    masks: list[BitTuple] = []
    for left, right in combinations(range(BIT_COUNT), 2):
        mask = [0] * BIT_COUNT
        mask[left] = 1
        mask[right] = 1
        masks.append(tuple(mask))
    return tuple(masks)


def pair_flip_transition(probability: float) -> np.ndarray:
    """Return the lazy pair-flip Markov kernel on admissible ASH states.

    With probability ``1 - probability`` the state is unchanged.  With
    probability ``probability`` one of the 36 coordinate pairs is selected
    uniformly and both bits are flipped.  The transition preserves total
    parity, is symmetric, and keeps the uniform law stationary.
    """

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    states = physical_state_space()
    index_by_state = {state: index for index, state in enumerate(states)}
    masks = pair_flip_masks()
    kernel = np.zeros((len(states), len(states)), dtype=float)
    stay_probability = 1.0 - probability
    jump_probability = probability / float(len(masks))
    for row, state in enumerate(states):
        kernel[row, row] += stay_probability
        for mask in masks:
            target = xor_bits(state, mask)
            kernel[row, index_by_state[target]] += jump_probability
    return kernel


def pair_flip_generator(rate: float) -> np.ndarray:
    """Return the continuous-time pair-flip generator."""

    if rate < 0.0:
        raise ValueError("rate must be non-negative")
    states = physical_state_space()
    index_by_state = {state: index for index, state in enumerate(states)}
    masks = pair_flip_masks()
    generator = np.zeros((len(states), len(states)), dtype=float)
    jump_rate = rate / float(len(masks))
    for row, state in enumerate(states):
        for mask in masks:
            target = xor_bits(state, mask)
            column = index_by_state[target]
            generator[row, column] += jump_rate
        generator[row, row] -= rate
    return generator


def weight_background_kernel(probability: float) -> np.ndarray:
    """Return the exact Hamming-weight background kernel.

    Rows and columns are ordered by even weights ``0, 2, 4, 6, 8``.  This is
    the lumped background equation induced by the pair-flip kernel.
    """

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    weights = even_weight_levels()
    index_by_weight = {weight: index for index, weight in enumerate(weights)}
    kernel = np.zeros((len(weights), len(weights)), dtype=float)
    for row, weight in enumerate(weights):
        down = comb(weight, 2)
        same = weight * (BIT_COUNT - weight)
        up = comb(BIT_COUNT - weight, 2)
        transitions = (
            (weight - 2, down),
            (weight, same),
            (weight + 2, up),
        )
        kernel[row, row] += 1.0 - probability
        for target_weight, count in transitions:
            if target_weight in index_by_weight:
                kernel[row, index_by_weight[target_weight]] += probability * count / PAIR_FLIP_COUNT
    return kernel


def even_weight_levels() -> tuple[int, ...]:
    """Return admissible Hamming-weight levels for parity-valid ASH states."""

    return tuple(weight for weight in range(BIT_COUNT + 1) if weight % 2 == 0)


def weight_level_degeneracies() -> tuple[int, ...]:
    """Return exact state counts for the admissible even Hamming-weight levels."""

    return tuple(comb(BIT_COUNT, weight) for weight in even_weight_levels())


def uniform_background_distribution() -> np.ndarray:
    """Return the Hamming-weight law induced by uniform admissible states."""

    degeneracies = np.asarray(weight_level_degeneracies(), dtype=float)
    return degeneracies / float(len(physical_state_space()))


def _validated_weight_distribution(weight_distribution: Sequence[float]) -> np.ndarray:
    weights = even_weight_levels()
    values = np.asarray(weight_distribution, dtype=float)
    if values.shape != (len(weights),):
        raise ValueError(f"expected {len(weights)} weight probabilities")
    if np.any(values < -1e-15):
        raise ValueError("probabilities must be non-negative")
    total = float(values.sum())
    if not np.isclose(total, 1.0):
        raise ValueError("probabilities must sum to 1")
    return values


def background_moments(weight_distribution: Sequence[float]) -> BackgroundMoments:
    """Return mean, variance, and order parameter for a weight law."""

    values = _validated_weight_distribution(weight_distribution)
    weights = np.asarray(even_weight_levels(), dtype=float)
    mean = float(values @ weights)
    centered = weights - mean
    variance = float(values @ (centered * centered))
    return BackgroundMoments(
        mean_hamming_weight=mean,
        variance_hamming_weight=variance,
        order_parameter=1.0 - (2.0 * mean / BIT_COUNT),
    )


def evolve_weight_distribution(
    weight_distribution: Sequence[float],
    *,
    probability: float,
    steps: int = 1,
) -> np.ndarray:
    """Evolve a Hamming-weight law through repeated background-kernel steps."""

    if not isinstance(steps, int):
        raise TypeError("steps must be an integer")
    if steps < 0:
        raise ValueError("steps must be non-negative")
    values = _validated_weight_distribution(weight_distribution).copy()
    kernel = weight_background_kernel(probability)
    for _ in range(steps):
        values = values @ kernel
    return values


def state_distribution_from_weights(weight_distribution: Sequence[float]) -> np.ndarray:
    """Lift a background distribution to a uniform-within-weight state law."""

    weights = even_weight_levels()
    values = _validated_weight_distribution(weight_distribution)

    states = physical_state_space()
    law = np.zeros(len(states), dtype=float)
    for index, state in enumerate(states):
        weight = hamming_weight(state)
        law[index] = values[weights.index(weight)] / comb(BIT_COUNT, weight)
    return law


def bridge_observables(distribution: Sequence[float]) -> PhysicsObservables:
    """Map a finite state law to dimensionless observer observables."""

    values = np.asarray(distribution, dtype=float)
    states = physical_state_space()
    if values.shape != (len(states),):
        raise ValueError(f"expected {len(states)} state probabilities")
    if np.any(values < -1e-15):
        raise ValueError("probabilities must be non-negative")
    total = float(values.sum())
    if not np.isclose(total, 1.0):
        raise ValueError("probabilities must sum to 1")

    weights = np.asarray([hamming_weight(state) for state in states], dtype=float)
    mean_weight = float(values @ weights)
    nonzero = values[values > 0.0]
    entropy = float(-np.sum(nonzero * np.log2(nonzero)))
    parity_valid = float(
        sum(probability for probability, state in zip(values, states, strict=True) if is_integrity_valid(state))
    )
    return PhysicsObservables(
        mean_hamming_weight=mean_weight,
        order_parameter=1.0 - (2.0 * mean_weight / BIT_COUNT),
        shannon_entropy_bits=entropy,
        parity_valid_probability=parity_valid,
    )


def uniform_physical_distribution() -> np.ndarray:
    """Return the uniform law on the admissible physical state space."""

    states = physical_state_space()
    return np.full(len(states), 1.0 / len(states), dtype=float)


def pair_flip_eigenvalue(mode_weight: int) -> float:
    """Return the normalized weight-two Krawtchouk eigenvalue.

    ``mode_weight`` is the Hamming weight of a Walsh character.  The value is
    the eigenvalue of uniform pair flipping before laziness is applied.
    """

    if not 0 <= mode_weight <= BIT_COUNT:
        raise ValueError("mode_weight outside ASH bit count")
    value = 0
    for overlap in range(3):
        if overlap <= mode_weight and 2 - overlap <= BIT_COUNT - mode_weight:
            value += ((-1) ** overlap) * comb(mode_weight, overlap) * comb(BIT_COUNT - mode_weight, 2 - overlap)
    return float(value / PAIR_FLIP_COUNT)


def lazy_pair_flip_eigenvalue(mode_weight: int, probability: float) -> float:
    """Return a perturbation-mode decay factor for one lazy update."""

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    return float((1.0 - probability) + probability * pair_flip_eigenvalue(mode_weight))


def payload_state_space() -> tuple[BitTuple, ...]:
    """Return the eight-coordinate payload state space in integer order."""

    return tuple(int_to_bits(index, length=PAYLOAD_BIT_COUNT) for index in range(1 << PAYLOAD_BIT_COUNT))


def compatible_payload_state(payload: Sequence[int]) -> BitTuple:
    """Build an admissible physical state from eight payload coordinates."""

    bits = normalize_bits(payload, length=PAYLOAD_BIT_COUNT)
    return bits + (integrity_bit(bits),)


def payload_to_physical_state(payload: Sequence[int]) -> BitTuple:
    """Map an eight-coordinate payload to a parity-valid ASH state."""

    return compatible_payload_state(payload)


def _payload_pair_flip_masks() -> tuple[BitTuple, ...]:
    masks: list[BitTuple] = []
    for left, right in combinations(range(PAYLOAD_BIT_COUNT), 2):
        mask = [0] * PAYLOAD_BIT_COUNT
        mask[left] = 1
        mask[right] = 1
        masks.append(tuple(mask))
    return tuple(masks)


def payload_pair_flip_transition(probability: float = 1.0, *, lazy: bool = True) -> np.ndarray:
    """Return the payload-coordinate pair-flip workbench kernel.

    This kernel acts on the eight payload coordinates in integer order and
    leaves the ninth ASH integrity coordinate implicit.  It is separate from
    the repository's nine-coordinate physical pair-flip kernel.
    """

    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    if not lazy and probability != 1.0:
        raise ValueError("non-lazy payload pair flips require probability=1")
    payloads = payload_state_space()
    masks = _payload_pair_flip_masks()
    kernel = np.zeros((len(payloads), len(payloads)), dtype=float)
    jump_total = probability if lazy else 1.0
    stay_probability = 1.0 - jump_total
    jump_probability = jump_total / float(len(masks))
    for row, payload in enumerate(payloads):
        kernel[row, row] += stay_probability
        for mask in masks:
            target = xor_bits(payload, mask)
            kernel[row, bits_to_int(target)] += jump_probability
    return kernel


def sector_refresh_transition() -> np.ndarray:
    """Return the admissibility-preserving payload-sector refresh kernel."""

    payloads = payload_state_space()
    kernel = np.zeros((len(payloads), len(payloads)), dtype=float)
    for row, payload in enumerate(payloads):
        for coordinate in range(PAYLOAD_BIT_COUNT):
            target = list(payload)
            target[coordinate] ^= 1
            kernel[row, bits_to_int(target)] += 1.0 / PAYLOAD_BIT_COUNT
    return kernel


def mixed_sector_transition(epsilon: float, *, pair_probability: float = 1.0) -> np.ndarray:
    """Return the mixed payload pair-flip and sector-refresh kernel."""

    if not 0.0 <= epsilon <= 1.0:
        raise ValueError("epsilon must lie in [0,1]")
    if not 0.0 <= pair_probability <= 1.0:
        raise ValueError("pair_probability must lie in [0,1]")
    pair_kernel = payload_pair_flip_transition(pair_probability, lazy=True)
    refresh_kernel = sector_refresh_transition()
    return (1.0 - epsilon) * pair_kernel + epsilon * refresh_kernel


def _validate_payload_mode_weight(mode_weight: int) -> None:
    if not 0 <= mode_weight <= PAYLOAD_BIT_COUNT:
        raise ValueError("mode_weight outside payload bit count")


def payload_pair_flip_eigenvalue(mode_weight: int, *, probability: float = 1.0) -> float:
    """Return the Walsh-mode eigenvalue for lazy payload pair flips."""

    _validate_payload_mode_weight(mode_weight)
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    base = (((PAYLOAD_BIT_COUNT - 2 * mode_weight) ** 2) - PAYLOAD_BIT_COUNT) / (
        PAYLOAD_BIT_COUNT * (PAYLOAD_BIT_COUNT - 1)
    )
    return float((1.0 - probability) + probability * base)


def sector_refresh_eigenvalue(mode_weight: int) -> float:
    """Return the Walsh-mode eigenvalue for one-bit payload refreshes."""

    _validate_payload_mode_weight(mode_weight)
    return float(1.0 - mode_weight / 4.0)


def mixed_sector_eigenvalue(
    mode_weight: int,
    epsilon: float,
    *,
    pair_probability: float = 1.0,
) -> float:
    """Return the Walsh-mode eigenvalue for the mixed sector kernel."""

    if not 0.0 <= epsilon <= 1.0:
        raise ValueError("epsilon must lie in [0,1]")
    return float(
        (1.0 - epsilon) * payload_pair_flip_eigenvalue(mode_weight, probability=pair_probability)
        + epsilon * sector_refresh_eigenvalue(mode_weight)
    )


def graph_distance_bound(left: Sequence[int], right: Sequence[int]) -> int:
    """Return the minimum number of pair-flip events between states."""

    a = normalize_bits(left)
    b = normalize_bits(right)
    if not is_integrity_valid(a) or not is_integrity_valid(b):
        raise ValueError("states must be parity-valid")
    distance = hamming_distance(a, b)
    if distance % 2:
        raise ValueError("parity-valid states must be separated by even Hamming distance")
    return distance // 2


def maximum_entropy_bits() -> float:
    """Return the entropy of the uniform admissible state law."""

    return log2(len(physical_state_space()))
