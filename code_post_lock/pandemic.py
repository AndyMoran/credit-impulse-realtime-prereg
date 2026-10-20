"""
Pandemic-period illustration, 2020-21 (non-preregistered; plan: pandemic/PLAN.md, tag `pandemic-plan`).

Runs the LOCKED specification (phase2.py, unedited, hash-checked) for the eight forecasts the locked rule excluded:
targets 2020Q1-2021Q4 at h = 4, origins 2019Q1-2020Q4, for P1a, P1b and P2a. Nothing in the locked release is modified;
the three 2020 Z.1 vintages and the 2020 SPF deadlines are read from separate files and added in memory.

Modes
  check : uses only locked data; reproduces the locked 1999Q3-2018Q4 forecasts exactly and stops. Safe to run any time.
  real  : the single run on real 2020 data. Refuses to run unless pandemic/PLAN_LOCK.json (commit and tag of the frozen
          plan) and the three input files exist, and refuses if an output folder already exists (one run only).
"""
import sys, os, json, hashlib, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.dirname(HERE); sys.path.insert(0, P2)
LOCKED_PHASE2 = 'da697030f2349feae24dc79a3dfcbb786552b62186ffbf624a027c591814766e'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
if sha(os.path.join(P2, 'phase2.py')) != LOCKED_PHASE2: sys.exit('phase2.py is not the locked file; stopping.')
import numpy as np, pandas as pd, phase2 as P

PAN = os.path.join(P2, '..', 'pandemic')                     # inputs for the real run (plan section 5, steps 3-5)
F_CRED, F_LOG, F_DEAD = (os.path.join(PAN, f) for f in ('credit_vintages_2020.csv', 'download_log_2020.csv', 'spf_deadlines_2020.csv'))
OUT = os.path.join(PAN, 'results')

def add_2020(D):
    """Add the 2020 Z.1 vintages exactly as p1/build.py builds the locked ones, and the 2020 SPF deadlines."""
    c = pd.read_csv(F_CRED); log = pd.read_csv(F_LOG)
    rel = dict(zip(log.folder.astype(str), log.release_date)); c['t'] = c.quarter.map(D['qn']); c = c[c.t >= D['qn']('1953Q1')]
    for v, g in c.groupby('vintage_folder'):
        w = g.pivot_table(index='t', columns='concept', values='value_bn')
        D['Z'][str(v)] = pd.DataFrame({'F': (w.hh_flow_saar + w.nfb_flow_saar) / 4.0, 'L': w.hh_level_sa + w.nfb_level_sa,
                                      'Fhh': w.hh_flow_saar / 4, 'Fnfb': w.nfb_flow_saar / 4}).sort_index()
        D['rel'][str(v)] = pd.Timestamp(rel[str(v)])
    D['zv'] = sorted([k for k in D['Z'] if k != 'current'], key=lambda k: D['rel'][k])
    for r in pd.read_csv(F_DEAD).itertuples(): D['DEADLINE'][D['qn'](r.spf_survey)] = pd.Timestamp(r.deadline)
    return D

def p1_detail(D, var, origins):
    """Locked P1 forecasts plus the credit term, replicating direct_forecast exactly (asserted)."""
    d = P.run_p1(D, var, origins); rows = []; h = P.H_PRIMARY; start = D['qn']('1965Q1')
    for o in d.o:
        oi = P.origin_info(D, o); y = P.series(D, var, oi['w']).loc[:o - 1]; X = P.credit(D, oi['v'], oi['w'], 'rt')['CI']
        Yt, A, C = P.direct_rows(y, X, np.arange(start, o - 1 - h + 1), h, oi['k'])
        ok = np.isfinite(Yt) & np.isfinite(A).all(1) & np.isfinite(C).all(1); _, a, c = P.direct_rows(y, X, np.array([o]), h, oi['k'])
        b = P.ols(np.column_stack([A, C])[ok], Yt[ok])
        rows.append(dict(o=o, ci_qstar=c[0][0], coef_sum=b[3:].sum(), credit_term=c[0] @ b[3:], fa_check=np.r_[a[0], c[0]] @ b))
    d = d.merge(pd.DataFrame(rows), on='o'); assert np.allclose(d.fa, d.fa_check), 'credit-term replication failed'
    return d.drop(columns='fa_check')

def p2_detail(D, origins):
    d = P.run_p2(D, 'g', origins); ci = []
    for o in d.o:
        v = P.z1_before(D, D['DEADLINE'][o]); w = P.vint(o); qstar = D['Z'][v].index.max()
        ci.append(P.credit(D, v, w, 'rt')['CI'][qstar])
    return d.assign(ci_qstar=ci, credit_term=d.fa - d.fb)

