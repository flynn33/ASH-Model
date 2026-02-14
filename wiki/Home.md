# ASH Model Wiki

Welcome to the Adinkra-Stabilized Hypercube (ASH) Model wiki.

This wiki is aligned with the current repository state and provides a practical guide for setup, simulation entry points, and project structure.

## Project Snapshot

- **Model**: 9-dimensional hypercube procedural cosmology (512 binary-encoded vertices)
- **Core themes**: adinkra-inspired transformations, error-correction concepts, Hamming-plane dynamics
- **Status**: active development, preprint in preparation

For full manuscript content, see the LaTeX source in `latex/main.tex`.

## Quick Start

### Prerequisites

Use Python 3.10+ and install required packages:

```bash
python -m pip install numpy matplotlib sympy
```

### Run simulations

- **Visualization-focused run** (renders/displays distribution figure):

```bash
python simulation.py
```

- **Data-focused run** (writes CSV output):

```bash
python src/simulate.py
```

## Key Paths

- `simulation.py` — plotting-oriented simulation workflow
- `src/simulate.py` — CSV/data-oriented simulation workflow
- `data/simulation-results.csv` — generated data output
- `figures/` — included/generated visual artifacts
- `axioms-of-existence.json` — modal-logic axioms used by the model framing
- `latex/main.tex` — publication manuscript source

## Validation Commands

Before opening a PR, run:

```bash
python -m pip install numpy  # Install required dependencies
python -m py_compile simulation.py src/simulate.py src/derive-9-properties.py tools/audit_simulation_data.py
python -m json.tool axioms-of-existence.json > /dev/null
python -m compileall -q simulation.py src tools
python tools/audit_simulation_data.py
```

## Related Pages

- [[Simulation Guide]]
- [[Repository Structure]]
- [[Consistency Checklist]]
