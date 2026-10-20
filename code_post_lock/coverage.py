"""Post-lock diagnostic (synthetic targets, real credit path; no real outcome read).
Coverage of the locked block-bootstrap 90% RMSE-ratio interval for P1a, full sample and the S6 halves.
Usage: python coverage.py R OFFSET   (the published run used 150 0 and 150 150 in parallel); writes out/coverage_<OFFSET>.csv"""
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))  # run from p2/post_lock/
import numpy as np, pandas as pd, phase2 as P, test_phase2 as T
D0=P.load('synthetic'); qn=D0['qn']; O=list(range(qn('1999Q3'),qn('2018Q4')+1)); cut=qn('2008Q4')
R=int(sys.argv[1]); OFF=int(sys.argv[2]); rows=[]
for kg in (0.0,0.15,0.25):
    for sd in range(OFF,OFF+R):
        D=T.synth(D0,kg,0.008,0.15,7000+sd); a=P.run_p1(D,'g',O).reset_index(drop=True)
        for part,m in (('full',np.ones(len(a),bool)),('pre',(a.o<cut).values),('post',(a.o>=cut).values)):
            d=a[m].reset_index(drop=True)
            lo,hi=P.boot_interval(lambda idx,d=d: P.rmse_ratio(d.y,d.fb,d.fa,idx),len(d))
            rows.append(dict(kg=kg,sd=sd,part=part,mse_a=np.mean((d.y-d.fa)**2),mse_b=np.mean((d.y-d.fb)**2),
                             ratio=P.rmse_ratio(d.y,d.fb,d.fa),lo=lo,hi=hi))
    print('done',kg,flush=True)
d=pd.DataFrame(rows); d.to_csv(os.path.join(HERE,"out",f"coverage_{OFF}.csv"),index=False)
for (kg,part),s in d.groupby(['kg','part']):
    true=np.sqrt(s.mse_a.mean()/s.mse_b.mean())
    print(f"kappa={kg} {part:4s} true={true:.3f} median={s.ratio.median():.3f} coverage={((s.lo<=true)&(true<=s.hi)).mean():.2f} "
          f"whole<1={(s.hi<1).mean():.2f} whole>1={(s.lo>1).mean():.2f} medwidth={(s.hi-s.lo).median():.3f}")
