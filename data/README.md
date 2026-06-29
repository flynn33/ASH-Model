# Data Directory

## Overview

This directory contains tracked ASH evidence data, research-package data, and generated validation outputs that support the repository documentation and proof boundaries. No raw survey-level observational dataset or official full likelihood product is bundled with the R012-R016 integration. The supplemental R012-R016 science-remediation handoff stores compact public numerical summaries, generated pilot outputs, figures, and provenance notes under `docs/ash-cosmology/r012-r016-science-remediation/`; this documentation records generated, synthetic, readiness, lock, formal-closure, and compact pilot assets already tracked by repository documentation.

## Directory Structure

```text
data/
├── manifests/
│   └── data_manifest.json
├── ash-cosmology/
├── ash-physics-sector-mixing/
├── ablation-results.csv
├── ash-state-reference.csv
├── branch-topology.json
├── codewords.csv
├── simulation-metadata.json
└── simulation-results.csv
```

Related synthetic validation outputs are tracked under:

```text
validation/background_bridge/pass_003/outputs/
validation/*/roadmap-0*/outputs/
```

## File Inventory

The authoritative data inventory is `data/manifests/data_manifest.json`. It records each tracked data asset's role, format, size, SHA-256 checksum, provenance statement, sensitivity classification, tracking policy, and validation status.

## Data Categories

| Category | Paths | Role |
|---|---|---|
| Core generated evidence | `data/ash-state-reference.csv`, `data/codewords.csv`, `data/branch-topology.json`, `data/ablation-results.csv`, `data/simulation-*` | Deterministic finite ASH data generated from tracked source code |
| Branch-centered roadmap assets | `data/ash-cosmology/branch-centered-roadmap/v0.2/` | Project-owner-provided roadmap package assets |
| Roadmap 007 finite perturbation outputs | `data/ash-cosmology/linear-perturbations/v0.1/`, `figures/ash-cosmology/linear-perturbations/v0.1/`, `validation/linear-perturbations/roadmap-007/outputs/` | Deterministic finite-observer perturbation transfer, Green-function, shell-power, figure, and verification outputs generated from tracked source code |
| Roadmap 008 finite branch-measure outputs | `data/ash-cosmology/branch-measure/v0.1/`, `validation/branch-measure/roadmap-008/outputs/` | Deterministic finite branch-measure frontier, entropy, transfer-penalty, candidate, and verification outputs generated from tracked source code |
| Roadmap 009 finite observer-commitment outputs | `data/ash-cosmology/observer-commitment/v0.1/`, `validation/observer-commitment/roadmap-009/outputs/` | Deterministic finite observer-commitment frontier, commitment distribution, branch-separation sample, depth summary, and verification outputs generated from tracked source code |
| Roadmap 010 unit-bearing bridge outputs | `data/ash-cosmology/unit-bridge/v0.1/`, `validation/unit-bridge/roadmap-010/outputs/` | Deterministic synthetic finite-observer unit-bearing bridge features, proxy observables, bootstrap samples, covariance, provenance, and verification outputs generated from tracked source code |
| Roadmap 011 finite-observer limit outputs | `data/ash-cosmology/finite-observer-limit/v0.1/`, `figures/ash-cosmology/finite-observer-limit/v0.1/`, `validation/finite-observer-limit/roadmap-011/outputs/` | Deterministic finite hierarchy, shell, cone, spectrum, projective-fiber, scale-annotation, figure, and verification outputs generated from tracked source code |
| Roadmap 012 background-equation outputs | `data/ash-cosmology/background-equations/v0.1/`, `figures/ash-cosmology/background-equations/v0.1/`, `validation/background-equations/roadmap-012/outputs/` | Deterministic synthetic finite-observer background curves, source features, covariance, grid-fit, figure, and verification outputs generated from tracked source code |
| Roadmap 013 physical-perturbation outputs | `data/ash-cosmology/physical-perturbations/v0.1/`, `figures/ash-cosmology/physical-perturbations/v0.1/`, `validation/physical-perturbations/roadmap-013/outputs/` | Deterministic bounded matter-sector perturbation workbench outputs, proxy spectra, figure, and validation summary generated from tracked source code |
| Roadmap 014 external-likelihood readiness outputs | `data/ash-cosmology/external-likelihoods/v0.1/`, `figures/ash-cosmology/external-likelihoods/v0.1/`, `validation/external-likelihoods/roadmap-014/outputs/` | Deterministic synthetic likelihood fixtures, covariance summaries, matched baseline comparisons, figure, preregistration lock, and verification outputs generated from tracked source code |
| Roadmap 015 locked prediction-template outputs | `data/ash-cosmology/locked-predictions/v0.1/`, `figures/ash-cosmology/locked-predictions/v0.1/`, `predictions/locked/`, `validation/locked-predictions/roadmap-015/outputs/` | Immutable prospective prediction templates, lock certificate, generated figures, and validation outputs; these are templates for future held-out comparison, not observed-data results |
| Roadmap 016 branch-centered closure outputs | `data/ash-cosmology/branch-centered-closure/v0.1/`, `figures/ash-cosmology/branch-centered-closure/v0.1/`, `validation/branch-centered-closure/roadmap-016/outputs/` | Deterministic closure-matrix, falsification-gate, model-card, closure-certificate, runtime verification, and figure outputs generated from tracked source code |
| R012-R016 science-remediation supplement | `docs/ash-cosmology/r012-r016-science-remediation/` | Supplemental first-pass finite-spectral FRW extension, compact DESI DR2 BAO + compressed Planck pilot fit, DES Y3 S8 proxy calibration, R015 pilot scoring, generated figures, report, reproduction script, and explicit non-validation boundary |
| Sector-mixing evidence | `data/ash-physics-sector-mixing/` | Project-owner-provided pass 002 finite workbench evidence |
| Background bridge diagnostics | `validation/background_bridge/pass_003/outputs/` | Pass 003 synthetic diagnostic outputs |
| Validation status | `validation/status.json` | Repository-maintained validation-status manifest |

