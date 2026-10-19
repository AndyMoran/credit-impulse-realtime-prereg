import sys,os; sys.path.insert(0,'.')
import numpy as np, pandas as pd, phase2 as P, test_phase2 as T
def wild_p(df, B=999, seed=0, block=4):
    """Restricted wild (Rademacher) block bootstrap-t for the CI coefficient (H0: beta_CI=0)."""
    X = np.column_stack([np.ones(len(df)), df.CI, df.g_adv, df.g_lag]); y = df.R.values
    b, se = P.hac_ols(X, y, 4); t0 = b[1] / se[1]
    X0 = X[:, [0, 2, 3]]; b0 = P.ols(X0, y); f0 = X0 @ b0; e0 = y - f0
    rng = np.random.default_rng(seed); n = len(y); nb = int(np.ceil(n / block)); tb = []
    for _ in range(B):
        v = np.repeat(rng.choice([-1, 1], nb), block)[:n]; yb = f0 + e0 * v
        bb, sb = P.hac_ols(X, yb, 4); tb.append(bb[1] / sb[1])
    return float(np.mean(np.abs(tb) >= abs(t0)))
D0 = P.load('synthetic'); qn = D0['qn']; Q3 = list(range(qn('1999Q2'), qn('2019Q4') + 1)); out = []
for b3 in (0.0, 0.15):
    for sd in range(int(sys.argv[1])):
        D = T.synth(D0, 0, 0, b3, 9000 + sd); df, r = P.run_p3(D, Q3)
        out.append(dict(b3=b3, p_fixedb=r['p'], p_wild=wild_p(df, seed=sd)))
d = pd.DataFrame(out); print((d[['p_fixedb', 'p_wild']] < 0.05).groupby(d.b3).mean())
