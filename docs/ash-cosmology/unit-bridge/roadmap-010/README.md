# R-010 Unit-Bearing Bridge to Observables

## Status

This directory documents the Roadmap R-010 finite-observer unit-bearing bridge.

## Scope

R-010 introduces a versioned bridge

\[
\mathcal{B}_{\ell}:(\Gamma,\mathcal{T},\mu,\mathcal{M};\Theta_{\ell})\to\mathcal{Y}_{\ell}
\]

from finite branch-ensemble summaries to named unit-bearing proxy observables.

The finite feature vector is

\[
f_n=(n,\mathbb{E}_{\mu}q,\operatorname{Var}_{\mu}q,\mathbb{E}_{\mu}d,\mathbb{E}_{\mu}|M|,S_B,S_M,\chi_D).
\]

Here:

- \(q\) is shell index;
- \(d\) is defect count;
- \(|M|\) is committed-memory length;
- \(S_B\) is branch entropy;
- \(S_M\) is memory entropy;
- \(\chi_D\) is a finite branch-separation/decoherence summary from R-009.

## Unit-bearing map

Given calibration constants

\[
\Theta_{\ell}=(\tau_*,\ell_*,\epsilon_*,\alpha_S,\theta_0,\theta_q,G,c),
\]

the implemented bridge computes:

\[
t_n=\tau_* n,
\]

\[
L_n=\ell_*\sqrt{\mathbb{E}_{\mu}q/9},
\]

\[
a_n=\exp\{\alpha_S(S_B(n)-S_B(n_0))\},
\]

\[
H_n=\frac{\log a_n-\log a_{n-1}}{t_n-t_{n-1}},
\]

\[
\rho_E(n)=\frac{\epsilon_*\mathbb{E}_{\mu}d}{\ell_*^3},
\]

\[
\rho_m(n)=\rho_E(n)/c^2,
\]

\[
\mathcal{K}_n=\frac{8\pi G}{c^4}\rho_E(n),
\]

\[
M_{\mathrm{len}}(n)=\ell_*\mathbb{E}_{\mu}|M|,
\]

\[
T_n=\theta_0+\theta_q\mathbb{E}_{\mu}q/9.
\]

## Why this is beyond the affine placeholder

The prior observable contract allowed an affine mapping from dimensionless finite-observer values to named unit-bearing values. R-010 adds a versioned nonlinear synthetic bridge: entropy enters exponentially, expansion is a finite difference of log scale factor, and defect density is converted through dimensional constants into mass-density and curvature-proxy units.

## Calibration policy

The default constants in `config/ash_r010_unit_bridge_calibration.json` are fiducial synthetic defaults. They are not reviewed ASH physical constants.

Empirical use requires:

- provenance for each ASH-specific scale;
- data release identifier and access date;
- estimator definition;
- cuts, masks, and nuisance policy;
- covariance source;
- matched non-ASH controls;
- prediction lock before unblinding.

## Data products

Generated outputs live in:

```text
data/ash-cosmology/unit-bridge/v0.1/
```

Validation output lives in:

```text
validation/unit-bridge/roadmap-010/outputs/verification.json
```

## Verification

```bash
python tools/generate_unit_bridge.py --out-root .
python -m pytest tests/test_unit_bridge.py
```

## Boundary

This is a synthetic finite-observer bridge. It does not prove a physical metric, Einstein equations, FRW limit, LCDM relation, external likelihood, CMB/matter solver, or empirical cosmology.
