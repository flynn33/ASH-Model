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

Current repository posture:

- Repository finite-observer implementation work through Roadmap 011 is
  complete and verified.
- Roadmap 010, Roadmap 011, and Roadmap 012 are part of the repository's
  current proof, data-manifest, and validation surfaces.
- Scientific readiness is not complete: reviewed physical calibration,
  differentiable continuum or physical metric interpretation, physical
  perturbation solver, external likelihoods, and locked predictions remain
  blocked until their required evidence exists in the repository. Roadmap 010
  supplies a synthetic unit-bearing bridge workbench, and Roadmap 011 closes
  only the finite-observer limit route, not reviewed physical calibration or
  empirical validation.
- Roadmap 007 adds a finite perturbation sector only. Roadmap 008 adds a finite
  branch-measure law only. Roadmap 009 adds a finite observer-relative
  commitment and branch-separation workbench only. Roadmap 010 adds a synthetic
  unit-bearing bridge workbench only. Roadmap 011 adds a finite observer
  hierarchy and finite causal substrate only. These supply quotient-shell
  transfer mathematics, finite branch-normalization mathematics,
  committed-memory push-forward mathematics, synthetic unit-bearing bridge
  artifacts, finite projective hierarchy checks, and deterministic validation
  outputs, but they do not close physical calibration, differentiable
  continuum geometry, physical perturbation, CMB, matter-spectrum,
  physical-wavenumber, locked-prediction, empirical-validation, or full
  model-closure gates. Roadmap 012 adds a synthetic finite-observer
  cosmological background-equation workbench and exact standard-baseline
  relation only; it does not close physical perturbation equations, CMB,
  matter-spectrum, external-likelihood, empirical-validation, or
  locked-prediction gates.

Post-R011 publication state:

| Surface | Current state |
|---|---|
| Repository roadmap | R-001 through R-012 are complete within their stated finite scopes. |
| README and data documentation | Current through the synthetic unit bridge and finite-observer hierarchy. |
| Proof certificate | Covers finite ASH, finite-observer physics, R-010 bridge checks, and R-011 finite-observer checks. |
| Data manifest | Tracks R-007 through R-011 generated CSV/JSON/PNG evidence. |
| Wiki | Mirrors the current finite-observer state and keeps empirical cosmology boundaries open. |

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
| R-007 | Roadmap 007 finite linear perturbation sector | `complete` | 2026-06-26 | [`src/ash_model/linear_perturbations.py`](src/ash_model/linear_perturbations.py), [`tests/test_linear_perturbations.py`](tests/test_linear_perturbations.py), [`tools/generate_linear_perturbations.py`](tools/generate_linear_perturbations.py), [`data/ash-cosmology/linear-perturbations/v0.1/`](data/ash-cosmology/linear-perturbations/v0.1/), [`figures/ash-cosmology/linear-perturbations/v0.1/`](figures/ash-cosmology/linear-perturbations/v0.1/), [`validation/linear-perturbations/roadmap-007/outputs/verification.json`](validation/linear-perturbations/roadmap-007/outputs/verification.json) |
| R-008 | Branch measure or amplitude law | `complete` | 2026-06-26 | [`src/ash_model/branch_measure.py`](src/ash_model/branch_measure.py), [`tests/test_branch_measure.py`](tests/test_branch_measure.py), [`tools/generate_branch_measure.py`](tools/generate_branch_measure.py), [`docs/ash-cosmology/branch-measure/roadmap-008/README.md`](docs/ash-cosmology/branch-measure/roadmap-008/README.md), [`data/ash-cosmology/branch-measure/v0.1/`](data/ash-cosmology/branch-measure/v0.1/), [`validation/branch-measure/roadmap-008/outputs/verification.json`](validation/branch-measure/roadmap-008/outputs/verification.json) |
| R-009 | Commitment, observer memory, and decoherence rule | `complete` | 2026-06-26 | [`src/ash_model/observer_commitment.py`](src/ash_model/observer_commitment.py), [`tests/test_observer_commitment.py`](tests/test_observer_commitment.py), [`tools/generate_observer_commitment.py`](tools/generate_observer_commitment.py), [`docs/ash-cosmology/observer-commitment/roadmap-009/README.md`](docs/ash-cosmology/observer-commitment/roadmap-009/README.md), [`data/ash-cosmology/observer-commitment/v0.1/`](data/ash-cosmology/observer-commitment/v0.1/), [`validation/observer-commitment/roadmap-009/outputs/verification.json`](validation/observer-commitment/roadmap-009/outputs/verification.json) |
| R-010 | Unit-bearing physical bridge to observables | `complete` | 2026-06-26 | [`src/ash_model/unit_bridge.py`](src/ash_model/unit_bridge.py), [`tests/test_unit_bridge.py`](tests/test_unit_bridge.py), [`tools/generate_unit_bridge.py`](tools/generate_unit_bridge.py), [`config/ash_r010_unit_bridge_calibration.json`](config/ash_r010_unit_bridge_calibration.json), [`docs/ash-cosmology/unit-bridge/roadmap-010/README.md`](docs/ash-cosmology/unit-bridge/roadmap-010/README.md), [`data/ash-cosmology/unit-bridge/v0.1/`](data/ash-cosmology/unit-bridge/v0.1/), [`validation/unit-bridge/roadmap-010/outputs/verification.json`](validation/unit-bridge/roadmap-010/outputs/verification.json) |
| R-011 | Continuum, geometry, causal-structure, or finite-observer limit closure | `complete` | 2026-06-26 | [`src/ash_model/finite_observer_limit.py`](src/ash_model/finite_observer_limit.py), [`tests/test_finite_observer_limit.py`](tests/test_finite_observer_limit.py), [`tools/generate_finite_observer_limit.py`](tools/generate_finite_observer_limit.py), [`config/ash_r011_finite_observer_limit_contract.json`](config/ash_r011_finite_observer_limit_contract.json), [`docs/ash-cosmology/finite-observer-limit/roadmap-011/README.md`](docs/ash-cosmology/finite-observer-limit/roadmap-011/README.md), [`data/ash-cosmology/finite-observer-limit/v0.1/`](data/ash-cosmology/finite-observer-limit/v0.1/), [`figures/ash-cosmology/finite-observer-limit/v0.1/`](figures/ash-cosmology/finite-observer-limit/v0.1/), [`validation/finite-observer-limit/roadmap-011/outputs/verification.json`](validation/finite-observer-limit/roadmap-011/outputs/verification.json), [`theory/continuum-limit_R011_addendum.md`](theory/continuum-limit_R011_addendum.md), [`theory/causal-structure_R011_addendum.md`](theory/causal-structure_R011_addendum.md), [`proofs/physics-proof-obligations_R011_addendum.md`](proofs/physics-proof-obligations_R011_addendum.md) |
| R-012 | Cosmological background equations and standard-baseline relation | `complete` | 2026-06-28 | [`src/ash_model/cosmological_background.py`](src/ash_model/cosmological_background.py), [`tests/test_cosmological_background.py`](tests/test_cosmological_background.py), [`tools/generate_cosmological_background.py`](tools/generate_cosmological_background.py), [`config/ash_r012_background_contract.json`](config/ash_r012_background_contract.json), [`docs/ash-cosmology/background-equations/roadmap-012/README.md`](docs/ash-cosmology/background-equations/roadmap-012/README.md), [`data/ash-cosmology/background-equations/v0.1/`](data/ash-cosmology/background-equations/v0.1/), [`figures/ash-cosmology/background-equations/v0.1/`](figures/ash-cosmology/background-equations/v0.1/), [`validation/background-equations/roadmap-012/outputs/verification.json`](validation/background-equations/roadmap-012/outputs/verification.json) |
| R-013 | Physical perturbation equations and CMB or matter-sector solver | `blocked` | 2026-06-26 | [`theory/linear-perturbations.md`](theory/linear-perturbations.md), [`phenomenology/ash_perturbations_spec.md`](phenomenology/ash_perturbations_spec.md), [`docs/ash-cosmology/linear-perturbations/roadmap-007/README.md`](docs/ash-cosmology/linear-perturbations/roadmap-007/README.md) |
| R-014 | External likelihoods, matched empirical baselines, and reviewed data products | `blocked` | 2026-06-26 | [`validation/preregistration.md`](validation/preregistration.md), [`validation/matched-ablations/README.md`](validation/matched-ablations/README.md), [`validation/status.json`](validation/status.json) |
| R-015 | Locked prospective or held-out scientific predictions | `blocked` | 2026-06-26 | [`predictions/prediction-ledger.json`](predictions/prediction-ledger.json), [`predictions/falsification-criteria.md`](predictions/falsification-criteria.md) |
| R-016 | Branch-centered cosmology model closure | `open` | 2026-06-26 | [`docs/ash-cosmology/branch-centered-roadmap/v0.2/`](docs/ash-cosmology/branch-centered-roadmap/v0.2/) |

