# Timestral extension: real-time GDP forecasts with Mistral's time-series foundation model

Analysis plan · frozen 29 October 2026 at tag `timestral-plan` · Andy Moran (Heaviside Analytics)

> **Status.** Drafted before Timestral was run on any real series. The author installed the `timestral` package and downloaded the Timestral-209M weights on 29 October 2026 and has run no forecast with them. In script testing, the real inputs were passed only to a stand-in AR(2) and to a small network with Timestral's architecture and random weights; that network is not Timestral, and its outputs mean nothing. No Timestral forecast of any real target has been computed or seen. The plan will be committed and tagged before the first real run, and the tag's timestamp is the evidence of timing.
>
> **What is already known.** The author knows the locked study's results and the TimesFM extension's results (DOI 10.5281/zenodo.23675487): TimesFM 2.5 and 3.0 finished in a dead heat with the AR(2), and credit did not help either. This plan repeats the TimesFM design for a second model, with the lessons from that run, and fixes every choice before any Timestral forecast exists.

## 1. The question, and what the answer can and cannot show

The TimesFM extension asked whether a pretrained foundation model, given only real-time data, forecasts US GDP growth four quarters ahead better than a direct AR(2). Neither TimesFM model did. Timestral, released by Mistral AI on 15 October 2026, is reported by Mistral to lead the three main zero-shot forecasting benchmarks (GIFT-Eval, TIME and fev-bench). This extension asks the same three questions of it:

1. **Does Timestral, used as published and given only real-time data, forecast GDP growth better than the AR(2)?**
2. **Does adding the real-time credit impulse help Timestral?**
3. **Do revised credit data change the answer to question 2?**

What it can show: whether a second model family, with a different architecture and mostly synthetic training data, behaves as TimesFM did on the same 78 origins.

What it cannot show:

- **Clean out-of-sample skill.** Timestral was trained in 2026, partly on real data that Mistral does not list (Section 5). Its weights may carry information from after the forecast dates.
- **Anything general about foundation models.** This is one model, one country, one horizon and one credit cycle.
- **A revised answer to the locked study's question.** The locked headline stands.

## 2. Model, licence and settings

| Item | Value |
| --- | --- |
| Model | Timestral-209M (Mistral AI), the largest of four sizes |
| Weights | `mistralai/Timestral-209M` @ `9874d252ab0aae16f7f7c999f98f98d6ad7d8365`; `model.safetensors` SHA-256 `1456effb9927e3daa8c7234f10497e3424233869245a9c72b8ecebaf7ad2b7fa`; `config.json` `1764139b…`; `LICENSE` `64819472…`; `README.md` `f85a2083…` |
| Package | `timestral` 1.0.0, GitHub `mistralai/timestral` @ `a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff`, installed with `--no-deps` |
| Environment | The TimesFM extension's pinned environment (`timesfm/PLAN_LOCK.json`): torch 2.14.1, numpy 2.4.6, huggingface_hub 2.3.0, safetensors 0.8.0, Python 3.11.17, Linux under WSL2, CPU only |

**Licence.** The package code is under Apache 2.0. The weights are under Mistral's "Modified MIT License", read by the author on 29 October 2026. It permits use, copying, modification, publication and sale, with two conditions: the attribution and permission notice must accompany copies of the model, and no rights may be exercised if the user's company has a global consolidated monthly revenue above $20 million. Neither condition restricts this study: no copy of the weights is distributed (the scripts download them from Hugging Face), and Heaviside Analytics is far below the threshold. Unlike TimesFM 3.0, there is no non-commercial restriction, so the Timestral script is published with the others.

**Use as published.** The model is not fine-tuned, retrained or adapted, and no setting is tuned on the forecast sample. The package's default forecast settings are used, as in Mistral's benchmark runs: symmetric averaging on (the forecast is averaged with the reflected forecast of the negated series) and non-negative clipping on. Clipping applies only to a series whose whole context is non-negative; every GDP context here contains negative quarters, so it never applies. The median (the 0.5 quantile) is scored; the 10th percentile is the 0.1 quantile.

