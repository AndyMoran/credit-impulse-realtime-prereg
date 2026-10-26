# TimesFM extension: real-time GDP forecasts with a time-series foundation model

Analysis plan · draft for agreement · 26 October 2026 · Andy Moran (Heaviside Analytics)

> **Status.** This plan was drafted before TimesFM was installed. Since then, TimesFM has been installed and run only on synthetic series (and, in one plumbing test, with random weights), to test the scripts (Section 8, step 2). No real US series has been passed to either TimesFM model, and no TimesFM forecast of any real target has been computed or seen. The plan will be committed to the public repository and tagged before the first run, and that tag's timestamp, not this document, is the evidence of timing. The extension is preregistered in its own right, but it is not part of the original confirmatory family. It cannot change the locked study's headline, and everything listed in Section 6 is reported whatever it shows.
>
> **What is already known.** The author knows the locked study's results: the AR(2) and credit-model forecasts, their errors, and the outcomes for every target. No TimesFM forecast for any target has been computed or seen. This plan fixes every choice about those forecasts before they exist.

## 1. The question, and what the answer can and cannot show

The locked study found that adding the real-time credit impulse to a direct AR(2) did not improve four-quarter-ahead forecasts of US GDP growth over 1999–2019. Its largest losses came in 2010–11, when the model read the collapse in borrowing as a sign of a sharp rebound.

This extension asks three narrower questions:

1. **Does a pretrained foundation model, used as published and given only real-time data, forecast GDP growth better than the AR(2)?**
2. **Does adding the real-time credit impulse help the foundation model, where it did not help the linear model?**
3. **Do revised credit data change the answer to question 2?**

What it can show:

- how an off-the-shelf foundation model behaves through the 2008–12 episode when given only what was published at each origin;
- whether TimesFM 3.0, which takes credit natively and can in principle use it non-linearly, forecasts the 2011–12 recovery differently (F3; F4 cannot show this, see Section 4).

What it cannot show:

- **Clean out-of-sample skill.** TimesFM was trained in 2024–26, on data that may include series shaped by the 2008–12 episode. Its weights may carry hindsight that no real-time forecaster had. Section 5 sets out the checks, and Section 7 fixes how each result will be read in light of them.
- **Anything general about foundation models.** This is one model family, one country, one horizon and one credit cycle.
- **A revised answer to the locked study's question.** The locked headline stands.

## 2. Models and licences

| Model | Weights licence | Role | Credit input |
| --- | --- | --- | --- |
| TimesFM 2.5 (200M) | Apache-2.0 | Main analysis. Code and results fully public. | Through the XReg add-on, as four lags known at the origin (see below) |
| TimesFM 3.0 (330M) | TimesFM Non-Commercial License v1.0 | Research-only comparison | Native past-only covariate |

**Checkpoints.** Each model is loaded from the exact revision below, downloaded by the author on 26 October 2026. The run script checks the SHA-256 of each weights file before the first forecast.

| Model | Hugging Face repository and revision | Weights file SHA-256 |
| --- | --- | --- |
| TimesFM 2.5 | `google/timesfm-2.5-200m-pytorch` @ `1d952420fba87f3c6dee4f240de0f1a0fbc790e3` | `2f776efe6245e42b24bc4153ffdf61810140210e4bd3b01fb21f7aa779ab6ce8` (925,181,104 bytes) |
| TimesFM 3.0 | `google/timesfm-3.0-pytorch` @ `43046b85ec22d584a13f8098c2ed39c889e129c2` | `a7592b0a8432baee54483254e5647856911ce69e09d09a9bb65904b2d98f17da` (1,322,898,824 bytes) |

Packages: `timesfm` 3.0.2, `torch` 2.14.1, `jax` and `jaxlib` 0.10.2, `scikit-learn` 1.9.1, `numpy` 2.4.6, `huggingface_hub` 2.3.0, `safetensors` 0.8.0, on Python 3.11.17 (Linux under WSL2, CPU only).

**Use as published.** Neither model is fine-tuned, retrained or adapted, and no setting is tuned on the forecast sample. The package is `timesfm` 3.0.2 from PyPI, which contains both models. The settings are fixed in the scripts:

- **TimesFM 2.5:** maximum context 256 quarters, maximum horizon 128 (5 steps requested), input normalisation on, continuous quantile head on, flip invariance on, positivity off (GDP growth can be negative), quantile-crossing fix on.
- **TimesFM 3.0:** symmetric averaging off, positivity clamp off, quantiles sorted, no extra z-normalisation, no padding.

