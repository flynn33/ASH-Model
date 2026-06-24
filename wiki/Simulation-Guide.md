# Simulation and Evidence Guide

## Generate all evidence

```bash
python simulation.py
```

This regenerates code/state tables, branch topology, seeded simulation data, controlled ablations, evidence figures, and artifact hashes.

## Generate only terminal state data

```bash
python src/simulate.py --agents 1000 --ticks 250 --noise 0.01 --seed 20260624
```

## Interpretation

A bell-shaped Hamming-weight histogram is the expected marginal of uniform 9-bit occupancy. It must not be interpreted as ASH-specific without comparison against the no-transform and matched-random controls in `data/ablation-results.csv`.
