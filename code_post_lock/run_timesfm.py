"""
TimesFM extension: the single real run (plan: timesfm/PLAN.md, Sections 4-6 and 8).

Modes
  pipeline-test OUTDIR : runs the whole pipeline on the real inputs with the stand-in 'dummy' back-end in every
                         model slot. No TimesFM model is loaded. Used to test the code before freezing.
  real                 : the single run. Refuses unless timesfm/PLAN_LOCK.json exists, and refuses if
                         timesfm/results/ already exists (one run only). Loads TimesFM 2.5 and, if the private
                         file is present, TimesFM 3.0.
"""
import os, sys, json, hashlib, datetime, platform
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tfm_data as T, tfm_models as M
P = T.P
EXT = os.path.join(T.P2, '..', 'timesfm')                    # plan, lock file and results live here
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
L1_DRAWS, L1_SEED = 20, 20261019
L1_EXCESS_ALL, L1_EXCESS_2010_11 = 0.10, 0.20   # plan Section 5, L1 flag thresholds
L2_DRAWS, L2_SEED, L2_SCALE = 50, 20261100, (0.8, 1.2)
CHECKPOINTS = {  # plan Section 2: exact revisions and weights hashes, fixed before freezing
    'tfm25': ('google/timesfm-2.5-200m-pytorch', '1d952420fba87f3c6dee4f240de0f1a0fbc790e3',
              '2f776efe6245e42b24bc4153ffdf61810140210e4bd3b01fb21f7aa779ab6ce8'),
    'tfm30': ('google/timesfm-3.0-pytorch', '43046b85ec22d584a13f8098c2ed39c889e129c2',
              'a7592b0a8432baee54483254e5647856911ce69e09d09a9bb65904b2d98f17da')}
EPISODE = ('2008Q1', '2012Q4'); TABLE_ORIGINS = ('2010Q1', '2011Q4'); TAIL_TARGETS = ('2008Q1', '2012Q4')


def build(D):
    rows = []
    for o in T.origins(D):
        y = T.gdp_context(D, o)
        fb, fa = T.locked_benchmark(D, o, y)
        rows.append(dict(o=o, y_ctx=y, outcome=T.outcome(D, o), ar2=fb, credit_model=fa,
                         ar2_q10=fb + T.ar2_residual_quantile(D, o, 0.1),
                         lags_rt=T.credit_lags_for_xreg(D, o, y, 'rt'), lags_rev=T.credit_lags_for_xreg(D, o, y, 'credrev'),
                         cov_rt=T.credit_aligned(D, o, y, 'rt'), cov_rev=T.credit_aligned(D, o, y, 'credrev')))
    return rows


def step5(res):  # median and 10th percentile of the fifth step (target o+4)
    return np.array([r['point'][4] for r in res]), np.array([r['q'][4, 0] for r in res])


def forecasts(rows, m25, m30):
    ys = [r['y_ctx'].values for r in rows]; F = {}
    F['tfm25'], F['tfm25_q10'] = step5(m25.forecast(ys))
    F['tfm25_cr_rt'], F['tfm25_cr_rt_q10'] = step5(m25.forecast_xreg(ys, [r['lags_rt'] for r in rows]))
    F['tfm25_cr_rev'], _ = step5(m25.forecast_xreg(ys, [r['lags_rev'] for r in rows]))
    if m30 is not None:
        F['tfm30'], F['tfm30_q10'] = step5(m30.forecast(ys))
        F['tfm30_cr_rt'], F['tfm30_cr_rt_q10'] = step5(m30.forecast_past_cov(ys, [r['cov_rt'] for r in rows]))
        F['tfm30_cr_rev'], _ = step5(m30.forecast_past_cov(ys, [r['cov_rev'] for r in rows]))
    return F


def compare(y, f_comp, f_model):
    n = len(y); r = P.rmse_ratio(y, f_comp, f_model)
    lo, hi = P.boot_interval(lambda i: P.rmse_ratio(y, f_comp, f_model, i), n)
    dm = P.hln_dm(y, f_comp, f_model, T.H)
    return dict(ratio=float(r), ci90=[float(lo), float(hi)], credible_improvement=bool(hi < 1),
                hln_t=float(dm['hln_t']), p_boot=float(dm['p_boot']))


def premium(y, base, f_rt, f_rev):
    """Locked convention: ratio with real-time credit minus ratio with revised credit; positive = revised better."""
    n = len(y); stat = lambda i=None: P.rmse_ratio(y, base, f_rt, i) - P.rmse_ratio(y, base, f_rev, i)
    lo, hi = P.boot_interval(stat, n); v = stat()
    return dict(premium=float(v), ci90=[float(lo), float(hi)],
                size='large' if (abs(v) >= 0.05 and (lo > 0 or hi < 0)) else 'small')


def pinball(y, q, tau=0.1):
    u = y - q; return float(np.mean(np.maximum(tau * u, (tau - 1) * u)))