The point forecast is the median (0.5 quantile); the 10th percentile is the 0.1 quantile.

**Credit in TimesFM 2.5.** TimesFM 2.5's XReg add-on needs covariate values over the forecast horizon as well as the history. Script testing confirmed this from the package code and in a test with random weights: covariates of context length only are refused. Credit values for the horizon are not known at the origin, so credit cannot enter as a contemporaneous series.

Instead, credit enters TimesFM 2.5 as **four lagged covariates**, the regressors of the locked credit model, and TimesFM 3.0 takes it as **one shifted past-only series**. The two models therefore use different alignment rules, set out in Section 3. XReg runs in the package's default mode, "xreg + timesfm": the linear credit fit first, then TimesFM on the residuals.

**Licence handling for TimesFM 3.0.** The author read the licence on 26 October 2026. Two clauses govern this study:

- **Non-Commercial Purpose** includes "academic research, and experimentation on private or public datasets, provided the results are not used in commercial decision-making, client deliverables, or paid products/services".
- **Derivative** includes any "work that incorporates, utilizes, or is otherwise based on" the model, and Derivatives may not be distributed. Outputs (forecasts) are expressly not Derivatives.

So:

- TimesFM 3.0's forecasts and summary results are published.
- The TimesFM 3.0-specific script is not placed in the public MIT-licensed repository unless Google confirms in writing that doing so is permitted. The settings are described in prose (Section 10, decision 7).
- No TimesFM 3.0 output is used in client work, paid products or commercial decisions.
- No weights are committed to the repository.

## 3. Sample and data

All data come from the frozen files of the locked release (`v1.0-lock`) and the results release (`v2.0-results`), identified by the hashes in their manifests. Nothing new is downloaded except the model checkpoints.

**Origins.** The same 78 origins as the locked study, 1999Q3–2018Q4.

**Target and horizon.** The target is quarter o + 4, as in the locked study. GDP is observed through o − 1, so each forecast is the fifth step ahead of the last observation: the model is asked for 5 steps, and only the fifth is scored.

**GDP input.** At origin o, annualised quarterly real GDP growth (discretely compounded, as in the locked study) from the origin's RTDSM vintage, from 1965Q1 to o − 1. This is the same window the AR(2) is estimated on. The outcome is taken from the 2026Q3 vintage, as in the main study.

**Credit input.** The real-time credit impulse from the latest Z.1 release before the origin, ending at q\* = o − 2. The release lag k = o − q\* is 2 at every origin. Write CI(s) for the impulse in quarter s.

The two models take credit in different forms, so each has its own alignment rule.

**Rule A: TimesFM 2.5, XReg (F4).** Four covariate columns, j = 0, 1, 2, 3. At every position t, in the history and over the five forecast steps:

> column j at position t = CI(t − 4 − k − j) = CI(t − 6 − j).

At the fifth step, t = o + 4, column j holds CI(q\* − j): exactly the four credit regressors the locked credit model uses at origin o. At each history position t, the columns hold the regressors of the locked model's training row whose target is t. So the XReg linear fit pairs GDP with the same credit values as the locked direct regression. The latest credit value used anywhere is CI(q\*), at the fifth step.

**Rule B: TimesFM 3.0, past-only covariate (F3).** One series, the same length as the GDP context:

> covariate at position t = CI(t − (k − 1)) = CI(t − 1).

The last position, o − 1, holds CI(q\*). The covariate ends where GDP ends, and no credit value appears before it was published. Rule B gives TimesFM 3.0 the credit series itself and leaves the lag structure to the model; it does not reproduce the locked regressors.

**Worked example, origin 2010Q1** (GDP to 2009Q4, q\* = 2009Q3, target 2011Q1). Values are the real-time impulse in percentage points, printed by the self-test.

