"""Post-lock descriptive diagnostics (Entry 29). Imports the locked phase2.py unchanged; no confirmatory quantity is
re-estimated or replaced. Outputs: coefficient paths for P1a, the largest-loss origins, P2a training-start sensitivity."""
import sys, os, json; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd, phase2 as P
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
D = P.load('real'); qn = D['qn']; O = list(range(qn('1999Q3'), qn('2018Q4') + 1)); q = lambda t: f"{t//4}Q{t%4+1}"
lock = pd.read_csv(os.path.join(os.path.dirname(HERE), 'results_real', 'P1a_forecasts.csv'))

# 1. P1a coefficient paths and inputs, replicating direct_forecast exactly
rows = []; h = P.H_PRIMARY; start = qn('1965Q1')
for o in O:
    if o + h > P.LAST_TARGET: continue
    oi = P.origin_info(D, o); y = P.series(D, 'g', oi['w']).loc[:o - 1]
    X = P.credit(D, oi['v'], oi['w'], 'rt')['CI']; k = oi['k']
    js = np.arange(start, o - 1 - h + 1); Yt, A, C = P.direct_rows(y, X, js, h, k)
    ok = np.isfinite(Yt) & np.isfinite(A).all(1) & np.isfinite(C).all(1)
    _, a, c = P.direct_rows(y, X, np.array([o]), h, k)
    bb = P.ols(A[ok], Yt[ok]); ba = P.ols(np.column_stack([A, C])[ok], Yt[ok])
    fb = a[0] @ bb; fa = np.r_[a[0], c[0]] @ ba
    rows.append(dict(o=o, origin=q(o), s=o + h, target=q(o + h), fb=fb, fa=fa,
                     **{f'b_ci{l}': ba[3 + l] for l in range(4)}, b_ci_sum=ba[3:].sum(),
                     **{f'ci_lag{l}': c[0][l] for l in range(4)}, credit_term=c[0] @ ba[3:]))
cp = pd.DataFrame(rows).merge(lock[['o', 'y']], on='o')
assert np.allclose(cp.fb, lock.fb) and np.allclose(cp.fa, lock.fa), 'replication of locked P1a forecasts failed'
cp['loss'] = (cp.y - cp.fa) ** 2 - (cp.y - cp.fb) ** 2              # positive = credit model worse
cp.to_csv(os.path.join(OUT, 'p1a_coefficient_paths.csv'), index=False)
top = cp.sort_values('loss', ascending=False).head(6)
top[['origin', 'target', 'ci_lag0', 'ci_lag1', 'ci_lag2', 'ci_lag3', 'b_ci_sum', 'credit_term', 'fb', 'fa', 'y', 'loss']].round(3) \
   .to_csv(os.path.join(OUT, 'p1a_top_loss_origins.csv'), index=False)

# 2. P2a training-start sensitivity: run_p2 with j0 as a parameter (otherwise identical; checked at 1990Q3)
def run_p2_j0(var, j0):
    hh = 4; spf = P.spf_series(D, var); out = []
    for o in O:
        s = o + hh
        if s > P.LAST_TARGET or o not in D['DEADLINE']: continue
        d = D['DEADLINE'][o]; v = P.z1_before(D, d); qstar = D['Z'][v].index.max(); k = o - qstar
        w = P.vint(o); y = P.series(D, var, w); ci = P.credit(D, v, w, 'rt')['CI']
        js = [j for j in range(j0, o - hh) if j in spf.index and np.isfinite(spf[j])]
        e = np.array([y.get(j + hh, np.nan) - spf[j] for j in js]); cc = np.array([ci.get(j - k, np.nan) for j in js])
        ok = np.isfinite(e) & np.isfinite(cc)
        if ok.sum() < 20: continue
        b = P.ols(np.column_stack([np.ones(ok.sum()), cc[ok]]), e[ok]); f0 = spf[o]
        out.append(dict(o=o, n_train=int(ok.sum()), fb=f0 + e[ok].mean(), fa=f0 + b[0] + b[1] * ci[qstar],
                        y=P.target(D, var, s, 'revised')))
    return pd.DataFrame(out)
lockp2 = pd.read_csv(os.path.join(os.path.dirname(HERE), 'results_real', 'P2a_forecasts.csv'))
base = run_p2_j0('g', qn('1990Q3')); assert np.allclose(base.fa.values, lockp2.fa.values), 'P2a replication failed'
sens = {}
for st in ('1990Q3', '1993Q1', '1996Q1'):
    d = run_p2_j0('g', qn(st)); sens[st] = d
common = sorted(set.intersection(*[set(d.o) for d in sens.values()]))
srows = []
for st, d in sens.items():
    dc = d[d.o.isin(common)]
    srows.append(dict(start=st, n_origins=len(d), first_origin=q(d.o.min()), min_pairs=int(d.n_train.min()),
                      ratio_own=P.rmse_ratio(d.y, d.fb, d.fa), ratio_common=P.rmse_ratio(dc.y, dc.fb, dc.fa)))
pd.DataFrame(srows).round(3).to_csv(os.path.join(OUT, 'p2a_training_start.csv'), index=False)
print(top[['origin','target','ci_lag0','b_ci_sum','credit_term','fb','fa','y','loss']].round(2).to_string(index=False))
print(pd.DataFrame(srows).round(3).to_string(index=False), '\ncommon origins', len(common), q(common[0]))
print(cp[['origin','b_ci_sum']].iloc[::8].round(3).to_string(index=False))
