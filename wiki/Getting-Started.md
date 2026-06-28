# Getting Started

This page gets a local ASH Model checkout installed and verified.

## Clone

```bash
git clone https://github.com/flynn33/ASH-Model.git
cd ASH-Model
```

## Install

```bash
python3 -m pip install -e ".[dev]"
```

The editable package install is the repository-supported setup path for the current validation suite.

## First verification pass

```bash
python3 tools/generate_artifacts.py
python3 tools/build_manuscript.py
python3 tools/run_proof_suite.py
python3 -m pytest
python3 tools/verify_repository.py
```

Expected current result:

| Command | Expected result |
|---|---|
| `tools/generate_artifacts.py` | generated data and figure artifacts verified |
| `tools/build_manuscript.py` | manuscript source inputs recorded |
| `tools/run_proof_suite.py` | `all_checks_pass: true` |
| `python3 -m pytest` | collected tests pass |
| `tools/verify_repository.py` | no manifest, version, or proof mismatches |
| `tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json` | data-manifest validation passes |

## Next reading step

Read these in order:

1. `README.md`
2. `docs/canonical-computational-specification.md`
3. `docs/mathematical-proof.md`
4. `ROADMAP.md`
5. `docs/ash-physics-validation/README.md`
6. `docs/ash-cosmology/unit-bridge/roadmap-010/README.md`
7. `docs/ash-cosmology/finite-observer-limit/roadmap-011/README.md`
8. `docs/ash-cosmology/background-equations/roadmap-012/README.md`
9. `docs/ash-cosmology/physical-perturbations/roadmap-013/README.md`
10. `docs/ash-cosmology/external-likelihoods/roadmap-014/README.md`
11. `docs/ash-cosmology/locked-predictions/roadmap-015/README.md`
12. `docs/ash-cosmology/branch-centered-closure/roadmap-016/README.md`
