"""
Appendix C.1. Leave-One-Out Robustness.

Recomputes the baseline average treatment effect (pooled district-level DiD,
2014-2019 vs 2021-2024) ten times, each time excluding one donor district.

Produces: output/AppendixC1_leave_one_out.csv
"""
import pandas as pd
import numpy as np
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["year"] = viirs["year"].astype(int)
treated = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
donors = sorted(viirs.loc[viirs["group"] == "comparison", "district"].unique())


def compute_did(df, treated_set, exclude=None):
    df = df[df["district"] != exclude].copy() if exclude else df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    pre = df[df["year"] <= 2019].groupby("treat")["log_lights"].mean()
    post = df[df["year"] >= 2021].groupby("treat")["log_lights"].mean()
    return (post[1] - pre[1]) - (post[0] - pre[0])


baseline = compute_did(viirs, treated)
print(f"Full sample (baseline): {baseline:.3f}")
rows = []
for d in donors:
    est = compute_did(viirs, treated, exclude=d)
    rows.append((d, round(est, 3)))
    print(f"Dropped {d:12s}: DiD = {est:.3f}")

res_df = pd.DataFrame(rows, columns=["dropped_district", "DiD_estimate"])
res_df = pd.concat([res_df, pd.DataFrame([{"dropped_district": "Full sample (baseline)", "DiD_estimate": round(baseline, 3)}])], ignore_index=True)
res_df.to_csv(OUTPUT_DIR / "AppendixC1_leave_one_out.csv", index=False)
print("\nSaved to output/AppendixC1_leave_one_out.csv")
