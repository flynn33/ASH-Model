# Simulation and Evidence Guide

## Generate repository evidence

```bash
python tools/generate_artifacts.py
```

This regenerates deterministic data artifacts, verifies the tracked figure artifacts by hash, and writes `proofs/artifact-manifest.json`.

To intentionally redraw tracked figure PNGs:

```bash
python tools/generate_artifacts.py --refresh-figures
```

## Run the simulation entry point

```bash
python src/simulate.py --agents 1000 --ticks 250 --noise 0.01 --seed 20260624
```

This writes terminal binary-state data for the configured run.

## Interpretation

A bell-shaped Hamming-weight histogram is the expected marginal of uniform 9-bit occupancy. It must not be interpreted as ASH-specific without comparison against the no-transform and matched-random controls in `data/ablation-results.csv`.

## Controlled ablations

The tracked ablation table compares uniform starts, zero starts, ASH transforms, no-transform controls, random weight-four transforms, and bit-flip noise. Use `docs/falsification-and-controls.md` when interpreting the table.
