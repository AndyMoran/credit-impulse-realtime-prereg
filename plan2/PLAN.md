# Plan 2: At which horizon does the Manufacturing Business Outlook Survey earn its place beside an AR(2)? Real-time US GDP, 1999–2019

Analysis plan · frozen 29 October 2026 at tag `plan2` · Andy Moran (Heaviside Analytics)

> **Status.** Drafted after the feasibility check in `plan2/feasibility/` (commit d2df844) and before any Plan 2 model has been fitted to real data. The plan will be committed and tagged before the first real run, and the tag's timestamp is the evidence of timing.
>
> **What is already known.** The author knows the locked study's results, including the four-quarter-ahead credit result (h = 4), and the TimesFM extension. The author has seen the Philadelphia Fed survey indexes only in the feasibility check, which compared vintages and fitted nothing. No forecast using the survey, and no credit forecast at h = 0, 1 or 2, has been computed.

## 1. The question, and what the answer can and cannot show

The locked study found that the real-time credit impulse did not improve an AR(2)'s forecast of US GDP growth four quarters ahead. This plan asks where that null sits in a wider pattern:

1. **Does a timely survey of manufacturers improve the AR(2) at short horizons?**
2. **Does its contribution fade as the horizon lengthens?**
3. **Does the credit impulse help at any horizon shorter than four quarters?**

What it can show:

- whether the prespecified survey indicators (General Activity, and New Orders as a secondary) available at each forecast date add to an AR(2), and at which horizons;
- whether the credit null at h = 4 also holds at shorter horizons.

What it cannot show:

- **Why the AR(2) is hard to beat a year ahead.** A rising ratio curve would be consistent with the survey's relative advantage over the AR(2) fading. It would not by itself show that the survey's information decays: the ratios also carry estimation cost, and the AR(2)'s own accuracy and the difficulty of the target change with h. Nor does it show why persistence dominates at long horizons. The two claims are kept apart.
- **That surveys sit causally upstream of growth.** The headline survey index measures current activity; its advantage is release timing. Only its New Orders component is treated as carrying a short genuine lead.
- **That the survey's content beats credit's.** The survey is fresher than credit at every origin, and the two comparisons use different training windows (Section 3). The credit and survey ratio curves are therefore not directly comparable. Each shows whether that indicator's own information helps at each target horizon, and any head-to-head result is framed as "the survey indicator tested here against credit, each as available at the origin, on the common sample". No search over indicators is made.

**Figure 1. Framing hypothesis, not tested in this plan.** Its arrows encode assumed causal structure; they are assumptions behind the design, not findings, and no result in this plan is read as confirming or refuting one. The authoritative graph is the dagitty block below; the sketch shows its shape. Times are counted from the origin o.

```
  Crisis (latent) ──► lending standards, balance sheets, rates ──► Credit (o−2) ┄┄► GDP (o+h)
        │
        ▼
  Activity (o) ──────► Activity (o+1) ──► … ──► Activity (o+h) ──► GDP (o+h)
     │      │                ▲
     │      └─► New Orders (o)
     ├─► Survey, General Activity (o)      published before the origin
     └─► GDP (o)                           published after the origin
```

```
dag {
  C [latent] ; Act0 [latent] ; Act1 [latent] ; ActH [latent]
  C -> LS ; C -> HBS ; C -> R ; C -> Act0
  LS -> K ; HBS -> K ; R -> K
  Act0 -> S ; Act0 -> NO ; Act0 -> Y0 ; Act0 -> Act1
  NO -> Act1 ; Act1 -> ActH ; ActH -> YH
  K -> YH
}
```

The block is drawn for one intermediate quarter; in the analysis an activity node stands for every quarter from o to o + h.

The figure records three assumptions behind the design:

1. **The survey is a timely measure, not a cause.** General Activity is a child of current activity, alongside GDP for the same quarter. Its advantage is that it is published before the origin and GDP is not. Any gain at short horizons is therefore read as release timing first; Q4 and Q5 (Section 5) bound how much of any gain could be attributable to freshness.
2. **New Orders carries a short lead.** Orders become output in later months, so New Orders is the one component with a forward arrow. Separate activity nodes for each quarter are needed to draw that lead. Q6 tests it.
3. **Credit sits on the crisis path.** As in the post-hoc DAG for the locked study, the crisis lowers credit through lending standards, household balance sheets and interest rates, and lowers activity directly. That graph was drawn after the 2010–11 errors were seen; it is a hypothesis, used here only to interpret the credit cells (Q3). The dashed arrow from credit to GDP is a candidate effect; the locked study found no reliable predictive content.

Activity at every date and the crisis are latent. The graph's only testable implications link credit to the activity measures through the mediators: credit should be independent of the survey, New Orders and current GDP once lending standards, household balance sheets and interest rates are held fixed. Testing those needs real-time mediators, which is Plan 3's data problem; this plan does not test them.

## 2. Data

All GDP and credit data are the frozen files of the locked release (`v1.0-lock`, `v2.0-results`), identified by the hashes in their manifests.

