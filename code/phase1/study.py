import warnings; warnings.filterwarnings('ignore')
exec(open('build.py').read())
FR=pd.read_csv('out/first_release_vs_revised.csv'); FR['t']=FR.quarter.map(qn)
REC={qn(q) for q in ['2001Q2','2001Q3','2001Q4']+[f'{y}Q{i}' for y,i in [(2008,1),(2008,2),(2008,3),(2008,4),(2009,1),(2009,2)]]}
FR['rec']=FR.t.isin(REC)
def stats(rt,rev,mask=None):
    d=pd.DataFrame({'rt':rt,'rev':rev}).dropna()
    if mask is not None: d=d[mask.reindex(d.index).values]
    r=d.rev-d.rt
    return dict(n=len(d),mean_rev=r.mean(),sd_rev=r.std(),sd_final=d.rev.std(),
                noise_signal=r.std()/d.rev.std(),corr=d.rt.corr(d.rev),
                sign_agree=(np.sign(d.rt)==np.sign(d.rev)).mean(),mean_abs_rev=r.abs().mean())
out=[]
for k in ['CI','CG','RCG','GAP','CI_lev']:
    for label,col in [('total',f'{k}_rev'),('credit_only',f'{k}_credrev')]:
        if col not in FR: continue
        for sub,m in [('all',None),('recession',FR.rec),('expansion',~FR.rec)]:
            out.append(dict(measure=k,revision=label,subsample=sub,**stats(FR[f'{k}_rt'],FR[col],m)))
RS=pd.DataFrame(out); RS.to_csv('out/revision_stats.csv',index=False)
print(RS[RS.subsample=='all'].round(3).to_string(index=False))
print(RS[(RS.revision=='total')&(RS.subsample!='all')][['measure','subsample','n','mean_rev','noise_signal','corr','sign_agree']].round(3).to_string(index=False))
# ---------- D2: gap decomposition (Edge-Meisenzahl style) ----------
REV=measures(Z['current'],NO[LATEST],P[LATEST])
Rf=REV.R.dropna(); Rf19=Rf.loc[:qn('2019Q4')]
final19=pd.Series(Rf19.values-hp_trend(Rf19.values),index=Rf19.index)
finalall=pd.Series(Rf.values-hp_trend(Rf.values),index=Rf.index)
D=FR.set_index('t')[['quarter','GAP_rt','GAP_rev']].rename(columns={'GAP_rev':'GAP_qrt'})
D['GAP_final']=final19.reindex(D.index); D['GAP_final_to2026']=finalall.reindex(D.index)
D['data_part']=D.GAP_qrt-D.GAP_rt; D['filter_part']=D.GAP_final-D.GAP_qrt; D['total']=D.GAP_final-D.GAP_rt
D.to_csv('out/gap_decomposition_D2.csv',index=False)
v=D[['data_part','filter_part','total']].var()
cov=D[['data_part','filter_part']].cov().iloc[0,1]
print('\nD2 var(total)=%.2f  data share=%.2f  filter share=%.2f  2cov share=%.2f'%(v.total,v.data_part/v.total,v.filter_part/v.total,2*cov/v.total))
print('mean |data|=%.2f mean |filter|=%.2f  corr(rt,final)=%.2f corr(qrt,final)=%.2f sign(rt,final)=%.2f'%(
  D.data_part.abs().mean(),D.filter_part.abs().mean(),D.GAP_rt.corr(D.GAP_final),D.GAP_qrt.corr(D.GAP_final),(np.sign(D.GAP_rt)==np.sign(D.GAP_final)).mean()))
print('final to-2026 vs to-2019 max abs diff over 1999-2019: %.2f'%(D.GAP_final_to2026-D.GAP_final).abs().max())
