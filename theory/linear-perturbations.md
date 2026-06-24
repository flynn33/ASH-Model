# Linear Perturbations

Status: finite perturbation modes specified

## Perturbation variables

Perturbations are deviations of a state law from the uniform admissible law:

```text
delta rho_t = rho_t - u
```

where `u` is uniform on the 256 admissible states.

## Mode basis

For the finite-observer layer, perturbation modes are Walsh characters
restricted to the admissible state space.  Modes are grouped by Hamming
weight `k` of the character index.

## Linear evolution

Because the dynamics is already linear in `rho`,

```text
delta rho_{t+1} = delta rho_t P_p
```

For a mode of weight `k`, the lazy pair-flip decay factor is

```text
mu_k(p) = 1 - p + p K_2(k;9) / C(9,2)
```

with `K_2` defined in `theory/continuum-limit.md`.

## Stability

The repository verifies that all mode factors are bounded by one in absolute
value for the checked update probability.  This is finite-state linear
stability, not a metric perturbation result.

## Observable map

Current perturbation observables are internal mode decay factors and their
effect on the finite bridge observables.  No cosmic power spectrum or
large-scale-structure statistic is derived.

## Evidence

- `ash_model.physics.pair_flip_eigenvalue`
- `ash_model.physics.lazy_pair_flip_eigenvalue`
- `tests/test_physics.py`

## Verification status

Implemented and computationally verified for finite ASH perturbation modes.
