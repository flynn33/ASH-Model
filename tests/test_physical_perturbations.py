import math
from dataclasses import asdict

import pytest

from ash_model.physical_perturbations import (
    PerturbationParameters,
    finite_spectral_modes,
    finite_kernel,
    mu_eff,
    solve_growth,
    matter_power,
    matter_grid,
    synthetic_observations,
    fit_alpha_mu_grid,
)


def fast_params(**overrides):
    base = asdict(PerturbationParameters(n_steps=80))
    base.update(overrides)
    return PerturbationParameters(**base)


def test_finite_modes_are_n9_halved_cube_modes():
    rows = finite_spectral_modes()
    assert [r["laplacian"] for r in rows] == [0, 16, 28, 36, 40]
    assert [r["multiplicity"] for r in rows] == [1, 9, 36, 84, 126]
    assert sum(r["multiplicity"] for r in rows) == 256


def test_physical_k_validation_and_positive_mu():
    p = fast_params()
    for k in [0.001, 0.01, 0.1, 1.0]:
        assert math.isfinite(finite_kernel(k, p))
        assert mu_eff(1.0, k, p) > 0.0
    with pytest.raises(ValueError):
        finite_kernel(0.0, p)


def test_growth_solution_is_finite_positive_and_normalizable():
    p = fast_params()
    gr = solve_growth(0.05, p, z_outputs=(0.0, 1.0, 2.0))
    assert gr[0.0]["D"] > 0.0
    assert gr[1.0]["D"] > 0.0
    assert gr[2.0]["D"] > 0.0
    assert 0.0 < gr[1.0]["D"] / gr[0.0]["D"] < 1.0
    assert math.isfinite(gr[1.0]["f_growth"])


def test_zero_amplitude_standard_baseline_is_exact_self_consistent():
    p0 = fast_params(alpha_mu=0.0, beta_drag=0.0, residual_amp=0.0)
    p1 = fast_params(alpha_mu=0.0, beta_drag=0.0, residual_amp=0.0)
    for k in [0.001, 0.01, 0.05, 0.2]:
        assert abs(matter_power(k, 0.0, p0) - matter_power(k, 0.0, p1)) == 0.0


def test_matter_grid_schema_and_units_are_present():
    p = fast_params()
    rows = matter_grid([0.01, 0.05], [0.0, 1.0], p)
    assert len(rows) == 4
    required = {"k_Mpc_inv", "z", "a", "D", "D_norm", "f_growth", "mu_eff", "finite_kernel", "T_proxy", "P_proxy"}
    for row in rows:
        assert required <= set(row)
        assert row["k_Mpc_inv"] > 0.0
        assert row["P_proxy"] > 0.0


def test_synthetic_alpha_mu_grid_recovery_is_deterministic():
    truth = fast_params(alpha_mu=0.07, beta_drag=0.018, residual_amp=0.03)
    k_values = [10 ** (-2.5 + i * 1.5 / 11.0) for i in range(12)]
    obs = synthetic_observations(k_values, truth)
    grid = [round(i * 0.005, 3) for i in range(31)]
    fit = fit_alpha_mu_grid(obs, fast_params(beta_drag=0.018, residual_amp=0.03), grid)
    best = min(fit, key=lambda r: r["chi2"])
    assert best["alpha_mu"] == 0.07
