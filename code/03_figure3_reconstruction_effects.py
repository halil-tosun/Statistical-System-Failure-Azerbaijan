"""
Figure 3. Estimated Reconstruction Effects Relative to the Synthetic
Counterfactual.

Two-layer panel design: top shows observed vs. synthetic log Nighttime
Lights; bottom shows the difference (the reconstruction effect), colored
gray pre-2020 and navy post-2020.

Produces: figures/Figure3_reconstruction_effects.png
"""
from _paths import DATA_DIR, OUTPUT_DIR, FIG_DIR, FIGURE_DPI
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

mpl.rcParams['font.family'] = 'Liberation Sans'

NAVY = '#1f4e79'
GRAY = '#808080'
PRE_COLOR = '#9a9a9a'
POST_COLOR = NAVY

ndvi = pd.read_csv(DATA_DIR / 'AZE_district_NDVI_2000_2024.csv')[['district', 'group', 'year', 'ndvi_growing_season']]
viirs = pd.read_csv(DATA_DIR / 'AZE_district_VIIRS_2014_2024.csv')[['district', 'group', 'year', 'nighttime_lights']]
viirs['log_lights'] = np.log(viirs['nighttime_lights'] + 0.01)

treated_list = sorted(ndvi[ndvi['group'] == 'treated']['district'].unique())
donor_list = sorted(ndvi[ndvi['group'] == 'comparison']['district'].unique())

pre_ndvi = ndvi[ndvi['year'] < 2020].pivot(index='year', columns='district', values='ndvi_growing_season')
viirs_pivot = viirs.pivot(index='year', columns='district', values='log_lights')
donor_mat = pre_ndvi[donor_list].values


def fit_weights(tv):
    n = donor_mat.shape[1]
    def obj(w):
        return np.sum((tv - donor_mat @ w) ** 2)
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n
    w0 = np.ones(n) / n
    return minimize(obj, w0, method='SLSQP', bounds=bounds, constraints=cons,
                     options={'maxiter': 1000, 'ftol': 1e-12}).x


years_v = viirs_pivot.index.values
series = {}
for td in treated_list:
    w = fit_weights(pre_ndvi[td].values)
    synth = viirs_pivot[donor_list].values @ w
    actual = viirs_pivot[td].values
    series[td] = {'actual': actual, 'synth': synth, 'diff': actual - synth}

# Shared y-scale for the TOP (levels) panels only, for cross-district comparability of fit
all_levels = np.concatenate([np.concatenate([s['actual'], s['synth']]) for s in series.values()])
level_pad = 0.06 * (all_levels.max() - all_levels.min())
LEVEL_YLIM = (all_levels.min() - level_pad, all_levels.max() + level_pad)

fig = plt.figure(figsize=(14, 13))
outer = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.28)

split_idx = np.where(years_v == 2020)[0][0]  # index of 2020 in the year array

for idx, td in enumerate(treated_list):
    row, col = divmod(idx, 3)
    inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[row, col],
                                              height_ratios=[3, 1.1], hspace=0.08)
    ax_main = fig.add_subplot(inner[0])
    ax_diff = fig.add_subplot(inner[1], sharex=ax_main)

    d = series[td]

    # --- main panel: observed vs synthetic ---
    ax_main.axvspan(2020.5, years_v.max() + 0.4, color='black', alpha=0.05, linewidth=0)
    ax_main.axvline(2020.4, color='#333333', linestyle='--', linewidth=1.1)
    line_obs, = ax_main.plot(years_v, d['actual'], color=NAVY, linewidth=2.0, solid_capstyle='round')
    line_syn, = ax_main.plot(years_v, d['synth'], color=GRAY, linewidth=1.8, linestyle=(0, (4, 2)))
    ax_main.set_ylim(*LEVEL_YLIM)
    ax_main.set_title(td, fontsize=12, fontweight='bold', pad=6)
    ax_main.grid(axis='y', color='#dddddd', linewidth=0.7)
    ax_main.grid(axis='x', visible=False)
    ax_main.tick_params(axis='x', labelbottom=False, length=0, labelsize=8.5)
    ax_main.tick_params(axis='y', labelsize=8.5)
    for spine in ['top', 'right']:
        ax_main.spines[spine].set_visible(False)
    if col == 0:
        ax_main.set_ylabel('log Nighttime\nLights', fontsize=9)
    else:
        ax_main.tick_params(axis='y', labelleft=False)

    # small legend, first panel only
    if idx == 0:
        ax_main.legend([line_obs, line_syn], ['Observed', 'Synthetic'],
                        loc='upper left', frameon=False, fontsize=8.5,
                        handlelength=2.2, borderaxespad=0.3, labelspacing=0.3)

    # --- lower panel: difference (ATT), two-tone, tight auto-scaled y-axis ---
    ax_diff.axvspan(2020.5, years_v.max() + 0.4, color='black', alpha=0.05, linewidth=0)
    ax_diff.axvline(2020.4, color='#333333', linestyle='--', linewidth=1.1)
    ax_diff.axhline(0, color='#555555', linewidth=1.3, zorder=1)

    # pre-2020 segment (gray), post-2020 segment (navy), overlapping at the split point
    ax_diff.plot(years_v[:split_idx + 1], d['diff'][:split_idx + 1],
                 color=PRE_COLOR, linewidth=1.9, solid_capstyle='round', zorder=2)
    ax_diff.plot(years_v[split_idx:], d['diff'][split_idx:],
                 color=POST_COLOR, linewidth=1.9, solid_capstyle='round', zorder=2)

    # tight, per-panel automatic y-scale (own data + small padding)
    dmin, dmax = d['diff'].min(), d['diff'].max()
    pad = max(0.08 * (dmax - dmin), 0.03)
    ax_diff.set_ylim(dmin - pad, dmax + pad)

    ax_diff.grid(axis='y', color='#eeeeee', linewidth=0.6)
    ax_diff.grid(axis='x', visible=False)
    ax_diff.tick_params(axis='y', labelsize=7.5)
    for spine in ['top', 'right']:
        ax_diff.spines[spine].set_visible(False)
    if col == 0:
        ax_diff.set_ylabel('Obs. \u2212\nSynth.', fontsize=8.5)
    else:
        ax_diff.tick_params(axis='y', labelleft=False)

    if row == 2:
        ax_diff.set_xticks([2014, 2016, 2018, 2020, 2022, 2024])
        ax_diff.tick_params(axis='x', labelsize=8.5)
        ax_diff.set_xlabel('')
    else:
        ax_diff.tick_params(axis='x', labelbottom=False, length=0)

fig.suptitle('Figure 3. Estimated Reconstruction Effects\nRelative to the Synthetic Counterfactual',
             fontsize=14, fontweight='bold', y=1.01)

plt.savefig(FIG_DIR / 'Figure3_reconstruction_effects.png', dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
print("Figure 3 saved to figures/Figure3_reconstruction_effects.png")
