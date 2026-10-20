"""Post-lock (Entry 30): calibrate the nominal level of the locked block-bootstrap RMSE-ratio interval so that it
achieves 90% coverage on synthetic outcomes with the real credit path. No real outcome is read here."""
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd, phase2 as P, test_phase2 as T
LEVELS = [0.90, 0.93, 0.95, 0.97, 0.98, 0.99]
D0 = P.load('synthetic'); qn = D0['qn']; O = list(range(qn('1999Q3'), qn('2018Q4') + 1))
R, OFF = int(sys.argv[1]), int(sys.argv[2]); rows = []
def boot_q(d):
    rng = np.random.default_rng(P.SEED); n = len(d)
    v = np.array([P.rmse_ratio(d.y, d.fb, d.fa, P.block_boot_idx(n, rng)) for _ in range(P.BOOT_B)])
    return {f'{s}{L}': np.quantile(v, (1 - L) / 2 if s == 'lo' else 1 - (1 - L) / 2) for L in LEVELS for s in ('lo', 'hi')}
for kg, ku, b3 in [(0.0, 0.0, 0.0), (0.25, 0.015, 0.25)]:
    for sd in range(OFF, OFF + R):
        D = T.synth(D0, kg, ku, b3, 9100 + sd)
        for name, d in (('P1a', P.run_p1(D, 'g', O)), ('P1b', P.run_p1(D, 'u', O)), ('P2a', P.run_p2(D, 'g', O))):
            rows.append(dict(kg=kg, sd=sd, test=name, mse_a=np.mean((d.y - d.fa) ** 2), mse_b=np.mean((d.y - d.fb) ** 2),
                             ratio=P.rmse_ratio(d.y, d.fb, d.fa), **boot_q(d)))
    print('done', kg, flush=True)
pd.DataFrame(rows).to_csv(os.path.join(HERE, 'out', f'calib_{OFF}.csv'), index=False)
