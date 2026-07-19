"""
Appendix C.6. Heterogeneity by Control-Establishment Timing.

Splits the nine treated districts into a war-recaptured subgroup (n=6,
control established during the 44-day war itself) and a ceasefire-handover
subgroup (n=3, control transferred under the 9 November 2020 trilateral
ceasefire statement), and tests whether their post-treatment effects
differ significantly via a permutation test over subgroup assignment.

Produces: output/AppendixC6_staggered_heterogeneity.csv
"""
import pandas as pd
import numpy as np
from _paths import DATA_DIR, OUTPUT_DIR

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
viirs["year"] = viirs["year"].astype(int)

war_recaptured = ["Shusha", "Jabrayil", "Fuzuli", "Zangilan", "Gubadli", "Khojavand"]
ceasefire_handover = ["Aghdam", "Kalbajar", "Lachin"]


def year_effects(df, treated_set, ref_year=2019):
    df = df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    ref = df[df["year"] == ref_year].groupby("treat")["log_lights"].mean()
    out = {}
    for y in sorted(df["year"].unique()):
        if y == ref_year:
            continue
        cur = df[df["year"] == y].groupby("treat")["log_lights"].mean()
        if 1 in cur.index and 0 in cur.index:
            out[y] = (cur[1] - ref[1]) - (cur[0] - ref[0])
    return out


def group_avg_post(df, treated_set, ref_year=2019, post_years=(2021, 2022, 2023, 2024)):
    df = df.copy()
    df["treat"] = df["district"].isin(treated_set).astype(int)
    ref = df[df["year"] == ref_year].groupby("treat")["log_lights"].mean()
    post = df[df["year"].isin(post_years)].groupby("treat")["log_lights"].mean()
    return (post[1] - ref[1]) - (post[0] - ref[0])


eff_war = year_effects(viirs, war_recaptured)
eff_cf = year_effects(viirs, ceasefire_handover)

print("Year | War-recaptured (n=6) | Ceasefire-handover (n=3)")
rows = []
for y in sorted(set(eff_war) | set(eff_cf)):
    print(f"{y}: {eff_war.get(y, float('nan')):.3f}  |  {eff_cf.get(y, float('nan')):.3f}")
    rows.append({"year": y, "war_recaptured": round(eff_war.get(y, float("nan")), 3),
                 "ceasefire_handover": round(eff_cf.get(y, float("nan")), 3)})

war_post = group_avg_post(viirs, war_recaptured)
cf_post = group_avg_post(viirs, ceasefire_handover)
print(f"\nWar-recaptured group (n=6) 2021-24 avg effect: {war_post:.3f}")
print(f"Ceasefire-handover group (n=3) 2021-24 avg effect: {cf_post:.3f}")
print(f"Difference (war - ceasefire): {war_post - cf_post:.3f}")

treated_all = war_recaptured + ceasefire_handover
rng = np.random.default_rng(123)
diffs = []
for _ in range(5000):
    perm = rng.permutation(treated_all)
    g1, g2 = list(perm[:6]), list(perm[6:])
    diffs.append(group_avg_post(viirs, g1) - group_avg_post(viirs, g2))
diffs = np.array(diffs)
obs_diff = war_post - cf_post
p = (np.sum(np.abs(diffs) >= np.abs(obs_diff)) + 1) / (len(diffs) + 1)
print(f"\nPermutation p-value for war-vs-ceasefire subgroup difference: {p:.4f}")

pd.DataFrame(rows).to_csv(OUTPUT_DIR / "AppendixC6_staggered_heterogeneity.csv", index=False)