| Position | t | Column 0 | Column 1 | Column 2 | Column 3 |
| --- | --- | --- | --- | --- | --- |
| Last GDP observation | 2009Q4 | CI(2008Q2) = −3.024 | CI(2008Q1) = −0.336 | CI(2007Q4) = +0.353 | CI(2007Q3) = +0.345 |
| Step 1 | 2010Q1 | CI(2008Q3) = −6.803 | CI(2008Q2) = −3.024 | CI(2008Q1) = −0.336 | CI(2007Q4) = +0.353 |
| Step 2 | 2010Q2 | CI(2008Q4) = −10.565 | CI(2008Q3) = −6.803 | CI(2008Q2) = −3.024 | CI(2008Q1) = −0.336 |
| Step 3 | 2010Q3 | CI(2009Q1) = −11.823 | CI(2008Q4) = −10.565 | CI(2008Q3) = −6.803 | CI(2008Q2) = −3.024 |
| Step 4 | 2010Q4 | CI(2009Q2) = −11.301 | CI(2009Q1) = −11.823 | CI(2008Q4) = −10.565 | CI(2008Q3) = −6.803 |
| **Step 5 (target)** | **2011Q1** | **CI(2009Q3) = −10.356** | **CI(2009Q2) = −11.301** | **CI(2009Q1) = −11.823** | **CI(2008Q4) = −10.565** |

The step-5 row is CI(q\*), CI(q\* − 1), CI(q\* − 2), CI(q\* − 3): the locked credit model's regressors at this origin. Under Rule B, TimesFM 3.0's covariate at the last position, 2009Q4, is CI(2009Q3) = −10.356.

**Alignment self-test.** Publication-timing checks alone would not catch a covariate shifted by the wrong number of quarters, so the self-test compares values directly with the locked code, for real-time and revised credit separately:

- Rule A, fifth step: equal to the locked credit regressors at all 78 origins;
- Rule A, history: equal to the locked training-row regressors at every position and origin (13,767 pairs);
- Rule B: position t holds CI(t − 1) and the last value is CI(q\*), at all 78 origins.

All passed on 26 October 2026 (`tfm_selftest_A.txt`).

**Revised credit (question 3).** The same two rules are applied to the impulse from the September 2026 release, cut at q\* as in the locked study's grid.

**Not used.** Unemployment (P1b), the SPF comparisons (P2a, P2b) and the revision test (P3) are not extended. The extension stays on GDP, where the locked study's turning-point failure occurred. The SPF test corrects a survey forecast, which has no TimesFM analogue, and P3 is not a forecasting comparison.

## 4. Comparisons and statistics

All comparisons are reported as estimates with intervals, in the locked study's "estimate only" style. No significance language is used.

| Label | Comparison | Question |
| --- | --- | --- |
| F1 | TimesFM 2.5, GDP only, against the AR(2) | 1 |
| F2 | TimesFM 3.0, GDP only, against the AR(2) | 1 |
| F3 | TimesFM 3.0 with real-time credit, against TimesFM 3.0 without | 2 |
| F4 | TimesFM 2.5 with real-time credit (XReg, lagged), against TimesFM 2.5 without | 2 |
| F5 | F3 and F4 with revised credit instead of real-time credit (the premium) | 3 |

**F4 is not a test of non-linear credit use.** In "xreg + timesfm" mode, the package fits a linear regression of GDP on the four credit columns first, and TimesFM then forecasts the residuals. Any credit effect in F4 therefore passes through a linear fit, much like the locked credit model's. F4 asks whether TimesFM handles the GDP dynamics around that linear credit term better; it says nothing about whether a foundation model can use credit non-linearly. Only F3, where TimesFM 3.0 takes credit natively, bears on that question, and the note will say so.

**Point forecasts.** TimesFM's median forecast (the 50th percentile) is scored.

**Main statistic.** The RMSE ratio, model ÷ comparator, over the 78 origins. Below 1 means the model in the first position forecast better.

**Intervals.** The locked bootstrap: a moving-block bootstrap of the forecast-error pairs, block length 4, 2,000 draws, seed 20261019, percentile 90% intervals. The locked study showed that these intervals undercover on this credit path (Section 5.1 of the paper). Every reported interval carries that note. No new calibration is run.

**Credible improvement.** As in the locked study: claimed only if the whole 90% interval lies below 1.

**Test statistic, for completeness.** The comparisons are not nested in the linear sense, so the Diebold–Mariano statistic with the Harvey–Leybourne–Newbold correction is reported, with a block-bootstrap p-value, as for the locked BVAR comparison. It is reported, not interpreted.

**Power.** No new power analysis is run. The locked study showed that, on this credit path, only gains of roughly 40% or more could be reliably detected in the credit comparisons. That limit is stated beside F3–F5. For F1 and F2, the power is unknown, and that is stated too.

## 5. Leakage checks

The checks come in two parts. L0 is done **before the plan is frozen**. L1 and L2 are run with the main analysis, under the same single-run rule.

**L0. Training-data check (before freezing).** The model cards list the training sources. For TimesFM 3.0 these are GiftEvalPretrain (excluding datasets that overlap with fev-bench), Wikipedia page views to November 2023, Google Trends top queries to the end of 2022, and synthetic data. The author will check the GiftEvalPretrain dataset list for US macroeconomic series:

- US GDP or its components;
- the unemployment rate;
- household, business or total credit;
- collections known to contain them, such as FRED-MD, FRED-QD and the M4 macroeconomic subsets.

The same check is done for TimesFM 2.5's sources. The finding is recorded in the audit log with the date and the list consulted, and it sets the leakage rating used in Section 7:

- **High:** US GDP, unemployment or credit series appear in the training data.
- **Uncertain:** the training data cannot be checked fully, or contain related US macroeconomic series.
- **Low:** no US macroeconomic series appear.

**L0 result (26 October 2026).** Both model cards list GiftEvalPretrain as a training source; TimesFM 3.0's card adds "excluding the datasets that overlap with fev-bench". The author listed GiftEvalPretrain's 152 top-level datasets from Hugging Face. They include:

- **`fred_md`**, the FRED-MD monthly database of US macroeconomic series (107 series, differenced and log-transformed, in the Monash repository version). FRED-MD includes the US unemployment rate and several US credit series, and spans the 2008–12 episode. It does not include GDP, which is quarterly.
- **M1 and M3 macroeconomic and other series** (`m1_quarterly`, `monash_m3_quarterly` and others), whose countries are not identified;
- **`tourism_*`** and **`cif_2016_*`**, which are not US macroeconomic series.

So:

- **TimesFM 2.5: High.** US unemployment and credit series are in its training data.
- **TimesFM 3.0: Uncertain.** The author listed fev-bench's datasets (`autogluon/fev_datasets`, 26 October 2026). They include `fred_md_2025` and `fred_qd_2025`, later vintages of the FRED-MD and FRED-QD databases. So `fred_md` overlaps fev-bench and, on the model card's description, was excluded from TimesFM 3.0's training. The rating is Uncertain rather than Low for three reasons: Google does not publish the exact list of excluded datasets or how "overlap" was judged; the M1 and M3 series kept in training may include US data; and the synthetic and augmented data cannot be checked.

**What the High rating means.** Under Section 7, any credible improvement by a High-rated model is reported as possibly reflecting data seen in training, not as evidence of real-time skill. Only a null result, or a gain that survives L1 and L2 for a model rated Uncertain or Low, is informative about real-time skill. This was fixed before any TimesFM forecast of real data was made.

**L1. Perturbation test.** The GDP history fed to TimesFM 2.5 and 3.0 is perturbed by adding Gaussian noise, one independent draw per calendar quarter, so that the same quarter gets the same perturbation at every origin. The noise standard deviation is the standard deviation of GDP growth revisions in the locked data, from the early estimate (the vintage two quarters after the target) to the 2026Q3 vintage, over the target quarters 2000Q3–2019Q4: 1.405 percentage points. This is done 20 times, with seeds 20261019 + k for k = 1, …, 20. The same perturbations are applied to the AR(2).

The statistic is the ratio of the mean perturbed RMSE to the unperturbed RMSE, for TimesFM and for the AR(2), over the 78 origins and separately over the eight origins 2010Q1–2011Q4.

- A model that has learned general patterns should degrade about as much as the AR(2).
- A model relying on the exact US sequence should degrade more, especially in 2010–11.

L1 is run on the GDP-only forecasts of each TimesFM model. In each draw, TimesFM and the AR(2) receive the same perturbed history. For model m and window W, the **degradation ratio** is

> R(m, W) = [mean over the 20 draws of the perturbed RMSE of m over W] ÷ [the unperturbed RMSE of m over W].

The **excess** is E(W) = R(TimesFM, W) − R(AR(2), W). **The L1 flag is set if E(all 78 origins) > 0.10 OR E(2010Q1–2011Q4) > 0.20.** Either condition alone sets it.

The thresholds are differences in the degradation ratio, measured in ratio points: 0.10 means TimesFM's ratio is 0.10 higher than the AR(2)'s, for example 1.12 against 1.02. They are not a 10% relative difference. The 2010–11 margin is wider because it rests on eight origins, where one bad quarter can move the ratio a lot.

For each model and window the note reports both degradation ratios, the excess, and the 20 per-draw ratios, flagged or not.

**What was known before freezing.** The thresholds were written into the run script before the pipeline test. That test runs L1 on the real inputs, with the stand-in AR(2) in place of TimesFM, so it computed the AR(2)'s own L1 values: R(AR(2)) = 0.995 over all 78 origins and 0.984 over 2010Q1–2011Q4 (logged in Entry 65). The AR(2) part of L1 is therefore known before the run. The TimesFM part is not. The note will say so.

