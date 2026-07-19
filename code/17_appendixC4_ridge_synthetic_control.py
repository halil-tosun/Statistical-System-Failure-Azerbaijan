"""
Appendix C.4. Ridge-Regularized Synthetic Control Weights.

Re-estimates treated-district synthetic control weights with an L2 (ridge)
penalty added to the weight-fitting objective, at penalty strengths of
0.01, 0.05, and 0.10, and reports the resulting average treated effect
against the unregularized (lambda=0) baseline.

Produces: output/AppendixC4_ridge_synthetic_control.csv
"""
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from _paths import DATA_DIR, OUTPUT_DIR

ndvi = pd.read_csv(DATA_DIR / "AZE_district_NDVI_2000_2024.csv")[["district", "group", "year", "ndvi_growing_season"]]
viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)

treated_list = sorted(ndvi.loc[ndvi["group"] == "treated", "district"].unique())
donor_list = sorted(ndvi.loc[ndvi["group"] == "comparison", "district"].unique())
pre_ndvi = ndvi[ndvi["year"] < 2020].pivot(index="year", columns="district", values="ndvi_growing_season")
donor_mat = pre_ndvi[donor_list].values
viirs_pivot = viirs.pivot(index="year", columns="district", values="log_lights")


def fit_weights_ridge(tv, lam):
    n = donor_mat.shape[1]

    def obj(w):
        return np.sum((tv - donor_mat @ w) ** 2) + lam * np.sum(w ** 2)

    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    return minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=cons,
                     options={"maxiter": 1000, "ftol": 1e-12}).x


rows = []
for lam in [0.0, 0.01, 0.05, 0.10]:
    gaps = []
    for td in treated_list:
        w = fit_weights_ridge(pre_ndvi[td].values, lam)
        synth_viirs = viirs_pivot[donor_list].values @ w
        gap = viirs_pivot[td].values - synth_viirs
        yrs = viirs_pivot.index.values
        gaps.append(gap[yrs >= 2021].mean() - gap[yrs < 2020].mean())
    print(f"lambda={lam:5.2f}: mean treated effect = {np.mean(gaps):.4f}, range=[{min(gaps):.3f}, {max(gaps):.3f}]")
    rows.append({"lambda": lam, "mean_treated_effect": round(np.mean(gaps), 4),
                 "min": round(min(gaps), 3), "max": round(max(gaps), 3)})

pd.DataFrame(rows).to_csv(OUTPUT_DIR / "AppendixC4_ridge_synthetic_control.csv", index=False)
