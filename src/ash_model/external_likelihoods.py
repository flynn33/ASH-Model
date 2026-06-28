
"""R-014 external-likelihood readiness workbench for ASH Cosmology.

Repository overlay module adapted from the independent R-014 research package.
The module defines
reviewed data-product contracts, Gaussian likelihoods with covariance
handling, matched baselines, synthetic blinded-data products, and
falsification/accounting utilities for the R-014 gate.

The numeric products here are synthetic validation fixtures generated
from the accepted R-012/R-013 style equations.  They are not external
cosmology measurements and are not claims of empirical validation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Dict, Iterable, List, Tuple
import hashlib, json, math
import numpy as np

C_KM_S = 299792.458

@dataclass(frozen=True)
class Params:
    H0: float = 70.0
    omega_m: float = 0.30
    omega_b: float = 0.049
    omega_r: float = 8.5e-5
    omega_k: float = 0.0
    omega_ash: float = 0.020
    alpha_mu: float = 0.070
    ash_p: float = 2.0
    rd_mpc: float = 147.1
    mb: float = -19.25
    sigma8: float = 0.80

    @property
    def omega_lam(self) -> float:
        return 1.0 - self.omega_m - self.omega_r - self.omega_k - self.omega_ash

def ash_source_a(a: np.ndarray | float, p: Params) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    # smooth finite-observer entropy/branch source: zero at a=1 after normalization only in derivative? positive E2 contribution
    return (a ** p.ash_p) * np.exp(-0.4*(1-a)**2)

def E2(a: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    a = np.asarray(a, dtype=float)
    if model == "lcdm":
        omega_ash = 0.0
        omega_lam = 1.0 - p.omega_m - p.omega_r - p.omega_k
        ash = 0.0
    else:
        omega_ash = p.omega_ash
        omega_lam = p.omega_lam
        ash = omega_ash * ash_source_a(a,p)
    return p.omega_r*a**-4 + p.omega_m*a**-3 + p.omega_k*a**-2 + omega_lam + ash

def H_z(z: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    a = 1/(1+np.asarray(z,dtype=float))
    return p.H0*np.sqrt(E2(a,p,model))

def integrate_trapz(fn: Callable[[np.ndarray], np.ndarray], lo: float, hi: float, n: int=4096) -> float:
    xs=np.linspace(lo,hi,n)
    return float(np.trapezoid(fn(xs), xs))

def comoving_distance(z: float, p: Params, model: str="ash") -> float:
    if z <= 0: return 0.0
    return C_KM_S * integrate_trapz(lambda zp: 1.0/H_z(zp,p,model), 0.0, z, 2048)

def d_lum(z: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    zarr=np.atleast_1d(np.asarray(z,dtype=float))
    vals=np.array([(1+zz)*comoving_distance(float(zz),p,model) for zz in zarr])
    return vals.reshape(np.shape(z))

def mu_distance(z: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    dl=np.maximum(d_lum(z,p,model),1e-9)
    return 5*np.log10(dl)+25.0

def DM_over_rd(z: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    zarr=np.atleast_1d(np.asarray(z,dtype=float))
    vals=np.array([comoving_distance(float(zz),p,model)/p.rd_mpc for zz in zarr])
    return vals.reshape(np.shape(z))

def DH_over_rd(z: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    return C_KM_S/H_z(z,p,model)/p.rd_mpc

def mu_eff(k: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    k=np.asarray(k,dtype=float)
    if model=="lcdm": return np.ones_like(k)
    shell = 0.5*(1 + np.cos(2*np.pi*np.log(k/0.02 + 1.0)/np.log(4.0)))
    damping = np.exp(-(k/0.75)**2)
    return 1.0 + p.alpha_mu*shell*damping

def growth_proxy(z: np.ndarray | float, k: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    z=np.asarray(z,dtype=float); k=np.asarray(k,dtype=float)
    Omz = p.omega_m*(1+z)**3 / (H_z(z,p,model)/p.H0)**2
    base = p.sigma8 * (Omz**0.55)/(1+z)**0.25
    return base * np.sqrt(mu_eff(k,p,model))

def cmb_lowell_proxy(ell: np.ndarray | float, p: Params, model: str="ash") -> np.ndarray:
    ell=np.asarray(ell,dtype=float)
    base = 1000.0/(ell*(ell+1))*(1+0.08*np.exp(-((ell-3)/3)**2))
    if model=="lcdm":
        return base
    modulation = 1 + 0.025*p.alpha_mu/0.07*np.cos(np.pi*ell/4)*np.exp(-ell/25)
    return base*modulation

def theory_vector(rows: List[dict], p: Params, model: str="ash") -> np.ndarray:
    vals=[]
    for r in rows:
        probe=r["probe"]; x=float(r["x"])
        if probe=="SN_mu":
            vals.append(float(mu_distance(x,p,model)))
        elif probe=="BAO_DM_rd":
            vals.append(float(DM_over_rd(x,p,model)))
        elif probe=="BAO_DH_rd":
            vals.append(float(DH_over_rd(x,p,model)))
        elif probe=="GROWTH_fsigma8":
            vals.append(float(growth_proxy(float(r["z"]),float(r["k"]),p,model)))
        elif probe=="CMB_lowell_Dl":
            vals.append(float(cmb_lowell_proxy(x,p,model)))
        else:
            raise ValueError(f"unknown probe {probe}")
    return np.array(vals,dtype=float)

def block_covariance(sigmas: np.ndarray, rho: float=0.15) -> np.ndarray:
    n=len(sigmas)
    idx=np.arange(n)
    corr=rho**np.abs(idx[:,None]-idx[None,:])
    return corr*np.outer(sigmas,sigmas)

def gaussian_loglike(y: np.ndarray, t: np.ndarray, cov: np.ndarray) -> Tuple[float,float,float]:
    r=y-t
    L=np.linalg.cholesky(cov)
    sol=np.linalg.solve(L,r)
    chi2=float(sol@sol)
    logdet=2*float(np.sum(np.log(np.diag(L))))
    loglike=-0.5*(chi2+logdet+len(y)*np.log(2*np.pi))
    return loglike, chi2, logdet

def aic_bic(loglike: float, n_params: int, n_data: int) -> Tuple[float,float]:
    return 2*n_params - 2*loglike, n_params*np.log(n_data) - 2*loglike

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canonical_json_hash(obj) -> str:
    return sha256_bytes(json.dumps(obj,sort_keys=True,separators=(",",":")).encode())

def make_rows() -> List[dict]:
    rows=[]
    for z in [0.01,0.05,0.10,0.20,0.35,0.50,0.70,0.90,1.10,1.30]:
        rows.append({"probe":"SN_mu","x":z,"z":z,"k":0.0,"unit":"mag"})
    for z in [0.38,0.51,0.70,0.93,1.32,2.33]:
        rows.append({"probe":"BAO_DM_rd","x":z,"z":z,"k":0.0,"unit":"dimensionless"})
        rows.append({"probe":"BAO_DH_rd","x":z,"z":z,"k":0.0,"unit":"dimensionless"})
    for z in [0.15,0.38,0.61,0.85,1.10]:
        for k in [0.02,0.05,0.10,0.20]:
            rows.append({"probe":"GROWTH_fsigma8","x":z,"z":z,"k":k,"unit":"dimensionless"})
    for ell in range(2,31):
        rows.append({"probe":"CMB_lowell_Dl","x":float(ell),"z":1089.0,"k":0.0,"unit":"uK^2_proxy"})
    return rows

def make_sigmas(rows: List[dict]) -> np.ndarray:
    sig=[]
    for r in rows:
        if r["probe"]=="SN_mu": sig.append(0.08)
        elif r["probe"].startswith("BAO"): sig.append(0.025*abs(float(r.get("x",1)))+0.05)
        elif r["probe"]=="GROWTH_fsigma8": sig.append(0.012)
        elif r["probe"]=="CMB_lowell_Dl": sig.append(0.025*abs(cmb_lowell_proxy(float(r["x"]),Params(),"ash"))+0.10)
    return np.array(sig,dtype=float)

def generate_synthetic(seed: int=20260626) -> Tuple[List[dict], np.ndarray, np.ndarray, np.ndarray]:
    rows=make_rows()
    p=Params()
    truth=theory_vector(rows,p,"ash")
    sig=make_sigmas(rows)
    cov=block_covariance(sig, rho=0.10)
    rng=np.random.default_rng(seed)
    y=truth.copy()  # deterministic blinded synthetic fixture at model truth; external data are not bundled
    return rows, y, cov, truth

def fit_grid(rows: List[dict], y: np.ndarray, cov: np.ndarray,
             omega_grid: np.ndarray, alpha_grid: np.ndarray) -> List[dict]:
    out=[]
    for om in omega_grid:
        for al in alpha_grid:
            p=Params(omega_ash=float(om), alpha_mu=float(al))
            t=theory_vector(rows,p,"ash")
            ll,chi2,ld=gaussian_loglike(y,t,cov)
            aic,bic=aic_bic(ll,8,len(y))
            out.append({"omega_ash":float(om),"alpha_mu":float(al),"loglike":ll,"chi2":chi2,"aic":aic,"bic":bic})
    out.sort(key=lambda r: r["chi2"])
    return out

def evaluate_models(rows: List[dict], y: np.ndarray, cov: np.ndarray) -> List[dict]:
    specs=[
        ("ASH_truth_family", Params(omega_ash=0.02, alpha_mu=0.07), "ash", 8),
        ("LCDM_nested_baseline", Params(omega_ash=0.0, alpha_mu=0.0), "lcdm", 6),
        ("ASH_background_only", Params(omega_ash=0.02, alpha_mu=0.0), "ash", 7),
        ("ASH_perturbation_only", Params(omega_ash=0.0, alpha_mu=0.07), "ash", 7),
    ]
    res=[]
    for name,p,model,k in specs:
        t=theory_vector(rows,p,model)
        ll,chi2,ld=gaussian_loglike(y,t,cov)
        aic,bic=aic_bic(ll,k,len(y))
        res.append({"model":name,"n_params":k,"loglike":ll,"chi2":chi2,"aic":aic,"bic":bic})
    res.sort(key=lambda r:r["aic"])
    return res

def whitened_residuals(y: np.ndarray, t: np.ndarray, cov: np.ndarray) -> np.ndarray:
    L=np.linalg.cholesky(cov)
    return np.linalg.solve(L,y-t)

def condition_number(cov: np.ndarray) -> float:
    return float(np.linalg.cond(cov))

def is_spd(cov: np.ndarray, tol: float=1e-12) -> bool:
    ev=np.linalg.eigvalsh(cov)
    return bool(np.min(ev)>tol)


def validation_summary() -> dict:
    """Return deterministic R-014 synthetic-validation summary.

    This summary is intentionally synthetic.  It is not an empirical likelihood
    result and must not be used as evidence that ASH fits external data.
    """
    rows, y, cov, truth = generate_synthetic()
    payload = {"rows": rows, "y": [round(float(v), 10) for v in y], "cov_shape": list(cov.shape), "seed": 20260626}
    lock_hash = canonical_json_hash(payload)
    grid = fit_grid(rows, y, cov, np.linspace(0.0, 0.04, 41), np.linspace(0.0, 0.14, 29))
    best = grid[0]
    models = evaluate_models(rows, y, cov)
    tbest = theory_vector(rows, Params(omega_ash=best["omega_ash"], alpha_mu=best["alpha_mu"]), "ash")
    wr = whitened_residuals(y, tbest, cov)
    return {
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
