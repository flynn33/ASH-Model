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
   python -m pip install numpy matplotlib sympy pytest
   python -m compileall .
   python -m pytest -q
   python tools/audit_claims.py
   python tools/run_simulation_controls.py --quick
   python tools/verify_branch.py --required-only
   python tools/audit_simulation_data.py
   python scripts/github/discussion_agent.py --validate-config --root .
   python scripts/github/discussion_topic_agent.py --validate-config --root .
   python scripts/github/discussion_moderation_agent.py --validate-config --root .
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

## Review and Merge Process

- CI checks on pull requests must pass.
- Maintainers may request revisions for scope, clarity, reproducibility, or scientific framing.
- Significant theoretical changes may require additional discussion before merge.

## Code of Conduct

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md). GitHub Discussions are subject to automated moderation for racist, vulgar, profane, threatening, or harassing content.

## Questions?

Open an issue for clarification or proposal discussion.
