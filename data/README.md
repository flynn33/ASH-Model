# Data Directory

## Overview

This directory contains tracked ASH evidence data, research-package data, and generated validation outputs that support the repository documentation and proof boundaries. No new raw dataset was supplied for the 2026-06-26 repository update; this pass documents and validates the data assets already committed to the repository.

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
| Sector-mixing evidence | `data/ash-physics-sector-mixing/` | Project-owner-provided pass 002 finite workbench evidence |
| Background bridge diagnostics | `validation/background_bridge/pass_003/outputs/` | Pass 003 synthetic diagnostic outputs |
| Validation status | `validation/status.json` | Repository-maintained validation-status manifest |

## Provenance

Core ASH evidence files are produced by repository tools such as `tools/generate_artifacts.py`, `tools/run_proof_suite.py`, `tools/reproduce_sector_mixing.py`, `tools/run_background_bridge_validation.py`, `tools/generate_linear_perturbations.py`, `tools/generate_branch_measure.py`, and `tools/generate_observer_commitment.py`. Roadmap and sector-mixing package files are recorded as project-owner-provided package assets; missing license or provenance details are not inferred beyond what is already present in the repository.

## Validation

Validate the manifest and referenced files with:

```bash
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/validate_json_assets.py .
```

Run the broader repository evidence checks with:

```bash
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

## Privacy and Sensitivity

The tracked assets in the manifest are classified as public repository evidence. They are finite-state tables, package metadata, CSV evidence, synthetic diagnostic outputs, and validation manifests. No regulated personal data, credentials, or private user data should be added here.

## License and Usage Restrictions

Core generated evidence follows the repository `LICENSE`. Package-derived roadmap and sector-mixing assets preserve their repository provenance notes; where a source package does not state a separate license, the manifest records the license status conservatively.

## Large-File Policy

Large raw data should not be added directly unless approved for repository storage. Prefer external storage or Git LFS for large assets, and commit a manifest plus retrieval instructions instead of local caches.

## Update Procedure

1. Add or regenerate data using repository tools.
2. Update `data/manifests/data_manifest.json` with exact size and SHA-256 values.
3. Run `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`.
4. Run the relevant proof, artifact, and test commands.
5. Keep scientific claim wording aligned with the current validation scope.
