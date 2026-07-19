"""
Table C1 (Appendix C.2). Pre-Treatment Event-Study Coefficients
(relative to 2019).

Uses the identical permutation methodology and random seed as Table 2 (see
_permutation.py), applied to the pre-treatment years 2014-2018, so that the
joint pre-trend test discussed in Appendix C.2 is computed on a fully
consistent basis with the main post-treatment results.

Produces: output/TableC1_pretreatment_coefficients.csv
"""
import pandas as pd
from _paths import OUTPUT_DIR
from _permutation import load_viirs, build_placebo_sets, permutation_p_value

PRE_YEARS = [2014, 2015, 2016, 2017, 2018]

viirs = load_viirs()
treated_districts = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
all_districts = sorted(viirs["district"].unique())
n_treated = len(treated_districts)

placebo_sets = build_placebo_sets(all_districts, n_treated)

rows = []
for y in PRE_YEARS:
    observed, p, _ = permutation_p_value(viirs, treated_districts, placebo_sets, y)
    rows.append({"Year": y, "Coefficient": round(observed, 3), "Permutation p": round(p, 4)})

table_c1 = pd.DataFrame(rows)
print("Table C1. Pre-Treatment Event-Study Coefficients (relative to 2019)\n")
print(table_c1.to_string(index=False))
table_c1.to_csv(OUTPUT_DIR / "TableC1_pretreatment_coefficients.csv", index=False)

print(
    "\nNote: 2017 shows a nominally significant coefficient (p < 0.01) considered in "
    "isolation. As discussed in the paper (Appendix C.2), this is not interpreted as "
    "evidence of a genuine pre-trend: it is a single coefficient among five pre-treatment "
    "years, its magnitude is small relative to the post-treatment effects, and the properly "
    "sized joint tests (OLS F-test and permutation joint test) do not reject the null of "
    "jointly zero pre-trends; only the cluster-robust Wald test does, which is attributable "
    "to a well-documented small-cluster pathology (see 13_appendixC2_cluster_robust.py)."
)
