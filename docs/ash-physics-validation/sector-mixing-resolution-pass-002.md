# ASH-Physics Sector-Mixing Resolution Pass 002

## Scope

This page records a finite ASH-Physics workbench extension for payload-sector
mixing.  It does not replace the repository's existing nine-coordinate
finite-observer pair-flip kernel in `src/ash_model/physics.py`.

The existing kernel acts on the 256 parity-valid ASH states using pair flips
over all nine coordinates.  This pass adds a separate eight-payload-coordinate
workbench in which the ninth integrity coordinate is recomputed from the
payload after each refresh.

## Model

Let the payload state be an element of `F_2^8`.  The corresponding ASH state is

```text
(x_1, ..., x_8, x_1 xor ... xor x_8)
```

The payload pair-flip kernel flips an unordered pair of payload coordinates.
That kernel preserves the parity sector of the eight-bit payload Hamming
weight, so the payload state graph splits into two 128-state communicating
classes when no sector refresh is present.

The sector-refresh kernel flips one payload coordinate uniformly and then
recomputes the integrity bit.  The mixed workbench kernel is

```text
K_epsilon = (1 - epsilon) K_pair + epsilon S
```

where `S` is the sector-refresh kernel.

## Repository Integration

The implementation is provided as a named extension:

- `payload_state_space()`
- `payload_to_physical_state(payload)`
- `payload_pair_flip_transition(probability=1.0, lazy=True)`
- `sector_refresh_transition()`
- `mixed_sector_transition(epsilon, pair_probability=1.0)`
- `payload_pair_flip_eigenvalue(mode_weight, probability=1.0)`
- `sector_refresh_eigenvalue(mode_weight)`
- `mixed_sector_eigenvalue(mode_weight, epsilon, pair_probability=1.0)`

The imported research bundle is tracked under:

- `data/ash-physics-sector-mixing/`
- `figures/ash-physics-sector-mixing/`
- `docs/ash-physics-validation/reports/sector-mixing-resolution-report.pdf`
- `proofs/sector-mixing-resolution.md`
- `config/ash_physics_sector_mixing_v1.json`

The reproduction command is:

```bash
python tools/reproduce_sector_mixing.py --output-dir .
```

## Validation Status

This pass verifies finite workbench properties:

- the pair-only payload kernel has two 128-state parity sectors;
- the sector-refresh kernel flips payload parity while preserving ASH
  admissibility after integrity-bit recomputation;
- the mixed kernel is stochastic, symmetric, and has the uniform 256-state
  payload law as a stationary distribution;
- the finite spectrum matches the closed-form Walsh-mode formula;
- the former sector mode shifts from eigenvalue `1` to `1 - 2 epsilon`.

`epsilon` is a finite-observer sector-refresh parameter for this workbench.  It
is not a measured physical constant and is not an empirical cosmology result.
