# GitHub Copilot Custom Instructions

These instructions guide Copilot Chat and Copilot code review suggestions for this repository.

## Repository Context

- This project combines theoretical research content with executable simulation scripts.
- Prioritize scientific reproducibility, clear assumptions, and minimal-risk edits.
- Prefer small, reviewable changes over broad refactors.

## Review Priorities

When reviewing pull requests, focus on the following in order:

1. **Correctness and reproducibility**
   - Verify commands and file paths are accurate and runnable from the repository root.
   - Flag changes that break documented outputs (`data/simulation-results.csv`, generated figures, LaTeX build artifacts).

2. **Documentation alignment**
   - Ensure README/CONTRIBUTING/wiki references stay consistent with script behavior and outputs.
   - Ask for doc updates when commands, dependencies, or file names change.

3. **Scientific and mathematical consistency**
   - Highlight unsupported claims, unexplained parameter changes, or altered definitions.
   - Request concise rationale when model assumptions are modified.

4. **Code quality and maintainability**
   - Prefer explicit variable names and short helper functions for non-trivial logic.
   - Recommend lightweight comments/docstrings for formulas or non-obvious simulation steps.

## Python Guidance

- Target Python 3.10+ compatibility.
- Follow PEP 8 style and keep scripts straightforward.
- Preserve deterministic behavior where practical (e.g., reproducible seeds when added).

## LaTeX and Docs Guidance

- Keep notation consistent with existing manuscript conventions.
- Do not introduce citation placeholders without matching bibliography entries.
- Preserve section structure and avoid sweeping style-only rewrites.

## Suggested PR Review Tone

- Be specific, actionable, and concise.
- Distinguish blocking issues from optional improvements.
- Provide patch-style suggestions when a fix is straightforward.
