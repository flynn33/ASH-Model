# R-015 validation

This directory records repository validation for the R-015 locked prediction ledger and its immutable CSV artifacts.

Run:

```bash
PYTHONPATH=src python tools/generate_locked_predictions.py --out-root . --require-pass
PYTHONPATH=src python -m pytest -q tests/test_locked_predictions.py
```

`outputs/verification.json` should report:

- `passed: true`
- `ledger_hash_matches: true`
- `all_locked_files_match: true`
- exactly three locked prediction IDs.

The validation does not compare predictions to external data. It verifies only lock integrity, schema completeness, hash consistency, and boundary documentation.
