"""
Plan 2: inputs at each forecast origin (plan2/PLAN.md, Sections 2-4).

Builds, from the LOCKED phase2.py and the locked data, what a forecaster had at origin o:
  - GDP growth through o-1 in the origin's real-time vintage (locked);
  - the credit impulse through q* = o-2 from the latest Z.1 release before the origin (locked);
  - the Philadelphia Fed survey, not seasonally adjusted, through the latest release strictly before the origin
    (00:00 ET on the 15th of the quarter's middle month): the first month of quarter o.

Survey covariates are quarterly series indexed by quarter number q (P's convention):
  M1[q] = reading for the first month of quarter q;  M3[q] = reading for the third month of quarter q.
Q1 uses M1 at release lag k = 0; Q4 uses M1 at k = 2; Q5 uses M3 at k = 1 (Section 5).
Seasonality, method A (Section 4): each reading minus the mean of all readings for the same calendar month
released before the origin, full pre-origin history (drift rule did not trigger; Section 13).
"""
import os, sys, hashlib, datetime as dt
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.dirname(HERE); sys.path.insert(0, P2)
LOCKED_PHASE2 = 'da697030f2349feae24dc79a3dfcbb786552b62186ffbf624a027c591814766e'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
if sha(os.path.join(P2, 'phase2.py')) != LOCKED_PHASE2: sys.exit('phase2.py is not the locked file; stopping.')
import phase2 as P

EXT = os.path.join(P2, '..', 'plan2')
DATA = os.path.join(EXT, 'data')
HORIZONS = (0, 1, 2, 4)
START = '1965Q1'                               # locked AR(2) estimation start
SURVEY = {'GA': 'GACDFNA066MNFRBPHI', 'NO': 'NOCDFNA066MNFRBPHI'}


# ------------------------------------------------------------------ GDP and credit (locked)
def load(mode='real'):
    D = P.load(mode)
    P.LAST_TARGET = D['qn']('2019Q4')          # locked COVID exclusion
    return D


def origins(D):
    qn = D['qn']; return list(range(qn('1999Q3'), qn('2018Q4') + 1))


def gdp(D, o):
    """GDP growth up to o-1 in origin o's vintage (full history, as the locked direct_forecast uses)."""
    return P.series(D, 'g', P.origin_info(D, o)['w']).loc[:o - 1]


def credit(D, o, which='rt'):
    oi = P.origin_info(D, o); cm = P.credit(D, oi['v'], oi['w'], which)
    if which != 'rt': cm = cm.loc[:oi['qstar']]
    return cm['CI'], oi['k']


def outcome(D, t):
    return P.target(D, 'g', t, 'revised')


# ------------------------------------------------------------------ survey release rule (Section 3)
def third_thursday(y, m):
    d = dt.date(y, m, 1); return d + dt.timedelta(days=(3 - d.weekday()) % 7 + 14)


def origin_date(o):
    """00:00 ET on the 15th of the middle month of quarter o (P.vint)."""
    return P.vint(o).date()


def released_before(month_ts, cut):
    """True if the survey for month `month_ts` (first of month) was released strictly before date `cut`."""
    return third_thursday(month_ts.year, month_ts.month) < cut


def load_survey(name='GA', path=None):
    path = path or os.path.join(DATA, f"{SURVEY[name]}.csv")
    s = pd.read_csv(path, parse_dates=['date']).set_index('date')['value'].astype(float)
    if s.index.min() != pd.Timestamp('1968-05-01'): raise ValueError('survey must start in May 1968')
    return s


def survey_quarterly(D, s, o, cut=None):
    """Seasonally adjusted (method A) M1 and M3 quarterly series as available at origin o.
    `cut` defaults to the origin date; Q5 passes the end of quarter o-1 instead."""
    cut = cut or origin_date(o)
    avail = s[[released_before(t, cut) for t in s.index]]
    means = avail.groupby(avail.index.month).mean()           # one mean per calendar month, pre-cut data only
    adj = avail - means.reindex(avail.index.month).values
    qn = lambda t: t.year * 4 + (t.month - 1) // 3            # P's quarter numbering
    m1 = adj[(adj.index.month - 1) % 3 == 0]; m3 = adj[(adj.index.month - 1) % 3 == 2]
    M1 = pd.Series(m1.values, index=[qn(t) for t in m1.index])
    M3 = pd.Series(m3.values, index=[qn(t) for t in m3.index])
    return M1, M3, avail.index.max()


def quarter_end(o_minus_1):
    """First day after quarter q ends, as a date (cut for Q5: end of quarter o-1)."""
    y, q = divmod(o_minus_1, 4); m = 3 * q + 4
    return dt.date(y + (m > 12), (m - 1) % 12 + 1, 1)


def release_table(D):
    rows = []
    for o in origins(D):
        od = origin_date(o); y, q = divmod(o, 4); m1 = dt.date(y, 3 * q + 1, 1); m2 = dt.date(y, 3 * q + 2, 1)
        rows.append(dict(origin=D['qs'](o), origin_date=od, month_used=m1, release=third_thursday(y, m1.month),
                         next_release=third_thursday(y, m2.month)))
    return pd.DataFrame(rows)
