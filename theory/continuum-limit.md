# Continuum or Finite-Observer Limit

Status: finite-observer substitute specified

## Decision

This branch does not claim an actual continuum limit.  It defines a
finite-observer substitute: exact evolution on the 256-state admissible state
space and an exact five-level Hamming-weight background equation.

## Background equation

Let `W_t(w)` be the probability that the state has Hamming weight `w`, where

```text
w in {0, 2, 4, 6, 8}
```

Under the lazy pair-flip kernel with probability `p`,

```text
W_{t+1} = W_t K_p
```

where

```text
K_p(w, w-2) = p C(w,2) / C(9,2)
K_p(w, w)   = 1 - p + p w(9-w) / C(9,2)
K_p(w, w+2) = p C(9-w,2) / C(9,2)
```

with terms outside `{0,2,4,6,8}` omitted.

## Perturbation-mode factors

For a Walsh mode of Hamming weight `k`, the non-lazy pair-flip eigenvalue is

```text
lambda_k = K_2(k; 9) / C(9,2)
```

where

```text
K_2(k; 9) =
  C(9-k,2) - k(9-k) + C(k,2)
```

The lazy one-step decay factor is

```text
mu_k(p) = 1 - p + p lambda_k
```

The repository verifies that these factors are bounded in `[-1,1]`.

## Boundary

This finite-observer substitute supplies exact finite equations.  It does not
derive a differentiable spacetime continuum, metric field, or field equation.

## Evidence

- `ash_model.physics.weight_background_kernel`
- `ash_model.physics.lazy_pair_flip_eigenvalue`
- `tests/test_physics.py`

## Verification status

Implemented and computationally verified for the finite-observer substitute.
