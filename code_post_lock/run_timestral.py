"""
Timestral extension: the official run (plan: timestral/PLAN.md, Sections 4-8).

Modes
  pipeline-test OUTDIR : the whole pipeline on the real inputs with the stand-in 'dummy' back-end (an iterated
                         AR(2), never reported) in the Timestral slot. No Timestral model is loaded.
  real                 : the official run. Refuses unless timestral/PLAN_LOCK.json exists, and refuses once an
                         earlier attempt has passed the validity gate. Each attempt is saved to
                         timestral/results_attemptN/; the first attempt that passes every gate is the run.

The statistics (compare, premium, pinball, L1, L2) are imported unchanged from the frozen run_timesfm.py.
"""
import os, sys, json, glob, hashlib, datetime, platform
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tfm_data as T, tsl_models as M
import run_timesfm as R                                   # frozen TimesFM run script: statistics only
P = T.P
EXT = os.path.join(T.P2, '..', 'timestral')
TFM_RESULTS = os.path.join(T.P2, '..', 'timesfm', 'results', 'forecasts.csv')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def forecasts(rows, m):
    ys = [r['y_ctx'].values for r in rows]; F = {}
    gdp = m.forecast(ys)
    F['tsl'], F['tsl_q10'] = R.step5(gdp)
    F['tsl_cr_rt'], F['tsl_cr_rt_q10'] = R.step5(m.forecast_past_cov(ys, [r['cov_rt'] for r in rows]))
    F['tsl_cr_rev'], _ = R.step5(m.forecast_past_cov(ys, [r['cov_rev'] for r in rows]))
    return F, gdp


def gates(D, rows, m, gdp_out, lock, mode):
    """Validity gate (plan Section 8). Every check must pass for the attempt to be the official run."""
    g = {}
    # 1. locked AR(2) and credit-model forecasts reproduced at all 78 origins; frozen scripts unchanged
    L = pd.read_csv(os.path.join(T.P2, 'results_real', 'P1a_forecasts.csv')).set_index('o')
    O = [r['o'] for r in rows]
    g['1_locked_benchmark'] = bool(np.allclose([r['ar2'] for r in rows], L.loc[O, 'fb'], atol=1e-10, rtol=0)
                                   and np.allclose([r['credit_model'] for r in rows], L.loc[O, 'fa'], atol=1e-10, rtol=0))
    if mode == 'real':
        g['1_frozen_scripts'] = all(sha(os.path.join(HERE, f)) == lock['files_sha256'][f'code_post_lock/{f}']
                                    for f in ('tfm_data.py', 'run_timesfm.py', 'tsl_models.py', 'run_timestral.py'))
    # 2. credit covariate: Rule B at every origin, real-time and revised; nothing published after the origin
    bad = 0
    for r in rows:
        o = r['o']
        for which, key in (('rt', 'cov_rt'), ('credrev', 'cov_rev')):
            ci, qstar, k = T.credit_series(D, o, which)
            exp = np.array([ci[t - 1] for t in r['y_ctx'].index])
            bad += not (np.array_equal(exp, r[key]) and r['y_ctx'].index[-1] - 1 == qstar)
    g['2_credit_rule_B'] = bad == 0
    # 3. every forecast finite; exactly 5 steps; median equals the 0.5 quantile (checked in the back-end)
    g['3_shapes_finite'] = all(np.isfinite(x['point']).all() and np.isfinite(x['q']).all()
                               and x['point'].shape == (5,) and x['q'].shape == (5, 9) for x in gdp_out)
    # 4. repeatability: the first and last origins forecast again give identical results
    again = m.forecast([rows[0]['y_ctx'].values, rows[-1]['y_ctx'].values])
    g['4_repeatable'] = bool(np.array_equal(again[0]['point'], gdp_out[0]['point'])
                             and np.array_equal(again[1]['point'], gdp_out[-1]['point']))
    # 5. responsiveness: moving the last GDP value moves the forecast
    y2 = rows[-1]['y_ctx'].values.copy(); y2[-1] += 10
    g['5_responsive'] = bool(abs(m.forecast([y2])[0]['point'][4] - gdp_out[-1]['point'][4]) > 1e-6)
    # 6. weights and TimesFM comparison file match the lock
    if mode == 'real':
        from huggingface_hub import hf_hub_download
        g['6_weights_hash'] = sha(hf_hub_download(M.REPO, 'model.safetensors', revision=M.REVISION)) == M.WEIGHTS_SHA256
        g['6_timesfm_file_hash'] = sha(TFM_RESULTS) == lock['timesfm_forecasts_sha256']
    return g


