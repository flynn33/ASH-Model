# Blocker Register

## Resolved In Pass 003

### B003-1: No Computable Background Bridge

Resolved by adding a fixed scalar branch template and background-observable
functions for `H(z)`, `D_M(z)`, `D_L(z)`, `D_A(z)`, and `mu(z)`.

### B003-2: No Synthetic Recovery Gate

Resolved by deterministic synthetic ASH data and grid recovery of injected
`beta_branch` and `gamma_branch`.

### B003-3: No Matched Null Comparison

Resolved by nested LCDM and matched smooth random-template controls.

### B003-4: No Numerical Remediation Checks

Resolved by `np.trapezoid`, posterior-grid uncertainty, AIC/BIC diagnostics,
and 384-to-768 integration-grid convergence checks.

## Still Open

### B003-O1: Bridge Is Phenomenological

The scalar branch template is a candidate bridge. It is not yet derived from a
microscopic branch measure or amplitude law.

### B003-O2: No Perturbation Sector

This pass cannot produce matter-power spectra, CMB spectra, growth functions,
or gravitational-wave propagation corrections.

### B003-O3: No External-Data Inference

External data comparison is deferred until the bridge, covariance handling,
and perturbation-sector adapters are frozen.

### B003-O4: No Full Stress-Energy Mapping

The bridge contributes to `E(z)^2`, but does not derive `rho`, `p`, or an
equation of state from first principles.

### B003-O5: No Production Bayesian Inference

The posterior is a coarse grid diagnostic. A production sampler, priors,
coverage tests, and model-comparison protocol remain future work.

### B003-O6: No Locked Prediction

This pass creates no prospective prediction ledger entry.
