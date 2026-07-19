"""
Figure 7. Event-Study Estimates of Reconstruction Effects Relative to 2019.

Reports the full 2014-2024 event-study coefficient trajectory (pooled
district-level DiD, treated vs. comparison, relative to 2019). The
2021-2024 coefficients match Table 2 exactly; the 2014-2018 coefficients
match Table C1 (Appendix C.2) exactly.

Produces: figures/Figure7_event_study.png
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
from _paths import OUTPUT_DIR, FIG_DIR, FIGURE_DPI
from _permutation import load_viirs, att_for_year, REF_YEAR

mpl.rcParams["font.family"] = "Liberation Sans"

viirs = load_viirs()
treated_list = sorted(viirs.loc[viirs["group"] == "treated", "district"].unique())
years_v = sorted(viirs["year"].unique())

coefs = [att_for_year(viirs, treated_list, y) for y in years_v]

fig, ax = plt.subplots(figsize=(9, 6))
ax.axhline(0, color="#666666", linewidth=0.8)
ax.axvline(2019.5, color="#333333", linestyle="--", linewidth=1.2)
ax.plot(years_v, coefs, marker="o", color="#c0392b", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Coefficient (log points, relative to 2019)")
ax.set_title("Figure 7. Event-Study Estimates of Reconstruction Effects\nRelative to 2019",
              fontsize=13, fontweight="bold")
ax.grid(alpha=0.25, linestyle=":")
plt.tight_layout()
plt.savefig(FIG_DIR / "Figure7_event_study.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")

print("Figure 7 saved to figures/Figure7_event_study.png\n")
for y, c in zip(years_v, coefs):
    print(f"  {y}: {c:.3f}")
