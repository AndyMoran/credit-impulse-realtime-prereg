# Did the Credit Impulse Help Forecasters in Real Time? A Preregistered Test, 1999–2019

Working paper, version 2.2 · 22 October 2026 · Andy Moran, Heaviside Analytics (independent researcher). Locked protocol: DOI 10.5281/zenodo.23477871; results: DOI 10.5281/zenodo.23479717; replication package: DOI 10.5281/zenodo.23497087

## Abstract

Could a forecaster have used the credit data published at the time to improve on a simple autoregressive forecast of US output and unemployment? On the 1999–2019 evidence, no. The best estimate is that adding credit made four-quarter-ahead GDP forecasts 10.6% worse. With only one credit cycle in the sample, the uncertainty is wide: a post-lock sensitivity interval, calibrated by simulation, runs from about 6% better to 44% worse, so a small benefit cannot be ruled out. Credit also made unemployment forecasts 1.1% worse, and adding a credit correction to professional forecasters' median GDP forecast made it 2.5% worse. Revised credit data did no better. The credit model misread the 2009–10 contraction as the start of a sharp rebound that did not materialise.

Much of the evidence that credit matters for the business cycle comes from revised data, which no forecaster had at the time. I rebuilt 83 dated releases of the Federal Reserve's Financial Accounts (Z.1) into a real-time credit dataset, showing what a forecaster could have seen each quarter. With it I tested the credit impulse, the change in new borrowing as a share of GDP. I published the plan and code before scoring any forecast.

