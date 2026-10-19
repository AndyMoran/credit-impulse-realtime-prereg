"""§13 pre-registered figures from the locked Phase 2 outputs (results_real/). No new estimation."""
import json, os, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, 'results_real'); OUT = os.path.join(HERE, 'figures')
os.makedirs(OUT, exist_ok=True)
res = json.load(open(os.path.join(R, 'results.json')))
BLUE, ORANGE, INK, INK2, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#8a8984', '#e6e5e1'
plt.rcParams.update({'font.size': 9.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False, 'text.color': INK,
                     'axes.titlesize': 10.5, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left'})
qx = lambda t: t / 4 + 0.125                                   # quarter index -> decimal year (mid-quarter)
qs = lambda t: f"{t // 4}Q{t % 4 + 1}"
REC = [(2001.25, 2002.0), (2008.0, 2009.5)]                    # NBER recessions (quarters)
def shade(ax):
    for a, b in REC: ax.axvspan(a, b, color='#efeeea', lw=0, zorder=0)
def save(fig, name, note):
    fig.text(0.01, 0.01, note, fontsize=7.5, color=INK2, ha='left', va='bottom', wrap=True)
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=300); fig.savefig(os.path.join(OUT, name + '.pdf')); plt.close(fig)

# ------------------------------------------------------------- Figure 3: headline grid (forest plot of RMSE ratios)
c, g = res['core'], res['grid']
rows = [  # label, point, interval or None, kind
    ('GDP growth: real-time credit, revised target (P1a)', c['P1a']['ratio'], c['P1a']['ratio_ci90'], 'primary'),
    ('GDP growth: real-time credit, early target', g['g']['rt_early'], None, 'cell'),
    ('GDP growth: revised credit, revised target', g['g']['totrev_revised'], None, 'cell'),
    ('Unemployment: real-time credit, revised target (P1b)', c['P1b']['ratio'], c['P1b']['ratio_ci90'], 'primary'),
    ('Unemployment: real-time credit, early target', g['u']['rt_early'], None, 'cell'),
    ('Unemployment: revised credit, revised target', g['u']['totrev_revised'], None, 'cell'),
    ('SPF median GDP forecast, credit-corrected (P2a)', c['P2a']['ratio'], c['P2a']['ratio_ci90'], 'primary')]
fig, ax = plt.subplots(figsize=(7.2, 3.9)); fig.subplots_adjust(left=0.43, right=0.80, top=0.86, bottom=0.27)
y = np.arange(len(rows))[::-1]
ax.axvline(1.0, color=INK2, lw=1, zorder=1)
for yi, (lab, pt, ci, kind) in zip(y, rows):
    if ci: ax.plot(ci, [yi, yi], color=BLUE, lw=2, solid_capstyle='round', zorder=2)
    if kind == 'primary': ax.plot(pt, yi, 'o', ms=8, color=BLUE, mec='white', mew=2, zorder=3)
    else: ax.plot(pt, yi, 'D', ms=6, mfc='white', mec=BLUE, mew=1.6, zorder=3)
    ax.text(1.02, yi, f'{pt:.3f}' + (f'  [{ci[0]:.2f}, {ci[1]:.2f}]' if ci else ''), va='center', ha='left', fontsize=8.5, color=INK2, transform=ax.get_yaxis_transform())
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8.8); ax.tick_params(axis='y', length=0)
ax.set_xlim(0.9, 1.40); ax.set_xlabel('RMSE ratio, credit model ÷ benchmark  (below 1 = credit helps)')
ax.grid(axis='x', color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.text(0.993, y[0] + 0.75, '← helps', fontsize=8, color=INK2, ha='right'); ax.text(1.007, y[0] + 0.75, 'hurts →', fontsize=8, color=INK2, ha='left')
ax.set_ylim(-0.6, y[0] + 1.1)
fig.suptitle('Figure 3. Credit did not improve real-time forecasts at h = 4', x=0.01, ha='left', fontsize=11, fontweight='bold')
save(fig, 'fig3_grid_rmse_ratios', 'Filled dots with bars: confirmatory tests with 90% block-bootstrap intervals (estimate-only band).\nOpen diamonds: other grid cells (point estimates). '
     'Credit-revision premium: GDP +0.0005 [−0.066, 0.037]; unemployment +0.008 [−0.018, 0.024]. 78 origins, 1999Q3–2018Q4. Source: locked Phase 2 run (results.json).')

# ------------------------------------------------------------- Figure 4: cumulative squared-error differences
panels = [('P1a', 'GDP growth (P1a)'), ('P1b', 'Unemployment rate (P1b)'), ('P2a', 'SPF median GDP forecast (P2a)')]
fig, axs = plt.subplots(3, 1, figsize=(7.2, 7.8), sharex=True); fig.subplots_adjust(left=0.1, right=0.97, top=0.92, bottom=0.15, hspace=0.42)
for ax, (k, title) in zip(axs, panels):
    d = pd.read_csv(os.path.join(R, f'{k}_forecasts.csv')); gain = (d.y - d.fb) ** 2 - (d.y - d.fa) ** 2
    x = qx(d.o.values); cs = gain.cumsum().values
    shade(ax); ax.axvspan(qx(8028) - 0.125, qx(8043) + 0.125, ymin=0, ymax=1, color=ORANGE, alpha=0.08, lw=0, zorder=0)
    ax.axhline(0, color=INK2, lw=0.8); ax.plot(x, cs, color=BLUE, lw=2, solid_joinstyle='round')
    sh = c[k]['crisis_share']; tot = sh['total_gain']
    ax.set_title(f'{title}: total {tot:+.1f}; origins 2007Q1–2010Q4 contribute {sh["window_gain"]:+.1f}'.replace('-', '−'), fontsize=9.5)
    ax.grid(axis='y', color=GRID, lw=0.6); ax.set_axisbelow(True); ax.set_ylabel('cumulative gain')
axs[0].text(qx(8028) - 0.05, -0.05, 'origins 2007Q1–2010Q4', fontsize=8, color=ORANGE, ha='left', va='top', transform=axs[0].get_xaxis_transform())
axs[-1].set_xlabel('forecast origin'); axs[-1].set_xlim(1999.5, 2019.0); axs[-1].set_xticks(range(2000, 2020, 2))
fig.suptitle('Figure 4. Where credit gained and lost: cumulative squared-error differences', x=0.01, ha='left', fontsize=11, fontweight='bold')
save(fig, 'fig4_cumulative_sed', 'Cumulative sum over origins of (benchmark error² − credit-model error²): rising = credit helping, falling = credit hurting. h = 4; revised targets.\n'
     'Grey: NBER recessions. Orange band: pre-registered 2007Q1–2010Q4 window (§13). Exploratory split S6, GDP RMSE ratio: 0.959 [0.896, 0.982]\n'
     'for origins to 2008Q3; 1.522 [1.148, 1.863] from 2008Q4. Source: locked Phase 2 run.')

# ------------------------------------------------------------- Figure 5: threshold timeline (D1)
d1 = res['D1']; order = [('rt_sig_ci', 'CI < 0 two quarters, real time'), ('totrev_sig_ci', 'CI < 0 two quarters, revised'),
                         ('rt_sig_cg', 'credit growth < nominal GDP growth, real time'), ('totrev_sig_cg', 'credit growth < nominal GDP growth, revised')]
fig, ax = plt.subplots(figsize=(7.2, 3.2)); fig.subplots_adjust(left=0.44, right=0.86, top=0.84, bottom=0.27)
for i, (k, lab) in enumerate(order):
    yi = len(order) - 1 - i
    for e in d1[k]['episodes']:
        a, b = qx(e['start']) - 0.125, qx(e['end']) + 0.125
        col = ORANGE if e['label'] == 'late' else BLUE
        ax.barh(yi, b - a, left=a, height=0.5, color=col, edgecolor='white', lw=1)
    ax.text(1.01, yi, f"{d1[k]['share']:.0%} of quarters", va='center', fontsize=8, color=INK2, transform=ax.get_yaxis_transform())
for p, lab in ((8004, '2001Q1 peak'), (8031, '2007Q4 peak')):
    ax.axvline(qx(p) - 0.125, color=INK, lw=1, ls=(0, (3, 2))); ax.text(qx(p) - 0.1, 3.55, lab, fontsize=8, color=INK)
ax.set_yticks(range(len(order))); ax.set_yticklabels([o[1] for o in order][::-1], fontsize=8.6); ax.tick_params(axis='y', length=0)
ax.set_xlim(1999.5, 2019.3); ax.set_ylim(-0.6, 3.9); ax.set_xticks(range(2000, 2020, 4)); ax.set_xlabel('forecast origin (signal assigned to its origin quarter)')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=ORANGE, label='late (starts at or after the peak)'), Patch(color=BLUE, label='false alarm')],
          loc='upper left', bbox_to_anchor=(0, -0.2), ncol=2, frameon=False, fontsize=8.5)
