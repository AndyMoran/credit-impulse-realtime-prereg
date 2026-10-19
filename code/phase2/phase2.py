"""
Phase 2 analysis: real-time credit and macro forecasting, 1999Q3-2018Q4 (h=4).
Every specification element cites the protocol v2.3 section that defines it.

Modes
  synthetic : targets, SPF and yields replaced by simulated series (test_phase2.py). Credit is real.
  real      : refuses to run unless LOCK.json exists with the public release URL, tag commit and DOI.
"""
import os, sys, json, contextlib, io, functools
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = os.path.join(HERE, '..', 'p1')
sys.path.insert(0, P1)
from fixedb import nw_t                                     # Bartlett-kernel NW t-statistic

# ---------------------------------------------------------------- constants (protocol section)
H_PRIMARY = 4                                               # §5 horizon
HORIZONS = (1, 2, 4)                                        # §5
NL = 4                                                      # §8 credit lags j = 0..3
LAST_TARGET = None                                          # set from qn('2019Q4'); §5 COVID exclusion s <= 2019Q4
ALPHA = 0.05                                                # §4 Holm level
BOOT_B, BOOT_BLOCK = 2000, 4                                # §12 block bootstrap
FB_DRAWS, FB_N = 20000, 2000                                # fixed-b null simulation (Entry 13)
SEED = 20261019

# ---------------------------------------------------------------- data
def load(mode='synthetic'):
    if mode == 'real':
        lock = os.path.join(HERE, 'LOCK.json')
        if not os.path.exists(lock):
            raise SystemExit('Real mode refused: LOCK.json (release URL, tag commit, DOI) not found. Lock first.')
        L = json.load(open(lock))
        for k in ('release_url', 'tag_commit', 'doi'):
            if not L.get(k): raise SystemExit(f'Real mode refused: LOCK.json missing {k}.')
    g = {}
    cwd = os.getcwd(); os.chdir(P1)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('build.py').read(), g)
    os.chdir(cwd)
    qn, qs = g['qn'], g['qs']
    global LAST_TARGET; LAST_TARGET = qn('2019Q4')
    D = dict(Z=g['Z'], rel={k: pd.Timestamp(v) for k, v in g['rel'].items()}, zv=g['zv'],
             NO=g['NO'], P=g['P'], RO=g['RO'], RU=g['RU'], qn=qn, qs=qs,
             measures=g['measures'], hp_trend=g['hp_trend'], LATEST=g['LATEST'])
    D['LATEST_RU'] = max(D['RU'])
    # SPF (§8 SPF alignment); deadlines from the Phase 0 release-dates map (G4)
    spfdir = os.path.join(P1, 'data', 'spf')
    gr = pd.read_excel(os.path.join(spfdir, 'medianGrowth.xlsx'), sheet_name='RGDP')
    lv = pd.read_excel(os.path.join(spfdir, 'medianLevel.xlsx'), sheet_name='UNEMP')
    gr['t'] = gr.YEAR * 4 + gr.QUARTER - 1; lv['t'] = lv.YEAR * 4 + lv.QUARTER - 1
    D['SPF_G'] = gr.set_index('t').drgdp6.astype(float)
    D['SPF_U'] = lv.set_index('t').UNEMP6.astype(float)
    D['SPF_MICRO'] = os.path.join(spfdir, 'SPFmicrodata.xlsx')
    dl = pd.read_csv(os.path.join(HERE, '..', 'phase0', 'spf_deadlines_z1_map.csv'))
    D['DEADLINE'] = {qn(r.spf_survey): pd.Timestamp(r.deadline) for r in dl.itertuples()}
    gs2 = os.path.join(P1, 'data', 'GS2.csv')                  # FRED 2-year Treasury, monthly (S4); not revised
    if os.path.exists(gs2):
        m = pd.read_csv(gs2); m.columns = ['date', 'GS2']; m['date'] = pd.to_datetime(m.date)
        m['t'] = m.date.dt.year * 4 + (m.date.dt.month - 1) // 3; gq = m.groupby('t').GS2
        D['GS2'] = gq.mean()[gq.count() == 3]
    D['mode'] = mode
    return D

