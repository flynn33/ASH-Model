# Roadmap 010 Unit-Bearing Bridge

Roadmap 010 adds a synthetic finite-observer bridge from accepted Roadmap 009 branch-frontier outputs to named SI-unit proxy observables.

## Purpose

The bridge turns finite branch summaries into a versioned observable table:

\[
\mathcal{B}_{\ell}:(\Gamma,\mathcal{T},\mu,\mathcal{M};\Theta_{\ell})\to\mathcal{Y}_{\ell}.
\]

The finite feature vector is

\[
f_n=(n,\mathbb{E}_{\mu}q,\operatorname{Var}_{\mu}q,\mathbb{E}_{\mu}d,\mathbb{E}_{\mu}|M|,S_B,S_M,\chi_D).
\]

## Computed proxy observables

| Quantity | Meaning |
|---|---|
| `time_s` | fiducial elapsed observer time |
| `coarse_length_m` | fiducial coarse length proxy |
| `scale_factor_dimensionless` | entropy-derived synthetic scale factor |
| `H_bridge_s_inv` | finite difference of log scale factor |
| `energy_density_J_m3` | defect-density energy proxy |
| `mass_density_kg_m3` | energy proxy divided by \(c^2\) |
| `einstein_curvature_proxy_m_inv2` | curvature proxy from fiducial constants |
| `memory_length_m` | committed-memory length proxy |
| `temperature_proxy_K` | shell-index temperature proxy |

## Repository evidence

| Evidence | Path |
|---|---|
| Implementation | `src/ash_model/unit_bridge.py` |
| Generator | `tools/generate_unit_bridge.py` |
| Calibration contract | `config/ash_r010_unit_bridge_calibration.json` |
| Tests | `tests/test_unit_bridge.py` |
| Documentation | `docs/ash-cosmology/unit-bridge/roadmap-010/README.md` |
| Data outputs | `data/ash-cosmology/unit-bridge/v0.1/` |
| Validation output | `validation/unit-bridge/roadmap-010/outputs/verification.json` |
| Proof certificate | `proofs/computational-certificate.json` |

## Verification

```bash
python tools/generate_unit_bridge.py --out-root .
python -m pytest tests/test_unit_bridge.py
python tools/run_proof_suite.py
python tools/verify_repository.py
python tools/validate_data_manifest.py --manifest data/manifests/data_manifest.json
```

## Boundary

R-010 is a synthetic finite-observer bridge workbench. Its default calibration constants are fiducial. It does not supply reviewed ASH physical constants, a continuum metric, FRW/LCDM derivation, external likelihood, empirical validation, CMB or matter-spectrum solver, or locked scientific prediction.
