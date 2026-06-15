# ASH Model Consistency and Theoretical Accuracy Report

**Date**: February 14, 2026  
**Status**: Superseded by Skir claim-alignment work

## Scope

This report is retained as a historical consistency record. The Skir branch narrows the repository's claims to the properties that are implemented and tested:

- rank-4 doubly-even linear `[9,4,4]` canonical code
- coordinate 9 as parity/integrity coordinate
- explicit nearest-codeword decoder behavior
- reproducible noisy-mixing controls
- claim-audit checks for unsupported language

## Current Consistency Checks

Run these commands from the repository root:

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

## Current Findings

- The code layer is verified by `tests/test_ash_code.py`.
- Simulation scripts are demos and controls, not proof of decoder behavior.
- Documentation should use binomial/Haar noisy-mixing language where controls support it.
- Validation reports must not claim to certify all interpretive or physical claims.

## Historical Notes

Earlier versions of this report used broader validation language. Skir supersedes that framing with explicit code-theoretic tests and a narrower claim boundary.
