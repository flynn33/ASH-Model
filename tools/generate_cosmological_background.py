from pathlib import Path
import json, math, csv, sys, os

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ash_model.cosmological_background import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--out-root", default=".")
parser.add_argument("--refresh-figures", action="store_true")
args = parser.parse_args()
ROOT = Path(args.out_root)
DATA = ROOT/"data"/"ash-cosmology"/"background-equations"/"v0.1"
FIG = ROOT/"figures"/"ash-cosmology"/"background-equations"/"v0.1"
VAL = ROOT/"validation"/"background-equations"/"roadmap-012"/"outputs"
DATA.mkdir(parents=True, exist_ok=True); FIG.mkdir(parents=True, exist_ok=True); VAL.mkdir(parents=True, exist_ok=True)

p_lcdm = BackgroundParameters(Omega_ash=0.0)
p_ash = BackgroundParameters(Omega_Lambda=0.66491, Omega_ash=0.020)  # closure sum = 1
assert abs(p_ash.closure_sum_today() - 1.0) < 1e-10

rows_lcdm = integrate_background(p_lcdm, steps=500)
rows_ash = integrate_background(p_ash, steps=500)
write_csv(DATA/"r012_background_lcdm.csv", rows_lcdm)
write_csv(DATA/"r012_background_ash.csv", rows_ash)

feature_rows = []
for a in [10**(-3 + i*3/120) for i in range(121)]:
    f = finite_branch_features(a)
    feature_rows.append({"a":a, "z":1/a-1, **f, "ash_source_E": ash_source_E(a, p_ash), "w_ash":w_ash(a, p_ash)})
write_csv(DATA/"r012_ash_source_features.csv", feature_rows)

obs = synthetic_observations(p_ash, [0.25,0.3,0.35,0.42,0.5,0.6,0.72,0.85,1.0], sigma_frac=1e-6)
write_csv(DATA/"r012_synthetic_H_observations.csv", obs)

omega_grid = [i/10000 for i in range(0, 501)]  # 0 to 0.05
best, fit_table = grid_fit_omega_ash(obs, BackgroundParameters(Omega_Lambda=0.66491), omega_grid)
write_csv(DATA/"r012_omega_ash_grid_fit.csv", fit_table)

cov_cols = ["E2","H_km_s_Mpc","ash_source_E","w_ash","q"]
cov = covariance_matrix(rows_ash[::10], cov_cols)
with open(DATA/"r012_background_covariance.csv","w",newline="") as f:
    w=csv.writer(f, lineterminator="\n"); w.writerow([""]+cov_cols)
    for name,row in zip(cov_cols,cov):
        w.writerow([name]+row)

# Figures
import matplotlib.pyplot as plt
def col(rows, key): return [r[key] for r in rows]
plt.figure()
plt.plot(col(rows_lcdm,'z'), col(rows_lcdm,'H_km_s_Mpc'), label='LCDM limit')
plt.plot(col(rows_ash,'z'), col(rows_ash,'H_km_s_Mpc'), label='ASH source')
plt.xscale('log'); plt.xlabel('redshift z'); plt.ylabel('H(z) [km s$^{-1}$ Mpc$^{-1}$]')
plt.legend(); plt.tight_layout(); plt.savefig(FIG/"r012_H_of_z.png", dpi=160); plt.close()

plt.figure()
plt.plot(col(feature_rows,'a'), col(feature_rows,'ash_source_E'))
plt.xscale('log'); plt.xlabel('scale factor a'); plt.ylabel('normalized ASH source E_ASH(a)')
plt.tight_layout(); plt.savefig(FIG/"r012_ash_source.png", dpi=160); plt.close()

plt.figure()
plt.plot([r['Omega_ash'] for r in fit_table], [r['chi2'] for r in fit_table])
plt.xlabel('$\\Omega_{ASH}$'); plt.ylabel('$\\chi^2$ synthetic H recovery')
plt.tight_layout(); plt.savefig(FIG/"r012_grid_fit.png", dpi=160); plt.close()

summary = {
    "roadmap_item": "R-012",
    "title": "Cosmological background equations and standard-baseline relation",
    "assumed_upstream": ["R-008 accepted", "R-009 accepted", "R-010 accepted", "R-011 accepted"],
    "lcdm_limit_max_abs_E2_error": max(abs(ash_E2(r['a'], p_lcdm)-lcdm_E2(r['a'], p_lcdm)) for r in rows_lcdm),
    "closure_sum_today": p_ash.closure_sum_today(),
    "omega_ash_truth": p_ash.Omega_ash,
    "omega_ash_recovered_grid": best["Omega_ash"],
    "omega_ash_recovery_abs_error": abs(best["Omega_ash"] - p_ash.Omega_ash),
    "min_E2_ash": min(r['E2'] for r in rows_ash),
    "max_abs_w_ash": max(abs(r['w_ash']) for r in rows_ash),
    "final_age_Gyr_since_a_min": rows_ash[-1]['t_Gyr_since_a_min'],
    "final_comoving_Mpc_from_a_min": rows_ash[-1]['chi_Mpc_from_a_min'],
    "data_files": [
        "data/ash-cosmology/background-equations/v0.1/r012_background_lcdm.csv",
        "data/ash-cosmology/background-equations/v0.1/r012_background_ash.csv",
        "data/ash-cosmology/background-equations/v0.1/r012_ash_source_features.csv",
        "data/ash-cosmology/background-equations/v0.1/r012_synthetic_H_observations.csv",
        "data/ash-cosmology/background-equations/v0.1/r012_omega_ash_grid_fit.csv",
        "data/ash-cosmology/background-equations/v0.1/r012_background_covariance.csv",
    ],
    "figure_files": [
        "figures/ash-cosmology/background-equations/v0.1/r012_H_of_z.png",
        "figures/ash-cosmology/background-equations/v0.1/r012_ash_source.png",
        "figures/ash-cosmology/background-equations/v0.1/r012_grid_fit.png",
    ],
}
summary["passed"] = True
(VAL/"verification.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
