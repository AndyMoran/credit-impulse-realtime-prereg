"""Figure 7 (post-lock, descriptive): P1a credit coefficients and forecasts by origin. Reads post_lock/out only."""
import os, numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); cp = pd.read_csv(os.path.join(HERE, 'out', 'p1a_coefficient_paths.csv'))
BLUE, ORANGE, INK, INK2, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#8a8984', '#e6e5e1'
plt.rcParams.update({'font.size': 9.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2,
                     'axes.spines.top': False, 'axes.spines.right': False, 'text.color': INK, 'axes.titlesize': 10, 'axes.titlelocation': 'left'})
x = cp.o / 4 + 0.125
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 6.4), sharex=True, gridspec_kw=dict(height_ratios=[1, 1.6]))
fig.subplots_adjust(left=0.1, right=0.83, top=0.9, bottom=0.15, hspace=0.3)
for ax in (a1, a2):
    for lo, hi in [(2001.25, 2002.0), (2008.0, 2009.5)]: ax.axvspan(lo, hi, color='#efeeea', lw=0, zorder=0)
    ax.grid(axis='y', color=GRID, lw=0.6); ax.set_axisbelow(True)
a1.axhline(0, color=INK2, lw=0.8); a1.plot(x, cp.b_ci_sum, color=BLUE, lw=2)
a1.set_ylim(-0.35, 0.05); a1.set_ylabel('sum of coefficients')
a1.set_title('A. Net effect of a one-point impulse on forecast GDP growth (four credit lags summed)', fontsize=9.5)
a2.plot(x, cp.y, 'o', ms=4.5, color=INK2, mec='white', mew=0.8, zorder=3)
a2.plot(x, cp.fb, color=MUTED, lw=1.6, ls=(0, (4, 2)))
a2.plot(x, cp.fa, color=ORANGE, lw=2)
last = cp.iloc[-1]
for val, lab, col in ((last.fa + 0.6, 'credit model', ORANGE), (last.fb - 0.6, 'AR(2) benchmark', INK2)):
    a2.text(x.iloc[-1] + 0.3, val, lab, color=INK2, fontsize=8.5, va='center')
a2.set_ylabel('GDP growth at origin + 4 (% annualised)'); a2.set_xlabel('forecast origin')
a2.set_title('B. Forecasts for four quarters ahead, and the outcome (dots)', fontsize=9.5)
a2.set_xlim(1999.5, 2019.0); a2.set_xticks(range(2000, 2020, 2))
i = cp.loss.idxmax(); a2.annotate(f"{cp.origin[i]}: credit model {cp.fa[i]:.1f}%, outcome {cp.y[i]:.1f}%".replace('-', '−'),
                                  (x[i], cp.fa[i]), xytext=(2011.6, 7.6), fontsize=8, color=INK2,
                                  arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
fig.suptitle('Figure 7. The credit model forecast a rebound that did not come', x=0.01, ha='left', fontsize=11, fontweight='bold')
fig.text(0.01, 0.015, 'Post-lock descriptive figure (Entry 29), from the locked P1a specification re-run unchanged; forecasts match the locked run exactly.\n'
         'A negative sum means a credit contraction raised the forecast. Grey bands: NBER recessions.', fontsize=7.5, color=INK2)
for ext in ('png', 'pdf'): fig.savefig(os.path.join(HERE, 'out', f'fig7_p1a_coefficients_forecasts.{ext}'), dpi=300)
