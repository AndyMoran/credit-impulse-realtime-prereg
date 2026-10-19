# Power simulation v2: matches protocol v2.3 sections 6, 8 and 9 exactly (see audit Entry 16).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from fixedb import nw_t
C=np.load('out/calib.npz'); bx,bg,bu,S=C['bx'],C['bg'],C['bu'],C['S']
SDNU=0.946; SDF=0.5
T=260; BURN=200; O0,O1=178,255          # t=0 is 1955Q1; origins 1999Q3..2018Q4 (78)
EST0=40                                 # 1965Q1: start of estimation (protocol section 8)
SPF0=142                                # 1990Q3: first SPF survey usable (protocol section 8)
P3_0,P3_N=177,83                        # P3 quarters 1999Q2..2019Q4, one observation each
H=4; K=2; NL=4; LAG=6                   # q* = o-2; credit lags j=0..3; true effect via CI_{o-2}
xbar=bx[0]/(1-bx[1]-bx[2])
def null(n,lags,N=2000,R=20000,seed=0):
    L=int(round((lags+1)/n*N))-1; rng=np.random.default_rng(seed)
    return np.sort(np.array([nw_t(rng.standard_normal(N),L) for _ in range(R)]))
NULL_CW=null(78,3); NULL_P3=np.sort(np.abs(null(P3_N,4,seed=1)))
p_one=lambda t:1-np.searchsorted(NULL_CW,t)/len(NULL_CW)
p_two=lambda t:1-np.searchsorted(NULL_P3,abs(t))/len(NULL_P3)
def simulate(n,kg,ku,rng):
    L=np.linalg.cholesky(S); e=rng.standard_normal((n+BURN,3))@L.T
    x=np.zeros(n+BURN); g=np.full(n+BURN,3.1); u=np.full(n+BURN,5.9)
    for t in range(2,n+BURN):
        x[t]=bx[0]+bx[1]*x[t-1]+bx[2]*x[t-2]+e[t,0]
        c=(x[t-LAG]-xbar) if t>=LAG else 0
        g[t]=bg[0]+bg[1]*g[t-1]+bg[2]*g[t-2]+kg*c+e[t,1]
        u[t]=bu[0]+bu[1]*u[t-1]+bu[2]*u[t-2]-ku*c+e[t,2]
    return x[BURN:],g[BURN:],u[BURN:]
def design(y,x,j):   # direct AR(2) and ADL with CI_{q*-0..3}, q*=j-K
    Xb=np.column_stack([np.ones(len(j)),y[j-1],y[j-2]])
    Xc=np.column_stack([x[j-K-l] for l in range(NL)])
    return Xb,Xc,y[j+H]
def pop_ratio(k,which,n=300000,seed=1):
    rng=np.random.default_rng(seed); x,g,u=simulate(n,k if which!='u' else 0,k if which=='u' else 0,rng)
    j=np.arange(10,n-H); y=u if which=='u' else g; Xb,Xc,Y=design(y,x,j)
    if which=='spf':
        bb=np.linalg.lstsq(Xb,Y,rcond=None)[0]; f=Xb@bb+SDF*rng.standard_normal(len(j))
        Yd=Y-f; mb=np.var(Yd); X=np.column_stack([np.ones(len(j)),Xc[:,0]])
        ba=np.linalg.lstsq(X,Yd,rcond=None)[0]; ma=np.mean((Yd-X@ba)**2)+ba[1]**2*SDNU**2
        return np.sqrt(ma/mb)
    bb=np.linalg.lstsq(Xb,Y,rcond=None)[0]; mb=np.mean((Y-Xb@bb)**2)
    Xa=np.column_stack([Xb,Xc]); ba=np.linalg.lstsq(Xa,Y,rcond=None)[0]
    ma=np.mean((Y-Xa@ba)**2)+ba[3]**2*SDNU**2          # edge noise hits the q* lag only
    return np.sqrt(ma/mb)
def calibrate(r,which):
    if r>=1: return 0.0
    lo,hi=0.0,4.0
    for _ in range(30):
        k=(lo+hi)/2; lo,hi=(k,hi) if pop_ratio(k,which)>r else (lo,k)
    return (lo+hi)/2
def cw(Xb,Xa,Y,orig,start):
    fb,fa=[],[]
    for o in orig:
        tr=slice(start,o-H)                          # targets j+4 <= o-1
        fb.append(Xb[o]@np.linalg.lstsq(Xb[tr],Y[tr],rcond=None)[0]); fa.append(Xa[o]@np.linalg.lstsq(Xa[tr],Y[tr],rcond=None)[0])
    fb,fa=np.array(fb),np.array(fa); y=Y[orig]
    f=(y-fb)**2-((y-fa)**2-(fb-fa)**2)
    return p_one(nw_t(f,H-1)), np.sqrt(np.mean((y-fa)**2)/np.mean((y-fb)**2))
