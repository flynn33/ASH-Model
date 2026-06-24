"""Canonical ASH transform code and strict recovery semantics.

The code C is generated over F_2 by the four rows below.  It is a rank-four,
length-nine, minimum-distance-four, doubly-even linear code.  Coordinate 9 is
active and satisfies the parity relation c_9 = c_1 xor ... xor c_8.  Coordinate
8 is invariant under code translations.  The nine-dimensional code is not
self-dual; puncturing coordinate 8 gives the doubly-even self-dual [8,4,4]
code used by the Adinkra quotient.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
from typing import Literal, Sequence

from .bits import (
    BIT_COUNT,
    BitTuple,
    bits_to_int,
    hamming_distance,
    hamming_weight,
    integrity_bit,
    normalize_bits,
    xor_bits,
)

GENERATOR_MATRIX: tuple[BitTuple, ...] = (
    (1, 1, 1, 1, 0, 0, 0, 0, 0),
    (1, 1, 0, 0, 1, 1, 0, 0, 0),
    (1, 0, 1, 0, 1, 0, 1, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 0, 1),
)

# A full-rank parity-check matrix H with G H^T = 0 over F_2.
PARITY_CHECK_MATRIX: tuple[BitTuple, ...] = (
    (1, 1, 1, 1, 0, 0, 0, 0, 0),
    (1, 1, 0, 0, 1, 1, 0, 0, 0),
    (1, 0, 1, 0, 1, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 0),
    (0, 1, 1, 0, 1, 0, 0, 0, 1),
)

MESSAGE_BITS = 4
INVARIANT_COORDINATE = 7  # zero-based coordinate 8
PARITY_COORDINATE = 8     # zero-based coordinate 9
ACTIVE_CODE_COORDINATES = (0, 1, 2, 3, 4, 5, 6, 8)


def _linear_combination(message: Sequence[int]) -> BitTuple:
    msg = normalize_bits(message, length=MESSAGE_BITS)
    result = (0,) * BIT_COUNT
    for bit, row in zip(msg, GENERATOR_MATRIX, strict=True):
        if bit:
            result = xor_bits(result, row)
    return result


def _all_message_codeword_pairs() -> tuple[tuple[BitTuple, BitTuple], ...]:
    pairs = [
        (tuple(message), _linear_combination(message))
        for message in product((0, 1), repeat=MESSAGE_BITS)
    ]
    return tuple(sorted(pairs, key=lambda pair: bits_to_int(pair[1])))


MESSAGE_CODEWORD_PAIRS = _all_message_codeword_pairs()
CODEWORDS: tuple[BitTuple, ...] = tuple(codeword for _, codeword in MESSAGE_CODEWORD_PAIRS)
CODEWORD_TO_MESSAGE = {codeword: message for message, codeword in MESSAGE_CODEWORD_PAIRS}
MESSAGE_TO_CODEWORD = {message: codeword for message, codeword in MESSAGE_CODEWORD_PAIRS}

# Six canonical nonzero masks retained as a compact transform palette.  They
# belong to the span of GENERATOR_MATRIX; the first four are a basis.
TRANSFORM_MASKS: tuple[BitTuple, ...] = (
    GENERATOR_MATRIX[0],
    GENERATOR_MATRIX[1],
    GENERATOR_MATRIX[2],
    GENERATOR_MATRIX[3],
    (1, 1, 1, 1, 1, 1, 1, 0, 1),
    (0, 0, 0, 0, 1, 1, 1, 0, 1),
)

DecodeStatus = Literal["exact", "corrected", "uncorrectable"]


@dataclass(frozen=True)
class DecodeResult:
    """Result of strict bounded-distance decoding.

    Decoding succeeds only at distance zero or one.  A unique nearest codeword
    at distance two is still rejected because d_min=4 does not identify the
    transmitted codeword safely beyond radius one.
    """

    status: DecodeStatus
    received: BitTuple
    codeword: BitTuple | None
    message: BitTuple | None
    distance: int
    nearest_count: int

    @property
    def succeeded(self) -> bool:
        return self.status in ("exact", "corrected")


@dataclass(frozen=True)
class AffineDecodeResult:
    """Recovery result for a translated code orbit anchor + C."""

    status: DecodeStatus
    received: BitTuple
    anchor: BitTuple
    recovered_state: BitTuple | None
    codeword: BitTuple | None
    message: BitTuple | None
    distance: int
    nearest_count: int

    @property
    def succeeded(self) -> bool:
        return self.status in ("exact", "corrected")


def encode(message: Sequence[int]) -> BitTuple:
    """Encode a four-bit message as a canonical ASH codeword."""

    return MESSAGE_TO_CODEWORD[normalize_bits(message, length=MESSAGE_BITS)]


def message_for(codeword: Sequence[int]) -> BitTuple:
    """Return the unique four-bit payload for a valid codeword."""

    word = normalize_bits(codeword)
    try:
        return CODEWORD_TO_MESSAGE[word]
    except KeyError as exc:
        raise ValueError("input is not an ASH codeword") from exc


def is_codeword(word: Sequence[int]) -> bool:
    return normalize_bits(word) in CODEWORD_TO_MESSAGE


def translate(state: Sequence[int], codeword: Sequence[int]) -> BitTuple:
    """Apply x -> x xor c, rejecting masks outside C."""

    state_bits = normalize_bits(state)
    word = normalize_bits(codeword)
    if word not in CODEWORD_TO_MESSAGE:
        raise ValueError("translation mask is not in the canonical code")
    return xor_bits(state_bits, word)


def decode(received: Sequence[int]) -> DecodeResult:
    """Nearest-codeword decoding with guaranteed radius one only."""

    word = normalize_bits(received)
    distances = [(hamming_distance(word, codeword), codeword) for codeword in CODEWORDS]
    minimum = min(distance for distance, _ in distances)
    nearest = [codeword for distance, codeword in distances if distance == minimum]
    if minimum <= 1 and len(nearest) == 1:
        codeword = nearest[0]
        status: DecodeStatus = "exact" if minimum == 0 else "corrected"
        return DecodeResult(
            status=status,
            received=word,
            codeword=codeword,
            message=CODEWORD_TO_MESSAGE[codeword],
            distance=minimum,
            nearest_count=1,
        )
    return DecodeResult(
        status="uncorrectable",
        received=word,
        codeword=None,
        message=None,
        distance=minimum,
        nearest_count=len(nearest),
    )


def decode_affine(received: Sequence[int], anchor: Sequence[int]) -> AffineDecodeResult:
    """Decode in the known affine orbit anchor + C.

    Branch states are generated as ``anchor xor codeword``.  XOR with the known
    anchor reduces recovery to decoding a codeword.  This is the only recovery
    policy used by the reference pipeline; it never silently guesses beyond
    one bit.
    """

    received_bits = normalize_bits(received)
    anchor_bits = normalize_bits(anchor)
    relative = xor_bits(received_bits, anchor_bits)
    result = decode(relative)
    recovered = None if result.codeword is None else xor_bits(anchor_bits, result.codeword)
    return AffineDecodeResult(
        status=result.status,
        received=received_bits,
        anchor=anchor_bits,
        recovered_state=recovered,
        codeword=result.codeword,
        message=result.message,
        distance=result.distance,
        nearest_count=result.nearest_count,
    )


def syndrome(word: Sequence[int]) -> BitTuple:
    """Compute H x^T over F_2."""

    bits = normalize_bits(word)
    return tuple(sum(a * b for a, b in zip(row, bits, strict=True)) & 1 for row in PARITY_CHECK_MATRIX)


def gf2_rank(rows: Sequence[Sequence[int]]) -> int:
    """Exact Gaussian-elimination rank over F_2."""

    if not rows:
        return 0
    column_count = len(rows[0])
    matrix = [list(normalize_bits(row, length=column_count)) for row in rows]
    rank = 0
    for column in range(column_count):
        pivot = next((index for index in range(rank, len(matrix)) if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row_index in range(len(matrix)):
            if row_index != rank and matrix[row_index][column]:
                matrix[row_index] = [
                    left ^ right
                    for left, right in zip(matrix[row_index], matrix[rank], strict=True)
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def weight_distribution(words: Sequence[Sequence[int]] = CODEWORDS) -> dict[int, int]:
    return dict(sorted(Counter(hamming_weight(word) for word in words).items()))


def minimum_distance(words: Sequence[Sequence[int]] = CODEWORDS) -> int:
    if len(words) < 2:
        raise ValueError("minimum distance requires at least two words")
    width = len(words[0])
    normalized = tuple(normalize_bits(word, length=width) for word in words)
    return min(
        hamming_distance(left, right)
        for left, right in combinations(normalized, 2)
    )


def dual_codewords() -> tuple[BitTuple, ...]:
    """Enumerate C^perp exactly in F_2^9."""

    dual = []
    for candidate in product((0, 1), repeat=BIT_COUNT):
        if all(sum(a * b for a, b in zip(candidate, codeword, strict=True)) % 2 == 0 for codeword in CODEWORDS):
            dual.append(tuple(candidate))
    return tuple(sorted(dual, key=bits_to_int))


def puncture_invariant_coordinate(word: Sequence[int]) -> BitTuple:
    """Remove coordinate 8, yielding the associated eight-bit code."""

    bits = normalize_bits(word)
    return bits[:INVARIANT_COORDINATE] + bits[INVARIANT_COORDINATE + 1 :]


def punctured_codewords() -> tuple[BitTuple, ...]:
    return tuple(sorted((puncture_invariant_coordinate(word) for word in CODEWORDS), key=bits_to_int))


def orbit(state: Sequence[int]) -> tuple[BitTuple, ...]:
    """Return the 16-state affine code orbit x + C."""

    bits = normalize_bits(state)
    return tuple(sorted((xor_bits(bits, codeword) for codeword in CODEWORDS), key=bits_to_int))


def coset_representative(state: Sequence[int]) -> BitTuple:
    """Canonical orbit representative: numerically least state in x + C."""

    return orbit(state)[0]


def code_certificate() -> dict[str, object]:
    """Return exact finite invariants used by the proof suite."""

    dual = dual_codewords()
    punctured = punctured_codewords()
    punctured_dual = []
    for candidate in product((0, 1), repeat=8):
        if all(sum(a * b for a, b in zip(candidate, word, strict=True)) % 2 == 0 for word in punctured):
            punctured_dual.append(tuple(candidate))
    return {
        "length": BIT_COUNT,
        "rank": gf2_rank(GENERATOR_MATRIX),
        "size": len(CODEWORDS),
        "minimum_distance": minimum_distance(),
        "weight_distribution": weight_distribution(),
        "doubly_even": all(hamming_weight(word) % 4 == 0 for word in CODEWORDS),
        "self_orthogonal": all(
            sum(a * b for a, b in zip(left, right, strict=True)) % 2 == 0
            for left in CODEWORDS
            for right in CODEWORDS
        ),
        "self_dual_in_f2_9": set(CODEWORDS) == set(dual),
        "dual_size": len(dual),
        "coordinate_8_invariant": all(word[INVARIANT_COORDINATE] == 0 for word in CODEWORDS),
        "coordinate_9_active": {word[PARITY_COORDINATE] for word in CODEWORDS} == {0, 1},
        "coordinate_9_parity": all(word[PARITY_COORDINATE] == integrity_bit(word[:8]) for word in CODEWORDS),
        "punctured_length": 8,
        "punctured_rank": gf2_rank(tuple(puncture_invariant_coordinate(row) for row in GENERATOR_MATRIX)),
        "punctured_minimum_distance": minimum_distance(punctured),
        "punctured_self_dual": set(punctured) == set(punctured_dual),
    }
