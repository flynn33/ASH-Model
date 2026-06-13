# Python Code Validation Report

**Date**: 2026-02-14  
**Status**: Superseded by Skir smoke validation

This historical report is retained for traceability. Its scope is now limited to syntax, script execution, data-shape checks, and selected computational checks. It does not certify all interpretive, philosophical, or physical claims of ASH.

## Current Skir Validation Entry Points

Use the Skir validation report and commands in `docs/python-smoke-validation.md`.

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

## Validation Boundary

Validated surfaces:

- Python syntax and bytecode compilation
- JSON syntax for `axioms-of-existence.json`
- CSV shape and row-count checks for `data/simulation-results.csv`
- Selected code-theoretic checks in `src/ash_code.py`
- Claim-audit checks for Skir documentation language

Not validated by this report:

- empirical physical cosmology
- code-specific Gaussian emergence
- runtime Hamming-bound resilience in simulations
- quantum measurement statistics from L-system strings

## Current Recommendation

Treat this file as a historical smoke-validation note. For current acceptance, use:

- `docs/python-smoke-validation.md`
- `tools/audit_claims.py`
- `tools/run_simulation_controls.py`
- `tests/test_ash_code.py`
