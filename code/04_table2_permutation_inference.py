"""
Table 2. Randomization Inference for Average Reconstruction Effects.

Reports the average treatment effect (ATT) for each post-treatment year
(2021-2024), together with the empirical 95% permutation null interval and
permutation p-value, based on 5,000 district-level relabelings of treatment
status among the 19 study districts.

Produces:
  output/Table2_permutation_inference.csv
  output/Table2_permutation_inference.xlsx
"""
import pandas as pd
import numpy as np
from _paths import OUTPUT_DIR
from _permutation import load_viirs, build_placebo_sets, permutation_p_value

POST_YEARS = [2021, 2022, 2023, 2024]

viirs = load_viirs()
treated_districts = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
all_districts = sorted(viirs["district"].unique())
n_treated = len(treated_districts)

placebo_sets = build_placebo_sets(all_districts, n_treated)

rows = []
for y in POST_YEARS:
    observed_att, p_value, null_dist = permutation_p_value(viirs, treated_districts, placebo_sets, y)
    ci_low, ci_high = np.percentile(null_dist, [2.5, 97.5])
    rows.append({
        "Post-treatment Year": y,
        "Average Treatment Effect (ATT)": round(observed_att, 3),
        "95% Permutation Null Interval": f"[{ci_low:.3f}, {ci_high:.3f}]",
        "Permutation p-value": round(p_value, 4),
    })

table2 = pd.DataFrame(rows)
print("Table 2. Randomization Inference for Average Reconstruction Effects\n")
print(table2.to_string(index=False))

table2.to_csv(OUTPUT_DIR / "Table2_permutation_inference.csv", index=False)
table2.to_excel(OUTPUT_DIR / "Table2_permutation_inference.xlsx", index=False)

print(
    "\nNotes: Average treatment effects (ATT) are computed as the district-level "
    "difference-in-differences in log nighttime-light radiance between the nine "
    "treated districts and the ten comparison districts, relative to 2019. "
    "Statistical significance is evaluated using 5,000 random permutations of "
    "district-level treatment assignment among the 19 study districts. The 95% "
    "permutation null interval reports the empirical 2.5th and 97.5th percentiles "
    "of the randomization distribution under the null hypothesis of no treatment effect."
)
