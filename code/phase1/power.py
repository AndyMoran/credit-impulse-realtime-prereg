import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, sys, json
from scipy import stats
from fixedb import nw_t as _nwt
# fixed-b null distributions (Kiefer-Vogelsang), simulated once: n=78 (forecast tests), n=82 (P3)
def _null(n,lags=3,N=2000,R=20000,seed=0):
    L=int(round((lags+1)/n*N))-1; rng=np.random.default_rng(seed)
    return np.sort(np.array([_nwt(rng.standard_normal(N),L) for _ in range(R)]))
NULL78=_null(78); NULL82=np.sort(np.abs(_null(82,seed=1)))
def p_one(t): return 1-np.searchsorted(NULL78,t)/len(NULL78)
def p_two(t): return 1-np.searchsorted(NULL82,abs(t))/len(NULL82)
C=np.load('out/calib.npz'); bx,bg,bu,S=C['bx'],C['bg'],C['bu'],C['S']
SDNU=0.946         # real-time edge noise in CI (Phase 1, total revision SD)
SDF=0.5            # SPF idiosyncratic noise around the AR-information forecast (nuisance)
T=260; BURN=200; O0,O1=178,255   # 1955Q1=0; origins 1999Q3..2018Q4 (78)
SPF0=56                          # 1969Q1: first SPF survey used for correction training
H=4; LAG=6                       # credit at q*=o-2 affects target o+4
xbar=bx[0]/(1-bx[1]-bx[2])
def simulate(n,kg,ku,rng):
    L=np.linalg.cholesky(S); e=rng.standard_normal((n+BURN,3))@L.T
    x=np.zeros(n+BURN); g=np.full(n+BURN,3.1); u=np.full(n+BURN,5.9)
    for t in range(2,n+BURN):
        x[t]=bx[0]+bx[1]*x[t-1]+bx[2]*x[t-2]+e[t,0]
        c=(x[t-LAG]-xbar) if t>=LAG else 0
        g[t]=bg[0]+bg[1]*g[t-1]+bg[2]*g[t-2]+kg*c+e[t,1]
        u[t]=bu[0]+bu[1]*u[t-1]+bu[2]*u[t-2]-ku*c+e[t,2]
    return x[BURN:],g[BURN:],u[BURN:]
def rows(y,x,j):   # design for forecast made at origin j for target j+4
    return np.column_stack([np.ones(len(j)),y[j-1],y[j-2]]),x[j-2],y[j+H]
def pop_ratio(kg,ku,which,n=300000,seed=1):
    rng=np.random.default_rng(seed); x,g,u=simulate(n,kg,ku,rng); j=np.arange(8,n-H)
    y=g if which in('g','spf') else u
    Xb,xc,Y=rows(y,x,j)
    bb=np.linalg.lstsq(Xb,Y,rcond=None)[0]
    if which=='spf':
        f=Xb@bb+SDF*rng.standard_normal(len(j)); Xb=np.column_stack([np.ones(len(j)),f])
        bb=np.linalg.lstsq(Xb,Y,rcond=None)[0]
    mb=np.mean((Y-Xb@bb)**2); Xa=np.column_stack([Xb,xc]); ba=np.linalg.lstsq(Xa,Y,rcond=None)[0]
    ma=np.mean((Y-Xa@ba)**2)+ba[-1]**2*SDNU**2
    return np.sqrt(ma/mb)
def calibrate(r,which):
    if r>=1: return 0.0
    lo,hi=0.0,3.0
    for _ in range(30):
        k=(lo+hi)/2; v=pop_ratio(k if which!='u' else 0,k if which=='u' else 0,which)
        lo,hi=(k,hi) if v>r else (lo,k)
    return (lo+hi)/2
def nw_t(f,lags):
    n=len(f); d=f-f.mean(); v=d@d/n
    for l in range(1,lags+1): v+=2*(1-l/(lags+1))*(d[l:]@d[:-l])/n
    return f.mean()/np.sqrt(v/n)
def recursive_cw(Xb,Xa,Y,origins,start):
    # expanding OLS: train on rows start..o-5 (targets published by origin), forecast row o
    fb,fa=[],[]
    for o in origins:
        tr=slice(start,o-H-1+1)
        bb=np.linalg.lstsq(Xb[tr],Y[tr],rcond=None)[0]; ba=np.linalg.lstsq(Xa[tr],Y[tr],rcond=None)[0]
        fb.append(Xb[o]@bb); fa.append(Xa[o]@ba)
    fb,fa=np.array(fb),np.array(fa); y=Y[origins]
    f=(y-fb)**2-((y-fa)**2-(fb-fa)**2); t=nw_t(f,H-1)
    return p_one(t), np.sqrt(np.mean((y-fa)**2)/np.mean((y-fb)**2))
