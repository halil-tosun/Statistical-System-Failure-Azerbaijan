"""
run_all.py
==========
Runs the full replication pipeline in order and writes every table
(.csv/.xlsx) reported in the paper to ../output/, and every figure
(.png, 600 DPI) to ../figures/.

Expected runtime: under 2 minutes total on a standard laptop. The
slowest steps are the permutation-based inference procedures
(5,000 draws each), each of which completes in a few seconds.

Run individual numbered scripts directly to regenerate only one
table or figure.
"""
import importlib.util
import os
import time

HERE = os.path.dirname(__file__)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    t0 = time.time()

    print("=== 01: Table 1 -- Synthetic control donor weights and pre-treatment fit ===")
    _load("01_table1_donor_weights")

    print("\n=== 02: Figure 2 -- Observed and synthetic NDVI trajectories ===")
    _load("02_figure2_ndvi_trajectories")

    print("\n=== 03: Figure 3 -- Estimated reconstruction effects ===")
    _load("03_figure3_reconstruction_effects")

    print("\n=== 04: Table 2 -- Randomization inference for reconstruction effects ===")
    _load("04_table2_permutation_inference")

    print("\n=== 05: Figure 4 -- Permutation and placebo-based statistical validation ===")
    _load("05_figure4_statistical_validation")

    print("\n=== 06: Table 3 -- External validation using official statistics ===")
    _load("06_table3_external_validation")

    print("\n=== 07: Figure 5 -- Cross-validation scatter plot ===")
    _load("07_figure5_crossvalidation_scatter")

    print("\n=== 08: Figure 6 -- Sentinel-2 satellite imagery ===")
    _load("08_figure6_satellite_imagery")

    print("\n=== 09: Figure 7 -- Event-study estimates ===")
    _load("09_figure7_event_study")

    print("\n=== 10: Figure B1 -- Geographic distribution map ===")
    _load("10_figureB1_district_map")

    print("\n=== 11: Table C1 -- Pre-treatment event-study coefficients (Appendix C.2) ===")
    _load("11_tableC1_pretreatment_coefficients")

    print("\n=== 12: Appendix A -- National extensive/intensive margin decomposition ===")
    _load("12_appendixA_national_decomposition")

    print("\n=== 13: Appendix C.1 -- Leave-one-out robustness ===")
    _load("13_appendixC1_leave_one_out")

    print("\n=== 14: Appendix C.2 (1/2) -- Cluster-robust inference ===")
    _load("14_appendixC2_cluster_robust")

    print("\n=== 15: Appendix C.2 (2/2) -- Joint pre-trend test (OLS + permutation) ===")
    _load("15_appendixC2_joint_pretrend_permutation")

    print("\n=== 16: Appendix C.3 -- Placebo-in-time test ===")
    _load("16_appendixC3_placebo_in_time")

    print("\n=== 17: Appendix C.4 -- Ridge-regularized synthetic control ===")
    _load("17_appendixC4_ridge_synthetic_control")

    print("\n=== 18: Appendix C.5 -- Statistical power analysis ===")
    _load("18_appendixC5_power_analysis")

    print("\n=== 19: Appendix C.6 -- Heterogeneity by control-establishment timing ===")
    _load("19_appendixC6_staggered_heterogeneity")

    print("\n=== 20: Appendix C.7 -- Cloud/shadow masking sensitivity check ===")
    _load("20_appendixC7_qa_ndvi_check")

    print("\n=== 21: Figure 1 -- Conceptual framework (two-panel composite) ===")
    _load("21_figure1_conceptual_framework")

    print(f"\nAll done in {time.time() - t0:.0f} seconds.")
    print("See ../output/ for all tables and ../figures/ for all figures (600 DPI).")