def l1(D, rows, models, rsd):
    """Perturbation test (plan Section 5, L1)."""
    qn = D['qn']; O = np.array([r['o'] for r in rows]); y = np.array([r['outcome'] for r in rows])
    sub = (O >= qn(TABLE_ORIGINS[0])) & (O <= qn(TABLE_ORIGINS[1]))
    base = {'ar2': np.array([r['ar2'] for r in rows])}
    for name, m in models.items(): base[name] = step5(m.forecast([r['y_ctx'].values for r in rows]))[0]
    rmse = lambda f, s=slice(None): float(np.sqrt(np.mean((y[s] - f[s]) ** 2)))
    out = {k: dict(all=[], sub=[]) for k in base}
    lo_q, hi_q = qn('1947Q1'), qn('2019Q4')
    for k in range(1, L1_DRAWS + 1):
        rng = np.random.default_rng(L1_SEED + k); eps = pd.Series(rng.normal(0, rsd, hi_q - lo_q + 1), index=range(lo_q, hi_q + 1))
        ar = []
        for r in rows:
            o = r['o']; oi = P.origin_info(D, o)
            yfull = P.series(D, 'g', oi['w']).loc[:o - 1]; yp = yfull + eps.reindex(yfull.index).fillna(0)
            ar.append(P.direct_forecast(yp, None, o, T.H, oi['k'], qn(T.START))[0])
        pert = {'ar2': np.array(ar)}
        ctxs = [(r['y_ctx'] + eps.reindex(r['y_ctx'].index)).values for r in rows]
        for name, m in models.items(): pert[name] = step5(m.forecast(ctxs))[0]
        for name in base:
            out[name]['all'].append(rmse(pert[name])); out[name]['sub'].append(rmse(pert[name], sub))
    res = {name: dict(ratio_all=float(np.mean(out[name]['all']) / rmse(base[name])),
                      ratio_2010_11=float(np.mean(out[name]['sub']) / rmse(base[name], sub)),
                      unperturbed_rmse_all=rmse(base[name]), unperturbed_rmse_2010_11=rmse(base[name], sub),
                      draw_ratios_all=[float(v / rmse(base[name])) for v in out[name]['all']],
                      draw_ratios_2010_11=[float(v / rmse(base[name], sub)) for v in out[name]['sub']]) for name in base}
    for name in models:      # flag: TimesFM degrades by more than the AR(2), by the fixed margins (either window)
        ea = res[name]['ratio_all'] - res['ar2']['ratio_all']; es = res[name]['ratio_2010_11'] - res['ar2']['ratio_2010_11']
        res[name].update(excess_all=ea, excess_2010_11=es,
                         flag=bool(ea > L1_EXCESS_ALL or es > L1_EXCESS_2010_11))
    return res


def l2(D, models, rsd):
    """Shape-matched placebo (plan Section 5, L2), on the 2026Q3-vintage series."""
    qn = D['qn']; yrev = P.series(D, 'g', D['LATEST']); start = qn(T.START)
    e0, e1 = qn(EPISODE[0]), qn(EPISODE[1]); O = list(range(qn(TABLE_ORIGINS[0]), qn(TABLE_ORIGINS[1]) + 1))
    pre = yrev.loc[start - 2:e0 - 1]
    X = np.column_stack([np.ones(len(pre) - 2), pre.values[1:-1], pre.values[:-2]]); b, *_ = np.linalg.lstsq(X, pre.values[2:], rcond=None)
    s = np.std(pre.values[2:] - X @ b, ddof=3); actual = yrev.loc[e0:e1].values

    def ratios(series):
        tgt = np.array([series[o + T.H] for o in O])
        ar = np.array([P.direct_forecast(series.loc[:o - 1], None, o, T.H, 2, start)[0] for o in O])
        res = {}
        for name, m in models.items():
            f = step5(m.forecast([series.loc[start:o - 1].values for o in O]))[0]
            res[name] = float(np.sqrt(np.mean((tgt - f) ** 2)) / np.sqrt(np.mean((tgt - ar) ** 2)))
        return res

    real = ratios(yrev.loc[:e1])
    plac = {name: [] for name in models}
    for k in range(1, L2_DRAWS + 1):
        rng = np.random.default_rng(L2_SEED + k); idx = range(start - 2, e1 + 1); v = {}
        for t in idx:
            if t < start: v[t] = yrev[t]
            elif t < e0: v[t] = b[0] + b[1] * v[t - 1] + b[2] * v[t - 2] + rng.normal(0, s)
        sc = rng.uniform(*L2_SCALE); ep = actual * sc + rng.normal(0, rsd, len(actual))
        for i, t in enumerate(range(e0, e1 + 1)): v[t] = ep[i]
        r = ratios(pd.Series(v))
        for name in models: plac[name].append(r[name])
    return {name: dict(real_ratio=real[name], placebo_p10=float(np.quantile(plac[name], 0.1)),
                       placebo_median=float(np.median(plac[name])), placebo_ratios=plac[name],
                       real_percentile=float(100 * np.mean(np.array(plac[name]) < real[name])),
                       flag=bool(real[name] < np.quantile(plac[name], 0.1))) for name in models}