def summarise(d):
    return dict(n=len(d), ratio=float(P.rmse_ratio(d.y, d.fb, d.fa)),
                mean_error_benchmark=float((d.fb - d.y).mean()), mean_error_credit=float((d.fa - d.y).mean()))

def wording(r):                                              # plan section 4, verbatim
    if r < 0.90: s = "more accurate than"
    elif r <= 1.10: s = "about as accurate as"
    else: s = "less accurate than"
    return (f"Over the eight pandemic-period targets, the credit model's forecasts were {s} the benchmark's (ratio {r:.3f}). "
            "With eight targets dominated by one shock that did not originate in credit, this is an illustration, not evidence "
            "about predictive content. It does not alter the pre-registered conclusion.")

def main(mode):
    D = P.load('real'); qn, qs = D['qn'], D['qs']
    O_locked = list(range(qn('1999Q3'), qn('2018Q4') + 1))
    if mode == 'check':                                      # cut-off stays at the locked 2019Q4
        R = os.path.join(P2, 'results_real')
        for name, d in (('P1a', p1_detail(D, 'g', O_locked)), ('P1b', p1_detail(D, 'u', O_locked)), ('P2a', p2_detail(D, O_locked))):
            L = pd.read_csv(os.path.join(R, f'{name}_forecasts.csv'))
            assert len(d) == len(L) and np.allclose(d[['fb', 'fa', 'y']].values, L[['fb', 'fa', 'y']].values), name
            print(f'{name}: {len(d)} locked forecasts reproduced exactly; ratio {summarise(d)["ratio"]:.4f}')
        print('check passed: no 2020 data used'); return
    for f in (os.path.join(PAN, 'PLAN_LOCK.json'), F_CRED, F_LOG, F_DEAD):
        if not os.path.exists(f): sys.exit(f'Real run refused: {f} not found.')
    if os.path.exists(OUT): sys.exit(f'Real run refused: {OUT} exists. The plan allows one run only.')
    D = add_2020(D); P.LAST_TARGET = qn('2021Q4')            # the one parameter changed (plan section 3)
    O8 = list(range(qn('2019Q1'), qn('2020Q4') + 1)); O86 = list(range(qn('1999Q3'), qn('2020Q4') + 1))
    os.makedirs(OUT); res = dict(plan_lock=json.load(open(os.path.join(PAN, 'PLAN_LOCK.json'))),
                                 run_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                                 inputs={os.path.basename(f): sha(f) for f in (F_CRED, F_LOG, F_DEAD)}, tests={})
    for name, var in (('P1a', 'g'), ('P1b', 'u'), ('P2a', None)):
        d8 = p1_detail(D, var, O8) if var else p2_detail(D, O8)
        d86 = P.run_p1(D, var, O86) if var else P.run_p2(D, 'g', O86)
        d8 = d8.assign(origin=d8.o.map(qs), target=d8.s.map(qs), sq_err_diff=(d8.y - d8.fa) ** 2 - (d8.y - d8.fb) ** 2)
        d8.to_csv(os.path.join(OUT, f'{name}_pandemic_forecasts.csv'), index=False)
        s8 = summarise(d8)
        res['tests'][name] = dict(eight_targets=s8, wording=wording(s8['ratio']),
                                  extended_1999Q3_2020Q4=summarise(d86), origins=[qs(o) for o in d8.o])
    rows = []                                                # plan section 4, item 4: real-time impulse as published in 2020
    for v in [k for k in D['zv'] if k.startswith('2020')]:
        w = P.vint(qn(f"{D['rel'][v].year}Q{(D['rel'][v].month - 1) // 3 + 1}"))
        m = P.credit(D, v, w, 'rt')['CI']
        rows += [dict(release=v, quarter=qs(t), CI=m[t]) for t in m.index if t >= qn('2019Q1')]
    rev = D['measures'](D['Z']['current'], D['NO'][D['LATEST']], D['P'][D['LATEST']], gap=False).CI
    rows += [dict(release='current (revised)', quarter=qs(t), CI=rev[t]) for t in rev.index if qn('2019Q1') <= t <= qn('2020Q2')]
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'impulse_2019_2020.csv'), index=False)
    json.dump(res, open(os.path.join(OUT, 'pandemic_results.json'), 'w'), indent=1)
    print(json.dumps({k: v['eight_targets'] | {'extended_ratio': v['extended_1999Q3_2020Q4']['ratio']} for k, v in res['tests'].items()}, indent=1))
    print('outputs:', sorted(os.listdir(OUT)))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'check')
