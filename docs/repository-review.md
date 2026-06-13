# Repository Review and Consistency Check

Date: 2026-06-13

## Scope

Reviewed repository documentation and executable scripts for internal consistency, reproducibility guidance, and factual accuracy after the Skir update.

## Current Checks

Use:

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

## Consistency Findings

### 1. README structure

The root `README.md` lists the Skir canonical code module, tests, claim audit, controls, docs, simulation entry points, and data artifacts.

### 2. Simulation entry points

The repository exposes three distinct scripts:

- `simulation.py` for visualization output
- `src/simulate.py` for CSV output
- `tools/run_simulation_controls.py` for Skir control comparisons

### 3. Validation scope

The Skir branch separates code-theoretic validation from simulation demos. Decoder correction claims are tied to `src/ash_code.py` and `tests/test_ash_code.py`. Simulation controls support conservative noisy-mixing language only.

### 4. Dependency setup

The README and contribution guide list the required Python packages:

```bash
python -m pip install numpy matplotlib sympy pytest
```

## Summary

The current repository documentation is aligned with the Skir code layer and validation commands. Future updates should keep README, wiki pages, and validation reports in sync whenever scripts, file names, or claim language change.
