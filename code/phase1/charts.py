import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def qn(q): return int(q[:4])*4+int(q[-1])-1
def x(q): t=q.map(qn); return t/4+0.125
FR=pd.read_csv('out/first_release_vs_revised.csv'); D=pd.read_csv('out/gap_decomposition_D2.csv')
REC=[(2001.25,2002.0),(2008.0,2009.5)]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
C={'rt':'#c0392b','rev':'#1f3b73','mid':'#7f8c8d'}
def shade(ax):
    for a,b in REC: ax.axvspan(a,b,color='#e5e5e5',lw=0)
    ax.axhline(0,color='#999',lw=.6)
fig,axs=plt.subplots(2,1,figsize=(9,7.5),sharex=True)
for ax,k,ttl in [(axs[0],'CI','Credit impulse, % of GDP (change in 4-qtr flow)'),(axs[1],'CG','Credit growth, % y/y (stocks)')]:
    shade(ax); xx=x(FR.quarter)
    ax.plot(xx,FR[f'{k}_rev'],color=C['rev'],lw=1.8,label='Revised (Z.1 Sep 2026)')
    ax.plot(xx,FR[f'{k}_rt'],color=C['rt'],lw=1.4,ls='--',label='First release (real time)')
    ax.set_title(ttl,loc='left',fontsize=11)
axs[0].legend(frameon=False,loc='lower left'); axs[1].set_xlim(1999,2020); axs[1].set_xticks(range(2000,2021,2))
fig.suptitle('Household + nonfinancial business credit: first release vs revised, 1999Q1–2019Q3',x=0.02,ha='left',fontsize=12,weight='bold')
fig.text(0.02,0.01,'Grey = NBER recessions. Each first-release point is the newest quarter in the Z.1 release that first published it. Source: Fed Z.1 archive, Philadelphia Fed RTDSM.',fontsize=8,color='#555')
fig.tight_layout(rect=(0,0.03,1,0.96)); fig.savefig('out/fig1_first_release_vs_revised.png',dpi=160)
fig,axs=plt.subplots(2,1,figsize=(9,7.5),sharex=True,gridspec_kw={'height_ratios':[3,2]})
xx=x(D.quarter); ax=axs[0]; shade(ax)
ax.plot(xx,D.GAP_final,color=C['rev'],lw=1.8,label='Final (two-sided HP, data to 2019Q4)')
ax.plot(xx,D.GAP_qrt,color=C['mid'],lw=1.4,label='Quasi-real-time (latest data, one-sided)')
ax.plot(xx,D.GAP_rt,color=C['rt'],lw=1.4,ls='--',label='Real time (vintage data, one-sided)')
ax.set_title('Credit-to-GDP gap, pp',loc='left',fontsize=11); ax.legend(frameon=False,fontsize=9,loc='lower left')
ax=axs[1]; shade(ax)
ax.bar(xx-0.06,D.data_part,width=0.12,color=C['rt'],label='Data revisions (quasi-real-time − real time)')
ax.bar(xx+0.06,D.filter_part,width=0.12,color=C['rev'],label='End-point filter (final − quasi-real-time)')
ax.set_title('Decomposition of total revision (D2), pp',loc='left',fontsize=11); ax.legend(frameon=False,fontsize=9,loc='upper left',bbox_to_anchor=(0,1.0)); ax.set_ylim(-10,22); ax.set_xlim(1999,2020); ax.set_xticks(range(2000,2021,2))
fig.suptitle('The gap is unreliable because of the filter, not the data',x=0.02,ha='left',fontsize=12,weight='bold')
fig.text(0.02,0.01,'HP λ = 400,000. Filter end-point revision explains ~all of the total revision variance; data revisions ~3%.',fontsize=8,color='#555')
fig.tight_layout(rect=(0,0.03,1,0.96)); fig.savefig('out/fig2_gap_decomposition_D2.png',dpi=160)
