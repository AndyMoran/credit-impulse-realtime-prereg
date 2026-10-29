"""Plan 2 figures (plan2/PLAN.md, Section 5) from results_attempt1/results.json. Reads no data."""
import json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, '..', 'results_attempt1', 'results.json')))
C = R['comparisons']; H = [0, 1, 2, 4]
INK, MUTED, GRID = '#1f2328', '#59636e', '#d8dee4'
SURVEY, CREDIT = '#1f6feb', '#bc4c00'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False})
NOTE = ('Coverage note: in simulations with the real indicator paths, these 90% intervals contained the true ratio in '
        '83–100% of replications when the indicator had an effect.\nWith no effect, they contained 1 in only 79–83% '
        '(survey) and 67–73% (credit) of replications; almost all misses lay wholly above 1, reflecting estimation cost.\n'
        'A credible improvement with no effect occurred in at most 3% of replications.')

# Figure 1: ratio curve
fig, ax = plt.subplots(figsize=(8, 5))
ax.axhline(1, color=MUTED, lw=1, ls='--', zorder=1)
for key, lab, col, dx, eoff in (('survey', 'Survey (General Activity)', SURVEY, -0.07, 0), ('credit', 'Credit impulse', CREDIT, 0.07, 2)):
    r = [C[f'{key}_h{h}']['ratio'] for h in H]; lo = [C[f'{key}_h{h}']['ci90'][0] for h in H]; hi = [C[f'{key}_h{h}']['ci90'][1] for h in H]
    x = [h + dx for h in H]
    ax.errorbar(x, r, yerr=[[a - b for a, b in zip(r, lo)], [b - a for a, b in zip(r, hi)]], fmt='o-', color=col,
                lw=1.6, capsize=3, ms=5, label=lab, zorder=3)
    for xi, hh, lv, hv in zip(x, H, lo, hi):
        below = key == 'survey'                       # survey labels under the bars, credit labels over them
        ax.annotate(f'e = {hh + eoff}', (xi, lv if below else hv), textcoords='offset points', xytext=(0, -11 if below else 4),
                    ha='center', fontsize=8, color=col)
ax.set_xticks(H); ax.set_xlabel('Target horizon h (quarters after the origin)')
ax.set_ylabel('RMSE ratio, model ÷ AR(2)\n(below 1: the indicator helped)'); ax.set_ylim(0.72, 1.38)
ax.set_title('Plan 2: the ratio curve, 78 real-time origins 1999Q3–2018Q4', loc='left', fontsize=11, color=INK)
ax.grid(axis='y', color=GRID, lw=0.6); ax.legend(frameon=False, loc='upper left')
fig.text(0.01, 0.01, 'Points: RMSE ratios; bars: 90% moving-block bootstrap intervals. e: quarters from the indicator\'s '
         'latest data. Primary test: survey at h = 1.\n' + NOTE, fontsize=6.8, color=MUTED, va='bottom')
fig.subplots_adjust(bottom=0.27); fig.savefig(os.path.join(HERE, 'plan2_fig1_ratio_curve.png'), dpi=200)
fig.savefig(os.path.join(HERE, 'plan2_fig1_ratio_curve.pdf'))

# Figure 2: coefficient curve
K = R['coefficients_last_origin']; b = [K[f'h{h}']['coef'] for h in H]
lo = [K[f'h{h}']['ci90'][0] for h in H]; hi = [K[f'h{h}']['ci90'][1] for h in H]
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.axhline(0, color=MUTED, lw=1, ls='--')
ax.errorbar(H, b, yerr=[[x - y for x, y in zip(b, lo)], [y - x for x, y in zip(b, hi)]], fmt='o-', color=SURVEY, lw=1.6, capsize=3, ms=5)
ax.set_xticks(H); ax.set_xlabel('Target horizon h (quarters after the origin)')
ax.set_ylabel('Survey coefficient\n(GDP growth, pp per index point)')
ax.set_title('Plan 2: the survey coefficient by horizon, estimated at the last origin (2018Q4)', loc='left', fontsize=11, color=INK)
ax.grid(axis='y', color=GRID, lw=0.6)
fig.text(0.01, 0.01, 'Bars: 90% moving-block bootstrap intervals over the training rows (block 4, 2,000 draws, seed 20261019). '
         'Intervals widen with h partly because\nmulti-step errors are serially correlated; a widening fan reflects a changing '
         'coefficient plus noise, not noise alone.', fontsize=6.8, color=MUTED, va='bottom')
fig.subplots_adjust(bottom=0.2); fig.savefig(os.path.join(HERE, 'plan2_fig2_coefficient_curve.png'), dpi=200)
fig.savefig(os.path.join(HERE, 'plan2_fig2_coefficient_curve.pdf'))
print('written')