def vint(t):                                    # §6: origin date = RTDSM vintage date for quarter t (middle month, 15th)
    return pd.Timestamp(t // 4, 3 * (t % 4) + 2, 15)

def growth(level):                              # §5: 100*[(Y_s/Y_{s-1})^4 - 1]
    return 100 * ((level / level.shift(1)) ** 4 - 1)

def z1_before(D, date):                         # §6 credit availability: latest Z.1 release dated before `date`
    prior = [v for v in D['zv'] if D['rel'][v] < date]
    return prior[-1]

def series(D, var, w):                          # target variable as published in RTDSM vintage w
    if var == 'g': return growth(D['RO'][w])
    if var == 'u': return D['RU'][w]
    raise ValueError(var)

def target(D, var, s, kind):                    # §5 revised / early-estimate targets
    if kind == 'revised':
        w = D['LATEST'] if var == 'g' else D['LATEST_RU']
    else:                                       # early: RTDSM vintage dated quarter s+2
        w = vint(s + 2)
    return series(D, var, w).get(s, np.nan)

@functools.lru_cache(maxsize=None)
def _credit_cached(key):
    D, v, w, which, gap = _CACHE_CTX[key]
    z = D['Z'][v] if which != 'current' else D['Z']['current']
    nom = D['NO'][w]; pr = D['P'][w]
    return D['measures'](z, nom, pr, gap=gap)
_CACHE_CTX = {}
def credit(D, v, w, which='rt', gap=False):
    """§7 credit measures. which='rt': Z.1 vintage v; 'credrev': current Z.1, denominator from w (S1);
       'totrev': current Z.1 and latest GDP vintage (secondary decomposition, §2)."""
    if which == 'totrev': w = D['LATEST']
    key = (id(D), v if which == 'rt' else 'current', w, 'current' if which != 'rt' else 'rt', gap)
    _CACHE_CTX[key] = (D, v, w, 'current' if which != 'rt' else 'rt', gap)
    return _credit_cached(key)

def origin_info(D, o):                          # §6 origin-release table row
    od = vint(o); v = z1_before(D, od); qstar = D['Z'][v].index.max()
    return dict(o=o, date=od, v=v, qstar=qstar, k=o - qstar, w=od)

# ---------------------------------------------------------------- estimation (§8)
def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None); return b

def direct_rows(y, X, js, h, k, nl=NL):
    """Direct design: target y_{j+h}; regressors 1, y_{j-1}, y_{j-2}; credit X_{j-k-l}, l=0..nl-1 (§8)."""
    Yt = np.array([y.get(j + h, np.nan) for j in js])
    A = np.column_stack([np.ones(len(js)), [y.get(j - 1, np.nan) for j in js], [y.get(j - 2, np.nan) for j in js]])
    if X is None: C = np.zeros((len(js), 0))
    else:
        cols = X if isinstance(X, (list, tuple)) else [X]
        C = np.column_stack([[x.get(j - k - l, np.nan) for j in js] for x in cols for l in range(nl)])
    return Yt, A, C

def direct_forecast(y, X, o, h, k, start, window=None, nl=NL):
    """Forecast y_{o+h} at origin o. Training rows j: start <= j and j+h <= o-1 (targets published by the origin).
       Returns (AR(2) forecast, ADL forecast)."""
    j1 = o - 1 - h
    j0 = start if window is None else max(start, j1 - window + 1)
    js = np.arange(j0, j1 + 1)
    Yt, A, C = direct_rows(y, X, js, h, k, nl)
    ok = np.isfinite(Yt) & np.isfinite(A).all(1) & np.isfinite(C).all(1)
    _, a, c = direct_rows(y, X, np.array([o]), h, k, nl)
    fb = a[0] @ ols(A[ok], Yt[ok])
    if C.shape[1] == 0: return fb, fb
    Xa = np.column_stack([A, C]); fa = np.r_[a[0], c[0]] @ ols(Xa[ok], Yt[ok])
    return fb, fa

def reference_benchmarks(y, o, h, start):       # §8 benchmarks: RW, 8-quarter mean, AR(1), AR(2) (reference only)
    js = np.arange(start, o - 1 - h + 1)
    Yt = np.array([y.get(j + h, np.nan) for j in js]); y1 = np.array([y.get(j - 1, np.nan) for j in js])
    ok = np.isfinite(Yt) & np.isfinite(y1)
    ar1 = np.r_[1, y[o - 1]] @ ols(np.column_stack([np.ones(ok.sum()), y1[ok]]), Yt[ok])
    return dict(RW=y[o - 1], MEAN8=np.mean([y[o - i] for i in range(1, 9)]), AR1=ar1)

# ---------------------------------------------------------------- inference (§11, §12; Entry 13 fixed-b)
@functools.lru_cache(maxsize=None)
def fixedb_null(n, lags, two_sided):
    L = int(round((lags + 1) / n * FB_N)) - 1
    rng = np.random.default_rng(SEED + 7 * n + lags)
    t = np.array([nw_t(rng.standard_normal(FB_N), L) for _ in range(FB_DRAWS)])
    return np.sort(np.abs(t) if two_sided else t)

def p_fixedb(t, n, lags, two_sided):
    nd = fixedb_null(n, lags, two_sided)
    return 1 - np.searchsorted(nd, abs(t) if two_sided else t) / len(nd)

