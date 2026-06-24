# ASH Background Specification

Status: finite background implemented

## Variables

```text
W_t(w), w in {0,2,4,6,8}
m_t = sum_w W_t(w) w
phi_t = 1 - 2 m_t / 9
S_t = entropy of the lifted state law
```

## Equation

```text
W_{t+1} = W_t K_p
```

where `K_p` is the exact Hamming-weight lumping of the pair-flip microscopic
kernel.

## Implementation

- `ash_model.physics.weight_background_kernel`
- `ash_model.physics.state_distribution_from_weights`
- `ash_model.physics.bridge_observables`

## Acceptance gates

- Kernel rows sum to one.
- The lifted state law matches direct state-kernel evolution.
- The uniform admissible law gives `m = 4.5`, `phi = 0`, and `S = 8`.

These gates are covered by `tests/test_physics.py`.

## Boundary

This is a finite background surrogate.  It is not a Friedmann background
equation and has no unitful cosmological time coordinate.
