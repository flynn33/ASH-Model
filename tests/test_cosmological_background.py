import sys, math
from pathlib import Path
from ash_model.cosmological_background import *

def test_lcdm_limit_exact():
    p = BackgroundParameters(Omega_ash=0.0)
    for a in [1e-3, 0.01, 0.1, 0.5, 1.0]:
        assert abs(ash_E2(a, p) - lcdm_E2(a, p)) < 1e-15

def test_today_closure_with_ash_source_normalized():
    p = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    assert abs(ash_source_E(1.0, p) - 1.0) < 1e-12
    assert abs(ash_E2(1.0, p) - p.closure_sum_today()) < 1e-12
    assert abs(p.closure_sum_today() - 1.0) < 1e-10

def test_positive_expansion_and_finite_w():
    p = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    for a in [1e-3, 0.01, 0.1, 0.5, 1.0]:
        assert ash_E2(a, p) > 0
        assert math.isfinite(H_km_s_Mpc(a, p))
        assert math.isfinite(w_ash(a, p))

def test_integration_monotone_age_distance():
    p = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    rows = integrate_background(p, steps=50)
    ages = [r["t_Gyr_since_a_min"] for r in rows]
    chis = [r["chi_Mpc_from_a_min"] for r in rows]
    assert all(y >= x for x, y in zip(ages, ages[1:]))
    assert all(y >= x for x, y in zip(chis, chis[1:]))

def test_synthetic_recovery_near_truth():
    truth = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    obs = synthetic_observations(truth, [0.25,0.33,0.45,0.6,0.8,1.0], sigma_frac=1e-6)
    grid = [i/10000 for i in range(0, 501)]
    best, _ = grid_fit_omega_ash(obs, BackgroundParameters(Omega_Lambda=0.66491), grid)
    assert abs(best["Omega_ash"] - 0.020) <= 0.010


def test_repository_aliases_available():
    p = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    assert abs(ash_source_xi(1.0, p) - 1.0) < 1e-12
    assert finite_background_features(1.0)["parity_density"] == 0.5
    assert math.isfinite(effective_w_ash(0.5, p))

def test_covariance_matrix_shape():
    p = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)
    rows = integrate_background(p, steps=40)
    cols = ["E2", "H_km_s_Mpc", "ash_source_E", "w_ash", "q"]
    cov = covariance_matrix(rows[::4], cols)
    assert len(cov) == len(cols)
    assert all(len(row) == len(cols) for row in cov)