def clark_west(y, fb, fa, h):                   # §4: CW, one-sided, NW HAC h-1 lags, fixed-b
    y, fb, fa = map(np.asarray, (y, fb, fa))
    f = (y - fb) ** 2 - ((y - fa) ** 2 - (fb - fa) ** 2)
    lags = max(h - 1, 0); t = nw_t(f, lags) if lags > 0 else f.mean() / (f.std(ddof=1) / np.sqrt(len(f)))
    p = p_fixedb(t, len(f), lags, False) if lags > 0 else 1 - __import__('scipy.stats', fromlist=['t']).t.cdf(t, len(f) - 1)
    return dict(n=len(f), cw_t=t, p=p, ratio=np.sqrt(np.mean((y - fa) ** 2) / np.mean((y - fb) ** 2)))

def hac_ols(X, y, lags):                        # Bartlett HAC for OLS coefficients
    b = ols(X, y); e = y - X @ b; XtXi = np.linalg.inv(X.T @ X); z = X * e[:, None]; S = z.T @ z
    for l in range(1, lags + 1):
        G = z[l:].T @ z[:-l]; S += (1 - l / (lags + 1)) * (G + G.T)
    return b, np.sqrt(np.diag(XtXi @ S @ XtXi))

def holm(p, alpha=ALPHA):
    rej = {k: False for k in p}
    for i, k in enumerate(sorted(p, key=p.get)):
        if p[k] <= alpha / (len(p) - i): rej[k] = True
        else: break
    return rej

def block_boot_idx(n, rng, block=BOOT_BLOCK):
    starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
    return np.concatenate([np.arange(s, s + block) for s in starts])[:n]

def boot_interval(stat_fn, n, level=0.90, B=BOOT_B, seed=SEED):
    rng = np.random.default_rng(seed); vals = np.array([stat_fn(block_boot_idx(n, rng)) for _ in range(B)])
    a = (1 - level) / 2; return np.quantile(vals, [a, 1 - a])

def rmse_ratio(y, fb, fa, idx=None):
    y, fb, fa = map(np.asarray, (y, fb, fa))
    if idx is not None: y, fb, fa = y[idx], fb[idx], fa[idx]
    return np.sqrt(np.mean((y - fa) ** 2) / np.mean((y - fb) ** 2))

def crisis_share(d, a, b):
    """§13 descriptive (Entry 19): share of the total squared-error gain (benchmark minus credit model) that comes
       from origins in [a, b]. Reported with the signed total so a negative total is not misread."""
    gain = (d.y - d.fb) ** 2 - (d.y - d.fa) ** 2; tot = gain.sum(); win = gain[(d.o >= a) & (d.o <= b)].sum()
    return dict(total_gain=float(tot), window_gain=float(win), share=float(win / tot) if tot != 0 else float('nan'))

# ---------------------------------------------------------------- P1: direct AR(2) vs ADL (§4, §8)
def run_p1(D, var, origins, h=H_PRIMARY, measure='CI', which='rt', target_kind='revised',
           window=None, start=None, extra=None):
    """Forecast table for P1 at each origin. measure: CI, CG, GAP, RCG, CI_lev, or callable (S5).
       which: 'rt' | 'credrev' | 'totrev' credit version (§2 grid, S1)."""
    start = start or D['qn']('1965Q1')
    rows = []
    for o in origins:
        s = o + h
        if s > LAST_TARGET: continue                        # §5 COVID exclusion by target quarter
        oi = origin_info(D, o)
        y = series(D, var, oi['w']).loc[:o - 1]              # observed through o-1 in the origin vintage (§6)
        need_gap = (measure == 'GAP')
        cm = credit(D, oi['v'], oi['w'], which, gap=need_gap)
        if which != 'rt': cm = cm.loc[:oi['qstar']]          # same release-time edge as real time (§6 primary)
        X = measure(cm) if callable(measure) else cm[measure]
        if extra is not None: X = extra(D, oi, cm)           # robustness Y/Z imputation (§6)
        k = oi['k'] if extra is None else 1
        fb, fa = direct_forecast(y, X, o, h, k, start, window)
        rows.append(dict(o=o, s=s, k=oi['k'], fb=fb, fa=fa, y=target(D, var, s, target_kind)))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- P2: SPF counterfactual (§8 SPF alignment)
def spf_series(D, var, robust=False):
    if var == 'g' and robust: return D['SPF_MICRO_SERIES'] if 'SPF_MICRO_SERIES' in D else spf_micro_growth(D)
    return D['SPF_G'] if var == 'g' else D['SPF_U']

