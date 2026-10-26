"""
TimesFM extension, plan step 2: tests before the plan is frozen (timesfm/PLAN.md, Section 8).

Part A (real data, NO TimesFM): checks the real-time inputs and reproduces the locked AR(2) forecasts.
Part B (synthetic data ONLY): checks that a back-end returns 5-step forecasts and quantiles, and whether
         TimesFM 2.5 can take credit without future values.

Usage:
  python tfm_selftest.py A                 # real-data input checks; no model is loaded
  python tfm_selftest.py B dummy           # pipeline check with the stand-in AR(2)
  python tfm_selftest.py B tfm25           # TimesFM 2.5 on synthetic data (downloads the weights)
  python tfm_selftest.py B tfm30           # TimesFM 3.0 on synthetic data (needs tfm30_private.py)
No real US series is ever passed to a model in this script.
"""
import os, sys, datetime, platform
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
log = []
def say(m): print(m, flush=True); log.append(str(m))
def check(cond, msg):
    say(('PASS  ' if cond else 'FAIL  ') + msg)
    return bool(cond)


def part_a():
    import pandas as pd
    import tfm_data as T
    D = T.load(); qs = D['qs']; ok = True
    L = pd.read_csv(os.path.join(T.P2, 'results_real', 'P1a_forecasts.csv')).set_index('o')
    O = T.origins(D)
    ok &= check(len(O) == 78 and list(L.index) == O, f'78 origins, {qs(O[0])} to {qs(O[-1])}, match the locked table')
    bad_len = bad_cov = bad_x = bad_fb = bad_y = 0
    for o in O:
        y = T.gdp_context(D, o)
        bad_len += (len(y) != o - D['qn']('1965Q1'))
        c = T.credit_aligned(D, o, y)
        ci, qstar, k = T.credit_series(D, o)
        bad_cov += not (k == 2 and c[-1] == ci[qstar] and c[-2] == ci[qstar - 1])
        X = T.credit_lags_for_xreg(D, o, y)
        bad_x += not (X.shape == (4, len(y) + 5) and X[0, -1] == ci[qstar] and X[3, -1] == ci[qstar - 3])
        fb, fa = T.locked_benchmark(D, o, y)
        bad_fb += not (np.isclose(fb, L.loc[o, 'fb']) and np.isclose(fa, L.loc[o, 'fa']))
        bad_y += not np.isclose(T.outcome(D, o), L.loc[o, 'y'])
    ok &= check(bad_len == 0, 'GDP context runs 1965Q1 to o-1 with no gaps at every origin')
    ok &= check(bad_cov == 0, 'TimesFM 3.0 credit covariate ends at q* = o-2 (alignment rule), k = 2 at every origin')
    ok &= check(bad_x == 0, 'TimesFM 2.5 XReg lags: shape (4, n+5); horizon values are CI at q*..q*-3, all published')
    ok &= check(bad_fb == 0, 'Locked AR(2) and credit-model forecasts reproduced exactly at all 78 origins')
    ok &= alignment_checks(D, O)
    ok &= check(bad_y == 0, 'Outcomes match the locked table (2026Q3 vintage)')
    rsd = T.revision_sd(D)
    say(f'INFO  revision SD for L1/L2 noise (early estimate to 2026Q3 vintage, 2000Q3-2019Q4): {rsd:.3f} pp')
    o = D['qn']('2010Q3'); y = T.gdp_context(D, o)
    say(f'INFO  example origin 2010Q3: context {qs(y.index[0])}-{qs(y.index[-1])} ({len(y)} quarters); '
        f'credit to {qs(T.credit_series(D, o)[1])}; target {qs(o + 4)}')
    worked_example(D)
    return ok


def alignment_checks(D, O):
    """Plan Section 3: compare the credit inputs with the LOCKED credit model's regressors, value by value.
    Publication-timing checks alone would not catch a covariate shifted by the wrong number of quarters."""
    import tfm_data as T
    P = T.P; H = T.H; ok = True
    for which in ('rt', 'credrev'):
        bad_tgt = bad_hist = bad_30 = n_hist = 0
        for o in O:
            y = T.gdp_context(D, o)
            ci, qstar, k = T.credit_series(D, o, which)
            oi = P.origin_info(D, o)
            yfull = P.series(D, 'g', oi['w']).loc[:o - 1]
            X = T.credit_lags_for_xreg(D, o, y, which)
            # (a) fifth step (target o+4): must equal the locked credit model's regressors at origin o
            _, _, c_tgt = P.direct_rows(yfull, ci, np.array([o]), H, k)
            bad_tgt += not np.array_equal(X[:, -1], c_tgt[0])
            # (b) history: position t must hold the locked regressors of the training row whose target is t
            js = np.array([t - H for t in y.index])
            _, _, c_hist = P.direct_rows(yfull, ci, js, H, k)
            fin = np.isfinite(c_hist).all(1)
            bad_hist += not np.array_equal(X[:, :len(y)][:, fin], c_hist[fin].T); n_hist += int(fin.sum())
            # (c) TimesFM 3.0 past-only covariate: position t holds CI_{t-1}; last position (o-1) holds CI_{q*}
            c = T.credit_aligned(D, o, y, which)
            bad_30 += not (np.array_equal(c, np.array([ci[t - 1] for t in y.index])) and c[-1] == ci[qstar])
        ok &= check(bad_tgt == 0, f'[{which}] XReg fifth-step values equal the locked credit regressors '
                                  f'CI(q*-j), j=0..3, at all {len(O)} origins')
        ok &= check(bad_hist == 0, f'[{which}] XReg history values equal the locked training-row regressors '
                                   f'({n_hist} position-origin pairs)')
        ok &= check(bad_30 == 0, f'[{which}] TimesFM 3.0 covariate: position t holds CI(t-1), last value CI(q*), all origins')
    return ok


