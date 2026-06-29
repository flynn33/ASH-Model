# ASH R012–R016 Science Remediation Package

**Prepared:** 2026-06-28  
**Scope:** Independent scientific remediation artifacts for ASH-Model R012–R016 handoff. This package does not modify, manage, or propose version-control operations for the source repository.  
**Reference model:** Daley, J. (2026), *Adinkra-Stabilized Hypercube Model: Canonical Computational Specification and Reference Implementation*, version 1.1.0.

## Executive summary

The auditor's science-layer criticism is accepted as valid: R012–R016 in the current source are completed as synthetic/readiness/lock/contract workbenches, not as executed empirical cosmology. The current source itself states that R012–R016 do not close reviewed physical calibration, observed-data scoring, empirical preference, or full physical model validation.

This package performs the missing first-pass scientific work instead of only defining templates:

1. **R012 background derivation:** derives an exact finite ASH pair-flip spectrum on the 256-state admissible parity hyperplane and maps the two slowest nontrivial ASH modes into a concrete flat-FRW finite-spectral dark-sector equation.
2. **R014 real-data scoring:** fits the derived model to **DESI DR2 BAO Table IV** using published covariance correlations and compares it with flat ΛCDM and CPL `w0wa` baselines. It also performs a compressed Planck H0/Omega_m calibration.
3. **R013 perturbation/growth calculation:** derives and solves a sub-horizon matter-growth equation and calibrates the finite slow-mode scalar coupling to the DES Y3 S8 compression.
4. **R015 locked-prediction pilot execution:** scores the three current R015 locked templates against the new real-data pilot. P001 and P002 are **not confirmed** by this pilot; P003 receives only qualitative sign support.
5. **R016 closure certificate:** supplies a deterministic finite-kernel-to-observable model tuple and a machine-readable closure certificate with explicit remaining limitations.

This is still not a full ASH empirical validation. It is a concrete, reproducible first scientific execution of R012–R016 against external data.

## Canonical ASH inputs used

The current ASH source defines the finite core as a 9-bit state space with 256 admissible parity-valid states, a rank-four doubly-even `[9,4,4]` code, active coordinate 9 parity, invariant coordinate 8 under code actions, a strict radius-one decoder, and a lazy pair-flip finite-observer dynamics. The source also states that R012–R016 are complete only within synthetic-workbench, readiness, lock-mechanics, and formal-contract scopes, and that physical calibration, observed likelihood scoring, empirical preference, and physical model validation remain open.

The present work uses only the finite mathematical structure as an input. The continuum/FRW mapping below is a **new proposed extension**, not a claim already contained in the canonical ASH source.

## R012 — Actual background-equation derivation

Let

\[
X=\{x\in \mathbb F_2^9:x_9=x_1\oplus\cdots\oplus x_8\},
\qquad |X|=256.
\]

A pair flip in 9D toggles two coordinates and preserves admissibility. In the independent 8-bit payload coordinates, the induced move set contains all 8 one-bit flips and all 28 two-bit flips. For a Walsh character of payload Hamming weight `r`, the non-lazy eigenvalue is

\[
\mu_r = \frac{8-2r+\binom82-2r(8-r)}{36}
       = \frac{r^2-9r+18}{18}.
\]

For lazy probability `ell=1/2`,

\[
\eta_r = \frac12 + \frac12\mu_r,
\qquad
m_r=\binom8r.
\]

The exact shell spectrum is:

|   r |   multiplicity |   mu_nonlazy |   eta_lazy |   kappa_minus_ln_eta | parity_shell   |
|----:|---------------:|-------------:|-----------:|---------------------:|:---------------|
|   0 |              1 |     1        |   1        |            -0        | even           |
|   1 |              8 |     0.555556 |   0.777778 |             0.251314 | odd            |
|   2 |             28 |     0.222222 |   0.611111 |             0.492476 | even           |
|   3 |             56 |     0        |   0.5      |             0.693147 | odd            |
|   4 |             70 |    -0.111111 |   0.444444 |             0.81093  | even           |
|   5 |             56 |    -0.111111 |   0.444444 |             0.81093  | odd            |
|   6 |             28 |     0        |   0.5      |             0.693147 | even           |
|   7 |              8 |     0.222222 |   0.611111 |             0.492476 | odd            |
|   8 |              1 |     0.555556 |   0.777778 |             0.251314 | even           |