@functools.lru_cache(maxsize=1)
def _micro(path):
    m = pd.read_excel(path, sheet_name='RGDP'); m['t'] = m.YEAR * 4 + m.QUARTER - 1
    m['g6'] = 100 * ((m.RGDP6 / m.RGDP5) ** 4 - 1)          # each forecaster's own implied growth (§8 robustness)
    return m.groupby('t').g6.median()
def spf_micro_growth(D): return _micro(D['SPF_MICRO'])

def run_p2(D, var, origins, robust=False, target_kind='revised'):
    """Corrected (SPF + a + b*CI_{q*}) vs bias-corrected (SPF + a). Training: surveys j >= 1990Q3 with
       target j+4 published by the deadline (j+4 <= o-1), errors from values as published at d_o; >= 20 pairs."""
    h = 4; spf = spf_series(D, var, robust); j0 = D['qn']('1990Q3'); rows = []
    for o in origins:
        s = o + h
        if s > LAST_TARGET or o not in D['DEADLINE']: continue
        d = D['DEADLINE'][o]; v = z1_before(D, d); qstar = D['Z'][v].index.max(); k = o - qstar
        w = vint(o)                                          # values as published at d_o (vintage of survey quarter)
        y = series(D, var, w); cm = credit(D, v, w, 'rt'); ci = cm['CI']
        js = [j for j in range(j0, o - h) if j in spf.index and np.isfinite(spf[j])]
        e = np.array([y.get(j + h, np.nan) - spf[j] for j in js]); c = np.array([ci.get(j - k, np.nan) for j in js])
        ok = np.isfinite(e) & np.isfinite(c)
        if ok.sum() < 20: continue                           # §8: at least 20 training pairs
        a_b = e[ok].mean()
        b = ols(np.column_stack([np.ones(ok.sum()), c[ok]]), e[ok])
        f0 = spf[o]
        rows.append(dict(o=o, s=s, k=k, n_train=int(ok.sum()), spf=f0, fb=f0 + a_b, fa=f0 + b[0] + b[1] * ci[qstar],
                         y=target(D, var, s, target_kind)))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- P3: revision regression (§9)
