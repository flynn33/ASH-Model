# Matched Ablation Validation

Status: likelihood mechanics implemented; external ablations blocked

## Implemented controls

The repository now separates:

- the verified finite ASH code layer;
- the existing simulation controls in `ash_model.simulation`;
- the finite-observer pair-flip physics layer in `ash_model.physics`;
- the diagonal Gaussian likelihood and model-comparison interface in
  `ash_model.empirical`.

The pair-flip layer is intentionally simple and symmetric, which makes the
uniform stationary law and finite-mode decay factors auditable.

## External ablation blocker

Matched empirical ablations remain blocked until external observables, data
cuts, covariance sources, matched baseline predictions, and parameter counts
exist.  The likelihood interface exists; the external comparison package does
not.
