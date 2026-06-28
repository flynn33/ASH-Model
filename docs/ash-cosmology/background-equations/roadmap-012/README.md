# R-012 Cosmological Background Equations and Standard-Baseline Relation

## Classification

- **Layer 1 — finite/algebraic relation:** \(\Omega_{\mathrm{ASH}}=0\) exactly recovers the standard \(\Lambda\)CDM-form background expression, and the finite ASH source is normalized so \(\Xi_{\mathrm{ASH}}(1)=1\).
- **Layer 2 — deterministic computation:** `src/ash_model/cosmological_background.py`, `tools/generate_cosmological_background.py`, and `tests/test_cosmological_background.py` generate and verify tables, synthetic observations, a grid recovery test, covariance output, figures, and validation JSON.
- **Layer 3 — interpretive workbench:** interpreting \(\Xi_{\mathrm{ASH}}(a)\) as a finite-observer background source is model-dependent and synthetic.

## Background equation

\[
E_{\mathrm{ASH}}^2(a)=\frac{H^2(a)}{H_0^2}
=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_k a^{-2}+\Omega_\Lambda
+\Omega_{\mathrm{ASH}}\Xi_{\mathrm{ASH}}(a).
\]

The source is

\[
\Xi_{\mathrm{ASH}}(a)=
\frac{\alpha S_b(a)+\beta D_b(a)+\gamma M_b(a)}
{\alpha+\beta+\gamma}.
\]

The implementation uses the canonical \(n=9\) parity layer with \(2^8=256\) admissible states.

## Standard-baseline relation

\[
\Omega_{\mathrm{ASH}}=0 \Rightarrow
E_{\mathrm{ASH}}^2(a)=
\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_k a^{-2}+\Omega_\Lambda.
\]

## Effective continuity proxy

\[
w_{\mathrm{ASH}}(a)=-1-\frac{1}{3}\frac{d\ln \Xi_{\mathrm{ASH}}}{d\ln a}.
\]

This is a background-level proxy for later work. It is not a fundamental stress-energy derivation.

## Verification

```bash
python tools/generate_cosmological_background.py --out-root . --refresh-figures
python -m pytest tests/test_cosmological_background.py
```

## Boundary

This closes a synthetic finite-observer background-equation workbench and standard-baseline relation only. It does not close perturbation equations, CMB/matter solvers, external likelihoods, empirical validation, or locked predictions.
