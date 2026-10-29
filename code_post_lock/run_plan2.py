"""
Plan 2: the horizon sweep (plan2/PLAN.md). Modes:

  pipeline-test OUTDIR [--placebo-survey]
        Synthetic GDP outcomes (locked test_phase2.synth, real credit path, no credit effect), real survey file
        (or a synthetic placebo survey if --placebo-survey or no file). Runs every comparison and gate. No real
        GDP outcome is read.
  real
        The official run. Refuses without plan2/PLAN2_LOCK.json, and refuses if an earlier attempt passed the gate.
        Each attempt is saved to plan2/results_attemptN/; the first attempt that passes every gate is the run.
"""
import os, sys, json, glob, hashlib, datetime, platform
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan2_data as T, plan2_models as M
P = T.P

SEED_PLACEBO = 20261201
TAIL = {'Q8a': ('2008Q1', '2009Q4'), 'Q8b': ('2001Q1', '2001Q4')}     # targets dropped in Q8


# ------------------------------------------------------------------ statistics (Section 6)
def hd(h): return max(h, 1)                       # DM lag order: h - 1 lags, at least 0 (locked uses h = 4)


def compare(y, f_comp, f_model, h):
    y, f_comp, f_model = map(np.asarray, (y, f_comp, f_model)); n = len(y)
    r = P.rmse_ratio(y, f_comp, f_model)
    lo, hi = P.boot_interval(lambda i: P.rmse_ratio(y, f_comp, f_model, i), n)
    dm = P.hln_dm(y, f_comp, f_model, hd(h))
    e1, e2 = y - f_comp, y - f_model
    return dict(ratio=float(r), ci90=[float(lo), float(hi)], credible_improvement=bool(hi < 1), n=int(n),
                hln_t=float(dm['hln_t']), p_boot=float(dm['p_boot']), error_corr=float(np.corrcoef(e1, e2)[0, 1]))


def ratio_diff(y_a, c_a, m_a, y_b, c_b, m_b):
    """R_b - R_a with a paired bootstrap over origins (same resampled origins for both): Q2's R4 - R1."""
    n = len(y_a); stat = lambda i=None: P.rmse_ratio(y_b, c_b, m_b, i) - P.rmse_ratio(y_a, c_a, m_a, i)
    lo, hi = P.boot_interval(stat, n); return dict(diff=float(stat()), ci90=[float(lo), float(hi)])


def coef_interval(y, block, o, h, start):
    """Survey coefficient at the last origin, with a moving-block bootstrap of training rows (Section 5, figure 2)."""
    js = np.arange(start, o - 1 - h + 1); Yt, A, Cs = M.rows(y, [block], js, h)
    ok = np.isfinite(Yt) & np.isfinite(A).all(1) & np.isfinite(Cs[0]).all(1)
    X = np.column_stack([A, Cs[0]])[ok]; Y = Yt[ok]; b = P.ols(X, Y)[-1]
    lo, hi = P.boot_interval(lambda i: P.ols(X[i], Y[i])[-1], len(Y))
    return dict(coef=float(b), ci90=[float(lo), float(hi)], rows=int(len(Y)))


# ------------------------------------------------------------------ placebo survey (gate 5)
def placebo_survey(s):
    """Independent draws with the survey's calendar-month means and standard deviations. No link to GDP."""
    rng = np.random.default_rng(SEED_PLACEBO)
    mu = s.groupby(s.index.month).mean(); sd = s.groupby(s.index.month).std(ddof=1)
    idx = pd.date_range('1968-05-01', '2019-12-01', freq='MS')
    return pd.Series([rng.normal(mu[t.month], sd[t.month]) for t in idx], index=idx)


# ------------------------------------------------------------------ one origin, every comparison
def forecasts_at(D, o, h, s, placebo):
    y = T.gdp(D, o); start = D['qn'](T.START); out = {}
    cb = M.credit_block(D, o)
    f, _, _ = M.fit(y, [cb], o, h, start); out.update(credit_ar=f['ar'], credit=f['all'])
    for kind in ('q1', 'q4', 'q5'):
        sb, last = M.survey_block(D, s['GA'], o, kind)
        f, _, _ = M.fit(y, [sb], o, h, start); out.update({f'{kind}_ar': f['ar'], kind: f['all'], f'{kind}_last': last})
    sb, _ = M.survey_block(D, s['NO'], o, 'q1')
    f, _, _ = M.fit(y, [sb], o, h, start); out.update(no_ar=f['ar'], no=f['all'])
    sb, _ = M.survey_block(D, s['GA'], o, 'q1')                                   # Q7 and the nested exploratory
    f, _, _ = M.fit(y, [cb, sb], o, h, start, models=('ar', 0, 1, 'all'))
    out.update(common_ar=f['ar'], common_credit=f[0], common_survey=f[1], common_both=f['all'])
    pb, _ = M.survey_block(D, placebo, o, 'q1')
    f, _, _ = M.fit(y, [pb], o, h, start); out.update(placebo_ar=f['ar'], placebo=f['all'])
    f, _, _ = M.fit(y, [sb], o, h, D['qn']('1985Q1')); out.update(post85_ar=f['ar'], post85=f['all'])
    return out


