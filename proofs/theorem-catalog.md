# ASH Theorem Catalog

## FIN-001: finite state space

Status: computationally verified

Statement: ASH local finite states are represented in `F_2^9` with 512
possible bit strings before admissibility restrictions.

Proof location: `tools/run_proof_suite.py`

Executable verification: `tests/test_bits_hypercube.py`

## FIN-002: canonical code parameters

Status: computationally verified

Statement: The canonical ASH code has length 9, rank 4, size 16, minimum
distance 4, and doubly-even codeword weights.

Proof location: `tools/run_proof_suite.py`

Executable verification: `tests/test_code.py`

## FIN-003: single-bit correction

Status: implemented where decoder is invoked

Statement: For codewords in the canonical code, all single-bit corruptions
decode uniquely to the source codeword.

Executable verification: `tests/test_code.py`

## PHY-001: physical-state interpretation

Status: computationally verified for finite-observer scope

Statement: The finite-observer physical state space is the 256-state
parity-valid hyperplane of `F_2^9`.

Assumptions: The interpretation is finite and dimensionless.

Proof location: `theory/physical-postulates.md`

Executable verification: `tests/test_physics.py`

Limitations: This does not assign SI units or observed spacetime meaning.

## PHY-002: microscopic dynamics

Status: computationally verified for finite-observer scope

Statement: The lazy pair-flip transition kernel preserves admissibility, is
row-stochastic, is symmetric, and has the uniform admissible law stationary.

Definitions used: `ash_model.physics.pair_flip_transition`

Executable verification: `tests/test_physics.py`

Limitations: This is a finite stochastic dynamics, not a derived physical law.

## PHY-003: finite bridge map

Status: computationally verified for finite-observer scope

Statement: The bridge map sends a state law to mean Hamming weight, order
parameter, Shannon entropy, and parity-valid probability.

Definitions used: `ash_model.physics.bridge_observables`

Executable verification: `tests/test_physics.py`

Limitations: The observables are internal and dimensionless.

## PHY-004: finite background equation

Status: computationally verified

Statement: The Hamming-weight background kernel is the exact lumping of the
pair-flip transition kernel over even weights.

Definitions used: `ash_model.physics.weight_background_kernel`

Executable verification: `tests/test_physics.py`

Limitations: This is not a standard cosmological background equation.

## PHY-005: finite perturbation factors

Status: computationally verified

Statement: Lazy pair-flip perturbation-mode factors are bounded in `[-1,1]`
and the uniform mode has factor `1`.

Definitions used: `ash_model.physics.lazy_pair_flip_eigenvalue`

Executable verification: `tests/test_physics.py`

Limitations: This is not a metric perturbation or external power spectrum.

## EMP-001: calibration contract

Status: computationally verified

Statement: A finite internal observable can be mapped through an explicit
affine calibration into a named unit-bearing value.

Definitions used: `ash_model.empirical.ObservableCalibration`

Executable verification: `tests/test_empirical_bridge.py`

Limitations: This verifies the calibration contract, not the physical validity
of any calibration constants.

## EMP-002: diagonal Gaussian likelihood contract

Status: computationally verified

Statement: The empirical interface computes diagonal-covariance chi-square and
Gaussian log-likelihood values for finite vectors with positive standard
deviations.

Definitions used: `ash_model.empirical.diagonal_gaussian_log_likelihood`

Executable verification: `tests/test_empirical_bridge.py`

Limitations: This verifies likelihood arithmetic, not an external data fit.

## PRED-001: prediction-lock contract

Status: computationally verified

Statement: Frozen prediction-ledger entries can be assigned deterministic
canonical hashes and rejected when the stored hash does not match the entry
content.

Definitions used: `ash_model.prediction_ledger.canonical_prediction_hash`

Executable verification: `tests/test_prediction_ledger.py`

Limitations: This verifies ledger mechanics; no scientific prediction is
locked by the current repository ledger.
