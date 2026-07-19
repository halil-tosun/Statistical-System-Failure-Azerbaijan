"""
Figure 4. Permutation and Placebo-Based Statistical Validation.

Single-panel design: bold navy "Observed ATT" line (pooled district-level
DiD, treated vs. comparison, relative to 2019 -- identical methodology to
Table 2) plotted against ten thin gray "placebo" lines (each donor district
individually treated as the "treated" unit against the other nine donors).

Produces: figures/Figure4_statistical_validation.png
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
from _paths import OUTPUT_DIR, FIG_DIR, FIGURE_DPI
from _permutation import load_viirs, att_for_year, REF_YEAR

mpl.rcParams["font.family"] = "Liberation Sans"
NAVY = "#1F4E79"
PLACEBO_GRAY = "#C7C7C7"

viirs = load_viirs()
treated_list = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
donor_list = sorted(viirs.loc[viirs["group"] == "comparison", "district"].unique())
years_v = sorted(viirs["year"].unique())


def did_trajectory(df, treated_set, control_set):
    is_t = df["district"].isin(treated_set)
    is_c = df["district"].isin(control_set)
    ref_t = df.loc[is_t & (df["year"] == REF_YEAR), "log_lights"].mean()
    ref_c = df.loc[is_c & (df["year"] == REF_YEAR), "log_lights"].mean()
    out = []
    for y in years_v:
        cur_t = df.loc[is_t & (df["year"] == y), "log_lights"].mean()
        cur_c = df.loc[is_c & (df["year"] == y), "log_lights"].mean()
        out.append((cur_t - ref_t) - (cur_c - ref_c))
    return np.array(out)


real_att = did_trajectory(viirs, treated_list, donor_list)

placebo_trajs = {}
for d in donor_list:
    other_donors = [x for x in donor_list if x != d]
    placebo_trajs[d] = did_trajectory(viirs, {d}, set(other_donors))

# Table 2 permutation p-values (reported for reference in the figure inset)
pvals = {2021: 0.0042, 2022: 0.0006, 2023: 0.0008, 2024: 0.0010}
years_arr = np.array(years_v)

fig, ax = plt.subplots(figsize=(11, 6.2))
for d, traj in placebo_trajs.items():
    ax.plot(years_arr, traj, color=PLACEBO_GRAY, linewidth=1.0, zorder=2)
ax.plot(years_arr, real_att, color=NAVY, linewidth=3.0, zorder=4, solid_capstyle="round")

ax.axhline(0, color="black", linewidth=0.6, zorder=1)
ax.axvspan(2020.4, years_arr.max() + 0.4, color="gray", alpha=0.09, linewidth=0, zorder=0)
ax.axvline(2020.4, color="black", linestyle="--", linewidth=1.3, zorder=3)

ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Average Treatment Effect (Observed \u2212 Synthetic NTL)", fontsize=11)
ax.set_title("Figure 4. Permutation and Placebo-Based Statistical Validation",
             fontsize=12.5, fontweight="bold", pad=12)
ax.grid(axis="y", color="#f0f0f0", linewidth=0.6)
ax.grid(axis="x", visible=False)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ylim = ax.get_ylim()
ax.annotate("Reintegration", xy=(2020.4, ylim[1] * 0.92), xytext=(2020.55, ylim[1] * 0.92),
            fontsize=8.5, color="#333333", va="top", ha="left")

legend_elems = [
    plt.Line2D([0], [0], color=NAVY, linewidth=3.0, label="Observed ATT"),
    plt.Line2D([0], [0], color=PLACEBO_GRAY, linewidth=1.5, label="Placebo estimates"),
]
ax.legend(handles=legend_elems, loc="upper left", frameon=False, fontsize=9.5)

p_text = "Permutation p-values\n" + "\n".join(f"{y} = {p:.4f}" for y, p in pvals.items())
ax.text(0.985, 0.97, p_text, transform=ax.transAxes, fontsize=8.7, va="top", ha="right",
        linespacing=1.5, bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                                    edgecolor="#cccccc", linewidth=0.8))

ax.set_xticks(years_v)
ax.tick_params(axis="both", labelsize=9.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure4_statistical_validation.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")

print("Figure 4 saved to figures/Figure4_statistical_validation.png")
print("\nObserved ATT by year (should match Table 2 exactly for 2021-2024):")
for y, v in zip(years_v, real_att):
    print(f"  {y}: {v:.3f}")
