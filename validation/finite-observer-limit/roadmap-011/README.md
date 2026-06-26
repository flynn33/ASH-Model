# R-011 Validation Notes

This directory records validation evidence for the finite-observer limit closure.

## Scope

The validation checks finite graph and projection identities only. It does not validate physical spacetime, relativistic causality, FRW dynamics, perturbation physics, external data products, or empirical cosmology.

## Primary command

```bash
python tools/generate_finite_observer_limit.py --out-root . --refresh-figures
```

Expected generated output:

```text
data/ash-cosmology/finite-observer-limit/v0.1/r011_shells_cones_by_level.csv
data/ash-cosmology/finite-observer-limit/v0.1/r011_halved_cube_spectrum.csv
data/ash-cosmology/finite-observer-limit/v0.1/r011_projective_fibers.csv
data/ash-cosmology/finite-observer-limit/v0.1/r011_normalized_unit_scales.csv
data/ash-cosmology/finite-observer-limit/v0.1/r011_causal_interval_counts.csv
validation/finite-observer-limit/roadmap-011/outputs/verification.json
figures/ash-cosmology/finite-observer-limit/v0.1/r011_n9_shells_and_cones.png
figures/ash-cosmology/finite-observer-limit/v0.1/r011_n9_spectrum.png
figures/ash-cosmology/finite-observer-limit/v0.1/r011_projective_fibers.png
```

If `matplotlib` is unavailable, the CSV and JSON artifacts remain authoritative. Figure regeneration may be deferred or performed in the repository environment.

## Required assertions

`verification.json` should contain:

```json
{
  "r011_scope": "finite_observer_limit_closure_not_differentiable_continuum",
  "projective_consistency": true,
  "projection_lipschitz_on_events": true
}
```

The \(n=9\) shell counts must be:

```json
{"0": 1, "1": 36, "2": 126, "3": 84, "4": 9}
```

The \(n=9\) adjacency spectrum must be:

```json
[[0, 36, 1], [1, 20, 9], [2, 8, 36], [3, 0, 84], [4, -4, 126]]
```

## Failure semantics

Do not mark R-011 complete if any finite identity, projective consistency check, uniform-fiber check, event non-expansion check, or \(n=9\) spectrum/gap check fails.
