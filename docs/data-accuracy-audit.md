# ASH Model Data Accuracy Audit

**Last Updated**: 2026-02-14  
**Status**: PASS for structural CSV checks

This audit checks whether `data/simulation-results.csv` is structurally consistent with the expectations encoded in `src/simulate.py`.

## Method

- Parse simulation constants (`NUM_AGENTS`, `DIM`, `TICKS`) directly from `src/simulate.py`.
- Parse `data/simulation-results.csv` with strict CSV validation.
- Check row count, column count, malformed rows, and basic state-distribution sanity metrics.
- Report transform parity implied by the simulation loop.

## Current Validation Command

```bash
python tools/audit_simulation_data.py
```

## Validation Boundary

This audit verifies CSV shape and selected computational consistency checks. It does not prove empirical physical claims or code-specific occupancy causation.

For Skir code properties and simulation controls, use:

```bash
python -m pytest -q
python tools/run_simulation_controls.py --quick
```

## Data Regeneration

To regenerate the CSV:

```bash
python src/simulate.py
```

This will create/update `data/simulation-results.csv` with fresh simulation data.
