"""
Figure 2. Observed and Synthetic NDVI Trajectories for the Nine Treated
Districts, 2000-2024.

Produces: figures/Figure2_NDVI_trajectories.png
"""
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
from _paths import DATA_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI

mpl.rcParams["font.family"] = "Liberation Sans"
NAVY = "#1F4E79"
GRAY = "#808080"

ndvi = pd.read_csv(DATA_DIR / "AZE_district_NDVI_2000_2024.csv")[
    ["district", "group", "year", "ndvi_growing_season"]
]
treated_list = sorted(ndvi.loc[ndvi["group"] == "treated", "district"].unique())
donor_list = sorted(ndvi.loc[ndvi["group"] == "comparison", "district"].unique())

full_pivot = ndvi.pivot(index="year", columns="district", values="ndvi_growing_season")
pre_pivot = ndvi[ndvi["year"] < 2020].pivot(index="year", columns="district", values="ndvi_growing_season")
donor_mat = pre_pivot[donor_list].values
years_full = full_pivot.index.values


def fit_weights(target_vec):
    n = donor_mat.shape[1]

    def objective(w):
        return np.sum((target_vec - donor_mat @ w) ** 2)

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    result = minimize(objective, w0, method="SLSQP", bounds=bounds,
                       constraints=constraints, options={"maxiter": 1000, "ftol": 1e-12})
    return result.x


fig, axes = plt.subplots(3, 3, figsize=(13, 11), sharex=True)
for i, td in enumerate(treated_list):
    ax = axes.flat[i]
    w = fit_weights(pre_pivot[td].values)
    synth_full = full_pivot[donor_list].values @ w
    actual_full = full_pivot[td].values

    ax.plot(years_full, actual_full, color=NAVY, linewidth=2, label="Observed")
    ax.plot(years_full, synth_full, color=GRAY, linewidth=1.8, linestyle=(0, (4, 2)), label="Synthetic")
    ax.axvline(2020, color="#333333", linestyle=":", linewidth=1)
    ax.set_title(td, fontsize=12, fontweight="bold")
    ax.grid(alpha=0.25, linestyle=":")
    ax.set_ylim(0.15, 0.75)
    if i == 0:
        ax.legend(loc="lower right", frameon=False, fontsize=9)

fig.suptitle("Figure 2. Observed and Synthetic NDVI Trajectories for the Nine Treated Districts",
              fontsize=14, fontweight="bold", y=1.0)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(FIG_DIR / "Figure2_NDVI_trajectories.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
print("Figure 2 saved to figures/Figure2_NDVI_trajectories.png")