Each origin is forecast in its own call, because the contexts differ in length. The package left-pads each context to a whole number of patches with unobserved values; this code adds no padding.

## 3. Sample and data

As in the TimesFM extension (`timesfm/PLAN.md`, Section 3), with no change:

- **Origins:** the locked study's 78 origins, 1999Q3–2018Q4. **Target:** quarter o + 4; Timestral is asked for 5 steps and only the fifth is scored.
- **GDP input:** annualised quarterly real GDP growth from the origin's RTDSM vintage, 1965Q1 to o − 1. **Outcome:** the 2026Q3 vintage.
- **Credit input:** the real-time credit impulse from the latest Z.1 release before the origin, ending at q\* = o − 2, as **one past-only covariate aligned by Rule B**: position t holds CI(t − 1), so the last position, o − 1, holds CI(q\*). This is the rule used for TimesFM 3.0. Timestral's covariates "never read the targets" (package README), and a past-only covariate covers exactly the context, so no credit value after q\* can enter.
- **Revised credit (question 3):** the same rule applied to the impulse from the September 2026 release, cut at q\*.

Everything comes from the frozen files of the locked releases. Nothing new is downloaded except the model.

## 4. Comparisons and statistics

| Label | Comparison | Question | Status |
| --- | --- | --- | --- |
| **T1** | Timestral, GDP only, against the AR(2) | 1 | **Primary** |
| T2 | Timestral with real-time credit, against Timestral without | 2 | Secondary |
| T3 | T2 with revised credit instead of real-time credit (the premium) | 3 | Secondary |
| T4 | Timestral against TimesFM 3.0, and against TimesFM 2.5, GDP only, using the published TimesFM forecasts (`timesfm/results/forecasts.csv`) | — | Descriptive |

T4 is descriptive because the TimesFM forecasts were seen before this plan was written. It answers a reader's natural question, whether the newer model did better than the older one on the same task, without being a test.

**Statistics,** unchanged from the TimesFM extension and imported from its frozen run script: the RMSE ratio, model ÷ comparator, over the 78 origins; the locked moving-block bootstrap (block 4, 2,000 draws, seed 20261019, 90% percentile intervals); a credible improvement only if the whole interval lies below 1; the Diebold–Mariano statistic with the Harvey–Leybourne–Newbold correction, reported and not interpreted; the premium rule for T3 ("large" if at least 0.05 in absolute value with an interval excluding zero).

**Power.** No new power analysis is run. For T2 and T3, the locked study's simulations imply that only RMSE reductions of roughly 40% could be reliably detected on this credit path; that limit is stated beside them. For T1 and T4 the power is unknown, and that is stated too.

## 5. Leakage checks

**L0. Training data (before freezing).** Mistral states that most of Timestral's training data were synthetic: the first training stage used synthetic data only, and the second mixed real and synthetic data. Mistral does not list the real datasets, and makes no statement about excluding benchmark test sets or economic series.

**L0 result (29 October 2026): Uncertain.** The author read the model card at the pinned revision (README.md, SHA-256 `f85a2083…`). It describes the architecture, inputs, outputs and benchmark scores but has no training-data section, and says a technical report is "coming soon". Mistral's announcement says only that most training data were synthetic and that the second stage mixed in real data. The real data cannot be checked, so under the TimesFM plan's rule the rating is **Uncertain**. It is not High: there is no evidence that US GDP, unemployment or credit series were used. It is not Low: they cannot be ruled out. If Mistral's technical report appears before the run and lists the training data, the rating is re-checked against that list and any change is logged before the run.

**L1. Perturbation test** and **L2. Shape-matched placebo:** exactly as in the TimesFM extension (`timesfm/PLAN.md`, Section 5), with the same seeds, the same revision-sized noise (1.405 percentage points), the same 50 placebos and the same flags: L1 is flagged if Timestral's degradation ratio exceeds the AR(2)'s by more than 0.10 over all 78 origins or by more than 0.20 over 2010Q1–2011Q4; L2 is flagged if the real-series ratio lies below the 10th percentile of the placebo ratios. The AR(2)'s L1 values are already known (0.995 and 0.984); Timestral's are not.

