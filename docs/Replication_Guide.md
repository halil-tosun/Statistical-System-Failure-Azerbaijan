# Replication Guide

**Measuring Agricultural Reconstruction under Statistical System Failure: Evidence from Post-Conflict Azerbaijan**

Author: Halil Tosun, Ph.D.

ORCID: https://orcid.org/0000-0001-5117-0390

---

## 1. Overview

This guide walks through reproducing every table and figure reported in the paper,
starting from a clean clone of the repository.

## 2. Requirements

- Python 3.11 (recommended) or any Python 3.9+ installation
- ~200 MB of free disk space
- No GPU or specialized hardware required
- No internet connection required to run the analysis (all satellite/administrative
  data are already extracted and included as static CSV/PNG files in `data/`)

## 3. Setup

### Option A -- conda (recommended)

```bash
conda env create -f environment.yml
conda activate ajae-repro
```

### Option B -- pip

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Running the Full Pipeline

```bash
cd code
python run_all.py
```

This runs all 21 scripts in the order in which their outputs appear in the paper
(Table 1 first, Figure 1 last, matching the order documented in `docs/CODEBOOK.md`).
Expect the full run to complete in under three minutes.

## 5. Running an Individual Script

Every script can also be run on its own, e.g.:

```bash
cd code
python 04_table2_permutation_inference.py
```

Each script prints its results to the console in addition to saving them to
`output/` (tables) or `figures/` (figures, 600 DPI).

## 6. Verifying the Results

After running `run_all.py`, check that:

1. `output/` contains 15 result files (12 `.csv`, 1 `.xlsx`, 2 `.txt`).
2. `figures/` contains 8 `.png` files, each at 600 DPI.
3. The printed console values for Table 1, Table 2, Table 3, and Table C1 match the
   corresponding tables in the manuscript exactly.
4. The note printed at the end of script 05 and script 09 ("Observed ATT by year")
   matches Table 2's ATT column for 2021-2024, confirming that the shared permutation
   module (`_permutation.py`) is producing internally consistent results.

## 7. Notes on the Google Earth Engine Extraction Workflow

The four Sentinel-2 images in `data/satellite_images/` and the QA-masked NDVI
comparison in `data/gee_outputs/ndvi_qa_comparison.csv` were generated once via
Google Earth Engine and archived as static files, since re-running this step
requires a (free) Google Earth Engine account and cannot be executed offline. The
notebook used to produce these files is included for transparency in
`gee_notebook/GEE_Before_After_Images.ipynb`; it does not need to be re-run to
reproduce any table or figure in the paper, since its outputs are already provided.

## 8. Known Sources of Numerical Variation

- All permutation-based p-values (Table 2, Table C1, Appendix C.2/C.3/C.6) use fixed
  random seeds and will reproduce exactly on rerun with the same NumPy version.
  Different NumPy/SciPy versions can in principle produce tiny (third-decimal-place)
  differences through differences in floating-point summation order; substantive
  conclusions are unaffected.
- Figure 1's panel (a) is a static, pre-existing design asset (not code-generated);
  see the docstring of `21_figure1_conceptual_framework.py` for details.

## 9. Contact

For questions about this replication package, please contact:

Halil Tosun, Ph.D. -- halilibrahimtosun@gmail.com -- https://orcid.org/0000-0001-5117-0390
