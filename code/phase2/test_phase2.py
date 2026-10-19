"""Synthetic test of phase2.py. Credit is real; every target, GDP/unemployment vintage and SPF series is simulated,
so no real outcome is read. A known effect is planted (or not) and the pipeline must find it (or not)."""
import sys, os, copy, time, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase2 as P

def synth(D0, kappa_g, kappa_u, b3, seed):
    rng = np.random.default_rng(seed); D = dict(D0); qn = D['qn']
    t0, t1 = qn('1947Q1'), qn('2026Q2'); T = np.arange(t0, t1 + 1)
    ci = D['measures'](D['Z']['current'], D['NO'][D['LATEST']], D['P'][D['LATEST']], gap=False).CI
    c = (ci - ci.mean()).reindex(T).fillna(0.0).values
    g = np.zeros(len(T)); u = np.zeros(len(T)); g[:2] = 3.1; u[:2] = 5.9
    e = rng.multivariate_normal([0, 0], [[10.8, -0.47], [-0.47, 0.068]], len(T))
    for i in range(2, len(T)):
        lag = c[i - 6] if i >= 6 else 0.0
        g[i] = 1.84 + 0.264 * g[i-1] + 0.137 * g[i-2] + kappa_g * lag + e[i, 0]
        u[i] = 0.231 + 1.619 * u[i-1] - 0.659 * u[i-2] - kappa_u * lag + e[i, 1]
    gS, uS = pd.Series(g, T), pd.Series(u, T)
    R = pd.Series(b3 * np.r_[0, c[:-1]] + 1.3 * rng.standard_normal(len(T)), T)   # advance-to-revised revision
    RO, RU = {}, {}
    for w in D0['RO']:
        tw = w.year * 4 + (w.month - 2) // 3; last = tw - 1
        if last < t0 + 8: continue
        idx = T[T <= last]; age = last - idx
        decay = np.clip(1 - age / 12, 0, 1)                                      # revisions fade over 3 years
        gw = gS[idx] - R[idx] * decay
        lvl = 100 * np.cumprod((1 + gw.values / 100) ** 0.25)
        RO[w] = pd.Series(lvl, idx)
        RU[w] = uS[idx] + 0.05 * rng.standard_normal(len(idx)) * (age < 4)
    D['RO'], D['RU'] = RO, RU
    D['LATEST'] = max(w for w in RO if w in D0['NO']); D['LATEST_RU'] = max(RU)
    # SPF: direct AR(2)-information forecast of quarter o+4 plus idiosyncratic noise; no credit information
    def proj(y):
        X = np.column_stack([np.ones(len(T) - 6), y[4:-2], y[3:-3]]); Y = y[6:]
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; f = {}
        for i in range(2, len(T)): f[T[i]] = np.r_[1, y[i-1], y[i-2]] @ b
        return pd.Series(f)
    D['SPF_G'] = proj(g) + 0.5 * rng.standard_normal(len(T) - 2)
    D['SPF_U'] = proj(u) + 0.1 * rng.standard_normal(len(T) - 2)
    D['SPF_MICRO_SERIES'] = D['SPF_G'] + 0.2 * rng.standard_normal(len(D['SPF_G']))
    y2 = np.zeros(len(T)); y2[0] = 5.0
    for i in range(1, len(T)): y2[i] = max(0.1, 0.05 + 0.98 * y2[i-1] - 0.2 * e[i, 1] + 0.4 * rng.standard_normal())
    D['GS2'] = pd.Series(y2, T).loc[qn('1976Q3'):]
    D['mode'] = 'synthetic'; P._credit_cached.cache_clear()
    return D

def core(D):
    qn = D['qn']; O = list(range(qn('1999Q3'), qn('2018Q4') + 1))
    a = P.run_p1(D, 'g', O); b = P.run_p1(D, 'u', O); c = P.run_p2(D, 'g', O)
    _, p3 = P.run_p3(D, list(range(qn('1999Q2'), qn('2019Q4') + 1)))
    r = {'P1a': P.clark_west(a.y, a.fb, a.fa, 4), 'P1b': P.clark_west(b.y, b.fb, b.fa, 4),
         'P2a': P.clark_west(c.y, c.fb, c.fa, 4), 'P3': p3}
    return r, len(a), len(b), len(c), p3['n'], int(c.n_train.min())

if __name__ == '__main__':
    D0 = P.load('synthetic')
    for k in ('RO', 'RU'): assert isinstance(D0[k], dict)
    nseeds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    out = []
    for label, kg, ku, b3 in [('null', 0, 0, 0), ('planted', 1.2, 0.08, 0.8)]:
        for sd in range(nseeds):
            t = time.time(); D = synth(D0, kg, ku, b3, 1000 + sd); r, n1, n2, n3, n4, ntr = core(D)
            out.append(dict(case=label, seed=sd, n_P1a=n1, n_P1b=n2, n_P2a=n3, n_P3=n4, min_train_P2a=ntr,
                            **{f'p_{k}': v['p'] for k, v in r.items()},
                            **{f'ratio_{k}': v['ratio'] for k, v in r.items() if 'ratio' in v},
                            beta_P3=r['P3']['beta_CI'], secs=round(time.time() - t, 1)))
            print(out[-1], flush=True)
    df = pd.DataFrame(out); df.to_csv(os.path.join(os.path.dirname(__file__), 'synthetic_test_results.csv'), index=False)
    print(df.groupby('case')[[c for c in df if c.startswith('p_')]].apply(lambda x: (x < 0.05).mean()).round(2))
