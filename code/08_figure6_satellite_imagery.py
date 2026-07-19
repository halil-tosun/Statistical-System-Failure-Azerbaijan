"""
Figure 6. Representative Sentinel-2 imagery illustrating visible
reconstruction in Aghdam city centre and Zangilan, comparing 2019
(pre-reintegration) and 2024 (post-reintegration).

Requires the four source PNG images (downloaded via Google Earth Engine;
see gee_notebook/GEE_Before_After_Images.ipynb for the extraction code) in
data/satellite_images/.

Produces: figures/Figure6_satellite_imagery.png
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from _paths import SAT_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI

fig, axes = plt.subplots(2, 2, figsize=(9, 9.2))

pairs = [
    ("Aghdam city centre", "Aghdam_city_2019_before.png", "Aghdam_city_2024_after.png"),
    ("Zangilan (border settlement)", "Zangilan_area_2019_before.png", "Zangilan_area_2024_after.png"),
]

for row, (label, before_f, after_f) in enumerate(pairs):
    im_before = Image.open(SAT_DIR / before_f)
    im_after = Image.open(SAT_DIR / after_f)

    axes[row, 0].imshow(im_before)
    axes[row, 0].set_title(f"{label}\n2019 (pre-reintegration)", fontsize=11, fontweight="bold")
    axes[row, 0].axis("off")

    axes[row, 1].imshow(im_after)
    axes[row, 1].set_title(f"{label}\n2024 (post-reintegration)", fontsize=11, fontweight="bold")
    axes[row, 1].axis("off")

fig.suptitle(
    "Figure 6. Sentinel-2 Imagery: Reconstruction in Reintegrated Districts\n"
    "(true-color composites, growing-season median)",
    fontsize=13, fontweight="bold", y=0.995,
)
plt.figtext(0.5, 0.005, "Source: Copernicus Sentinel-2 (COPERNICUS/S2_SR_HARMONIZED), Google Earth Engine.",
            ha="center", fontsize=8.5, style="italic")

plt.tight_layout(rect=[0, 0.02, 1, 0.96])
plt.savefig(FIG_DIR / "Figure6_satellite_imagery.png", dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
print("Figure 6 saved to figures/Figure6_satellite_imagery.png")
