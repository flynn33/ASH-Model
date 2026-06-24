"""N=8 Adinkra quotient and an exact Garden-algebra representation.

Puncturing coordinate 8 of the canonical nine-bit transform code gives the
self-dual doubly-even [8,4,4] code C8.  The colored quotient graph Q8/C8 has
16 vertices, split into eight even and eight odd cosets.  The signed
permutation matrices below provide a dashing and satisfy the Garden algebra
exactly over the integers.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import Sequence

import numpy as np

from .bits import BitTuple, bits_to_int, hamming_weight, normalize_bits, xor_bits
from .code import punctured_codewords

I2 = np.asarray([[1, 0], [0, 1]], dtype=int)
X2 = np.asarray([[0, 1], [1, 0]], dtype=int)
Z2 = np.asarray([[1, 0], [0, -1]], dtype=int)
J2 = np.asarray([[0, 1], [-1, 0]], dtype=int)

_KRONECKER_FACTORS = {"I": I2, "X": X2, "Z": Z2, "J": J2}
# L1 is III.  The remaining seven words are pairwise anticommuting,
# antisymmetric signed-permutation matrices with square -I8.
_GARDEN_WORDS = ("III", "IIJ", "IJX", "XJZ", "ZJZ", "JZX", "JIZ", "JXX")

# A color relabeling that gives a color-preserving isomorphism between the
# quotient Q8/C8 coordinate colors and the matrix-edge colors.
QUOTIENT_TO_MATRIX_COLOR = (0, 1, 2, 4, 3, 7, 5, 6)


@dataclass(frozen=True)
class QuotientVertex:
    identifier: int
    representative: BitTuple
    parity: int
    members: tuple[BitTuple, ...]


@dataclass(frozen=True)
class AdinkraEdge:
    boson: int
    fermion: int
    color: int
    sign: int


def _kron_word(word: str) -> np.ndarray:
    return reduce(np.kron, (_KRONECKER_FACTORS[character] for character in word))


def garden_matrices() -> tuple[np.ndarray, ...]:
    """Return L_1,...,L_8 as exact 8x8 signed-permutation matrices."""

    return tuple(_kron_word(word) for word in _GARDEN_WORDS)


def verify_garden_algebra() -> dict[str, object]:
    """Verify L_I L_J^T + L_J L_I^T = 2 delta_IJ I_8 exactly."""

    matrices = garden_matrices()
    identity = np.eye(8, dtype=int)
    maximum_residual = 0
    signed_permutation = True
    for matrix in matrices:
        signed_permutation &= bool(
            np.all(np.sum(np.abs(matrix), axis=0) == 1)
            and np.all(np.sum(np.abs(matrix), axis=1) == 1)
        )
    for left_index, left in enumerate(matrices):
        for right_index, right in enumerate(matrices):
            target = 2 * identity if left_index == right_index else np.zeros((8, 8), dtype=int)
            residual = left @ right.T + right @ left.T - target
            maximum_residual = max(maximum_residual, int(np.max(np.abs(residual))))
    return {
        "matrix_count": len(matrices),
        "matrix_shape": [8, 8],
        "signed_permutation": signed_permutation,
        "maximum_integer_residual": maximum_residual,
        "garden_algebra_holds": maximum_residual == 0 and signed_permutation,
        "kronecker_words": list(_GARDEN_WORDS),
    }


def quotient_vertices() -> tuple[QuotientVertex, ...]:
    """Construct the 16 cosets of C8 in F_2^8."""

    code = set(punctured_codewords())
    universe = set(product((0, 1), repeat=8))
    raw_cosets: list[set[BitTuple]] = []
    while universe:
        representative = min(universe, key=bits_to_int)
        coset = {xor_bits(representative, codeword) for codeword in code}
        raw_cosets.append(coset)
        universe.difference_update(coset)
    raw_cosets.sort(key=lambda coset: bits_to_int(min(coset, key=bits_to_int)))
    vertices = []
    for identifier, coset in enumerate(raw_cosets):
        representative = min(coset, key=bits_to_int)
        vertices.append(
            QuotientVertex(
                identifier=identifier,
                representative=representative,
                parity=hamming_weight(representative) & 1,
                members=tuple(sorted(coset, key=bits_to_int)),
            )
        )
    return tuple(vertices)


def quotient_edges() -> tuple[tuple[int, int, int], ...]:
    """Return undirected colored edges (u,v,color) of Q8/C8."""

    vertices = quotient_vertices()
    member_to_vertex = {
        member: vertex.identifier for vertex in vertices for member in vertex.members
    }
    edges: set[tuple[int, int, int]] = set()
    for vertex in vertices:
        for color in range(8):
            unit = tuple(1 if index == color else 0 for index in range(8))
            adjacent_member = xor_bits(vertex.representative, unit)
            adjacent = member_to_vertex[adjacent_member]
            lower, upper = sorted((vertex.identifier, adjacent))
            edges.add((lower, upper, color))
    return tuple(sorted(edges))


def matrix_edges() -> tuple[AdinkraEdge, ...]:
    """Return the 64 signed colored edges encoded by the Garden matrices."""

    edges = []
    for color, matrix in enumerate(garden_matrices()):
        for boson in range(8):
            nonzero = np.flatnonzero(matrix[boson])
            if nonzero.size != 1:
                raise AssertionError("Garden matrix is not a signed permutation")
            fermion = int(nonzero[0])
            edges.append(
                AdinkraEdge(
                    boson=boson,
                    fermion=fermion,
                    color=color,
                    sign=int(matrix[boson, fermion]),
                )
            )
    return tuple(edges)


def quotient_matrix_isomorphism() -> dict[str, object]:
    """Derive and verify a color-preserving quotient-to-matrix isomorphism."""

    vertices = quotient_vertices()
    quotient_edge_lookup: dict[tuple[int, int], int] = {}
    for left, right, color in quotient_edges():
        quotient_edge_lookup[(left, color)] = right
        quotient_edge_lookup[(right, color)] = left

    matrix_permutations: list[list[int]] = []
    for matrix in garden_matrices():
        matrix_permutations.append(
            [int(np.flatnonzero(matrix[boson])[0]) for boson in range(8)]
        )

    even_vertices = [vertex.identifier for vertex in vertices if vertex.parity == 0]
    odd_vertices = [vertex.identifier for vertex in vertices if vertex.parity == 1]
    boson_map: dict[int, int] = {even_vertices[0]: 0}
    fermion_map: dict[int, int] = {}
    queue: list[tuple[str, int]] = [("boson", even_vertices[0])]

    while queue:
        kind, vertex_id = queue.pop(0)
        if kind == "boson":
            boson = boson_map[vertex_id]
            for quotient_color, matrix_color in enumerate(QUOTIENT_TO_MATRIX_COLOR):
                odd_id = quotient_edge_lookup[(vertex_id, quotient_color)]
                fermion = matrix_permutations[matrix_color][boson]
                prior = fermion_map.get(odd_id)
                if prior is not None and prior != fermion:
                    raise AssertionError("inconsistent quotient-to-matrix map")
                if prior is None:
                    fermion_map[odd_id] = fermion
                    queue.append(("fermion", odd_id))
        else:
            fermion = fermion_map[vertex_id]
            for quotient_color, matrix_color in enumerate(QUOTIENT_TO_MATRIX_COLOR):
                inverse = matrix_permutations[matrix_color].index(fermion)
                even_id = quotient_edge_lookup[(vertex_id, quotient_color)]
                prior = boson_map.get(even_id)
                if prior is not None and prior != inverse:
                    raise AssertionError("inconsistent quotient-to-matrix map")
                if prior is None:
                    boson_map[even_id] = inverse
                    queue.append(("boson", even_id))

    valid = len(boson_map) == 8 and len(fermion_map) == 8
    if valid:
        for even_id, boson in boson_map.items():
            for quotient_color, matrix_color in enumerate(QUOTIENT_TO_MATRIX_COLOR):
                odd_id = quotient_edge_lookup[(even_id, quotient_color)]
                valid &= fermion_map[odd_id] == matrix_permutations[matrix_color][boson]

    return {
        "valid": bool(valid),
        "quotient_vertex_count": len(vertices),
        "quotient_edge_count": len(quotient_edges()),
        "even_vertex_count": len(even_vertices),
        "odd_vertex_count": len(odd_vertices),
        "color_permutation_one_based": [value + 1 for value in QUOTIENT_TO_MATRIX_COLOR],
        "boson_map": {str(key): value for key, value in sorted(boson_map.items())},
        "fermion_map": {str(key): value for key, value in sorted(fermion_map.items())},
    }


def adinkra_certificate() -> dict[str, object]:
    garden = verify_garden_algebra()
    isomorphism = quotient_matrix_isomorphism()
    return {
        **garden,
        **isomorphism,
        "matrix_edge_count": len(matrix_edges()),
    }
