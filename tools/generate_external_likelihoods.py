#!/usr/bin/env python3
"""Generate R-014 external-likelihood readiness artifacts.

The generated products are synthetic ASH workbench fixtures plus metadata-only
external data-product contracts.  No third-party observational data are bundled
or analyzed by this generator.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ash_model.external_likelihoods import (
    Params,
    canonical_json_hash,
    condition_number,
    evaluate_models,
    fit_grid,
    generate_synthetic,
    is_spd,
    theory_vector,
    whitened_residuals,
)

REGISTRY = [
    {
        "id": "Planck2018_PLC",
        "probe": "CMB TTTEEE+lensing",
        "role": "reviewed external target",
        "data_status": "not bundled; contract only",
        "covariance_policy": "use official Planck likelihood/covariance where licensed",
        "source": "ESA Planck Legacy Archive / Planck 2018 papers",
        "license_note": "external user must obtain from official release",
    },
    {
        "id": "PantheonPlus",
        "probe": "Type Ia SN distance moduli",
        "role": "reviewed external target",
        "data_status": "not bundled; contract only",
        "covariance_policy": "use Pantheon+ statistical+systematic covariance",
        "source": "Pantheon+ public release/papers",
        "license_note": "external user must obtain from official release",
    },
    {
        "id": "DESI_DR2_BAO",
        "probe": "BAO distances",
        "role": "current reviewed BAO target",
        "data_status": "not bundled; contract only",
        "covariance_policy": "use DESI DR2 published covariance/likelihood",
        "source": "DESI DR2 publications/data portal",
        "license_note": "external user must obtain from official release",
    },
    {
        "id": "BOSS_DR12_BAO",
        "probe": "BAO/RSD distances",
        "role": "stable matched baseline target",
        "data_status": "not bundled; contract only",
        "covariance_policy": "use SDSS/BOSS DR12 measurement covariance/likelihood",
        "source": "SDSS/BOSS publications and SAS",
        "license_note": "external user must obtain from official release",
    },
]

LIKELIHOOD_CONTRACT = {
    "package": "ASH R-014 external likelihoods and matched baselines",
    "version": "0.1.0-repository-overlay",
    "upstream_assumed": [
        "R-008 accepted",
        "R-009 accepted",
        "R-010 accepted",
        "R-011 accepted",
        "R-012 accepted",
        "R-013 accepted",
    ],
    "closure_route": "external-likelihood readiness with synthetic fixtures and reviewed-data contracts",
    "probes": ["SN_mu", "BAO_DM_rd", "BAO_DH_rd", "GROWTH_fsigma8", "CMB_lowell_Dl"],
    "likelihood": "Gaussian -0.5[(d-m)^T C^-1 (d-m)+log det C+n log(2pi)] with Cholesky solve",
    "external_data_policy": "No third-party data are bundled. Registry defines required official products, covariance source, provenance, and lock hashes to be computed after ingestion.",
    "matched_baselines": ["LCDM_nested_baseline", "ASH_background_only", "ASH_perturbation_only", "ASH_truth_family"],
    "falsification_thresholds": {
        "covariance_not_spd": "fail",
        "unregistered_external_hash_change_after_unblinding": "fail",
        "matched_LCDM_or_control_DeltaAIC_le_0_on_claimed_signature": "demote ASH-specific claim",
        "locked_prediction_modified_after_freeze": "fail R-015, not R-014",
        "ASH_grid_recovery_abs_error_omega_ash_gt_0.005_on_synthetic": "fail synthetic readiness",
        "ASH_grid_recovery_abs_error_alpha_mu_gt_0.02_on_synthetic": "fail synthetic readiness",
    },
    "limitations": [
        "synthetic validation only",
        "not a real-data likelihood run",
        "not a Planck/Pantheon/DESI/BOSS redistribution",
        "not an empirical claim",
    ],
}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def generate(out_root: Path) -> dict:
    config_dir = out_root / "config"
    data_dir = out_root / "data" / "ash-cosmology" / "external-likelihoods" / "v0.1"
    val_dir = out_root / "validation" / "external-likelihoods" / "roadmap-014" / "outputs"
    for p in [config_dir, data_dir, val_dir]:
        p.mkdir(parents=True, exist_ok=True)

    rows, y, cov, truth = generate_synthetic()
    hash_payload = {"rows": rows, "y": [round(float(v), 10) for v in y], "cov_shape": list(cov.shape), "seed": 20260626}
    lock_hash = canonical_json_hash(hash_payload)

    _write_json(config_dir / "ash_r014_data_product_registry.json", REGISTRY)
    _write_json(config_dir / "ash_r014_likelihood_contract.json", LIKELIHOOD_CONTRACT)

    with (data_dir / "r014_synthetic_observations.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["index", "probe", "x", "z", "k", "unit", "observed", "truth"])
        for i, (r, obs, tr) in enumerate(zip(rows, y, truth)):
            w.writerow([i, r["probe"], r["x"], r["z"], r["k"], r["unit"], obs, tr])

    with (data_dir / "r014_synthetic_covariance.csv").open("w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(cov)

    sig = np.sqrt(np.diag(cov))
    corr = cov / np.outer(sig, sig)
    with (data_dir / "r014_covariance_summary.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["index", "probe", "sigma", "row_abs_corr_sum"])
        for i, r in enumerate(rows):
            w.writerow([i, r["probe"], sig[i], np.sum(np.abs(corr[i]))])

    models = evaluate_models(rows, y, cov)
    with (data_dir / "r014_model_comparison.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(models[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(models)

    omega_grid = np.linspace(0.0, 0.04, 41)
    alpha_grid = np.linspace(0.0, 0.14, 29)
    grid = fit_grid(rows, y, cov, omega_grid, alpha_grid)
    with (data_dir / "r014_ash_grid_likelihood.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grid[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(grid)

    best = grid[0]
    tbest = theory_vector(rows, Params(omega_ash=best["omega_ash"], alpha_mu=best["alpha_mu"]), "ash")
    wr = whitened_residuals(y, tbest, cov)
    with (data_dir / "r014_whitened_residuals_bestfit.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["index", "probe", "whitened_residual"])
        for i, (r, val) in enumerate(zip(rows, wr)):
            w.writerow([i, r["probe"], val])

    prereg = {
        "freeze_label": "R014_SYNTHETIC_EXTERNAL_LIKELIHOOD_FIXTURE",
        "freeze_date_utc": "2026-06-26T00:00:00Z",
        "is_blinded_fixture": True,
        "synthetic_seed": 20260626,
        "data_vector_sha256": lock_hash,
        "model_grid": {
            "omega_ash_min": 0.0,
            "omega_ash_max": 0.04,
            "omega_ash_step": 0.001,
            "alpha_mu_min": 0.0,
            "alpha_mu_max": 0.14,
            "alpha_mu_step": 0.005,
        },
        "unblinding_policy": "External products may be evaluated only after registry entry includes official source, license note, covariance file hash, data-vector hash, and baseline freeze.",
    }
    _write_json(val_dir / "r014_preregistration_lock.json", prereg)

    validation = {
        "pytest_expected": "see tests/test_external_likelihoods.py",
        "n_data": len(rows),
        "covariance_spd": is_spd(cov),
        "covariance_condition_number": condition_number(cov),
        "synthetic_data_hash": lock_hash,
        "best_grid_omega_ash": best["omega_ash"],
        "best_grid_alpha_mu": best["alpha_mu"],
        "truth_omega_ash": 0.02,
        "truth_alpha_mu": 0.07,
        "omega_recovery_abs_error": abs(best["omega_ash"] - 0.02),
        "alpha_recovery_abs_error": abs(best["alpha_mu"] - 0.07),
        "best_model_by_AIC": models[0]["model"],
        "model_comparison": models,
        "whitened_residual_mean": float(np.mean(wr)),
        "whitened_residual_std": float(np.std(wr, ddof=1)),
        "external_data_claim": "none; contracts only",
        "closure_boundary": "R-014 external-likelihood readiness and synthetic validation, not empirical validation",
    }
    _write_json(val_dir / "verification.json", validation)
    return validation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=".", type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.out_root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
