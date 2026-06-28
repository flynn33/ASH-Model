"""R-012 ASH cosmological background equations finite workbench.

Repository integration candidate. Assumes R-008/R-009/R-010/R-011 acceptance:
- finite normalized branch measure,
- observer memory/decoherence summaries,
- unit-bearing bridge contract,
- finite-observer causal/projective levels.

This module defines a unit-bearing homogeneous/isotropic background bridge and
an exact standard-baseline relation to flat/curved LCDM when the ASH source
amplitude is zero.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Iterable, Tuple
import math
import csv
import json
from pathlib import Path

MPC_KM = 3.0856775814913673e19  # kilometers in one megaparsec
SEC_PER_GYR = 3.15576e16
C_KM_S = 299792.458

@dataclass(frozen=True)
class BackgroundParameters:
    H0_km_s_Mpc: float = 70.0
    Omega_r: float = 9.0e-5
    Omega_m: float = 0.315
    Omega_k: float = 0.0
    Omega_Lambda: float = 0.68491
    Omega_ash: float = 0.0
    ash_alpha_entropy: float = 0.45
    ash_beta_defect: float = 0.35
    ash_gamma_memory: float = 0.20
    ash_lambda_decay: float = 2.0
    a_star: float = 0.5
    source_floor: float = 1.0e-12

    def H0_s_inv(self) -> float:
        return self.H0_km_s_Mpc / MPC_KM

    def H0_Gyr_inv(self) -> float:
        return self.H0_s_inv() * SEC_PER_GYR

    def closure_sum_today(self) -> float:
        return self.Omega_r + self.Omega_m + self.Omega_k + self.Omega_Lambda + self.Omega_ash

def finite_branch_features(a: float, n: int = 9) -> Dict[str, float]:
    """Synthetic but finite-derived homogeneous features normalized to unity today.

    The n=9 layer is the canonical ASH admissible parity layer with 256 states.
    Features are smooth summaries of finite shell/branch quantities:
    - entropy channel saturates toward late time,
    - defect channel dilutes with branch depth/expansion,
    - memory channel grows monotonically with committed depth.
    """
    if a <= 0:
        raise ValueError("scale factor a must be positive")
    admissible = 2 ** (n - 1)
    max_shell = (n - 1) // 2
    # normalized finite combinatorial constants
    parity_density = admissible / (2 ** n)
    shell_width = max_shell / n
    x = a / (a + 1.0)
    entropy_channel = math.log1p(admissible * x) / math.log1p(admissible * 0.5)
    defect_channel = ((1.0 + 1.0) / (1.0 + a)) ** 1.5
    memory_channel = math.log1p(n * a) / math.log1p(n)
    # normalize all to exactly 1 at a=1
    return {
        "parity_density": parity_density,
        "shell_width": shell_width,
        "entropy_channel": entropy_channel,
        "defect_channel": defect_channel,
        "memory_channel": memory_channel,
    }

def ash_source_E(a: float, p: BackgroundParameters, n: int = 9) -> float:
    f = finite_branch_features(a, n=n)
    raw = (
        p.ash_alpha_entropy * f["entropy_channel"]
        + p.ash_beta_defect * f["defect_channel"]
        + p.ash_gamma_memory * f["memory_channel"]
    )
    today = (
        p.ash_alpha_entropy * 1.0
        + p.ash_beta_defect * 1.0
        + p.ash_gamma_memory * 1.0
    )
    return max(p.source_floor, raw / today)

def lcdm_E2(a: float, p: BackgroundParameters) -> float:
    if a <= 0:
        raise ValueError("scale factor a must be positive")
    return p.Omega_r/a**4 + p.Omega_m/a**3 + p.Omega_k/a**2 + p.Omega_Lambda

def ash_E2(a: float, p: BackgroundParameters, n: int = 9) -> float:
    return lcdm_E2(a, p) + p.Omega_ash * ash_source_E(a, p, n=n)

def H_km_s_Mpc(a: float, p: BackgroundParameters, n: int = 9) -> float:
    e2 = ash_E2(a, p, n=n)
    if e2 < 0:
        raise ValueError("negative H^2")
    return p.H0_km_s_Mpc * math.sqrt(e2)

def w_ash(a: float, p: BackgroundParameters, n: int = 9, eps: float = 1e-4) -> float:
    """Effective equation of state from continuity:
    w = -1 - (1/3) d ln E_ash / d ln a.
    """
    ap = a * math.exp(eps)
    am = a * math.exp(-eps)
    dln = (math.log(ash_source_E(ap, p, n=n)) - math.log(ash_source_E(am, p, n=n))) / (2 * eps)
    return -1.0 - dln / 3.0

def q_deceleration(a: float, p: BackgroundParameters, n: int = 9, eps: float = 1e-4) -> float:
    """q(a) = -1 - d ln H / d ln a."""
    ap = a * math.exp(eps)
    am = a * math.exp(-eps)
    dlnH = (math.log(H_km_s_Mpc(ap, p, n=n)) - math.log(H_km_s_Mpc(am, p, n=n))) / (2 * eps)
    return -1.0 - dlnH

def integrate_background(p: BackgroundParameters, a_min: float = 1e-3, a_max: float = 1.0, steps: int = 400, n: int = 9):
    """Integrate cosmic age and comoving distance on a log-spaced grid.

    Returns rows with a, z, E2, H, t_Gyr_since_a_min, chi_Mpc.
    """
    if steps < 3:
        raise ValueError("steps must be >= 3")
    log_min, log_max = math.log(a_min), math.log(a_max)
    grid = [math.exp(log_min + i*(log_max-log_min)/(steps-1)) for i in range(steps)]
    rows = []
    t_acc = 0.0
    chi_acc = 0.0
    prev_a = None
    prev_ft = None
    prev_fc = None
    H0_Gyr = p.H0_Gyr_inv()
    for a in grid:
        E = math.sqrt(ash_E2(a, p, n=n))
        ft = 1.0/(a * H0_Gyr * E)  # Gyr per da
        fc = C_KM_S/(a*a*p.H0_km_s_Mpc*E)  # Mpc per da
        if prev_a is not None:
            da = a - prev_a
            t_acc += 0.5 * da * (prev_ft + ft)
            chi_acc += 0.5 * da * (prev_fc + fc)
        rows.append({
            "a": a,
            "z": 1.0/a - 1.0,
            "E2": ash_E2(a, p, n=n),
            "H_km_s_Mpc": H_km_s_Mpc(a, p, n=n),
            "ash_source_E": ash_source_E(a, p, n=n),
            "w_ash": w_ash(a, p, n=n),
            "q": q_deceleration(a, p, n=n),
            "t_Gyr_since_a_min": t_acc,
            "chi_Mpc_from_a_min": chi_acc,
        })
        prev_a, prev_ft, prev_fc = a, ft, fc
    return rows

def synthetic_observations(p_truth: BackgroundParameters, a_values, sigma_frac: float = 0.01, seed: int = 12012):
    """Deterministic synthetic H(a) observations for recovery tests."""
    rng = __import__("random").Random(seed)
    rows = []
    for a in a_values:
        true_H = H_km_s_Mpc(a, p_truth)
        sigma = sigma_frac * true_H
        noisy = true_H + rng.gauss(0.0, sigma)
        rows.append({"a": a, "z": 1/a-1, "H_obs": noisy, "sigma_H": sigma, "H_truth": true_H})
    return rows

def grid_fit_omega_ash(obs_rows, template: BackgroundParameters, omega_grid):
    """One-parameter finite grid fit for Omega_ash with fixed other parameters."""
    best = None
    table = []
    for om in omega_grid:
        p = BackgroundParameters(**{**asdict(template), "Omega_ash": float(om)})
        chi2 = 0.0
        for r in obs_rows:
            pred = H_km_s_Mpc(r["a"], p)
            chi2 += ((r["H_obs"] - pred)/r["sigma_H"])**2
        row = {"Omega_ash": float(om), "chi2": chi2}
        table.append(row)
        if best is None or chi2 < best["chi2"]:
            best = row
    return best, table

def write_csv(path: str | Path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError("no rows")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def covariance_matrix(rows, cols):
    data = [[float(r[c]) for c in cols] for r in rows]
    n = len(data)
    means = [sum(row[j] for row in data)/n for j in range(len(cols))]
    cov = []
    for i in range(len(cols)):
        cov_row = []
        for j in range(len(cols)):
            cov_row.append(sum((row[i]-means[i])*(row[j]-means[j]) for row in data)/(n-1))
        cov.append(cov_row)
    return cov


# Repository-facing aliases with clearer R-012 notation.
finite_background_features = finite_branch_features
ash_source_xi = ash_source_E
effective_w_ash = w_ash
deceleration_q = q_deceleration
synthetic_H_observations = synthetic_observations
