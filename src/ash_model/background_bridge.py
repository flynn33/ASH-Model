"""Synthetic ASH background-bridge validation utilities.

This module implements a deterministic, phenomenological bridge template for
synthetic background-observable tests. It is a numerical validation and
statistical diagnostic track only. It is not an empirical cosmology result, a
continuum derivation, or a replacement for standard cosmology.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

C_LIGHT_KM_S = 299_792.458
MODEL_VERSION = "ash_background_bridge_pass_003_remediated"
SCIENTIFIC_BOUNDARY = (
    "Synthetic validation and statistical diagnostics only; "
    "no observational validation claim is made."
)


@dataclass(frozen=True)
class BackgroundParams:
    """Flat background parameters plus a phenomenological branch term."""

    H0: float = 70.0
    Omega_m: float = 0.30
    Omega_r: float = 0.0
    Omega_lambda: float = 0.70
    beta_branch: float = 0.0
    gamma_branch: float = 1.5

    def as_dict(self) -> dict[str, float]:
        return {
            "H0": float(self.H0),
            "Omega_m": float(self.Omega_m),
            "Omega_r": float(self.Omega_r),
            "Omega_lambda": float(self.Omega_lambda),
            "beta_branch": float(self.beta_branch),
            "gamma_branch": float(self.gamma_branch),
        }


def _as_redshift_array(z: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    values = np.asarray(z, dtype=float)
    if np.any(~np.isfinite(values)):
        raise ValueError("redshift values must be finite")
    if np.any(values < 0):
        raise ValueError("redshift values must be nonnegative")
    return values


def _validate_grid_size(n_grid: int) -> int:
    if n_grid < 2:
        raise ValueError("n_grid must be at least 2")
    return int(n_grid)


def branch_entropy_template(
    z: np.ndarray | list[float] | tuple[float, ...],
    gamma_branch: float,
    z_pivot: float = 1.0,
) -> np.ndarray:
    """Return a bounded redshift template q(z; gamma) with q(0) = 0."""

    z_values = _as_redshift_array(z)
    if gamma_branch <= 0 or not math.isfinite(gamma_branch):
        raise ValueError("gamma_branch must be positive and finite")
    if z_pivot <= -1.0 or not math.isfinite(z_pivot):
        raise ValueError("z_pivot must be finite and greater than -1")
    return 1.0 - np.exp(-float(gamma_branch) * z_values / (1.0 + float(z_pivot)))


def e2_lcdm(z: np.ndarray | list[float] | tuple[float, ...], p: BackgroundParams) -> np.ndarray:
    """Return the dimensionless squared expansion baseline E(z)^2."""

    z_values = _as_redshift_array(z)
    e2 = (
        p.Omega_m * (1.0 + z_values) ** 3
        + p.Omega_r * (1.0 + z_values) ** 4
        + p.Omega_lambda
    )
    if np.any(e2 <= 0):
        raise ValueError("LCDM baseline E(z)^2 must be positive")
    return e2


def e2_ash(z: np.ndarray | list[float] | tuple[float, ...], p: BackgroundParams) -> np.ndarray:
    """Return E(z)^2 after adding the synthetic branch template term."""

    base = e2_lcdm(z, p)
    q = branch_entropy_template(np.asarray(z, dtype=float), p.gamma_branch)
    e2 = base + p.beta_branch * q
    if np.any(e2 <= 0):
        raise ValueError("ASH candidate E(z)^2 became nonpositive")
    return e2


def H_ash(z: np.ndarray | list[float] | tuple[float, ...], p: BackgroundParams) -> np.ndarray:
    """Return H(z) in km s^-1 Mpc^-1 for the synthetic bridge."""

    if p.H0 <= 0 or not math.isfinite(p.H0):
        raise ValueError("H0 must be positive and finite")
    return p.H0 * np.sqrt(e2_ash(z, p))


def comoving_distance(
    z: np.ndarray | list[float] | tuple[float, ...],
    p: BackgroundParams,
    n_grid: int = 768,
) -> np.ndarray:
    """Return flat comoving distance in Mpc using trapezoid integration."""

    z_values = _as_redshift_array(z)
    steps = _validate_grid_size(n_grid)
    if p.H0 <= 0 or not math.isfinite(p.H0):
        raise ValueError("H0 must be positive and finite")

    distances = np.empty_like(z_values, dtype=float)
    for index, redshift in np.ndenumerate(z_values):
        if redshift == 0:
            distances[index] = 0.0
            continue
        grid = np.linspace(0.0, float(redshift), steps)
        inv_e = 1.0 / np.sqrt(e2_ash(grid, p))
        distances[index] = (C_LIGHT_KM_S / p.H0) * np.trapezoid(inv_e, grid)
    return distances


def luminosity_distance(
    z: np.ndarray | list[float] | tuple[float, ...],
    p: BackgroundParams,
    n_grid: int = 768,
) -> np.ndarray:
    z_values = _as_redshift_array(z)
    return (1.0 + z_values) * comoving_distance(z_values, p, n_grid=n_grid)


def angular_diameter_distance(
    z: np.ndarray | list[float] | tuple[float, ...],
    p: BackgroundParams,
    n_grid: int = 768,
) -> np.ndarray:
    z_values = _as_redshift_array(z)
    return comoving_distance(z_values, p, n_grid=n_grid) / (1.0 + z_values)


def distance_modulus(
    z: np.ndarray | list[float] | tuple[float, ...],
    p: BackgroundParams,
    n_grid: int = 768,
) -> np.ndarray:
    z_values = _as_redshift_array(z)
    if np.any(z_values <= 0):
        raise ValueError("distance modulus requires positive redshift values")
    dl_mpc = luminosity_distance(z_values, p, n_grid=n_grid)
    return 5.0 * np.log10(dl_mpc) + 25.0


def generate_synthetic_background(seed: int = 33) -> dict[str, Any]:
    """Create deterministic ASH and LCDM synthetic background datasets."""

    rng = np.random.default_rng(seed)
    z_sn = np.linspace(0.02, 1.8, 28)
    z_h = np.linspace(0.05, 2.2, 16)
    truth_ash = BackgroundParams(beta_branch=0.180, gamma_branch=1.55)
    truth_lcdm = BackgroundParams(beta_branch=0.0, gamma_branch=1.55)

    mu_true = distance_modulus(z_sn, truth_ash, n_grid=1024)
    h_true = H_ash(z_h, truth_ash)
    sigma_mu = np.full_like(z_sn, 0.004)
    sigma_h = 0.25 + 0.002 * h_true

    mu_lcdm_true = distance_modulus(z_sn, truth_lcdm, n_grid=1024)
    h_lcdm_true = H_ash(z_h, truth_lcdm)

    return {
        "z_sn": z_sn,
        "mu_obs": mu_true + rng.normal(0.0, sigma_mu),
        "sigma_mu": sigma_mu,
        "z_H": z_h,
        "H_obs": h_true + rng.normal(0.0, sigma_h),
        "sigma_H": sigma_h,
        "mu_lcdm_obs": mu_lcdm_true + rng.normal(0.0, sigma_mu),
        "H_lcdm_obs": h_lcdm_true + rng.normal(0.0, sigma_h),
        "truth_ash": truth_ash.as_dict(),
        "truth_lcdm": truth_lcdm.as_dict(),
    }


def chi2_background(
    data: dict[str, Any],
    p: BackgroundParams,
    lcdm_control: bool = False,
    n_grid: int = 384,
) -> float:
    """Return diagonal chi-square for synthetic distance and H(z) data."""

    mu_key = "mu_lcdm_obs" if lcdm_control else "mu_obs"
    h_key = "H_lcdm_obs" if lcdm_control else "H_obs"
    mu_model = distance_modulus(data["z_sn"], p, n_grid=n_grid)
    h_model = H_ash(data["z_H"], p)
    chi_mu = np.sum(((data[mu_key] - mu_model) / data["sigma_mu"]) ** 2)
    chi_h = np.sum(((data[h_key] - h_model) / data["sigma_H"]) ** 2)
    return float(chi_mu + chi_h)


def grid_fit(
    data: dict[str, Any],
    beta_grid: np.ndarray,
    gamma_grid: np.ndarray,
    lcdm_control: bool = False,
    n_grid: int = 384,
) -> dict[str, Any]:
    """Fit beta and gamma by deterministic grid search."""

    records: list[tuple[float, float, float]] = []
    best_chi2 = math.inf
    best_params: BackgroundParams | None = None
    for beta in beta_grid:
        for gamma in gamma_grid:
            params = BackgroundParams(beta_branch=float(beta), gamma_branch=float(gamma))
            try:
                chi2 = chi2_background(
                    data,
                    params,
                    lcdm_control=lcdm_control,
                    n_grid=n_grid,
                )
            except ValueError:
                continue
            records.append((float(beta), float(gamma), chi2))
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_params = params
    if best_params is None or not records:
        raise RuntimeError("no valid grid point found")
    return {
        "best_params": best_params.as_dict(),
        "best_chi2": float(best_chi2),
        "records": np.asarray(records, dtype=float),
    }


def _weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    ordered_values = values[order]
    ordered_weights = weights[order]
    cdf = np.cumsum(ordered_weights)
    return float(np.interp(quantile, cdf, ordered_values))


def posterior_from_grid(records: np.ndarray) -> dict[str, Any]:
    """Summarize a normalized posterior over a uniform beta/gamma grid."""

    if records.ndim != 2 or records.shape[1] != 3 or records.shape[0] == 0:
        raise ValueError("records must be a nonempty N x 3 array")
    beta = records[:, 0]
    gamma = records[:, 1]
    chi2 = records[:, 2]
    delta = chi2 - float(np.min(chi2))
    log_weights = -0.5 * delta
    log_weights -= float(np.max(log_weights))
    weights = np.exp(log_weights)
    weights /= float(np.sum(weights))

    beta_mean = float(np.sum(weights * beta))
    gamma_mean = float(np.sum(weights * gamma))
    beta_var = float(np.sum(weights * (beta - beta_mean) ** 2))
    gamma_var = float(np.sum(weights * (gamma - gamma_mean) ** 2))
    return {
        "beta_branch_mean": beta_mean,
        "beta_branch_std": math.sqrt(max(beta_var, 0.0)),
        "beta_branch_16_50_84": [
            _weighted_quantile(beta, weights, 0.16),
            _weighted_quantile(beta, weights, 0.50),
            _weighted_quantile(beta, weights, 0.84),
        ],
        "gamma_branch_mean": gamma_mean,
        "gamma_branch_std": math.sqrt(max(gamma_var, 0.0)),
        "gamma_branch_16_50_84": [
            _weighted_quantile(gamma, weights, 0.16),
            _weighted_quantile(gamma, weights, 0.50),
            _weighted_quantile(gamma, weights, 0.84),
        ],
        "effective_sample_size": float(1.0 / np.sum(weights**2)),
    }


def information_criteria(chi2: float, n_observations: int, n_parameters: int) -> dict[str, float]:
    """Return AIC and BIC values for a diagonal Gaussian chi-square fit."""

    if n_observations <= 0:
        raise ValueError("n_observations must be positive")
    if n_parameters < 0:
        raise ValueError("n_parameters must be nonnegative")
    return {
        "chi2": float(chi2),
        "n_observations": float(n_observations),
        "n_parameters": float(n_parameters),
        "aic": float(chi2 + 2 * n_parameters),
        "bic": float(chi2 + n_parameters * math.log(n_observations)),
    }


def grid_log_evidence(records: np.ndarray) -> dict[str, Any]:
    """Return a coarse uniform-grid log-evidence diagnostic."""

    if records.ndim != 2 or records.shape[1] != 3 or records.shape[0] == 0:
        raise ValueError("records must be a nonempty N x 3 array")
    log_likelihood = -0.5 * records[:, 2]
    shift = float(np.max(log_likelihood))
    log_mean_likelihood = shift + math.log(float(np.mean(np.exp(log_likelihood - shift))))
    return {
        "diagnostic_label": "coarse uniform-grid likelihood integral; diagnostic only",
        "log_evidence": float(log_mean_likelihood),
        "grid_point_count": int(records.shape[0]),
    }


def fit_lcdm_nested(
    data: dict[str, Any],
    lcdm_control: bool = False,
    n_grid: int = 384,
) -> dict[str, Any]:
    """Evaluate the nested beta=0 baseline with the same synthetic data."""

    params = BackgroundParams(beta_branch=0.0, gamma_branch=1.0)
    return {
        "params": params.as_dict(),
        "chi2": chi2_background(data, params, lcdm_control=lcdm_control, n_grid=n_grid),
    }


def random_matched_null_fit(
    data: dict[str, Any],
    seed: int = 101,
    n_grid: int = 384,
) -> dict[str, Any]:
    """Fit a deterministic smooth random two-parameter null template."""

    rng = np.random.default_rng(seed)
    coeffs = rng.normal(size=4)
    z_nodes = np.linspace(0.0, 2.3, 256)
    modes = np.vstack(
        [np.sin((index + 1) * np.pi * z_nodes / z_nodes.max()) for index in range(4)]
    )
    raw = coeffs @ modes
    raw -= raw[0]
    raw /= max(float(np.max(np.abs(raw))), 1e-12)

    def q_null(z: np.ndarray, gamma_scale: float) -> np.ndarray:
        z_values = _as_redshift_array(z)
        base = np.interp(z_values, z_nodes, raw)
        return base * (1.0 - np.exp(-gamma_scale * z_values / 2.0))

    def e2_null(z: np.ndarray, beta: float, gamma: float) -> np.ndarray:
        baseline = e2_lcdm(z, BackgroundParams(beta_branch=0.0))
        e2 = baseline + beta * q_null(z, gamma)
        if np.any(e2 <= 0):
            raise ValueError("matched null E(z)^2 became nonpositive")
        return e2

    def h_null(z: np.ndarray, beta: float, gamma: float) -> np.ndarray:
        return BackgroundParams().H0 * np.sqrt(e2_null(z, beta, gamma))

    def mu_null(z: np.ndarray, beta: float, gamma: float) -> np.ndarray:
        z_values = _as_redshift_array(z)
        out = np.empty_like(z_values, dtype=float)
        for index, redshift in np.ndenumerate(z_values):
            grid = np.linspace(0.0, float(redshift), n_grid)
            inv_e = 1.0 / np.sqrt(e2_null(grid, beta, gamma))
            dm = (C_LIGHT_KM_S / BackgroundParams().H0) * np.trapezoid(inv_e, grid)
            out[index] = 5.0 * np.log10((1.0 + redshift) * dm) + 25.0
        return out

    beta_grid = np.linspace(-0.20, 0.30, 21)
    gamma_grid = np.linspace(0.30, 3.00, 19)
    best: tuple[float, float, float] | None = None
    for beta in beta_grid:
        for gamma in gamma_grid:
            try:
                mu_model = mu_null(data["z_sn"], float(beta), float(gamma))
                h_model = h_null(data["z_H"], float(beta), float(gamma))
            except ValueError:
                continue
            chi2 = float(
                np.sum(((data["mu_obs"] - mu_model) / data["sigma_mu"]) ** 2)
                + np.sum(((data["H_obs"] - h_model) / data["sigma_H"]) ** 2)
            )
            if best is None or chi2 < best[0]:
                best = (chi2, float(beta), float(gamma))
    if best is None:
        raise RuntimeError("no valid matched-null grid point found")
    return {
        "chi2": best[0],
        "beta": best[1],
        "gamma_like": best[2],
        "null_coefficients": [float(value) for value in coeffs],
    }


def convergence_diagnostics(
    data: dict[str, Any] | None = None,
    beta_grid: np.ndarray | None = None,
    gamma_grid: np.ndarray | None = None,
) -> dict[str, Any]:
    """Compare 384-point and 768-point distance integration fits."""

    synthetic = generate_synthetic_background() if data is None else data
    betas = np.linspace(-0.05, 0.25, 61) if beta_grid is None else beta_grid
    gammas = np.linspace(0.60, 2.60, 41) if gamma_grid is None else gamma_grid
    fit_384 = grid_fit(synthetic, betas, gammas, n_grid=384)
    fit_768 = grid_fit(synthetic, betas, gammas, n_grid=768)
    beta_difference = abs(
        fit_384["best_params"]["beta_branch"] - fit_768["best_params"]["beta_branch"]
    )
    gamma_difference = abs(
        fit_384["best_params"]["gamma_branch"] - fit_768["best_params"]["gamma_branch"]
    )
    chi2_difference = abs(fit_384["best_chi2"] - fit_768["best_chi2"])
    passes = beta_difference <= 0.01 and gamma_difference <= 0.05 and chi2_difference <= 0.25
    return {
        "n_grid_values": [384, 768],
        "fit_384": {
            "best_params": fit_384["best_params"],
            "best_chi2": fit_384["best_chi2"],
        },
        "fit_768": {
            "best_params": fit_768["best_params"],
            "best_chi2": fit_768["best_chi2"],
        },
        "beta_difference": float(beta_difference),
        "gamma_difference": float(gamma_difference),
        "chi2_difference": float(chi2_difference),
        "passes": bool(passes),
    }


def _write_csv(path: Path, data: np.ndarray, header: str) -> None:
    np.savetxt(path, data, delimiter=",", header=header, comments="", fmt="%.12g")


def run_validation(output_dir: str | Path) -> dict[str, Any]:
    """Run deterministic Pass 003 synthetic validation and write artifacts."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    data = generate_synthetic_background()
    beta_grid = np.linspace(-0.05, 0.25, 61)
    gamma_grid = np.linspace(0.60, 2.60, 41)
    observation_count = int(len(data["z_sn"]) + len(data["z_H"]))

    fit_ash = grid_fit(data, beta_grid, gamma_grid, n_grid=384)
    fit_lcdm_ash = fit_lcdm_nested(data, n_grid=384)
    fit_null = random_matched_null_fit(data, n_grid=384)
    fit_ash_on_lcdm = grid_fit(data, beta_grid, gamma_grid, lcdm_control=True, n_grid=384)
    fit_lcdm_on_lcdm = fit_lcdm_nested(data, lcdm_control=True, n_grid=384)
    posterior = posterior_from_grid(fit_ash["records"])
    convergence = convergence_diagnostics(data, beta_grid, gamma_grid)

    ash_ic = information_criteria(fit_ash["best_chi2"], observation_count, 2)
    lcdm_ic = information_criteria(fit_lcdm_ash["chi2"], observation_count, 0)
    null_ic = information_criteria(fit_null["chi2"], observation_count, 2)
    acceptance_checks = {
        "recovers_beta_within_0p03": abs(
            fit_ash["best_params"]["beta_branch"] - data["truth_ash"]["beta_branch"]
        )
        <= 0.03,
        "recovers_gamma_within_0p30": abs(
            fit_ash["best_params"]["gamma_branch"] - data["truth_ash"]["gamma_branch"]
        )
        <= 0.30,
        "beats_nested_lcdm_on_ash_synthetic": fit_ash["best_chi2"] < fit_lcdm_ash["chi2"],
        "beats_random_matched_null_on_ash_synthetic": fit_ash["best_chi2"] < fit_null["chi2"],
        "does_not_force_beta_on_lcdm_synthetic": abs(
            fit_ash_on_lcdm["best_params"]["beta_branch"]
        )
        <= 0.04,
        "posterior_std_positive": posterior["beta_branch_std"] > 0.0
        and posterior["gamma_branch_std"] > 0.0,
        "convergence_384_to_768": convergence["passes"],
    }

    summary: dict[str, Any] = {
        "model_version": MODEL_VERSION,
        "scientific_boundary": SCIENTIFIC_BOUNDARY,
        "validation_scope": "synthetic background-observable recovery and numerical diagnostics",
        "remediates_audit_findings": {
            "uses_np_trapezoid": True,
            "has_matched_lcdm_control": True,
            "has_matched_random_null_control": True,
            "reports_posterior_uncertainty_grid": True,
            "reports_information_criteria": True,
            "reports_convergence_diagnostics": True,
        },
        "truth_ash": data["truth_ash"],
        "truth_lcdm": data["truth_lcdm"],
        "ash_fit_on_ash_synthetic": fit_ash["best_params"],
        "ash_chi2_on_ash_synthetic": fit_ash["best_chi2"],
        "lcdm_chi2_on_ash_synthetic": fit_lcdm_ash["chi2"],
        "matched_random_null_on_ash_synthetic": fit_null,
        "ash_fit_on_lcdm_synthetic": fit_ash_on_lcdm["best_params"],
        "ash_chi2_on_lcdm_synthetic": fit_ash_on_lcdm["best_chi2"],
        "lcdm_chi2_on_lcdm_synthetic": fit_lcdm_on_lcdm["chi2"],
        "posterior_uncertainty_grid": posterior,
        "information_criteria": {
            "ash_grid": ash_ic,
            "nested_lcdm": lcdm_ic,
            "matched_random_null": null_ic,
            "delta_aic_lcdm_minus_ash": float(lcdm_ic["aic"] - ash_ic["aic"]),
            "delta_bic_lcdm_minus_ash": float(lcdm_ic["bic"] - ash_ic["bic"]),
            "delta_aic_null_minus_ash": float(null_ic["aic"] - ash_ic["aic"]),
            "delta_bic_null_minus_ash": float(null_ic["bic"] - ash_ic["bic"]),
        },
        "evidence_diagnostics": {
            "ash_grid_on_ash_synthetic": grid_log_evidence(fit_ash["records"]),
            "ash_grid_on_lcdm_synthetic": grid_log_evidence(fit_ash_on_lcdm["records"]),
        },
        "convergence_diagnostics": convergence,
        "acceptance_checks": acceptance_checks,
    }

    (output_path / "validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_csv(
        output_path / "synthetic_supernova_ash.csv",
        np.column_stack([data["z_sn"], data["mu_obs"], data["sigma_mu"]]),
        "z,mu_obs,sigma_mu",
    )
    _write_csv(
        output_path / "synthetic_H_ash.csv",
        np.column_stack([data["z_H"], data["H_obs"], data["sigma_H"]]),
        "z,H_obs,sigma_H",
    )
    _write_csv(
        output_path / "ash_grid_fit_records.csv",
        fit_ash["records"],
        "beta_branch,gamma_branch,chi2",
    )
    z_curve = np.linspace(0.0, 2.2, 160)
    best_params = BackgroundParams(
        beta_branch=fit_ash["best_params"]["beta_branch"],
        gamma_branch=fit_ash["best_params"]["gamma_branch"],
    )
    lcdm_params = BackgroundParams(beta_branch=0.0)
    _write_csv(
        output_path / "background_curves.csv",
        np.column_stack(
            [
                z_curve,
                H_ash(z_curve, best_params),
                H_ash(z_curve, lcdm_params),
                branch_entropy_template(z_curve, best_params.gamma_branch),
            ]
        ),
        "z,H_ash_best,H_lcdm,branch_template",
    )
    return summary


def main() -> int:
    output_dir = Path("validation/background_bridge/pass_003/outputs")
    summary = run_validation(output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
