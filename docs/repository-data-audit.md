# Repository Data Audit

## Project Summary

ASH Model is a Python research and reference-implementation repository for finite ASH mathematics, deterministic mapping semantics, finite-observer physics, sector-mixing workbench evidence, and synthetic background-bridge diagnostics.

| Field | Value |
|---|---|
| Project type | Python package, research repository, documentation and validation repository |
| Primary language | Python |
| Package manager | `pyproject.toml` with editable install support |
| Test framework | `pytest` |
| Current version | `1.1.0` |
| Current audited branch | `main` |

## Existing Structure

| Area | Paths |
|---|---|
| Package source | `src/ash_model/` |
| Tests | `tests/` |
| Data and evidence | `data/`, `validation/`, `figures/`, `proofs/` |
| Documentation | `README.md`, `docs/`, `wiki/`, `changelog/CHANGELOG.md` |
| Validation tooling | `tools/`, `docs/ash-physics-validation/scripts/` |
| Automation | `.github/workflows/` |

## Data Handling Observations

- Core data files in `data/` are deterministic repository evidence or committed package assets.
- Synthetic background-bridge diagnostics live under `validation/background_bridge/pass_003/outputs/`.
- The repository already records generated artifact hashes in `proofs/artifact-manifest.json`.
- The repository did not have one consolidated data manifest covering data assets and synthetic validation outputs before this update.
- No new raw dataset was supplied with the 2026-06-26 instruction package.

## Tooling and Dependencies

The repository uses `numpy`, `matplotlib`, `pytest`, and `jsonschema` through `pyproject.toml`. Existing validation commands include:

```bash
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python tools/validate_json_assets.py .
python tools/check_generated_outputs.py . --include-manuscript
```

## Security and Privacy Review

| Risk category | Rating | Notes |
|---|---|---|
| Security | low | No secrets are required for local data validation. |
| Privacy | low | Manifested files are finite-state evidence, package metadata, and synthetic diagnostics. |
| Licensing | medium | Core generated evidence follows the repository license; some package-derived data has no separate source license statement. |
| Maintainability | low | Data assets are already structured, but consolidated manifest validation was missing. |
| Large files | low | Current manifested assets are small enough for Git; future large raw data should use external storage or Git LFS. |

## Documentation Review

The README and wiki describe data and evidence at a high level. This update adds `data/README.md` and a machine-readable data manifest so future maintainers can validate the tracked data inventory directly.

## Test and CI Review

The repository already has a comprehensive test suite and CI workflow. This update adds a dedicated data-manifest validator and wires it into both tests and CI.

## Recommended Integration Strategy

Because no new dataset was supplied, the safe integration is metadata-first:

1. Add a consolidated manifest for existing tracked data assets.
2. Add a manifest schema and validator.
3. Add a regression test for the manifest validator.
4. Document data provenance, validation, privacy, and large-file policy.
5. Keep raw-data integration deferred until actual raw data and publication approval are supplied.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Package-derived data has incomplete standalone license metadata | Manifest records conservative license status instead of inventing terms. |
| Future raw data could contain sensitive content | `data/README.md` requires review before adding raw data. |
| Manifest drift | `tools/validate_data_manifest.py` checks paths, sizes, and SHA-256 hashes. |
| Generated evidence drift | Existing proof and artifact checks remain required. |

## Open Questions

- If future raw datasets are supplied, should they be committed directly, stored with Git LFS, or referenced externally?
- Should package-derived roadmap and sector-mixing assets receive a separate explicit data license statement?
