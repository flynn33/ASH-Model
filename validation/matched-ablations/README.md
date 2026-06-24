# Matched Ablation Validation

Status: internal controls specified; external ablations blocked

## Implemented controls

The repository now separates:

- the verified finite ASH code layer;
- the existing simulation controls in `ash_model.simulation`;
- the finite-observer pair-flip physics layer in `ash_model.physics`.

The pair-flip layer is intentionally simple and symmetric, which makes the
uniform stationary law and finite-mode decay factors auditable.

## External ablation blocker

Matched empirical ablations remain blocked until external observables,
likelihood, data cuts, and parameter counts exist.