def run(mode, outdir, lock=None):
    m = M.get('timestral') if mode == 'real' else M.get('dummy')
    D = T.load(); rows = R.build(D); qn, qs = D['qn'], D['qs']
    y = np.array([r['outcome'] for r in rows]); O = np.array([r['o'] for r in rows])
    ar2 = np.array([r['ar2'] for r in rows])
    F, gdp_out = forecasts(rows, m)
    if mode == 'pipeline-test':                                  # the dummy back-end has no _pack check
        for x in gdp_out: x['point'] = np.asarray(x['point']); x['q'] = np.asarray(x['q'])
    G = gates(D, rows, m, gdp_out, lock, mode)
    tab = pd.DataFrame(dict(origin=[qs(o) for o in O], target=[qs(o + T.H) for o in O], outcome=y, ar2=ar2,
                            credit_model=[r['credit_model'] for r in rows], ar2_q10=[r['ar2_q10'] for r in rows], **F))
    C = {'T1 Timestral vs AR(2)': R.compare(y, ar2, F['tsl']),
         'T2 Timestral + credit vs Timestral': R.compare(y, F['tsl'], F['tsl_cr_rt']),
         'T3 premium, Timestral + credit': R.premium(y, F['tsl'], F['tsl_cr_rt'], F['tsl_cr_rev'])}
    if os.path.exists(TFM_RESULTS):                              # T4, descriptive: against the published TimesFM run
        tf = pd.read_csv(TFM_RESULTS).set_index('origin').loc[tab.origin]
        if not np.allclose(tf.outcome.values, y, atol=1e-10): raise ValueError('TimesFM file outcomes differ')
        C['T4 Timestral vs TimesFM 3.0 (descriptive)'] = R.compare(y, tf.tfm30.values, F['tsl'])
        C['T4 Timestral vs TimesFM 2.5 (descriptive)'] = R.compare(y, tf.tfm25.values, F['tsl'])
        tab['tfm25'] = tf.tfm25.values; tab['tfm30'] = tf.tfm30.values
    tt = (O + T.H >= qn(R.TAIL_TARGETS[0])) & (O + T.H <= qn(R.TAIL_TARGETS[1]))
    q10 = {'ar2': tab.ar2_q10.values, 'tsl': F['tsl_q10'], 'tsl_cr_rt': F['tsl_cr_rt_q10']}
    tail = {k: dict(pinball10_all=R.pinball(y, q), pinball10_2008_12=R.pinball(y[tt], q[tt]),
                    below_q10_all=float(np.mean(y < q)), below_q10_2008_12=float(np.mean(y[tt] < q[tt])))
            for k, q in q10.items()}
    rsd = T.revision_sd(D)
    L1 = R.l1(D, rows, {'tsl': m}, rsd); L2 = R.l2(D, {'tsl': m}, rsd)
    os.makedirs(outdir)
    tab.to_csv(os.path.join(outdir, 'forecasts.csv'), index=False)
    sub = (O >= qn(R.TABLE_ORIGINS[0])) & (O <= qn(R.TABLE_ORIGINS[1]))
    tab[sub].to_csv(os.path.join(outdir, 'table_2010_12.csv'), index=False)
    res = dict(mode=mode, backend=m.name, run_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
               python=platform.python_version(), platform=platform.platform(),
               scripts={f: sha(os.path.join(HERE, f)) for f in ('tfm_data.py', 'run_timesfm.py', 'tsl_models.py', 'run_timestral.py')},
               phase2=T.LOCKED_PHASE2, revision_sd=rsd, comparisons=C, tail=tail, L1=L1, L2=L2,
               gates=G, gate_passed=bool(all(G.values())))
    if mode == 'real':
        res['plan_lock'] = lock
        import torch, timestral  # noqa: F401
        res['versions'] = dict(torch=torch.__version__, numpy=np.__version__)
    json.dump(res, open(os.path.join(outdir, 'results.json'), 'w'), indent=1, default=float)
    print(json.dumps({'gates': G, 'gate_passed': res['gate_passed']}, indent=1))
    return res


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'pipeline-test':
        if len(sys.argv) < 3: sys.exit('Give an output folder for the pipeline test.')
        run(mode, sys.argv[2])
    elif mode == 'real':
        lockf = os.path.join(EXT, 'PLAN_LOCK.json')
        if not os.path.exists(lockf): sys.exit('Real run refused: timestral/PLAN_LOCK.json not found (plan not frozen).')
        lock = json.load(open(lockf))
        done = sorted(glob.glob(os.path.join(EXT, 'results_attempt*')))
        for d in done:
            f = os.path.join(d, 'results.json')
            if not os.path.exists(f): sys.exit(f'Real run refused: {os.path.basename(d)} has no results.json; log it before rerunning.')
            if json.load(open(f)).get('gate_passed'): sys.exit(f'Real run refused: {os.path.basename(d)} already passed the gate.')
        run(mode, os.path.join(EXT, f'results_attempt{len(done) + 1}'), lock)
    else:
        sys.exit(__doc__)
