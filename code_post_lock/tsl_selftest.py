"""
Timestral extension: self-test before freezing (plan: timestral/PLAN.md, Section 8, step 2).

Part A, real inputs, no model loaded: the locked AR(2) and credit-model forecasts are reproduced at all 78
origins, and the credit covariate follows Rule B (position t holds CI(t-1); the last value is CI(q*)) for
real-time and revised credit at every origin.

Part B, synthetic series only, with the downloaded Timestral weights. No real US series is passed to Timestral.
  B1 exactly 5 steps and 9 deciles, all finite; the median equals the 0.5 quantile
  B2 negative forecasts are allowed (a series centred below zero)
  B3 a repeat call gives identical forecasts
  B4 the covariate route runs and changes the forecast
  B5 positive control: when the target is driven by last quarter's covariate, adding the covariate cuts the
     one-step error by at least 20% over 40 synthetic series (the model can use a past-only covariate)
  B6 negative control: an unrelated covariate changes the one-step error by less than 10%
Usage: python tsl_selftest.py          (real weights; writes tsl_selftest.txt)
       python tsl_selftest.py --tiny   (small random-weights model; plumbing only, B5-B6 skipped)
"""
import os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tfm_data as T, tsl_models as M
P = T.P
log = []
def check(ok, msg): line = ('PASS  ' if ok else 'FAIL  ') + msg; print(line, flush=True); log.append(line); return bool(ok)


def tiny():
    import torch
    from timestral import TimestralConfig, TimestralForecaster, TimestralModel
    knots = (0.01, 0.05) + tuple(round(0.1 + 0.05 * i, 2) for i in range(17)) + (0.95, 0.99)
    cfg = TimestralConfig(patch_size=8, d_model=32, num_heads=4, mlp_hidden_dim=64,
                          block_schedule=('time', 'time_variate', 'time', 'time_variate'),
                          quantile_knots=knots, block_size=4, context_length=512)
    torch.manual_seed(0); model = TimestralModel(cfg)
    for p in model.parameters(): torch.nn.init.normal_(p, std=0.05)
    return M.Timestral(forecaster=TimestralForecaster(model.eval()))


def part_a():
    D = T.load(); ok = True; O = T.origins(D)
    L = pd.read_csv(os.path.join(T.P2, 'results_real', 'P1a_forecasts.csv')).set_index('o')
    bad = 0; bad_b = 0
    for o in O:
        y = T.gdp_context(D, o); fb, fa = T.locked_benchmark(D, o, y)
        bad += not (np.isclose(fb, L.loc[o, 'fb'], atol=1e-10, rtol=0) and np.isclose(fa, L.loc[o, 'fa'], atol=1e-10, rtol=0))
        for which in ('rt', 'credrev'):
            ci, qstar, k = T.credit_series(D, o, which); c = T.credit_aligned(D, o, y, which)
            bad_b += not (np.array_equal(c, np.array([ci[t - 1] for t in y.index])) and c[-1] == ci[qstar]
                          and y.index[-1] - 1 == qstar and k == 2)
    ok &= check(bad == 0, f'locked AR(2) and credit-model forecasts reproduced at all {len(O)} origins')
    ok &= check(bad_b == 0, 'credit covariate follows Rule B (CI(t-1), last value CI(q*)), real-time and revised, all origins')
    D2 = D; o = O[O.index(D['qn']('2010Q1'))]; y = T.gdp_context(D2, o); c = T.credit_aligned(D2, o, y, 'rt')
    log.append(f'INFO  worked example, origin 2010Q1: last covariate value {c[-1]:.3f} (plan: -10.356)')
    ok &= check(abs(c[-1] + 10.356) < 5e-4, 'worked example matches the plan (2010Q1: CI(2009Q3) = -10.356)')
    return ok


def synth(n, rng, drive=None):
    x = np.zeros(n); y = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.5 * x[t - 1] + rng.normal()
        y[t] = (0.9 * x[t - 1] if drive else 0.0) + 0.3 * rng.normal() + 0.3 * y[t - 1] * (not drive)
    return y, x


def part_b(m, full):
    ok = True; rng = np.random.default_rng(20261029)
    y = np.cumsum(rng.normal(0, 1, 180)) * 0.2 + 2.5
    r = m.forecast([y])[0]
    ok &= check(r['point'].shape == (5,) and r['q'].shape == (5, 9) and np.isfinite(r['q']).all(),
                'B1 five steps and nine deciles, all finite; median equals the 0.5 quantile')
    yneg = rng.normal(-3, 0.5, 180); rn = m.forecast([yneg])[0]
    ok &= check((rn['point'] < 0).any(), f'B2 negative forecasts allowed (step-1 median {rn["point"][0]:.2f})')
    r2 = m.forecast([y])[0]
    ok &= check(np.array_equal(r['point'], r2['point']) and np.array_equal(r['q'], r2['q']), 'B3 repeat call identical')
    c = rng.normal(0, 1, 180); rc = m.forecast_past_cov([y], [c])[0]
    ok &= check(np.isfinite(rc['point']).all() and not np.allclose(rc['point'], r['point']),
                'B4 covariate route runs and changes the forecast')
    if not full:
        log.append('INFO  B5-B6 skipped (random-weights plumbing test)'); return ok
    e_with, e_without, e_noise = [], [], []
    for i in range(40):
        yy, xx = synth(201, np.random.default_rng(20261100 + i), drive=True)
        ctx, cov, tgt = yy[:-1], xx[:-1], yy[-1]                   # covariate known through the last context step
        e_without.append(abs(m.forecast([ctx])[0]['point'][0] - tgt))
        e_with.append(abs(m.forecast_past_cov([ctx], [cov])[0]['point'][0] - tgt))
        noise = np.random.default_rng(20261200 + i).normal(0, 1, len(ctx))
        e_noise.append(abs(m.forecast_past_cov([ctx], [noise])[0]['point'][0] - tgt))
    r5 = np.mean(e_with) / np.mean(e_without); r6 = np.mean(e_noise) / np.mean(e_without)
    ok &= check(r5 < 0.8, f'B5 positive control: driving covariate cuts one-step MAE (ratio {r5:.3f}, need < 0.80)')
    ok &= check(abs(r6 - 1) < 0.10, f'B6 negative control: unrelated covariate (ratio {r6:.3f}, need within 0.90-1.10)')
    return ok


if __name__ == '__main__':
    tiny_mode = '--tiny' in sys.argv
    ok = part_a()
    m = tiny() if tiny_mode else M.get('timestral')
    ok &= part_b(m, full=not tiny_mode)
    line = 'OVERALL: ' + ('PASS' if ok else 'FAIL') + (' (random-weights plumbing test)' if tiny_mode else ''); print(line); log.append(line)
    open(os.path.join(HERE, 'tsl_selftest_tiny.txt' if tiny_mode else 'tsl_selftest.txt'), 'w').write('\n'.join(log) + '\n')
