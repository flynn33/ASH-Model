# ASH Model Data Accuracy Audit

This audit checks whether `data/simulation-results.csv` is structurally and numerically consistent with the expectations encoded in `src/simulate.py`.

## Method

- Parsed simulation constants (`NUM_AGENTS`, `DIM`, `TICKS`) directly from `src/simulate.py`.
- Parsed `data/simulation-results.csv` with strict CSV validation.
- Checked row count, column count, malformed rows, and basic state-distribution sanity metrics.
- Verified model transform parity implied by the simulation loop.

## Findings

1. **Row count mismatch**: simulation configuration expects `NUM_AGENTS = 1000`, but the CSV contains only **864 valid rows**.
2. **Malformed data present**: one row is truncated (line 866) with only 3 columns instead of 9.
3. **Structural expectations**: header column count and valid row width are both 9 (matching `DIM = 9`).
4. **Model parity implication**: with `TICKS = 1000` and a fixed transform vector applied every tick, the net adinkra transform is identity (even parity), so the final state should equal the initial state absent additional noise.

## Reproducible Command

```bash
python tools/audit_simulation_data.py
```

Current result: **FAIL** due to row count mismatch and malformed CSV row.

## Recommended Remediation

- Regenerate `data/simulation-results.csv` from `src/simulate.py` in a fully provisioned Python environment.
- Add this audit script to CI so malformed or incomplete data files fail fast.
- Optionally include an explicit random seed in `src/simulate.py` for reproducible data snapshots.
