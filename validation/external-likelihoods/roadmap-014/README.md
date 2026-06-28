# R-014 Validation Notes

This validation directory records synthetic external-likelihood readiness for R-014.

## Products

- `outputs/verification.json`: deterministic synthetic validation summary.
- `outputs/r014_preregistration_lock.json`: synthetic-fixture freeze metadata.

## Interpretation

The validation artifacts demonstrate that the finite Gaussian likelihood, covariance handling, matched baselines, and synthetic recovery tests execute reproducibly. They do **not** constitute empirical cosmology validation because no external data vector or official covariance product is bundled or scored.

## Failure gates

R-014 readiness fails if:

- covariance inputs are not SPD and no predeclared regularization policy is locked;
- data or covariance hashes change after unblinding;
- matched baselines are omitted;
- the synthetic recovery errors exceed the declared tolerances;
- a claimed ASH-specific signature is matched or beaten by a preregistered non-ASH control.
