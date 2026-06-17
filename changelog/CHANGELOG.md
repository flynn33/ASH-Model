# Changelog

All notable changes to the ASH Model project will be documented in this file.

---

## 2026-06-15 — Skir canonical code documentation merge

**Title**: Document merged Skir canonical code and wiki updates
**Change Class**: docs
**Version Impact**: none
**Summary**: Updates repository documentation, changelog, validation notes, and wiki source pages after the Skir branch merged into main with the canonical code layer and controls.
**Affected Area**: README, changelog, docs, wiki, validation guidance

- Documents the merged Skir code boundary as a rank-4 doubly-even linear `[9,4,4]` code over `F2^9`.
- Adds explicit navigation from the README into Skir validation, controls, and wiki pages.
- Expands docs and wiki source pages with visual logic maps, formulas, validation commands, and claim boundaries.
- Keeps version number `1.0.0` unchanged because this is a documentation and publication update.

## v1.0.0 — 2025-12-23

**Title**: Initial release of the Adinkra-Stabilized Hypercube Model
**Change Class**: release
**Version Impact**: major
**Summary**: First public release of the ASH Model framework including the 9-dimensional hypercube simulation, agent-based dynamics, L-system branching, modal-logic axioms, and the accompanying LaTeX research paper.
**Affected Area**: entire repository

- Core simulation (`simulation.py`, `src/simulate.py`)
- LaTeX research paper (`latex/main.tex`)
- Axioms of existence (`axioms-of-existence.json`)
- Derived 9-dimensional properties (`src/derive-9-properties.py`)
- Data audit tooling (`tools/audit_simulation_data.py`)
- Sample simulation results (`data/simulation-results.csv`)
- Figures and visualizations (`figures/`)
