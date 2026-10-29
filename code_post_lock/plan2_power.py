"""
Plan 2: power and coverage before freezing (plan2/PLAN.md, Section 6). No real GDP outcome is read.

Realised-path method, as in the locked study: the REAL indicator path (the survey, or the real-time credit impulse),
SYNTHETIC GDP. Synthetic GDP follows the locked simulation's AR(2) process (test_phase2.synth: 1.84 + 0.264 g1 + 0.137 g2,
shock variance 10.8) plus beta times the indicator, timed so that the direct h-step regression is correctly specified:
  survey cell at horizon h: beta * S1[t - h]      (first-month reading, seasonally adjusted on the full history)
  credit cell at horizon h: beta * CI[t - h - 2]  (latest Z.1 impulse, as the locked synth uses CI[t - 6] at h = 4)
Effect sizes are defined by the expected RMSE ratio they produce at the 78 origins: 1.00 (beta = 0), 0.95, 0.90, 0.80.
beta is found by bisection on the mean simulated ratio (seed 20261202). Then R replications give power (share of
90% intervals wholly below 1), coverage (share of intervals containing the target ratio), the mean error correlation,
and, for cells with power below 0.80 at 0.90, the minimum detectable ratio is reported from the grid.

Simplification, stated in the plan: synthetic GDP has one vintage (no revisions), so contexts and outcomes coincide.
Usage: python plan2_power.py [R]      (default R = 300)  -> ../../plan2/power_coverage.json
"""
import os, sys, json
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan2_data as T, plan2_models as M
P = T.P

SEED_SEARCH, SEED_SIM = 20261202, 20261203
TARGETS = (1.00, 0.95, 0.90, 0.80)
AR = (1.84, 0.264, 0.137); SHOCK_VAR = 10.8


def paths(D, s):
    """Indicator series used in the DGP and, per origin, the regressor block the forecaster would have."""
    qn = D['qn']; O = T.origins(D)
    M1_full, _, _ = T.survey_quarterly(D, s, qn('2020Q1'))       # full-history adjustment, for the DGP only
    ci_full = P.credit(D, None, D['LATEST'], 'credrev')['CI']
    survey_blocks = {o: M.survey_block(D, s, o, 'q1')[0] for o in O}
    credit_blocks = {o: M.credit_block(D, o) for o in O}
    return M1_full, ci_full, survey_blocks, credit_blocks


def simulate(ind, lag, beta, rng, t0, t1):
    T_ = np.arange(t0, t1 + 1); g = np.zeros(len(T_)); g[:2] = 3.1
    x = ind.reindex(T_ - lag).fillna(0.0).values; e = rng.normal(0, np.sqrt(SHOCK_VAR), len(T_))
    for i in range(2, len(T_)):
        g[i] = AR[0] + AR[1] * g[i - 1] + AR[2] * g[i - 2] + beta * x[i] + e[i]
    return pd.Series(g, index=T_)


def one_rep(D, ind, lag, blocks, h, beta, rng):
    qn = D['qn']; y = simulate(ind, lag, beta, rng, qn('1960Q1'), qn('2019Q4'))
    O = T.origins(D); start = qn(T.START); fb, fa, yy = [], [], []
    for o in O:
        f, _, _ = M.fit(y.loc[:o - 1], [blocks[o]], o, h, start); fb.append(f['ar']); fa.append(f['all']); yy.append(y[o + h])
    return np.array(yy), np.array(fb), np.array(fa)


def mean_ratio(D, ind, lag, blocks, h, beta, reps, seed):
    rng = np.random.default_rng(seed)
    return float(np.mean([P.rmse_ratio(*one_rep(D, ind, lag, blocks, h, beta, rng)) for _ in range(reps)]))


def find_beta(D, ind, lag, blocks, h, target, reps=40, iters=12):
    if target >= 1.0: return 0.0
    sgn = 1.0; lo, hi = 0.0, 0.05
    while mean_ratio(D, ind, lag, blocks, h, sgn * hi, reps, SEED_SEARCH) > target and hi < 50: hi *= 2
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mean_ratio(D, ind, lag, blocks, h, sgn * mid, reps, SEED_SEARCH) > target: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def cell(D, ind, lag, blocks, h, R):
    out = {}
    for tgt in TARGETS:
        beta = find_beta(D, ind, lag, blocks, h, tgt); rng = np.random.default_rng(SEED_SIM)
        res = []
        for _ in range(R):
            yy, fb, fa = one_rep(D, ind, lag, blocks, h, beta, rng)
            lo, hi = P.boot_interval(lambda i: P.rmse_ratio(yy, fb, fa, i), len(yy), B=500)
            res.append((P.rmse_ratio(yy, fb, fa), lo, hi, np.corrcoef(yy - fb, yy - fa)[0, 1]))
        r = np.array(res)
        out[f'{tgt:.2f}'] = dict(beta=beta, median_ratio=float(np.median(r[:, 0])), power=float(np.mean(r[:, 2] < 1)),
                                 coverage=float(np.mean((r[:, 1] <= tgt) & (tgt <= r[:, 2]))),
                                 error_corr=float(np.mean(r[:, 3])))
        print(f'  h={h} target={tgt:.2f} beta={beta:.4f} power={out[f"{tgt:.2f}"]["power"]:.2f} '
              f'coverage={out[f"{tgt:.2f}"]["coverage"]:.2f}', flush=True)
    grid = [t for t in TARGETS if t < 1 and out[f'{t:.2f}']['power'] >= 0.80]
    out['underpowered_at_0.90'] = out['0.90']['power'] < 0.80
    out['minimum_detectable_ratio_on_grid'] = max(grid) if grid else None
    return out


if __name__ == '__main__':
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    D = T.load('synthetic')
    s = T.load_survey('GA') if os.path.exists(os.path.join(T.DATA, 'GACDFNA066MNFRBPHI.csv')) else None
    if s is None: sys.exit('Survey file missing: run plan2_fetch.py first.')
    M1_full, ci_full, sblocks, cblocks = paths(D, s)
    result = dict(R=R, bootstrap_draws_per_rep=500, seeds=dict(search=SEED_SEARCH, sim=SEED_SIM), cells={})
    for h in T.HORIZONS:
        print(f'survey, h = {h}', flush=True); result['cells'][f'survey_h{h}'] = cell(D, M1_full, h, sblocks, h, R)
    for h in (0, 1, 2):
        print(f'credit, h = {h}', flush=True); result['cells'][f'credit_h{h}'] = cell(D, ci_full, h + 2, cblocks, h, R)
    json.dump(result, open(os.path.join(T.EXT, 'power_coverage.json'), 'w'), indent=1)
    print('written', os.path.join(T.EXT, 'power_coverage.json'))
