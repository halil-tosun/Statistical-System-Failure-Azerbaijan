# REPRODUCIBILITY_CHECKLIST

## Study
**Measuring Agricultural Reconstruction under Statistical System Failure: Evidence from Post-Conflict Azerbaijan**

---

## Reproducibility Status

| Item | Status |
|------|:------:|
| Manuscript included | ✓ |
| Cover letter prepared | ✓ |
| Source code included | ✓ |
| Raw data included | ✓ |
| Analytical datasets reproducible from raw data | ✓ |
| README provided | ✓ |
| CODEBOOK provided | ✓ |
| Data documentation provided | ✓ |
| Software dependencies documented | ✓ |
| Conda environment provided | ✓ |
| License provided | ✓ |
| Citation metadata (CITATION.cff) | ✓ |
| One-command workflow (`run_all.py`) | ✓ |
| Figures reproducible (600 DPI) | ✓ |
| Tables reproducible | ✓ |
| Shared, seeded permutation module for cross-table consistency | ✓ |
| Open repository planned | ✓ |
| Zenodo DOI | ☐ Pending repository release |

---

## Computational Environment

- Python environment documented in `environment.yml`
- Package list documented in `requirements.txt`
- Expected runtime: under 3 minutes on a standard laptop

---

## Expected Workflow

1. Create the Python environment (`conda env create -f environment.yml` or `pip install -r requirements.txt`).
2. Run `python code/run_all.py`.
3. Verify that all tables appear in `output/` and all figures appear in `figures/` at 600 DPI.
4. Cross-check reported values against the manuscript's tables and figures (see `docs/CODEBOOK.md` for the full script-to-manuscript correspondence).

---

## Internal Consistency Checks

The following results are computed by more than one script using a shared, seeded
methodology and should match exactly:

| Quantity | Computed in | Cross-checked in |
|---|---|---|
| Post-treatment ATT (2021-2024) | `04_table2_permutation_inference.py` | `05_figure4_statistical_validation.py`, `09_figure7_event_study.py` |
| Pre-treatment coefficients (2014-2018) | `11_tableC1_pretreatment_coefficients.py` | `09_figure7_event_study.py` |
| Cluster-robust joint F-test | `14_appendixC2_cluster_robust.py` | Referenced (not recomputed) in `15_appendixC2_joint_pretrend_permutation.py` |

---

## Transparency Statement

This repository has been prepared to maximize computational reproducibility and
long-term accessibility. After public release, the archived GitHub repository will
be linked to Zenodo to obtain a permanent DOI.
