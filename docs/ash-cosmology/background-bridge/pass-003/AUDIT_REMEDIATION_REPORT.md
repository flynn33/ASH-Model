# Pass 003 Audit Remediation Report

## Scope

This pass remediates background-bridge audit gaps with a package-integrated,
deterministic synthetic-validation track. The work is limited to numerical
background observables and statistical diagnostics.

## Remediated Items

| Audit gap | Remediation |
|---|---|
| No package-level background bridge | Added `src/ash_model/background_bridge.py`. |
| Deprecated trapezoid integration risk | Uses `np.trapezoid` in distance integrals. |
| Missing synthetic recovery gate | Adds deterministic ASH synthetic data and parameter recovery. |
| Missing matched controls | Adds nested LCDM and smooth random-template controls. |
| Missing no-false-positive check | Fits ASH bridge to LCDM synthetic data and requires near-zero `beta_branch`. |
| Missing uncertainty reporting | Adds grid-posterior mean, standard deviation, and quantile summaries. |
| Missing model-comparison diagnostics | Adds AIC/BIC and coarse likelihood-grid diagnostics. |
| Missing convergence check | Compares 384-point and 768-point integration-grid fits. |

## Implemented Interface

The integrated module exposes:

```text
BackgroundParams
branch_entropy_template
e2_lcdm
e2_ash
H_ash
comoving_distance
luminosity_distance
angular_diameter_distance
distance_modulus
generate_synthetic_background
chi2_background
grid_fit
posterior_from_grid
information_criteria
grid_log_evidence
fit_lcdm_nested
random_matched_null_fit
convergence_diagnostics
run_validation
```

## Output Contract

`tools/run_background_bridge_validation.py` writes deterministic outputs under:

```text
validation/background_bridge/pass_003/outputs/
```

The summary includes `model_version`, `remediates_audit_findings`,
`posterior_uncertainty_grid`, `information_criteria`, `evidence_diagnostics`,
`convergence_diagnostics`, `acceptance_checks`, and `scientific_boundary`.

## Boundary

The bridge template is phenomenological. This pass does not add external-data
likelihoods, perturbation spectra, a full geometry theorem, or a physical
derivation of the bridge law.
