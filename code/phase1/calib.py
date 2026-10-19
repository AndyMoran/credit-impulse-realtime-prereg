import warnings; warnings.filterwarnings('ignore')
import contextlib,io
with contextlib.redirect_stdout(io.StringIO()): exec(open('build.py').read())
REV=measures(Z['current'],NO[LATEST],P[LATEST],gap=False)
x=REV.CI.loc[qn('1955Q1'):qn('2019Q4')]
ro=RO[LATEST]; g=(100*((ro/ro.shift(1))**4-1)).loc[x.index]
u=RU[max(RU)].loc[x.index]
print(len(x),g.isna().sum(),u.isna().sum(), g.mean().round(2), u.mean().round(2))
import numpy as np
def ar2(s):
    y=s.values; X=np.column_stack([np.ones(len(y)-2),y[1:-1],y[:-2]]); b=np.linalg.lstsq(X,y[2:],rcond=None)[0]; e=y[2:]-X@b; return b,e
PR={}
for k,s in [('x',x),('g',g),('u',u)]:
    b,e=ar2(s); PR[k]=b; PR[k+'_e']=e
E=np.column_stack([PR['x_e'],PR['g_e'],PR['u_e']]); S=np.cov(E.T)
print({k:np.round(PR[k],3) for k in 'xgu'}); print(np.round(S,3)); print(np.round(np.corrcoef(E.T),2))
np.savez('out/calib.npz',bx=PR['x'],bg=PR['g'],bu=PR['u'],S=S)
