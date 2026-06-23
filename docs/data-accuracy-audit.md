# ASH Model Data Accuracy Audit

**Last Updated**: 2026-02-14  
**Status**: ✅ PASS

This audit checks whether `data/simulation-results.csv` is structurally and numerically consistent with the expectations encoded in `src/simulate.py`.

## Method

- Parsed simulation constants (`NUM_AGENTS`, `DIM`, `TICKS`) directly from `src/simulate.py`.
- Parsed `data/simulation-results.csv` with strict CSV validation.
- Checked row count, column count, malformed rows, and basic state-distribution sanity metrics.
- Verified model transform parity implied by the simulation loop.

## Current Findings

All checks pass:

1. ✅ **Row count**: simulation expects `NUM_AGENTS = 1000`, CSV contains exactly **1000 valid rows**
2. ✅ **No malformed data**: all rows have exactly 9 columns
3. ✅ **Structural consistency**: header and data rows match `DIM = 9`
4. ✅ **Transform parity**: with `TICKS = 1000` (even) and fixed transform vector, net adinkra transform is identity
5. ✅ **Hamming weight distribution**: shows expected Gaussian-like pattern centered on middle planes

## Reproducible Command

```bash
python tools/audit_simulation_data.py
```

Current result: **PASS**

```
ASH data audit
- Source constants: NUM_AGENTS=1000, DIM=9, TICKS=1000
- CSV header columns: 9
- Valid rows: 1000
- Inferred row width: 9
- Unique binary states: 427
- Hamming weight distribution: {1: 24, 2: 63, 3: 145, 4: 238, 5: 255, 6: 170, 7: 78, 8: 25, 9: 2}
- Transform parity after TICKS: identity (because same codeword is used every tick)

RESULT: PASS
```

## Data Regeneration

The CSV file has been regenerated and all data integrity checks now pass. To regenerate in the future:

```bash
python src/simulate.py
```

This will create/update `data/simulation-results.csv` with fresh simulation data.

## Notes

- The absence of realm 0 in the distribution is expected: with 1000 (even) ticks using the same codeword, agents return to their original random states, which typically don't include Hamming weight 0.
- The audit tool correctly uses AST parsing to extract constants directly from source code for validation.
- Consider adding this audit to CI for continuous validation of data integrity.
