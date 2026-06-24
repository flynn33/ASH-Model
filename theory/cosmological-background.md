# Cosmological Background Equations

Status: finite background surrogate specified; physical cosmology not derived

## Background variables

The current background variables are finite-observer quantities:

```text
W_t(w): Hamming-weight probability over w in {0,2,4,6,8}
m_t: mean Hamming weight
phi_t = 1 - 2 m_t / 9
S_t: Shannon entropy in bits
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
phi = 0
S = 8 bits
```

This is an internal equilibrium baseline, not a standard cosmological model.

## Physical-cosmology boundary

No Friedmann equation, metric expansion law, matter content, radiation content,
dark-sector interpretation, or unitful time coordinate is derived here.  A
comparison to standard cosmological backgrounds remains a future model-building
task.

## Evidence

- `ash_model.physics.weight_background_kernel`
- `ash_model.physics.bridge_observables`
- `tests/test_physics.py`

## Verification status

Finite background surrogate implemented and verified.  Physical cosmological
background equations remain outside the current proved scope.