## Active priority queue

| Priority | Roadmap item | Required closure evidence |
|---:|---|---|
| 1 | R-013 Physical perturbation equations and solver | Derivation that maps finite shell variables to physical perturbation variables, executable solver, gauge or boundary policy where applicable, synthetic recovery tests, and boundary documentation. |
| 2 | R-014 External likelihoods and matched baselines | Reviewed data products, covariance inputs, matched baseline definitions, preregistered likelihoods, and reproducible validation commands. |
| 3 | R-015 Locked prospective or held-out predictions | Frozen prediction entries with hashes, falsification criteria, input freeze date, and repository validation. |
| 4 | R-016 Branch-centered cosmology model closure | Closed branch-centered model definition, integration of the completed finite measure and observer workbenches, bridge-map relation, and validation boundary evidence. |

Priority interpretation:

- R-013 is a mathematical and computational derivation task, not a
  documentation task.
- R-014 cannot close until external data products, covariance handling,
  preregistration, and matched controls exist in the repository.
- R-015 cannot close without frozen prediction-ledger entries.
- R-016 remains open until the completed finite workbenches are integrated into
  a closed branch-centered cosmology model with explicit validation boundaries.

## Completion log

### 2026-06-28

- R-012 marked complete for a synthetic finite-observer cosmological
  background-equation workbench and exact standard-baseline relation. Evidence:
  explicit background parameters and source normalization,
  \(\Omega_{\mathrm{ASH}}=0\) standard-baseline identity, deterministic
  generator, targeted tests, generated CSV/PNG artifacts, validation JSON,
  covariance output, and boundary documentation. This does not derive
  Einstein equations, prove physical FRW continuum cosmology, validate or
  replace \(\Lambda\)CDM, compute CMB or matter spectra, provide external
  likelihoods, detect dark energy or modified gravity, or lock prospective
  predictions.
  Verification: `python3 tools/generate_cosmological_background.py --out-root . --refresh-figures`,
  `python3 -m pytest tests/test_cosmological_background.py`,
  `python3 tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  `python3 tools/run_proof_suite.py`, `python3 -m pytest`,
  `python3 tools/verify_repository.py`, and
  `python3 tools/final_repository_audit.py .`.

### 2026-06-26

- Post-merge publication state refreshed after R-010 and R-011 landed on
  `main`. Repository documentation, roadmap status, changelog, tracked wiki
  mirror, and live wiki publication are aligned to the current finite-observer
  state. Boundary: this is a documentation/publication update only; it does
  not close R-012 through R-016.
- R-011 marked complete for finite-observer limit closure only. Evidence:
  nested parity-valid observer hierarchy over odd levels `1,3,5,7,9`,
  projective consistency and uniform-fiber verification, finite pair-flip
  causal cones, event non-expansion under projection, normalized
  R010-compatible scale annotations, generated CSV/JSON/PNG artifacts,
  targeted tests, proof-suite coverage, and boundary documentation. This does
  not derive a differentiable continuum, Lorentzian metric, physical light
  cones, Einstein equations, FRW/LCDM background dynamics, physical
  perturbation equations, CMB/matter spectra, external likelihoods, empirical
  cosmology, locked scientific prediction, or model closure.
  Verification: `python tools/generate_finite_observer_limit.py --out-root . --refresh-figures`,
  `python -m pytest tests/test_finite_observer_limit.py`,
  `python tools/generate_artifacts.py`, `python tools/run_proof_suite.py`,
  `python -m pytest`, `python tools/verify_repository.py`,
  `python docs/ash-physics-validation/scripts/run_repository_gate.py .`,
  `python tools/validate_json_assets.py .`,
  `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  and `python tools/final_repository_audit.py .`.
