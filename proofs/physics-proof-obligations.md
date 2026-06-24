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

## Remaining obligations

1. Unitful physical scale and time mapping.
2. Spacetime metric or explicit non-spacetime physical interpretation.
3. Gauge redundancy and physical degrees of freedom for any continuum reading.
4. Standard cosmological background or proof that no such limit exists.
5. External observable likelihood and matched baseline validation.
6. Locked prediction.

## Evidence

- `src/ash_model/physics.py`
- `tests/test_physics.py`
- `proofs/computational-certificate.json`
