"""
Plan 2: direct forecasts at horizon h (plan2/PLAN.md, Section 4), built from the locked phase2 functions.

fit(y, blocks, o, h, start, models) estimates every requested model on ONE common row mask: the rows where the target
and every regressor in `blocks` are present. Each block is (X, k, nl): series X entering at release lag k with nl lags,
exactly as the locked direct_rows builds credit. Nested comparisons pass one block; the head-to-head (Q7) passes both
indicators, so both single-indicator models share rows. The gate checks that fit() with one credit block reproduces the
locked direct_forecast at h = 4 exactly.
"""
import numpy as np
import plan2_data as T
P = T.P


def rows(y, blocks, js, h):
    """Target, AR(2) design and one regressor matrix per block, from the locked direct_rows."""
    Yt, A, _ = P.direct_rows(y, None, js, h, 0)
    Cs = [P.direct_rows(y, X, js, h, k, nl)[2] for X, k, nl in blocks]
    return Yt, A, Cs


def fit(y, blocks, o, h, start, models=('ar', 'all')):
    """Forecasts of y_{o+h} at origin o. models: 'ar' (AR(2)), 'all' (AR(2) + every block), or an int b
    (AR(2) + block b only). Returns {model: forecast} and {model: coefficients}."""
    j1 = o - 1 - h; js = np.arange(start, j1 + 1)
    Yt, A, Cs = rows(y, blocks, js, h)
    ok = np.isfinite(Yt) & np.isfinite(A).all(1)
    for C in Cs: ok &= np.isfinite(C).all(1)
    _, a, cs = rows(y, blocks, np.array([o]), h)
    if not (np.isfinite(a).all() and all(np.isfinite(c).all() for c in cs)):
        raise ValueError(f'regressor missing at origin {o}')
    f, coef = {}, {}
    for m in models:
        use = [] if m == 'ar' else (list(range(len(blocks))) if m == 'all' else [m])
        X = np.column_stack([A] + [Cs[b] for b in use]); x = np.r_[a[0], *[cs[b][0] for b in use]]
        b = P.ols(X[ok], Yt[ok]); f[m] = float(x @ b); coef[m] = b
    return f, coef, int(ok.sum())


# ------------------------------------------------------------------ per-origin inputs for every comparison
def survey_block(D, s, o, kind):
    """(X, k, nl) for the survey under each Section 5 definition."""
    if kind == 'q1':                                     # first month of quarter j, lag 0
        M1, _, last = T.survey_quarterly(D, s, o); return (M1, 0, 1), last
    if kind == 'q4':                                     # first month of quarter j-2 (staleness-matched)
        M1, _, last = T.survey_quarterly(D, s, o); return (M1, 2, 1), last
    if kind == 'q5':                                     # third month of quarter j-1, cut at end of quarter o-1
        _, M3, last = T.survey_quarterly(D, s, o, cut=T.quarter_end(o - 1)); return (M3, 1, 1), last
    raise ValueError(kind)


def credit_block(D, o, which='rt'):
    ci, k = T.credit(D, o, which); return (ci, k, P.NL)
