# Numerical Convergence Validation

Status: finite exact solver gate implemented; continuum convergence blocked

## Implemented finite gate

The current finite-observer layer does not require a numerical ODE/PDE solver.
It uses exact finite matrices:

- `pair_flip_transition(p)` over 256 states;
- `pair_flip_generator(lambda)` over 256 states;
- `weight_background_kernel(p)` over five Hamming-weight levels.

The gate verifies stochastic normalization, generator row sums, symmetry, and
bounded perturbation factors.

## Continuum blocker

Continuum convergence remains blocked because no continuum limit or continuum
equation is claimed.
