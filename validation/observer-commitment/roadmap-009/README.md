# Validation — R-009 Observer Commitment

This directory records deterministic validation outputs for the finite R-009 observer-commitment workbench.

## Regeneration

```bash
python tools/generate_observer_commitment.py --out-root . --depth 4 --pair-sample-limit 5000
```

## Required invariant checks

The validation JSON must report:

- `"passed": true`;
- frontier measure total equals 1 within tolerance;
- commitment distribution total equals 1 within tolerance;
- memory-prefix embedding passes;
- diagonal trace invariant passes.

## Boundary

Finite observer-relative commitment and branch-separation workbench only; no collapse claim, no Born-rule proof, no unitary Hilbert-space dynamics, no unit-bearing spacetime bridge, no CMB/matter-spectrum solver, and no empirical cosmology validation.
