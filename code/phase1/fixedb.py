# Fixed-b critical values (Kiefer-Vogelsang) for the Bartlett-kernel NW t-stat used in power.py,
# simulated directly: large-T i.i.d. normal series, bandwidth M=(lags+1) scaled as b=M/n_actual.
import numpy as np
def nw_t(f,lags):
    n=len(f); d=f-f.mean(); v=d@d/n
    for l in range(1,lags+1): v+=2*(1-l/(lags+1))*(d[l:]@d[:-l])/n
    return f.mean()/np.sqrt(v/n)
def cv(n_actual,lags,N=2000,R=20000,seed=0):
    b=(lags+1)/n_actual; L=int(round(b*N))-1; rng=np.random.default_rng(seed)
    t=np.array([nw_t(rng.standard_normal(N),L) for _ in range(R)])
    return b,np.quantile(t,0.95),np.quantile(np.abs(t),0.95)
if __name__=='__main__':
  for n in (78,82):
    b,c1,c2=cv(n,3); print(n,round(b,4),'one-sided 5%:',round(c1,3),' two-sided 5%:',round(c2,3))
