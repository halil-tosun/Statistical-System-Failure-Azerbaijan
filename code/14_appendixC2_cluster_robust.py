"""
Appendix C.2 (part 1 of 2). Small-Cluster Inference: Cluster-Robust vs.
Conventional Standard Errors.

Estimates the full event-study specification with cluster-robust (CR1
sandwich) standard errors clustered by district, and computes a joint
Wald F-test of all pre-treatment (2014-2018) coefficients. With only 19
clusters, this test is subject to a well-documented small-G pathology
(over-rejection); see 15_appendixC2_joint_pretrend_permutation.py for the
correctly-sized alternatives referenced in the paper.

Produces: output/AppendixC2_cluster_robust_event_study.csv
"""
import pandas as pd
import numpy as np
from scipy.stats import t as tdist, f as fdist
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["treat"] = (viirs["group"] == "treated").astype(int)
viirs["year"] = viirs["year"].astype(int)

ref_year = 2019
years = sorted(viirs["year"].unique())
event_years = [y for y in years if y != ref_year]


def build_design(df):
    district_dummies = pd.get_dummies(df["district"], drop_first=True)
    year_dummies = pd.get_dummies(df["year"], prefix="y", drop_first=True)
    inter = {f"treat_x_{y}": ((df["year"] == y) & (df["treat"] == 1)).astype(int) for y in event_years}
    inter_df = pd.DataFrame(inter, index=df.index)
    return pd.concat([pd.Series(1, index=df.index, name="const"), district_dummies, year_dummies, inter_df], axis=1)


def cluster_robust_se(X, y, cluster_ids):
    Xm = X.values.astype(float)
    beta, *_ = np.linalg.lstsq(Xm, y, rcond=None)
    resid = y - Xm @ beta
    XtX_inv = np.linalg.pinv(Xm.T @ Xm)
    meat = np.zeros((Xm.shape[1], Xm.shape[1]))
    clusters = cluster_ids.unique()
    G = len(clusters)
    for c in clusters:
        idx = (cluster_ids == c).values
        Xg, ug = Xm[idx], resid[idx]
        score = Xg.T @ ug
        meat += np.outer(score, score)
    N, k = Xm.shape
    dof_correction = (G / (G - 1)) * ((N - 1) / (N - k))
    cov_cluster = dof_correction * XtX_inv @ meat @ XtX_inv
    return beta, np.sqrt(np.diag(cov_cluster)), cov_cluster, G


X = build_design(viirs)
y = viirs["log_lights"].values
beta, se_c, cov_c, G = cluster_robust_se(X, y, viirs["district"])

col_names = X.columns.tolist()
coef_table = pd.DataFrame({"var": col_names, "coef": beta, "se_cluster": se_c})
dof = G - 1
coef_table["t"] = coef_table["coef"] / coef_table["se_cluster"]
coef_table["p"] = 2 * (1 - tdist.cdf(np.abs(coef_table["t"]), dof))

event_coefs = coef_table[coef_table["var"].str.startswith("treat_x_")].copy()
event_coefs["year"] = event_coefs["var"].str.replace("treat_x_", "").astype(int)
event_coefs = event_coefs.sort_values("year").reset_index(drop=True)

print(f"Number of clusters (districts): {G}\n")
print("=== Event-study with district-clustered standard errors ===")
print(event_coefs[["year", "coef", "se_cluster", "p"]].to_string(index=False))

pre_vars = [f"treat_x_{y}" for y in event_years if y < 2020]
idx_pre = [col_names.index(v) for v in pre_vars]
R = np.zeros((len(idx_pre), len(col_names)))
for i, j in enumerate(idx_pre):
    R[i, j] = 1
Rb = R @ beta
mid = np.linalg.pinv(R @ cov_c @ R.T)
Fstat = (Rb @ mid @ Rb) / len(idx_pre)
p_joint = 1 - fdist.cdf(Fstat, len(idx_pre), G - 1)
print(f"\nJoint cluster-robust F-test of pre-trends (H0: all pre-2020 coefficients = 0):")
print(f"F({len(idx_pre)}, {G - 1}) = {Fstat:.3f}, p = {p_joint:.4f}")
print("(This nominally rejects H0; see 15_appendixC2_joint_pretrend_permutation.py for why this is a small-G artefact.)")

coef_table.to_csv(OUTPUT_DIR / "AppendixC2_cluster_robust_event_study.csv", index=False)
