# CODEBOOK

## Replication Package

**Measuring Agricultural Reconstruction under Statistical System Failure: Evidence from Post-Conflict Azerbaijan**

**Author:** Halil Tosun, Ph.D.

---

## Purpose

This document describes the role of each script included in the replication package, its required inputs, and its expected outputs. It serves as a roadmap for reproducing all empirical analyses, tables, and figures reported in the manuscript.

---

## Workflow

```text
Raw Data (data/raw/, data/satellite_images/, data/gee_outputs/, data/design_assets/)
    |
    +--> 01_table1_donor_weights.py .................... Table 1
    +--> 02_figure2_ndvi_trajectories.py ................ Figure 2
    +--> 03_figure3_reconstruction_effects.py ........... Figure 3
    +--> 04_table2_permutation_inference.py ............. Table 2
    +--> 05_figure4_statistical_validation.py ........... Figure 4
    +--> 06_table3_external_validation.py ............... Table 3
    +--> 07_figure5_crossvalidation_scatter.py .......... Figure 5
    +--> 08_figure6_satellite_imagery.py ................ Figure 6
    +--> 09_figure7_event_study.py ....................... Figure 7
    +--> 10_figureB1_district_map.py ..................... Figure B1
    +--> 11_tableC1_pretreatment_coefficients.py ......... Table C1
    +--> 12_appendixA_national_decomposition.py .......... Appendix A
    +--> 13_appendixC1_leave_one_out.py ................... Appendix C.1
    +--> 14_appendixC2_cluster_robust.py .................. Appendix C.2 (1/2)
    +--> 15_appendixC2_joint_pretrend_permutation.py ...... Appendix C.2 (2/2)
    +--> 16_appendixC3_placebo_in_time.py .................. Appendix C.3
    +--> 17_appendixC4_ridge_synthetic_control.py .......... Appendix C.4
    +--> 18_appendixC5_power_analysis.py ................... Appendix C.5
    +--> 19_appendixC6_staggered_heterogeneity.py .......... Appendix C.6
    +--> 20_appendixC7_qa_ndvi_check.py ..................... Appendix C.7
    +--> 21_figure1_conceptual_framework.py ................ Figure 1
    |
    v
run_all.py
```

Two shared modules are imported by the numbered scripts and are not run directly:

- **`_paths.py`** -- defines all input/output directories used throughout the package.
- **`_permutation.py`** -- shared, seeded permutation-inference machinery. This is what
  guarantees that Table 2, Figure 4, Figure 7, and Table C1 are computed on an
  identical methodological basis (same 5,000 district-relabeling placebos, same seed).

---

## Script Descriptions

### `01_table1_donor_weights.py`
Estimates synthetic-control donor weights for each of the nine treated districts by
minimizing pre-treatment (2000-2019) NDVI discrepancy, subject to non-negativity and
adding-up constraints. Reports weights and pre-treatment RMSE.
**Reproduces:** Table 1.

### `02_figure2_ndvi_trajectories.py`
Plots observed vs. synthetic NDVI trajectories (2000-2024) for all nine treated
districts, using the donor weights estimated in script 01.
**Reproduces:** Figure 2.

### `03_figure3_reconstruction_effects.py`
Two-layer panel figure: upper panels compare observed vs. synthetic Nighttime Lights;
lower panels show the annual treatment effect (observed minus synthetic), colored
gray pre-2020 and navy post-2020.
**Reproduces:** Figure 3.

### `04_table2_permutation_inference.py`
Computes the average treatment effect (ATT) for each post-treatment year (2021-2024)
and its permutation-based p-value and 95% null interval, using 5,000 district-level
relabelings of treatment status.
**Reproduces:** Table 2.

### `05_figure4_statistical_validation.py`
Plots the pooled observed ATT trajectory against ten placebo trajectories (each donor
district individually treated as "treated" against the remaining nine donors).
**Reproduces:** Figure 4.

