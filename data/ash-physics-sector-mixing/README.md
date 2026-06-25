# ASH-Physics Sector-Mixing Data

This directory contains finite workbench data for sector-mixing resolution pass
002.

## Files

- `admissible_state_metadata_256.csv` records all eight-bit payload states, the
  recomputed ASH integrity coordinate, payload Hamming weight, and payload
  parity sector.
- `sector_mixing_spectral_scan.csv` records exact finite-matrix spectrum checks
  for selected `epsilon` values.
- `sector_mixing_time_series.csv` records convergence diagnostics from the
  all-zero payload state.
- `lumped_weight_transition_epsilon_*.csv` records payload Hamming-weight
  transition matrices for selected refresh parameters.
- `upstream-payload-manifest.json` records SHA-256 hashes and byte counts from
  the supplied research payload.

The reproduction command is:

```bash
python tools/reproduce_sector_mixing.py --output-dir .
```

The data describe a finite sector-refresh workbench, not an empirical
cosmology measurement.