| Input | Source | Real-time route | Licence handling |
| --- | --- | --- | --- |
| Real GDP growth | Philadelphia Fed RTDSM, the origin's vintage (locked files) | As in the locked study | Public; locked hashes |
| Credit impulse | Fed Z.1, latest release before the origin (locked files) | As in the locked study; ends at q\* = o − 2 | Public; locked hashes |
| Survey: Current General Activity, not seasonally adjusted (`GACDFNA066MNFRBPHI`) | Philadelphia Fed Manufacturing Business Outlook Survey, via FRED | Unadjusted values are unrevised (below) | Research use permitted; redistribution not granted. A fetch script and SHA-256 hashes are published; the data are not. Conclusions are the author's, not the Bank's. |
| Survey: Current New Orders, not seasonally adjusted (`NOCDFNA066MNFRBPHI`) | As above | As above | As above |

**Why the unadjusted series.** The Philadelphia Fed re-estimates seasonal factors each January, which revises the adjusted series. The feasibility check compared the earliest ALFRED vintage (16 April 2015) with the latest (15 October 2026), for May 1968 to March 2015. The unadjusted General Activity and New Orders indexes did not change in any of 564 months; the adjusted control changed in 404. (A first run from 18 June 2015 gave the same result over 565 months.) Stability before 2015 is inferred, not observed, because ALFRED's archive starts in 2015. The series' own vintage list confirms 16 April 2015 as the earliest of 138 vintages (Section 13).

**Methodology breaks.** A revision check cannot detect a break: a sample redesign or a change in how the index is calculated would leave old values unchanged but not comparable. Such a break does not affect the real-time claim, because a forecaster at each origin used the same history with the same breaks. It does affect estimation over 1968–2019. The Philadelphia Fed's documentation was checked for changes in the sample, the questions behind the two indexes and the diffusion-index formula; the findings, including a candidate break in January 1985, are in Section 13. **Default if a break is found:** keep the full sample in every preregistered comparison, report the break in this section, and, as an exploratory check, rerun the comparisons with the same 78 origins and training rows starting at the break (1985Q1 for the candidate break in Section 13). Excluding the pre-break years from the primary is not the default, because a break in 1990 or 2000 could change the primary result and that choice must not depend on it.

**Not used.** The ISM PMI and the Conference Board's indexes fail the reproducibility standard (proprietary, not redistributable). The Chicago Fed National Activity Index has no real-time archive before 23 May 2011, the first ALFRED release date. Initial jobless claims are out of Plan 2 for scope, not data: one indicator keeps the plan to one table and one primary. ALFRED's archive of claims vintages starts on 28 May 2009, for both the adjusted (ICSA) and unadjusted (ICNSA) series, but the unadjusted series may be essentially unrevised, which would let claims use the survey's method. That needs its own design (weekly-to-quarterly aggregation, weather and holiday seasonality, its own drift check) and belongs to a later plan.

## 3. Sample and timing

**Origins.** The locked study's 78 origins, 1999Q3–2018Q4. The origin is **00:00 ET on the 15th of the quarter's middle month**; a release dated the 15th is not used. The same origins are used at every horizon, so every target satisfies the locked COVID exclusion (o + h ≤ 2019Q4).

**Horizons.** h = 0, 1, 2 and 4, counted from the origin: the target is quarter o + h. At h = 0 the target is the origin quarter itself, unpublished at the origin. h = 4 is the locked study's horizon.

**Fixed information set.** The information set is fixed at the origin; only the target changes with h.

| Input | Latest value available at origin o |
| --- | --- |
| GDP | Quarter o − 1, origin's vintage |
| Credit impulse | Quarter o − 2 (q\*), latest Z.1 before the origin |
| Survey | The latest release dated strictly before the origin |

**Survey release rule.** The survey is published on the third Thursday of the month it covers: at 10:00 ET until November 2015, at 8:30 ET since. A third Thursday falls between the 15th and the 21st. Applied to all 78 origins, the rule gives the **first month of quarter o** at every origin; the second month is never out before the origin. A per-origin table of release dates is generated by rule and checked against the survey's published release history before freezing.

**Effective information horizon.** The target horizon h is counted from the origin, but each indicator's own latest data are older or newer:

| Target horizon h | 0 | 1 | 2 | 4 |
| --- | --- | --- | --- | --- |
| Quarters from GDP's latest quarter (o − 1) | 1 | 2 | 3 | 5 |
| Quarters from credit's latest quarter (o − 2) | 2 | 3 | 4 | 6 |
| Quarters from the survey's latest quarter (o) | 0 | 1 | 2 | 4 |

At h = 0 the credit model is not a nowcast: it forecasts the current quarter from credit data two quarters old. In quarter labels the survey is two quarters fresher than credit; measured from the middle of credit's last quarter to the survey's first-month reading, the gap is about five months.

**Training windows.** Training rows run from the first quarter at which every regressor is available to the last row whose target was published by the origin. The AR(2) and credit comparisons start in 1965Q1, as in the locked study. The survey comparisons start in 1968Q3, the first quarter with a first-month reading (July 1968). Q7 uses the common sample of both. The AR(2) in each comparison is estimated on that comparison's rows, so the denominators of the survey, credit and head-to-head ratios differ. This does not affect any within-pair comparison; it is a second reason the curves are not directly comparable.

**Outcome.** Quarterly real GDP growth, annualised, from the 2026Q3 vintage, as in the locked study.

## 4. Models

Every forecast is a direct regression built from the locked functions in `phase2.py` (SHA-256 da697030…), with the horizon set to h.