### `06_table3_external_validation.py`
Compares satellite-based estimates with official district-level agricultural
statistics (herd inventory, milk production, milk yield) for the three districts with
available post-2021 data, and classifies the dominant recovery margin using the
extensive/intensive decomposition described in Appendix A.
**Reproduces:** Table 3.

### `07_figure5_crossvalidation_scatter.py`
Correlates the district-level satellite reconstruction signal with the
extensive-margin share of official agricultural growth (Spearman's rho).
**Reproduces:** Figure 5.

### `08_figure6_satellite_imagery.py`
Assembles the Sentinel-2 true-color before/after image panels (Aghdam, Zangilan;
2019 vs. 2024) from the source PNGs in `data/satellite_images/`.
**Reproduces:** Figure 6.

### `09_figure7_event_study.py`
Full 2014-2024 event-study coefficient trajectory (pooled district-level DiD,
relative to 2019).
**Reproduces:** Figure 7.

### `10_figureB1_district_map.py`
Renders the geographic distribution of treated and donor districts using
administrative boundaries from geoBoundaries.
**Reproduces:** Figure B1.

### `11_tableC1_pretreatment_coefficients.py`
Pre-treatment (2014-2018) event-study coefficients and permutation p-values, computed
with the identical methodology and seed as Table 2 (see `_permutation.py`).
**Reproduces:** Table C1 (Appendix C.2).

### `12_appendixA_national_decomposition.py`
Applies the extensive/intensive margin growth-accounting decomposition to the full
national panel of dairy-producing districts (2000-2024).
**Reproduces:** Appendix A figures (63.6% / 22.8% / 48 of 71 districts).

### `13_appendixC1_leave_one_out.py`
Re-estimates the average treatment effect ten times, each time excluding one donor
district.
**Reproduces:** Appendix C.1.

### `14_appendixC2_cluster_robust.py`
Estimates the full event-study specification with district-clustered standard
errors and reports the joint Wald test of pre-treatment coefficients.
**Reproduces:** Appendix C.2 (part 1).

### `15_appendixC2_joint_pretrend_permutation.py`
Computes the same joint pre-trend test using (a) conventional OLS standard errors
and (b) a permutation-based joint statistic, to show that the cluster-robust
rejection in script 14 is a small-cluster (small-G) artefact.
**Reproduces:** Appendix C.2 (part 2).

### `16_appendixC3_placebo_in_time.py`
Assigns false treatment dates (2016, 2017, 2018) to the true treated districts using
only pre-2020 data.
**Reproduces:** Appendix C.3.

### `17_appendixC4_ridge_synthetic_control.py`
Re-estimates synthetic-control weights with L2 (ridge) regularization at three
penalty strengths.
**Reproduces:** Appendix C.4.

### `18_appendixC5_power_analysis.py`
Computes the minimum detectable effect (MDE) from the empirical permutation null
distribution.
**Reproduces:** Appendix C.5.

### `19_appendixC6_staggered_heterogeneity.py`
Splits treated districts into war-recaptured (n=6) and ceasefire-handover (n=3)
subgroups and tests for heterogeneous effects.
**Reproduces:** Appendix C.6.

### `20_appendixC7_qa_ndvi_check.py`
Compares NDVI extracted with vs. without an explicit cloud/shadow mask.
**Reproduces:** Appendix C.7.

### `21_figure1_conceptual_framework.py`
Combines the static measurement-framework schematic (`data/design_assets/`) with a
code-generated extensive/intensive-margin diagram into the manuscript's two-panel
Figure 1.
**Reproduces:** Figure 1.

### `run_all.py`
Executes the complete replication workflow in order.

Run:

```bash
python code/run_all.py
```

to reproduce the complete set of analyses, tables, and figures.

---

## Expected Outputs

The workflow generates:

- All manuscript tables (`.csv` / `.xlsx`) in `output/`
- All manuscript figures (`.png`, 600 DPI) in `figures/`

---

## Reproducibility

The repository is organized to maximize transparency and computational reproducibility.
All analyses can be reproduced from the supplied data and source code. Permutation-based
results use fixed seeds (documented in each script) and are exactly reproducible on
rerun with the same NumPy version.