def advance_anchor(s):
    """Anchor a_s = release of the advance estimate for s (end of month 1 of s+1). Day 28 is used: no Z.1 release
       in 1999-2019 falls in days 25-31 of the first month of a quarter, so the Z.1 selected is unaffected."""
    t = s + 1; return pd.Timestamp(t // 4, 3 * (t % 4) + 1, 28)

def run_p3(D, quarters):
    rows = []
    for s in quarters:
        a = advance_anchor(s); v = z1_before(D, a); qstar = D['Z'][v].index.max()
        w_adv = vint(s + 1)                                  # first RTDSM vintage containing the advance estimate of s
        g_adv = series(D, 'g', w_adv)
        if not np.isfinite(g_adv.get(s, np.nan)): continue
        ci = credit(D, v, w_adv, 'rt')['CI']
        rows.append(dict(s=s, qstar=qstar, CI=ci[qstar], g_adv=g_adv[s], g_lag=g_adv[s - 1],
                         R=target(D, 'g', s, 'revised') - g_adv[s]))
    df = pd.DataFrame(rows)
    X = np.column_stack([np.ones(len(df)), df.CI, df.g_adv, df.g_lag]); y = df.R.values; b, se = hac_ols(X, y, 4)
    t = b[1] / se[1]; n = len(df)
    tb = wild_block_t(X, y, 1)                                        # §9 as amended (Entry 19)
    p = float(np.mean(np.abs(tb) >= abs(t))); q90 = np.quantile(np.abs(tb), 0.90)
    return df, dict(n=n, beta_CI=b[1], se=se[1], t=t, p=p, ci90=(b[1] - q90 * se[1], b[1] + q90 * se[1]),
                    p_fixedb_hac=p_fixedb(t, n, 4, True))

def wild_block_t(X, y, j, B=999, block=4, lags=4, seed=SEED):
    """Restricted wild (Rademacher) block bootstrap of the HAC t-statistic for coefficient j under H0: b_j = 0."""
    keep = [c for c in range(X.shape[1]) if c != j]; X0 = X[:, keep]; f0 = X0 @ ols(X0, y); e0 = y - f0
    rng = np.random.default_rng(seed); n = len(y); nb = int(np.ceil(n / block)); out = np.empty(B)
    for i in range(B):
        v = np.repeat(rng.choice([-1.0, 1.0], nb), block)[:n]; bb, sb = hac_ols(X, f0 + e0 * v, lags); out[i] = bb[j] / sb[j]
    return out

# ---------------------------------------------------------------- robustness Y / Z: ragged-edge fill (§6)
def impute_Y(D, oi, cm):
    """AR(4) on the 4-quarter flow S_t alone, estimated on vintage v up to q*; fill q*+1..o-1; recompute CI.
       Models then use calendar lags ending at o-1 (k=1)."""
    z = D['Z'][oi['v']]; S = z.F.rolling(4).sum().dropna(); q = oi['qstar']
    Y = S.values; X = np.column_stack([np.ones(len(Y) - 4)] + [Y[4 - l:len(Y) - l] for l in range(1, 5)])
    b = ols(X, Y[4:]); ext = list(Y)
    for _ in range(oi['o'] - 1 - q): ext.append(np.r_[1, ext[-1], ext[-2], ext[-3], ext[-4]] @ b)
    Sx = pd.Series(ext, index=np.arange(S.index[0], S.index[0] + len(ext)))
    return _ci_from_S(D, Sx, oi)

def impute_Z(D, oi, cm):
    """VAR(2) on household and business flows (credit only), forecast q*+1..o-1 (Kalman forecast of the
       state-space form equals the iterated VAR forecast when no in-sample observation is missing)."""
    z = D['Z'][oi['v']]; Fm = z[['Fhh', 'Fnfb']].dropna().values; q = oi['qstar']
    Yv = Fm[2:]; Xv = np.column_stack([np.ones(len(Yv)), Fm[1:-1], Fm[:-2]]); B = ols(Xv, Yv)
    ext = [r for r in Fm]
    for _ in range(oi['o'] - 1 - q): ext.append(np.r_[1, ext[-1], ext[-2]] @ B)
    F = pd.Series(np.array(ext).sum(1), index=np.arange(z.index[-len(Fm)], z.index[-len(Fm)] + len(ext)))
    return _ci_from_S(D, F.rolling(4).sum(), oi)

def _ci_from_S(D, S, oi):
    nom = D['NO'][oi['w']]; N4 = (nom / 4).rolling(4).sum()
    return 100 * (S - S.shift(4)) / N4.reindex(S.index)

# ---------------------------------------------------------------- S5 measures (§7, §8)
def ci_pos(cm): return [cm.CI.clip(lower=0), cm.CI.clip(upper=0)]           # asymmetric ADL: CI+ and CI-
def contraction(cm):                                                          # RCG and RCG x 1(RCG<0)
    return [cm.RCG, cm.RCG * (cm.RCG < 0)]

# ---------------------------------------------------------------- D1 threshold signals (§10)
def d1_signals(D, origins, which='rt'):
    rows = []
    for o in origins:
        oi = origin_info(D, o); cm = credit(D, oi['v'], oi['w'], which).loc[:oi['qstar']]
        q = oi['qstar']; nom = D['NO'][oi['w']]
        s1 = (cm.CI.get(q, np.nan) < 0) and (cm.CI.get(q - 1, np.nan) < 0)
        ngr = 100 * (nom.get(q, np.nan) / nom.get(q - 4, np.nan) - 1)
        s2 = cm.CG.get(q, np.nan) < ngr
        rows.append(dict(o=o, sig_ci=bool(s1), sig_cg=bool(s2)))
    return pd.DataFrame(rows)

def d1_episodes(sig, origins, peaks):
    on = dict(zip(origins, sig)); eps = []; o = origins[0]
    while o <= origins[-1]:
        if on.get(o):
            st = o
            while on.get(o) or (on.get(o + 1) and not on.get(o)): o += 1   # merge single-quarter gaps
            eps.append((st, o - 1))
        o += 1
    out = []
    for st, en in eps:
        lab = 'false alarm'
        for p, tr in peaks:
            if 1 <= p - st <= 6: lab = 'hit'; break
            if p <= st <= tr: lab = 'late'; break
        out.append(dict(start=st, end=en, label=lab, lead=[p - st for p, _ in peaks if 1 <= p - st <= 6]))
    miss = [p for p, _ in peaks if not any(1 <= p - e['start'] <= 6 for e in out) and p >= origins[0] + 6]
    return pd.DataFrame(out), miss, float(np.mean(sig))

# ---------------------------------------------------------------- E2 revision paths (descriptive; Entry 14)
def e2_revision_paths(D, threshold=0.25):
    rev = D['measures'](D['Z']['current'], D['NO'][D['LATEST']], D['P'][D['LATEST']], gap=False).CI
    sd = rev.std(); prev = None; out = []
    for v in D['zv']:
        w = max(d for d in D['NO'] if d < D['rel'][v]); ci = D['measures'](D['Z'][v], D['NO'][w], D['P'][w], gap=False).CI
        if prev is not None:
            q = D['Z'][v].index.max(); old = [t for t in ci.index if t <= q - 12 and t in prev.index]
            med = np.nanmedian(np.abs(ci[old] - prev[old])); out.append(dict(v=v, med_old_rev=med, benchmark=med > threshold * sd))
        prev = ci
    return pd.DataFrame(out)


# ---------------------------------------------------------------- S4: Minnesota BVAR, 1A vs 1B (§8)
BVAR = dict(tight=0.2, cross=0.5, decay=2.0, lags=2)
def _minnesota_fit(Y, p, own_rw, hp=BVAR):
    """Equation-by-equation posterior mean under a Minnesota prior with fixed residual scale (AR(4) residual SDs)."""
    T_, n = Y.shape; sig = np.zeros(n)
    for i in range(n):
        y = Y[4:, i]; X = np.column_stack([np.ones(T_ - 4)] + [Y[4 - l:T_ - l, i] for l in range(1, 5)])
        e = y - X @ ols(X, y); sig[i] = e.std()
    X = np.column_stack([np.ones(T_ - p)] + [Y[p - l:T_ - l] for l in range(1, p + 1)])
    B = np.zeros((1 + n * p, n))
    for i in range(n):
        b0 = np.zeros(1 + n * p); v = np.zeros(1 + n * p); v[0] = 1e6
        if own_rw[i]: b0[1 + i] = 1.0
        for l in range(1, p + 1):
            for j in range(n):
                sd = hp['tight'] / l ** hp['decay'] * (1 if i == j else hp['cross'] * sig[i] / sig[j])
                v[1 + (l - 1) * n + j] = sd ** 2
        A = X.T @ X / sig[i] ** 2 + np.diag(1 / v); B[:, i] = np.linalg.solve(A, X.T @ Y[p:, i] / sig[i] ** 2 + b0 / v)
    return B
def _bvar_forecast(Y, B, p, h):
    hist = [r for r in Y[-p:]]
    for _ in range(h): hist.append(np.r_[1, np.concatenate([hist[-l] for l in range(1, p + 1)])] @ B)
    return hist[-1]
def run_s4(D, origins, h=4):
    """1A: g, deflator inflation, u, 2-year yield; 1B adds CI_{t-2} (credit as published). Data through o-1."""
    y2 = D['GS2']; rows = []
    for o in origins:
        s = o + h
        if s > LAST_TARGET: continue
        oi = origin_info(D, o); w = oi['w']
        g = series(D, 'g', w); infl = growth(D['P'][w]); u = series(D, 'u', w)
        ci = credit(D, oi['v'], w, 'rt')['CI']
        if oi['k'] > 2: ci = impute_Y(D, oi, None)               # §8: fill only when k_o > 2
        t0 = max(y2.index.min(), D['qn']('1976Q3')); idx = np.arange(t0, o)
        A = np.column_stack([g.reindex(idx), infl.reindex(idx), u.reindex(idx), y2.reindex(idx)])
        Bm = np.column_stack([A, ci.reindex(idx - 2)])
        ok = np.isfinite(Bm).all(1); A, Bm = A[ok], Bm[ok]
        fa = _bvar_forecast(A, _minnesota_fit(A, 2, [0, 0, 1, 1]), 2, h + 1)   # o-1 -> o+h is h+1 steps
        fb = _bvar_forecast(Bm, _minnesota_fit(Bm, 2, [0, 0, 1, 1, 0]), 2, h + 1)
        rows.append(dict(o=o, s=s, g_1A=fa[0], g_1B=fb[0], u_1A=fa[2], u_1B=fb[2],
                         y_g=target(D, 'g', s, 'revised'), y_u=target(D, 'u', s, 'revised')))
    return pd.DataFrame(rows)
def hln_dm(y, f1, f2, h, B=BOOT_B):
    """HLN-corrected Diebold-Mariano (1B vs 1A, one-sided: 1B better) with a block-bootstrap p-value (§8, S4)."""
    from scipy import stats
    d = (np.asarray(y) - f1) ** 2 - (np.asarray(y) - f2) ** 2; n = len(d)
    t = nw_t(d, h - 1) * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    rng = np.random.default_rng(SEED); dc = d - d.mean()
    tb = np.array([dc[block_boot_idx(n, rng)].mean() for _ in range(B)])
    return dict(n=n, hln_t=t, p_t=1 - stats.t.cdf(t, n - 1), p_boot=float(np.mean(tb >= d.mean())),
                ratio=np.sqrt(np.mean((np.asarray(y) - f2) ** 2) / np.mean((np.asarray(y) - f1) ** 2)))

# ---------------------------------------------------------------- E1: Markov-switching replication (§8)
def run_e1(D, origins, h=4):
    """Operationalisation (to be confirmed at lock): two-regime Markov-switching regression of the change in
       unemployment on a switching intercept and variance, with real credit growth at its release lag as a
       non-switching regressor; estimated at each origin on data through o-1; the FILTERED probability of the
       rising-unemployment regime at o-1 is added to the direct AR(2) for u_{o+h}. Origins from 2000Q1."""
    import warnings; from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    rows = []
    for o in origins:
        s = o + h
        if s > LAST_TARGET or o < D['qn']('2000Q1'): continue
        oi = origin_info(D, o); u = series(D, 'u', oi['w']).loc[:o - 1]
        rcg = credit(D, oi['v'], oi['w'], 'rt')['RCG']; k = oi['k']
        idx = np.arange(D['qn']('1965Q1'), o); du = u.diff().reindex(idx); x = pd.Series(rcg.reindex(idx - k).values, index=idx)   # aligned on t, value from t-k
        ok = du.notna() & x.notna()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m = MarkovRegression(du[ok].values, k_regimes=2, exog=x[ok].values[:, None], switching_exog=False,
                                 switching_variance=True).fit(disp=False)
        pn = list(m.model.param_names); hi = int(np.argmax([m.params[pn.index(f'const[{r}]')] for r in range(2)]))
        prob = pd.Series(m.filtered_marginal_probabilities[:, hi], index=idx[ok.values])
        fb, fa = direct_forecast(u, prob, o, h, 1, D['qn']('1966Q1'), nl=1)
        rows.append(dict(o=o, s=s, fb=fb, fa=fa, y=target(D, 'u', s, 'revised')))
    return pd.DataFrame(rows)

# ---------------------------------------------------------------- the confirmatory core and everything else
def run_all(D, outdir):
    qn, qs = D['qn'], D['qs']; os.makedirs(outdir, exist_ok=True)
    O = list(range(qn('1999Q3'), qn('2018Q4') + 1))                 # §3 sample-start decision: 78 origins at h=4
    res = {}
    # ---- confirmatory core
    p1a = run_p1(D, 'g', O); p1b = run_p1(D, 'u', O); p2a = run_p2(D, 'g', O)
    p3df, p3 = run_p3(D, list(range(qn('1999Q2'), qn('2019Q4') + 1)))
    core = {'P1a': clark_west(p1a.y, p1a.fb, p1a.fa, 4), 'P1b': clark_west(p1b.y, p1b.fb, p1b.fa, 4),
            'P2a': clark_west(p2a.y, p2a.fb, p2a.fa, 4), 'P3': p3}
    rej = holm({k: v['p'] for k, v in core.items()})
    bands = {k: 'estimate_only' for k in core}                       # §11 bands from conditional-path power (Entry 19)
    for k, d in (('P1a', p1a), ('P1b', p1b), ('P2a', p2a)):          # §11 <0.50 band: 'credible improvement' rule
        lo, hi = boot_interval(lambda idx, a=d: rmse_ratio(a.y, a.fb, a.fa, idx), len(d))
        core[k].update(ratio_ci90=(lo, hi), credible_improvement=bool(hi < 1.0),
                       crisis_share=crisis_share(d, qn('2007Q1'), qn('2010Q4')))
    core['P3'].update(credible_effect=bool(core['P3']['ci90'][0] > 0 or core['P3']['ci90'][1] < 0))
    for k in core: core[k].update(holm_reject=rej[k], band=bands[k])
    res['core'] = core
    for name, df in [('P1a', p1a), ('P1b', p1b), ('P2a', p2a), ('P3', p3df)]: df.to_csv(f'{outdir}/{name}_forecasts.csv', index=False)
    # ---- grid (§2) and S1 premium
    grid = {}
    for var in ('g', 'u'):
        rt_rev = run_p1(D, var, O); rt_early = run_p1(D, var, O, target_kind='early')
        cr = run_p1(D, var, O, which='credrev'); tr = run_p1(D, var, O, which='totrev')
        grid[var] = dict(rt_revised=rmse_ratio(rt_rev.y, rt_rev.fb, rt_rev.fa),
                         rt_early=rmse_ratio(rt_early.y, rt_early.fb, rt_early.fa),
                         totrev_revised=rmse_ratio(tr.y, tr.fb, tr.fa))
        n = len(rt_rev)
        prem = lambda idx, a=rt_rev, b=cr: rmse_ratio(a.y, a.fb, a.fa, idx) - rmse_ratio(b.y, b.fb, b.fa, idx)
        totp = lambda idx, a=rt_rev, b=tr: rmse_ratio(a.y, a.fb, a.fa, idx) - rmse_ratio(b.y, b.fb, b.fa, idx)
        grid[var].update(credit_revision_premium=prem(None), premium_ci90=tuple(boot_interval(prem, n)),
                         total_premium=totp(None), total_premium_ci90=tuple(boot_interval(totp, n)))
        prem_val, lo_hi = grid[var]['credit_revision_premium'], grid[var]['premium_ci90']
        grid[var]['premium_size'] = 'large' if (abs(prem_val) >= 0.05 and (lo_hi[0] > 0 or lo_hi[1] < 0)) else 'small'
        # interval for the primary cell ratio (estimation-only language, §11)
        grid[var]['rt_revised_ci90'] = tuple(boot_interval(lambda idx, a=rt_rev: rmse_ratio(a.y, a.fb, a.fa, idx), n))
    res['grid'] = grid
    # ---- exploratory
    ex = {}
    ex['P2b'] = clark_west(*(lambda d: (d.y, d.fb, d.fa))(run_p2(D, 'u', O)), 4)
    ex['P2a_micro'] = clark_west(*(lambda d: (d.y, d.fb, d.fa))(run_p2(D, 'g', O, robust=True)), 4)
    for m in ('CG', 'GAP', 'RCG', 'CI_lev'):                         # S2 horse race (+ stock-difference CI robustness)
        for var in ('g', 'u'):
            d = run_p1(D, var, O, measure=m); ex[f'S2_{m}_{var}'] = clark_west(d.y, d.fb, d.fa, 4)
    for var in ('g', 'u'):                                           # S5
        d = run_p1(D, var, O, measure=ci_pos); ex[f'S5_asym_{var}'] = clark_west(d.y, d.fb, d.fa, 4)
        d = run_p1(D, var, O, measure=contraction); ex[f'S5_contraction_{var}'] = clark_west(d.y, d.fb, d.fa, 4)
        d = run_p1(D, var, O); split = qn('2008Q3')                  # S6
        for lab, m in (('pre', d.o <= split), ('post', d.o > split)):
            dd = d[m].reset_index(drop=True)
            ex[f'S6_{lab}_{var}'] = dict(ratio=rmse_ratio(dd.y, dd.fb, dd.fa),
                                         ci90=tuple(boot_interval(lambda idx, a=dd: rmse_ratio(a.y, a.fb, a.fa, idx), len(dd))))
        for lab, fn in (('Y', impute_Y), ('Z', impute_Z)):           # R1 robustness
            d = run_p1(D, var, O, extra=fn); ex[f'R1_{lab}_{var}'] = clark_west(d.y, d.fb, d.fa, 4)
        d = run_p1(D, var, O, window=60); ex[f'rolling60_{var}'] = clark_west(d.y, d.fb, d.fa, 4)
        for h in (1, 2):                                             # secondary horizons (§5)
            Oh = list(range(qn('1999Q3'), LAST_TARGET - h + 1))
            d = run_p1(D, var, Oh, h=h); ex[f'h{h}_{var}'] = clark_west(d.y, d.fb, d.fa, h)
    # direction metric for unemployment (§5)
    d = run_p1(D, 'u', O); base = np.array([series(D, 'u', vint(o)).get(o - 1) for o in d.o])
    act = d.y.values - base; keep = np.abs(act) >= 0.05
    ex['P1b_direction'] = dict(ar2=np.mean(np.sign(d.fb.values - base)[keep] == np.sign(act)[keep]),
                               adl=np.mean(np.sign(d.fa.values - base)[keep] == np.sign(act)[keep]), n=int(keep.sum()))
    s4 = run_s4(D, O); s4.to_csv(f'{outdir}/S4_forecasts.csv', index=False)
    for var in ('g', 'u'): ex[f'S4_{var}'] = hln_dm(s4[f'y_{var}'].values, s4[f'{var}_1A'].values, s4[f'{var}_1B'].values, 4)
    e1 = run_e1(D, O); e1.to_csv(f'{outdir}/E1_forecasts.csv', index=False); ex['E1'] = clark_west(e1.y, e1.fb, e1.fa, 4)
    res['exploratory'] = ex
    # ---- descriptive
    peaks = [(qn('2001Q1'), qn('2001Q4')), (qn('2007Q4'), qn('2009Q2'))]
    d1 = {}
    for which in ('rt', 'totrev'):
        sig = d1_signals(D, O, which)
        for col in ('sig_ci', 'sig_cg'):
            eps, miss, share = d1_episodes(sig[col].tolist(), O, peaks)
            d1[f'{which}_{col}'] = dict(episodes=eps.to_dict('records'), misses=miss, share=share)
    res['D1'] = d1
    res['origin_table'] = [dict((k, (str(v) if k == 'date' else v)) for k, v in origin_info(D, o).items() if k != 'w') for o in O]
    json.dump(res, open(f'{outdir}/results.json', 'w'), indent=1, default=lambda x: float(x) if np.isscalar(x) else str(x))
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'synthetic'
    if mode != 'real': raise SystemExit('Use test_phase2.py for synthetic runs.')
    D = load('real'); run_all(D, os.path.join(HERE, 'results_real'))
