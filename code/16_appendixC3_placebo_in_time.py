"""
Appendix C.3. Placebo-in-Time Test.

Assigns a false "treatment" date (2016, 2017, or 2018) to the true treated
districts, using only pre-2020 data, and re-estimates the identical
difference-in-differences procedure. None of the three placebo dates
should yield a significant effect.

Produces: output/AppendixC3_placebo_in_time.csv
"""
import pandas as pd
import numpy as np
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["year"] = viirs["year"].astype(int)
treated = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
districts = sorted(viirs["district"].unique())
n_treated = len(treated)


def compute_did(df, treated_set, fake_year):
    df = df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    pre = df[df["year"] < fake_year].groupby("treat")["log_lights"].mean()
    post = df[(df["year"] >= fake_year) & (df["year"] < 2020)].groupby("treat")["log_lights"].mean()
    if 1 not in pre.index or 1 not in post.index or 0 not in pre.index or 0 not in post.index:
        return np.nan
    return (post[1] - pre[1]) - (post[0] - pre[0])


print("Placebo-in-time test: fake treatment date assigned to true treated districts, using only pre-2020 data\n")

rng = np.random.default_rng(123)
rows = []
for fake_year in [2016, 2017, 2018]:
    obs = compute_did(viirs, treated, fake_year)
    perms = np.array([compute_did(viirs, set(rng.choice(districts, n_treated, replace=False)), fake_year)
                       for _ in range(2000)])
    perms = perms[~np.isnan(perms)]
    p = (np.sum(np.abs(perms) >= np.abs(obs)) + 1) / (len(perms) + 1)
    print(f"fake_year={fake_year}: observed DiD={obs:.4f}, permutation p={p:.4f}, n_valid_perms={len(perms)}")
    rows.append({"fake_year": fake_year, "observed_DiD": round(obs, 4), "permutation_p": round(p, 4)})

pd.DataFrame(rows).to_csv(OUTPUT_DIR / "AppendixC3_placebo_in_time.csv", index=False)
