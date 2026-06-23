# Repository Review and Consistency Check

Date: 2026-02-12

## Scope

Reviewed repository documentation and executable scripts for internal consistency, reproducibility guidance, and factual accuracy.

## Checks Performed

- `python -m py_compile simulation.py src/simulate.py src/derive-9-properties.py`
- `python -m json.tool axioms-of-existence.json > /dev/null`
- `python -m compileall -q simulation.py src`
- Manual review of:
  - `README.md`
  - `CONTRIBUTING.md`
  - `simulation.py`
  - `src/simulate.py`
  - `docs/ASH-research-paper.md`

## Consistency Findings

### 1) Prior README formatting issue is resolved (verified)

The root `README.md` currently has valid Markdown sectioning and properly closed code fences.

- "Run the Simulation" block is correctly closed.
- "Repository Contents", "Citation", and "Contributing" sections render as intended.

**Status:** No action required.

### 2) `src/simulate.py` path handling is now robust (verified)

`src/simulate.py` now resolves output paths using `pathlib.Path(__file__).resolve()` and writes to `data/simulation-results.csv` inside the repository root.

**Status:** No action required.

### 3) Dependency installation instructions are still incomplete (open)

The repository still lacks a dependency manifest (`requirements.txt` or `pyproject.toml`) even though scripts import external packages:

- `simulation.py`: `numpy`, `matplotlib`
- `src/simulate.py`: `numpy`
- `src/derive-9-properties.py`: `sympy`

**Impact:** New users cannot reliably reproduce the environment from docs alone.

**Recommended correction:**
- Add a dependency manifest and reference it in `README.md` quick start.

### 4) Simulation entry points remain intentionally separate but should be clarified (open)

There are two simulation scripts with different goals and outputs:

- `simulation.py`: plotting-oriented run that saves `figures/simulation-histogram-generated.png`
- `src/simulate.py`: lightweight numeric run that saves `data/simulation-results.csv`

This is valid, but this distinction is not explicit in the README.

**Impact:** Users may run the wrong script for their task (visualization vs data generation).

**Recommended correction:**
- Add one sentence in `README.md` distinguishing the two scripts and their outputs.

### 5) Research-paper markdown aligns with available artifacts (verified)

`docs/ASH-research-paper.md` references figures that exist in `figures/` and correctly points to `axioms-of-existence.json` for formal axioms.

**Status:** No action required.

## Summary

The repository is largely consistent and executable for existing maintainers. The major remaining accuracy/reproducibility gap is dependency declaration and clearer script-role documentation in the README.

## Next Wiki Update Suggestions

1. Add an "Environment Setup" section to README with pinned dependencies.
2. Add a "Which simulation script should I run?" subsection.
3. Keep this review updated whenever scripts, file names, or outputs change.
