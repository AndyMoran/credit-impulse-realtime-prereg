"""Post-lock (Entry 30): coverage by nominal level from calibrate.py, a coverage-calibrated widening factor per test, and the locked
outputs' block-bootstrap intervals at that level (same seed, draws and blocks as the locked run)."""
import sys, os, glob, json; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd, phase2 as P
d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'calib_[0-9]*.csv')))])
LEVELS = [0.90, 0.93, 0.95, 0.97, 0.98, 0.99]; cov = []
for (kg, t), s in d.groupby(['kg', 'test']):
    true = np.sqrt(s.mse_a.mean() / s.mse_b.mean())
    cov.append(dict(kg=kg, test=t, n=len(s), true=round(true, 3),
                    **{f'cov{L}': ((s[f'lo{L}'] <= true) & (true <= s[f'hi{L}'])).mean() for L in LEVELS}))
cov = pd.DataFrame(cov); print(cov.round(3).to_string(index=False))
# Raising the percentile level does not reach 90% coverage for P1b and P2a (86-93% even at 99%): the misses are
# one-sided (intervals sit below the truth with no effect, above it with an effect). So the 90% interval is widened
# about the point estimate by a factor c, the smallest that gives >= 90% coverage at BOTH simulated effect sizes.
cs = np.round(np.arange(1, 3.001, 0.05), 2); fac = {}
for t, g in d.groupby('test'):
    need = []
    for kg, s in g.groupby('kg'):
        true = np.sqrt(s.mse_a.mean() / s.mse_b.mean()); r = s.ratio
        need.append(next(c for c in cs if ((r - c * (r - s['lo0.9']) <= true) & (true <= r + c * (s['hi0.9'] - r))).mean() >= 0.90))
    fac[t] = max(need)
print('inflation factors:', fac)
R = os.path.join(os.path.dirname(HERE), 'results_real'); res = json.load(open(os.path.join(R, 'results.json')))['core']; out = {}
for t in ('P1a', 'P1b', 'P2a'):
    f = pd.read_csv(os.path.join(R, f'{t}_forecasts.csv')); c = fac[t]; r = P.rmse_ratio(f.y, f.fb, f.fa)
    l9, h9 = P.boot_interval(lambda idx, a=f: P.rmse_ratio(a.y, a.fb, a.fa, idx), len(f))
    assert np.allclose([l9, h9], res[t]['ratio_ci90']), 'locked 90% interval not reproduced'
    lo, hi = r - c * (r - l9), r + c * (h9 - r)
    out[t] = dict(ratio=round(res[t]['ratio'], 3), locked90=[round(l9, 3), round(h9, 3)], inflation=c,
                  calibrated=[round(lo, 3), round(hi, 3)], max_gain_pct=round(100 * (1 - lo), 1))
print(json.dumps(out, indent=1)); cov.to_csv(os.path.join(HERE, 'out', 'coverage_by_level.csv'), index=False)
json.dump(out, open(os.path.join(HERE, 'out', 'calibrated_intervals.json'), 'w'), indent=1)
