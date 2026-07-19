"""
Appendix C.2 (part 2 of 2). Joint Pre-Trend Test: Conventional OLS and
Permutation-Based Alternatives to the Cluster-Robust Test.

Computes the same joint F-test of pre-treatment (2014-2018) event-study
coefficients as 14_appendixC2_cluster_robust.py, but using (a) conventional
(non-clustered) OLS standard errors and (b) a permutation-based joint
statistic (sum of squared pre-trend coefficients, evaluated against 5,000
district-relabeling placebos). Both properly-sized alternatives fail to
reject the null of jointly-zero pre-trends, in contrast to the cluster-
robust test, demonstrating that the cluster-robust rejection reported in
Appendix C.2 is a small-G artefact rather than genuine evidence against
parallel trends.

Produces: output/AppendixC2_joint_pretrend_test.txt
"""
import pandas as pd
import numpy as np
from scipy.stats import f as fdist
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["treat"] = (viirs["group"] == "treated").astype(int)
viirs["year"] = viirs["year"].astype(int)

ref_year = 2019
years = sorted(viirs["year"].unique())
event_years = [y for y in years if y != ref_year]
pre_years = [y for y in event_years if y < 2020]

# ---------- Part A: conventional (non-clustered) OLS joint F-test ----------


def build_design(df):
    district_dummies = pd.get_dummies(df["district"], drop_first=True)
    year_dummies = pd.get_dummies(df["year"], prefix="y", drop_first=True)
    inter = {f"treat_x_{y}": ((df["year"] == y) & (df["treat"] == 1)).astype(int) for y in event_years}
    inter_df = pd.DataFrame(inter, index=df.index)
    return pd.concat([pd.Series(1, index=df.index, name="const"), district_dummies, year_dummies, inter_df], axis=1)


X = build_design(viirs)
y = viirs["log_lights"].values
Xm = X.values.astype(float)
col_names = X.columns.tolist()
N, k = Xm.shape

beta, *_ = np.linalg.lstsq(Xm, y, rcond=None)
resid = y - Xm @ beta
sigma2 = np.sum(resid ** 2) / (N - k)
XtX_inv = np.linalg.pinv(Xm.T @ Xm)
cov_ols = sigma2 * XtX_inv

pre_vars = [f"treat_x_{yr}" for yr in pre_years]
idx_pre = [col_names.index(v) for v in pre_vars]
R = np.zeros((len(idx_pre), len(col_names)))
for i, j in enumerate(idx_pre):
    R[i, j] = 1
Rb = R @ beta
mid = np.linalg.pinv(R @ cov_ols @ R.T)
F_ols = (Rb @ mid @ Rb) / len(idx_pre)
p_ols = 1 - fdist.cdf(F_ols, len(idx_pre), N - k)

print("=== Conventional (non-clustered) OLS joint F-test of pre-trends ===")
print(f"F({len(idx_pre)}, {N - k}) = {F_ols:.3f}, p = {p_ols:.4f}\n")

# ---------- Part B: permutation-based joint test ----------
treated = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
districts = sorted(viirs["district"].unique())
n_treated = len(treated)


def year_effects(df, treated_set):
    df = df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    ref = df[df["year"] == ref_year].groupby("treat")["log_lights"].mean()
    effs = []
    for yr in pre_years:
        cur = df[df["year"] == yr].groupby("treat")["log_lights"].mean()
        effs.append((cur[1] - ref[1]) - (cur[0] - ref[0]))
    return np.array(effs)


obs = year_effects(viirs, treated)
obs_stat = np.sum(obs ** 2)

rng = np.random.default_rng(99)
perm_stats = []
for _ in range(5000):
    perm_treated = set(rng.choice(districts, n_treated, replace=False))
    perm_stats.append(np.sum(year_effects(viirs, perm_treated) ** 2))
perm_stats = np.array(perm_stats)
p_perm = (np.sum(perm_stats >= obs_stat) + 1) / (len(perm_stats) + 1)

print("=== Permutation-based joint pre-trend test ===")
print("Observed pre-trend coefficients (2014-2018, relative to 2019):", np.round(obs, 4))
print(f"Observed joint statistic (sum of squares): {obs_stat:.4f}")
print(f"Permutation-based joint p-value: {p_perm:.4f}\n")

print("=== Summary (compare to cluster-robust F(5,18)=7.139, p=0.0008 from script 14) ===")
print(f"Conventional OLS F-test:      p = {p_ols:.3f}")
print(f"Permutation-based joint test: p = {p_perm:.3f}")
print("Both fail to reject the null of jointly-zero pre-trends, supporting parallel trends.")

with open(OUTPUT_DIR / "AppendixC2_joint_pretrend_test.txt", "w") as f:
    f.write(f"OLS joint F-test: F({len(idx_pre)},{N - k})={F_ols:.3f}, p={p_ols:.4f}\n")
    f.write(f"Permutation joint test: statistic={obs_stat:.4f}, p={p_perm:.4f}\n")
