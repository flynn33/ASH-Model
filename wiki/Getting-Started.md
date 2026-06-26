# Getting Started

This page gets a local ASH Model checkout installed and verified.

## Clone

```bash
git clone https://github.com/flynn33/ASH-Model.git
cd ASH-Model
```

## Install

```bash
python -m pip install -e ".[dev]"
```

The editable package install is the repository-supported setup path for the current validation suite.

## First verification pass

```bash
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

Expected current result:

| Command | Expected result |
|---|---|
| `tools/generate_artifacts.py` | 6 data artifacts generated, 5 figure artifacts verified |
| `tools/build_manuscript.py` | 9 source inputs recorded |
| `tools/run_proof_suite.py` | `all_checks_pass: true` |
| `python -m pytest` | 143 collected tests pass |
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
