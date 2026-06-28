# R-016 validation

This validation folder records the deterministic closure certificate and verifier outputs for the branch-centered ASH model closure candidate.

## Scope

The verifier checks contract presence, upstream hash recording, falsification-gate presence, and explicit non-empirical boundary language.

## Commands

```bash
PYTHONPATH=src python tools/generate_branch_centered_closure.py --out-root . --require-pass
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_branch_centered_closure.py
```

## Scientific boundary

A passing R-016 validation means the branch-centered model is formally assembled at repository-contract level. It does not mean the model has passed external observational data, has empirical preference over matched baselines, or is a demonstrated physical cosmology.
