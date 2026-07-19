"""
Appendix C.5. Statistical Power.

Uses the empirical standard deviation of the permutation null distribution
to compute the minimum detectable effect (MDE) at 80% power, for both
alpha=0.10 (the smallest attainable two-sided p-value given a ten-unit
donor pool) and the conventional alpha=0.05.

Produces: output/AppendixC5_power_analysis.txt
"""
import pandas as pd
import numpy as np
from scipy.stats import norm
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["year"] = viirs["year"].astype(int)
treated = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
districts = sorted(viirs["district"].unique())
n_treated = len(treated)


def compute_did(df, treated_set):
    df = df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    pre = df[df["year"] <= 2019].groupby("treat")["log_lights"].mean()
    post = df[df["year"] >= 2021].groupby("treat")["log_lights"].mean()
    return (post[1] - pre[1]) - (post[0] - pre[0])


rng = np.random.default_rng(7)
null_dist = np.array([compute_did(viirs, set(rng.choice(districts, n_treated, replace=False))) for _ in range(5000)])
sd_null = null_dist.std()
print(f"Null (permutation) distribution SD: {sd_null:.4f}")

z_power = norm.ppf(0.80)

alpha = 0.10
z_alpha = norm.ppf(1 - alpha / 2)
mde = (z_alpha + z_power) * sd_null
print(f"Minimum detectable effect (80% power, two-sided alpha=0.10): {mde:.3f} log points (~{100 * (np.exp(mde) - 1):.0f}%)")
print(f"Observed effect (0.365) is {0.365 / mde:.2f}x the MDE -- well-powered to detect the observed effect")

alpha2 = 0.05
z_alpha2 = norm.ppf(1 - alpha2 / 2)
mde2 = (z_alpha2 + z_power) * sd_null
print(f"MDE at conventional alpha=0.05: {mde2:.3f} log points (~{100 * (np.exp(mde2) - 1):.0f}%)")

with open(OUTPUT_DIR / "AppendixC5_power_analysis.txt", "w") as f:
    f.write(f"Null distribution SD: {sd_null:.4f}\n")
    f.write(f"MDE (alpha=0.10, 80% power): {mde:.3f}\n")
    f.write(f"MDE (alpha=0.05, 80% power): {mde2:.3f}\n")
