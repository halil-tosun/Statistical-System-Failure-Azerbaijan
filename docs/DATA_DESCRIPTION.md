# DATA_DESCRIPTION

## Overview

This document describes the datasets included in the replication package for:

**Measuring Agricultural Reconstruction under Statistical System Failure: Evidence from Post-Conflict Azerbaijan**

Author: **Halil Tosun, Ph.D.**

---

## Repository Structure

```text
data/
├── raw/
│   ├── AZE_district_NDVI_2000_2024.csv
│   ├── AZE_district_VIIRS_2014_2024.csv
│   ├── azerbaijan_dairy_panel_WIDE_districts.csv
│   └── geoBoundaries-AZE-ADM2.geojson
│
├── satellite_images/
│   ├── Aghdam_city_2019_before.png
│   ├── Aghdam_city_2024_after.png
│   ├── Zangilan_area_2019_before.png
│   └── Zangilan_area_2024_after.png
│
├── gee_outputs/
│   └── ndvi_qa_comparison.csv
│
└── design_assets/
    └── Figure1a_measurement_framework_ORIGINAL.png
```

---

## Data Sources

| File | Source | Coverage |
|---|---|---|
| `AZE_district_NDVI_2000_2024.csv` | MODIS MOD13Q1 (Google Earth Engine), growing-season composite | 19 districts, 2000-2024 |
| `AZE_district_VIIRS_2014_2024.csv` | NOAA/VIIRS DNB monthly composite (Google Earth Engine), annual mean | 19 districts, 2014-2024 |
| `azerbaijan_dairy_panel_WIDE_districts.csv` | State Statistical Committee of the Republic of Azerbaijan | District-year, 2000-2024 (national panel used for Appendix A; treated-district subset used for Table 3) |
| `geoBoundaries-AZE-ADM2.geojson` | geoBoundaries.org, ADM2-level administrative boundaries | Azerbaijan |
| `satellite_images/*.png` | Copernicus Sentinel-2 (COPERNICUS/S2_SR_HARMONIZED), Google Earth Engine | Aghdam, Zangilan; 2019 and 2024 |
| `gee_outputs/ndvi_qa_comparison.csv` | MODIS MOD13Q1 with SummaryQA cloud/shadow mask applied (Google Earth Engine) | 19 districts, 4 years (2000, 2012, 2019, 2024) |
| `design_assets/Figure1a_measurement_framework_ORIGINAL.png` | Static, manually designed schematic (not code-generated) | -- |

---

## Raw vs. Analytical Data

All files in `data/raw/`, `data/satellite_images/`, and `data/gee_outputs/` are source
data extracted directly from the providers listed above via Google Earth Engine or
obtained from official statistical publications. No manual edits should be made to
these files. All analytical panels, weights, tables, and figures are generated
programmatically by the scripts in `code/` and written to `output/` and `figures/`.

---

## Temporal Coverage

- NDVI: 2000-2024 (growing-season composite, April-September)
- VIIRS Nighttime Lights: 2014-2024 (annual mean)
- Official agricultural statistics: 2000-2024 (national panel); 2021-2024 (post-reintegration subset used in Table 3)
- Sentinel-2 imagery: 2019 and 2024 (growing-season median composites)

## Geographic Coverage

Republic of Azerbaijan: 9 treated districts (reintegrated in 2020), 10 comparison
(donor) districts used for the synthetic control, and the full national panel of
dairy-producing districts used for the Appendix A decomposition.

---

## Reproducibility Notes

- Raw/source data are preserved separately from all derived/analytical outputs.
- All empirical results can be reproduced using the supplied Python scripts.
- Analytical outputs (tables, figures) are generated automatically by running the
  replication workflow (`code/run_all.py`) and are not stored in the repository by
  default (see `output/README_output.md` and `figures/`).
- The Google Earth Engine extraction workflow used to generate the satellite imagery
  and the QA-mask comparison data is documented in
  `gee_notebook/GEE_Before_After_Images.ipynb`.

---

## Citation

If these data are used, please cite both the associated journal article and the
archived GitHub/Zenodo repository. Users of the underlying raw data should also cite
the original providers listed in the Data Sources table above (NASA/USGS MODIS,
NOAA/NASA VIIRS, Copernicus/ESA Sentinel-2, geoBoundaries.org, and the State
Statistical Committee of the Republic of Azerbaijan).