- R-010 marked complete for a synthetic finite-observer unit-bearing bridge to
  named proxy observables. Evidence: explicit SI unit map, versioned fiducial
  calibration contract, data provenance, generated finite features,
  unit-bearing proxy observables, bootstrap samples, final-depth covariance,
  deterministic generator, tests, proof-suite coverage, and boundary
  documentation. This does not close reviewed physical calibration, continuum
  metric, FRW/LCDM derivation, physical perturbation solver, external
  likelihood, empirical validation, locked scientific prediction, or model
  closure gates.
  Verification: `python tools/generate_unit_bridge.py --out-root .`,
  `python -m pytest tests/test_unit_bridge.py`,
  `python tools/generate_artifacts.py`, `python tools/run_proof_suite.py`,
  `python -m pytest`, `python tools/verify_repository.py`,
  `python docs/ash-physics-validation/scripts/run_repository_gate.py .`,
  `python tools/validate_json_assets.py .`,
  `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  and `python tools/final_repository_audit.py .`.
- R-009 marked complete for the finite observer-commitment, committed-memory,
  and branch-separation workbench. Evidence: deterministic observer commitment
  implementation, R-008-backed branch allocation in the reproducible demo tree,
  targeted tests, generated data products, proof-suite coverage, and validation
  JSON. Boundary: finite observer-relative commitment and branch-separation
  workbench only; no collapse claim, no Born-rule proof, no unitary
  Hilbert-space dynamics, no unit-bearing spacetime bridge, no
  CMB/matter-spectrum solver, and no empirical cosmology validation.
  Verification: `python tools/generate_observer_commitment.py --out-root . --depth 4 --pair-sample-limit 5000`,
  `python -m pytest tests/test_observer_commitment.py`,
  `python tools/run_proof_suite.py`, `python -m pytest`,
  `python tools/verify_repository.py`,
  `python docs/ash-physics-validation/scripts/run_repository_gate.py .`,
  `python tools/validate_json_assets.py .`,
  `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  and `python tools/final_repository_audit.py .`.
- R-008 marked complete for a finite-observer branch measure law. Evidence:
  explicit classical Gibbs/action-weighted branch measure, optional
  norm-preserving amplitude decoration, deterministic frontier artifacts, and
  tests verifying sibling normalization, total-measure preservation, and
  amplitude-norm preservation. Boundary: this closes only the finite
  branch-measure law. It does not prove a Born rule, define Hilbert-space
  dynamics, provide observer commitment or decoherence, define a unit-bearing
  physical bridge, compute empirical spectra, or validate cosmology.
  Verification: `python tools/generate_branch_measure.py --out-root .`,
  `python tools/generate_artifacts.py`, `python tools/run_proof_suite.py`,
  `python -m pytest`, `python tools/verify_repository.py`,
  `python docs/ash-physics-validation/scripts/run_repository_gate.py .`,
  `python tools/validate_json_assets.py .`,
  `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  and `python tools/final_repository_audit.py .`.
- R-007 marked complete for the finite-observer Roadmap 007 linear
  perturbation sector. Evidence: quotient Walsh-shell implementation,
  targeted tests, deterministic transfer artifacts, generated figures,
  validation JSON, and finite-boundary documentation. This does not close the
  physical perturbation, CMB, matter-spectrum, physical-wavenumber, or
  empirical-validation gates tracked by R-013 and R-014.
  Verification: `python tools/generate_linear_perturbations.py --out-root . --refresh-figures`,
  `python tools/generate_artifacts.py`, `python tools/run_proof_suite.py`,
  `python -m pytest`, `python tools/verify_repository.py`,
  `python docs/ash-physics-validation/scripts/run_repository_gate.py .`,
  `python tools/validate_json_assets.py .`,
  `python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json`,
  and `python tools/final_repository_audit.py .`.
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
