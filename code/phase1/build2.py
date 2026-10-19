exec(open('build.py').read())
import os; os.makedirs('out',exist_ok=True)
# ---- origin-release table: origins 1999Q3..2019Q4 (RTDSM vintage dates) ----
rows=[]
for o in range(qn('1999Q3'),qn('2019Q4')+1):
    od=pd.Timestamp(o//4,3*(o%4+1)-1,15)
    prior=[v for v in zv if pd.Timestamp(rel[v])<od]; v=prior[-1]; qstar=Z[v].index.max()
    rows.append(dict(origin=qs(o),origin_date=od.date(),z1_release=rel[v],z1_folder=v,q_star=qs(qstar),k=o-qstar))
OT=pd.DataFrame(rows); OT.to_csv('out/origin_release_table.csv',index=False)
print(OT.k.value_counts().to_dict(), OT.iloc[[0,-1]].to_string())
# ---- real-time vintage matrix: every Z.1 vintage with its contemporaneous GDP vintage ----
VM=[]
for v in zv:
    w=rt_before(pd.Timestamp(rel[v])); m=measures(Z[v],NO[w],P[w])
    m=m.assign(z1_folder=v,z1_release=rel[v],gdp_vintage=w.date(),quarter=[qs(t) for t in m.index]); VM.append(m)
VM=pd.concat(VM); VM.reset_index(drop=True).to_csv('out/credit_measures_by_vintage.csv',index=False)
# ---- revised: current Z.1 + latest GDP vintage; and credit-revised/real-time-denominator ----
REV=measures(Z['current'],NO[LATEST],P[LATEST])
# first-release (diagonal) series: value for quarter q* from the vintage that first published it
FR=[]
for v in zv:
    w=rt_before(pd.Timestamp(rel[v])); qstar=Z[v].index.max()
    rt=VM[(VM.z1_folder==v)].set_index(VM[(VM.z1_folder==v)].quarter.map(qn)).loc[qstar]
    # credit revised, denominator & deflator real-time (isolates credit-data revisions, protocol S1)
    cr=measures(Z['current'].loc[:qstar],NO[w],P[w],gap=False).loc[qstar]
    FR.append(dict(quarter=qs(qstar),z1_release=rel[v],gdp_vintage=w.date(),
      **{f'{k}_rt':rt[k] for k in ['CI','CG','RCG','GAP','R','CI_lev']},
      **{f'{k}_credrev':cr[k] for k in ['CI','CG','RCG','CI_lev']},
      **{f'{k}_rev':REV.loc[qstar,k] for k in ['CI','CG','RCG','GAP','R','CI_lev']}))
FR=pd.DataFrame(FR); FR.to_csv('out/first_release_vs_revised.csv',index=False)
REV.assign(quarter=[qs(t) for t in REV.index]).to_csv('out/credit_measures_revised.csv',index=False)
print(FR[['quarter','CI_rt','CI_credrev','CI_rev','GAP_rt','GAP_rev']].round(2).iloc[[0,20,36,38,40,45,-1]].to_string())