def one_rep(kg,ku,r2,rng,bpop):
    x,g,u=simulate(T,kg,ku,rng); nu=SDNU*rng.standard_normal(T); orig=np.arange(O0,O1+1)
    j=np.arange(10,T-H); out={}
    for name,y in [('P1a',g),('P1b',u)]:
        Xb=np.zeros((T-H,3)); Xc=np.zeros((T-H,NL)); Y=np.zeros(T-H)
        Xb[j],Xc[j],Y[j]=design(y,x,j); Xc[orig,0]+=nu[orig]          # real-time noise at the edge
        out[name]=cw(Xb,np.column_stack([Xb,Xc]),Y,orig,EST0)
    Xb=np.zeros((T-H,3)); Xc=np.zeros((T-H,NL)); Y=np.zeros(T-H); Xb[j],Xc[j],Y[j]=design(g,x,j)
    f=Xb@bpop+SDF*rng.standard_normal(T-H); Yd=Y-f                     # SPF error
    c=Xc[:,0].copy(); c[orig]+=nu[orig]
    out['P2a']=cw(np.ones((T-H,1)),np.column_stack([np.ones(T-H),c]),Yd,orig,SPF0)
    s=np.arange(P3_0,P3_0+P3_N); xt=x[s-1]+nu[s]                       # CI covering s-1, as published
    b=np.sqrt(r2/(1-r2))/xt.std() if r2>0 else 0
    rev=b*(xt-xt.mean())+rng.standard_normal(P3_N)
    X=np.column_stack([np.ones(P3_N),xt,g[s],g[s-1]]); bh,*_=np.linalg.lstsq(X,rev,rcond=None); e=rev-X@bh
    XtXi=np.linalg.inv(X.T@X); z=X*e[:,None]; Sh=z.T@z
    for l in range(1,5): G=z[l:].T@z[:-l]; Sh+=(1-l/5)*(G+G.T)
    tt=bh[1]/np.sqrt((XtXi@Sh@XtXi)[1,1]); out['P3']=(p_two(tt),None)
    return out
def holm(p,a=0.05):
    rej={t:False for t in p}
    for i,t in enumerate(sorted(p,key=p.get)):
        if p[t]<=a/(len(p)-i): rej[t]=True
        else: break
    return rej
if __name__=='__main__':
    R=int(sys.argv[1]) if len(sys.argv)>1 else 2000
    grid=[1.00,0.95,0.925,0.90,0.875,0.85,0.80]; r2map={1.00:0,0.95:0.02,0.925:0.02,0.90:0.05,0.875:0.05,0.85:0.10,0.80:0.10}
    res=[]
    for r in grid:
        kg,ku=calibrate(r,'g'),calibrate(r,'u')
        xx,gg,_=simulate(200000,kg,0,np.random.default_rng(7)); jj=np.arange(10,200000-H)
        Xb,_,Y=design(gg,xx,jj); bpop=np.linalg.lstsq(Xb,Y,rcond=None)[0]
        rng=np.random.default_rng(int(r*1000)); P={k:[] for k in ['P1a','P1b','P2a','P3']}; RJ={k:[] for k in P}; RAT={k:[] for k in ['P1a','P1b','P2a']}
        for _ in range(R):
            o=one_rep(kg,ku,r2map[r],rng,bpop); p={k:o[k][0] for k in o}; h=holm(p)
            for k in P: P[k].append(p[k]); RJ[k].append(h[k])
            for k in RAT: RAT[k].append(o[k][1])
        rj=pd.DataFrame(RJ); pp=pd.DataFrame(P)
        row=dict(true_ratio=r,kappa_g=kg,kappa_u=ku,spf_ratio_at_kg=pop_ratio(kg,'spf'),p3_partialR2=r2map[r],
                 **{f'pow_{k}_unadj':(pp[k]<0.05).mean() for k in P},**{f'pow_{k}_holm':rj[k].mean() for k in P},
                 fw_any=rj.any(axis=1).mean(),fw_all=rj.all(axis=1).mean(),**{f'median_oos_ratio_{k}':np.median(RAT[k]) for k in RAT})
        res.append(row); print({k:round(v,3) for k,v in row.items()},flush=True)
    pd.DataFrame(res).to_csv(f'out/power2_results_R{R}.csv',index=False)
