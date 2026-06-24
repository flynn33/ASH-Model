# Cosmological Background Equations

Status: finite background surrogate specified; physical cosmology not derived

## Background variables

The current background variables are finite-observer quantities:

```text
W_t(w): Hamming-weight probability over w in {0,2,4,6,8}
m_t: mean Hamming weight
sigma_t^2: Hamming-weight variance
phi_t = 1 - 2 m_t / 9
S_t: Shannon entropy in bits
```

These variables are derived from the nine-dimensional hypercube state
geometry.  The full hypercube has distance-shell counts
`C(9,r)`, and the admissible even-parity hyperplane has Hamming-weight shells
`C(9,w)` for `w in {0,2,4,6,8}`.

The implemented moment map is:

```text
m_t = sum_w W_t(w) w
sigma_t^2 = sum_w W_t(w) (w - m_t)^2
phi_t = 1 - 2 m_t / 9
```

## Evolution law

The background law is the exact Hamming-weight lumping of the pair-flip
microscopic dynamics:

```text
W_{t+1} = W_t K_p
```

where `K_p` is implemented by
`ash_model.physics.weight_background_kernel(p)`.

## Baseline limit

The stationary baseline of this finite model is the uniform admissible state
law.  It has:

```text
m = 9/2
sigma^2 = 9/4
phi = 0
S = 8 bits
```

This is an internal equilibrium baseline, not a standard cosmological model.

The pair-flip event graph has finite Laplacian spectral gap `16`, giving an
exact relaxation invariant for the finite substrate.  A physical expansion
rate would require a separate unit-bearing bridge from this finite relaxation
scale to measured time and distance.

## Physical-cosmology boundary

No Friedmann equation, metric expansion law, matter content, radiation content,
dark-sector interpretation, or unitful time coordinate is derived here.  A
comparison to standard cosmological backgrounds remains a future model-building
task.

## Evidence

- `ash_model.physics.weight_background_kernel`
- `ash_model.physics.uniform_background_distribution`
- `ash_model.physics.background_moments`
- `ash_model.physics.evolve_weight_distribution`
- `ash_model.physics.bridge_observables`
- `ash_model.hypercube.even_parity_shell_counts`
- `ash_model.hypercube.pair_flip_laplacian_spectrum`
- `tests/test_physics.py`
- `tests/test_bits_hypercube.py`

## Verification status

Finite background surrogate implemented and verified.  Physical cosmological
background equations remain outside the current proved scope.
