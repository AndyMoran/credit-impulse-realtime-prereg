"""Power conditional on the actual (revised) credit path: targets simulated, credit real. No real outcome is read."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, phase2 as P, test_phase2 as T
D0=P.load('synthetic'); qn=D0['qn']; O=list(range(qn('1999Q3'),qn('2018Q4')+1)); Q3=list(range(qn('1999Q2'),qn('2019Q4')+1))
R=int(sys.argv[1]) if len(sys.argv)>1 else 200
rows=[]
for kg,ku,b3 in [(0,0,0),(0.15,0.008,0.15),(0.25,0.015,0.25),(0.35,0.02,0.35),(0.5,0.03,0.5)]:
    for sd in range(R):
        D=T.synth(D0,kg,ku,b3,5000+sd)
        a=P.run_p1(D,'g',O); b=P.run_p1(D,'u',O); c=P.run_p2(D,'g',O); _,p3=P.run_p3(D,Q3)
        r={'P1a':P.clark_west(a.y,a.fb,a.fa,4),'P1b':P.clark_west(b.y,b.fb,b.fa,4),'P2a':P.clark_west(c.y,c.fb,c.fa,4)}
        p={k:v['p'] for k,v in r.items()}; p['P3']=p3['p']; h=P.holm(p)
        rows.append(dict(kg=kg,**{f'p_{k}':v for k,v in p.items()},**{f'holm_{k}':h[k] for k in p},
                         **{f'ratio_{k}':v['ratio'] for k,v in r.items()}))
    d=pd.DataFrame(rows); s=d[d.kg==kg]
    print(kg, 'median ratios', s[[c for c in s if c.startswith('ratio')]].median().round(3).to_dict(),
          'holm power', s[[c for c in s if c.startswith('holm')]].mean().round(3).to_dict(),
          'unadj', (s[[c for c in s if c.startswith('p_')]]<0.05).mean().round(3).to_dict(), flush=True)
pd.DataFrame(rows).to_csv('power_realpath.csv',index=False)
