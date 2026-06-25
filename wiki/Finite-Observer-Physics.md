# Finite-Observer Physics

ASH-Physics v0.2 is a conservative finite-state layer built over the verified ASH kernel.

## Implemented finite layer

| Item | Status |
|---|---|
| Admissible physical state space | 256 parity-valid states |
| Microscopic update | lazy pair-flip Markov kernel |
| Continuous-time form | finite generator |
| Event graph | finite pair-flip graph |
| Background surrogate | Hamming-weight lumping |
| Perturbation layer | bounded lazy pair-flip mode factors |
| Observables | dimensionless internal vector |
| Calibration | explicit affine contract for future unit-bearing quantities |
| Prediction ledger | hash-lock mechanics without locked entries |

## Boundary

This layer is finite and dimensionless. It is not a unit-bearing spacetime theory, not a metric derivation, not an external-data likelihood result, and not an empirical cosmology claim.

## Implementation evidence

- `src/ash_model/physics.py`
- `src/ash_model/empirical.py`
- `src/ash_model/cosmology.py`
- `tests/test_physics.py`
- `tests/test_empirical_bridge.py`
- `tests/test_cosmology.py`
- `theory/`
- `phenomenology/`

## Open transition

The next scientific step is not more repository scaffolding. It is a reviewed physical bridge from finite ASH states to unit-bearing observables, followed by external datasets, covariance models, matched baselines, and frozen predictions.
