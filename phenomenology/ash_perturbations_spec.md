# ASH Perturbations Specification

Status: finite-observer perturbation interface implemented; Roadmap 007 quotient-shell refinement proposed.

## Boundary

This specification is finite-state and dimensionless. It does not define metric
perturbations, gauge-fixed relativistic perturbations, physical wavenumbers,
observed matter spectra, CMB spectra, or empirical redshift calibration.

## Variables

Perturbations are deviations from the uniform admissible state law:

```text
delta rho_t = rho_t - u
```

where `u` is uniform on the 256 parity-valid ASH states.

The native mode basis is the restricted Walsh-character basis on the admissible
even-parity hyperplane. Because labels `a` and `a + 111111111` agree on that
hyperplane, modes are grouped by quotient shell:

```text
q([a]) = min(HammingWeight(a), 9 - HammingWeight(a))
q in {0, 1, 2, 3, 4}
```

Shell multiplicities:

```text
q=0: 1
q=1: 9
q=2: 36
q=3: 84
q=4: 126
```

The `q=0` shell is the constant normalization mode. Zero-sum perturbations have
no exact constant component.

## Mode evolution

For pair-flip probability `p`, one lazy update multiplies a quotient-shell mode
by

```text
mu_q(p) = 1 - p + p K_2(q;9) / C(9,2)
```

where

```text
K_2(q;9) = C(9-q,2) - q(9-q) + C(q,2)
```

The non-lazy shell eigenvalues are:

```text
lambda_q = (1, 5/9, 2/9, 0, -1/9)
```

The finite-clock decay rates are:

```text
gamma_q = 1 - lambda_q = (0, 4/9, 7/9, 1, 10/9)
```

For a finite schedule `p_t`,

```text
T_q(t0,t1) = product_{s=t0}^{t1-1} mu_q(p_s)
```

and shell powers evolve as

```text
P_q(t1) = |T_q(t0,t1)|^2 P_q(t0)
```

## Source extension

A declared finite source may be represented by

```text
alpha_[a](t+1) = mu_q(p_t) alpha_[a](t) + s_[a](t)
```

with the retarded finite Green response:

```text
G_q(t,n) = product_{r=n+1}^{t-1} mu_q(p_r) for t > n
G_q(t,n) = 0 for t <= n
```

This is a finite recurrence and does not imply a physical source term in a
spacetime field equation.

## Implementation

- `ash_model.physics.pair_flip_transition`
- `ash_model.physics.pair_flip_eigenvalue`
- `ash_model.physics.lazy_pair_flip_eigenvalue`
- `ash_model.linear_perturbations.canonical_character_labels`
- `ash_model.linear_perturbations.spectral_shell_table`
- `ash_model.linear_perturbations.verify_character_eigenmodes`
- `tools/generate_linear_perturbations.py`

## Generated artifacts

The Roadmap 007 generator writes deterministic finite-observer artifacts to:

```text
data/ash-cosmology/linear-perturbations/v0.1/
validation/linear-perturbations/roadmap-007/outputs/
figures/ash-cosmology/linear-perturbations/v0.1/
```

The file `synthetic_redshift_transfer.csv` is a synthetic, dimensionless solver
test object only. It is not an empirical redshift calibration.

## Acceptance gates

- Character quotient count is exactly 256.
- Shell counts are exactly `1, 9, 36, 84, 126`.
- Eigenmode residual under the lazy pair-flip kernel is at most `1e-12`.
- Random shell-power transfer check has nonconstant relative error at most `1e-10`.
- Claim-language checks pass with no metric, empirical, or physical-spectrum overclaim.

## Out-of-scope gates

The following remain open and must not be implied by this specification:

- reviewed map from finite shell `q` to physical wavenumber `k`;
- unit-bearing time, distance, expansion, or light-cone bridge;
- gauge convention for relativistic perturbations;
- matter power spectrum or CMB angular spectrum;
- external data covariance and matched baseline;
- locked prospective scientific prediction.
