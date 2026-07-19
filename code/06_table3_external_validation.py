"""
Table 3. External Validation of Satellite-Based Reconstruction Using
Official Agricultural Statistics.

Restricted to the three treated districts (Aghdam, Fuzuli, Gubadli) for
which official post-2021 agricultural statistics are available. Reports
percentage changes 2021->2024 in official herd inventory, milk production,
and milk yield, alongside the percentage change in observed annual VIIRS
nighttime lights, and classifies the dominant recovery margin using the
identical decomposition identity applied to the national panel in
Appendix A (only the time window differs: 2021-2024 here vs. 2000-2024
there).

Produces: output/Table3_external_validation.csv
"""
import pandas as pd
import numpy as np
from _paths import DATA_DIR, OUTPUT_DIR

DISTRICTS = ["Aghdam", "Fuzuli", "Gubadli"]
START_YEAR, END_YEAR = 2021, 2024

panel = pd.read_csv(DATA_DIR / "azerbaijan_dairy_panel_WIDE_districts.csv")
panel["region_clean"] = panel["region"].str.replace(" district", "", regex=False)

viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "year", "nighttime_lights"]]

rows = []
for d in DISTRICTS:
    sub = panel[panel["region_clean"] == d].set_index("year")
    herd0 = sub.loc[START_YEAR, "cows_dairy_buffaloes_stock_heads"]
    herd1 = sub.loc[END_YEAR, "cows_dairy_buffaloes_stock_heads"]
    milk0 = sub.loc[START_YEAR, "milk_production_tons"]
    milk1 = sub.loc[END_YEAR, "milk_production_tons"]
    yield0 = milk0 * 1000 / herd0
    yield1 = milk1 * 1000 / herd1

    v_sub = viirs[viirs["district"] == d].set_index("year")
    ntl0 = v_sub.loc[START_YEAR, "nighttime_lights"]
    ntl1 = v_sub.loc[END_YEAR, "nighttime_lights"]

    herd_pct = 100 * (herd1 - herd0) / herd0
    milk_pct = 100 * (milk1 - milk0) / milk0
    yield_pct = 100 * (yield1 - yield0) / yield0
    ntl_pct = 100 * (ntl1 - ntl0) / ntl0

    d_cows = herd1 - herd0
    d_yield = yield1 - yield0
    extensive = yield0 * d_cows / 1000
    intensive = herd0 * d_yield / 1000
    margin_gap_pct = 100 * (abs(extensive) - abs(intensive)) / max(abs(extensive), abs(intensive))
    dominant = "Intensive" if abs(intensive) > abs(extensive) else "Extensive"
    label = f"{dominant} (marginal)" if abs(margin_gap_pct) < 5 else dominant

    rows.append({
        "District": d,
        "Herd Inventory Change (2021\u20132024, %)": round(herd_pct, 1),
        "Milk Production Change (2021\u20132024, %)": round(milk_pct, 1),
        "Milk Yield Change (2021\u20132024, %)": round(yield_pct, 1),
        "Mean Nighttime-Light Change (2021\u20132024, %)": round(ntl_pct, 1),
        "Dominant Recovery Margin (2021\u20132024)": label,
    })

table3 = pd.DataFrame(rows)
print("Table 3. External Validation of Satellite-Based Reconstruction\n")
print(table3.to_string(index=False))
table3.to_csv(OUTPUT_DIR / "Table3_external_validation.csv", index=False)