**L2. Shape-matched placebo.** Fifty synthetic GDP histories are built (seeds 20261100 + k for k = 1, …, 50). For each:

- quarters from 1965Q1 to 2007Q4 are simulated from an AR(2) with Gaussian shocks, fitted to 1965Q1–2007Q4 in the 2026Q3 vintage;
- 2008Q1–2012Q4 copies the actual path in the 2026Q3 vintage, scaled by a factor drawn uniformly from 0.8 to 1.2, with independent noise of revision size (1.405 pp) added.

The last target is 2012Q4, so nothing after it is needed.

TimesFM 2.5, TimesFM 3.0 and the AR(2) forecast each synthetic history at the eight origins 2010Q1–2011Q4, using the same horizon rule. The statistic is TimesFM's RMSE over those eight targets divided by the direct AR(2)'s RMSE on the same series. It is computed for the real series (the 2026Q3 vintage, unscaled and without noise) and for each of the 50 placebos.

- If TimesFM does markedly better on the real series than on the placebos, that is consistent with memory of the real series.
- If it does about as well, its behaviour does not depend on the exact real sequence.

The flag is set if the real-series ratio lies below the 10th percentile of the placebo ratios. The flag is not reported alone: the note gives the real-series ratio, its percentile in the placebo distribution, and the 10th percentile and median of the 50 placebo ratios, with the full set in `results.json`.

**What the checks cannot do.** None of them proves or rules out leakage. A model can learn what recessions look like from many other series, which is legitimate skill and would pass L1 and L2. The checks can make memory of the specific US series more or less plausible. That is all they are reported as doing.

## 6. What will be reported

All of the following will be reported, whatever they show:

1. **The results table:** F1–F5, each with the RMSE ratio, its 90% interval, the credible-improvement verdict and the DM-HLN p-value.
2. **The 2010–12 forecasts:** for each origin from 2010Q1 to 2011Q4, the outcome and the forecasts from the AR(2), the locked credit model, TimesFM 2.5, TimesFM 3.0, and TimesFM 3.0 with credit.
3. **The lower tail, descriptive only:** the 10th-percentile quantile loss of TimesFM's forecasts, and how often the outcome fell below TimesFM's 10th percentile, over all 78 origins and over 2008Q1–2012Q4 targets. For comparison, the AR(2)'s 10th percentile is taken from the empirical quantile of its training residuals at each origin.
4. **The leakage checks:** the L0 rating and the evidence for it, the L1 degradation ratios, excesses and per-draw ratios, and the L2 real-series ratio with its percentile in the placebo distribution.
5. **The run record:** checkpoints, package versions, licence handling and the hashes of all inputs and outputs.

## 7. How results will be worded

The headline sentence for questions 1 and 2 is chosen by the credible-improvement verdict and the leakage evidence. "Leakage concern" means an L0 rating of High, or an L1 or L2 flag. An L0 rating of Uncertain is not by itself a leakage concern, but it is never covered by "no sign": it gets its own row and caveat.

| Result | Leakage evidence | Sentence |
| --- | --- | --- |
| No credible improvement | Any | "Given only real-time data, [model] did not forecast [GDP growth / better with credit] credibly better than [comparator] (ratio r; 90% interval a–b). Because the model may have seen data from after the forecast dates, this is, if anything, a generous test, and it still found no credible gain." |
| Credible improvement | L0 Low; no L1 or L2 flag | "Given only real-time data, [model] forecast credibly better than [comparator] (ratio r; 90% interval a–b), and the leakage checks give no sign that this reflects memory of the US series. One model and one credit cycle cannot establish that the gain would recur." |
| Credible improvement | L0 Uncertain; no L1 or L2 flag | "Given only real-time data, [model] forecast credibly better than [comparator] (ratio r; 90% interval a–b). The perturbation and placebo checks raised no flag, but the training-data check was Uncertain because [reason from Section 5], so memory of US series cannot be ruled out. One model and one credit cycle cannot establish that the gain would recur." |
| Credible improvement | Leakage concern (L0 High, or an L1 or L2 flag) | "[Model] forecast credibly better than [comparator] (ratio r; 90% interval a–b), but the leakage checks [state which] mean the gain may reflect data the model saw in training. It is not evidence of real-time skill." |

