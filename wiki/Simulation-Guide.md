# Simulation Guide

This project currently exposes two simulation entry points with different goals.

## 1) `simulation.py` (visualization path)

Use this when you want a plotted occupancy distribution and generated figure output.

```bash
python simulation.py
```

Expected behavior:

- Runs agent dynamics on a 9D binary state space
- Applies adinkra-inspired codeword transforms and low-probability noise
- Saves a chart to `figures/simulation-histogram-generated.png`
- Prints final occupancy per Hamming-weight plane

## 2) `src/simulate.py` (data path)

Use this when you want raw matrix output suitable for downstream analysis.

```bash
python src/simulate.py
```

Expected behavior:

- Runs lightweight iterative transformation loop
- Writes simulation state matrix to `data/simulation-results.csv`
- Prints summary distribution and output location

## Choosing the right script

- Pick **`simulation.py`** for visuals and quick exploratory runs.
- Pick **`src/simulate.py`** for reproducible CSV artifacts and data workflows.

## Troubleshooting

If imports fail, install dependencies first:

```bash
python -m pip install numpy matplotlib sympy
```
