# Mathematical Accuracy Review - ASH Model Repository

**Review Date**: February 14, 2026  
**Status**: Updated for Skir

## Scope

This review tracks mathematical accuracy for repository source files and documentation. Skir narrows the validated claim set to code-theoretic properties and explicit simulation controls.

## Skir Code Layer

The canonical code implementation in `src/ash_code.py` is tested by `tests/test_ash_code.py`.

Validated properties:

- length 9
- rank 4
- span size 16
- minimum distance 4
- weight distribution `{0: 1, 4: 14, 8: 1}`
- coordinate 9 active as parity/integrity coordinate
- coordinate 9 equals parity of coordinates 1 through 8
- decoder corrects unique single-bit errors around canonical codewords
- decoder refuses silent correction of double-bit errors by default

## Simulation Boundary

`simulation.py`, `src/simulate.py`, and `tools/run_simulation_controls.py` demonstrate codeword transforms and noisy hypercube mixing. They do not independently prove runtime decoder correction or empirical physical cosmology.

## Current Verification Commands

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

## Recommendations

- Keep code-theoretic claims tied to `src/ash_code.py` and `tests/test_ash_code.py`.
- Keep simulation claims tied to control outputs.
- Keep broader interpretive claims out of ASH base documentation unless separately specified and tested.
