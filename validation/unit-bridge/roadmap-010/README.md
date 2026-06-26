# R-010 Unit-Bridge Validation

## Purpose

This directory records deterministic validation evidence for the Roadmap R-010 unit-bearing bridge.

## Generated artifact

```text
outputs/verification.json
```

The validation JSON records:

- normalized branch measure by depth;
- presence of named unit-bearing columns;
- positive declared scale constants;
- finite physical-proxy output values;
- symmetric covariance;
- positive-semidefinite covariance up to floating-point tolerance;
- boundary statement.

## Regeneration

```bash
python tools/generate_unit_bridge.py --out-root .
```

## Boundary

The validation artifact is synthetic and repository-local. It is not an external observational covariance, likelihood, or empirical validation result.
