# ASH Background Bridge - Pass 003 Audit Remediation

## Purpose

Pass 003 adds a scoped synthetic-validation track for the ASH background bridge.
It implements a deterministic phenomenological template that maps a branch
scalar into homogeneous background observables for controlled numerical tests.

## What Was Remediated

- A package module now computes `H(z)`, `D_M(z)`, `D_L(z)`, `D_A(z)`, and
  distance modulus from the bridge template.
- Numerical integration uses `np.trapezoid`.
- Synthetic ASH data recover injected `beta_branch` and `gamma_branch` values
  within fixed tolerances.
- Nested LCDM and matched smooth random-template controls are included.
- LCDM synthetic controls check that the bridge does not force nonzero
  `beta_branch`.
- Posterior grid uncertainty, AIC/BIC diagnostics, coarse grid likelihood
  diagnostics, and convergence diagnostics are reported.

## Synthetic Validation Only

This track uses synthetic data emitted from fixed bridge parameters. It is not
an external-data comparison and does not claim that the bridge is a continuum
cosmology law.

## Files

- `src/ash_model/background_bridge.py`
- `tests/test_background_bridge_remediation.py`
- `tools/run_background_bridge_validation.py`
- `validation/background_bridge/pass_003/`
- `docs/ash-cosmology/background-bridge/pass-003/`

## How To Run

```bash
python tools/run_background_bridge_validation.py
python -m pytest tests/test_background_bridge_remediation.py -q
```

## Acceptance Checks

The validation summary must report all checks as true:

- `recovers_beta_within_0p03`
- `recovers_gamma_within_0p30`
- `beats_nested_lcdm_on_ash_synthetic`
- `beats_random_matched_null_on_ash_synthetic`
- `does_not_force_beta_on_lcdm_synthetic`
- `posterior_std_positive`
- `convergence_384_to_768`

## Remaining Blockers

External likelihood adapters, BAO/SNe data products, perturbation-sector
derivations, production Bayesian inference, full stress-energy mapping, and
locked predictions remain future work.

## Scientific Boundary

Synthetic validation and statistical diagnostics only; no observational
validation claim is made.