**What the checks cannot do.** None proves or rules out leakage. They make memory of the specific US series more or less plausible, and are reported as doing only that.

**Training exposure need not help.** The TimesFM note called a null "a generous test", on the assumption that seeing later data can only help a model. It need not: Timestral's training data, where real, are presumably revised series, while the model is given real-time vintages, so memory of revised data could pull its forecasts away from the real-time outcome as easily as towards it. The wording in Section 7 makes no assumption about the direction.

## 6. What will be reported

Whatever it shows:

1. **The results table:** T1–T4, each with the RMSE ratio, its 90% interval, the credible-improvement verdict (T1–T3) and the DM-HLN p-value.
2. **The 2010–12 forecasts:** for each origin from 2010Q1 to 2011Q4, the outcome and the forecasts of the AR(2), the locked credit model, Timestral, Timestral with credit, TimesFM 2.5 and TimesFM 3.0.
3. **The lower tail, descriptive only:** the 10th-percentile quantile loss and how often the outcome fell below the 10th percentile, over all 78 origins and over 2008Q1–2012Q4 targets, for Timestral, Timestral with credit and the AR(2).
4. **The leakage checks:** the L0 rating and its evidence, the L1 ratios, excesses and per-draw ratios, and the L2 real-series ratio with its placebo distribution.
5. **The run record:** the gate results, checkpoint and package versions, and the hashes of all inputs and outputs.

## 7. How results will be worded

"Leakage concern" means an L0 rating of High, or an L1 or L2 flag. An Uncertain rating is not by itself a concern, but it is never covered by "no sign".

| Result | Leakage evidence | Sentence |
| --- | --- | --- |
| No credible improvement | Any | "Given only real-time data, Timestral did not forecast [GDP growth / better with credit] credibly better than [comparator] (ratio r; 90% interval a–b). Its training data may include the forecast period; that could have helped or hurt it (Section 5), so this result does not show how a model without that exposure would fare." |
| Credible improvement | L0 Low; no L1 or L2 flag | "Given only real-time data, Timestral forecast credibly better than [comparator] (ratio r; 90% interval a–b), and the leakage checks give no sign that this reflects memory of the US series. One model and one credit cycle cannot establish that the gain would recur." |
| Credible improvement | L0 Uncertain; no L1 or L2 flag | "Given only real-time data, Timestral forecast credibly better than [comparator] (ratio r; 90% interval a–b). The perturbation and placebo checks raised no flag, but the training-data check was Uncertain because Mistral does not list the real data used in training, so memory of US series cannot be ruled out. One model and one credit cycle cannot establish that the gain would recur." |
| Credible improvement | Leakage concern | "Timestral forecast credibly better than [comparator] (ratio r; 90% interval a–b), but the leakage checks [state which] mean the gain may reflect data the model saw in training. It is not evidence of real-time skill." |
| T4 (descriptive) | — | "On the same 78 origins, Timestral's forecasts were [more accurate than / less accurate than / about as accurate as] TimesFM [3.0 / 2.5]'s (ratio r; 90% interval a–b). This comparison is descriptive: the TimesFM forecasts were seen before this plan was written." |

**T4 wording rule:** "more accurate" if the whole interval lies below 1; "less accurate" if it lies wholly above 1; "about as accurate as" if it contains 1.

Every sentence is followed by the interval note: "These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured."

For T3, the wording follows the premium rule (Section 4).

**Placement.** The results go in a short note, "A second foundation model", released alongside the TimesFM note. The working paper and the TimesFM note do not change.

## 8. Validity gate and procedure

**Validity gate.** The official run is the first run whose outputs pass every check below. A run that fails is a failed attempt: its outputs are kept, it is logged as a deviation, the cause is fixed, and the run is repeated. Results from a failed attempt are not reported as results. (The TimesFM extension used a single-run rule, and its first run had to be declared a deviation after a slicing bug; a gate catches such faults before a run counts.)

