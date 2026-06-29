# ASH R012-R016 Science Remediation Handoff

This ZIP is an independent science-remediation package for ASH R012-R016. It is not a repository patch, not a pull request, and not a version-control operation.

## What this package does

It performs actual first-pass scientific work in response to the accepted audit finding that R012-R016 were primarily scaffolding:

1. Derives the finite ASH pair-flip spectrum.
2. Constructs a finite-spectral FRW dark-sector extension.
3. Fits the model to compact DESI DR2 BAO data with covariance blocks.
4. Compares against flat LCDM and CPL baselines.
5. Calibrates a growth/S8 proxy against DES Y3.
6. Pilot-scores the three R015 locked predictions.
7. Emits a formal closure certificate and machine-readable outputs.

## Reproduction

From the top-level package directory:

```bash
python scripts/reproduce_ash_r012_r016_science.py
```

The script regenerates the data tables, outputs, and figures under `data/`, `outputs/`, and `figures/`.

## Main files

- `report/ASH_R012_R016_science_remediation_report.pdf` — human-readable report.
- `report/ASH_R012_R016_science_remediation_report.md` — Markdown source.
- `executive_summary.md` — short summary for handoff.
- `audit_science_finding_to_remediation_mapping.csv` — maps valid audit findings to performed work.
- `scripts/reproduce_ash_r012_r016_science.py` — complete reproducible analysis.
- `outputs/model_fit_summary.csv` — chi-square/AIC/BIC results.
- `outputs/locked_prediction_pilot_scores.json` — R015 pilot scoring.
- `outputs/r016_formal_closure_certificate.json` — R016 closure certificate.
- `formal/formal_expressions_latex.json` — machine-readable equations.
- `sources_and_values.json` — source provenance for compact data values.
- `quality_control/quality_control_manifest.json` — reproduction and PDF-render verification status.

## Scientific boundary

This package does not claim ASH is empirically validated cosmology. It is a concrete first-pass science execution. Remaining work includes full DESI likelihood products, supernova covariance, weak-lensing or galaxy P(k) covariance, and map-level low-ell CMB likelihoods.

## Citation of original ASH Model

Daley, J. (2026). *Adinkra-Stabilized Hypercube Model: Canonical Computational Specification and Reference Implementation*, version 1.1.0.
