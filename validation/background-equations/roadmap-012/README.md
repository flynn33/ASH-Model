# R-012 Validation Protocol

Run:

```bash
python tools/generate_cosmological_background.py --out-root . --refresh-figures
python -m pytest tests/test_cosmological_background.py
```

Pass criteria:

- exact \(\Omega_{\mathrm{ASH}}=0\) standard-baseline relation;
- \(\Xi_{\mathrm{ASH}}(1)=1\);
- positive \(E^2\) on sampled synthetic domain;
- deterministic one-parameter \(\Omega_{\mathrm{ASH}}\) recovery on synthetic H observations;
- covariance output exists;
- `validation/background-equations/roadmap-012/outputs/verification.json` records `"passed": true`.

This protocol uses synthetic data only.
