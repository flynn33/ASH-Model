# Validation — R-013

Run:

```bash
python -m compileall -q src tools
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_physical_perturbations.py
PYTHONPATH=src python tools/generate_physical_perturbations.py --out-root .
```

The validation is synthetic/internal and does not close R-014.