- **Benchmark:** the direct AR(2): Y_{j+h} on 1, Y_{j−1}, Y_{j−2}.
- **AR(2) + credit:** the locked specification: four lags of the impulse at release lag k = 2.
- **AR(2) + survey:** one regressor, S_j, the survey's first-month reading in quarter j, adjusted for seasonality as below. In the locked function's terms this is one lag at release lag 0, because S_j is published before origin j.
- **AR(2) + survey, staleness-matched (Q4):** one regressor, S_{j−2}, the first-month reading of quarter j − 2, adjusted by method A at the origin: release lag 2 in the locked function's terms. Training rows start in 1969Q1, the first quarter with S_{j−2}.
- **AR(2) + survey, third month (Q5):** one regressor, S³_{j−1}, the third-month reading (March, June, September or December) of quarter j − 1: release lag 1. The data available are cut at the start of quarter o, so the latest reading used at origin o is the third month of quarter o − 1. It is published on that month's third Thursday (Section 3), more than six weeks before the origin, and so always strictly before 00:00 ET on the origin date. Method A is applied with that cut: each third month's mean comes from readings of that calendar month published before the cut. Training rows start in 1968Q3, the first quarter with S³_{j−1} (June 1968).
- **AR(2) + credit + survey (exploratory, Section 5):** both.

Every model is fitted with the AR(2) it is compared with on one row mask: the rows where the target and every regressor are present, from the comparison's start (Section 3) to the last row whose target was published by the origin.

Nested comparisons (AR(2) against AR(2) + indicator) use `direct_forecast`, which estimates both models on the rows where every regressor is present. The non-nested head-to-head (Q7) needs a common row mask: it is built from `direct_rows` with both indicators, and each single-indicator model is fitted on exactly those rows with the locked `ols`.

**Why General Activity is primary.** New Orders is the theoretically motivated component, given the forward arrow in Figure 1. General Activity is primary because it is the default series: the headline index, the one used in practice. The primary test therefore does not depend on choosing the component the theory favours. If New Orders does better, Q6 reports it as a secondary result, which is the honest place for it.

**Seasonality in real time.** The covariate is always a first month of a quarter (January, April, July or October), so the seasonal pattern is quarterly. The plan uses one of two methods; the choice is the author's (Section 12):

- **A. Real-time demeaning (recommended).** At each origin, compute one mean per calendar month from every reading of that month published before the origin, and subtract it from every reading of that month, in training rows and at the origin alike. The mean includes the reading being adjusted, so it is defined from the first reading onward (July 1968 for July): the survey sample starts in 1968Q3 as stated, with no rows lost. Nothing from after the origin is used. At the first origin (1999Q3), the July mean rests on 32 readings (July 1968 to July 1999). This is what `plan2_data.survey_quarterly` computes and what gate 3 recomputes independently.
- **B. Quarter dummies.** Add three quarter dummies to the survey regression. These also act on the seasonally adjusted GDP, adding three noise parameters.

Both methods assume a stable seasonal pattern. If it has drifted over 1968–2019, the covariate is mismeasured by an amount that varies with the origin. **Drift rule, fixed now.** Before freezing, each first-month calendar month's mean (January, April, July, October) is compared between July 1968–December 1983 and January 1984–December 1998. The check uses survey data only, with no GDP outcome and nothing after 1998, so it uses no data from the forecast sample. The standard error is Welch's, built from each period's own standard deviation and count, sqrt(s₁²/n₁ + s₂²/n₂), not a pooled one, so a rise in variance in the later period does not hide drift. If any of the four differences exceeds twice its standard error, method A uses a rolling window of the last 15 years; otherwise it uses the full pre-origin history. With four months tested, the chance that at least one triggers when there is no drift is about 17%. The rule errs toward triggering deliberately, because a false trigger only switches to the rolling window, the more adaptive estimate; a trigger is therefore not read as evidence of drift. The four differences, their standard errors and the resulting choice are recorded here before freezing.

## 5. Comparisons

All comparisons are RMSE ratios, model ÷ comparator, over the 78 origins, reported as estimates with intervals in the locked study's "estimate only" style. Below 1 means the model forecast better. Every reported cell shows its effective information horizon (Section 3).

**Primary (one comparison).**

| Label | Comparison | Horizon |
| --- | --- | --- |
| **Q1** | AR(2) + survey (General Activity) vs AR(2) | **h = 1** |

h = 1 is chosen because h = 0 is a nowcast with partial same-quarter data and h = 4 is already settled for credit. h = 2 is also short and is reported in Q2; h = 1 is preferred as the shortest genuine forecast, closest to the survey's release, and so the cell most likely to show a content effect if one exists. If the survey helps at h = 2 but not at h = 1, the primary fails and the result is reported in Q2; that risk is accepted in advance.

**Secondary, preregistered.**

