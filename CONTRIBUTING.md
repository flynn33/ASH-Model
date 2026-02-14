# Contributing to the Adinkra-Stabilized Hypercube Model (ASH Model)

Thank you for your interest in improving the ASH Model. This repository combines research artifacts and executable scripts, so contributions should be clear, reproducible, and reviewable.

## Contribution Requirements

1. **Open an Issue first (required)**
   - Propose the change before implementation so scope and direction can be aligned.
   - Reference the issue in your pull request (for example: `Closes #123`).

2. **Work from a focused branch**
   - Use a descriptive branch name, such as:
     - `feature/<short-description>`
     - `fix/<short-description>`
     - `docs/<short-description>`

3. **Keep changes scoped and documented**
   - Include only files required for the intended improvement.
   - Update docs when behavior, commands, or outputs change.

4. **Pass repository checks before opening a PR**
   - Run the same checks used in CI locally:

   ```bash
   python -m pip install numpy matplotlib sympy  # Install all required dependencies
   python -m py_compile simulation.py src/simulate.py src/derive-9-properties.py tools/audit_simulation_data.py
   python -m json.tool axioms-of-existence.json > /dev/null
   python -m compileall -q simulation.py src tools
   python tools/audit_simulation_data.py
   ```

5. **Use clear commit messages**
   - Write imperative, descriptive messages (example: `Add CI checks for Python and JSON validation`).

## What to Contribute

- **Theoretical extensions**: Proofs, code-theoretic links, tensor/holographic interpretations.
- **Simulation improvements**: Better performance, new dynamics, additional dimensions, improved output analysis.
- **Logic/formalism additions**: Better validation of axioms and modal-logic framing.
- **Documentation/reproducibility**: Better setup docs, examples, notebooks, and consistency updates.

## Pull Request Expectations

Each pull request should include:

- A concise summary of the change.
- A linked issue.
- A validation section listing commands run and their outcomes.
- Any known limitations or follow-up work.

A pull request template is provided at `.github/pull_request_template.md` and should be completed.

## Code Style Guidelines

- **Python**
  - Follow PEP 8 conventions.
  - Prefer small, composable functions over long script blocks when changing logic.
  - Add short docstrings for non-trivial functions.

- **LaTeX / docs**
  - Keep notation and formatting consistent with existing manuscript conventions.
  - Keep references and bibliography entries accurate and complete.


## Automated Copilot Review

This repository automatically requests a GitHub Copilot review on pull requests when they are opened, updated, or marked ready for review.

- Workflow: `.github/workflows/copilot-review.yml`
- Custom instructions: `.github/copilot-instructions.md`
- Learn how to get started with Copilot custom instructions: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- If Copilot review is not available for a repository plan or organization policy, the workflow exits without failing the pull request checks.

## Review and Merge Process

- CI checks on pull requests must pass.
- Maintainers may request revisions for scope, clarity, reproducibility, or scientific framing.
- Significant theoretical changes may require additional discussion before merge.

## Code of Conduct

Be respectful, constructive, and collaborative. The project welcomes interdisciplinary contributions across mathematics, physics, computer science, and philosophy.

## Questions?

Open an issue for clarification or proposal discussion.
