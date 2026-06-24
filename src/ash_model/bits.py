"""Exact bit-level operations for the ASH 9-bit state space."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

BIT_COUNT = 9
BitTuple = tuple[int, ...]


def normalize_bits(bits: Iterable[int], *, length: int = BIT_COUNT) -> BitTuple:
    """Return an immutable binary tuple and reject malformed input."""

    values = tuple(int(value) for value in bits)
    if len(values) != length:
        raise ValueError(f"expected {length} bits, received {len(values)}")
    if any(value not in (0, 1) for value in values):
        raise ValueError("bit vectors may contain only 0 and 1")
    return values


def bits_to_int(bits: Sequence[int]) -> int:
    """Encode bits in display order, coordinate 1 as the most-significant bit."""

    value = 0
    for bit in normalize_bits(bits, length=len(bits)):
        value = (value << 1) | bit
    return value


def int_to_bits(value: int, *, length: int = BIT_COUNT) -> BitTuple:
    """Decode a non-negative integer using coordinate 1 as the MSB."""

    if not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value < 0 or value >= (1 << length):
        raise ValueError(f"value must be in [0, {1 << length})")
    return tuple((value >> shift) & 1 for shift in range(length - 1, -1, -1))


def xor_bits(left: Sequence[int], right: Sequence[int]) -> BitTuple:
    """Coordinate-wise addition in F_2."""

    a = normalize_bits(left, length=len(left))
    b = normalize_bits(right, length=len(a))
    return tuple(x ^ y for x, y in zip(a, b, strict=True))


def hamming_weight(bits: Sequence[int]) -> int:
    """Return the number of nonzero coordinates."""

    return sum(normalize_bits(bits, length=len(bits)))


def hamming_distance(left: Sequence[int], right: Sequence[int]) -> int:
    """Return Hamming distance between equal-length binary vectors."""

    return hamming_weight(xor_bits(left, right))


def parity(bits: Sequence[int]) -> int:
    """Return XOR parity of a binary vector."""

    return hamming_weight(bits) & 1


def integrity_bit(payload: Sequence[int]) -> int:
    """Return the ASH coordinate-9 parity for an eight-bit payload."""

    payload_bits = normalize_bits(payload, length=8)
    return parity(payload_bits)


def make_integrity_state(payload: Sequence[int]) -> BitTuple:
    """Append coordinate 9 so that total state parity is even."""

    payload_bits = normalize_bits(payload, length=8)
    return payload_bits + (integrity_bit(payload_bits),)


def is_integrity_valid(state: Sequence[int]) -> bool:
    """Test the canonical relation x_9 = x_1 xor ... xor x_8."""

    bits = normalize_bits(state)
    return bits[8] == integrity_bit(bits[:8])


def flip_bit(state: Sequence[int], coordinate: int) -> BitTuple:
    """Flip a zero-based coordinate in a binary state."""

    bits = list(normalize_bits(state, length=len(state)))
    if coordinate < 0 or coordinate >= len(bits):
        raise IndexError("coordinate outside state")
    bits[coordinate] ^= 1
    return tuple(bits)
