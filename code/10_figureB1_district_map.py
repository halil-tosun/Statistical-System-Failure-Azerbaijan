"""
Figure B1. Geographic distribution of treated and donor districts used in
the synthetic-control analysis.

Produces: figures/FigureB1_district_map.png
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch
from _paths import DATA_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI

mpl.rcParams["font.family"] = "Liberation Sans"

with open(DATA_DIR / "geoBoundaries-AZE-ADM2.geojson") as f:
    geo = json.load(f)

name_map = {
    "Aghdam": "Agdam District", "Fuzuli": "Fuzuli District", "Jabrayil": "Jabrayil District",
    "Kalbajar": "Kalbajar District", "Gubadli": "Qubadli District", "Lachin": "Lachin District",
    "Zangilan": "Zangilan District", "Khojavand": "Khojavend District", "Shusha": "Shusha District",
    "Tartar": "Tartar District", "Goranboy": "Goranboy District", "Barda": "Barda District",
    "Aghjabadi": "Aghjabadi District", "Beylagan": "Beylagan District", "Jalilabad": "Jalilabad District",
    "Gadabay": "Gadabay District", "Dashkasan": "Dashkasan District", "Gazakh": "Qazakh District",
    "Tovuz": "Tovuz District",
}
treated_geo = {name_map[d] for d in ["Aghdam", "Fuzuli", "Jabrayil", "Kalbajar", "Gubadli",
                                      "Lachin", "Zangilan", "Khojavand", "Shusha"]}
comparison_geo = {name_map[d] for d in ["Tartar", "Goranboy", "Barda", "Aghjabadi", "Beylagan",
                                         "Jalilabad", "Gadabay", "Dashkasan", "Gazakh", "Tovuz"]}

fig, ax = plt.subplots(figsize=(9, 7))
patches_treated, patches_comparison, patches_other = [], [], []

for feat in geo["features"]:
    name = feat["properties"]["shapeName"]
    geom = feat["geometry"]
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    for poly in polys:
        ring = poly[0]
        mpl_poly = MplPolygon(np.array(ring), closed=True)
        if name in treated_geo:
            patches_treated.append(mpl_poly)
        elif name in comparison_geo:
            patches_comparison.append(mpl_poly)
        else:
            patches_other.append(mpl_poly)

ax.add_collection(PatchCollection(patches_other, facecolor="#e8e8e8", edgecolor="white", linewidths=0.4))
ax.add_collection(PatchCollection(patches_comparison, facecolor="#a9c8e8", edgecolor="white", linewidths=0.6))
ax.add_collection(PatchCollection(patches_treated, facecolor="#c0392b", edgecolor="white", linewidths=0.6))

ax.set_xlim(44.7, 50.7)
ax.set_ylim(38.3, 41.9)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Figure B1. Geographic Distribution of Treated and Donor Districts", fontsize=13, fontweight="bold")

legend_elems = [
    Patch(facecolor="#c0392b", label="Treated (reintegrated 2020)"),
    Patch(facecolor="#a9c8e8", label="Donor pool (comparison)"),
    Patch(facecolor="#e8e8e8", label="Other Azerbaijani districts"),
]
ax.legend(handles=legend_elems, loc="lower left", frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig(FIG_DIR / "FigureB1_district_map.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
print("Figure B1 saved to figures/FigureB1_district_map.png")