| Label | Comparison | Purpose |
| --- | --- | --- |
| Q2 | Survey ratios at h = 0, 1, 2, 4 | **Directional prediction**: the ratio rises toward 1 as h lengthens, read as a fading relative advantage (Section 6) |
| Q3 | Credit ratios at h = 0, 1, 2 (h = 4 reproduces the locked result) | Does the credit null hold at shorter horizons? These three cells are new tests, not replications |
| Q4 | Staleness-matched survey: the first-month reading of quarter o − 2, at h = 1 | Does the survey help when cut to credit's quarter? Matched in quarter, not in month: a first-month reading against a quarterly flow. A null means the content does not survive two quarters *or* the survey is too stale; it is not read as evidence about content. |
| Q5 | One-month freshness: the survey cut at the end of quarter o − 1, at h = 1. The covariate is the latest release before that date: the third-month reading of quarter o − 1 (December for a Q1 origin), demeaned with that calendar month's mean | A comparison with a reading one month staler than Q1's. It is not a pure freshness contrast: the vintage, the calendar month (December rather than January, for example) and that month's seasonal mean all change with it |
| Q6 | Q1–Q2 with New Orders in place of General Activity | Does the forward-looking component behave differently? |
| Q7 | AR(2) + survey vs AR(2) + credit, h = 1, common sample | The survey indicator tested here against credit, each as available at the origin: a comparison of two prespecified indicators, not a search over a wider set. Not a content comparison (Section 3) |
| Q8 | Q1 dropping 2008–09 targets; Q1 dropping 2001 targets | Is a short-horizon gain a recession artefact? |

**Exploratory.** AR(2) + credit + survey vs AR(2) + credit, h = 1, common sample (does the survey add beyond credit?); Q1 and Q2 with the same 78 origins and training rows starting in 1985Q1 (the candidate break in Section 13); and anything not listed.

**Figures.** (1) The ratio curve: RMSE ratio against h for the survey and for credit, with 90% intervals, each point labelled with its effective information horizon. (2) The coefficient curve: the survey coefficient against h, estimated at the last origin (2018Q4) on its training rows, with a moving-block bootstrap interval over those rows (block 4, 2,000 draws, seed 20261019). Intervals widen with h partly because multi-step errors are serially correlated; a widening fan reflects a changing coefficient plus noise, not noise alone.

## 6. Statistics and decision rules

**Intervals.** The locked moving-block bootstrap: block length 4, 2,000 draws, seed 20261019, percentile 90% intervals. Each comparison is paired: the same resampled origins for both forecasts.

**Credible improvement.** Claimed only if the whole 90% interval lies below 1. In testing terms this corresponds approximately to a one-sided test at the 5% level; the results section does not use significance language.

**Credible loss.** Reported if the whole 90% interval lies above 1. With no effect, the augmented model's expected ratio is slightly above 1, because it estimates extra coefficients and adds no information (Section 13), so a credible loss is a likely outcome, not an edge case. It is worded as possible estimation cost, not as harm.

**Q7 wording rule.** "Better" if the whole interval lies below 1; "worse" if it lies wholly above 1; "about as well as" if it contains 1.

**Directional prediction (Q2).** Supported only if (a) the point ratios do not fall as h lengthens (R₀ ≤ R₁ ≤ R₂ ≤ R₄), and (b) the 90% interval for R₄ − R₁ lies wholly above zero. If (a) holds and (b) does not, the result is "consistent with a fading relative advantage, not established". If (a) fails, a fading advantage is not established, whatever (b) shows. The requirement is conservative: a fading advantage that is not monotone, such as gains at h = 0 and h = 1 that vanish at h = 2, with a small gain returning at h = 4, would not satisfy it.

**Secondary comparisons are descriptive.** Q2–Q8 contain many cells and contrasts, with no adjustment for multiple comparisons. Only Q1 is confirmatory. An isolated secondary interval below or above 1 is reported as a description of that cell, not read as one of a family of confirmatory findings.

**Test statistic, for completeness.** The Diebold–Mariano statistic with the Harvey–Leybourne–Newbold correction, with its one-sided block-bootstrap p-value for an improvement, using h − 1 lags (at least 0) as the locked code does at h = 4. Reported, not interpreted.

**Effective sample.** 78 origins give 78 distinct target quarters at every h; targets do not overlap. Multi-step errors are serially correlated, so longer horizons carry less effective information. Differences in which cells clear their intervals are partly differences in power and are reported as such; the ratio curve is the result.

**Power and coverage, checked before freezing.** Gaussian simulations overstated power in the locked study, so the realised-path method is used: the real indicator path, synthetic GDP outcomes, no real outcome. Effect sizes are defined by the **true RMSE ratio they imply**, so that they are comparable across indicators: 1.00 (no effect), 0.95, 0.90 and 0.80. For each, synthetic GDP follows the locked simulation's AR(2) process (1.84 + 0.264 g₋₁ + 0.137 g₋₂, shock variance 10.8) plus a coefficient times the real indicator, timed so the direct regression is correctly specified: the survey's first-month reading h quarters back, or the credit impulse h + 2 quarters back. The coefficient is found by bisection (seed 20261202) as the value at which the mean simulated RMSE ratio at the 78 origins equals the target. Synthetic GDP has a single vintage, so contexts and outcomes coincide; each replication's interval uses 500 bootstrap draws (the real run uses 2,000). Script: `plan2_power.py`, 300 replications per cell (seed 20261203). The check reports power and the coverage of the 90% intervals for:

- the survey at h = 0, 1, 2 and 4;
- credit at h = 0, 1 and 2, each run separately, not extrapolated from the locked h = 4 result.

