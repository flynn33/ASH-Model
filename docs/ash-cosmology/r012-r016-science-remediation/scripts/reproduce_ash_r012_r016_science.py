#!/usr/bin/env python3
"""
ASH R012-R016 science remediation reproduction script.

This is an independent research artifact. It does not modify or manage the ASH-Model
repository. It uses the finite ASH parity/pair-flip structure as a mathematical input
and evaluates a concrete finite-spectral cosmology extension against compact published
external measurements.

Outputs:
  data/ash_pair_flip_spectrum.csv
  outputs/model_fit_summary.csv/json
  outputs/bao_residuals.csv
  outputs/growth_predictions.csv
  outputs/locked_prediction_pilot_scores.json/csv
  figures/*.png
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from scipy.integrate import quad, solve_ivp
from scipy.optimize import differential_evolution, minimize, brentq
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
FIG = ROOT / "figures"
for d in (DATA, OUT, FIG):
    d.mkdir(exist_ok=True, parents=True)

C_KM_S = 299_792.458
R_D_PLANCK_MPC = 147.09

# Compact real-data table transcribed from DESI DR2 Results II, Table IV.
# Values are BAO distance ratios at effective redshifts. Correlation signs are
# negative in the table; the PDF text extraction renders the minus glyph imperfectly.
DESI_BGS = {"tracer": "BGS", "z": 0.295, "DV": 7.942, "sigma_DV": 0.075}
DESI_ANISO = pd.DataFrame(
    [
        ("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
        ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
        ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
        ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
        ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500),
        ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431),
    ],
    columns=["tracer", "z", "DM_over_rd", "sigma_DM", "DH_over_rd", "sigma_DH", "rho_MH"],
)
DESI_ANISO.to_csv(DATA / "desi_dr2_bao_compact_table_iv.csv", index=False)
pd.DataFrame([DESI_BGS]).to_csv(DATA / "desi_dr2_bao_bgs_dv_table_iv.csv", index=False)

PRIORS = {
    "planck2018_base_lcdm": {
        "H0": 67.4,
        "sigma_H0": 0.5,
        "Omega_m": 0.315,
        "sigma_Omega_m": 0.007,
        "sigma8": 0.811,
        "sigma_sigma8": 0.006,
        "rd_Mpc": R_D_PLANCK_MPC,
        "sigma_rd_Mpc": 0.26,
    },
    "shoes_2022": {"H0": 73.04, "sigma_H0": 1.04},
    "des_y3_3x2pt_optimized_scale_cuts": {"S8": 0.772, "sigma_S8": 0.017},
}
pd.DataFrame(
    [
        {"dataset": "Planck2018", "quantity": "H0", "value": 67.4, "sigma": 0.5, "unit": "km/s/Mpc"},
        {"dataset": "Planck2018", "quantity": "Omega_m", "value": 0.315, "sigma": 0.007, "unit": "dimensionless"},
        {"dataset": "Planck2018", "quantity": "sigma8", "value": 0.811, "sigma": 0.006, "unit": "dimensionless"},
        {"dataset": "Planck2018-derived", "quantity": "r_d", "value": R_D_PLANCK_MPC, "sigma": 0.26, "unit": "Mpc"},
        {"dataset": "SH0ES2022", "quantity": "H0", "value": 73.04, "sigma": 1.04, "unit": "km/s/Mpc"},
        {"dataset": "DESY3_3x2pt", "quantity": "S8", "value": 0.772, "sigma": 0.017, "unit": "dimensionless"},
    ]
).to_csv(DATA / "compact_external_priors.csv", index=False)


def ash_pair_flip_spectrum(lazy: float = 0.5) -> pd.DataFrame:
    """Exact Walsh spectrum for the ASH admissible 256-state pair-flip kernel.

    In 8 independent payload coordinates, the 9D admissible pair-flip move set
    induces all 8 one-bit and all 28 two-bit flips. For a Walsh character of
    Hamming weight r, the non-lazy eigenvalue is
        mu_r = [8 - 2r + C(8,2) - 2r(8-r)] / 36
             = (r^2 - 9r + 18) / 18.
    A lazy kernel with stay probability lazy has eta_r = lazy + (1-lazy) mu_r.
    """
    rows = []
    for r in range(9):
        mu = (r * r - 9 * r + 18) / 18.0
        eta = lazy + (1.0 - lazy) * mu
        rows.append(
            {
                "r": r,
                "multiplicity": math.comb(8, r),
                "mu_nonlazy": mu,
                "eta_lazy": eta,
                "kappa_minus_ln_eta": -math.log(eta) if eta > 0 else float("nan"),
                "parity_shell": "odd" if r % 2 else "even",
            }
        )
    return pd.DataFrame(rows)


SPECTRUM = ash_pair_flip_spectrum()
SPECTRUM.to_csv(DATA / "ash_pair_flip_spectrum.csv", index=False)
KAPPA_1 = float(SPECTRUM.loc[SPECTRUM.r == 1, "kappa_minus_ln_eta"].iloc[0])
KAPPA_2 = float(SPECTRUM.loc[SPECTRUM.r == 2, "kappa_minus_ln_eta"].iloc[0])
P1 = 1.0
P2 = KAPPA_2 / KAPPA_1


def rho_de_lcdm(z: float) -> float:
    return 1.0


def rho_de_cpl(z: float, w0: float, wa: float) -> float:
    return (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z))


def rho_de_ash(z: float, b1: float, b2: float) -> float:
    a = 1.0 / (1.0 + z)
    return math.exp(b1 * (a**P1 - 1.0) + b2 * (a**P2 - 1.0))


def E_lcdm(z: float, H0: float, Om: float) -> float:
    return math.sqrt(Om * (1 + z) ** 3 + (1.0 - Om))


def E_cpl(z: float, H0: float, Om: float, w0: float, wa: float) -> float:
    val = Om * (1 + z) ** 3 + (1.0 - Om) * rho_de_cpl(z, w0, wa)
    return math.sqrt(val) if val > 0 and np.isfinite(val) else float("nan")


def E_ash(z: float, H0: float, Om: float, b1: float, b2: float) -> float:
    val = Om * (1 + z) ** 3 + (1.0 - Om) * rho_de_ash(z, b1, b2)
    return math.sqrt(val) if val > 0 and np.isfinite(val) else float("nan")


def distance_model(z: float, params: np.ndarray, model: str) -> dict[str, float] | None:
    H0 = float(params[0])
    if model == "lcdm":
        Om = float(params[1])
        Efun = lambda zz: E_lcdm(zz, H0, Om)
    elif model == "cpl":
        Om, w0, wa = map(float, params[1:4])
        Efun = lambda zz: E_cpl(zz, H0, Om, w0, wa)
    elif model == "ash":
        Om, b1, b2 = map(float, params[1:4])
        Efun = lambda zz: E_ash(zz, H0, Om, b1, b2)
    else:
        raise ValueError(f"unknown model: {model}")

    try:
        ez = Efun(z)
        if not np.isfinite(ez):
            return None
        dc = C_KM_S / H0 * quad(lambda zz: 1.0 / Efun(zz), 0.0, z, epsabs=1e-8, epsrel=1e-8, limit=128)[0]
    except Exception:
        return None
    dm = dc
    dh = C_KM_S / (H0 * ez)
    dv = (z * dm * dm * dh) ** (1.0 / 3.0)
    return {"DM_over_rd": dm / R_D_PLANCK_MPC, "DH_over_rd": dh / R_D_PLANCK_MPC, "DV_over_rd": dv / R_D_PLANCK_MPC, "E": ez}


def bounds_for(model: str) -> list[tuple[float, float]]:
    if model == "lcdm":
        return [(55.0, 80.0), (0.15, 0.45)]
    if model == "cpl":
        return [(55.0, 80.0), (0.15, 0.45), (-2.5, 0.0), (-5.0, 5.0)]
    if model == "ash":
        return [(55.0, 80.0), (0.15, 0.45), (-8.0, 8.0), (-8.0, 8.0)]
    raise ValueError(model)


def chi2_bao(params: np.ndarray, model: str, use_corr: bool = True) -> float:
    m = distance_model(DESI_BGS["z"], params, model)
    if m is None:
        return 1e100
    chi = ((m["DV_over_rd"] - DESI_BGS["DV"]) / DESI_BGS["sigma_DV"]) ** 2
    for row in DESI_ANISO.itertuples(index=False):
        pred = distance_model(float(row.z), params, model)
        if pred is None:
            return 1e100
        delta = np.array([pred["DM_over_rd"] - row.DM_over_rd, pred["DH_over_rd"] - row.DH_over_rd], dtype=float)
        if use_corr:
            cov = np.array(
                [
                    [row.sigma_DM**2, row.rho_MH * row.sigma_DM * row.sigma_DH],
                    [row.rho_MH * row.sigma_DM * row.sigma_DH, row.sigma_DH**2],
                ]
            )
            chi += float(delta @ np.linalg.inv(cov) @ delta)
        else:
            chi += (delta[0] / row.sigma_DM) ** 2 + (delta[1] / row.sigma_DH) ** 2
    return float(chi)


def in_bounds(params: np.ndarray, model: str) -> bool:
    return all(lo <= float(v) <= hi for v, (lo, hi) in zip(params, bounds_for(model), strict=True))


def chi2_bao_bounded(params: np.ndarray, model: str) -> float:
    if not in_bounds(params, model):
        return 1e50
    H0, Om = float(params[0]), float(params[1])
    if not (0.0 < Om < 1.0 and 0.0 < H0 < 200.0):
        return 1e50
    # Guard positivity/finite expansion over data domain.
    for z in np.linspace(0.0, 2.5, 64):
        m = distance_model(float(z), params, model)
        if m is None or not np.isfinite(m["E"]):
            return 1e50
    return chi2_bao(params, model, use_corr=True)


def chi2_bao_planck(params: np.ndarray, model: str) -> float:
    chi = chi2_bao_bounded(params, model)
    if not np.isfinite(chi) or chi > 1e20:
        return chi
    H0, Om = float(params[0]), float(params[1])
    p = PRIORS["planck2018_base_lcdm"]
    chi += ((H0 - p["H0"]) / p["sigma_H0"]) ** 2
    chi += ((Om - p["Omega_m"]) / p["sigma_Omega_m"]) ** 2
    return float(chi)


def fit_model(model: str, objective: Callable[[np.ndarray, str], float], seed: int = 20260628) -> tuple[np.ndarray, float]:
    """Fast deterministic multi-start fit.

    The package intentionally avoids long global optimization during reproduction.
    Starts include LCDM-like points, DESI-dynamic-DE points, and the previously
    identified finite-spectral basin; L-BFGS-B then performs the actual local fit.
    """
    bounds = bounds_for(model)
    starts: dict[str, list[list[float]]] = {
        "lcdm": [
            [67.4, 0.315],
            [69.0, 0.297],
            [66.5, 0.26],
            [72.0, 0.30],
        ],
        "cpl": [
            [67.4, 0.315, -1.0, 0.0],
            [62.1, 0.386, -0.18, -2.70],
            [67.3, 0.315, -0.82, -0.53],
            [70.0, 0.30, -0.9, -1.0],
            [64.0, 0.36, -0.5, -2.0],
        ],
        "ash": [
            [67.4, 0.315, 0.0, 0.0],
            [61.1, 0.392, 8.0, -5.72],
            [67.24, 0.314, 1.27, -0.97],
            [66.5, 0.32, 2.0, -1.5],
            [70.0, 0.30, 0.8, -0.8],
        ],
    }
    best_x = None
    best_f = float("inf")
    for start in starts[model]:
        loc = minimize(
            lambda x: objective(np.asarray(x), model),
            np.asarray(start, dtype=float),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2500, "ftol": 1e-12, "gtol": 1e-10},
        )
        if loc.fun < best_f:
            best_x = np.asarray(loc.x, dtype=float)
            best_f = float(loc.fun)
    assert best_x is not None
    return best_x, best_f


def ash_w_of_a(a: float, b1: float, b2: float) -> float:
    return -1.0 - (b1 * P1 * a**P1 + b2 * P2 * a**P2) / 3.0


def ash_wa_eff(b1: float, b2: float) -> float:
    # CPL local slope: w(a) ≈ w0 + wa(1-a), so wa = -dw/da at a=1.
    return (b1 * P1**2 + b2 * P2**2) / 3.0


def cpl_w_of_a(a: float, w0: float, wa: float) -> float:
    return w0 + wa * (1.0 - a)


def E2_lcdm_a(a: float, Om: float) -> float:
    return Om * a ** -3 + (1.0 - Om)


def E2_ash_a(a: float, Om: float, b1: float, b2: float) -> float:
    F = math.exp(b1 * (a**P1 - 1.0) + b2 * (a**P2 - 1.0))
    return Om * a ** -3 + (1.0 - Om) * F


def dlnH_dlnA_lcdm(a: float, Om: float) -> float:
    e2 = E2_lcdm_a(a, Om)
    return 0.5 * (-3.0 * Om * a ** -3) / e2


def dlnH_dlnA_ash(a: float, Om: float, b1: float, b2: float) -> float:
    F = math.exp(b1 * (a**P1 - 1.0) + b2 * (a**P2 - 1.0))
    dF = F * (b1 * P1 * a**P1 + b2 * P2 * a**P2)
    e2 = Om * a ** -3 + (1.0 - Om) * F
    de2 = -3.0 * Om * a ** -3 + (1.0 - Om) * dF
    return 0.5 * de2 / e2


def Om_a_lcdm(a: float, Om: float) -> float:
    return Om * a ** -3 / E2_lcdm_a(a, Om)


def Om_a_ash(a: float, Om: float, b1: float, b2: float) -> float:
    return Om * a ** -3 / E2_ash_a(a, Om, b1, b2)


def integrate_growth(model: str, params: np.ndarray, alpha_mu: float = 0.0, a_ini: float = 1e-3, npoints: int = 500) -> pd.DataFrame:
    x0 = math.log(a_ini)
    x1 = 0.0
    y0 = [a_ini, a_ini]  # matter-era growing mode D=a, dD/dln a = a

    def rhs(x: float, y: np.ndarray) -> list[float]:
        a = math.exp(x)
        D, V = float(y[0]), float(y[1])
        if model == "lcdm":
            Om = float(params[1])
            dlnH = dlnH_dlnA_lcdm(a, Om)
            Oma = Om_a_lcdm(a, Om)
        elif model == "ash":
            _, Om, b1, b2 = map(float, params)
            dlnH = dlnH_dlnA_ash(a, Om, b1, b2)
            Oma = Om_a_ash(a, Om, b1, b2)
        else:
            raise ValueError(model)
        # Minimal finite-mode scalar-sector coupling. The slowest ASH shell is the
        # only additional perturbation shape here; alpha_mu is calibrated below.
        mu = 1.0 + alpha_mu * a**P1
        dV = -(2.0 + dlnH) * V + 1.5 * Oma * mu * D
        return [V, dV]

    xs = np.linspace(x0, x1, npoints)
    sol = solve_ivp(rhs, (x0, x1), y0, t_eval=xs, rtol=1e-8, atol=1e-10)
    a = np.exp(sol.t)
    D = sol.y[0]
    V = sol.y[1]
    return pd.DataFrame({"a": a, "z": 1.0 / a - 1.0, "D_unnormalized": D, "f_growth": V / D})


def parity_proxy_A(tau: float) -> float:
    df = SPECTRUM[SPECTRUM.r > 0].copy()
    power = df["multiplicity"].to_numpy(dtype=float) * np.power(df["eta_lazy"].to_numpy(dtype=float), 2.0 * tau)
    odd = power[(df["r"].to_numpy() % 2) == 1].sum()
    even = power[(df["r"].to_numpy() % 2) == 0].sum()
    return float((odd - even) / (odd + even))


def compute_residuals(params_by_model: dict[str, np.ndarray]) -> pd.DataFrame:
    rows = []
    for model, params in params_by_model.items():
        pred = distance_model(DESI_BGS["z"], params, model)
        rows.append(
            {
                "model": model,
                "tracer": "BGS",
                "z": DESI_BGS["z"],
                "observable": "DV_over_rd",
                "observed": DESI_BGS["DV"],
                "sigma": DESI_BGS["sigma_DV"],
                "predicted": pred["DV_over_rd"],
                "pull": (pred["DV_over_rd"] - DESI_BGS["DV"]) / DESI_BGS["sigma_DV"],
            }
        )
        for row in DESI_ANISO.itertuples(index=False):
            pred = distance_model(float(row.z), params, model)
            rows.append(
                {
                    "model": model,
                    "tracer": row.tracer,
                    "z": row.z,
                    "observable": "DM_over_rd",
                    "observed": row.DM_over_rd,
                    "sigma": row.sigma_DM,
                    "predicted": pred["DM_over_rd"],
                    "pull": (pred["DM_over_rd"] - row.DM_over_rd) / row.sigma_DM,
                }
            )
            rows.append(
                {
                    "model": model,
                    "tracer": row.tracer,
                    "z": row.z,
                    "observable": "DH_over_rd",
                    "observed": row.DH_over_rd,
                    "sigma": row.sigma_DH,
                    "predicted": pred["DH_over_rd"],
                    "pull": (pred["DH_over_rd"] - row.DH_over_rd) / row.sigma_DH,
                }
            )
    return pd.DataFrame(rows)


def finite_difference_hessian(func: Callable[[np.ndarray], float], x: np.ndarray, rel_step: float = 2e-4) -> np.ndarray:
    """Symmetric central finite-difference Hessian of chi2 at x."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    H = np.zeros((n, n), dtype=float)
    steps = np.array([max(abs(v) * rel_step, rel_step) for v in x])
    f0 = func(x)
    for i in range(n):
        ei = np.zeros(n); ei[i] = steps[i]
        fpp = func(x + ei)
        fmm = func(x - ei)
        H[i, i] = (fpp - 2 * f0 + fmm) / (steps[i] ** 2)
        for j in range(i + 1, n):
            ej = np.zeros(n); ej[j] = steps[j]
            fpp = func(x + ei + ej)
            fpm = func(x + ei - ej)
            fmp = func(x - ei + ej)
            fmm = func(x - ei - ej)
            H[i, j] = H[j, i] = (fpp - fpm - fmp + fmm) / (4 * steps[i] * steps[j])
    return H


