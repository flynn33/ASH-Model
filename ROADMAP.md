# ASH Model Roadmap Tracker

This tracker is the repository-maintained status log for identified ASH Model
roadmap items. It should be updated whenever a roadmap item changes state,
receives new evidence, or is completed.

## Update rule

When a roadmap item is completed or changes status:

1. Update the item status and last-updated date.
2. Add or refresh the evidence paths that prove the state of the item.
3. Record the verification commands used for the change.
4. Add a dated completion entry when the item reaches `complete`.
5. Keep scientific blockers open unless the repository contains the derivation,
   implementation, validation command, and boundary statement that close them.

Use these statuses consistently:

| Status | Meaning |
|---|---|
| `open` | Identified work has not been completed. |
| `active` | Work is in progress and has committed repository evidence. |
| `blocked` | Work is waiting on missing evidence, derivation, data, or review. |
| `complete` | Repository evidence and verification commands close the item. |
| `deferred` | Work is intentionally out of the current roadmap scope. |

## Current snapshot

Snapshot date: 2026-06-26

Primary roadmap sources:

- [`docs/ash-cosmology/branch-centered-roadmap/v0.2/`](docs/ash-cosmology/branch-centered-roadmap/v0.2/)
- [`docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md`](docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md)
- [`docs/ash-physics-validation/tasks/task_manifest.json`](docs/ash-physics-validation/tasks/task_manifest.json)
- [`docs/ash-physics-validation/tasks/science_manifest.json`](docs/ash-physics-validation/tasks/science_manifest.json)
- [`docs/ash-cosmology/background-bridge/pass-003/ROADMAP_STATUS.md`](docs/ash-cosmology/background-bridge/pass-003/ROADMAP_STATUS.md)
- [`wiki/Science-Roadmap.md`](wiki/Science-Roadmap.md)
- [`validation/status.json`](validation/status.json)

## Tracker

| ID | Roadmap item | Status | Last updated | Evidence |
|---|---|---:|---:|---|
| R-001 | Finite ASH algebra and canonical mapping | `complete` | 2026-06-24 | [`src/ash_model/`](src/ash_model/), [`tests/`](tests/), [`proofs/computational-certificate.md`](proofs/computational-certificate.md) |
| R-002 | ASH-Physics finite-observer state layer | `complete` | 2026-06-24 | [`src/ash_model/physics.py`](src/ash_model/physics.py), [`tests/test_physics.py`](tests/test_physics.py), [`docs/ash-physics-validation/README.md`](docs/ash-physics-validation/README.md) |
| R-003 | Prediction-ledger mechanics and lock-status validation | `complete` | 2026-06-24 | [`predictions/prediction-ledger.json`](predictions/prediction-ledger.json), [`src/ash_model/prediction_ledger.py`](src/ash_model/prediction_ledger.py), [`tests/test_prediction_ledger.py`](tests/test_prediction_ledger.py) |
| R-004 | Sector-mixing resolution pass 002 finite workbench | `complete` | 2026-06-25 | [`docs/ash-physics-validation/sector-mixing-resolution-pass-002.md`](docs/ash-physics-validation/sector-mixing-resolution-pass-002.md), [`data/ash-physics-sector-mixing/`](data/ash-physics-sector-mixing/), [`tests/test_sector_mixing.py`](tests/test_sector_mixing.py) |
| R-005 | Background bridge pass 003 synthetic diagnostics | `complete` | 2026-06-25 | [`docs/ash-cosmology/background-bridge/pass-003/`](docs/ash-cosmology/background-bridge/pass-003/), [`src/ash_model/background_bridge.py`](src/ash_model/background_bridge.py), [`validation/background_bridge/pass_003/`](validation/background_bridge/pass_003/) |
| R-006 | Consolidated data governance manifest | `complete` | 2026-06-26 | [`data/README.md`](data/README.md), [`data/manifests/data_manifest.json`](data/manifests/data_manifest.json), [`tools/validate_data_manifest.py`](tools/validate_data_manifest.py), [`tests/test_data_manifest.py`](tests/test_data_manifest.py) |
| R-007 | Branch-centered cosmology model closure | `open` | 2026-06-26 | [`docs/ash-cosmology/branch-centered-roadmap/v0.2/`](docs/ash-cosmology/branch-centered-roadmap/v0.2/) |
| R-008 | Branch measure or amplitude law | `blocked` | 2026-06-26 | [`docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md`](docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md) |
| R-009 | Commitment, observer memory, and decoherence rule | `blocked` | 2026-06-26 | [`docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md`](docs/ash-cosmology/branch-centered-roadmap/v0.2/human-readable/10_FULL_BRANCH_CENTERED_ROADMAP.md) |
| R-010 | Unit-bearing physical bridge to observables | `blocked` | 2026-06-26 | [`theory/coarse-graining-and-bridge-map.md`](theory/coarse-graining-and-bridge-map.md), [`phenomenology/observables_spec.md`](phenomenology/observables_spec.md), [`validation/status.json`](validation/status.json) |
| R-011 | Continuum, geometry, causal-structure, or finite-observer limit closure | `blocked` | 2026-06-26 | [`theory/continuum-limit.md`](theory/continuum-limit.md), [`theory/causal-structure.md`](theory/causal-structure.md), [`proofs/physics-proof-obligations.md`](proofs/physics-proof-obligations.md) |
| R-012 | Cosmological background equations and standard-baseline relation | `blocked` | 2026-06-26 | [`theory/cosmological-background.md`](theory/cosmological-background.md), [`phenomenology/ash_background_spec.md`](phenomenology/ash_background_spec.md), [`validation/lcdm-limit/README.md`](validation/lcdm-limit/README.md) |
| R-013 | Physical perturbation equations and CMB or matter-sector solver | `blocked` | 2026-06-26 | [`theory/linear-perturbations.md`](theory/linear-perturbations.md), [`phenomenology/ash_perturbations_spec.md`](phenomenology/ash_perturbations_spec.md) |
| R-014 | External likelihoods, matched empirical baselines, and reviewed data products | `blocked` | 2026-06-26 | [`validation/preregistration.md`](validation/preregistration.md), [`validation/matched-ablations/README.md`](validation/matched-ablations/README.md), [`validation/status.json`](validation/status.json) |
| R-015 | Locked prospective or held-out scientific predictions | `blocked` | 2026-06-26 | [`predictions/prediction-ledger.json`](predictions/prediction-ledger.json), [`predictions/falsification-criteria.md`](predictions/falsification-criteria.md) |
| R-016 | Roadmap 007 finite linear perturbation sector | `complete` | 2026-06-26 | [`src/ash_model/linear_perturbations.py`](src/ash_model/linear_perturbations.py), [`tests/test_linear_perturbations.py`](tests/test_linear_perturbations.py), [`tools/generate_linear_perturbations.py`](tools/generate_linear_perturbations.py), [`validation/linear-perturbations/roadmap-007/outputs/verification.json`](validation/linear-perturbations/roadmap-007/outputs/verification.json) |