The check also reports, for each cell, the correlation between the two forecasts' errors: it explains why two cells with the same ratio can have very different interval widths. The results are written into this plan before it is frozen. **Underpowered cells, fixed now:** if a cell's power is below 0.80 at a true ratio of 0.90, the plan is amended before freezing to state that cell's minimum detectable ratio (the true ratio at which power reaches 0.80), and its null is reported with that caveat. If power is below 0.80 at every simulated ratio, down to 0.80, no minimum detectable ratio is extrapolated: the cell is reported as unable to detect reliably even a 20% gain, and its null carries that caveat. Power for Q4, Q5 and Q7 is not simulated; their intervals are reported as estimates only, and their nulls are not over-read.

## 7. How results will be worded

Every single-cell sentence names the horizon, the effective information horizon, the ratio and the interval. The Q2 sentences summarise the curve across cells that have each already been reported in a single-cell sentence; they name the horizons and effective horizons they compare, and the interval of the difference. The pre-written sentences:

| Result | Sentence |
| --- | --- |
| No credible improvement | "At h = [h] ([e] quarters from the indicator's latest data), the [survey / credit impulse] did not improve the AR(2) credibly (ratio r; 90% interval a–b)." |
| Credible improvement | "At h = [h] ([e] quarters from the indicator's latest data), the [survey / credit impulse] improved the AR(2) credibly (ratio r; 90% interval a–b)." For the survey only, add: "Its value at the origin may reflect freshness as well as content (Section 3)." |
| Credible loss | "At h = [h] ([e] quarters from the indicator's latest data), the [survey / credit impulse] forecast credibly worse than the AR(2) (ratio r; 90% interval a–b)." The coverage caveat that follows gives the estimation-cost reading. |
| Q2 supported | "The survey's ratio rose monotonically with the horizon, from r₁ at h = 1 (1 quarter from its latest data) to r₄ at h = 4 (4 quarters) (difference d; 90% interval a–b). This is consistent with its relative advantage over the AR(2) fading with the horizon; it does not by itself show that the survey's information decays, and it does not explain why the AR(2) is hard to beat a year ahead." |
| Q2 consistent with a fading advantage, not established | "The survey's ratios rose monotonically with the horizon, consistent with a fading relative advantage, but the rise from h = 1 (1 quarter from its latest data) to h = 4 (4 quarters) was not established (difference d; 90% interval a–b)." |
| Q2 not established, not monotone | "The survey's ratios did not rise monotonically with the horizon (r₀, r₁, r₂ and r₄ at h = 0, 1, 2 and 4, which are 0, 1, 2 and 4 quarters from its latest data), so a fading relative advantage was not established (difference from h = 1 to h = 4: d; 90% interval a–b)." |
| Q7 | "On the common sample, at h = 1 (1 quarter from the survey's latest data and 3 from credit's), the survey forecast [better / worse / about as well as] the credit model (wording by the Q7 rule, Section 6) (ratio r; 90% interval a–b). The survey's data were about five months fresher; this compares the survey indicator tested here with credit, each as available at the origin, not the two indicators' content." |

**Coverage caveat.** Every result sentence is followed by one caveat, chosen by the cell:

- **Simulated cells** (the survey at h = 0, 1, 2, 4, including Q1; credit at h = 0, 1, 2): "Coverage caveat (Section 13): with no effect, the 90% interval contains 1 in [79–83 / 67–73]% of replications; the median no-effect ratio is [1.003 / 1.018–1.024], so a credible loss can reflect estimation cost, not harm. Reliable detection needs a true ratio of about [m]." In the first two brackets the first figure is the survey's and the second credit's. [m] is the cell's own minimum detectable ratio from Section 13; for credit at h = 1 and h = 2 the sentence ends instead "This cell cannot reliably detect even a 20% gain."
- **Cells not simulated** (Q2's difference, Q4–Q8, the exploratory comparisons): "Power and coverage were not simulated for this comparison (Section 6); the interval is an estimate only."

The ratio-curve figure carries the full note as a footnote: "In simulations using the real indicator paths, these 90% intervals contained the true ratio in 83–100% of replications when the indicator had an effect. With no effect, they contained 1 in only 79–83% of replications for the survey and 67–73% for credit; almost all the misses lay wholly above 1, reflecting estimation cost. A credible improvement with no effect occurred in at most 3% of replications."

No sentence assumes the direction of an unmeasured bias. The placebo (gate 5) is a pipeline check, not a result: its ratio and interval are reported in the gate record only, and a placebo interval wholly above 1 is never described as a finding.

**Headline framing.** The result is reported as a test of whether these particular real-time survey measures, and the credit impulse, improve a direct AR(2) at the chosen horizons, with the stated power limits. It is not a general verdict on survey forecasting, nor an account of why simple models forecast well.

## 8. Validity gate

The official run is the **first run whose outputs pass every gate check**. A run that fails a gate is a failed attempt, logged as a deviation with its outputs kept, and fixed before a rerun. Results from a failed attempt are not reported as results.

1. The AR(2) and credit forecasts at h = 4 reproduce the locked study's forecasts exactly at all 78 origins.
2. At every origin, the survey value used matches the release-rule table: first month of quarter o, never later; and for Q4 and Q5, the readings their rules specify.
3. The seasonal adjustment is recomputed independently and matches (method A), or the quarter dummies are present (method B).
4. Every forecast is finite and moves when the last observations move (a synthetic shift test).
5. **Placebo pipeline check.** A synthetic series with the survey's release timing and its calendar-month means and standard deviations, drawn as independent normal values with no link to GDP (seed 20261201), is run through the Q1 pipeline. Its expected ratio is slightly above 1, about 1.00–1.05, because it adds a parameter and no information. The gate requires that its ratio is **not credibly below 1**. A credible "gain" from a series with no information means the pipeline is leaking. A placebo interval wholly above 1 is reported but does not fail the gate: with no effect this happens in about one survey run in six (Section 13), and because the placebo seed is fixed, a rerun would repeat it, so a two-sided gate could block a sound run indefinitely. A systematic penalty in the pipeline is caught by gate 1 instead, which requires exact reproduction of the locked forecasts.
6. The fetched survey files match the hashes recorded at freezing.

## 9. Procedure

1. **Agree this plan.** Settle the decisions in Section 12.
2. **Run the pre-freeze data checks:** the survey's vintage list and earliest vintage (Section 2); the methodology review (Section 2); the seasonal-drift comparison (Section 4); the claims archive date (Section 2); the release-date table against the published history (Section 3). Record each result here.
3. **Write and test the scripts** on synthetic outcomes only: the release-date table, the survey fetch, the covariate builder, the common-row mask, the horizon loop and the gate checks. No real GDP outcome is used with the survey, or with credit at h ≠ 4.
4. **Run the power and coverage check** (Section 6) and record its results here.
5. **Freeze.** Commit the plan, scripts, release-date table and file hashes; tag `plan2`; write `PLAN2_LOCK.json`.
6. **Run until one run passes the gate.** Save every attempt.
7. **Report** using only the Section 7 sentences, with a declared-deviation section.

## 10. What counts as a deviation

After the tag, any of these is a deviation, logged with its date and whether results had been seen: a change to origins, horizons, the origin time, inputs, the release rule, the seasonal method or window, the primary comparison or the gate; a second passing run; a comparison not listed in Section 5 reported as anything but exploratory; wording other than Section 7's; an unreported listed output.

**What the tag does and does not lock.** The tag fixes the plan, the model specifications and the code. It does not lock every later analysis choice: the plan declares exploratory analyses and permits reruns after a failed gate. The report states this plainly and reports both exactly as specified here.

## 11. Out of scope

TimesFM (its leakage questions would confound the horizon question); the ISM PMI and other proprietary indicators; initial jobless claims; the mediator test (Plan 3); any causal claim about credit or the survey.

## 12. Decisions for the author before freezing

| # | Decision | Recommendation |
| --- | --- | --- |
| 1 | Seasonal method: A (real-time demeaning) or B (quarter dummies) | **A**: the GDP regression keeps three parameters, only pre-origin data are used, and the covariate reads as a deviation from its calendar-month norm. The window (full history or last 15 years) is set by the drift rule in Section 4 |
| 2 | Primary series: General Activity or New Orders | **General Activity**, as the default series (Section 4); New Orders as Q6 |
| 3 | Primary horizon | **h = 1**, the shortest genuine forecast (Section 5) |
| 4 | Initial jobless claims | **Not in Plan 2**, for scope: one indicator, one table, one primary (Section 2) |
| 5 | TimesFM arms | **Out**: keeps the horizon question separate from leakage |
| 6 | Power and coverage check before freezing, for the survey and for credit at h = 0, 1, 2 | **Yes**, with error correlations reported and the underpowered-cell rule in Section 6 |
| 7 | "Does the survey add beyond credit?" as exploratory, or as a secondary | **Exploratory**: it matters only if Q7 shows the survey beating credit, so promoting it would add a test without a hypothesis. The plan has one primary and seven secondary labels (Q2–Q8), eight tests in all because Q8 has two parts |
| 8 | Seasonal drift threshold | **Fixed in Section 4**: twice the Welch standard error (each period's own SD) of the difference in calendar-month means, 1968–1983 against 1984–1998; errs toward the rolling window |
| 9 | What happens if the methodology review finds a break | **Fixed in Section 2**: keep the full sample; report the break; post-break comparisons are exploratory |
| 10 | Seeds | Bootstrap 20261019 (locked); placebo 20261201; effect-size search 20261202 |

## 13. Pre-freeze check results

Recorded as each check is run. Survey data were used only for the vintage and drift checks; no GDP outcome was used.

| Check | Date | Result |
| --- | --- | --- |
| Survey vintage list | 28 Oct 2026 | Earliest ALFRED vintage for both survey series: **16 April 2015**; 138 vintages to 15 October 2026. The unrevised check is to be rerun from 16 April 2015. |
| Unrevised check, rerun from earliest vintage | 28 Oct 2026 | 16 April 2015 against 15 October 2026, May 1968 to March 2015: General Activity and New Orders, unadjusted, **0 of 564 months differ**; the adjusted control differs in 404 (largest 7.1). |
| Claims archive | 28 Oct 2026 | ICSA: 903 vintages from **28 May 2009**; ICNSA: 902 vintages from 28 May 2009. |
| Seasonal drift (Section 4) | 28 Oct 2026 | No month triggers; **method A uses the full pre-origin history**. See the table below. |
| Release-date table (Section 3) | 28 Oct 2026 | Built by rule for all 78 origins (`release_dates.csv`). The month used is the first month of quarter o at every origin. At 12 origins the second month's survey was released on the origin date itself, after 00:00 ET, so it is excluded: 2001Q1, 2001Q4, 2002Q3, 2003Q2, 2007Q1, 2007Q4, 2008Q2, 2012Q4, 2013Q3, 2014Q2, 2018Q1, 2018Q4. Checked against ALFRED's release dates for this survey (available from 2015): at all 14 origins from 2015Q3 to 2018Q4, the rule's release date is in ALFRED's list and is the latest release before the origin; every monthly third Thursday from June 2015 to December 2018 is listed. ALFRED also lists four dates off the rule: 15 June 2015 and the second Thursday of each January 2016–2018, when the annual seasonal revisions are published; they change only the adjusted series and never alter which month is available at an origin. Before 2015 the table rests on the rule, which the Philadelphia Fed's 2015 notice says had not changed (third Thursday; 10:00 ET until November 2015). |
| Survey fetch (`plan2_fetch.py`) | 29 Oct 2026 | ALFRED vintage 15 October 2026, May 1968–December 2019, 620 months each. SHA-256: General Activity (`GACDFNA066MNFRBPHI.csv`) `ff6a27903bfbf08d53bc80c3834c272a229568db83a98f17e8f26930e7b9fdf4`; New Orders (`NOCDFNA066MNFRBPHI.csv`) `01e2835e0bb763c591b39e3bd567d78fc1182a0712797219abe1b74894bc7e45`. These are the hashes gate 6 checks. |
| Self-test and pipeline test | 29 Oct 2026 | On the author's machine with the real survey and synthetic GDP: self-test six of six PASS (planted effect: mean ratio 0.785; no effect: 1.003); pipeline test gates 1–5 all pass, with gate 1 in its synthetic form only. Gate 1 has two parts: that `fit()` reproduces the locked `direct_forecast` exactly (checked here, on synthetic GDP), and that the h = 4 forecasts reproduce the locked study's published forecasts exactly. The second part needs real GDP and credit, so it runs only in the real run. Gate 6 also runs only in the real run. |
| Environment additions | 29 Oct 2026 | Plan 2 uses the locked study's pinned environment plus `requests` 2.34.2 (fetch only). The locked `test_phase2.py` on the author's machine matches the repository: SHA-256 `f7d71fbfba753c36857fa52c6b06053fc007184c93e18773a254217b4dfc0036`. |
| Methodology review | 28 Oct 2026 | No documented break in the core questions or the index formula (percentage reporting increases minus percentage reporting decreases, unweighted) since May 1968. The panel is not a probability sample and is replenished continuously (about 120 firms now), so composition drifts gradually; collection moved from mail to the web on undated steps; supplementary questions were added in 2001 and 2015, outside the core. **One candidate break is visible in the data:** from January 1985 the index is reported to one decimal (86% of months, against 1 month before 1985), and its standard deviation falls from 26.8 (1968–84) to 18.9 (1985–98) and stays there (19.4, 1999–2015). This fits a change in the number of respondents or in tabulation, but it coincides with the start of the Great Moderation, so the cause cannot be separated. **Applying the Section 2 default:** the full sample is kept in every preregistered comparison; January 1985 is reported as a candidate break; Q1 and Q2 are rerun from 1985Q1 as an exploratory check. |
| Power and coverage | 29 Oct 2026 | `plan2_power.py`, 300 replications per cell, on the author's machine; results below. **Every cell is underpowered at a true ratio of 0.90** (power 0.38–0.72), so under Section 6's rule each cell's minimum detectable ratio is stated below, and its null is reported with that caveat. False "credible improvements" with no effect: 0–3% of replications. |
| Review amendments | 29 Oct 2026 | After the power check and before freezing: title names the survey; Section 6 adds the credible-loss rule, the Q7 wording rule, the not-monotone case for Q2 and the not-reached case for minimum detectable ratios; Section 7 adds the credible-loss and not-monotone sentences and limits the freshness clause to the survey; Section 8 explains why the placebo gate stays one-sided; Section 13 adds Monte Carlo precision. No real GDP outcome had been read. |
| Second review amendments | 29 Oct 2026 | Q7's survey horizon corrected to 1 quarter; coverage note text and placement fixed in Section 7; "information decays" replaced by "relative advantage fading"; "best indicator" replaced by the prespecified indicators; secondary comparisons declared descriptive; Q5 described as a one-month staleness contrast that also changes month and seasonal mean; Figure 1's arrows labelled as assumptions; headline framing and what the tag locks stated. No real GDP outcome had been read. |
| Third review amendments | 29 Oct 2026 | The single coverage note replaced by a per-sentence caveat (bracketed survey or credit figures, and the cell's minimum detectable ratio) for simulated cells, and an "estimate only" caveat for cells not simulated; the full note kept as the ratio-curve footnote; the credible-loss sentence no longer repeats the caveat; the Q2-supported sentence no longer repeats itself; Q7 stated in Section 5 to compare two prespecified indicators. No real GDP outcome had been read. |
| Fourth review amendments | 29 Oct 2026 | Method A's wording corrected to match the code (one mean per calendar month from all readings published before the origin, including the reading adjusted; no rows lost); Q4 and Q5 regressors, release lags, cuts and training starts defined in Section 4, with the common row mask; the pipeline-test record now separates gate 1's synthetic and real parts; Q2 sentences name effective horizons, and the sentence rule distinguishes single-cell from summary sentences; the not-reached caveat no longer implies a detection ratio; the break check keeps the 78 origins and moves only the training start; the placebo is never reported as a finding. Text only: no script changed. No real GDP outcome had been read. |

**Seasonal drift: first-month readings, General Activity, not seasonally adjusted.**

| Month | Mean, Jul 1968–1983 (n) | Mean, 1984–1998 (n) | Difference | Welch SE | Difference ÷ SE | Triggers? |
| --- | --- | --- | --- | --- | --- | --- |
| January | 1.5 (15) | 7.4 (15) | +6.0 | 8.6 | 0.69 | No |
| April | 20.7 (15) | 19.6 (15) | −1.1 | 8.3 | −0.13 | No |
| July | −4.8 (16) | −6.1 (15) | −1.4 | 7.8 | −0.17 | No |
| October | 18.5 (16) | 13.6 (15) | −4.9 | 7.4 | −0.66 | No |

The calendar-month means differ widely from one another (from about −5 in July to about 20 in April), so seasonal adjustment matters; but each month's mean is stable between the two periods.

**Power and coverage: realised indicator paths, synthetic GDP, 300 replications per cell.** Power is the share of replications whose 90% interval lies wholly below 1. Coverage is the share whose interval contains the target ratio.

| Cell | Power at 0.95 | Power at 0.90 | Power at 0.80 | Minimum detectable ratio (power 0.80) | Coverage at 0.95 / 0.90 / 0.80 | Coverage with no effect |
| --- | --- | --- | --- | --- | --- | --- |
| Survey, h = 0 | 0.43 | 0.72 | 0.94 | about 0.86 | 0.88 / 0.89 / 0.91 | 0.79 |
| **Survey, h = 1 (Q1)** | 0.42 | 0.66 | 0.95 | **about 0.85** | 0.88 / 0.92 / 0.94 | 0.82 |
| Survey, h = 2 | 0.45 | 0.63 | 0.91 | about 0.84 | 0.89 / 0.91 / 0.94 | 0.80 |
| Survey, h = 4 | 0.42 | 0.61 | 0.89 | about 0.83 | 0.88 / 0.91 / 0.93 | 0.83 |
| Credit, h = 0 | 0.21 | 0.43 | 0.86 | about 0.81 | 0.93 / 0.97 / 1.00 | 0.73 |
| Credit, h = 1 | 0.20 | 0.39 | 0.65 | not reached; cannot reliably detect a 20% gain | 0.88 / 0.92 / 0.97 | 0.68 |
| Credit, h = 2 | 0.20 | 0.38 | 0.61 | not reached; cannot reliably detect a 20% gain | 0.83 / 0.89 / 0.94 | 0.67 |

Minimum detectable ratios are interpolated linearly between the grid points 0.90 and 0.80, so they are approximate. With 300 replications, each power figure has a Monte Carlo standard error of up to about 0.03, so a reported 0.66 is consistent with roughly 0.60–0.72; the 500 bootstrap draws per replication and single-vintage GDP add some further imprecision. The figures guide reading; they are not exact.

**What this means for the reading of results.**

- **The primary comparison (Q1) can reliably detect only a gain of about 15% or more.** A null at h = 1 rules out large gains, not modest ones. The survey cells are alike at every horizon, so differences between horizons in the ratio curve are not differences in power.
- **The credit cells at h = 1 and h = 2 cannot reliably detect even a 20% gain.** Their nulls say little, and are reported as such. This is consistent with the locked study, where only gains of roughly 40% could be reliably detected at h = 4.
- **With an effect present, the survey intervals cover close to their nominal 90%.** With no effect, they include 1.00 only 79–83% of the time (credit 67–73%), because the extra estimated coefficient pushes the expected ratio slightly above 1: about one interval in six then lies wholly above 1 (survey 14–18%, credit 27–31%), reading as a loss. The median simulated ratio with no effect confirms the cost: 1.003 for the survey, 1.018–1.024 for credit, which has more lags to estimate. So a credible *loss* from adding an indicator can reflect estimation cost, not harm, and is reported that way. False credible *improvements* with no effect are rare (0–3%).
- **Simplifications.** Synthetic GDP has a single vintage, and each replication's interval uses 500 bootstrap draws, against 2,000 in the real run.

**Error correlations (Decision 6).** Mean correlation, across replications, between the AR(2)'s forecast errors and the augmented model's. A high correlation is why small RMSE differences can still be measured: the two models miss in the same quarters.

| Cell | No effect | 0.95 | 0.90 | 0.80 |
| --- | --- | --- | --- | --- |
| Survey, h = 0 | 1.00 | 0.94 | 0.89 | 0.79 |
| Survey, h = 1 (Q1) | 1.00 | 0.93 | 0.88 | 0.78 |
| Survey, h = 2 | 1.00 | 0.94 | 0.89 | 0.79 |
| Survey, h = 4 | 1.00 | 0.93 | 0.88 | 0.79 |
| Credit, h = 0 | 0.98 | 0.91 | 0.87 | 0.75 |
| Credit, h = 1 | 0.97 | 0.91 | 0.86 | 0.76 |
| Credit, h = 2 | 0.97 | 0.89 | 0.85 | 0.76 |
