"""The 9-dimensional ASH hypercube (Enneahcube) and orbit partitions."""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb, pi
from typing import Sequence

import numpy as np

from .bits import (
    BIT_COUNT,
    BitTuple,
    bits_to_int,
    flip_bit,
    hamming_weight,
    int_to_bits,
    is_integrity_valid,
    normalize_bits,
)
from .code import CODEWORDS, coset_representative, decode


def states() -> tuple[BitTuple, ...]:
    """Enumerate all 512 vertices in integer order."""

    return tuple(int_to_bits(index) for index in range(1 << BIT_COUNT))


def integrity_states() -> tuple[BitTuple, ...]:
    """Enumerate the 256 states satisfying coordinate-9 parity."""

    return tuple(state for state in states() if is_integrity_valid(state))


def neighbors(state: Sequence[int]) -> tuple[BitTuple, ...]:
    """Return the nine Q_9 neighbors in coordinate order."""

    bits = normalize_bits(state)
    return tuple(flip_bit(bits, coordinate) for coordinate in range(BIT_COUNT))


def plane(state: Sequence[int]) -> int:
    """Canonical state-to-plane mapping: Hamming weight 0 through 9."""

    return hamming_weight(state)


def theoretical_plane_counts() -> tuple[int, ...]:
    return tuple(comb(BIT_COUNT, weight) for weight in range(BIT_COUNT + 1))


def observed_plane_counts(collection: Sequence[Sequence[int]]) -> tuple[int, ...]:
    counts = Counter(plane(state) for state in collection)
    return tuple(counts.get(weight, 0) for weight in range(BIT_COUNT + 1))


def coset_partition(*, integrity_only: bool = False) -> tuple[tuple[BitTuple, ...], ...]:
    """Partition F_2^9 (or the parity hyperplane) into affine C-orbits."""

    universe = integrity_states() if integrity_only else states()
    groups: dict[BitTuple, tuple[BitTuple, ...]] = {}
    for state in universe:
        representative = coset_representative(state)
        if representative not in groups:
            members = tuple(sorted((tuple(a ^ b for a, b in zip(state, word, strict=True)) for word in CODEWORDS), key=bits_to_int))
            groups[representative] = members
    return tuple(groups[key] for key in sorted(groups, key=bits_to_int))


def projection_coordinates(state: Sequence[int]) -> tuple[float, float, float]:
    """Deterministic 9D-to-3D linear projection used by generated figures.

    Bits are mapped to {-1,+1}.  The first two rows lie on a regular nonagon;
    the third row alternates sign and is normalized.  This is a visualization,
    not an isometry and not evidence for physical geometry.
    """

    bits = np.asarray(normalize_bits(state), dtype=float)
    signed = 2.0 * bits - 1.0
    angles = 2.0 * pi * np.arange(BIT_COUNT) / BIT_COUNT
    matrix = np.vstack(
        [
            np.cos(angles),
            np.sin(angles),
            np.asarray([1.0 if index % 2 == 0 else -1.0 for index in range(BIT_COUNT)]),
        ]
    )
    matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    point = matrix @ signed
    return float(point[0]), float(point[1]), float(point[2])


def state_reference_rows() -> list[dict[str, object]]:
    """Build the exhaustive 512-state reference table."""

    rows: list[dict[str, object]] = []
    representative_to_id = {
        orbit[0]: orbit_id for orbit_id, orbit in enumerate(coset_partition())
    }
    for index, state in enumerate(states()):
        result = decode(state)
        representative = coset_representative(state)
        rows.append(
            {
                "index": index,
                "bits": "".join(str(bit) for bit in state),
                "hamming_weight": hamming_weight(state),
                "integrity_valid": int(is_integrity_valid(state)),
                "coset_id": representative_to_id[representative],
                "coset_representative": "".join(str(bit) for bit in representative),
                "nearest_code_distance": result.distance,
                "nearest_codeword_count": result.nearest_count,
                "decoder_status": result.status,
            }
        )
    return rows
