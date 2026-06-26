# Validation

## Commands

```bash
python tools/run_background_bridge_validation.py
python -m pytest tests/test_background_bridge_remediation.py -q
python -m pytest
python tools/validate_json_assets.py .
python tools/verify_repository.py
python tools/generate_artifacts.py
python tools/run_proof_suite.py
python tools/verify_repository.py
python tools/check_generated_outputs.py . --include-manuscript
python -m compileall -q simulation.py src tools scripts docs/ash-physics-validation/scripts
```

## Deterministic Outputs

The runner writes:

```text
validation/background_bridge/pass_003/outputs/validation_summary.json
validation/background_bridge/pass_003/outputs/synthetic_supernova_ash.csv
validation/background_bridge/pass_003/outputs/synthetic_H_ash.csv
validation/background_bridge/pass_003/outputs/ash_grid_fit_records.csv
validation/background_bridge/pass_003/outputs/background_curves.csv
```

Focused test stdout is captured in:

```text
validation/background_bridge/pass_003/outputs/pytest_validation.log
```

## Required Summary Keys

- `model_version`
- `remediates_audit_findings`
- `posterior_uncertainty_grid`
- `information_criteria`
- `evidence_diagnostics`
- `convergence_diagnostics`
- `acceptance_checks`
- `scientific_boundary`

## Acceptance Checks

The validation accepts only if all listed checks are true:

```text
recovers_beta_within_0p03
recovers_gamma_within_0p30
beats_nested_lcdm_on_ash_synthetic
beats_random_matched_null_on_ash_synthetic
does_not_force_beta_on_lcdm_synthetic
posterior_std_positive
convergence_384_to_768
```

## Limitation

The synthetic data are intentionally emitted from the same bridge family being
tested. Passing this gate shows internal recovery and guardrail behavior only.
