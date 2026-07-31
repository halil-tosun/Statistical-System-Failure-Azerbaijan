# Measuring Agricultural Reconstruction under Statistical System Failure

## Open Science Replication Package

This repository contains the complete replication package accompanying the manuscript **"Measuring Agricultural Reconstruction under Statistical System Failure: Evidence from Post-Conflict Azerbaijan"**.

---

## Repository Overview

This repository follows open science and computational reproducibility principles and includes:

- Complete Python source code
- Raw satellite and administrative datasets
- Reproducible computational workflow
- Comprehensive documentation
- Software environment specifications
- Replication guide

---

## Repository Structure

```text
AJAE_Replication/
├── code/
├── data/
├── docs/
├── manuscript/
├── output/
├── figures/
├── gee_notebook/
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Documentation

- **docs/CODEBOOK.md** -- Analytical workflow and script-by-script description
- **docs/DATA_DESCRIPTION.md** -- Data sources and dataset structure
- **docs/REPRODUCIBILITY_CHECKLIST.md** -- Reproducibility checklist
- **docs/Replication_Guide.md** -- Complete replication guide

## Installation

```bash
conda env create -f environment.yml
conda activate ajae-repro
```

or

```bash
pip install -r requirements.txt
```

## Run

```bash
python code/run_all.py
```

This reproduces the complete analytical workflow: synthetic-control estimation, randomization and placebo inference, external validation against official statistics, cross-validation against independent satellite indicators, the event-study specification, seven robustness and sensitivity analyses (Appendix C), the national extensive/intensive margin decomposition (Appendix A), and all manuscript tables and figures.

Expected runtime is under three minutes on a standard laptop.

## Script-to-Manuscript Correspondence

| Script | Produces | Manuscript location |
|---|---|---|
| `01_table1_donor_weights.py` | Table 1 | Section 4.2 |
| `02_figure2_ndvi_trajectories.py` | Figure 2 | Section 5.1 |
| `03_figure3_reconstruction_effects.py` | Figure 3 | Section 5.2 |
| `04_table2_permutation_inference.py` | Table 2 | Section 5.3 |
| `05_figure4_statistical_validation.py` | Figure 4 | Section 5.3 |
| `06_table3_external_validation.py` | Table 3 | Section 5.4 |
| `07_figure5_crossvalidation_scatter.py` | Figure 5 | Section 5.5 |
| `08_figure6_satellite_imagery.py` | Figure 6 | Section 5.5 |
| `09_figure7_event_study.py` | Figure 7 | Section 5.6 |
| `10_figureB1_district_map.py` | Figure B1 | Appendix B |
| `11_tableC1_pretreatment_coefficients.py` | Table C1 | Appendix C.2 |
| `12_appendixA_national_decomposition.py` | Appendix A figures | Appendix A |
| `13_appendixC1_leave_one_out.py` | Leave-one-out robustness | Appendix C.1 |
| `14_appendixC2_cluster_robust.py` | Cluster-robust event study | Appendix C.2 |
| `15_appendixC2_joint_pretrend_permutation.py` | OLS + permutation joint test | Appendix C.2 |
| `16_appendixC3_placebo_in_time.py` | Placebo-in-time test | Appendix C.3 |
| `17_appendixC4_ridge_synthetic_control.py` | Ridge-regularized SCM | Appendix C.4 |
| `18_appendixC5_power_analysis.py` | Minimum detectable effect | Appendix C.5 |
| `19_appendixC6_staggered_heterogeneity.py` | Timing heterogeneity | Appendix C.6 |
| `20_appendixC7_qa_ndvi_check.py` | QA-mask sensitivity check | Appendix C.7 |
| `21_figure1_conceptual_framework.py` | Figure 1 | Section 2.4 |

## Citation

Please cite both the published article and the archived GitHub/Zenodo repository. Citation metadata are provided in `CITATION.cff`.

## License

MIT License (code). Data files retain the licensing terms of their original sources; see `docs/DATA_DESCRIPTION.md`.

## Contact

**Halil Tosun, Ph.D.**

ORCID: https://orcid.org/0000-0001-5117-0390

Email: halilibrahimtosun@gmail.com

**Zenodo DOI:** https://doi.org/10.5281/zenodo.21435733

**Version:** 1.0.0
