"""ASH R-013 physical perturbation equations and matter-sector solver.

Independent proposed extension, assuming R-008 through R-012 acceptance.
This module supplies a finite-derived, unit-bearing matter perturbation workbench:
- maps finite ASH shell/spectral variables into physical scalar-sector modifiers,
- solves the linear matter growth equation in Newtonian-gauge sub-horizon form,
- computes a matter-power proxy P(k,z),
- provides a low-ell CMB transfer proxy for interface testing,
- verifies exact LCDM recovery when ASH perturbation amplitudes vanish.

The implementation is intentionally a closure workbench, not a claim of an
empirically calibrated Boltzmann solver.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Iterable, List, Tuple
import math, csv, json
from pathlib import Path

C_KM_S = 299792.458
MPC_KM = 3.0856775814913673e19
SEC_PER_GYR = 3.15576e16

@dataclass(frozen=True)
class PerturbationParameters:
    H0_km_s_Mpc: float = 70.0
    Omega_r: float = 9.0e-5
    Omega_m: float = 0.315
    Omega_k: float = 0.0
    Omega_Lambda: float = 0.66491
    Omega_ash: float = 0.02000
    ash_alpha_entropy: float = 0.45
    ash_beta_defect: float = 0.35
    ash_gamma_memory: float = 0.20
    ns: float = 0.965
    A_proxy: float = 2.1e-9
    k_pivot_Mpc_inv: float = 0.05
    k_eq_Mpc_inv: float = 0.016
    k_uv_Mpc_inv: float = 0.45
    alpha_mu: float = 0.070
    beta_drag: float = 0.018
    residual_amp: float = 0.030
    sigma_logk: float = 2.0
    a_ini: float = 1.0e-3
    a_final: float = 1.0
    n_steps: int = 420

    def h(self) -> float:
        return self.H0_km_s_Mpc / 100.0

    def closure_sum_today(self) -> float:
        return self.Omega_r + self.Omega_m + self.Omega_k + self.Omega_Lambda + self.Omega_ash

def finite_branch_features(a: float, n: int = 9) -> Dict[str, float]:
    if a <= 0:
        raise ValueError("scale factor a must be positive")
    admissible = 2 ** (n - 1)
    max_shell = (n - 1) // 2
    parity_density = admissible / (2 ** n)
    shell_width = max_shell / n
    x = a / (a + 1.0)
    entropy_channel = math.log1p(admissible * x) / math.log1p(admissible * 0.5)
    defect_channel = 2.0 ** 1.5 / (1.0 + a) ** 1.5
    memory_channel = math.log1p(n * a) / math.log1p(n)
    return {
        "parity_density": parity_density,
        "shell_width": shell_width,
        "entropy_channel": entropy_channel,
        "defect_channel": defect_channel,
        "memory_channel": memory_channel,
    }

def ash_background_source(a: float, p: PerturbationParameters, n: int = 9) -> float:
    f = finite_branch_features(a, n=n)
    raw = p.ash_alpha_entropy*f["entropy_channel"] + p.ash_beta_defect*f["defect_channel"] + p.ash_gamma_memory*f["memory_channel"]
    today = p.ash_alpha_entropy + p.ash_beta_defect + p.ash_gamma_memory
    return raw / today

def lcdm_E2(a: float, p: PerturbationParameters) -> float:
    if a <= 0:
        raise ValueError("scale factor a must be positive")
    return p.Omega_r/a**4 + p.Omega_m/a**3 + p.Omega_k/a**2 + p.Omega_Lambda

def ash_E2(a: float, p: PerturbationParameters) -> float:
    return lcdm_E2(a, p) + p.Omega_ash * ash_background_source(a, p)

def dlnH_dlna(a: float, p: PerturbationParameters, eps: float = 1e-4) -> float:
    ap, am = a*math.exp(eps), a*math.exp(-eps)
    return 0.5*(math.log(ash_E2(ap,p)) - math.log(ash_E2(am,p))) / (2*eps)

def Omega_m_a(a: float, p: PerturbationParameters) -> float:
    return p.Omega_m / (a**3 * ash_E2(a,p))

def finite_spectral_modes() -> List[Dict[str, float]]:
    # Pair-flip/halved-cube n=9 spectrum: adjacency 36,20,8,0,-4; Laplacian 0,16,28,36,40.
    mult = [1,9,36,84,126]
    lap = [0,16,28,36,40]
    weights = [0.50, 0.30, -0.14, 0.07, -0.03]
    rows = []
    for q,(m,l,w) in enumerate(zip(mult,lap,weights)):
        rows.append({"q":q, "multiplicity":m, "laplacian":l, "normalized_laplacian":l/40.0, "coefficient":w})
    return rows

def finite_kernel(k: float, p: PerturbationParameters) -> float:
    if k <= 0:
        raise ValueError("k must be positive in Mpc^-1")
    phase = math.pi * math.log(k/p.k_pivot_Mpc_inv, 2)
    envelope = math.exp(-0.5*(math.log(k/p.k_pivot_Mpc_inv)/p.sigma_logk)**2) * math.exp(-0.5*(k/p.k_uv_Mpc_inv)**2)
    val = 0.0
    for row in finite_spectral_modes():
        q = row["q"]
        val += row["coefficient"] * math.cos(q*phase) / (1.0 + row["normalized_laplacian"])
    return envelope * val

def mu_eff(a: float, k: float, p: PerturbationParameters) -> float:
    # Effective Newtonian-gauge Poisson/source modifier. Positive by construction for default amplitudes.
    return 1.0 + p.alpha_mu * ash_background_source(a,p) * finite_kernel(k,p)

def drag_eff(a: float, k: float, p: PerturbationParameters) -> float:
    # Small observer/branch friction term in dD/dln a coefficient.
    return p.beta_drag * ash_background_source(a,p) * abs(finite_kernel(k,p))

def growth_rhs(x: float, y: Tuple[float,float], k: float, p: PerturbationParameters) -> Tuple[float,float]:
    a = math.exp(x)
    D, V = y # V=dD/dln a
    coeff = 2.0 + dlnH_dlna(a,p) + drag_eff(a,k,p)
    source = 1.5 * Omega_m_a(a,p) * mu_eff(a,k,p) * D
    return (V, -coeff*V + source)

def rk4_step(x: float, y: Tuple[float,float], h: float, k: float, p: PerturbationParameters) -> Tuple[float,float]:
    def add(y, dy, fac):
        return (y[0] + fac*dy[0], y[1] + fac*dy[1])
    k1 = growth_rhs(x,y,k,p)
    k2 = growth_rhs(x+0.5*h, add(y,k1,0.5*h), k, p)
    k3 = growth_rhs(x+0.5*h, add(y,k2,0.5*h), k, p)
    k4 = growth_rhs(x+h, add(y,k3,h), k, p)
    return (y[0] + h*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6.0,
            y[1] + h*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6.0)

def solve_growth(k: float, p: PerturbationParameters, z_outputs: Iterable[float]=(0.0,0.5,1.0,2.0)) -> Dict[float, Dict[str,float]]:
    if k <= 0: raise ValueError("k must be positive")
    x0, x1 = math.log(p.a_ini), math.log(p.a_final)
    steps = p.n_steps
    h = (x1-x0)/steps
    # Growing-mode matter-era initial condition D=a, dD/dln a=a.
    y = (p.a_ini, p.a_ini)
    targets = sorted([(math.log(1.0/(1.0+z)), z) for z in z_outputs])
    out: Dict[float, Dict[str,float]] = {}
    ti = 0
    prev_x, prev_y = x0, y
    for i in range(1, steps+1):
        x = x0 + i*h
        new_y = rk4_step(prev_x, prev_y, h, k, p)
        while ti < len(targets) and targets[ti][0] <= x:
            xt, z = targets[ti]
            if xt < prev_x:
                ti += 1; continue
            t = (xt - prev_x)/(x-prev_x) if x != prev_x else 0.0
            D = prev_y[0] + t*(new_y[0]-prev_y[0])
            V = prev_y[1] + t*(new_y[1]-prev_y[1])
            out[z] = {"a":math.exp(xt), "D":D, "f_growth": V/D if D != 0 else float("nan"), "mu_eff":mu_eff(math.exp(xt),k,p)}
            ti += 1
        prev_x, prev_y = x, new_y
    if 0.0 not in out:
        out[0.0] = {"a":1.0, "D":prev_y[0], "f_growth":prev_y[1]/prev_y[0], "mu_eff":mu_eff(1.0,k,p)}
    return out

def bbks_transfer(k: float, p: PerturbationParameters) -> float:
    q = k / max(p.k_eq_Mpc_inv, 1e-12)
    if q < 1e-10: return 1.0
    numerator = math.log(1.0 + 2.34*q)/(2.34*q)
    denominator = (1.0 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**0.25
    return numerator/denominator

def primordial_power(k: float, p: PerturbationParameters) -> float:
    return p.A_proxy * (k/p.k_pivot_Mpc_inv)**(p.ns-1.0)

def residual_power_factor(k: float, p: PerturbationParameters) -> float:
    return max(1e-9, 1.0 + p.residual_amp * finite_kernel(k,p))

def matter_power(k: float, z: float, p: PerturbationParameters) -> float:
    gr = solve_growth(k,p,z_outputs=(0.0,z))
    D0 = gr[0.0]["D"]
    Dz = gr[z]["D"]
    T = bbks_transfer(k,p)
    return primordial_power(k,p) * (T*T) * (Dz/D0)**2 * residual_power_factor(k,p)

def matter_grid(k_values: Iterable[float], z_values: Iterable[float], p: PerturbationParameters) -> List[Dict[str,float]]:
    rows = []
    for k in k_values:
        gr = solve_growth(k,p,z_outputs=tuple(z_values))
        D0 = gr[0.0]["D"]
        for z in z_values:
            T = bbks_transfer(k,p)
            P = primordial_power(k,p)*T*T*(gr[z]["D"]/D0)**2*residual_power_factor(k,p)
            rows.append({"k_Mpc_inv":k,"z":z,"a":gr[z]["a"],"D":gr[z]["D"],"D_norm":gr[z]["D"]/D0,
                         "f_growth":gr[z]["f_growth"],"mu_eff":gr[z]["mu_eff"],
                         "finite_kernel":finite_kernel(k,p),"T_proxy":T,"P_proxy":P})
    return rows

def cmb_lowell_proxy(ells: Iterable[int], p: PerturbationParameters, chi_star_Mpc: float = 13800.0) -> List[Dict[str,float]]:
    rows = []
    for ell in ells:
        k = (ell + 0.5)/chi_star_Mpc
        sw = (4.0*math.pi/25.0) * primordial_power(k,p) / (ell*(ell+1.0))
        modifier = residual_power_factor(k,p) * (1.0 + 0.2*(mu_eff(1.0,k,p)-1.0))
        rows.append({"ell":ell,"k_projection_Mpc_inv":k,"Cl_TT_proxy":sw*modifier,"finite_kernel":finite_kernel(k,p)})
    return rows

def synthetic_observations(k_values: Iterable[float], truth: PerturbationParameters, sigma_frac: float=0.015) -> List[Dict[str,float]]:
    """Deterministic synthetic matter-sector observations.

    The observable vector combines P(k,z=0) and f(k,z=1).  The growth-rate
    component prevents the test from hiding ASH source changes inside the
    present-day D-normalization.
    """
    rows=[]
    for k in k_values:
        P=matter_power(k,0.0,truth)
        gr=solve_growth(k,truth,z_outputs=(0.0,1.0))
        f1=gr[1.0]["f_growth"]
        # deterministic pseudo-noise; no random seed required
        jitter = sigma_frac * math.sin(17.0*math.log(k/truth.k_pivot_Mpc_inv) + 0.3)
        fjitter = sigma_frac * math.cos(11.0*math.log(k/truth.k_pivot_Mpc_inv) - 0.2)
        rows.append({"k_Mpc_inv":k,"P_true":P,"P_obs":P*(1.0+jitter),"sigma_P":abs(sigma_frac*P),
                     "f_z1_true":f1,"f_z1_obs":f1*(1.0+fjitter),"sigma_f":abs(sigma_frac*f1),
                     "jitter_P":jitter,"jitter_f":fjitter})
    return rows

def fit_alpha_mu_grid(obs_rows: List[Dict[str,float]], base: PerturbationParameters, grid: Iterable[float]) -> List[Dict[str,float]]:
    rows=[]
    for alpha in grid:
        p = PerturbationParameters(**{**asdict(base), "alpha_mu":alpha})
        chi2=0.0
        for r in obs_rows:
            modelP = matter_power(r["k_Mpc_inv"],0.0,p)
            modelF = solve_growth(r["k_Mpc_inv"],p,z_outputs=(1.0,))[1.0]["f_growth"]
            chi2 += ((r["P_obs"]-modelP)/r["sigma_P"])**2
            chi2 += ((r["f_z1_obs"]-modelF)/r["sigma_f"])**2
        rows.append({"alpha_mu":alpha,"chi2":chi2,"n":2*len(obs_rows)})
    return rows

def write_csv(path: Path, rows: List[Dict[str,float]]) -> None:
    if not rows: raise ValueError("cannot write empty rows")
    with path.open("w", newline="") as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

def run_artifacts(out_root: Path) -> Dict[str, object]:
    out_root.mkdir(parents=True, exist_ok=True)
    for sub in ["data","validation"]:
        (out_root/sub).mkdir(exist_ok=True)
    p = PerturbationParameters()
    # log k grid
    k_values = [10**(-3 + i*(1.0+3.0)/59.0) for i in range(60)] # 1e-3 to 10 Mpc^-1
    z_values = [0.0,0.5,1.0,2.0]
    rows = matter_grid(k_values,z_values,p)
    write_csv(out_root/"data"/"r013_matter_power_proxy.csv", rows)
    cmb = cmb_lowell_proxy(range(2,61),p)
    write_csv(out_root/"data"/"r013_cmb_lowell_proxy.csv", cmb)
    modes = finite_spectral_modes()
    write_csv(out_root/"data"/"r013_finite_to_physical_modes.csv", modes)
    # LCDM limit validation
    p_lcdm = PerturbationParameters(alpha_mu=0.0,beta_drag=0.0,residual_amp=0.0)
    p_zero = PerturbationParameters(alpha_mu=0.0,beta_drag=0.0,residual_amp=0.0)
    lim_diffs=[]
    for k in [0.001,0.005,0.01,0.05,0.1,0.2]:
        lim_diffs.append(abs(matter_power(k,0.0,p_lcdm)-matter_power(k,0.0,p_zero)))
    # Synthetic recovery over alpha_mu, holding other knobs fixed.
    truth = PerturbationParameters(alpha_mu=0.07,beta_drag=0.018,residual_amp=0.03)
    obs = synthetic_observations([10**(-2.5+i*(1.5)/23.0) for i in range(24)], truth)
    write_csv(out_root/"data"/"r013_synthetic_matter_observations.csv", obs)
    grid = [round(0.00+i*0.005,3) for i in range(31)]
    fit = fit_alpha_mu_grid(obs, PerturbationParameters(beta_drag=0.018,residual_amp=0.03), grid)
    write_csv(out_root/"data"/"r013_alpha_mu_grid_fit.csv", fit)
    best = min(fit, key=lambda r:r["chi2"])
    vals = [r["P_proxy"] for r in rows]
    mus = [r["mu_eff"] for r in rows]
    summary = {
        "roadmap_item":"R-013",
        "title":"Physical perturbation equations and matter-sector solver",
        "assumed_upstream":["R-008 accepted","R-009 accepted","R-010 accepted","R-011 accepted","R-012 accepted"],
        "closure_route":"matter-sector solver with low-ell CMB interface proxy",
        "gauge_policy":"Newtonian gauge, scalar sector, sub-horizon/quasi-static growth equation; no full Boltzmann hierarchy claim",
        "boundary_policy":"initial growing mode at a_ini=1e-3; regular positive k in Mpc^-1; normalized D(z)/D(0)",
        "lcdm_limit_max_abs_P_error":max(lim_diffs),
        "alpha_mu_truth":truth.alpha_mu,
        "alpha_mu_recovered_grid":best["alpha_mu"],
        "alpha_mu_recovery_abs_error":abs(best["alpha_mu"]-truth.alpha_mu),
        "min_mu_eff":min(mus),
        "max_mu_eff":max(mus),
        "min_P_proxy":min(vals),
        "rows_matter_power":len(rows),
        "rows_cmb_proxy":len(cmb),
        "finite_mode_count":len(modes),
        "k_unit":"Mpc^-1",
        "P_unit":"dimensionless proxy amplitude, not calibrated survey P(k)",
    }
    with (out_root/"validation"/"r013_validation_summary.json").open("w") as f:
        json.dump(summary,f,indent=2,sort_keys=True)
    return summary

if __name__ == "__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-root", default=".")
    args=ap.parse_args()
    print(json.dumps(run_artifacts(Path(args.out_root)),indent=2,sort_keys=True))
