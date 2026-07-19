"""
Figure 5. Cross-validation between synthetic-control treatment effects and
the extensive-margin share of official agricultural growth, across the nine
treated districts.

Produces: figures/Figure5_crossvalidation_scatter.png
"""
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
from _paths import DATA_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI

mpl.rcParams["font.family"] = "Liberation Sans"

ndvi = pd.read_csv(DATA_DIR / "AZE_district_NDVI_2000_2024.csv")[["district", "group", "year", "ndvi_growing_season"]]
viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[["district", "group", "year", "nighttime_lights"]]
viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)

treated_list = sorted(ndvi.loc[ndvi["group"] == "treated", "district"].unique())
donor_list = sorted(ndvi.loc[ndvi["group"] == "comparison", "district"].unique())
pre_ndvi = ndvi[ndvi["year"] < 2020].pivot(index="year", columns="district", values="ndvi_growing_season")
viirs_pivot = viirs.pivot(index="year", columns="district", values="log_lights")
donor_mat = pre_ndvi[donor_list].values


def fit_weights(tv):
    n = donor_mat.shape[1]

    def obj(w):
        return np.sum((tv - donor_mat @ w) ** 2)

    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    return minimize(obj, w0, method="SLSQP", bounds=bounds, constraints=cons,
                     options={"maxiter": 1000, "ftol": 1e-12}).x


sat_gap = {}
for td in treated_list:
    w = fit_weights(pre_ndvi[td].values)
    synth = viirs_pivot[donor_list].values @ w
    gap = viirs_pivot[td].values - synth
    yrs = viirs_pivot.index.values
    sat_gap[td] = gap[yrs >= 2021].mean() - gap[yrs < 2020].mean()

# Extensive/intensive decomposition, 2000-2024, for the nine treated districts
panel = pd.read_csv(DATA_DIR / "azerbaijan_dairy_panel_WIDE_districts.csv")
panel["yield_per_cow"] = panel["milk_production_tons"] * 1000 / panel["cows_dairy_buffaloes_stock_heads"]
panel["region_clean"] = panel["region"].str.replace(" district", "", regex=False)
BASE_YEAR, END_YEAR = 2000, 2024

rows = []
for td in treated_list:
    sub = panel[panel["region_clean"] == td].set_index("year")
    if BASE_YEAR not in sub.index or END_YEAR not in sub.index:
        continue
    c0, c1 = sub.loc[BASE_YEAR, "cows_dairy_buffaloes_stock_heads"], sub.loc[END_YEAR, "cows_dairy_buffaloes_stock_heads"]
    y0, y1 = sub.loc[BASE_YEAR, "yield_per_cow"], sub.loc[END_YEAR, "yield_per_cow"]
    ext = y0 * (c1 - c0) / 1000
    inten = c0 * (y1 - y0) / 1000
    delta_milk = sub.loc[END_YEAR, "milk_production_tons"] - sub.loc[BASE_YEAR, "milk_production_tons"]
    rows.append({
        "district": td,
        "satellite_gap": round(sat_gap[td], 3),
        "ext_share_pct": round(100 * ext / delta_milk, 1),
    })

table5 = pd.DataFrame(rows).sort_values("satellite_gap", ascending=False)
rho, pval = spearmanr(table5["satellite_gap"], table5["ext_share_pct"])
print(f"Spearman correlation (satellite gap vs. extensive-margin share): rho={rho:.3f}, p={pval:.3f}\n")
print(table5.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 6.5))
ax.scatter(table5["ext_share_pct"], table5["satellite_gap"], s=90, color="#c0392b", zorder=3)
for _, r in table5.iterrows():
    ax.annotate(r["district"], (r["ext_share_pct"], r["satellite_gap"]), fontsize=9,
                xytext=(5, 5), textcoords="offset points")
ax.set_xlabel("Extensive-margin share of growth (%, official statistics)")
ax.set_ylabel("Satellite reconstruction signal (synthetic control gap, log points)")
ax.set_title(f"(Spearman rho={rho:.2f}, p={pval:.3f})", fontsize=12.5, fontweight="bold")
ax.grid(alpha=0.25, linestyle=":")
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure5_crossvalidation_scatter.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
print("\nFigure 5 saved to figures/Figure5_crossvalidation_scatter.png")