The two slowest nontrivial decay rates are

\[
\kappa_1=-\ln(\eta_1)= 0.251314428,\qquad
\kappa_2=-\ln(\eta_2)= 0.492476485.
\]

A finite-spectral clock gauge is fixed by setting `p1=1`; then

\[
p_2=\kappa_2/\kappa_1 = 1.959602910.
\]

The proposed ASH finite-spectral dark-sector density is

\[
\frac{\rho_X(a)}{\rho_{X0}}
=
\exp\left[b_1(a^{p_1}-1)+b_2(a^{p_2}-1)\right],
\]

with

\[
E^2(a)=\Omega_m a^{-3}+(1-\Omega_m)\rho_X(a)/\rho_{X0},
\]

and the derived equation of state

\[
w_X(a)
=
-1-\frac13\left(b_1p_1a^{p_1}+b_2p_2a^{p_2}\right).
\]

This is an actual physical-background ansatz derived from the finite ASH pair-flip spectrum. It is not a unique derivation of GR from ASH; it is a falsifiable finite-spectral FRW extension.

## R014 — Real DESI DR2 BAO likelihood and model comparison

The data vector uses DESI DR2 BAO Table IV:

- BGS isotropic `D_V/r_d` at `z=0.295`.
- Six anisotropic `D_M/r_d`, `D_H/r_d` bins from `z=0.510` through `z=2.330`.
- The published `D_M`–`D_H` correlation coefficient for each anisotropic bin.
- `r_d=147.09 Mpc`, with compact Planck calibration used in the Planck-prior fits.

The Gaussian BAO likelihood uses block covariance

\[
C_i=
\begin{pmatrix}
\sigma_{M,i}^2 & \rho_i\sigma_{M,i}\sigma_{H,i}\\
\rho_i\sigma_{M,i}\sigma_{H,i} & \sigma_{H,i}^2
\end{pmatrix}.
\]

Distances are

\[
D_H=\frac{c}{H(z)},\qquad
D_M=\frac{c}{H_0}\int_0^z\frac{dz'}{E(z')},
\qquad
D_V=(zD_M^2D_H)^{1/3}.
\]

### Fit results

| fit                            | model   |     chi2 |   dof |     AIC |     BIC |      H0 |   Omega_m | w0        | wa        | w0_eff    | wa_eff    |
|:-------------------------------|:--------|---------:|------:|--------:|--------:|--------:|----------:|:----------|:----------|:----------|:----------|
| DESI_DR2_BAO_only              | lcdm    | 10.5386  |    11 | 14.5386 | 15.6685 | 69.0392 |  0.297345 |           |           |           |           |
| DESI_DR2_BAO_plus_Planck_H0_Om | lcdm    | 16.2015  |    13 | 20.2015 | 21.6176 | 68.1383 |  0.312786 |           |           |           |           |
| DESI_DR2_BAO_only              | cpl     |  5.81207 |     9 | 13.8121 | 16.0719 | 62.0732 |  0.386167 | -0.183276 | -2.70549  |           |           |
| DESI_DR2_BAO_plus_Planck_H0_Om | cpl     |  8.45951 |    11 | 16.4595 | 19.2917 | 67.2812 |  0.314954 | -0.820373 | -0.534094 |           |           |
| DESI_DR2_BAO_only              | ash     |  5.93449 |     9 | 13.9345 | 16.1943 | 61.1331 |  0.391716 |           |           | 0.0686067 | -4.65299  |
| DESI_DR2_BAO_plus_Planck_H0_Om | ash     |  8.79898 |    11 | 16.799  | 19.6312 | 67.2353 |  0.313819 |           |           | -0.792809 | -0.812636 |

Interpretation:

