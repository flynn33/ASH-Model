"""ASH Model deterministic reference implementation.

The public surface deliberately separates:

* the 512-state hypercube :math:`F_2^9`;
* the parity-valid application-state hyperplane;
* the canonical rank-four doubly-even ``[9, 4, 4]`` transform code;
* the punctured ``[8, 4, 4]`` code used for the N=8 Adinkra quotient;
* deterministic feature, branch, reconstruction, and validation layers.
"""

from .bits import (
    BIT_COUNT,
    bits_to_int,
    flip_bit,
    hamming_distance,
    hamming_weight,
    int_to_bits,
    integrity_bit,
    is_integrity_valid,
    make_integrity_state,
    xor_bits,
)
from .code import (
    CODEWORDS,
    GENERATOR_MATRIX,
    DecodeResult,
    decode,
    decode_affine,
    encode,
    translate,
)

__all__ = [
    "BIT_COUNT",
    "CODEWORDS",
    "GENERATOR_MATRIX",
    "DecodeResult",
    "bits_to_int",
    "decode",
    "decode_affine",
    "encode",
    "flip_bit",
    "hamming_distance",
    "hamming_weight",
    "int_to_bits",
    "integrity_bit",
    "is_integrity_valid",
    "make_integrity_state",
    "translate",
    "xor_bits",
]

__version__ = "1.1.0"