For F4, every sentence adds: "F4 runs credit through a linear fit, so it does not show whether the model uses credit non-linearly."

Every sentence is followed by the interval note: "These intervals are known to undercover on this credit path; see Section 5.1 of the paper."

For question 3, the wording follows the locked study's premium rule. The premium is the RMSE ratio with real-time credit minus the ratio with revised credit, both against the same model without credit, so a positive premium means revised credit forecasts better. A premium of 0.05 or more in absolute value, with a 90% interval excluding zero, is "large"; anything else is "small".

**Placement.** The results go in a separate short note, "A foundation-model extension", released alongside the working paper. They are not added to the v2.2 paper, whose abstract, headline and interpretive map do not change.

## 8. Procedure, in order

1. **Agree this plan.** The author reads it and settles any change. After step 4, it is frozen.
2. **Write and test the scripts.** The scripts are `tfm_data.py`, `tfm_models.py`, `tfm_selftest.py` and `run_timesfm.py` (public), and `tfm30_private.py` (not published). The checks are:
   - Part A, on the real inputs with no model loaded: the locked AR(2) and credit-model forecasts are reproduced exactly at all 78 origins, neither credit input ever uses a value published after the origin, and both credit inputs match the alignment rules value by value (Section 3);
   - Part B, on synthetic data only, with the downloaded weights: each model returns 5-step medians and 9 quantiles, the median equals the 0.5 quantile, negative forecasts are allowed, a repeat run gives identical forecasts, and both credit routes run;
   - a full pipeline test on the real inputs with a stand-in AR(2) in place of TimesFM.

   No real US series may be passed to TimesFM in this step.
3. **Do L0.** Check the training-data lists and record the leakage rating.
4. **Freeze the plan publicly.** Commit this plan and the four public scripts to the repository, tag the commit `timesfm-plan`, and record the commit hash, the tag time and the SHA-256 of the plan, all five scripts and both checkpoints in the audit log. The TimesFM 3.0 script's hash is recorded, but the script itself is not published (Section 2).
5. **Run once.** Run the main analysis and L1–L2 once, and save all outputs and logs with their hashes.
6. **Report.** Write the note using only the wording in Section 7, and log the run as an audit entry stating that results were seen.

If a step fails for a mechanical reason, such as a changed function name or array shape in the TimesFM package, only the mapping is fixed, and the fix is logged before the run. No model, sample, statistic or wording choice is reopened.

## 9. What counts as a deviation

Any of the following after step 4 is a deviation. It must be logged with its date and a statement of whether results had been seen, and reported in the note:

- a change to the origins, horizon, targets, inputs or alignment rule;
- fine-tuning, retraining or tuning any setting of either model on the forecast sample;
- a different checkpoint or package version from those recorded;
- running the analysis more than once;
- adding a model, comparison, target or statistic not listed in Sections 4–6;
- wording other than the pre-written sentences;
- leaving any listed output unreported.

If the extension raises a question worth testing, for example whether a foundation model sharpens downside-risk forecasts, it goes into a new plan, written before the data are examined.

## 10. Decisions taken before freezing

1. **Unemployment** is dropped. The extension covers GDP only.
2. **TimesFM 3.0** is included under the licence handling in Section 2, alongside TimesFM 2.5.
3. **L2 settings** are kept as written: 50 placebos, a scale range of 0.8–1.2, and a flag at the 10th percentile of the placebo distribution.
4. **Status statement.** To be confirmed by the author at freezing, as worded at the top of this plan: TimesFM has been installed and run only on synthetic series and random weights; no real US series has been passed to it; no TimesFM forecast of a real target has been computed or seen.
5. **Reviewer fixes (26 October 2026).** Separate alignment rules for the two models, with a worked example and a value-by-value self-test (Section 3); a numerical L1 flag (Section 5); a separate wording row for an Uncertain L0 rating (Section 7); F4 stated not to test non-linear credit use (Section 4); the L2 placebo distribution reported, not only the flag.
6. **L1 thresholds.** 0.10 over all origins and 0.20 over 2010Q1–2011Q4, either one setting the flag, accepted by the author on 26 October 2026. Fixed, not to be reopened. The AR(2) values computed by the pipeline test before freezing are disclosed in Section 5.
7. **TimesFM 3.0 method description.** The note describes the TimesFM 3.0 settings in prose, as listed in Section 2, but publishes no code that calls the model. Describing settings is not distributing a work that "utilizes" the model, so written confirmation from Google is not sought. If Google objects, the description is reduced and the change is logged.
