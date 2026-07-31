# CHANGELOG

All notable changes to this replication package will be documented in this file.

The format is inspired by *Keep a Changelog* and follows semantic versioning where appropriate.

---

## Version 1.0.0 (Initial Public Release)

### Added
- Complete Python source code for all empirical analyses, tables, and figures.
- Raw satellite (NDVI, VIIRS, Sentinel-2) and administrative datasets.
- README.md with repository overview and usage instructions.
- CODEBOOK.md describing the analytical workflow and script-to-manuscript correspondence.
- DATA_DESCRIPTION.md documenting data sources and structure.
- REPRODUCIBILITY_CHECKLIST.md.
- Replication_Guide.md.
- CITATION.cff for software citation.
- LICENSE file.
- requirements.txt.
- environment.yml.
- .gitignore.

### Reproducibility
- One-command workflow via `run_all.py` (all 21 scripts, under 3 minutes).
- All figures rendered at 600 DPI.
- Shared, seeded permutation-inference module (`_permutation.py`) ensures Table 2, Figure 4,
  Figure 7, and Table C1 are computed on an identical methodological basis.
- Computational environment documented.
- Repository prepared for GitHub release and Zenodo archiving.

### Notes
The Zenodo DOI: https://doi.org/10.5281/zenodo.21435733