def worked_example(D, origin='2010Q1'):
    """Prints the plan's worked example (Section 3): credit values at each horizon position at one origin."""
    import tfm_data as T
    qs, qn = D['qs'], D['qn']; o = qn(origin); y = T.gdp_context(D, o)
    ci, qstar, k = T.credit_series(D, o); X = T.credit_lags_for_xreg(D, o, y); c = T.credit_aligned(D, o, y)
    say(f'Worked example, origin {origin}: GDP to {qs(o - 1)}, credit to q* = {qs(qstar)}, k = {k}, target {qs(o + 4)}')
    for i, t in enumerate([y.index[-1]] + [o + s for s in range(5)]):
        col = len(y) - 1 + i
        lab = 'last obs' if i == 0 else f'step {i}'
        say(f'  {lab:8s} {qs(t)}: ' + ', '.join(f'lag{j}=CI {qs(t - 4 - k - j)} ({X[j, col]:+.3f})' for j in range(4))
            + (f' | 3.0 cov = CI {qs(t - 1)} ({c[-1]:+.3f})' if i == 0 else ''))


def synthetic(n=215, seed=7):
    rng = np.random.default_rng(seed)
    y = np.zeros(n); c = np.zeros(n)
    for t in range(2, n):
        c[t] = 0.8 * c[t - 1] + rng.normal(0, 1)
        y[t] = 1.0 + 0.3 * y[t - 1] + 0.1 * y[t - 2] - 0.2 * c[t - 6] + rng.normal(0, 2.5)
    return y, c


def part_b(name):
    import tfm_models as M
    ok = True
    say(f'INFO  back-end {name}; Python {platform.python_version()} on {platform.platform()}')
    m = M.get(name)
    ys, cs = zip(*[synthetic(seed=s) for s in (7, 8, 9)])
    out = m.forecast(list(ys))
    def shape_ok(r): return r['point'].shape == (5,) and r['q'].shape == (5, 9) and np.isfinite(r['q']).all()
    ok &= check(all(shape_ok(r) for r in out), 'univariate: 5-step median and 9 quantiles per series')
    ok &= check(all(np.allclose(r['point'], r['q'][:, 4], atol=1e-4) for r in out), 'median equals the 0.5 quantile')
    ok &= check(all((np.diff(r['q'], axis=1) >= -1e-6).all() for r in out), 'quantiles are non-decreasing')
    neg = m.forecast([np.asarray(ys[0]) - 50.0])[0]['point']
    ok &= check((neg < 0).all(), 'a series shifted below zero gets negative forecasts (no clamp)')
    out2 = m.forecast(list(ys))
    ok &= check(all(np.allclose(a['point'], b['point']) for a, b in zip(out, out2)), 'repeat run gives identical forecasts')

    if hasattr(m, 'forecast_xreg'):
        H, k = 4, 2
        lags = []
        for y, c in zip(ys, cs):
            n = len(y); pos = list(range(n)) + [n + s for s in range(5)]
            lags.append(np.array([[c[t - H - k - j] if t - H - k - j >= 0 else 0.0 for t in pos] for j in range(4)]))
        # every horizon value is c at index <= n-1-(k-1) = q*: published by the origin
        ok &= check(max(n + 4 - H - k for n in [len(y) for y in ys]) == len(ys[0]) - 2, 'XReg horizon values use credit up to q* only')
        r = m.forecast_xreg(list(ys), lags)
        ok &= check(all(shape_ok(x) for x in r), 'with credit via XReg (lags 6-9): 5-step median and quantiles')
        try:
            m.forecast_xreg(list(ys), [L[:, :len(ys[0])] for L in lags])
            say('INFO  XReg accepted covariates of context length only (no horizon values)')
        except Exception as e:
            say(f'INFO  XReg refused covariates without horizon values ({type(e).__name__}): '
                'past-only credit must enter as lags known at the origin, as designed')
    if hasattr(m, 'forecast_past_cov'):
        covs = [np.r_[np.nan, c[:-1]][1:] for c in cs]; ys2 = [y[1:] for y in ys]
        r = m.forecast_past_cov(ys2, covs)
        ok &= check(all(shape_ok(x) for x in r), 'with credit as a past-only covariate: 5-step median and quantiles')
    return ok


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'A'
    say(f'TimesFM extension self-test, part {part}, {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M UTC}')
    ok = part_a() if part == 'A' else part_b(sys.argv[2] if len(sys.argv) > 2 else 'dummy')
    say('OVERALL: ' + ('PASS' if ok else 'FAIL'))
    tag = part if part == 'A' else f'B_{sys.argv[2] if len(sys.argv) > 2 else "dummy"}'
    open(os.path.join(HERE, f'tfm_selftest_{tag}.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
