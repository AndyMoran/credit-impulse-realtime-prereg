"""Phase 1 build: real-time credit dataset (descriptive only; no forecasting)."""
import numpy as np, pandas as pd, scipy.sparse as sp, scipy.sparse.linalg as spl, datetime as dt
D='data/'
def qn(q): return int(q[:4])*4+int(q[-1])-1          # '1999Q1' -> int
def qs(n): return f"{n//4}Q{n%4+1}"
# ---------- Z.1 credit vintages ----------
c=pd.read_csv(D+'credit_vintages_long.csv')
log=pd.read_csv(D+'download_log.csv'); rel=dict(zip(log.folder.astype(str),log.release_date))
rel['current']='2026-09-11'   # current Z.1 at download (19 Oct 2026): Sept 11, 2026 release, data to 2026Q2
c['rel']=pd.to_datetime(c.vintage_folder.astype(str).map(rel)); c['t']=c.quarter.map(qn)
START=qn('1953Q1'); c=c[c.t>=START]
Z={}  # vintage folder -> DataFrame indexed by t with F (quarterly flow, $bn), L (level, $bn)
for v,g in c.groupby('vintage_folder'):
    w=g.pivot_table(index='t',columns='concept',values='value_bn')
    Z[str(v)]=pd.DataFrame({'F':(w.hh_flow_saar+w.nfb_flow_saar)/4.0,'L':w.hh_level_sa+w.nfb_level_sa,
                            'Fhh':w.hh_flow_saar/4,'Fnfb':w.nfb_flow_saar/4}).sort_index()
zv=sorted([k for k in Z if k!='current'],key=lambda k:rel[k])
# ---------- RTDSM vintages ----------
def rtdsm(f,col0):
    x=pd.read_excel(D+f,header=0); x=x.set_index('DATE')
    out={}
    for col in x.columns:
        yy=int(col[-4:-2]); q=int(col[-1]); yr=(1900 if yy>=65 else 2000)+yy
        vdate=pd.Timestamp(yr,3*q-1,15)
        s=pd.to_numeric(x[col],errors='coerce').dropna()
        out[vdate]=s
    return out
def qindex(s):  # '1947:Q1' -> t
    return s.rename(index=lambda d:int(d[:4])*4+int(d[-1])-1)
NO={k:qindex(v) for k,v in rtdsm('NOUTPUTQvQd.xlsx','NOUTPUT').items()}
P ={k:qindex(v) for k,v in rtdsm('PQvQd.xlsx','P').items()}
RO={k:qindex(v) for k,v in rtdsm('ROUTPUTQvQd.xlsx','ROUTPUT').items()}
RU0=rtdsm('rucQvMd.xlsx','RUC')
def ruc_q(s):  # monthly 'YYYY:MM' -> quarterly average, complete quarters only
    m=s.copy(); m.index=[int(d[:4])*4+(int(d[5:7])-1)//3 for d in m.index]
    g=m.groupby(level=0); return g.mean()[g.count()==3]
RU={k:ruc_q(v) for k,v in RU0.items()}
rv=sorted(NO)  # RTDSM vintage dates
def rt_before(date):
    prior=[d for d in rv if d<date]; return prior[-1]
LATEST=rv[-1]
# ---------- measures within one (credit vintage, GDP vintage) ----------
def hp_trend(y,lam=4e5):
    n=len(y); Dm=sp.diags([1,-2,1],[0,1,2],shape=(n-2,n)); A=sp.eye(n)+lam*(Dm.T@Dm)
    return spl.spsolve(A.tocsc(),y)
def onesided_gap(R):
    vals=R.values; out=np.full(len(vals),np.nan)
    for i in range(len(vals)):
        if i>=40: out[i]=vals[i]-hp_trend(vals[:i+1])[-1]   # need >=10y of history
    return pd.Series(out,index=R.index)
def measures(z,nom,pr,gap=True,last=None):
    t=z.index; last=last or t.max()
    N=nom.reindex(t)/4.0; N4=N.rolling(4).sum()          # 4-quarter nominal GDP, $bn
    S=z.F.rolling(4).sum()
    m=pd.DataFrame(index=t)
    m['CI']=100*(S-S.shift(4))/N4
    m['CG']=100*(z.L/z.L.shift(4)-1)
    m['R']=100*z.L/N4
    m['RCG']=100*((z.L/z.L.shift(4))/(pr.reindex(t)/pr.reindex(t).shift(4))-1)
    m['CI_lev']=100*((z.L-z.L.shift(4))-(z.L.shift(4)-z.L.shift(8)))/N4   # robustness: stock differences
    if gap: m['GAP']=onesided_gap(m.R.dropna()).reindex(t)
    return m.loc[:last]