## Completion log

### 2026-06-26

- R-016 marked complete for the finite-observer Roadmap 007 linear
  perturbation sector. Evidence: quotient Walsh-shell implementation,
  targeted tests, deterministic transfer artifacts, generated figures,
  validation JSON, and finite-boundary documentation. This does not close the
  physical perturbation, CMB, matter-spectrum, physical-wavenumber, or
  empirical-validation gates tracked by R-013 and R-014.
- R-006 marked complete for repository data governance. Evidence: consolidated
  data manifest, data README, manifest validator, regression test, and
  repository audit notes.
- Roadmap tracker added as the canonical repository status log for identified
  roadmap items and future completion updates.

### 2026-06-25

- R-004 marked complete for sector-mixing pass 002 finite workbench scope.
- R-005 marked complete for pass 003 synthetic background-bridge diagnostics.
  This completion is limited to synthetic diagnostics and does not close
  external cosmology validation.

### 2026-06-24

- R-001 marked complete for finite algebra and canonical mapping.
- R-002 marked complete for the finite-observer ASH-Physics layer.
- R-003 marked complete for prediction-ledger mechanics and lock-status
  validation. No locked scientific prediction is recorded by this entry.

## Completion entry template

Use this format when closing or changing an item:

```markdown
### YYYY-MM-DD

- R-000 changed from `open` to `complete`.
  - Evidence: `path/to/evidence.md`, `path/to/test.py`
  - Verification: `python tools/run_proof_suite.py`, `python -m pytest`
  - Boundary: state what the completion does and does not prove.
```

## Maintenance checklist

Before marking an item complete, run the strongest applicable checks for the
changed area. Typical repository-wide checks are:

```bash
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/final_repository_audit.py .
```

The proof certificate source manifest includes Markdown, JSON, YAML, Python,
TOML, TeX, CFF, license, version, and gitignore files. After changing this
tracker or other covered source files, refresh the proof certificate with
`python tools/run_proof_suite.py` before closing the change.