- DESI-only BAO prefers extra dark-energy freedom over flat ΛCDM, as expected from the DESI DR2 discussion. The ASH finite-spectral model and CPL have nearly identical DESI-only fit quality.
- With compressed Planck H0/Omega_m priors, ASH has `chi2=8.799` for 15 data points and 4 parameters, compared with `chi2=16.201` for flat ΛCDM and `chi2=8.460` for CPL.
- Information criteria in the compressed fit favor extra dark-energy freedom over ΛCDM, but CPL remains slightly ahead of this minimal ASH finite-spectral model.

The best compressed ASH fit is:

\[
H_0 = 67.235337\,\mathrm{km\,s^{-1}\,Mpc^{-1}},
\quad
\Omega_m=0.313819,
\quad
b_1=1.271224,
\quad
b_2=-0.965909.
\]

It implies local effective dark-energy parameters

\[
w_0^{\rm eff}=-0.792809,
\qquad
w_a^{\rm eff}=-0.812636.
\]

## R013 — Matter growth and S8 calibration

For sub-horizon scalar growth, the package solves

\[
\frac{d^2D}{d(\ln a)^2}
+
\left[2+\frac{d\ln H}{d\ln a}\right]
\frac{dD}{d\ln a}
-
\frac32\Omega_m(a)\mu(a)D=0,
\]

with finite slow-mode coupling

\[
\mu(a)=1+\alpha_\mu a^{p_1}.
\]

Using the Planck amplitude `sigma8=0.811` as the early-amplitude normalization reference and comparing to the DES Y3 optimized-scale-cuts value `S8=0.772±0.017`, the ASH background alone gives

\[
S_8^{\rm ASH,bg} = 0.820367.
\]

The R015 locked positive coupling `alpha_mu=+0.07` gives

\[
S_8(\alpha_\mu=0.07) = 0.840450,
\]

which worsens the low-S8 direction. The calibrated finite-mode growth coupling required by the DES Y3 compression is

\[
\alpha_\mu = -0.174245,
\]

yielding

\[
S_8=0.772000.
\]

This is an actual perturbation/growth calculation and not a template. It is still a compressed S8 treatment, not a full weak-lensing covariance analysis.

## R015 — Locked prediction pilot scoring

The current R015 ledger freezes three prospective templates. This package pilot-scores them as follows.

### P001 — Late-time branch-entropy expansion residual

Locked claim: maximum `Delta_H/H=0.0029124783`, nonnegative over `0<=z<=2.5`, with `Delta_H/H(z=1)=0.0029019640`.

Pilot fit from DESI DR2 BAO + compressed Planck priors:

- maximum `Delta_H/H = 0.02455738` at `z=0.315`;
- `Delta_H/H(z=1) = 0.00912555`;
- minimum `Delta_H/H = -0.00060042` at `z=2.500`.

Assessment: **not confirmed by the pilot fit.** The data-calibrated finite-spectral background wants percent-level residuals and a small high-redshift sign crossing, unlike the locked sub-percent nonnegative envelope. This is not a formal ledger-level falsification because the exact preregistered external likelihood has not been run, but it is a substantive scientific warning.

### P002 — Finite-shell matter-spectrum residual template

Locked claim includes positive `alpha_mu=0.07` and a small oscillatory matter-spectrum ratio envelope.

Pilot S8 compression:

- `alpha_mu=+0.07` gives `S8=0.840450`;
- DES Y3 requires `alpha_mu=-0.174245`;
- the locked-positive-coupling S8 proxy is `4.026 sigma` high relative to the DES Y3 compressed uncertainty.

Assessment: **tension in sign and magnitude under the S8 proxy.** A full `P(k)` or shear covariance likelihood is still required for formal falsification.

### P003 — Low-ell finite-parity even/odd proxy sign

The exact finite spectrum gives

\[
A(\tau)=
\frac{\sum_{r\,odd}\binom8r\eta_r^{2\tau}-
\sum_{r>0,\,even}\binom8r\eta_r^{2\tau}}
{\sum_{r=1}^8\binom8r\eta_r^{2\tau}}.
\]

This proxy is positive for the tested relaxation interval. The locked value `A=0.0259117623` corresponds to

\[
\tau=1.398890356.
\]

