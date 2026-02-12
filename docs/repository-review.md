# Repository Review and Fix Plan

Date: 2026-02-12

## Scope

Reviewed project structure, key scripts, and documentation for correctness, reproducibility, and maintainability.

## Checks Performed

- `python -m compileall .`
- `python simulation.py`
- Manual source review of:
  - `README.md`
  - `simulation.py`
  - `src/simulate.py`
  - `src/derive-9-properties.py`

## Findings

### 1) `README.md` has malformed Markdown structure (high)

- The "Run the Simulation" code block is never closed.
- Large sections beginning with "Repository Contents" are rendered as part of a code block.
- This reduces readability and makes onboarding error-prone.

**Impact:** Users may miss important setup and usage guidance.

**Fix plan:**
- Close the fenced code block after `python simulation.py`.
- Reformat section headings and lists using standard Markdown heading levels.
- Optionally add a "Requirements" section with explicit package dependencies.

### 2) Root simulation script lacks dependency declaration and graceful messaging (medium)

- `simulation.py` requires `numpy` and `matplotlib`, but there is no `requirements.txt`/`pyproject.toml`.
- Running `python simulation.py` currently fails in a clean environment due to missing packages.

**Impact:** Reproducibility is poor and first run fails for new users.

**Fix plan:**
- Add `requirements.txt` with pinned or minimally constrained versions for:
  - `numpy`
  - `matplotlib`
  - `sympy` (used in `src/derive-9-properties.py`)
- Update README with install step (`python -m pip install -r requirements.txt`).
- Optional: add a lightweight preflight dependency check in scripts with actionable error messages.

### 3) `src/simulate.py` writes output to a fragile relative path (high)

- Script saves to `../data/simulation_results.csv`, which depends on current working directory.
- If run from repo root, this path points outside the repository.
- Output filename also differs from repository convention (`simulation-results.csv` vs `simulation_results.csv`).

**Impact:** Data can be written to unexpected locations or fail silently in CI/sandbox workflows.

**Fix plan:**
- Resolve paths relative to the script location using `pathlib.Path(__file__).resolve()`.
- Standardize output name and destination to repository convention (e.g., `data/simulation-results.csv`).
- Ensure destination directory exists before writing.

### 4) Code duplication between simulation entry points (medium)

- There are two simulation scripts (`simulation.py` and `src/simulate.py`) with overlapping behavior but different parameters and output conventions.

**Impact:** Inconsistent behavior and increased maintenance cost.

**Fix plan:**
- Consolidate shared simulation logic into a reusable module (e.g., `src/ash_model/simulation_core.py`).
- Keep one user-facing CLI entry point and one optional research/experimental script.
- Document the canonical execution path in README.

### 5) Missing automated validation workflow (medium)

- Repository has no test suite and no basic CI checks.

**Impact:** Regressions can slip in (formatting breakage, path issues, dependency drift).

**Fix plan:**
- Add minimal tests:
  - smoke test for script import/execution path setup
  - path resolution test for output files
- Add CI workflow to run:
  - `python -m compileall .`
  - unit/smoke tests

## Prioritized Remediation Roadmap

1. **Documentation + dependency baseline**
   - Fix README markdown and usage instructions.
   - Add dependency manifest (`requirements.txt`).
2. **Path correctness and output consistency**
   - Fix `src/simulate.py` output pathing and filename conventions.
3. **Stability guardrails**
   - Add minimal tests + CI checks.
4. **Codebase consolidation**
   - Refactor duplicate simulation logic into shared module.

## Suggested Next PR Breakdown

- **PR 1:** README + requirements (low risk, immediate usability gains)
- **PR 2:** `src/simulate.py` path/output fixes (functional correctness)
- **PR 3:** tests + CI (quality gate)
- **PR 4:** simulation core refactor (larger structural change)