def one_rep(kg,ku,r2,rng,bpop):
    x,g,u=simulate(T,kg,ku,rng); j=np.arange(T-H); jj=np.arange(8,T-H)
    nu=SDNU*rng.standard_normal(T)            # edge noise, used only at forecast origins
    orig=np.arange(O0,O1+1); out={}
    for name,y in [('P1a',g),('P1b',u)]:
        Xb=np.zeros((T-H,3)); Xa=np.zeros((T-H,4)); Y=np.zeros(T-H)
        Xb[jj],xc,Y[jj]=rows(y,x,jj); Xa[jj]=np.column_stack([Xb[jj],xc]); Xa[orig,3]+=nu[orig]
        out[name]=recursive_cw(Xb,Xa,Y,orig,8)
    # P2a: SPF = AR-information forecast (population coefs) + idiosyncratic noise; bias-corrected benchmark
    Xg,xc,Yg=rows(g,x,jj); f=np.zeros(T-H); f[jj]=Xg@bpop+SDF*rng.standard_normal(len(jj))
    Y=np.zeros(T-H); Y[jj]=Yg; Xb=np.column_stack([np.ones(T-H),f]); Xa=np.column_stack([Xb,np.r_[np.zeros(8),xc]])
    Xa[orig,2]+=nu[orig]; out['P2a']=recursive_cw(Xb,Xa,Y,orig,SPF0)
    # P3: revision regression, one obs per quarter, n=82, two-sided HAC t
    xt=x[orig.min()-2:O1+4-2+1][:82]+nu[orig.min():O1+5][:82]; xt=xt-xt.mean()
    b=np.sqrt(r2/(1-r2))/xt.std() if r2>0 else 0
    rev=b*xt+rng.standard_normal(82); X=np.column_stack([np.ones(82),xt]); bh=np.linalg.lstsq(X,rev,rcond=None)[0]
    e=rev-X@bh; z=xt*e; n=82; d=z-z.mean(); v=d@d/n
    for l in range(1,4): v+=2*(1-l/4)*(d[l:]@d[:-l])/n
    se=np.sqrt(v/n)/np.mean(xt**2); tt=bh[1]/se
    out['P3']=(p_two(tt),None)
    return out
def holm(p,alpha=0.05):
    k=sorted(p,key=p.get); rej={t:False for t in p}
    for i,t in enumerate(k):
        if p[t]<=alpha/(len(p)-i): rej[t]=True
        else: break
    return rej
if __name__=='__main__':
    R=int(sys.argv[1]) if len(sys.argv)>1 else 2000
    grid=[1.00,0.95,0.925,0.90,0.875,0.85,0.80]; r2map={1.00:0.0,0.95:0.02,0.925:0.02,0.90:0.05,0.875:0.05,0.85:0.10,0.80:0.10}
    # population AR forecast coefs for the SPF proxy (no credit effect needed: SPF lacks credit info)
    rows_out=[]
    for r in grid:
        kg=calibrate(r,'g'); ku=calibrate(r,'u')
        rng=np.random.default_rng(int(r*1000)); xx,gg,uu=simulate(200000,kg,ku,np.random.default_rng(7))
        jj=np.arange(8,200000-H); Xb,_,Y=rows(gg,xx,jj); bpop=np.linalg.lstsq(Xb,Y,rcond=None)[0]
        ratio_spf=pop_ratio(kg,0,'spf')
        P={k:[] for k in ['P1a','P1b','P2a','P3']}; RJ={k:[] for k in P}; RAT={k:[] for k in ['P1a','P1b','P2a']}
        for rep in range(R):
            o=one_rep(kg,ku,r2map[r],rng,bpop); p={k:o[k][0] for k in o}; h=holm(p)
            for k in P: P[k].append(p[k]); RJ[k].append(h[k])
            for k in RAT: RAT[k].append(o[k][1])
        rj=pd.DataFrame(RJ); pp=pd.DataFrame(P)
        row=dict(true_ratio=r,kappa_g=kg,kappa_u=ku,spf_true_ratio=ratio_spf,p3_partialR2=r2map[r],
                 **{f'pow_{k}_unadj':(pp[k]<0.05).mean() for k in P},**{f'pow_{k}_holm':rj[k].mean() for k in P},
                 fw_any=rj.any(axis=1).mean(),fw_all=rj.all(axis=1).mean(),
                 **{f'median_oos_ratio_{k}':np.median(RAT[k]) for k in RAT})
        rows_out.append(row); print(pd.Series(row).round(3).to_dict(),flush=True)
    pd.DataFrame(rows_out).to_csv(f'out/power_results_fixedb_R{R}.csv',index=False)
