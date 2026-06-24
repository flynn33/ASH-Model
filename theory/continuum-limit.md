# Continuum or Finite-Observer Limit

Status: finite-observer substitute specified

## Decision

This branch does not claim an actual continuum limit.  It defines a
finite-observer substitute: exact evolution on the 256-state admissible state
space, exact nine-cube distance shells, an exact pair-flip graph spectrum, and
an exact five-level Hamming-weight background equation.

## Nine-cube shell geometry

For the full nine-dimensional hypercube `Q9`, every vertex has distance-shell
sizes:

```text
1, 9, 36, 84, 126, 126, 84, 36, 9, 1
```

The adjacency spectrum is `9-2r` with multiplicity `C(9,r)`, and the
unnormalized Laplacian spectral gap is `2`.  These are finite graph identities
for the model's state geometry.

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

The shell degeneracies are `(1, 36, 126, 84, 9)`, so the uniform admissible
state law induces `W_* = degeneracy / 256`.  The implemented moment map gives:

```text
m_* = 9/2
sigma_*^2 = 9/4
phi_* = 0
```

Finite-step background evolution is implemented by repeated application of
`K_p` and preserves normalization for every checked distribution.

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

The distance-two pair-flip graph on the admissible parity hyperplane has
Laplacian spectral gap `16`.  This supplies a finite relaxation scale for the
implemented stochastic substrate.  It does not define a continuum speed of
light, a metric tensor, or a physical diffusion constant without an additional
unit-bearing bridge.

## Boundary

This finite-observer substitute supplies exact finite equations.  It does not
derive a differentiable spacetime continuum, metric field, or field equation.

## Evidence

- `ash_model.physics.weight_background_kernel`
- `ash_model.physics.background_moments`
- `ash_model.physics.evolve_weight_distribution`
- `ash_model.physics.lazy_pair_flip_eigenvalue`
- `ash_model.hypercube.distance_shell_counts`
- `ash_model.hypercube.hypercube_laplacian_spectrum`
- `ash_model.hypercube.pair_flip_laplacian_spectrum`
- `tests/test_physics.py`
- `tests/test_bits_hypercube.py`

## Verification status

Implemented and computationally verified for the finite-observer substitute.
