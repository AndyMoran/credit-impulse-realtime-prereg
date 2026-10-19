"""False 'credible improvement' rate of the block-bootstrap ratio interval under the null, real credit path."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, phase2 as P, test_phase2 as T
D0=P.load('synthetic'); qn=D0['qn']; O=list(range(qn('1999Q3'),qn('2018Q4')+1)); out=[]
for kg in (0.0, 0.35):
    for sd in range(int(sys.argv[1])):
        D=T.synth(D0,kg,kg*0.06,0,7000+sd)
        for name,d in (('P1a',P.run_p1(D,'g',O)),('P1b',P.run_p1(D,'u',O)),('P2a',P.run_p2(D,'g',O))):
            lo,hi=P.boot_interval(lambda idx,a=d:P.rmse_ratio(a.y,a.fb,a.fa,idx),len(d),B=500,seed=sd)
            out.append(dict(kg=kg,test=name,credible=hi<1,ratio=P.rmse_ratio(d.y,d.fb,d.fa)))
d=pd.DataFrame(out); print(d.groupby(['kg','test']).agg(credible=('credible','mean'),median_ratio=('ratio','median')).round(3))
