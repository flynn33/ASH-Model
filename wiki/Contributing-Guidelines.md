# Contributing Guidelines

Use the repository's `CONTRIBUTING.md` and pull request template as the source of truth.

## Required process

1. Keep changes scoped.
2. Update documentation when behavior, commands, paths, artifacts, or claims change.
3. Regenerate affected evidence.
4. Run validation commands.
5. Keep empirical and physical claims within the evidence actually present.

## Validation commands

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

## Pull request metadata

The pull request template requires:

- change class;
- release impact;
- breaking-change status;
- commands and results;
- limitations.

Documentation-only changes should still identify whether they alter public interpretation or only align existing surfaces.
