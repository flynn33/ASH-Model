# Physics Proof Obligations

Status: finite-observer obligations partially discharged

## Discharged finite-observer obligations

1. Physical state ontology: admissible states are parity-valid elements of
   `F_2^9`.
2. Microscopic dynamics: lazy pair-flip Markov kernel and continuous-time
   generator are defined.
3. Closure: pair flips preserve parity-valid admissibility.
4. Finite locality: one event flips exactly two coordinates.
5. Normalization and positivity: the stochastic kernel is row-stochastic and
   non-negative.
6. Stationary law: the uniform admissible law is stationary.
7. Background equation: Hamming-weight lumping is exact.
8. Perturbation stability: lazy pair-flip mode factors are bounded.
9. Bridge observables: dimensionless finite-observer observables are defined.
10. Calibration contract: finite dimensionless observables can be mapped
    through explicit named affine calibrations.
11. Likelihood contract: diagonal Gaussian comparisons reject invalid vector
    shapes and non-positive uncertainty.
12. Prediction-lock contract: frozen prediction entries can be hashed and
    validated before evaluation.
13. Standard-baseline contract: flat standard-baseline distance curves can be
    computed and ranked by the likelihood contract.

## Remaining obligations

1. Reviewed physical calibration constants for scale, time, and measured data
   products.
2. Spacetime metric or explicit non-spacetime physical interpretation.
3. Gauge redundancy and physical degrees of freedom for any continuum reading.
4. ASH-derived standard cosmological background or proof that no such limit
   exists.
5. External data product, covariance source, and matched baseline validation.
6. Locked scientific prediction.

## Evidence

- `src/ash_model/physics.py`
- `src/ash_model/empirical.py`
- `src/ash_model/prediction_ledger.py`
- `src/ash_model/cosmology.py`
- `tests/test_physics.py`
- `tests/test_empirical_bridge.py`
- `tests/test_prediction_ledger.py`
- `tests/test_cosmology.py`
- `proofs/computational-certificate.json`
