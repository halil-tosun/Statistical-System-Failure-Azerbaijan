"""
Appendix A. Extensive-Intensive Margin Decomposition (National Panel).

Applies the growth-accounting decomposition to the full national panel of
dairy-producing districts (2000-2024), classifying each district as
extensive- or intensive-margin dominant and computing the national
aggregate share of growth attributable to each margin. This validates that
the classification rule produces sensible results at national scale, not
only for the three treated districts examined in Table 3.

Produces:
  output/AppendixA_national_aggregate.csv
  output/AppendixA_district_classification.csv
"""
import pandas as pd
import numpy as np
from _paths import DATA_DIR, OUTPUT_DIR

BASE_YEAR, END_YEAR = 2000, 2024

df = pd.read_csv(DATA_DIR / "azerbaijan_dairy_panel_WIDE_districts.csv")
df["yield_per_cow"] = df["milk_production_tons"] * 1000 / df["cows_dairy_buffaloes_stock_heads"]


def decompose(region):
    d0 = df[(df["region"] == region) & (df["year"] == BASE_YEAR)]
    d1 = df[(df["region"] == region) & (df["year"] == END_YEAR)]
    if d0.empty or d1.empty:
        return None
    c0, y0v, m0 = d0["cows_dairy_buffaloes_stock_heads"].iloc[0], d0["yield_per_cow"].iloc[0], d0["milk_production_tons"].iloc[0]
    c1, y1v, m1 = d1["cows_dairy_buffaloes_stock_heads"].iloc[0], d1["yield_per_cow"].iloc[0], d1["milk_production_tons"].iloc[0]
    if pd.isna(c0) or pd.isna(c1) or pd.isna(y0v) or pd.isna(y1v) or c0 == 0:
        return None
    d_cows, d_yield = c1 - c0, y1v - y0v
    extensive = y0v * d_cows / 1000
    intensive = c0 * d_yield / 1000
    interaction = d_cows * d_yield / 1000
    return dict(region=region, delta_milk=m1 - m0, extensive=extensive, intensive=intensive, interaction=interaction)


results = [decompose(r) for r in df["region"].unique()]
results = [r for r in results if r is not None]
res_df = pd.DataFrame(results)
res_df["dominant_margin"] = np.where(res_df["intensive"].abs() > res_df["extensive"].abs(), "Intensive", "Extensive")

print(f"N districts with valid {BASE_YEAR} & {END_YEAR} data: {len(res_df)}\n")

tot_ext, tot_int, tot_inter = res_df["extensive"].sum(), res_df["intensive"].sum(), res_df["interaction"].sum()
tot_delta = res_df["delta_milk"].sum()
national = pd.DataFrame([
    {"Component": "Extensive margin (herd growth)", "National share of total growth (%)": round(100 * tot_ext / tot_delta, 1)},
    {"Component": "Intensive margin (yield growth)", "National share of total growth (%)": round(100 * tot_int / tot_delta, 1)},
    {"Component": "Interaction term", "National share of total growth (%)": round(100 * tot_inter / tot_delta, 1)},
])
print("National Aggregate Decomposition:")
print(national.to_string(index=False))
national.to_csv(OUTPUT_DIR / "AppendixA_national_aggregate.csv", index=False)

classification = res_df["dominant_margin"].value_counts().rename_axis("Dominant margin").reset_index(name="Number of districts")
print("\nDistrict Classification:")
print(classification.to_string(index=False))
classification.to_csv(OUTPUT_DIR / "AppendixA_district_classification.csv", index=False)
