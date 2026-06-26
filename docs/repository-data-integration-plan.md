# Repository Data Integration Plan

## Summary

The 2026-06-26 instruction package supplied repository-update procedures but no new raw data. This plan therefore integrates data governance for the existing ASH data assets instead of importing a new dataset.

## Data Classification

| Data group | Classification | Tracking policy |
|---|---|---|
| Core finite ASH evidence in `data/*.csv` and `data/*.json` | generated-output | Git |
| Branch-centered roadmap package assets | documentation-asset | Git |
| Sector-mixing pass 002 evidence | generated-output and documentation-asset | Git |
| Background bridge pass 003 outputs | generated-output | Git |
| Future raw data not yet supplied | raw | Undecided; require owner approval |

## File Mapping

No external file is imported in this pass. The new manifest maps existing tracked assets in place:

```text
data/* -> data/manifests/data_manifest.json
validation/background_bridge/pass_003/outputs/* -> data/manifests/data_manifest.json
validation/status.json -> data/manifests/data_manifest.json
```

## Transformations

No data transformation is added. The manifest records current file size and SHA-256 values for existing tracked files.

## Code Changes

| Path | Purpose |
|---|---|
| `tools/validate_data_manifest.py` | Validate manifest structure, file existence, byte counts, and SHA-256 hashes. |
| `tools/validate_json_assets.py` | Include the data manifest schema in repository JSON validation. |
| `tests/test_data_manifest.py` | Regression test for manifest validation. |

## Documentation Changes

| Path | Purpose |
|---|---|
| `data/README.md` | Explain data layout, provenance, validation, privacy, license, and large-file policy. |
| `docs/repository-data-audit.md` | Record the repository audit required by the instruction package. |
| `docs/repository-data-integration-plan.md` | Record this integration plan. |
| `README.md` | Add a concise data governance pointer. |
| `changelog/CHANGELOG.md` | Record the metadata and validation update. |

## Testing Changes

The new validation path is:

```bash
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
python tools/validate_json_assets.py .
python -m pytest tests/test_data_manifest.py
```

The broader repository validation remains:

```bash
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
```

## Git Tracking Policy

Current manifested assets remain tracked in Git. Future large raw data should be tracked with Git LFS or referenced externally unless the owner explicitly approves normal Git tracking.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| No actual new data was supplied | Record a no-import integration rather than fabricating data assets. |
| Future raw data may be sensitive | Keep raw data approval and sensitivity review as required future work. |
| Manifest can become stale | Add validator and test coverage. |
| Documentation can overstate validation | Keep the manifest as metadata and preserve scientific claim boundaries. |

## Rollback Plan

Revert the manifest, validator, docs, test, and README/changelog updates. No raw data or processed outputs are created by this pass, so rollback does not require deleting imported data.
