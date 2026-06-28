
from pathlib import Path
import sys, json, numpy as np
from ash_model.external_likelihoods import *

def test_covariance_is_spd_and_cholesky_likelihood_finite():
    rows,y,cov,truth=generate_synthetic()
    assert is_spd(cov)
    ll,chi2,ld=gaussian_loglike(y,truth,cov)
    assert np.isfinite(ll) and np.isfinite(chi2) and chi2 >= 0

def test_lcdm_nested_limit_zero_ash_matches_lcdm():
    rows=make_rows()
    p=Params(omega_ash=0.0, alpha_mu=0.0)
    a=theory_vector(rows,p,"ash")
    b=theory_vector(rows,p,"lcdm")
    assert np.max(np.abs(a-b)) < 1e-12

def test_synthetic_grid_recovers_truth_within_r014_tolerance():
    rows,y,cov,truth=generate_synthetic()
    grid=fit_grid(rows,y,cov,np.linspace(0.0,0.04,41),np.linspace(0.0,0.14,29))
    best=grid[0]
    assert abs(best["omega_ash"]-0.02) <= 0.005
    assert abs(best["alpha_mu"]-0.07) <= 0.02

def test_matched_baselines_are_declared_and_ranked():
    rows,y,cov,truth=generate_synthetic()
    res=evaluate_models(rows,y,cov)
    names={r["model"] for r in res}
    assert {"LCDM_nested_baseline","ASH_background_only","ASH_perturbation_only","ASH_truth_family"} <= names
    assert res[0]["aic"] <= max(r["aic"] for r in res)

def test_prereg_hash_is_deterministic():
    rows,y,cov,truth=generate_synthetic()
    payload={"rows":rows,"y":[round(float(v),10) for v in y],"cov_shape":list(cov.shape),"seed":20260626}
    assert canonical_json_hash(payload) == canonical_json_hash(payload)
    altered=dict(payload); altered["seed"]=0
    assert canonical_json_hash(payload) != canonical_json_hash(altered)
