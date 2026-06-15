# Simulation Guide

This project currently exposes three simulation/control entry points with different goals.

## 1. `simulation.py` (visualization path)

Use this when you want a plotted occupancy distribution and generated figure output.

```bash
python simulation.py
```

Expected behavior:

- Runs agent dynamics on a 9D binary state space
- Applies canonical ASH codeword transforms and low-probability noise
- Saves a chart to `figures/simulation-histogram-generated.png`
- Prints final occupancy per Hamming-weight plane

## 2. `src/simulate.py` (data path)

Use this when you want raw matrix output suitable for downstream analysis.

```bash
python src/simulate.py
```

Expected behavior:

- Runs a lightweight iterative transformation loop
- Writes simulation state matrix to `data/simulation-results.csv`
- Prints summary distribution and output location

## 3. `tools/run_simulation_controls.py` (Skir controls)

Use this when you need conservative control comparisons for Skir documentation.

```bash
python tools/run_simulation_controls.py --quick
```

Expected behavior:

- Compares canonical codeword transforms against no-codeword and random-codeword baselines
- Writes `data/simulation-controls.json`
- Prints total-variation distance to the binomial/Haar occupancy envelope for each run

## Choosing the right script

- Pick `simulation.py` for visuals and exploratory runs.
- Pick `src/simulate.py` for CSV artifacts and data workflows.
- Pick `tools/run_simulation_controls.py` for claim-alignment controls.

## Troubleshooting

If imports fail, install dependencies first:

```bash
python -m pip install numpy matplotlib sympy pytest
```
