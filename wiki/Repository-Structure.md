# Repository Structure

This page maps major folders/files to their purpose.

## Top-level

- `README.md` — overview, quick start, and contribution checks
- `CONTRIBUTING.md` — contribution workflow and expectations
- `LICENSE` — MIT license
- `axioms-of-existence.json` — formal modal-logic axiom set
- `simulation.py` — visualization-focused simulation

## Research docs

- `docs/ASH-research-paper.md` — markdown-formatted paper narrative
- `docs/ASH-Model-Preprint-v1.pdf` — compiled preprint PDF
- `docs/repository-review.md` — consistency review and follow-up notes
- `docs/consistency-validation-report.md` — validation audit results
- `docs/data-accuracy-audit.md` — simulation data verification
- `docs/mathematical-accuracy-review.md` — mathematical correctness audit
- `docs/python-code-validation.md` — Python code verification
- `latex/main.tex` — canonical manuscript source
- `latex/references.bib` — active bibliography (used by main.tex)
- `latex/bibtex.bib` — legacy bibliography file (not currently used)

## Code and data

- `src/simulate.py` — data-focused simulation script
- `src/derive-9-properties.py` — symbolic/mathematical derivations
- `data/simulation-results.csv` — sample/generated simulation output
- `figures/` — model and simulation images
- `tools/audit_simulation_data.py` — data integrity validation tool

## CI and automation

- `.github/workflows/ci.yml` — continuous integration checks (Python syntax, JSON validation, data audit)
- `.github/workflows/copilot-review.yml` — automated Copilot code review on PRs
- `.github/copilot-instructions.md` — custom instructions for Copilot reviews
- `.github/pull_request_template.md` — PR template for contributors
