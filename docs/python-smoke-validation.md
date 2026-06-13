# Python Smoke Validation - Skir

## Scope

This report verifies syntax, script execution, selected code-theoretic properties, and claim-audit behavior for the Skir branch. It does not certify all interpretive, philosophical, or physical claims of ASH.

## Commands

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
```

## Validated code-theoretic properties

The canonical code module verifies:

- length 9;
- rank 4;
- closure size 16;
- doubly-even weights;
- minimum distance 4;
- coordinate 9 parity relation;
- coordinate 9 activity;
- single-bit correction by explicit decoder;
- no silent correction of double-bit errors by default.

## Validation boundary

The smoke validation does not prove:

- empirical physical cosmology;
- code-specific Gaussian emergence;
- runtime Hamming-bound resilience in simulations;
- quantum measurement statistics from L-system strings.
