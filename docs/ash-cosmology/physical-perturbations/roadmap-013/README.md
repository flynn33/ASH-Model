# R-013 Physical Perturbation Equations and Matter-Sector Solver

This document records the bounded closure route for R-013: a finite-to-physical perturbation map, executable matter-sector solver, gauge/boundary policy, synthetic recovery tests, generated artifacts, and explicit non-claim boundaries.

## Upstream assumptions

R-008 through R-012 are assumed accepted and merged.

## Finite spectral input

\[
\lambda_L=(0,16,28,36,40), \qquad m=(1,9,36,84,126),
\]
with \(\sum_q m_q=256\).

## Unit-bearing kernel

\[
K_{\rm ASH}(k)=
e^{-\frac{1}{2}(\ln(k/k_*))^2/\sigma^2}
e^{-k^2/(2k_{\rm uv}^2)}
\sum_q \frac{c_q \cos(q\pi\log_2(k/k_*))}{1+\lambda_q/40}.
\]

Here \(k\) is a physical comoving wavenumber in Mpc\(^{-1}\).

## Growth equation

\[
D_{xx}+\left(2+\frac{d\ln H}{d\ln a}+\gamma_{\rm ASH}(a,k)\right)D_x
-\frac{3}{2}\Omega_m(a)\mu_{\rm ASH}(a,k)D=0.
\]

The boundary condition is \(D(a_i)=a_i\), \(D_x(a_i)=a_i\), \(a_i=10^{-3}\).

## Validation

The tests verify finite multiplicities, positive \(k\) validation, finite positive growth, zero-amplitude baseline consistency, and deterministic synthetic \(\alpha_\mu\) recovery.

## Non-claims

This is not a full photon-baryon Boltzmann hierarchy, not a calibrated survey power spectrum, not an empirical CMB prediction, and not an external likelihood.