# ------------------------------------------------------------------ gates (Section 8)
def gates(D, F, s, placebo_cmp, mode, lock):
    g = {}
    # 1. h = 4 AR(2) and credit reproduce the locked forecasts
    f4 = F[F.h == 4].set_index('o')
    if mode == 'real':
        L = pd.read_csv(os.path.join(T.P2, 'results_real', 'P1a_forecasts.csv')).set_index('o')
        g['1_locked_h4'] = bool(np.allclose(f4.credit_ar, L.loc[f4.index, 'fb'], atol=1e-10, rtol=0)
                                and np.allclose(f4.credit, L.loc[f4.index, 'fa'], atol=1e-10, rtol=0))
    bad = 0
    for o in T.origins(D)[:: 13]:                                  # fit() against direct_forecast, sampled origins
        y = T.gdp(D, o); ci, k = T.credit(D, o)
        fb, fa = P.direct_forecast(y, ci, o, 4, k, D['qn'](T.START))
        bad += not (np.isclose(fb, f4.loc[o, 'credit_ar'], atol=1e-10, rtol=0) and np.isclose(fa, f4.loc[o, 'credit'], atol=1e-10, rtol=0))
    g['1_fit_equals_locked_function'] = bad == 0
    # 2. survey value used: first month of quarter o (Q1/Q4); third month of quarter o-1 (Q5)
    one = F[F.h == 1]
    want1 = [pd.Timestamp(T.origin_date(o).year, 3 * (o % 4) + 1, 1) for o in one.o]
    want5 = [pd.Timestamp((o - 1) // 4, 3 * ((o - 1) % 4) + 3, 1) for o in one.o]
    g['2_release_rule'] = bool((pd.to_datetime(one.q1_last).values == np.array(want1, dtype='datetime64[ns]')).all()
                               and (pd.to_datetime(one.q5_last).values == np.array(want5, dtype='datetime64[ns]')).all())
    # 3. seasonal adjustment recomputed independently (method A) at every origin
    bad = 0
    for o in T.origins(D):
        M1, _, _ = T.survey_quarterly(D, s['GA'], o); cut = T.origin_date(o)
        mon = 3 * (o % 4) + 1; past = [v for t, v in s['GA'].items() if t.month == mon and T.third_thursday(t.year, t.month) < cut]
        raw = s['GA'][pd.Timestamp(o // 4, mon, 1)]
        bad += not np.isclose(M1[o], raw - np.mean(past), atol=1e-12)
    g['3_seasonal_recomputed'] = bad == 0
    # 4. forecasts finite and responsive (shift the last GDP value and the origin's survey reading)
    o = T.origins(D)[-1]; y = T.gdp(D, o).copy(); start = D['qn'](T.START)
    sb, _ = M.survey_block(D, s['GA'], o, 'q1'); f0, _, _ = M.fit(y, [sb], o, 1, start)
    y2 = y.copy(); y2[o - 1] += 10; f1, _, _ = M.fit(y2, [sb], o, 1, start)
    X2 = sb[0].copy(); X2[o] += 10; f2, _, _ = M.fit(y, [(X2, 0, 1)], o, 1, start)
    g['4_finite_and_responsive'] = bool(np.isfinite(F.select_dtypes('number').values).all()
                                        and abs(f1['all'] - f0['all']) > 1e-6 and abs(f2['all'] - f0['all']) > 1e-6)
    # 5. placebo not credibly below 1
    g['5_placebo_not_credibly_below_1'] = bool(placebo_cmp['ci90'][1] >= 1)
    # 6. survey files match the lock
    if mode == 'real':
        g['6_survey_hashes'] = all(T.sha(os.path.join(T.DATA, f'{sid}.csv')) == lock['survey_sha256'][sid]
                                   for sid in T.SURVEY.values())
    return g


# ------------------------------------------------------------------ main
def run(D, s, mode, outdir, lock=None):
    placebo = placebo_survey(s['GA'])
    rows = []
    for h in T.HORIZONS:
        for o in T.origins(D):
            rows.append(dict(o=o, origin=D['qs'](o), h=h, target=D['qs'](o + h), y=T.outcome(D, o + h),
                             **forecasts_at(D, o, h, s, placebo)))
    F = pd.DataFrame(rows)
    C, X = {}, {}
    for h in T.HORIZONS:
        d = F[F.h == h]
        C[f'survey_h{h}'] = compare(d.y, d.q1_ar, d.q1, h)
        C[f'credit_h{h}'] = compare(d.y, d.credit_ar, d.credit, h)
        X[f'post85_survey_h{h}'] = compare(d.y, d.post85_ar, d.post85, h)
    d1, d4 = F[F.h == 1], F[F.h == 4]
    C['Q1'] = C['survey_h1']
    C['Q2_R4_minus_R1'] = ratio_diff(d1.y.values, d1.q1_ar.values, d1.q1.values, d4.y.values, d4.q1_ar.values, d4.q1.values)
    C['Q4'] = compare(d1.y, d1.q4_ar, d1.q4, 1)
    C['Q5'] = compare(d1.y, d1.q5_ar, d1.q5, 1)
    C['Q6'] = {f'h{h}': compare(F[F.h == h].y, F[F.h == h].no_ar, F[F.h == h].no, h) for h in T.HORIZONS}
    C['Q7'] = compare(d1.y, d1.common_credit, d1.common_survey, 1)
    for lab, (a, b) in TAIL.items():
        keep = ~d1.target.between(a, b)
        C[lab] = compare(d1.y[keep], d1.q1_ar[keep], d1.q1[keep], 1)
    X['survey_beyond_credit_h1'] = compare(d1.y, d1.common_credit, d1.common_both, 1)
    coef = {}
    for h in T.HORIZONS:
        o = T.origins(D)[-1]; sb, _ = M.survey_block(D, s['GA'], o, 'q1')
        coef[f'h{h}'] = coef_interval(T.gdp(D, o), sb, o, h, D['qn'](T.START))
    placebo_cmp = compare(d1.y, d1.placebo_ar, d1.placebo, 1)
    G = gates(D, F, s, placebo_cmp, mode, lock)
    res = dict(mode=mode, run_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
               python=platform.python_version(),
               scripts={f: T.sha(os.path.join(HERE, f)) for f in ('plan2_data.py', 'plan2_models.py', 'run_plan2.py')},
               phase2=T.LOCKED_PHASE2, comparisons=C, exploratory=X, coefficients_last_origin=coef,
               placebo=placebo_cmp, gates=G, gate_passed=bool(all(G.values())))
    if lock: res['plan_lock'] = lock
    os.makedirs(outdir, exist_ok=True)
    F.to_csv(os.path.join(outdir, 'forecasts.csv'), index=False)
    json.dump(res, open(os.path.join(outdir, 'results.json'), 'w'), indent=1, default=str)
    print(json.dumps({'gates': G, 'gate_passed': res['gate_passed']}, indent=1))
    return res


def synthetic_survey_file_missing():
    return not all(os.path.exists(os.path.join(T.DATA, f'{sid}.csv')) for sid in T.SURVEY.values())


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'pipeline-test':
        import test_phase2 as TP
        outdir = sys.argv[2]
        D = TP.synth(T.load('synthetic'), 0.0, 0.0, 0.0, 9001); P.LAST_TARGET = D['qn']('2019Q4')
        if '--placebo-survey' in sys.argv or synthetic_survey_file_missing():
            base = pd.Series(0.0, index=pd.date_range('1968-05-01', '2019-12-01', freq='MS'))
            rng = np.random.default_rng(7); base[:] = rng.normal(10, 20, len(base))
            s = {'GA': base, 'NO': base * 0.9 + rng.normal(0, 5, len(base))}
            print('NOTE: synthetic survey (no survey file found or --placebo-survey)')
        else:
            s = {k: T.load_survey(k) for k in T.SURVEY}
        run(D, s, 'pipeline-test', outdir)
    elif mode == 'real':
        lockf = os.path.join(T.EXT, 'PLAN2_LOCK.json')
        if not os.path.exists(lockf): sys.exit('Real run refused: plan2/PLAN2_LOCK.json not found (plan not frozen).')
        lock = json.load(open(lockf))
        done = sorted(glob.glob(os.path.join(T.EXT, 'results_attempt*')))
        for dd in done:
            r = json.load(open(os.path.join(dd, 'results.json')))
            if r.get('gate_passed'): sys.exit(f'Real run refused: {os.path.basename(dd)} already passed the gate.')
        outdir = os.path.join(T.EXT, f'results_attempt{len(done) + 1}')
        D = T.load('real'); s = {k: T.load_survey(k) for k in T.SURVEY}
        run(D, s, 'real', outdir, lock)
    else:
        sys.exit(__doc__)
