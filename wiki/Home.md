> **Canonical source**: `README.md`
> **Last synced**: 2026-06-13 16:40 UTC

# Adinkra-Stabilized Hypercube Model (ASH Model)

[![License: Custom](https://img.shields.io/badge/License-Custom-red.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv_in_preparation-red.svg)](https://arxiv.org)

**A Theoretical and Computational Framework for 9-Dimensional Procedural Cosmology**  
**Author**: James Daley (Independent Researcher, Full-Stack Developer, Author)  
**Date**: December 23, 2025

## Abstract

The Adinkra-Stabilized Hypercube Model (ASH Model) is an exploratory simulation-theory and procedural-cosmology framework built on a 9-bit raw state space `F2^9`. In the Skir formulation, the canonical stabilizer layer is a rank-4 doubly-even linear `[9,4,4]` code. Coordinate 9 is treated as a parity/integrity coordinate for the canonical code, not as an unrestricted independent payload coordinate.

Agent-based scripts in this repository visualize noisy hypercube mixing and codeword transforms. Error-correction claims are limited to the explicit nearest-codeword decoder in `src/ash_code.py` and its tests. Simulation outputs should be read as controls and demonstrations, not as standalone proof of runtime correction or empirical physical validation.

### Skir branch correction scope

Skir aligns ASH documentation and tests with the code layer implemented in this repository. It removes unsupported self-dual and Hamming-bound simulation claims, adds explicit decoder tests, and adds controls for noisy hypercube mixing.

## Quick Start

Use Python 3.10+ and install required packages:

```bash
python -m pip install numpy matplotlib sympy pytest
```

Run validations:

```bash
python -m compileall .
python -m pytest -q
python tools/audit_claims.py
python tools/run_simulation_controls.py --quick
python tools/audit_simulation_data.py
```

Run simulations:

```bash
python simulation.py
python src/simulate.py
python tools/run_simulation_controls.py --quick
```

## Repository Contents

- `src/ash_code.py` - Canonical Skir code layer and decoder
- `tests/test_ash_code.py` - Deterministic code and decoder tests
- `tools/audit_claims.py` - Claim-alignment audit
- `tools/run_simulation_controls.py` - Reproducible simulation controls
- `simulation.py` - Visualization-focused noisy-mixing demo
- `src/simulate.py` - Data-focused simulation demo
- `latex/main.tex` - Master LaTeX source for the research paper
- `axioms-of-existence.json` - Formal modal-logic axiom set
