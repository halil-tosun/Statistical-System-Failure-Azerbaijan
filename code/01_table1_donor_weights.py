"""
Table 1. Synthetic Control Donor Weights and Pre-treatment Fit.

For each of the nine treated districts, estimates synthetic-control weights
over the ten comparison districts by minimizing pre-treatment (2000-2019)
NDVI discrepancy, subject to non-negativity and adding-up constraints.
Reports the resulting weights and pre-treatment RMSE.

Produces: output/Table1_donor_weights.csv
"""
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from _paths import DATA_DIR, OUTPUT_DIR

ndvi = pd.read_csv(DATA_DIR / "AZE_district_NDVI_2000_2024.csv")[
    ["district", "group", "year", "ndvi_growing_season"]
]

treated_list = sorted(ndvi.loc[ndvi["group"] == "treated", "district"].unique())
donor_list = sorted(ndvi.loc[ndvi["group"] == "comparison", "district"].unique())

pre_ndvi = ndvi[ndvi["year"] < 2020].pivot(index="year", columns="district", values="ndvi_growing_season")
donor_mat = pre_ndvi[donor_list].values


def fit_weights(target_vec):
    n = donor_mat.shape[1]

    def objective(w):
        return np.sum((target_vec - donor_mat @ w) ** 2)

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    result = minimize(objective, w0, method="SLSQP", bounds=bounds,
                       constraints=constraints, options={"maxiter": 1000, "ftol": 1e-12})
    return result.x


weights_table, rmse_table = {}, {}
for td in treated_list:
    target = pre_ndvi[td].values
    w = fit_weights(target)
    weights_table[td] = w
    rmse_table[td] = np.sqrt(np.mean((target - donor_mat @ w) ** 2))

table1 = pd.DataFrame(weights_table, index=donor_list).T.round(3)
table1["RMSE (pre-fit)"] = pd.Series(rmse_table).round(4)

table1.to_csv(OUTPUT_DIR / "Table1_donor_weights.csv")
print("Table 1. Synthetic Control Donor Weights and Pre-treatment Fit\n")
print(table1.to_string())
