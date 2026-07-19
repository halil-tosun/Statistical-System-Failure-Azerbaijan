"""
Shared district-level permutation inference machinery, used identically by
both Table 2 (post-treatment ATT) and Table C1 (pre-treatment coefficients)
so that the two tables are computed with exactly the same methodology and
random seed.
"""
import numpy as np
import pandas as pd
from _paths import DATA_DIR

RNG_SEED = 20260717
N_PERM = 5000
REF_YEAR = 2019


def load_viirs():
    viirs = pd.read_csv(DATA_DIR / "AZE_district_VIIRS_2014_2024.csv")[
        ["district", "group", "year", "nighttime_lights"]
    ]
    viirs["log_lights"] = np.log(viirs["nighttime_lights"] + 0.01)
    viirs["year"] = viirs["year"].astype(int)
    return viirs


def att_for_year(df, treated_set, year, ref_year=REF_YEAR):
    """District-level difference-in-differences ATT relative to ref_year."""
    is_treated = df["district"].isin(treated_set)
    ref_t = df.loc[is_treated & (df["year"] == ref_year), "log_lights"].mean()
    ref_c = df.loc[~is_treated & (df["year"] == ref_year), "log_lights"].mean()
    cur_t = df.loc[is_treated & (df["year"] == year), "log_lights"].mean()
    cur_c = df.loc[~is_treated & (df["year"] == year), "log_lights"].mean()
    return (cur_t - ref_t) - (cur_c - ref_c)


def build_placebo_sets(all_districts, n_treated, seed=RNG_SEED, n_perm=N_PERM):
    """The identical 5,000 placebo district-relabelings used throughout the
    paper's permutation-based inference (Table 2, Table C1)."""
    rng = np.random.default_rng(seed)
    return [set(rng.choice(all_districts, n_treated, replace=False)) for _ in range(n_perm)]


def permutation_p_value(df, treated_set, placebo_sets, year):
    observed = att_for_year(df, treated_set, year)
    null_dist = np.array([att_for_year(df, pset, year) for pset in placebo_sets])
    p = (np.sum(np.abs(null_dist) >= np.abs(observed)) + 1) / (len(placebo_sets) + 1)
    return observed, p, null_dist