def main() -> None:
    # Fit to BAO-only and to BAO + Planck compressed priors.
    results = []
    params_bao: dict[str, np.ndarray] = {}
    params_planck: dict[str, np.ndarray] = {}
    for model in ("lcdm", "cpl", "ash"):
        x_bao, chi_bao = fit_model(model, chi2_bao_bounded, seed=20260628)
        x_bp, chi_bp = fit_model(model, chi2_bao_planck, seed=20260629)
        params_bao[model] = x_bao
        params_planck[model] = x_bp
        for label, x, chi, ndata in [
            ("DESI_DR2_BAO_only", x_bao, chi_bao, 13),
            ("DESI_DR2_BAO_plus_Planck_H0_Om", x_bp, chi_bp, 15),
        ]:
            k = len(x)
            row = {
                "fit": label,
                "model": model,
                "chi2": chi,
                "ndata": ndata,
                "nparams": k,
                "dof": ndata - k,
                "AIC": chi + 2 * k,
                "BIC": chi + k * math.log(ndata),
                "H0": x[0],
                "Omega_m": x[1],
                "param_2": x[2] if len(x) > 2 else np.nan,
                "param_3": x[3] if len(x) > 3 else np.nan,
                "parameter_labels": "H0,Omega_m" if model == "lcdm" else ("H0,Omega_m,w0,wa" if model == "cpl" else "H0,Omega_m,b1,b2"),
                "bao_chi2_at_fit": chi2_bao_bounded(x, model),
            }
            if model == "cpl":
                row["w0"] = x[2]
                row["wa"] = x[3]
            elif model == "ash":
                row["p1"] = P1
                row["p2"] = P2
                row["w0_eff"] = ash_w_of_a(1.0, x[2], x[3])
                row["wa_eff"] = ash_wa_eff(x[2], x[3])
            results.append(row)

    fit_df = pd.DataFrame(results)
    fit_df.to_csv(OUT / "model_fit_summary.csv", index=False)
    with open(OUT / "model_fit_summary.json", "w", encoding="utf-8") as f:
        json.dump(json.loads(fit_df.to_json(orient="records")), f, indent=2)

    # Residual table for Planck-compressed fits.
    residuals = compute_residuals(params_planck)
    residuals.to_csv(OUT / "bao_residuals_planck_compressed_fits.csv", index=False)

    # Approximate local covariance for the ASH Planck-compressed fit.
    ash_planck = params_planck["ash"]
    cpl_planck = params_planck["cpl"]
    cov_info = {}
    for model, pars in [("ash", ash_planck), ("cpl", cpl_planck), ("lcdm", params_planck["lcdm"])]:
        H = finite_difference_hessian(lambda y, m=model: chi2_bao_planck(y, m), pars)
        try:
            # For chi2, covariance ≈ 2 H^{-1}
            cov = 2.0 * np.linalg.inv(H)
            errs = np.sqrt(np.clip(np.diag(cov), 0, np.inf))
            cov_info[model] = {
                "hessian": H.tolist(),
                "covariance_approx": cov.tolist(),
                "parameter_errors_1sigma_local": errs.tolist(),
            }
        except np.linalg.LinAlgError:
            cov_info[model] = {"hessian": H.tolist(), "covariance_approx": None, "parameter_errors_1sigma_local": None}
    with open(OUT / "local_hessian_covariance_estimates.json", "w", encoding="utf-8") as f:
        json.dump(cov_info, f, indent=2)

    # R012 background outputs: w(a), H deviations relative to matched LCDM.
    zgrid = np.linspace(0.0, 2.5, 501)
    bg_rows = []
    for z in zgrid:
        a = 1.0 / (1.0 + z)
        H0, Om, b1, b2 = ash_planck
        ash_E = E_ash(float(z), H0, Om, b1, b2)
        lcdm_E_matched = E_lcdm(float(z), H0, Om)
        bg_rows.append(
            {
                "z": z,
                "a": a,
                "E_ash": ash_E,
                "E_matched_LCDM": lcdm_E_matched,
                "Delta_H_over_H_matched_LCDM": (ash_E - lcdm_E_matched) / lcdm_E_matched,
                "w_ash": ash_w_of_a(a, b1, b2),
                "rho_DE_factor_ash": rho_de_ash(float(z), b1, b2),
            }
        )
    bg_df = pd.DataFrame(bg_rows)
    bg_df.to_csv(OUT / "r012_ash_background_solution.csv", index=False)

    # R013 growth/S8 calibration.
    planck_lcdm_params = np.array([PRIORS["planck2018_base_lcdm"]["H0"], PRIORS["planck2018_base_lcdm"]["Omega_m"]])
    g_planck = integrate_growth("lcdm", planck_lcdm_params)
    D_planck_today = float(g_planck["D_unnormalized"].iloc[-1])

    def S8_for_alpha(alpha: float) -> float:
        g = integrate_growth("ash", ash_planck, alpha_mu=alpha, npoints=320)
        D_today = float(g["D_unnormalized"].iloc[-1])
        return PRIORS["planck2018_base_lcdm"]["sigma8"] * (D_today / D_planck_today) * math.sqrt(float(ash_planck[1]) / 0.3)

    target_S8 = PRIORS["des_y3_3x2pt_optimized_scale_cuts"]["S8"]
    alpha_cal = float(brentq(lambda a: S8_for_alpha(a) - target_S8, -0.9, 0.4, xtol=1e-7))
    growth_no_mu = integrate_growth("ash", ash_planck, alpha_mu=0.0)
    growth_cal = integrate_growth("ash", ash_planck, alpha_mu=alpha_cal)
    growth_locked_positive = integrate_growth("ash", ash_planck, alpha_mu=0.07)
    # Interpolate selected redshifts for compact output.
    z_eval = np.array([0.0, 0.25, 0.5, 0.8, 1.0, 1.5, 2.0])
    growth_rows = []
    for label, g, alpha in [
        ("Planck_LCDM_reference", g_planck, 0.0),
        ("ASH_background_only", growth_no_mu, 0.0),
        ("ASH_S8_calibrated_alpha_mu", growth_cal, alpha_cal),
        ("ASH_locked_P002_alpha_mu_plus_0p07", growth_locked_positive, 0.07),
    ]:
        # sort ascending z for interpolation
        gs = g.sort_values("z")
        for z in z_eval:
            D = float(np.interp(z, gs["z"].to_numpy(), gs["D_unnormalized"].to_numpy()))
            fgr = float(np.interp(z, gs["z"].to_numpy(), gs["f_growth"].to_numpy()))
            sigma8 = PRIORS["planck2018_base_lcdm"]["sigma8"] * (D / D_planck_today)
            Om_eff = float(ash_planck[1]) if "ASH" in label else PRIORS["planck2018_base_lcdm"]["Omega_m"]
            S8 = sigma8 * math.sqrt(Om_eff / 0.3)
            growth_rows.append(
                {
                    "model": label,
                    "alpha_mu": alpha,
                    "z": z,
                    "D_unnormalized": D,
                    "f_growth": fgr,
                    "sigma8_proxy": sigma8,
                    "S8_proxy": S8,
                    "fsigma8_proxy": fgr * sigma8,
                }
            )
    growth_df = pd.DataFrame(growth_rows)
    growth_df.to_csv(OUT / "growth_predictions.csv", index=False)

    # R015 pilot scoring.
    # Locked values from the current R015 locked prediction ledger.
    locked = {
        "P001": {
            "max_delta_H_over_H": 0.002912478326804413,
            "z_at_max": 1.04,
            "delta_H_over_H_at_z_1": 0.002901964021648995,
            "sign": "nonnegative",
        },
        "P002": {
            "alpha_mu_locked": 0.07,
            "min_ratio": 0.9937461402744073,
            "max_ratio": 1.0077122422747429,
        },
        "P003": {
            "A_2_30_proxy": 0.025911762310551256,
            "sign": "positive",
            "template_min": 0.9806578341931056,
            "template_max": 1.0207152953748184,
        },
    }
    max_idx = int(np.argmax(bg_df["Delta_H_over_H_matched_LCDM"].to_numpy()))
    min_idx = int(np.argmin(bg_df["Delta_H_over_H_matched_LCDM"].to_numpy()))
    delta_z1 = float(bg_df.iloc[(bg_df["z"] - 1.0).abs().argsort().iloc[0]]["Delta_H_over_H_matched_LCDM"])
    s8_no_mu = S8_for_alpha(0.0)
    s8_locked = S8_for_alpha(0.07)
    s8_cal = S8_for_alpha(alpha_cal)
    s8_sigma = PRIORS["des_y3_3x2pt_optimized_scale_cuts"]["sigma_S8"]
    tau_for_A_lock = float(brentq(lambda t: parity_proxy_A(t) - locked["P003"]["A_2_30_proxy"], 0.0, 5.0))
    pilot_scores = [
        {
            "prediction_id": "ASH-R015-P001",
            "observable": "Delta_H_over_H relative to matched LCDM",
            "locked_claim": locked["P001"],
            "pilot_external_data_used": "DESI DR2 BAO Table IV + Planck H0/Omega_m compressed priors",
            "pilot_fit_value": {
                "max_delta_H_over_H": float(bg_df.iloc[max_idx]["Delta_H_over_H_matched_LCDM"]),
                "z_at_max": float(bg_df.iloc[max_idx]["z"]),
                "delta_H_over_H_at_z_1": delta_z1,
                "min_delta_H_over_H": float(bg_df.iloc[min_idx]["Delta_H_over_H_matched_LCDM"]),
                "z_at_min": float(bg_df.iloc[min_idx]["z"]),
            },
            "assessment": "not_confirmed_by_pilot_fit",
            "reason": "The DESI+Planck calibrated ASH finite-spectral background requires percent-level residuals and develops a small high-z sign crossing, unlike the locked 0.29% nonnegative envelope. This is not a formal preregistered falsification of P001, but it is a substantive failed pilot match.",
        },
        {
            "prediction_id": "ASH-R015-P002",
            "observable": "matter-sector amplitude / S8 compression proxy",
            "locked_claim": locked["P002"],
            "pilot_external_data_used": "DES Y3 3x2pt optimized-scale-cuts S8 compression",
            "pilot_fit_value": {
                "alpha_mu_required_for_DESY3_S8": alpha_cal,
                "S8_background_only": s8_no_mu,
                "S8_locked_alpha_mu_plus_0p07": s8_locked,
                "S8_calibrated": s8_cal,
                "DESY3_S8": target_S8,
                "locked_alpha_pull_sigma_vs_DESY3": (s8_locked - target_S8) / s8_sigma,
            },
            "assessment": "tension_in_sign_and_magnitude_under_S8_proxy",
            "reason": "The locked positive alpha_mu=0.07 increases the S8 proxy; the DES Y3 compression requires alpha_mu≈-0.174 in this finite-spectral growth equation. A full P(k) covariance likelihood is still required for formal falsification.",
        },
        {
            "prediction_id": "ASH-R015-P003",
            "observable": "low-ell finite parity proxy sign",
            "locked_claim": locked["P003"],
            "pilot_external_data_used": "published CMB low-ell parity sign literature; no map-level likelihood ingested",
            "pilot_fit_value": {
                "finite_spectrum_sign": "positive_odd_over_even",
                "tau_matching_locked_A_2_30_proxy": tau_for_A_lock,
                "A_at_tau": parity_proxy_A(tau_for_A_lock),
                "A_at_tau_1": parity_proxy_A(1.0),
            },
            "assessment": "sign_consistent_only",
            "reason": "The exact finite ASH spectrum gives a positive odd-over-even proxy for all tested relaxation times; published CMB anomaly literature reports odd-over-even preference in temperature. This is only a sign check and not an empirical likelihood.",
        },
    ]
    with open(OUT / "locked_prediction_pilot_scores.json", "w", encoding="utf-8") as f:
        json.dump(pilot_scores, f, indent=2)
    pd.DataFrame(pilot_scores).to_csv(OUT / "locked_prediction_pilot_scores.csv", index=False)

    # R016 closure certificate, machine-readable.
    closure = {
        "model_tuple": {
            "finite_state_space": "X={x in F2^9: x9=x1 xor ... xor x8}, |X|=256",
            "move_set_in_payload_coordinates": "all 8 one-bit and all 28 two-bit flips induced by 9D pair flips",
            "kernel": "K_l = l I + (1-l)/36 sum_{s in S} T_s with l=1/2",
            "spectrum": "Walsh eigenvalue eta_r = 1/2 + 1/2*(r^2-9r+18)/18, multiplicity C(8,r)",
            "background_map": "rho_DE/rho_DE0=exp[b1(a^p1-1)+b2(a^p2-1)], p1=1, p2=kappa2/kappa1",
            "growth_map": "D''+[2+dlnH/dlna]D'-(3/2)Omega_m(a)(1+alpha_mu a^p1)D=0",
            "likelihood": "Gaussian DESI DR2 BAO Table IV with 2x2 DM/DH covariance blocks plus optional compressed Planck priors",
        },
        "closure_status": {
            "R012_background_equation": "closed for finite-spectral FRW extension in this package",
            "R013_growth_observable": "closed for sub-horizon scalar growth and S8 proxy in this package",
            "R014_real_data_likelihood": "closed for compact DESI DR2 BAO covariance pilot and compressed priors",
            "R015_locked_prediction_execution": "pilot-scored for P001-P003; P001/P002 not confirmed, P003 sign only",
            "R016_formal_closure": "closed as deterministic finite-kernel-to-observable map with explicit limitations",
        },
        "not_closed": [
            "full photon-baryon Boltzmann hierarchy",
            "map-level CMB likelihood",
            "full Pantheon+/DES-SN covariance likelihood",
            "full galaxy P(k) or weak-lensing shear covariance likelihood",
            "peer-reviewed physical ontology of ASH as spacetime",
        ],
        "best_fit_ash_desi_planck": {
            "H0": float(ash_planck[0]),
            "Omega_m": float(ash_planck[1]),
            "b1": float(ash_planck[2]),
            "b2": float(ash_planck[3]),
            "p1": P1,
            "p2": P2,
            "w0_eff": ash_w_of_a(1.0, ash_planck[2], ash_planck[3]),
            "wa_eff": ash_wa_eff(ash_planck[2], ash_planck[3]),
            "chi2": float(fit_df[(fit_df.fit == "DESI_DR2_BAO_plus_Planck_H0_Om") & (fit_df.model == "ash")]["chi2"].iloc[0]),
        },
    }
    with open(OUT / "r016_formal_closure_certificate.json", "w", encoding="utf-8") as f:
        json.dump(closure, f, indent=2)

    # Formal LaTeX expressions.
    formal = {
        "pair_flip_eigenvalue": r"\eta_r = \ell + (1-\ell)\frac{r^2-9r+18}{18},\quad r=0,\ldots,8,\quad m_r=\binom{8}{r}",
        "ash_dark_energy_density": rf"\rho_X(a)/\rho_{{X0}}=\exp\left[b_1(a^{{{P1:.8g}}}-1)+b_2(a^{{{P2:.8g}}}-1)\right]",
        "ash_equation_of_state": rf"w_X(a)=-1-\frac{{1}}{{3}}\left[{P1:.8g}b_1a^{{{P1:.8g}}}+{P2:.8g}b_2a^{{{P2:.8g}}}\right]",
        "friedmann": r"E^2(a)=\Omega_m a^{-3}+(1-\Omega_m)\rho_X(a)/\rho_{X0}",
        "growth_equation": rf"\frac{{d^2D}}{{d(\ln a)^2}}+\left[2+\frac{{d\ln H}}{{d\ln a}}\right]\frac{{dD}}{{d\ln a}}-\frac{{3}}{{2}}\Omega_m(a)\left(1+\alpha_\mu a^{{{P1:.8g}}}\right)D=0",
        "bao_distances": r"D_H=c/H(z),\quad D_M=cH_0^{-1}\int_0^z dz'/E(z'),\quad D_V=(zD_M^2D_H)^{1/3}",
        "parity_proxy": r"A(\tau)=\frac{\sum_{r\ {\rm odd}} \binom{8}{r}\eta_r^{2\tau}-\sum_{r>0,\ r\ {\rm even}}\binom{8}{r}\eta_r^{2\tau}}{\sum_{r=1}^{8}\binom{8}{r}\eta_r^{2\tau}}",
    }
    with open(ROOT / "formal" / "formal_expressions_latex.json", "w", encoding="utf-8") as f:
        json.dump(formal, f, indent=2)

    # Figures
    plt.figure(figsize=(7.2, 4.8))
    plt.plot(bg_df["z"], 100 * bg_df["Delta_H_over_H_matched_LCDM"], label="ASH finite-spectral fit")
    plt.axhline(100 * locked["P001"]["max_delta_H_over_H"], linestyle="--", label="R015 P001 locked max")
    plt.axhline(0, linewidth=0.8)
    plt.xlabel("redshift z")
    plt.ylabel(r"$\Delta H/H$ vs matched LCDM [%]")
    plt.title("R012: ASH finite-spectral background residual")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "r012_delta_H_over_H.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.8))
    plt.plot(bg_df["z"], bg_df["w_ash"], label="ASH $w_X(z)$")
    plt.axhline(-1, linewidth=0.8, linestyle="--", label="cosmological constant")
    plt.xlabel("redshift z")
    plt.ylabel(r"$w_X$")
    plt.title("R012: derived ASH equation of state")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "r012_equation_of_state.png", dpi=180)
    plt.close()

    # BAO residual pulls, Planck-compressed fits
    res_pivot = residuals.copy()
    plt.figure(figsize=(8.2, 5.2))
    for model in ("lcdm", "cpl", "ash"):
        sub = res_pivot[res_pivot["model"] == model]
        plt.scatter(sub["z"], sub["pull"], label=model.upper(), alpha=0.8)
    plt.axhline(0, linewidth=0.8)
    plt.axhline(2, linewidth=0.5, linestyle="--")
    plt.axhline(-2, linewidth=0.5, linestyle="--")
    plt.xlabel("redshift z")
    plt.ylabel("individual residual pull")
    plt.title("R014: DESI DR2 BAO residual pulls")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "r014_bao_residual_pulls.png", dpi=180)
    plt.close()

    # S8/growth bars
    s8_rows = [
        ("Planck LCDM", PRIORS["planck2018_base_lcdm"]["sigma8"] * math.sqrt(PRIORS["planck2018_base_lcdm"]["Omega_m"] / 0.3)),
        ("ASH bg only", s8_no_mu),
        ("ASH alpha=+0.07", s8_locked),
        ("ASH calibrated", s8_cal),
        ("DES Y3 target", target_S8),
    ]
    plt.figure(figsize=(8.2, 4.8))
    plt.bar([r[0] for r in s8_rows], [r[1] for r in s8_rows])
    plt.ylabel(r"$S_8$ proxy")
    plt.title("R013/R015: growth-amplitude comparison")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIG / "r013_s8_proxy_comparison.png", dpi=180)
    plt.close()

    # Pair-flip spectrum
    plt.figure(figsize=(7.2, 4.8))
    plt.scatter(SPECTRUM["r"], SPECTRUM["eta_lazy"], s=40)
    for _, row in SPECTRUM.iterrows():
        plt.text(row["r"], row["eta_lazy"] + 0.015, str(int(row["multiplicity"])), ha="center", fontsize=8)
    plt.xlabel("Walsh shell weight r")
    plt.ylabel(r"lazy eigenvalue $\eta_r$")
    plt.title("Exact ASH pair-flip spectrum (labels=multiplicity)")
    plt.tight_layout()
    plt.savefig(FIG / "finite_pair_flip_spectrum.png", dpi=180)
    plt.close()

    # Growth curves
    plt.figure(figsize=(7.2, 4.8))
    for label, g in [
        ("Planck LCDM", g_planck),
        ("ASH bg only", growth_no_mu),
        ("ASH S8-calibrated", growth_cal),
        ("ASH alpha=+0.07", growth_locked_positive),
    ]:
        plt.plot(g["a"], g["D_unnormalized"] / g["D_unnormalized"].iloc[-1], label=label)
    plt.xlabel("scale factor a")
    plt.ylabel("normalized growth D(a)/D(1)")
    plt.title("R013: sub-horizon growth solutions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "r013_growth_curves.png", dpi=180)
    plt.close()

    # Summary to text.
    summary = {
        "ash_spectral_exponents": {"p1": P1, "p2": P2, "kappa1": KAPPA_1, "kappa2": KAPPA_2},
        "best_fit_DESI_plus_Planck": json.loads(
            fit_df[(fit_df.fit == "DESI_DR2_BAO_plus_Planck_H0_Om")].to_json(orient="records")
        ),
        "s8_calibration": {
            "alpha_mu_required_for_DESY3_S8": alpha_cal,
            "S8_background_only": s8_no_mu,
            "S8_locked_alpha_mu_plus_0p07": s8_locked,
            "S8_calibrated": s8_cal,
        },
        "locked_prediction_pilot_assessments": pilot_scores,
    }
    with open(OUT / "executive_numeric_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