1. The locked AR(2) and credit-model forecasts are reproduced exactly at all 78 origins, and the frozen scripts match their hashes in the lock file.
2. The credit covariate follows Rule B at every origin, for real-time and revised credit.
3. Every Timestral forecast is finite, has exactly 5 steps and 9 deciles, and its median equals its 0.5 quantile.
4. Forecasting the first and last origins again gives identical results.
5. Moving the last GDP value moves the forecast.
6. The weights file and the TimesFM forecasts file match the hashes in the lock file.

**Procedure.**

1. **Agree this plan.** The author settles any change; after step 4 it is frozen.
2. **Self-test** (`tsl_selftest.py`), with the real weights on synthetic series only: shapes, negative forecasts allowed, repeatability, the covariate route, and two behavioural controls. In the positive control, the target is driven by last quarter's covariate, and adding the covariate must cut the one-step error by at least 20% over 40 series: this shows Timestral can use a past-only covariate at all, so that a null for T2 is not a plumbing failure. In the negative control, an unrelated covariate must change the error by less than 10%. Then the pipeline test (`run_timestral.py pipeline-test`) on the real inputs with the stand-in AR(2).
3. **L0.** Read the model card and record the rating in Section 5.
4. **Freeze.** Commit the plan and scripts, tag `timestral-plan`, and write `timestral/PLAN_LOCK.json` with the tag, the hashes of the plan, the scripts, the weights and the TimesFM forecasts file.
5. **Run until one attempt passes the gate** (`run_timestral.py real`).
6. **Report** using only the Section 7 sentences, with a declared-deviation section.

## 9. What counts as a deviation

After the tag: a change to the origins, horizon, inputs, alignment rule, settings, checkpoint, package version or gate; fine-tuning or tuning on the forecast sample; a second passing run; a comparison, model or statistic not listed here reported as anything but exploratory; wording other than Section 7's; an unreported listed output. Each is logged with its date and whether results had been seen.

## 10. Decisions taken before freezing

All six were agreed by the author on 29 October 2026, as recommended.

| # | Decision | Recommendation |
| --- | --- | --- |
| 1 | Model size | Timestral-209M only, the size Mistral compares with TimesFM; adding sizes multiplies comparisons for little gain |
| 2 | Forecast settings | The package defaults, as in Mistral's benchmarks. This differs from TimesFM 3.0, run with symmetric averaging off; the difference is stated in the note |
| 3 | T4, the descriptive comparison with TimesFM | Include, labelled descriptive |
| 4 | Validity gate instead of a single-run rule | Adopt (Section 8) |
| 5 | Null wording | The conditional sentence in Section 7, replacing the TimesFM note's "generous test" |
| 6 | L0 rating | Uncertain: the model card lists no training data (Section 5) |

## 11. Pre-freeze check results

| Check | Date | Result |
| --- | --- | --- |
| Install and download | 29 Oct 2026 | `timestral` 1.0.0 at commit a534bdbd installed with `--no-deps`; Timestral-209M revision and file hashes as in Section 2; torch 2.14.1, numpy 2.4.6 unchanged |
| L0 | 29 Oct 2026 | Uncertain (Section 5) |
| Self-test, Part A (real inputs, no model) | 29 Oct 2026 | Locked AR(2) and credit-model forecasts reproduced at all 78 origins; Rule B holds for real-time and revised credit at every origin; worked example matches (2010Q1: CI(2009Q3) = −10.356) |
| Self-test, Part B (real weights, synthetic series only) | 29 Oct 2026 | All pass. Five steps and nine deciles; negative forecasts allowed (step-1 median −2.94 for a series centred at −3); repeat call identical; covariate route runs. **Positive control:** a driving covariate cut Timestral's one-step error by 31% (ratio 0.690), so Timestral can use a past-only covariate. **Negative control:** an unrelated covariate changed it by 1% (ratio 1.010) |
| Pipeline test (real inputs, stand-in AR(2), no Timestral) | 29 Oct 2026 | Gates 1–5 pass. Gate 6 (weights and TimesFM file hashes) and the frozen-script part of gate 1 run only in the real run |

