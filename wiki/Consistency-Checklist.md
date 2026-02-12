# Consistency Checklist

Use this checklist when updating docs/wiki content.

## Accuracy checks

- Commands in wiki pages match `README.md` and executable scripts.
- Output file names/paths match current code behavior:
  - `figures/simulation-histogram-generated.png`
  - `data/simulation-results.csv`
- Validation commands match `CONTRIBUTING.md`.

## Review commands

```bash
python -m py_compile simulation.py src/simulate.py src/derive-9-properties.py
python -m json.tool axioms-of-existence.json > /dev/null
python -m compileall -q simulation.py src
```

## Maintenance note

GitHub wiki is hosted as a separate repository (`<repo>.wiki.git`).
When external network access is available, sync these pages to the remote wiki to keep GitHub Wiki and repository docs aligned.
