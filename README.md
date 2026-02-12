# Adinkra-Stabilized Hypercube Model (ASH Model)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-in_preparation-red.svg)](https://arxiv.org)

**A Theoretical and Computational Framework for 9-Dimensional Procedural Cosmology**  
**Author**: James Daley (Independent Researcher, Full-Stack Developer, Author)  
**Mathematics and Calculations**: A.I. Assistance  
**Date**: December 23, 2025  

## Abstract

The Adinkra-Stabilized Hypercube Model (ASH Model) constructs a procedural cosmology on a 9-dimensional hypercube whose 512 vertices represent distinct cosmological realms encoded as binary strings. Supersymmetric adinkra graphs and doubly-even self-dual error-correcting codes are embedded at each vertex, enforcing symmetry transformations and robust error correction.

Agent-based simulations reveal emergent phenomena:

- Rapid convergence to Gaussian occupancy distributions across Hamming weight planes
- Resilience to random bit-flip noise up to the theoretical Hamming bound
- Fractal branching via Lindenmayer systems analogous to quantum decoherence

The recurrence of nine dimensions is supported by connections to string theory anomaly cancellation, optimal lattice packing (E₈, Leech), and coding theory. A modal-logic foundation is provided by five axioms of existence in Kripke-frame semantics (see `axioms-of-existence.json`).

## Repository Status

**Active Development** – Preprint manuscript in preparation for submission (target: Q1 2026).  
The LaTeX paper compiles to PDF and includes figures, proofs, and references.

## Quick Start

### Prerequisites

Use Python 3.10+ and install required packages before running scripts:

```bash
python -m pip install numpy matplotlib sympy
```

### 1. View the Paper

- Compile locally: `cd latex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- Or upload the repository to [Overleaf](https://www.overleaf.com) for instant PDF rendering.

### 2. Run the Simulation

- Visualization-focused simulation (generates histogram figure):

```bash
python simulation.py
```

- Data-focused simulation (writes CSV output):

```bash
python src/simulate.py
```

## Wiki

Wiki source pages are maintained in `wiki/` and should be mirrored to the GitHub Wiki (`ASH-Model.wiki`) when publishing updates.

## Repository Contents

- `latex/main.tex` – Master LaTeX source for the research paper
- `latex/references.bib` / `latex/bibtex.bib` – BibTeX references
- `figures/` – Diagrams and generated visualizations
- `simulation.py` – Reproducible Python implementation of core dynamics
- `axioms-of-existence.json` – Formal modal-logic axioms underpinning the model
- `data/simulation-results.csv` – Sample raw data

## Citation
Please cite this work as:
Daley, J. (2025). "Adinkra-Stabilized Hypercube Model (ASH Model): A Theoretical Framework for 9-Dimensional Procedural Cosmology." Preprint, in preparation.
## Contributing
Contributions are welcome. Before opening a pull request, review `CONTRIBUTING.md` and run the required checks:

```bash
python -m py_compile simulation.py src/simulate.py src/derive-9-properties.py
python -m json.tool axioms-of-existence.json > /dev/null
python -m compileall -q simulation.py src
```

## License
This project is licensed under the MIT License – see LICENSE for details. Academic citation is requested for any use or derivative work.
## Contact
For inquiries, extensions, or collaboration, open an Issue or discuss via GitHub.


