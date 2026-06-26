# Roadmap Status

## Roadmap Basis

The ASH Cosmology roadmap requires a bridge from branch-centered structures to
computable background observables before external cosmology comparisons can be
considered. Pass 003 provides a minimal synthetic-only implementation step.

## Completed

| Roadmap item | Status | Artifact |
|---|---|---|
| Candidate background bridge | Implemented | `src/ash_model/background_bridge.py` |
| Background observables | Implemented | `background_curves.csv` |
| Synthetic ASH dataset | Implemented | `generate_synthetic_background()` |
| Parameter recovery | Passed by validation | `validation_summary.json` |
| Nested LCDM control | Implemented | `fit_lcdm_nested()` |
| Matched smooth null | Implemented | `random_matched_null_fit()` |
| LCDM no-false-positive check | Implemented | `validation_summary.json` |
| Posterior uncertainty diagnostic | Implemented | `posterior_from_grid()` |
| AIC/BIC diagnostic | Implemented | `information_criteria()` |
| Convergence diagnostic | Implemented | `convergence_diagnostics()` |

## Still Open

| Item | Reason |
|---|---|
| External likelihoods | Premature until bridge and covariance contracts are frozen. |
| BAO/SNe adapters | Need reviewed data products and preregistered statistics. |
| Perturbation and CMB sector | Requires equations beyond homogeneous background observables. |
| Branch amplitude or measure law | Later branch-centered derivation work. |
| Full geometry bridge | Pass 003 is scalar background-only. |
| Locked predictions | Requires a frozen observable and rejection rule. |

## Dependency Status

Pass 003 can be used as an implementation dependency for later bridge,
perturbation, and falsification work, provided its synthetic-only scope is
preserved.
