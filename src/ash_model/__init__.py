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
from .empirical import (
    CalibratedObservable,
    LikelihoodResult,
    ObservableCalibration,
    calibrate_observable,
    chi_square,
    compare_gaussian_models,
    diagonal_gaussian_log_likelihood,
)
from .physics import (
    PhysicsObservables,
    bridge_observables,
    pair_flip_transition,
    physical_state_space,
    uniform_physical_distribution,
    weight_background_kernel,
)
from .prediction_ledger import (
    canonical_prediction_hash,
    ledger_lock_status,
    validate_prediction_ledger,
)

__all__ = [
    "BIT_COUNT",
    "CODEWORDS",
    "GENERATOR_MATRIX",
    "CalibratedObservable",
    "PhysicsObservables",
    "DecodeResult",
    "LikelihoodResult",
    "ObservableCalibration",
    "bits_to_int",
    "calibrate_observable",
    "canonical_prediction_hash",
    "chi_square",
    "compare_gaussian_models",
    "decode",
    "decode_affine",
    "diagonal_gaussian_log_likelihood",
    "encode",
    "flip_bit",
    "hamming_distance",
    "hamming_weight",
    "int_to_bits",
    "integrity_bit",
    "is_integrity_valid",
    "ledger_lock_status",
    "make_integrity_state",
    "bridge_observables",
    "pair_flip_transition",
    "physical_state_space",
    "translate",
    "uniform_physical_distribution",
    "validate_prediction_ledger",
    "weight_background_kernel",
    "xor_bits",
]

__version__ = "1.1.0"