## Provenance

Core ASH evidence files are produced by repository tools such as `tools/generate_artifacts.py`, `tools/run_proof_suite.py`, `tools/reproduce_sector_mixing.py`, `tools/run_background_bridge_validation.py`, `tools/generate_linear_perturbations.py`, `tools/generate_branch_measure.py`, `tools/generate_observer_commitment.py`, `tools/generate_unit_bridge.py`, `tools/generate_finite_observer_limit.py`, `tools/generate_cosmological_background.py`, `tools/generate_physical_perturbations.py`, `tools/generate_external_likelihoods.py`, `tools/generate_locked_predictions.py`, and `tools/generate_branch_centered_closure.py`. The R012-R016 science-remediation supplement is reproduced by `docs/ash-cosmology/r012-r016-science-remediation/scripts/reproduce_ash_r012_r016_science.py` within its package root. Roadmap, sector-mixing, and science-remediation package files are recorded as project-owner-provided package assets; missing license or provenance details are not inferred beyond what is already present in the repository.

## Validation

Validate the manifest and referenced files with:

```bash
python3 tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python3 tools/validate_json_assets.py .
python3 -m pytest tests/test_r012_r016_science_remediation.py
```

Run the broader repository evidence checks with:

```bash
python3 tools/generate_artifacts.py
python3 tools/run_proof_suite.py
python3 -m pytest
python3 tools/verify_repository.py
```

## Privacy and Sensitivity

The tracked assets in the manifest and the supplemental science-remediation package are classified as public repository evidence. They are finite-state tables, package metadata, compact public numerical summaries, CSV evidence, synthetic diagnostic outputs, generated pilot outputs, and validation manifests. No regulated personal data, credentials, or private user data should be added here.

## License and Usage Restrictions

Core generated evidence follows the repository `LICENSE`. Package-derived roadmap and sector-mixing assets preserve their repository provenance notes; where a source package does not state a separate license, the manifest records the license status conservatively.

## Large-File Policy

Large raw data should not be added directly unless approved for repository storage. Prefer external storage or Git LFS for large assets, and commit a manifest plus retrieval instructions instead of local caches.

## Update Procedure

1. Add or regenerate data using repository tools.
2. Update `data/manifests/data_manifest.json` with exact size and SHA-256 values.
3. Run `python3 tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`.
4. Run the relevant proof, artifact, and test commands.
5. Keep scientific claim wording aligned with the current validation scope.
