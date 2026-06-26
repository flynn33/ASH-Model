# Auditor Checklist

## Package Completeness

- [ ] `src/ash_model/background_bridge.py` exists.
- [ ] `tests/test_background_bridge_remediation.py` exists.
- [ ] `tools/run_background_bridge_validation.py` exists.
- [ ] `docs/ash-cosmology/background-bridge/pass-003/` exists.
- [ ] `validation/background_bridge/pass_003/outputs/validation_summary.json` exists.
- [ ] `validation/background_bridge/pass_003/outputs/pytest_validation.log` exists.
- [ ] `validation/background_bridge/pass_003/SHA256SUMS.json` exists.

## Reproducibility

- [ ] Run `python tools/run_background_bridge_validation.py`.
- [ ] Run `python -m pytest tests/test_background_bridge_remediation.py -q`.
- [ ] Confirm JSON assets parse with `python tools/validate_json_assets.py .`.
- [ ] Confirm repository verification passes after proof metadata is refreshed.

## Scientific Discipline

- [ ] Confirm the validation is synthetic-only.
- [ ] Confirm the bridge equation is fixed before synthetic fitting.
- [ ] Confirm nested LCDM is included.
- [ ] Confirm a matched random-template null is included.
- [ ] Confirm LCDM synthetic data do not force nonzero branch coupling.
- [ ] Confirm unsupported claims are recorded as hypotheses or blockers.

## Numerical Checks

- [ ] Recovered `beta_branch` is within tolerance of the injected value.
- [ ] Recovered `gamma_branch` is within tolerance of the injected value.
- [ ] ASH chi-square on ASH synthetic data is lower than nested LCDM.
- [ ] ASH chi-square on ASH synthetic data is lower than matched random null.
- [ ] Grid-posterior standard deviations are positive.
- [ ] 384-to-768 integration-grid convergence passes.

## Handoff Decision

The pass is ready only if all checklist items pass or deviations are explicitly
documented in this directory.