def main(mode, outdir=None):
    if mode == 'real':
        lock = os.path.join(EXT, 'PLAN_LOCK.json'); outdir = os.path.join(EXT, 'results')
        if not os.path.exists(lock): sys.exit('Real run refused: timesfm/PLAN_LOCK.json not found (plan not frozen).')
        if os.path.exists(outdir): sys.exit('Real run refused: timesfm/results exists. The plan allows one run only.')
        from huggingface_hub import hf_hub_download
        for key, (repo, rev, digest) in CHECKPOINTS.items():
            try: path = hf_hub_download(repo, 'model.safetensors', revision=rev)
            except Exception as e: sys.exit(f'Real run refused: cannot fetch {repo}@{rev} ({e}).')
            if sha(path) != digest: sys.exit(f'Real run refused: {repo} weights do not match the recorded hash.')
        m25 = M.get('tfm25', revision=CHECKPOINTS['tfm25'][1])
        try: m30 = M.get('tfm30', revision=CHECKPOINTS['tfm30'][1])
        except ImportError: m30 = None
    elif mode == 'pipeline-test':
        if not outdir: sys.exit('Give an output folder for the pipeline test.')
        m25 = m30 = M.get('dummy')
    else:
        sys.exit(__doc__)
    os.makedirs(outdir)
    D = T.load(); rows = build(D); qn, qs = D['qn'], D['qs']
    y = np.array([r['outcome'] for r in rows]); O = np.array([r['o'] for r in rows])
    ar2 = np.array([r['ar2'] for r in rows])
    F = forecasts(rows, m25, m30)
    tab = pd.DataFrame(dict(origin=[qs(o) for o in O], target=[qs(o + T.H) for o in O], outcome=y, ar2=ar2,
                            credit_model=[r['credit_model'] for r in rows], ar2_q10=[r['ar2_q10'] for r in rows], **F))
    tab.to_csv(os.path.join(outdir, 'forecasts.csv'), index=False)
    C = {'F1 TimesFM 2.5 vs AR(2)': compare(y, ar2, F['tfm25']),
         'F4 TimesFM 2.5 + credit (XReg) vs TimesFM 2.5': compare(y, F['tfm25'], F['tfm25_cr_rt']),
         'F5 premium, TimesFM 2.5 + credit': premium(y, F['tfm25'], F['tfm25_cr_rt'], F['tfm25_cr_rev'])}
    if m30 is not None:
        C['F2 TimesFM 3.0 vs AR(2)'] = compare(y, ar2, F['tfm30'])
        C['F3 TimesFM 3.0 + credit vs TimesFM 3.0'] = compare(y, F['tfm30'], F['tfm30_cr_rt'])
        C['F5 premium, TimesFM 3.0 + credit'] = premium(y, F['tfm30'], F['tfm30_cr_rt'], F['tfm30_cr_rev'])
    tt = (O + T.H >= qn(TAIL_TARGETS[0])) & (O + T.H <= qn(TAIL_TARGETS[1]))
    q10 = {'ar2': tab.ar2_q10.values, **{k[:-4]: v for k, v in F.items() if k.endswith('_q10')}}
    tail = {k: dict(pinball10_all=pinball(y, q), pinball10_2008_12=pinball(y[tt], q[tt]),
                    below_q10_all=float(np.mean(y < q)), below_q10_2008_12=float(np.mean(y[tt] < q[tt]))) for k, q in q10.items()}
    sub = (O >= qn(TABLE_ORIGINS[0])) & (O <= qn(TABLE_ORIGINS[1]))
    tab[sub].to_csv(os.path.join(outdir, 'table_2010_12.csv'), index=False)
    rsd = T.revision_sd(D); models = {'tfm25': m25} if m30 is None else {'tfm25': m25, 'tfm30': m30}
    if mode == 'pipeline-test': models = {'tfm25': m25}
    L1 = l1(D, rows, models, rsd); L2 = l2(D, models, rsd)
    res = dict(mode=mode, run_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
               python=platform.python_version(), platform=platform.platform(),
               backends={'tfm25': m25.name, 'tfm30': None if m30 is None else m30.name},
               scripts={f: sha(os.path.join(HERE, f)) for f in ('tfm_data.py', 'tfm_models.py', 'run_timesfm.py')},
               phase2=T.LOCKED_PHASE2, revision_sd=rsd, comparisons=C, tail=tail, L1=L1, L2=L2)
    if mode == 'real':
        res['plan_lock'] = json.load(open(os.path.join(EXT, 'PLAN_LOCK.json')))
        try:
            import timesfm, torch; res['versions'] = dict(timesfm=getattr(timesfm, '__version__', 'see pip freeze'), torch=torch.__version__)
        except Exception: pass
    json.dump(res, open(os.path.join(outdir, 'results.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: (v.get('ratio', v.get('premium')), v['ci90']) for k, v in C.items()}, indent=1))
    print('outputs:', sorted(os.listdir(outdir)))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '', sys.argv[2] if len(sys.argv) > 2 else None)
