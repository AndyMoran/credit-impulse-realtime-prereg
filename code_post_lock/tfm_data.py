"""
TimesFM extension: real-time inputs for each forecast origin (plan: timesfm/PLAN.md, Sections 3 and 5).

Builds, from the LOCKED phase2.py and the locked data, exactly what a forecaster had at origin o:
  - GDP growth from 1965Q1 to o-1, from the origin's RTDSM vintage;
  - the credit impulse from the latest Z.1 release before the origin, ending at q* = o-2;
  - the revised outcome for target o+4 (2026Q3 vintage) and the locked AR(2) forecast.

No TimesFM code is imported here. Nothing in this file changes the locked release.
"""
import os, sys, hashlib
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.dirname(HERE); sys.path.insert(0, P2)
LOCKED_PHASE2 = 'da697030f2349feae24dc79a3dfcbb786552b62186ffbf624a027c591814766e'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
if sha(os.path.join(P2, 'phase2.py')) != LOCKED_PHASE2: sys.exit('phase2.py is not the locked file; stopping.')
import phase2 as P

H = 4                    # target o + 4 (locked horizon)
STEPS = H + 1            # GDP observed through o - 1, so the target is the 5th step ahead
NL = P.NL                # four credit lags, as in the locked credit model
START = '1965Q1'         # same estimation window as the locked AR(2)


def load():
    D = P.load('real')
    P.LAST_TARGET = D['qn']('2019Q4')                       # locked COVID exclusion
    return D


def origins(D):
    qn = D['qn']
    return list(range(qn('1999Q3'), qn('2018Q4') + 1))


def gdp_context(D, o):
    """GDP growth (annualised, as locked) from 1965Q1 to o-1 in origin o's vintage. Index = quarter numbers."""
    oi = P.origin_info(D, o)
    y = P.series(D, 'g', oi['w']).loc[D['qn'](START):o - 1]
    if y.isna().any() or y.index[-1] != o - 1 or len(y) != o - D['qn'](START):
        raise ValueError(f'GDP context incomplete at origin {D["qs"](o)}')
    return y


def credit_series(D, o, which='rt'):
    """Credit impulse as available at origin o. which='rt' (Z.1 release before origin) or 'credrev'
    (today's Z.1, cut at the same release-time edge q*, as in the locked grid)."""
    oi = P.origin_info(D, o)
    cm = P.credit(D, oi['v'], oi['w'], which)
    if which != 'rt': cm = cm.loc[:oi['qstar']]
    ci = cm['CI']
    if ci.index.max() != oi['qstar']: raise ValueError('credit does not end at q*')
    return ci, oi['qstar'], oi['k']


def credit_aligned(D, o, y, which='rt'):
    """Past-only covariate for TimesFM 3.0 (plan Section 3, alignment rule).
    Position t holds the impulse for t-(k-1); with k = 2 that is t-1, so the last position (o-1) holds q*."""
    ci, qstar, k = credit_series(D, o, which)
    vals = np.array([ci.get(t - (k - 1), np.nan) for t in y.index])
    assert y.index[-1] - (k - 1) == qstar
    if np.isnan(vals).any(): raise ValueError('credit covariate has gaps')
    return vals


def credit_lags_for_xreg(D, o, y, which='rt'):
    """Dynamic covariates for TimesFM 2.5 XReg (plan Section 2): four lags of the impulse, each lagged so that
    every value, including those over the 5-step horizon, was published by the origin.
    Lag j (j = 0..3) at position t is CI_{t-H-k-j}. At the target t = o+4 this is CI_{q*-j}, exactly the
    regressors of the locked credit model. Returns an array (NL, len(y) + STEPS)."""
    ci, qstar, k = credit_series(D, o, which)
    pos = list(y.index) + [o + s for s in range(STEPS)]          # positions o-1-n+1 .. o+4
    out = np.array([[ci.get(t - H - k - j, np.nan) for t in pos] for j in range(NL)])
    used_max = max(t - H - k for t in pos)
    assert used_max == qstar, 'XReg covariate would use credit published after the origin'
    if np.isnan(out).any(): raise ValueError('XReg covariate has gaps')
    return out


def outcome(D, o):
    return P.target(D, 'g', o + H, 'revised')


def locked_benchmark(D, o, y):
    """The locked AR(2) (and credit-model) forecast, recomputed with the locked function."""
    ci, qstar, k = credit_series(D, o, 'rt')
    oi = P.origin_info(D, o)
    yfull = P.series(D, 'g', oi['w']).loc[:o - 1]
    fb, fa = P.direct_forecast(yfull, ci, o, H, k, D['qn'](START))
    return fb, fa


def ar2_residual_quantile(D, o, q=0.1):
    """Empirical q-quantile of the locked AR(2)'s in-sample residuals at origin o (plan Section 6, item 3)."""
    oi = P.origin_info(D, o)
    yfull = P.series(D, 'g', oi['w']).loc[:o - 1]
    js = np.arange(D['qn'](START), o - 1 - H + 1)
    Yt, A, _ = P.direct_rows(yfull, None, js, H, oi['k'])
    ok = np.isfinite(Yt) & np.isfinite(A).all(1)
    b = P.ols(A[ok], Yt[ok])
    return float(np.quantile(Yt[ok] - A[ok] @ b, q))


def revision_sd(D):
    """SD of GDP growth revisions, first release (early-estimate target) to the 2026Q3 vintage, over the
    locked target quarters 2000Q3-2019Q4. Used for the L1 perturbation and the L2 placebo noise."""
    qn = D['qn']; s = range(qn('2000Q3'), qn('2019Q4') + 1)
    d = np.array([P.target(D, 'g', t, 'revised') - P.target(D, 'g', t, 'early') for t in s])
    return float(np.nanstd(d, ddof=1))