Assessment: **sign consistent only.** CMB temperature literature reports an odd-over-even low-ell preference, but this package does not ingest Planck maps or run a low-ell likelihood.

## R016 — Formal closure certificate

This package supplies a finite-kernel-to-observable closure tuple:

\[
\mathcal M_{ASH-SDE}
=
(X,K_\ell,\operatorname{Spec}K_\ell,
\rho_X(a),E(a),D(a),\mathcal L_{BAO},\mathcal S_{R015}).
\]

Every output in the package is a deterministic function of:

1. the finite ASH admissible state space and pair-flip kernel;
2. the finite spectral clock gauge;
3. compact external observational inputs;
4. explicitly fitted parameters.

The machine-readable closure certificate is `outputs/r016_formal_closure_certificate.json`.

## Scientific conclusions

1. The finite ASH pair-flip kernel yields a real spectral calculus. This is a mathematically nontrivial bridge from the 256-state finite core to a falsifiable FRW dark-sector ansatz.
2. The minimal two-mode ASH finite-spectral background fits DESI DR2 BAO nearly as well as CPL under the compressed pilot likelihood and better than flat ΛCDM by chi-square and AIC.
3. The ASH finite-spectral model is not yet a validated cosmology. The best fit uses phenomenological calibration parameters and has not been tested against full SN, CMB, weak-lensing, or matter-spectrum covariance products.
4. The current R015 P001 and P002 locked templates are not supported by this first real-data pilot. P003 has only sign-level consistency.
5. The most important next science work is not more scaffolding; it is full covariance ingestion for Pantheon+/DES-SN, DESI likelihood products, weak-lensing or galaxy-clustering `P(k)`, and low-ell CMB map/likelihood evaluation.

## Remaining limitations

This package closes a concrete first scientific pass, not the whole ASH cosmology program. It does **not** include:

- a derivation of Einstein equations from ASH;
- a full photon-baryon Boltzmann solver;
- a map-level CMB likelihood;
- full Pantheon+/DES-SN covariance ingestion;
- full weak-lensing shear tomography or galaxy `P(k)` covariance;
- proof that ASH is the observed physical cosmology.

Those remain scientific tasks for future work.

## Package contents

- `scripts/reproduce_ash_r012_r016_science.py` — full reproduction script.
- `data/desi_dr2_bao_compact_table_iv.csv` — compact DESI DR2 BAO table.
- `data/compact_external_priors.csv` — Planck, SH0ES, and DES Y3 compressed inputs.
- `data/ash_pair_flip_spectrum.csv` — exact finite ASH pair-flip spectrum.
- `outputs/model_fit_summary.csv/json` — model comparison table.
- `outputs/bao_residuals_planck_compressed_fits.csv` — residual pulls.
- `outputs/growth_predictions.csv` — growth and S8 proxy predictions.
- `outputs/locked_prediction_pilot_scores.json/csv` — R015 pilot execution.
- `outputs/r016_formal_closure_certificate.json` — closure certificate.
- `formal/formal_expressions_latex.json` — machine-readable equations.
- `figures/*.png` — generated figures.
- `report/ASH_R012_R016_science_remediation_report.pdf` — PDF report.

## References

- ASH-Model README, current source: https://raw.githubusercontent.com/flynn33/ASH-Model/main/README.md
- ASH-Model ROADMAP, current source: https://raw.githubusercontent.com/flynn33/ASH-Model/main/ROADMAP.md
- ASH canonical finite code source: https://raw.githubusercontent.com/flynn33/ASH-Model/main/src/ash_model/code.py
- ASH R015 locked ledger: https://raw.githubusercontent.com/flynn33/ASH-Model/main/predictions/locked/r015_prediction_ledger.locked.json
- DESI Collaboration, DESI DR2 Results II, BAO measurements and constraints, 2025.
- Planck Collaboration, Planck 2018 Results VI, cosmological parameters, A&A 641, A6 (2020).
- Riess et al. 2022, SH0ES H0 measurement.
- DES Collaboration Y3 3x2pt S8 results.
- CMB low-ell parity anomaly literature cited in the package source notes.
