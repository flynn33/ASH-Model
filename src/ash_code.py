"""
Skir canonical ASH code layer.

This module defines a parity-explicit rank-4 doubly-even linear [9,4,4]
code over F_2^9. Coordinate 9, represented by Python index 8, is the
parity/integrity coordinate for canonical codewords.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Literal, Sequence

Vector = tuple[int, ...]

DIM = 9
CODE_DIMENSION = 4
MIN_DISTANCE = 4
PARITY_COORDINATE = 9
PARITY_INDEX = 8
RESERVED_COORDINATES = (8,)

CANONICAL_TRANSFORMS: tuple[Vector, ...] = (
    (1, 1, 1, 1, 0, 0, 0, 0, 0),
    (1, 1, 0, 0, 1, 1, 0, 0, 0),
    (1, 0, 1, 0, 1, 0, 1, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1, 0, 1),
    (0, 0, 0, 0, 1, 1, 1, 0, 1),
)

GENERATOR_BASIS: tuple[Vector, ...] = CANONICAL_TRANSFORMS[:4]
CANONICAL_GENERATORS: tuple[Vector, ...] = CANONICAL_TRANSFORMS


@dataclass(frozen=True)
class DecodeResult:
    """Result of attempting to decode a 9-bit vector."""

    status: Literal["valid", "corrected", "ambiguous", "uncorrectable"]
    input: Vector
    corrected: Vector | None
    distance: int | None
    candidates: tuple[Vector, ...]


def normalize_vector(vector: Sequence[int]) -> Vector:
    """Return a checked 9-bit tuple."""
    if len(vector) != DIM:
        raise ValueError(f"expected {DIM} bits, got {len(vector)}")
    out = tuple(int(value) for value in vector)
    if any(value not in (0, 1) for value in out):
        raise ValueError("vector must contain only 0/1 bits")
    return out


def xor_vectors(*vectors: Sequence[int]) -> Vector:
    """XOR one or more 9-bit vectors."""
    if not vectors:
        return (0,) * DIM

    result = [0] * DIM
    for vector in vectors:
        checked = normalize_vector(vector)
        for index, bit in enumerate(checked):
            result[index] ^= bit
    return tuple(result)


def hamming_weight(vector: Sequence[int]) -> int:
    """Return the Hamming weight of a 9-bit vector."""
    return sum(normalize_vector(vector))


def hamming_distance(a: Sequence[int], b: Sequence[int]) -> int:
    """Return the Hamming distance between two 9-bit vectors."""
    av = normalize_vector(a)
    bv = normalize_vector(b)
    return sum(left ^ right for left, right in zip(av, bv))


def parity_first_eight(vector: Sequence[int]) -> int:
    """Return the parity of human coordinates 1 through 8."""
    checked = normalize_vector(vector)
    return sum(checked[:PARITY_INDEX]) % 2


def coordinate_9_matches_parity(vector: Sequence[int]) -> bool:
    """Return whether coordinate 9 matches parity of coordinates 1 through 8."""
    checked = normalize_vector(vector)
    return checked[PARITY_INDEX] == parity_first_eight(checked)


def is_doubly_even(vector: Sequence[int]) -> bool:
    """Return whether vector weight is divisible by 4."""
    return hamming_weight(vector) % 4 == 0


def span(generators: Iterable[Sequence[int]] = CANONICAL_GENERATORS) -> tuple[Vector, ...]:
    """Return the GF(2) closure of the supplied generators."""
    gens = tuple(normalize_vector(generator) for generator in generators)
    vectors: set[Vector] = set()

    for mask in product((0, 1), repeat=len(gens)):
        acc = (0,) * DIM
        for selected, generator in zip(mask, gens):
            if selected:
                acc = xor_vectors(acc, generator)
        vectors.add(acc)

    return tuple(sorted(vectors))


CANONICAL_CODEWORDS: tuple[Vector, ...] = span(GENERATOR_BASIS)
CANONICAL_CODEWORD_SET: frozenset[Vector] = frozenset(CANONICAL_CODEWORDS)


def gf2_rank(rows: Iterable[Sequence[int]]) -> int:
    """Compute row rank over GF(2)."""
    matrix = [list(normalize_vector(row)) for row in rows]
    rank = 0

    for column in range(DIM):
        pivot = next(
            (row_index for row_index in range(rank, len(matrix)) if matrix[row_index][column] == 1),
            None,
        )
        if pivot is None:
            continue

        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row_index, row in enumerate(matrix):
            if row_index != rank and row[column] == 1:
                matrix[row_index] = [left ^ right for left, right in zip(row, matrix[rank])]
        rank += 1

    return rank


def minimum_distance(codewords: Iterable[Sequence[int]] = CANONICAL_CODEWORDS) -> int:
    """Return the minimum pairwise Hamming distance for a codeword set."""
    words = tuple(normalize_vector(word) for word in codewords)
    if len(words) < 2:
        raise ValueError("need at least two codewords")
    return min(hamming_distance(left, right) for left, right in combinations(words, 2))


def weight_distribution(codewords: Iterable[Sequence[int]] = CANONICAL_CODEWORDS) -> dict[int, int]:
    """Return a Hamming-weight histogram for a codeword set."""
    distribution: dict[int, int] = {}
    for word in codewords:
        weight = hamming_weight(word)
        distribution[weight] = distribution.get(weight, 0) + 1
    return dict(sorted(distribution.items()))


def is_codeword(vector: Sequence[int]) -> bool:
    """Return whether a vector is a canonical codeword."""
    return normalize_vector(vector) in CANONICAL_CODEWORD_SET


def decode(vector: Sequence[int], *, max_correction_distance: int = 1) -> DecodeResult:
    """Decode by unique nearest canonical codeword."""
    received = normalize_vector(vector)
    if received in CANONICAL_CODEWORD_SET:
        return DecodeResult("valid", received, received, 0, (received,))

    distances = [
        (hamming_distance(received, codeword), codeword)
        for codeword in CANONICAL_CODEWORDS
    ]
    min_distance = min(distance for distance, _ in distances)
    candidates = tuple(codeword for distance, codeword in distances if distance == min_distance)

    if len(candidates) != 1:
        return DecodeResult("ambiguous", received, None, min_distance, candidates)
    if min_distance <= max_correction_distance:
        return DecodeResult("corrected", received, candidates[0], min_distance, candidates)
    return DecodeResult("uncorrectable", received, None, min_distance, candidates)


def validate_canonical_code() -> dict[str, object]:
    """Return computed properties used by tests and documentation."""
    return {
        "length": DIM,
        "rank": gf2_rank(CANONICAL_GENERATORS),
        "basis_rank": gf2_rank(GENERATOR_BASIS),
        "span_size": len(CANONICAL_CODEWORDS),
        "minimum_distance": minimum_distance(),
        "weight_distribution": weight_distribution(),
        "doubly_even": all(is_doubly_even(word) for word in CANONICAL_CODEWORDS),
        "coordinate_9_active": any(word[PARITY_INDEX] == 1 for word in CANONICAL_CODEWORDS),
        "coordinate_9_parity_valid": all(
            coordinate_9_matches_parity(word) for word in CANONICAL_CODEWORDS
        ),
        "reserved_coordinates": RESERVED_COORDINATES,
        "self_dual": False,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(validate_canonical_code(), indent=2))