About three-quarters of the impulse's variation occurred in 2008–09. Simulations on that realised path show that, across repeated samples, the test would reliably detect a benefit from credit only if it shrank forecast errors by about 40%. Smaller benefits, such as the 6% the sensitivity interval still allows, could easily have gone undetected. In this case study, a standard Gaussian power simulation overstated the test's sensitivity, and the moving-block bootstrap intervals were too narrow; simulating on the actual credit path exposed both. The protocol, code and data are public (locked release: DOI [10.5281/zenodo.23477871](https://doi.org/10.5281/zenodo.23477871)).

**Keywords:** real-time data, credit impulse, forecast evaluation, preregistration, Financial Accounts of the United States. **JEL:** C53, E17, E44, E51.

## 1. Introduction

Could a forecaster have used the credit data published at the time to improve on a simple autoregressive forecast of US output and unemployment? On the 1999–2019 evidence, no. The best estimate is that adding the real-time credit impulse made four-quarter-ahead GDP forecasts 10.6% worse (the target is quarter o + 4, four quarters after the origin quarter o, the SPF's convention; see Box 1). Because the sample holds only one credit cycle, the range of plausible effects is wide:

| Effect of adding credit on GDP forecast errors |  |
| --- | --- |
| Best estimate | 10.6% worse |
| Locked 90% interval | From about 2% better to 36% worse |
| Interval widened to offset its undercoverage (Section 5.1) | From about 6% better to 44% worse |

So a small benefit cannot be ruled out, but most of the range lies on the side of worse forecasts. The impulse showed no credible gain for any target and no stable relationship a forecaster could have exploited, and revised credit data would have done no better.

The question matters because the post-2008 literature gives credit a central role in macroeconomic dynamics, and much of the forecasting evidence for that role uses revised data, which no one had at the time. Revisions, release timing and the choice of transformation can each make a predictor look better in hindsight than it was in use. Edge and Meisenzahl (2011) showed this for the credit-to-GDP gap. The gap measures how far credit, relative to GDP, has risen above its long-run trend, and it serves as a guide for setting countercyclical capital buffers, the extra capital banks are asked to build up in good times. They found that later revisions to the gap were often as large as the first reading itself, enough to turn "on trend" into "well above trend", or the reverse. I ask the companion question: would credit, as published, have improved forecasts of GDP growth and unemployment, improved the professional forecasters' GDP forecast, or predicted how GDP would be revised?

To answer it, I rebuilt household and nonfinancial business credit from 83 dated Z.1 releases (June 1999 to December 2019), so that each forecast origin sees only what had been published before it. I then locked the protocol, all analysis code, the power analysis and the wording of the headline conclusions in a public release before scoring any forecast (DOI [10.5281/zenodo.23477871](https://doi.org/10.5281/zenodo.23477871)). Four pre-specified tests decide the result, and a pre-committed map fixes the words I use to report it.

Three findings stand out.

1. **Worse forecasts on average.** Adding the real-time credit impulse to a direct AR(2) raised the RMSE of four-quarter-ahead forecasts by 1.1% for unemployment, 2.5% for the credit-corrected median SPF forecast and 10.6% for GDP. GDP revisions show no detectable response to the impulse. All four 90% intervals include no change, so none shows a credible improvement, though intervals widened to offset their undercoverage still allow an improvement of up to about 6% (Section 5.1). Revised credit data would have changed nothing: the credit-revision premium is close to zero.
2. **An unstable relationship.** From 2008Q4 onwards the credit model's RMSE was 52% higher than the benchmark's. Almost all of the loss came from one misreading: the model took the deep 2009–10 contraction as a signal of recovery and forecast a sharp rebound in 2011–12 that did not materialise. Growth resumed, but far more slowly than forecast. Origins 2007Q1–2010Q4 account for 68% of the full-sample loss. Before 2008Q4 the exploratory split S6 shows a gain of about 4%, but it is fragile: the pre-crisis credit path varied too little for the design to identify an effect either way, and intervals like this one appear in about 5% of simulations with no credit effect at all (Section 5.3).
3. **Hints for unemployment, not GDP.** Four exploratory specifications built on slower-moving credit measures improve unemployment forecasts by 2–8%: the credit-to-GDP gap, real credit growth, a real-credit contraction model and a Markov-switching model. A BVAR with the impulse gains 4.6%. Nothing comparable appears for GDP. These results are uncorrected across the 27 exploratory tests, so I treat them as leads, not findings.

The paper contributes three things. The first is a public real-time dataset of household and nonfinancial business credit, with every change of series code and units documented. The second is a preregistered evaluation with a null result, and with it a design lesson. For this predictor, whose variation is concentrated in one episode, the Gaussian-path power simulation overstated power, and in simulations on the realised predictor path the chosen moving-block bootstrap intervals covered less than they claimed; conditioning on that path revealed both. I have not tested other clustered paths or error processes. The third is a dated log of every deviation, including errors I caught in my own power analysis before the lock, which lets readers judge the evidence rather than trust it.

Section 2 places the paper in the literature, Section 3 describes the data, Section 4 the design, Section 5 the results and Section 6 the interpretation; Section 7 concludes. Appendix A lists every deviation and disclosure.

**Box 1. Terms used in this paper**

| Term | Meaning |
| --- | --- |
| **Credit impulse** | The change in new borrowing by households and businesses over four quarters, as a share of GDP. It shows whether borrowing is speeding up or slowing down (§3.1). |
| **Z.1** | The Federal Reserve's quarterly *Financial Accounts of the United States*, the source of the credit data. |
| **Vintage** | The data as one release printed them. Later releases revise the figures, so each quarter has many vintages. |
| **Real time** | Only what had been published when the forecast was made. |
| **Revised** | The figures as they stand today, which no forecaster had at the time. |
| **Origin** | The date a forecast is made. At origin o, GDP is known through quarter o − 1 and credit through q\* = o − 2. |
| **Horizon** | How far ahead the forecast looks. The target is quarter o + 4, four quarters after the origin quarter o (h = 4), the convention the SPF uses, so the comparison with professional forecasts is like for like. GDP is observed only through o − 1, so the target lies five quarters after the latest GDP figure available. |
| **SPF** | The Philadelphia Fed's Survey of Professional Forecasters. Its median forecast stands for what professionals expected. |
| **AR(2)** | The benchmark. It forecasts a series from its two most recent values. The credit model adds four lags of the impulse. |
| **Direct forecast** | A regression of the value four quarters ahead on today's data, so the model never has to forecast credit. |
| **RMSE ratio** | The credit model's root-mean-square error divided by the benchmark's. Below 1, credit helped; above 1, it hurt. A gain is a fall in forecast error, not in output or unemployment: a 40% gain means errors 40% smaller (ratio 0.6). |
| **Clark–West test** | Tests whether the larger model forecasts better. It corrects for the estimation noise that the extra variables add even when they carry no information, noise that would otherwise bias the comparison towards the benchmark. |
| **Block bootstrap** | Builds intervals by resampling forecast errors in runs of four quarters, so that errors close in time stay together. |
| **Holm correction** | Keeps the chance of any false positive across the four confirmatory tests at the stated level. |
| **Preregistration** | Publishing the plan, the code and the wording of the conclusions before seeing any results. Here that happened in release v1.0-lock. |
| **Confirmatory** | Fixed in advance; these tests decide the conclusion. |
| **Exploratory** | Reported for insight; these analyses cannot overturn the conclusion. |

## 2. Related literature

The paper sits where three literatures meet: credit and the business cycle, real-time data, and forecast evaluation.

**Credit and the business cycle.** Long-run cross-country evidence links credit booms to later downturns (Schularick and Taylor, 2012; Jordà, Schularick and Taylor, 2013), and rises in household debt predict slower growth (Mian, Sufi and Verner, 2017). Buoyant credit-market sentiment predicts weaker growth (López-Salido, Stein and Zakrajšek, 2017), and credit-gap indicators underpin countercyclical policy rules (Aikman, Haldane and Nelson, 2015). The *credit impulse*, the change in new borrowing scaled by GDP, was proposed in late 2008 to explain why recoveries can occur without credit growth (Biggs, Mayer and Pick, 2009). Keen popularised a closely related "credit accelerator" within a Minskian account of financial instability (see Keen, 2013). Most of this evidence uses revised data and in-sample or pseudo-out-of-sample designs. Credit spreads, a price rather than a quantity, carry substantial predictive content (Gilchrist and Zakrajšek, 2012), but they measure a different channel from the credit flows studied here. My question is narrower: would credit quantities, as published, have improved forecasts?

**Real-time data.** Real-time datasets let a researcher reproduce what a forecaster could have known (Croushore and Stark, 2001; Croushore, 2011); Edge and Gürkaynak (2010) and Del Negro and Schorfheide (2013) use them to evaluate model forecasts. The closest precedent is Edge and Meisenzahl (2011). Using real-time Z.1 vintages, they showed that revisions to the US credit-to-GDP gap were about as large as the gap itself, and came mainly from the filter's end-point problem rather than from revisions to the data. They asked whether the gap was reliable; I ask whether credit improved forecasts, and I replicate their decomposition on my vintages as a check (Section 3).

**Credit signals out of sample.** Early-warning studies test credit indicators in real time as predictors of *crises* (for example, Alessi and Detken, 2011), not of output or unemployment. López-Buenache, Borsi and Rosa-García (2025) find that credit contractions improve the identification and recursive forecasting of US labour-market slack in a Markov-switching framework; I could not confirm whether their data are vintage-based. My exploratory E1 applies a version of their signal to strictly real-time vintages over an overlapping window, 2000–2019.

**Methods.** The tests follow Clark and West (2007) for nested forecast comparisons, with fixed-b inference (Kiefer and Vogelsang, 2005) and the Holm correction across the confirmatory family. Conditioning on realised regressors is established practice, for example in the fixed-regressor bootstrap (Hansen, 2000), and calibrating an interval's nominal level against simulated coverage goes back to Loh (1987); I claim priority for neither. For one predictor path and one simulated process, this paper shows that a single feature of the predictor can bias both the power analysis and the intervals of a real-time forecasting evaluation. Here the credit impulse's variation is concentrated in one episode: Gaussian simulations overstated power, and block-bootstrap intervals covered less than their nominal level (Sections 4.4 and 5.1).

## 3. Data

The dataset reconstructs what a forecaster could have read in each quarterly Z.1 release from June 1999 to December 2019, with every vintage dated to its day of publication.

### 3.1 Real-time credit vintages

I downloaded all 83 quarterly Z.1 releases from 11 June 1999 to 12 December 2019, plus the release current at download (11 September 2026, with data to 2026Q2), from the Federal Reserve's archive. I verified every release date against the archive and checked the June 1999 vintage by hand against the printed tables. June 1999 is the first release with a full machine-readable quarterly history. Earlier releases print only the last four or five years, which is why the confirmatory sample starts at the 1999Q3 origin. Reaching back to 1990 would need hybrid vintages, splicing the quarters printed in each earlier release (some only as scanned images) onto older history from June 1999; the protocol treats that extension as exploratory.

Credit is household plus nonfinancial business debt securities and loans, both as flows (seasonally adjusted transactions at annual rates, divided by four) and as levels. I handled three breaks by rule, not by smoothing:

- **Series code.** The household code changed from 154102005 to 154104005 in the September 2010 release, when "credit market instruments" became "debt securities and loans". The parser matches series by code, never by position.
- **Units.** In March 2011 the debt files switched, without notice or change of name, from billions to millions of dollars. A parser check that compares every consecutive pair of vintages caught the switch as a median level ratio of exactly 1000.000. After the fix, no consecutive pair differs by more than a factor of 2 in median level.
- **File format.** CSV files replaced fixed-width files in September 2016, and the current release renames the debt tables.

As a consistency check, changes in levels track the flows closely (correlation 0.98 in the December 2019 vintage).

The primary measure is the credit impulse, the change in the four-quarter credit flow scaled by four-quarter nominal GDP:

```latex
CI_t = 100 \times \frac{S_t - S_{t-4}}{N_t}, \qquad S_t = \sum_{j=0}^{3} F_{t-j}, \qquad N_t = \sum_{j=0}^{3} Y^{nom}_{t-j}
```

Nominal GDP comes from the GDP vintage available on the same date. Within every vintage I also compute three secondary measures:

- credit growth from levels;
- real credit growth, deflated by the real-time GDP deflator;
- the credit-to-GDP gap, from a one-sided HP filter with λ = 400,000 and at least 40 quarters of history, the Basel III convention (Drehmann et al., 2010; Drehmann and Yetman, 2018, defend it against alternative filters).

### 3.2 Macro vintages and forecasts

GDP, deflator and unemployment vintages come from the Philadelphia Fed's Real-Time Data Set for Macroeconomists, each dated to the 15th of the middle month of its quarter.

- **Revised targets** come from the 2026Q3 vintage, frozen and hashed.
- **Early-estimate targets** come from the vintage two quarters after the target quarter.
- **SPF forecasts** are the median four-quarter-ahead forecasts: drgdp6 for GDP growth and UNEMP6 for the unemployment rate. Survey deadlines come from the Philadelphia Fed's release-dates file.
- **The two-year Treasury yield** (FRED GS2), which is never revised, enters both versions of the exploratory BVAR, with and without credit, so the comparison isolates credit. Monthly values are averaged over each complete quarter.

At every one of the 78 forecast origins, the latest Z.1 release ended two quarters before the origin (k = 2).

### 3.3 How much are credit data revised?

Revisions to credit flows are modest: first releases correlate at 0.96–0.99 with today's values. Revisions to the credit-to-GDP gap are large, and almost all come from its filter. Table 1 compares each quarter's first-release value with today's for 83 quarters, 1999Q1–2019Q3.

**Table 1. First-release versus revised credit measures, 1999Q1–2019Q3**

| Measure | Mean revision (pp) | SD of revision | Noise / signal | Correlation | Sign agreement |
| --- | --- | --- | --- | --- | --- |
| Credit impulse | +0.03 | 0.95 | 0.28 | 0.96 | 86% |
| Credit growth | −0.19 | 0.69 | 0.18 | 0.99 | 98% |
| Real credit growth | −0.30 | 0.70 | 0.21 | 0.98 | 95% |
| Credit-to-GDP gap, data revisions only | −1.13 | 1.32 | 0.14 | 0.99 | 100% |

*Noise / signal = SD of revision ÷ SD of the revised series. Revisions to GDP barely matter: credit-only revisions to the impulse (noise / signal 0.28) are as large as total revisions.*

The largest revisions to the impulse fall at turning points (Figure 1). The first estimate for 2008Q3 was −7.5; today it is −5.2. For 2006Q4 the first estimate showed credit slowing (−0.27), where today's data show it still accelerating (+2.25).

![Figure 1. Credit impulse and credit growth: first release versus revised, 1999Q1–2019Q3](../figures/fig1_first_release_vs_revised.png)

Replicating Edge and Meisenzahl (2011) on these vintages (the pre-registered descriptive exercise D2; Figure 2), I split each quarter's gap revision into a data component (the gap recomputed on today's data, filtered only up to that quarter) and an end-point filter component. The data component accounts for 3% of the revision variance and the filter for 108%, with a covariance of −11%; mean absolute revisions are 1.4 pp (data) and 7.0 pp (filter). The real-time and final gaps correlate at 0.65 and share a sign in 76% of quarters. The gap's denominator distorts it too: it rose during the 2001 recession because GDP slowed while credit kept growing, the countercyclical bias that Repullo and Saurina (2011) identify in the gap-based Basel III buffer rule. The replication reproduces their finding, which supports the dataset, and it is why I made the unfiltered impulse the primary measure.

![Figure 2. Credit-to-GDP gap: real time, quasi-real time and final, with the D2 decomposition](../figures/fig2_gap_decomposition_D2.png)

## 4. Design

Every forecast uses only data published before its origin date, and I fixed every specification below in the locked protocol (v2.3, §§5–11) before scoring any outcome. The two version numbers differ in kind: v2.3 numbers the protocol document, and v1.0-lock tags the GitHub release that froze it. Appendix A gives the timeline.

### 4.1 Grid, origins and targets

The sample has 78 forecast origins, 1999Q3–2018Q4. The horizon is four quarters (h = 4), matching the SPF; one and two quarters are secondary. The origin date is the 15th of the middle month of quarter o. GDP and unemployment are observed through o − 1 in that date's vintage; credit comes from the latest Z.1 release before the origin and ends at q\* = o − 2. GDP growth is annualised and discretely compounded, as in BEA and SPF practice, and unemployment is the quarterly average.

The sample ends with targets in 2019Q4. The first draft of the protocol, which I wrote in 2026 with the pandemic known, already set that endpoint, for a substantive reason. In 2020–21 output moved for reasons unrelated to private credit, and government-guaranteed lending moved the credit series, so one linear model across the pandemic would mix two relationships. Section 5.6 reports the pandemic period separately, as the protocol's checklist promised.

The design crosses two credit vintages (real-time, revised) with two targets (early estimate, revised). The primary cell is real-time credit scored against the revised target. The *credit-revision premium* measures how much better the credit model would have looked with today's credit data. It is the primary-cell RMSE ratio minus the same ratio computed with revised credit and the real-time GDP denominator, so a positive premium means revised credit forecasts better. Keeping the real-time denominator isolates revisions to the credit data; I also report a total premium, which revises the denominator too. The premium is a difference between two ratios, not itself a forecasting gain.

### 4.2 Models

The benchmark is a direct AR(2). The credit model adds four published lags of the credit measure, each entering at its release lag with nothing filled in:

```latex
y_{o+h} = \alpha + \phi_1 y_{o-1} + \phi_2 y_{o-2} + \sum_{j=0}^{3} \beta_j X_{q^*-j} + \varepsilon_{o+h}
```

A direct specification needs no forecast of credit and nests the AR(2) exactly. I re-estimate both models at every origin on an expanding window from 1965Q1, using only pairs whose target had been published by the origin.

All estimation data come from the vintages available at the origin: GDP and unemployment from that origin's RTDSM vintage, and the whole credit history from the latest Z.1 release. Past quarters therefore enter as the origin's releases describe them, not as they were first published. This is end-of-sample-vintage estimation, the regression a forecaster at the origin could actually have run. Estimating each training pair on its own historical vintage would answer a different question (Koenig, Dolmas and Piger, 2003), and I do not test it. For example, the forecast at origin 2010Q3 (15 August 2010) uses GDP through 2010Q2 from the August 2010 vintage and credit through 2010Q1 from the Z.1 release of 10 June 2010. It is trained on pairs whose target is 2010Q2 or earlier, and it forecasts annualised GDP growth in 2011Q3. "Four quarters ahead" thus counts from the origin quarter: the target lies five quarters beyond the last GDP observation and six beyond the last credit observation.

The linear specification is a deliberate restriction, not a claim that credit acts linearly. It asks one falsifiable question: did a linear term in the impulse, with the same coefficients across the cycle, improve forecasts on average? It is also the specification the preregistration committed to. It has two costs. A linear model pools states, so if credit helps in some phases of the cycle and hurts in others, the pooled coefficient averages opposite-signed effects and can understate state-specific ones; Section 5.3 documents exactly that. And four fixed lags assume a relationship that is stable within the window and symmetric in sign. The exploratory specifications relax both: S5 allows asymmetric and contraction-specific effects, S4 and E1 allow richer dynamics and regimes, and the subsample split S6 and a rolling window allow instability. I kept the confirmatory family linear because building in state dependence would have multiplied the parameters to estimate against 78 origins dominated by one episode. Section 4.4 shows the design can reliably detect only gains of roughly 40% or more. The null in Section 5.1 is therefore about the average linear relationship, not about any particular regime.

For the SPF counterfactual (P2a), the bias-corrected benchmark is the SPF forecast plus α̂, and the credit-corrected forecast adds β̂ times the impulse published before the survey deadline. Both keep the coefficient on the SPF forecast at 1. They are estimated on surveys from 1990Q3 onwards whose targets had been published, with values as published at the deadline; the first origin has 32 training pairs. The result concerns this additive correction only; I do not test other ways of combining survey forecasts with credit.

The revision test (P3) asks whether the impulse predicts how GDP growth in quarter s is later revised. It regresses the revision, from the advance estimate to today's, on the impulse published before the advance release, controlling for advance growth in s and s − 1. The sample has one observation per quarter: 83 quarters, 1999Q2–2019Q4.

### 4.3 Inference and decision rules

The confirmatory family is P1a (GDP), P1b (unemployment), P2a (SPF) and P3, with the Holm correction across all four.

- **Forecast comparisons** use Clark–West statistics with Bartlett HAC variance (h − 1 lags) and fixed-b critical values, adopted because normal critical values over-rejected at these sample sizes.
- **P3** uses a restricted wild (Rademacher) block bootstrap of its HAC t-statistic (block length 4). A few extreme impulse values made the fixed-b HAC test over-reject: 14–18% at a nominal 5%, against 3.5% for the bootstrap. I made this switch on synthetic data before the lock. The locked code computes both p-values, and I saw both for the first time in the single run.
- **Intervals** for RMSE ratios come from a moving-block bootstrap (block length 4, 2,000 draws).

All interpretation runs through a pre-committed map. Before the lock I wrote three headline sentences, for "positive", "null with a large premium" and "null with a small premium". A premium is *large* if it is at least 0.05 in ratio units and its 90% interval excludes zero.

### 4.4 Power, and why a Gaussian simulation overstated it

The credit impulse is quiet for most of 1999–2019 and swings violently in 2008–09: those 8 of 83 quarters hold 72% of its squared deviations from the mean. Any forecasting gain must therefore come from a handful of quarters, which makes Clark–West loss differentials highly skewed. My first power simulations drew the impulse from a fitted Gaussian AR(2) and missed this. I re-ran them conditional on the realised credit path, simulating targets, vintages and SPF forecasts around the real impulse and using no outcome data. Table 2 compares the two.

**Table 2. Unadjusted power at a true RMSE ratio of about 0.90**

| Test | Gaussian-path simulation | Actual credit path |
| --- | --- | --- |
| P1a GDP | 0.86 | 0.45 |
| P1b unemployment | 0.70 | 0.31 |
| P2a SPF | 0.77 | 0.51 |

*Each cell uses the nearest simulated true ratio: 0.91 for P1a, 0.93 for P1b and P2a on the actual path, and 0.92 for P2a on the Gaussian path. Rows therefore compare the two simulations for one test; columns are not at identical ratios.*

On the actual path, 80% power requires a ratio of about 0.6, a gain of roughly 40%. Under the pre-registered power rule, every confirmatory test therefore falls in the "estimate only" band. I report each as an estimate with a 90% interval, claim a "credible improvement" only if the whole interval lies below 1 (for P3, excludes zero), and use no significance language. On synthetic data with the real credit path, this rule declares a false improvement 0–2% of the time and detects a true 7% gain 29–40% of the time. I took these decisions before seeing any outcome (Appendix A).

The lesson, shown here for one path, is that when a predictor's information sits in one episode, power should be simulated on its realised path. Section 5.1 shows that the same concentration distorts the intervals.

## 5. Results

No confirmatory estimate shows a credible improvement. On average, credit worsened real-time GDP forecasts by 10.6%, though the sample cannot rule out an improvement of up to about 6% (Table 3b), and the credit-revision premium is close to zero. Every result comes from a single run of the locked code (results.json, SHA-256 9e4239dd116eaea7c9f65df83f85d349f338aeb4adb6ff16904a6793ed6fa99c).

### 5.1 Confirmatory tests

**Table 3. Confirmatory results, h = 4, 1999Q3–2018Q4 origins**

| Test | Estimate | 90% interval | Credible improvement | Holm-adjusted rejection |
| --- | --- | --- | --- | --- |
| P1a: GDP growth, RMSE ratio | 1.106 | 0.984 – 1.356 | No | No |
| P1b: unemployment rate, RMSE ratio | 1.011 | 0.994 – 1.043 | No | No |
| P2a: SPF median GDP, RMSE ratio | 1.025 | 0.988 – 1.076 | No | No |
| P3: GDP revision on impulse, pp per point | 0.111 | −0.047 – 0.269 | No | No |

*Ratios are credit model ÷ benchmark; below 1 means credit helps. Unadjusted p-values, for completeness only: 0.555 (P1a), 0.618 (P1b) and 0.665 (P2a) from fixed-b Clark–West tests, and 0.221 (P3) from the wild block bootstrap. The locked code also reports a fixed-b HAC p-value of 0.036 for P3. It is not valid here: on the real credit path that test rejects a true null 14–18% of the time at a nominal 5%, which is why I adopted the wild bootstrap before the lock (Section 4.3). Figure 3 plots the estimates with the other grid cells.*

Read at face value, the favourable ends of these intervals correspond to gains of about 1.6% for GDP, 1.2% for the SPF and 0.6% for unemployment. They are not firm bounds, because the intervals are too narrow.

Power and intervals answer different questions. Power describes the design: how often a true gain of a given size would yield a credible improvement in repeated samples. An interval describes this sample. But an interval is also a repeated-sample procedure, and the concentration that weakens power also makes the interval less reliable. I checked this after the lock, on synthetic outcomes built around the real credit path (300 replications; Appendix A). Nominal 90% block-bootstrap intervals contained the true ratio only 80–81% of the time for GDP, 74–75% for unemployment and 69–77% for the SPF correction, with or without a true credit effect. In the two halves of the S6 split, the GDP figure was 74–83%. Resampling blocks from a sample whose information sits in one cluster understates the uncertainty.

The misses are also one-sided. With no credit effect, the intervals tend to sit below the true ratio, flattering credit; with an effect, they tend to sit above it, understating the gain. Raising the nominal level is not a general cure: for GDP a 97% percentile interval reaches 90% coverage, but for unemployment and the SPF correction even 99% intervals reach only 86–93%.

As a sensitivity analysis, Table 3b therefore widens each interval about its point estimate. It uses the smallest factor that restores 90% coverage at two simulated effect sizes, a simple form of calibrating a nominal level against simulated coverage (Loh, 1987). The factors are 1.35 for GDP, 1.75 for unemployment and 2.1 for the SPF correction. These are not repaired confidence intervals. They rest on one simulated data-generating process, on two effect sizes chosen after the results were seen (spanning no effect and a moderate one) and on 300 replications at each. I did not explore other error processes or bootstrap schemes (Appendix D). The pre-registered decision rule uses the locked intervals.

**Table 3b. Locked and coverage-calibrated 90% intervals (post-lock sensitivity analysis)**

| Test | Estimate | Locked interval | Widening factor | Calibrated interval | Largest gain inside |
| --- | --- | --- | --- | --- | --- |
| P1a: GDP growth | 1.106 | 0.984 – 1.356 | 1.35 | 0.941 – 1.443 | 5.9% |
| P1b: unemployment rate | 1.011 | 0.994 – 1.043 | 1.75 | 0.981 – 1.067 | 1.9% |
| P2a: SPF median GDP | 1.025 | 0.988 – 1.076 | 2.1 | 0.948 – 1.132 | 5.2% |

*Calibrated interval = estimate − factor × (estimate − lower end) to estimate + factor × (upper end − estimate), using the locked bootstrap draws. Factors from 300 replications at each of two effect sizes, synthetic outcomes on the real credit path. P3's interval uses a different bootstrap whose test size was checked before lock (Section 4.3) and is not recalibrated.*

Neither set of intervals shows a credible improvement, so the null does not depend on the correction. What changes is how much the data can exclude: the calibrated intervals allow average gains of up to about 6% for GDP, 5% for the SPF correction and 2% for unemployment. The power analysis agrees, since gains of that size would usually go undetected.

![Figure 3. RMSE ratios with 90% intervals for the confirmatory tests and grid cells](../figures/fig3_grid_rmse_ratios.png)

### 5.2 The grid and the credit-revision premium

Revised credit leaves the GDP ratio at 1.106. It moves only in the fourth decimal (1.1065 to 1.1060), because revisions to the impulse are small beside its 2008–09 swings. For unemployment the ratio moves from 1.011 to 1.003. The credit-revision premium is +0.0005 for GDP (90% interval −0.066 to 0.037) and +0.008 for unemployment (−0.018 to 0.024), both *small* under the pre-registered rule. The total premiums, which also revise the GDP denominator, are almost identical (+0.0005 and +0.0075). Against early-estimate targets the ratios are 1.129 for GDP and 1.011 for unemployment.

### 5.3 Where credit gained and lost

The full-sample loss for GDP comes from one turn of the cycle. Define the cumulative gain at origin o as the running sum, over origins up to o, of the benchmark's squared error minus the credit model's; positive values mean credit has helped so far. Figure 4 plots it. Table 4 splits the final totals into periods that partition the sample, so the contributions add to the total.

**Table 4. Contributions to the cumulative squared-error gain, by origin period (positive = credit helps)**

| Origins | GDP (P1a) | Unemployment (P1b) | SPF (P2a) |
| --- | --- | --- | --- |
| 1999Q3–2006Q4 | +18.2 | −0.75 | −23.2 |
| 2007Q1–2009Q4 | +11.6 | +1.04 | −8.5 |
| 2010Q1–2011Q4 | −135.6 | −1.07 | +5.0 |
| 2012Q1–2018Q4 | −3.1 | −1.16 | +0.2 |
| **Total** | **−108.9** | **−1.94** | **−26.5** |

**GDP.** The credit model is ahead from the first origin (1999Q3), peaks at the 2008Q2 origin and holds its lead through forecasts made in 2009. It then loses heavily on forecasts made in 2010–11 for 2011–12: −135.6 over origins 2010Q1–2011Q4. Of the total cumulative loss of 108.9, origins 2007Q1–2010Q4 contribute 74.1 (68%).

**Why the model lost: it expected a rebound.** The mechanism is simple (Table 5, and Figure 7 after Section 5.5). Throughout the sample the four credit coefficients sum to a negative number: between −0.16 and −0.28 up to 2010, and about −0.10 by 2018. At this lead, then, a credit contraction raised the growth forecast, a bounce-back pattern learned from earlier cycles. The collapse did not reshape the coefficients; it changed the inputs. At origins in 2010 the lags held real-time impulses of −3 to −12, so the credit term added 2.4–4.3 percentage points. The model forecast annualised growth of 5.4–7.5% for 2011; the outcomes were between −0.9% and 4.6%. Because the lags reach back a year, the credit term stayed at 1.2–3.4 points through origins in 2011, after the impulse itself had turned positive. As these misses entered the training sample, the coefficient sum shrank towards −0.1.

![Figure 4. Cumulative squared-error differences for P1a, P1b and P2a](../figures/fig4_cumulative_sed.png)

**Table 5. The six largest credit-model losses, P1a (post-lock, descriptive)**

| Origin | Target | Impulse at q\* | Coefficient sum | Credit term (pp) | AR(2) forecast | Credit forecast | Outcome | Loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2010Q3 | 2011Q3 | −5.4 | −0.27 | +3.6 | 3.0 | 6.8 | −0.1 | 37.6 |
| 2010Q1 | 2011Q1 | −10.4 | −0.28 | +2.4 | 2.8 | 5.4 | −0.9 | 26.1 |
| 2011Q3 | 2012Q3 | +3.7 | −0.14 | +2.2 | 3.1 | 5.5 | 0.6 | 17.9 |
| 2010Q2 | 2011Q2 | −7.1 | −0.27 | +3.6 | 2.9 | 6.7 | 2.7 | 15.6 |
| 2011Q2 | 2012Q2 | +3.1 | −0.21 | +2.6 | 3.0 | 5.8 | 1.8 | 14.3 |
| 2011Q1 | 2012Q1 | +0.6 | −0.25 | +3.4 | 2.9 | 6.5 | 3.4 | 9.6 |

*Growth is annualised quarterly real GDP growth in the target quarter. The credit term is the sum over the four lags of coefficient times impulse; the impulse column shows only the latest lag. Loss = credit-model squared error minus benchmark squared error. These six origins account for 121 of the 139 squared-error units lost after 2008Q4. Computed by re-running the locked P1a specification unchanged; the forecasts match the locked run exactly.*

**The pre-2008Q4 gain is fragile.** Splitting origins at 2008Q4 (exploratory S6) gives ratios of 0.959 (0.896–0.982) before and 1.522 (1.148–1.863) after. S6 was pre-specified as exploratory, and its split date reflects when the impulse was defined (late 2008), not the crisis. The gain is spread out: origins 1999–2006 contribute 18.2 of the 30.2 total, and 2007Q1–2008Q3 add 12.1. Its interval lies wholly below 1, but two things limit what that means.

First, the intervals undercover (Section 5.1), so the result looks cleaner than it is: with no credit effect, the pre-2008Q4 interval fell wholly below 1 in 5% of simulated replications. Widened by the factor the simulation supports for this half (1.35), the interval is 0.874–0.990 and still lies below 1. But a widened interval does that about 3% of the time with no credit effect, so among 32 exploratory comparisons one such result is unsurprising.

Second, the realised credit path gives the pre-2008Q4 forecasts almost nothing to work with. The quarters that enter them, up to 2008Q1, are 45% of the sample but hold only about 14% of the impulse's squared deviations, so any credit effect shows up after the split. The design could not have detected a pre-crisis effect even if one existed. That is a limit of the design, not evidence that no such effect exists.

**Unemployment and the SPF.** Neither shows a sustained gain; unemployment's 2007–10 contribution is a small +0.5. The SPF correction's losses come almost entirely from 1999–2006 (−23.2 of −26.5), when it was estimated on only 32 to 61 surveys, and it gained in 2010–11 (+5.0). Estimation noise in a short training sample is a likelier explanation than the SPF already containing the credit information, though the design cannot separate the two. A later training start does not help credit: on the 68 origins common to all three starts, the ratio is 1.019 with the locked 1990Q3 start, 1.130 from 1993Q1 and 1.095 from 1996Q1 (post-lock check, Appendix A).

The asymmetry also shows what a comparison of means can miss. A credit signal that sharpens forecasts of bad outcomes but adds noise in normal times would register as a null, or a loss, in RMSE terms. Testing for it needs quantile or growth-at-risk forecasts (Section 7).

### 5.4 Exploratory results

I made no multiple-comparison correction across the 27 exploratory tests (32 comparisons including the S6 splits and the direction check), so chance alone would be expected to produce one or two nominally significant results. Four fell below 0.05, all for unemployment. If the 27 tests were independent, four or more would occur with probability 0.044. But the four share one target and draw on one credit aggregate, so they are positively correlated and the true probability is higher. The pattern is suggestive, not confirmatory, and none of it moves the interpretation (Section 6).

**Table 6. Selected exploratory RMSE ratios, h = 4**

| Specification | GDP growth | Unemployment |
| --- | --- | --- |
| S2: credit growth (levels) | 1.089 | 1.041 |
| S2: credit-to-GDP gap | 1.102 | 0.922 |
| S2: real credit growth | 1.030 | 0.978 |
| S2: impulse from level differences | 1.107 | 1.014 |
| S5: asymmetric impulse (CI⁺, CI⁻) | 1.053 | 1.249 |
| S5: real-credit contraction model | 1.055 | 0.957 |
| S4: BVAR with credit vs without | 0.989 | 0.954 |
| E1: Markov-switching contraction signal | — | 0.968 |
| R1: ragged edge filled by AR(4) / VAR(2) | 1.054 / 1.056 | 1.001 / 1.000 |
| 60-quarter rolling window | 1.243 | 1.097 |
| h = 1 / h = 2 | 1.030 / 1.030 | 1.034 / 1.017 |

*Unadjusted one-sided p-values below 0.05 occur only for unemployment: the gap (0.002), real credit growth (0.025), the contraction model (0.002) and E1 (0.026). The BVAR's bootstrap p is 0.078.*

Slower-moving credit measures improve unemployment forecasts by 2–8%, and the BVAR with the impulse by 4.6%. For GDP only the BVAR falls below 1, at 0.989. The 60-quarter rolling window does worse than the expanding window: 1.243 for GDP and 1.097 for unemployment. Instability in the credit–output relationship would produce that pattern, but so would the extra estimation noise of a shorter window, and this comparison cannot tell them apart.

The SPF unemployment counterfactual (P2b, a pre-registered exploratory test) gives 1.115 (unadjusted p = 0.147): correcting the SPF unemployment forecast with credit made it worse, as it did for GDP in P2a. Unemployment at this horizon is hard to beat, and models of labour-market flows are the stronger benchmark for further work (Barnichon and Nekarda, 2012). The robustness version of P2a, using medians of forecasters' own growth rates, gives 1.026. Adding credit lowers the share of correct direction calls for unemployment from 66.2% to 64.9%.

### 5.5 Threshold signals (D1)

The impulse rule flagged both recessions late, and the credit-growth rule flagged neither (Figure 5, which labels both recession episodes late, as the rule does). The scoring rule comes from §10 of the protocol version dated 17 October, written before the signals were computed. A hit is an episode that starts one to six quarters before an NBER peak; an episode that starts between peak and trough is late. In real time, "impulse negative for two quarters" began in 2001Q4, three quarters after the 2001Q1 peak, and in 2007Q4, the peak quarter itself. The second is better described as coincident than late, but neither gave advance warning. In revised data the episodes began in 2001Q3 and 2009Q1. "Impulse negative for two quarters" also gave two false alarms in each version and was on in 29% of real-time quarters. "Credit growth below nominal GDP growth" produced only false alarms, all starting in 2010 or later.

![Figure 5. Credit threshold signals, real-time and revised (D1)](../figures/fig5_threshold_timeline.png)

Figure 6 plots the P3 data: the 2009 quarters, with impulses of −10 to −12, show revisions in both directions.

![Figure 6. GDP revisions against real-time credit (P3)](../figures/fig6_gdp_revisions_vs_ci.png)

![Figure 7. P1a credit coefficients and forecasts by origin](../figures/fig7_p1a_coefficients_forecasts.png)

### 5.6 The pandemic period, 2020–21 (not preregistered)

The protocol's checklist promised that 2020–21 would be "reported separately", and this subsection does so. I committed and tagged its plan and script (`pandemic-plan`, commit b9a7fc0) on 20 October 2026, before downloading any 2020 Z.1 release (Appendix A). The locked P1a, P1b and P2a models run unchanged for the eight forecasts the locked sample excluded: targets 2020Q1–2021Q4, from origins 2019Q1–2020Q4. Credit is as published in the December 2019 and the March, June and September 2020 releases. With only eight targets, I compute no p-values or intervals.

**Table 7. The pandemic-period forecasts, h = 4 (not preregistered)**

| Test | RMSE ratio, eight targets | Mean error, benchmark (pp) | Mean error, credit model (pp) | Ratio, origins 1999Q3–2020Q4 | Locked ratio, 1999Q3–2018Q4 |
| --- | --- | --- | --- | --- | --- |
| P1a: GDP growth | 0.992 | −1.00 | −0.80 | 1.014 | 1.106 |
| P1b: unemployment rate | 0.910 | −0.02 | −0.19 | 0.925 | 1.011 |
| P2a: SPF median GDP | 0.999 | −1.39 | −1.34 | 1.004 | 1.025 |

*Mean error = forecast minus outcome, averaged over the eight targets. Outcomes are from the 2026Q3 vintage, as in the main study. The forecast-by-forecast tables are in the release (pandemic/results/).*

The pre-written sentences (plan §4) are reproduced word for word, so their repeated clauses are deliberate:

- **P1a (GDP).** Over the eight pandemic-period targets, the credit model's forecasts were about as accurate as the benchmark's (ratio 0.992). With eight targets dominated by one shock that did not originate in credit, this is an illustration, not evidence about predictive content. It does not alter the pre-registered conclusion. On average the credit model under-forecast GDP growth (mean error −0.80 pp, against −1.00 for the benchmark). Adding these targets changes the full-sample ratio from 1.106 to 1.014.
- **P1b (unemployment).** Over the eight pandemic-period targets, the credit model's forecasts were about as accurate as the benchmark's (ratio 0.910). With eight targets dominated by one shock that did not originate in credit, this is an illustration, not evidence about predictive content. It does not alter the pre-registered conclusion. On average the credit model under-forecast unemployment (mean error −0.19 pp, against −0.02 for the benchmark). Adding these targets changes the full-sample ratio from 1.011 to 0.925.
- **P2a (SPF).** Over the eight pandemic-period targets, the credit model's forecasts were about as accurate as the benchmark's (ratio 0.999). With eight targets dominated by one shock that did not originate in credit, this is an illustration, not evidence about predictive content. It does not alter the pre-registered conclusion. On average the credit-corrected SPF forecast under-forecast GDP growth (mean error −1.34 pp, against −1.39 for the bias-corrected forecast). Adding these targets changes the full-sample ratio from 1.025 to 1.004.

**Explanatory note (a deviation from the plan's wording, declared under its §6; Appendix A).** The pre-written sentences omit two facts a reader needs.

- **One forecast decides the unemployment ratio.** At the 2020Q3 origin, both models had been trained on data that included the jump in unemployment to 13.0% in 2020Q2, and both extrapolated it: for 2021Q3 the benchmark forecast 26.0% and the credit model 23.8%, against an outcome of 5.1%. That target alone accounts for −88.8 of the eight-target squared-error difference. The ratio of 0.910 therefore reflects a less extreme extrapolation, not information in credit.
- **The extended-sample ratios move towards 1 mechanically.** Annualised GDP growth was −28.0% in 2020Q2 and +34.9% in 2020Q3, so both models' pandemic-period squared errors dwarf anything in 1999–2018. Adding them to both sides of the ratio pulls it towards 1. The falls from 1.106 to 1.014 for GDP and from 1.011 to 0.925 for unemployment reflect the scale of the pandemic errors, not better credit forecasts.

The real-time impulse turned strongly positive in the first half of 2020, as firms drew on credit lines and governments guaranteed new loans. The June release put it at 2.97 for 2020Q1 and the September release at 3.96 for 2020Q2, against 3.15 and 4.47 in revised data. By then the credit coefficients summed to only about −0.1, so the credit term was under half a percentage point in every pandemic-period forecast.

## 6. Interpretation and limits

Under the pre-committed map, the headline for the confirmatory family is **"null, small premium"**:

> *Credit shows no detectable predictive content in either real-time or revised data at this sample size; the published evidence does not rest on revisions, and given that the available credit variation is concentrated in 2008–09, the design could reliably detect only very large gains, of roughly 40% or more.*

The detailed map distinguishes two cases. In a "specification story", a signal appears only in a particular state (here, contractions: S5 supported). In a plain null, no pre-registered specification recovers one (S5 null). S5 was mixed: the contraction model improved unemployment forecasts (0.957), the asymmetric impulse worsened them (1.249), and both worsened GDP forecasts. The protocol left "supported" undefined for S5, so I record S5 as not supported, the conservative reading. I made that call after seeing the results, and Appendix A discloses it. The final reading under the map is: *no evidence of predictive content under real-time data at this sample size; only very large gains ruled out.*

In plain terms, the study found no improvement but is too underpowered to rule out modest gains. Two refinements sharpen the pre-committed wording without changing it. "No detectable predictive content" refers to the average relationship over the full sample; Section 5.3 shows that the relationship was not stable either. And the statement that only very large gains could be detected must be read with Section 5.1. The coverage-calibrated intervals allow gains of up to about 6%, and the power analysis implies that gains well short of 40% could have been missed. The pandemic-period illustration (Section 5.6), run under a plan frozen before the 2020 data were downloaded, leaves this reading unchanged.

Four limits shape what the null means.

1. **It concerns the average, in a sample with one credit cycle.** Credit improved GDP forecasts by about 4% before 2008Q4 and hurt forecasts of the recovery. A forecaster who used the impulse only to judge downside risk might have done better than this linear model, though the pre-registered evidence cannot say whether such a rule would hold beyond one episode. The sample holds one large credit cycle: 2008–09 carries about three-quarters of the impulse's variation, which is also why power is low. The two recessions differed in character. The 2001 downturn is not generally treated as credit-driven in this literature; 2008–09 is; and in real time the impulse threshold flagged both late (Section 5.5). Such differences caution against a single, state-independent coefficient. This design cannot classify recession types or estimate episode-specific effects; that needs a regime-switching or interaction specification. Settling the question needs a longer real-time history: the hybrid 1990–1999 vintages the protocol leaves exploratory, or other countries' real-time data.
2. **The exploratory unemployment signals are leads, not findings.** The gap, real credit growth, the contraction model and the Markov-switching model all point the same way for unemployment, by 2–8%, as does the BVAR (4.6%). But the first four rest on slower-moving stock measures, the impulse itself raised the unemployment RMSE by 1.1%, and the multiplicity is high. The strongest, the gap (0.922), also carries the denominator distortion documented in Section 3.3, so its gain may reflect GDP dynamics rather than credit. Confirming any of them would take a new preregistered test on a different sample.
3. **The credit measures are narrow and stale.** All four are transformations of one aggregate, household plus nonfinancial business credit; they exclude financial-sector credit, central to the 2008 crisis. None can speak to the sectoral composition of debt, to debt-service burdens or to credit-supply indicators such as lending standards, which several literatures treat as central. At each origin the credit data also end two quarters before the GDP data the benchmark already uses. The test is of credit as it was available, not of credit observed at higher frequency. Filling that gap with credit-only AR or VAR forecasts made GDP forecasts worse (1.054 and 1.056; Table 6), so staleness alone does not explain the null. These limits bound what the null covers; they are not a claim that those channels are absent.
4. **The comparison is narrow.** The benchmark is a direct AR(2), not the best available forecasting model, and the SPF exercise tests one additive correction, asking only whether the information was in published data. The results make no causal claim about credit and demand, no claim about forecasters' rationality, and none about the DSGE or policy debates that motivated the project. And because the credit impulse was not defined until late 2008, the pre-2008 results show what the transformation would have delivered, not what forecasters knew.

### 6.1 Discussion beyond the pre-registered map

*This subsection relates the results to one theoretical literature. It is not part of the pre-registered interpretive map and carries no evidential weight beyond the estimates above.*

The results speak only indirectly to Keen's argument that credit creation drives aggregate demand and financial instability (Keen, 2013). They do not test, and cannot rule out, the proposition that credit dynamics matter causally for demand or for crises. They test a narrower forecasting implication: that the real-time credit impulse, the closest observable counterpart of the credit accelerator, delivers systematic average gains in four-quarter-ahead GDP and unemployment forecasts whatever the state of the cycle. Over 1999–2019 it did not, though intervals widened to restore their coverage allow average gains of up to about 6% for GDP, 5% for the SPF correction and 2% for unemployment (Table 3b). The negative coefficient path in Figure 7 explains why this forecasting model failed in 2011–12; it says nothing about the contemporaneous channel the credit accelerator describes.

Two readings fit these results, and the design cannot separate them.

- **Episode-specific value.** Credit dynamics matter but differ across cycles, so their forecasting value does not survive as a stable linear signal. The asymmetry in Section 5.3 fits this only partly. The pre-2008Q4 gain was small and spread across the expansion, with 12.1 of 30.2 from 2007Q1–2008Q3. The contrast is therefore less between a crisis and a recovery than between a long expansion and a recovery, and one episode cannot establish either.
- **Little extra information.** The impulse adds little that recent output data do not already carry.

Nor do the exploratory unemployment results favour the credit-accelerator view in particular. The small gains came from slower-moving stock measures, while the impulse itself, the measure closest to that view, raised the unemployment RMSE by 1.1%.

## 7. Conclusion

As published at the time, the US credit impulse left average four-quarter-ahead forecasts no better than a direct autoregressive benchmark in 1999–2019: the point estimates were 1.1% worse for unemployment and 10.6% worse for GDP, and every interval includes no change. Revised credit data would have done no better. The study found no improvement, but it is too underpowered to rule out modest gains: the post-lock sensitivity interval still allows gains of up to about 6%, while simulations show that, across repeated samples, the test could reliably detect only gains of roughly 40% or more. Most of the predictor's variation came during the 2008–09 crisis, while most of the GDP forecast loss came from forecasts of the recovery that followed: a small and fragile pre-crisis gain was more than wiped out when the model read the deep 2009–10 contraction as the prelude to a sharp rebound that did not materialise.

Two lessons follow. First, as a hypothesis for a future preregistered test: credit may be worth more as a guide to downside risk than as a linear predictor (extension 2). The exploratory pre-crisis gain hints at this, but one episode cannot show it. Second, when a predictor's variation is concentrated in one episode, real-time evaluations should check both power and interval coverage on the realised predictor path. I show this for one path and one simulated process; extension 3 below would test how far it generalises. Here, a Gaussian power simulation made an underpowered design look adequate, and moving-block bootstrap intervals looked tighter than they were.

The design points to five extensions, in rough order of value for cost. Each tests a new hypothesis and needs its own preregistration.

1. **Household versus business credit.** Splitting the aggregate within the existing vintages would test whether the null hides the household-debt signal emphasised by Mian, Sufi and Verner (2017).
2. **Downside risk.** The asymmetry in Section 5.3 and the downside-risk reading in Section 6 can be tested directly with quantile or growth-at-risk forecasts (Adrian, Boyarchenko and Giannone, 2019), which ask whether credit sharpens forecasts of bad outcomes. A null for the mean is compatible with a gain in the lower tail, and this is the most promising untested hypothesis here.
3. **Power for crisis-dominated predictors.** Neither the power correction (Section 4.4) nor the coverage result (Section 5.1) is specific to credit; together they merit separate study across other clustered predictor paths and error processes.
4. **Credit supply.** Lending standards and debt-service burdens, both observable in real time, measure a different channel from credit quantities.
5. **A cross-country real-time panel.** The most expensive option, it multiplies episodes rather than origins, and it is the only route to real power for a state-dependent specification.

Two other extensions would add computation but not evidence. With 78 origins and one dominant episode, regularised or nonparametric learners have little independent variation to exploit. Further linear variants of the confirmatory family would add to the multiplicity of Table 6 without testing a new hypothesis. Neither is a criticism of those methods; both need the longer or wider samples above. The pandemic period (Section 5.6) suggests one more question for a new plan: how government-guaranteed lending changes what the credit impulse measures.

The real-time credit vintages, all code and the locked protocol are public.

## Appendix A. Deviations and disclosures

I logged every change made after the design was drafted, with its date and whether I had seen results. The full log is part of the protocol record, published with each release; the table lists the changes that bear on the reported tests.

| Date (2026) | What | Results seen? |
| --- | --- | --- |
| 17 Oct | Real-time GDI vintages were too short (gate G3 failed), so exploratory test S3 was dropped, as the protocol pre-specified. | No |
| 19 Oct | First power simulations used one credit lag, a 1955 start, a looser SPF correction and no P3 controls. Corrected to the protocol's specification; wording bands re-derived. | No |
| 19 Oct | Normal critical values over-rejected; switched to fixed-b. | No |
| 19 Oct | Power re-estimated conditional on the actual credit path. All four confirmatory tests moved to "estimate only"; P3 moved to a wild block bootstrap; a 2007–10 crisis-share statistic added. | No |
| 19 Oct | The premium's sign convention was corrected so that positive means revised credit forecasts better; the E1 specification was written out in full. | No |
| 19 Oct | D1 threshold signals were computed during synthetic testing, because they use only credit data and recession dates; seen before lock. | D1 only |
| 19 Oct | 14:55 UTC. Protocol locked: GitHub release v1.0-lock, commit 4eb084f, DOI 10.5281/zenodo.23477871. | No |
| 19 Oct | 15:00:47–15:01:25 UTC. Phase 2 run once with the locked code; no deviations. Figures and this paper were produced afterwards, from results.json. | — |
| 19 Oct | S5 recorded as not supported, the conservative reading; the protocol did not define S5 support. | Yes |

The ordering can be checked without relying on this log. The GitHub tag commit and the Zenodo record fix the lock time, the run log fixes the run time, and Section 5 gives the hash of results.json. Anyone can re-run the locked analysis with one command (verification/verify\_lock.py, release v2.1): it checks every file hash, runs the locked code once and compares the output with the published results. My own re-run on a different operating system passed (Entry 31). No independent re-run has been reported yet, and I invite reports through the repository's issue tracker.

**Post-lock checks (Entry 29, after results were seen).** None changes a confirmatory estimate.

| Check | Finding |
| --- | --- |
| Interval coverage and calibration (Entries 29–30): synthetic outcomes on the real credit path, 300 replications per effect size | Nominal 90% intervals cover the true ratio 80–81% of the time for GDP, 74–75% for unemployment and 69–77% for the SPF correction (74–83% in the S6 halves). With no credit effect, the full-sample GDP interval falls wholly below 1 in about 1–2% of replications and the pre-2008Q4 interval in 5%. Widening factors that restore 90% coverage (1.35, 1.75, 2.1) give the calibrated intervals in Table 3b; the locked intervals still govern the pre-registered rule. |
| P1a coefficient paths and largest losses | Credit coefficients sum to a negative number throughout. The 2010–11 losses came from forecasts of a rebound (Table 5, Figure 7). This corrects the earlier draft, which said the model "kept forecasting weakness". |
| P2a training start | Later starts (1993Q1, 1996Q1) give 1.130 and 1.095 against 1.019 for the locked start on 68 common origins. |

**Pandemic-period illustration (Entries 33–35).** I committed the plan and script and tagged them `pandemic-plan` (commit b9a7fc0) at about 08:58 UTC on 20 October 2026, before downloading the March, June and September 2020 Z.1 releases. The releases were hashed on download, parsed with the locked parser and passed the continuity check, and the analysis ran once. The explanatory note in Section 5.6 departs from the plan's pre-written wording and is declared here as a deviation; nothing else in the plan changed.

**Use of AI.** The analysis code, power simulations and drafting were carried out with Claude (Anthropic) under my direction. All design decisions and interpretive choices are mine, and each is recorded in the log.

## Appendix B. Exploratory model specifications

- **S4, Bayesian VAR.** Variant 1A contains real GDP growth, GDP-deflator inflation, the unemployment rate and the two-year Treasury yield, all observed through o − 1. Variant 1B adds the credit impulse lagged two quarters, so credit enters only as published. Both use two lags, estimated from 1976Q3 on the data available at each origin. They share a Minnesota prior: overall tightness 0.2, cross-variable tightness 0.5, lag decay 2; prior mean 1 on the first own lag of unemployment and the yield, and 0 otherwise; scales from AR(4) residual standard deviations. Forecasts are iterated five steps, from o − 1 to o + 4. The comparison uses the Diebold–Mariano statistic with the small-sample correction of Harvey, Leybourne and Newbold (1997), and a block-bootstrap p-value.
- **E1, Markov-switching signal.** A two-regime Markov-switching regression of the quarterly change in unemployment has a switching intercept and variance, with real credit growth at its release lag as a non-switching regressor. It is estimated from 1965Q1 at each origin from 2000Q1. The filtered (never smoothed) probability of the rising-unemployment regime at o − 1 is added to the direct AR(2) for unemployment at o + 4 and scored by Clark–West.
- **R1, ragged-edge fills.** In variant Y, an AR(4) on the four-quarter credit flow, estimated within each Z.1 vintage, fills the quarters between q\* and o − 1. In variant Z, a VAR(2) on household and business flows does the same. Both variants then use calendar lags ending at o − 1.

## Appendix C. Data files

The dated list of Z.1 releases (95 releases from September 1996 to March 2020, including the 83 used here, with archive folders and formats) is in `tables/z1_release_dates.csv`, and the origin–release table in `tables/origin_release_table.csv`. The real-time credit vintages, with the series code used in each vintage, are in `data_derived/credit_vintages_long.csv`. All three are part of the v1.0-lock release.

## Appendix D. Inference and simulation details

**Confirmatory inference (locked code).**

- **Clark–West tests** are one-sided. The variance of the adjusted loss differential uses a Bartlett (Newey–West) kernel with h − 1 = 3 lags.
- **Fixed-b p-values** come from a simulated null: 20,000 draws of the same t-statistic computed on Gaussian white noise of length 2,000, with the bandwidth scaled to the same fraction (lags + 1)/n as the sample (Kiefer and Vogelsang, 2005). The random seed is 20261019 plus a sample-specific offset.
- **RMSE-ratio intervals** are percentile intervals from a moving-block bootstrap of the forecast-error pairs: block length 4, 2,000 draws, seed 20261019.
- **P3** uses a restricted wild (Rademacher) block bootstrap of its HAC t-statistic, with block length 4, 4 HAC lags and 999 draws.
- **Holm's step-down procedure** at the 5% level runs across P1a, P1b, P2a and P3.

All of this is in `phase2.py` (SHA-256 da697030…).

**Post-lock coverage and calibration simulations.**

- **The simulated economy** (`test_phase2.py`, written before lock) has GDP growth and unemployment that follow AR(2) processes with coefficients and shock covariance fitted to revised data. Credit enters as κ times the real, revised credit impulse at lag 6. Data vintages and GDP revisions are simulated around these series, and the SPF is simulated as an AR-information forecast plus noise.
- **The coverage check** (`coverage.py`) uses κ\_g = 0, 0.15 and 0.25, with seeds 7000 + r.
- **The calibration** (`calibrate.py`) uses (κ\_g, κ\_u) = (0, 0) and (0.25, 0.015), with seeds 9100 + r.
- Both use r = 0, …, 299. At κ\_g = 0.25 the true GDP ratio is about 0.97, a gain of about 3%.
- **The true ratio** for each effect size is the square root of the ratio of mean squared errors pooled over replications.
- **Widening factors** were searched on a grid from 1.00 to 3.00 in steps of 0.05. The factor reported is the smallest that reaches 90% coverage at both effect sizes.

The scripts and their outputs are in `post_lock/` in the release.

## Data and code availability

- **Preregistration:** GitHub release [v1.0-lock](https://github.com/AndyMoran/credit-impulse-realtime-prereg/releases/tag/v1.0-lock), commit 4eb084f, archived at DOI [10.5281/zenodo.23477871](https://doi.org/10.5281/zenodo.23477871).
- **Results and figures** are in release [v2.0-results](https://github.com/AndyMoran/credit-impulse-realtime-prereg/releases/tag/v2.0-results) (commit 27fab0b), archived at DOI [10.5281/zenodo.23479717](https://doi.org/10.5281/zenodo.23479717), with a dated log of every post-lock step (DEVIATIONS.md). The post-lock checks of Appendix A (coverage.py, calibrate.py, calibrated\_intervals.py, diagnostics.py, fig7.py and the verification script verify\_lock.py) are in release v2.1 (tag v2.1-verification, commit 2510c83), archived at DOI 10.5281/zenodo.23497087, together with the pandemic-period plan, inputs, hashes and outputs (pandemic/), the verification kit and a journal-style replication README. This version of the paper, v2.2, is in release v2.2 of the same repository.
- **Raw inputs** are public: the Federal Reserve Z.1 archive, the Philadelphia Fed Real-Time Data Set and SPF, and FRED GS2. The exact versions are identified by the SHA-256 hashes in MANIFEST.txt.

## References

*Bibliographic details checked against publisher or RePEc records, 19 October 2026.*

- Adrian, T., Boyarchenko, N. and Giannone, D. (2019). Vulnerable growth. *American Economic Review* 109(4): 1263–1289. [doi:10.1257/aer.20161923](https://www.aeaweb.org/doi/10.1257/aer.20161923)
- Aikman, D., Haldane, A. G. and Nelson, B. D. (2015). Curbing the credit cycle. *Economic Journal* 125(585): 1072–1109.
- Alessi, L. and Detken, C. (2011). Quasi real time early warning indicators for costly asset price boom/bust cycles: a role for global liquidity. *European Journal of Political Economy* 27(3): 520–533.
- Barnichon, R. and Nekarda, C. J. (2012). The ins and outs of forecasting unemployment: using labor force flows to forecast the labor market. *Brookings Papers on Economic Activity* 43(2), Fall 2012: 83–131.
- Biggs, M., Mayer, T. and Pick, A. (2009). Credit and economic recovery. De Nederlandsche Bank Working Paper No. 218. Revised as "Credit and economic recovery: demystifying phoenix miracles" (2010); summary in [VoxEU, 14 May 2010](https://cepr.org/voxeu/columns/myth-phoenix-miracle).
- Clark, T. E. and West, K. D. (2007). Approximately normal tests for equal predictive accuracy in nested models. *Journal of Econometrics* 138(1): 291–311.
- Croushore, D. (2011). Frontiers of real-time data analysis. *Journal of Economic Literature* 49(1): 72–100. doi:10.1257/jel.49.1.72
- Croushore, D. and Stark, T. (2001). A real-time data set for macroeconomists. *Journal of Econometrics* 105(1): 111–130.
- Del Negro, M. and Schorfheide, F. (2013). DSGE model-based forecasting. In G. Elliott and A. Timmermann (eds), *Handbook of Economic Forecasting*, Vol. 2A, 57–140. Amsterdam: Elsevier/North-Holland.
- Drehmann, M., Borio, C., Gambacorta, L., Jiménez, G. and Trucharte, C. (2010). Countercyclical capital buffers: exploring options. BIS Working Papers No. 317.
- Drehmann, M. and Yetman, J. (2018). Why you should use the Hodrick–Prescott filter – at least to generate credit gaps. BIS Working Papers No. 744.
- Edge, R. M. and Gürkaynak, R. S. (2010). How useful are estimated DSGE model forecasts for central bankers? *Brookings Papers on Economic Activity* 41(2): 209–244. doi:10.1353/eca.2010.0015
- Edge, R. M. and Meisenzahl, R. R. (2011). The unreliability of credit-to-GDP ratio gaps in real time: implications for countercyclical capital buffers. *International Journal of Central Banking* 7(4), December; [FEDS 2011-37](https://www.federalreserve.gov/econres/feds/the-unreliability-of-credit-to-gdp-ratio-gaps-in-real-time-implications-for-countercyclical-capital-buffers.htm).
- Federal Reserve Bank of Philadelphia. [Real-Time Data Set for Macroeconomists](https://philadelphiafed.org/research-and-data/real-time-center/real-time-data); [Survey of Professional Forecasters documentation](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/spf-documentation.pdf).
- Gilchrist, S. and Zakrajšek, E. (2012). Credit spreads and business cycle fluctuations. *American Economic Review* 102(4): 1692–1720.
- Harvey, D., Leybourne, S. and Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting* 13(2): 281–291.
- Hansen, B. E. (2000). Testing for structural change in conditional models. *Journal of Econometrics* 97(1): 93–115.
- Jordà, Ò., Schularick, M. and Taylor, A. M. (2013). When credit bites back. *Journal of Money, Credit and Banking* 45(s2): 3–28.
- Keen, S. (2013). A monetary Minsky model of the Great Moderation and the Great Recession. *Journal of Economic Behavior & Organization* 86: 221–235.
- Kiefer, N. M. and Vogelsang, T. J. (2005). A new asymptotic theory for heteroskedasticity-autocorrelation robust tests. *Econometric Theory* 21(6): 1130–1164.
- Koenig, E. F., Dolmas, S. and Piger, J. (2003). The use and abuse of real-time data in economic forecasting. *Review of Economics and Statistics* 85(3): 618–628.
- Loh, W.-Y. (1987). Calibrating confidence coefficients. *Journal of the American Statistical Association* 82(397): 155–162.
- López-Buenache, G., Borsi, M. T. and Rosa-García, A. (2025). Credit cycles as predictors of labor market slack: evidence from the U.S. *Economic Analysis and Policy* 88. [doi:10.1016/j.eap.2025.08.006](https://doi.org/10.1016/j.eap.2025.08.006)
- López-Salido, D., Stein, J. C. and Zakrajšek, E. (2017). Credit-market sentiment and the business cycle. *Quarterly Journal of Economics* 132(3): 1373–1426.
- Mian, A., Sufi, A. and Verner, E. (2017). Household debt and business cycles worldwide. *Quarterly Journal of Economics* 132(4): 1755–1817.
- Repullo, R. and Saurina, J. (2011). The countercyclical capital buffer of Basel III: a critical assessment. CEPR Discussion Paper No. 8304.
- Schularick, M. and Taylor, A. M. (2012). Credit booms gone bust: monetary policy, leverage cycles, and financial crises, 1870–2008. *American Economic Review* 102(2): 1029–1061.
