"""Table 4 (manuscript): contributions to the cumulative squared-error gain by origin period, from the locked
forecast tables. Positive = credit helps. Descriptive; no estimation."""
import os, pandas as pd
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results_real')
qn = lambda q: int(q[:4]) * 4 + int(q[-1]) - 1
periods = [('1999Q3', '2006Q4'), ('2007Q1', '2009Q4'), ('2010Q1', '2011Q4'), ('2012Q1', '2018Q4')]
rows = {}
for t in ('P1a', 'P1b', 'P2a'):
    d = pd.read_csv(os.path.join(R, f'{t}_forecasts.csv')); g = (d.y - d.fb) ** 2 - (d.y - d.fa) ** 2
    rows[t] = [g[(d.o >= qn(a)) & (d.o <= qn(b))].sum() for a, b in periods] + [g.sum()]
out = pd.DataFrame(rows, index=[f'{a}-{b}' for a, b in periods] + ['Total'])
print(out.round(2)); out.round(4).to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'table4_contributions.csv'))
