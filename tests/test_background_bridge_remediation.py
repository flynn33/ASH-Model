import json
import warnings

import numpy as np
import pytest

from ash_model.background_bridge import (
    BackgroundParams,
    H_ash,
    angular_diameter_distance,
    branch_entropy_template,
    comoving_distance,
    convergence_diagnostics,
    distance_modulus,
    posterior_from_grid,
    run_validation,
)


def test_bridge_observables_are_finite_and_monotone():
    z = np.linspace(0.01, 2.0, 40)
    params = BackgroundParams(beta_branch=0.10, gamma_branch=1.4)

    h_values = H_ash(z, params)
    comoving = comoving_distance(z, params, n_grid=256)
    modulus = distance_modulus(z, params, n_grid=256)
    angular = angular_diameter_distance(z, params, n_grid=256)
    template = branch_entropy_template(z, params.gamma_branch)

    assert np.all(np.isfinite(h_values))
    assert np.all(h_values > 0)
    assert np.all(np.diff(comoving) > 0)
    assert np.all(np.diff(modulus) > 0)
    assert np.all(angular > 0)
    assert np.all(template >= 0)
    assert np.all(template < 1)


def test_invalid_inputs_are_rejected():
    params = BackgroundParams(beta_branch=0.10, gamma_branch=1.4)

    with pytest.raises(ValueError, match="nonnegative"):
        H_ash(np.array([-0.1]), params)
    with pytest.raises(ValueError, match="positive"):
        branch_entropy_template(np.array([0.1]), 0.0)
    with pytest.raises(ValueError, match="positive redshift"):
        distance_modulus(np.array([0.0]), params)
    with pytest.raises(ValueError, match="at least 2"):
        comoving_distance(np.array([0.1]), params, n_grid=1)


def test_deprecated_trapezoid_warning_is_not_emitted(tmp_path):
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        summary = run_validation(tmp_path)

    assert summary["acceptance_checks"]["recovers_beta_within_0p03"]


def test_validation_recovers_synthetic_parameters(tmp_path):
    summary = run_validation(tmp_path)
    checks = summary["acceptance_checks"]

    assert checks["recovers_beta_within_0p03"]
    assert checks["recovers_gamma_within_0p30"]
    assert checks["beats_nested_lcdm_on_ash_synthetic"]
    assert checks["beats_random_matched_null_on_ash_synthetic"]
    assert checks["does_not_force_beta_on_lcdm_synthetic"]
    assert checks["posterior_std_positive"]
    assert checks["convergence_384_to_768"]
    assert (tmp_path / "validation_summary.json").exists()

    saved = json.loads((tmp_path / "validation_summary.json").read_text(encoding="utf-8"))
    assert saved["model_version"] == "ash_background_bridge_pass_003_remediated"


def test_validation_summary_has_required_scientific_boundary(tmp_path):
    summary = run_validation(tmp_path)

    assert summary["model_version"] == "ash_background_bridge_pass_003_remediated"
    assert "posterior_uncertainty_grid" in summary
    assert "information_criteria" in summary
    assert "evidence_diagnostics" in summary
    assert "convergence_diagnostics" in summary
    assert summary["scientific_boundary"] == (
        "Synthetic validation and statistical diagnostics only; "
        "no observational validation claim is made."
    )
    assert all(summary["acceptance_checks"].values())


def test_posterior_summary_has_positive_uncertainty(tmp_path):
    summary = run_validation(tmp_path)
    posterior = summary["posterior_uncertainty_grid"]
    records = np.loadtxt(tmp_path / "ash_grid_fit_records.csv", delimiter=",", skiprows=1)

    assert posterior["beta_branch_std"] > 0.0
    assert posterior["gamma_branch_std"] > 0.0
    assert posterior_from_grid(records)["effective_sample_size"] > 1.0


def test_convergence_diagnostic_passes():
    diagnostic = convergence_diagnostics()

    assert diagnostic["passes"]
    assert diagnostic["beta_difference"] <= 0.01
    assert diagnostic["gamma_difference"] <= 0.05


def test_background_bridge_exports_from_package_surface():
    import ash_model

    assert ash_model.H_ash is H_ash
    assert ash_model.branch_entropy_template is branch_entropy_template
    assert ash_model.run_background_bridge_validation is run_validation
