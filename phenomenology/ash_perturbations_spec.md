# ASH Perturbations Specification

Status: finite perturbation interface implemented

## Variables

Perturbations are deviations from the uniform admissible state law:

```text
delta rho_t = rho_t - u
```

Modes are grouped by Walsh-character Hamming weight `k`.

## Mode evolution

For pair-flip probability `p`, one update multiplies a weight-`k` mode by

```text
mu_k(p) = 1 - p + p K_2(k;9) / C(9,2)
```

## Implementation

- `ash_model.physics.pair_flip_eigenvalue`
- `ash_model.physics.lazy_pair_flip_eigenvalue`

## Acceptance gates

- Mode factors are bounded in `[-1,1]`.
- The uniform mode has factor `1`.
- The linear update is consistent with the stochastic pair-flip kernel.

## Boundary

These are finite-state perturbation modes.  They are not metric perturbations,
gauge-fixed spacetime perturbations, or a cosmic power spectrum.
