"""
Plan 2 self-test, before freezing (plan2/PLAN.md, Section 9, step 3). No real GDP outcome is read.

  A. Release rule: at all 78 origins the survey month used is the first month of quarter o, released strictly before
     00:00 ET on the origin date, and the second month is never available.
  B. Seasonal adjustment uses only readings released before the origin (method A, full pre-origin history).
  C. Planted effect: synthetic GDP with a survey effect at h = 1 gives a ratio well below 1; with no effect, about 1.
  D. Shift test: forecasts move when the last GDP value or the origin's survey reading moves.
Uses the real survey file if present, otherwise a synthetic survey. Writes plan2_selftest.txt.
"""
import os, sys, datetime as dt
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan2_data as T, plan2_models as M, plan2_power as PW
P = T.P
log = []
def check(ok, msg): line = ('PASS  ' if ok else 'FAIL  ') + msg; print(line, flush=True); log.append(line); return bool(ok)


def main():
    D = T.load('synthetic'); ok = True
    f = os.path.join(T.DATA, 'GACDFNA066MNFRBPHI.csv')
    if os.path.exists(f): s = T.load_survey('GA'); log.append('INFO  real survey file')
    else:
        idx = pd.date_range('1968-05-01', '2019-12-01', freq='MS')
        s = pd.Series(np.random.default_rng(7).normal(10, 20, len(idx)), index=idx); log.append('INFO  synthetic survey')
    # A
    R = T.release_table(D)
    ok &= check(len(R) == 78 and all(r.release < r.origin_date <= r.next_release for r in R.itertuples())
                and all(r.month_used.month in (1, 4, 7, 10) for r in R.itertuples()),
                'release rule: first month of quarter o at all 78 origins; second month never before the origin')
    # B
    bad = 0
    for o in T.origins(D):
        _, _, last = T.survey_quarterly(D, s, o); y, q = divmod(o, 4)
        bad += last != pd.Timestamp(y, 3 * q + 1, 1)
    ok &= check(bad == 0, 'latest survey month available at each origin is the first month of quarter o')
    o = T.origins(D)[0]; M1a, _, _ = T.survey_quarterly(D, s, o)
    s2 = s.copy(); s2[s2.index > pd.Timestamp(T.origin_date(o))] += 1000          # change only post-origin data
    M1b, _, _ = T.survey_quarterly(D, s2, o)
    ok &= check(np.allclose(M1a.values, M1b.reindex(M1a.index).values), 'seasonal adjustment ignores data after the origin')
    # C
    M1_full, ci_full, sb, cb = PW.paths(D, s)
    r0 = PW.mean_ratio(D, M1_full, 1, sb, 1, 0.0, 20, 11)
    r1 = PW.mean_ratio(D, M1_full, 1, sb, 1, 0.15, 20, 11)
    ok &= check(0.98 < r0 < 1.06, f'no planted effect: mean ratio {r0:.3f} (about 1)')
    ok &= check(r1 < 0.95, f'planted survey effect: mean ratio {r1:.3f} (well below 1)')
    # D
    o = T.origins(D)[-1]; y = PW.simulate(M1_full, 1, 0.0, np.random.default_rng(3), D['qn']('1960Q1'), o - 1)
    start = D['qn'](T.START); blk = sb[o]; f0, _, _ = M.fit(y, [blk], o, 1, start)
    y2 = y.copy(); y2[o - 1] += 10; f1, _, _ = M.fit(y2, [blk], o, 1, start)
    X2 = blk[0].copy(); X2[o] += 10; f2, _, _ = M.fit(y, [(X2, 0, 1)], o, 1, start)
    ok &= check(abs(f1['all'] - f0['all']) > 1e-6 and abs(f2['all'] - f0['all']) > 1e-6,
                'forecast responds to the last GDP value and to the origin survey reading')
    line = 'OVERALL: ' + ('PASS' if ok else 'FAIL'); print(line); log.append(line)
    open(os.path.join(HERE, 'plan2_selftest.txt'), 'w').write('\n'.join(log) + '\n')


if __name__ == '__main__':
    main()
