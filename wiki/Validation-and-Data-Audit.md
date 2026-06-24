# Validation and Data Audit

## Validation stack

```mermaid
flowchart TD
    A["Repository checkout"] --> B["Install editable package"]
    B --> C["Generate artifact manifests"]
    C --> D["Run proof suite"]
    D --> E["Run tests"]
    E --> F["Verify repository manifests"]
    F --> G["Run repository and readiness gates"]
```

## Current command set

```bash
python -m pip install -e ".[dev]"
python tools/generate_artifacts.py
python tools/build_manuscript.py
python tools/run_proof_suite.py
python -m pytest
python tools/verify_repository.py
python docs/ash-physics-validation/scripts/check_claim_language.py .
python docs/ash-physics-validation/scripts/check_sensitive_language.py .
python docs/ash-physics-validation/scripts/run_repository_gate.py .
python tools/validate_json_assets.py .
python tools/check_generated_outputs.py . --include-manuscript
python tools/audit_physics_readiness.py . --expect-open --write-json docs/remediation/physics-readiness.json
python tools/audit_live_repository_readiness.py .
python tools/final_repository_audit.py . --write-json docs/remediation/final-remediation-evidence.json
```

## Current result

| Check | Result |
|---|---|
| Proof suite | all checks pass |
| Tests | 83 pass |
| Repository verifier | no mismatches |
| JSON schema validation | pass |
| Generated-output check | pass |
| Live repository readiness | pass |
| Physics readiness | not ready, 12 science blockers open |

## Audit files

- `docs/final-live-repository-audit.md`
- `docs/remediation/final-remediation-evidence.json`
- `docs/remediation/physics-readiness.json`
- `validation/status.json`