fig.suptitle('Figure 5. Credit threshold signals were late in both recessions (D1)', x=0.01, ha='left', fontsize=11, fontweight='bold')
save(fig, 'fig5_threshold_timeline', 'Rules fixed in §10; no free parameters. A hit requires an episode starting 1–6 quarters before an NBER peak: none occurred. Descriptive only.')

# ------------------------------------------------------------- Figure 6: GDP revisions vs real-time CI (P3)
d = pd.read_csv(os.path.join(R, 'P3_forecasts.csv')); p3 = c['P3']
fig, ax = plt.subplots(figsize=(7.2, 4.6)); fig.subplots_adjust(left=0.11, right=0.97, top=0.88, bottom=0.2)
ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
ax.scatter(d.CI, d.R, s=34, color=BLUE, edgecolor='white', lw=1.2, zorder=3)
b = np.polyfit(d.CI, d.R, 1); xx = np.linspace(d.CI.min(), d.CI.max(), 50)
ax.plot(xx, np.polyval(b, xx), color=ORANGE, lw=2, zorder=2)
for _, r in d.iterrows():
    if abs(r.R) > 3.2 or r.CI < -9: ax.annotate(qs(int(r.s)), (r.CI, r.R), xytext=(5, 3), textcoords='offset points', fontsize=7.5, color=INK2)
ax.set_xlabel('real-time credit impulse at the advance-estimate date (pp of GDP)'); ax.set_ylabel('revision: latest − advance GDP growth (pp, annualised)')
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.text(0.02, 0.97, f"partial β (controls: advance g_s, g_s−1) = {p3['beta_CI']:.3f}\n90% wild block bootstrap [{p3['ci90'][0]:.3f}, {p3['ci90'][1]:.3f}]".replace('-', '−') + f"  ·  n = {p3['n']}",
        transform=ax.transAxes, ha='left', va='top', fontsize=8.5, color=INK2)
fig.suptitle('Figure 6. GDP revisions against real-time credit (P3)', x=0.01, ha='left', fontsize=11, fontweight='bold')
save(fig, 'fig6_gdp_revisions_vs_ci', 'Each dot is one quarter, 1999Q2–2019Q4. Orange line: bivariate least-squares fit, for display only; the estimate reported is the partial coefficient from §9.\n'
     'Estimate-only band: the interval includes zero, so no credible effect.')
print('written:', sorted(os.listdir(OUT)))
