# A second foundation model: Timestral and real-time US GDP

Results note · 29 October 2026 · Andy Moran (Heaviside Analytics)

A preregistered extension to the TimesFM note (DOI [10.5281/zenodo.23675487](https://doi.org/10.5281/zenodo.23675487)) and the working paper (DOI [10.5281/zenodo.23560860](https://doi.org/10.5281/zenodo.23560860)). Plan: `timestral/PLAN.md`, frozen at tag `timestral-plan` (29 October 2026, 20:55:37 UTC) and locked in `timestral/PLAN_LOCK.json`.

**Result.** Given only real-time data, Mistral's Timestral-209M did not forecast US GDP growth four quarters ahead credibly better than a direct AR(2) over 78 origins, 1999Q3–2018Q4 (ratio 1.018; 90% interval 0.960–1.093). Adding the real-time credit impulse did not help, and the revised-credit premium was small. On the same origins, Timestral's forecasts were about as accurate as both TimesFM models'.

## The run

Official run: attempt 1, 29 October 2026, 21:02:02–21:08:42 UTC, on the author's machine. All six gates passed (`timestral/PLAN.md`, Section 8): the locked AR(2) and credit-model forecasts were reproduced exactly and the scripts matched the lock; the credit covariate followed Rule B at every origin; every forecast had five steps and nine deciles; forecasts were repeatable and responsive; the weights and the TimesFM forecasts file matched their recorded hashes. No deviations. Every ratio and interval below was recomputed independently from `forecasts.csv` with the locked bootstrap and agrees with `results.json`.

Every sentence below is a pre-written sentence from Section 7 of the plan.

## Results

| Label | Comparison | RMSE ratio | 90% interval | Credible improvement | DM-HLN p-value |
| --- | --- | --- | --- | --- | --- |
| **T1** | Timestral vs AR(2) (primary) | 1.018 | 0.960–1.093 | No | 0.78 |
| T2 | Timestral with credit vs without | 0.998 | 0.980–1.009 | No | 0.37 |
| T4 | Timestral vs TimesFM 3.0 (descriptive) | 1.014 | 0.981–1.033 | — | 0.79 |
| T4 | Timestral vs TimesFM 2.5 (descriptive) | 1.003 | 0.959–1.025 | — | 0.57 |

| Label | Premium (real-time ratio minus revised ratio) | 90% interval | Size |
| --- | --- | --- | --- |
| T3 | -0.002 | -0.006 to +0.001 | Small |

**T1.** Given only real-time data, Timestral did not forecast GDP growth credibly better than the AR(2) (ratio 1.018; 90% interval 0.960–1.093). Its training data may include the forecast period; that could have helped or hurt it (Section 5), so this result does not show how a model without that exposure would fare. *These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured.* The power of this comparison is unknown (Section 4 of the plan).

**T2.** Given only real-time data, Timestral did not forecast credibly better with credit than without credit (ratio 0.998; 90% interval 0.980–1.009). Its training data may include the forecast period; that could have helped or hurt it (Section 5), so this result does not show how a model without that exposure would fare. *These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured.* The self-test's positive control showed that Timestral does use a past-only covariate when it carries a signal (Section 11 of the plan), so this null is not a plumbing failure. Only reductions of roughly 40% would be reliably detected on this credit path.

**T3.** The revised-credit premium was small (-0.002; 90% interval -0.006 to +0.001): revised credit data did not change the answer to T2. *These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured.*

**T4.** On the same 78 origins, Timestral's forecasts were about as accurate as TimesFM 3.0's (ratio 1.014; 90% interval 0.981–1.033). This comparison is descriptive: the TimesFM forecasts were seen before this plan was written. *These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured.*

On the same 78 origins, Timestral's forecasts were about as accurate as TimesFM 2.5's (ratio 1.003; 90% interval 0.959–1.025). This comparison is descriptive: the TimesFM forecasts were seen before this plan was written. *These intervals are known to undercover on this credit path (Section 5.1 of the paper); for comparisons without credit, their coverage has not been measured.* The power of the T4 comparisons is unknown.

The T2 sentence uses the word order of the TimesFM note's F3 sentence ("did not forecast credibly better with credit than without credit"), the same pre-written template filled for a credit comparison.

## The 2010–12 forecasts

Origins 2010Q1–2011Q4, where the locked credit model failed. Annualised growth, percent.

| Origin | Target | Outcome | AR(2) | Credit model | Timestral | Timestral + credit | TimesFM 2.5 | TimesFM 3.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2010Q1 | 2011Q1 | -0.95 | 2.84 | 5.41 | 2.89 | 3.10 | 3.29 | 3.17 |
| 2010Q2 | 2011Q2 | 2.73 | 2.88 | 6.69 | 3.06 | 3.15 | 3.08 | 3.06 |
| 2010Q3 | 2011Q3 | -0.09 | 2.97 | 6.77 | 2.78 | 2.95 | 2.76 | 2.93 |
| 2010Q4 | 2011Q4 | 4.57 | 3.02 | 7.52 | 2.59 | 2.77 | 2.52 | 2.51 |
| 2011Q1 | 2012Q1 | 3.40 | 2.95 | 6.52 | 2.87 | 3.00 | 2.71 | 2.68 |
| 2011Q2 | 2012Q2 | 1.80 | 3.01 | 5.76 | 2.60 | 2.63 | 2.47 | 2.49 |
| 2011Q3 | 2012Q3 | 0.58 | 3.06 | 5.48 | 2.20 | 2.40 | 2.12 | 2.07 |
| 2011Q4 | 2012Q4 | 0.46 | 2.97 | 4.27 | 2.46 | 2.65 | 2.07 | 2.14 |

## The lower tail (descriptive)

| Model | 10th-percentile loss, all origins | Outcome below 10th percentile, all | Loss, 2008–12 targets | Below 10th percentile, 2008–12 |
| --- | --- | --- | --- | --- |
| AR(2) | 0.498 | 10% | 0.883 | 25% |
| Timestral | 0.570 | 12% | 1.093 | 25% |
| Timestral + credit | 0.550 | 12% | 1.089 | 25% |

Lower loss is better. A well-calibrated 10th percentile is breached about 10% of the time.

## Leakage checks

- **L0: Uncertain.** The model card lists no training data; Mistral says most training data were synthetic and does not name the real data.
- **L1: no flag.** Degradation ratio over all 78 origins: Timestral 1.002, AR(2) 0.995 (excess +0.007; threshold 0.10). Over 2010Q1–2011Q4: Timestral 0.986, AR(2) 0.984 (excess +0.002; threshold 0.20). Per-draw ratios are in `results.json`.
- **L2: no flag.** Real-series ratio 0.871, at the 48th percentile of the 50 placebo ratios (10th percentile 0.773; median 0.898).

None of these proves or rules out leakage. Since no comparison shows a gain, the wording of every result is the same whatever they show.

## Run record

Timestral-209M, `mistralai/Timestral-209M` @ `9874d252ab0aae16f7f7c999f98f98d6ad7d8365` (weights SHA-256 `1456effb…`); `timestral` 1.0.0 @ `a534bdbd`; torch 2.14.1, numpy 2.4.6, Python 3.11.17, Linux under WSL2, CPU only; package default settings. Outputs in `results_attempt1/`: `results.json`, `forecasts.csv` and `run_log.txt`. The run also wrote `table_2010_12.csv`, the 2010Q1–2011Q4 rows of `forecasts.csv`, shown above; it is not separately archived.

## Use of AI

The author is responsible for all design decisions, modelling runs, interpretation, and final content. AI tools (including Claude, Microsoft Copilot, DeepSeek, and Z.ai) were used for drafting text, writing and testing scripts, checking outputs, and performing sanity-checks on reasoning and code. All modelling was executed by the author, who retains full responsibility for the analysis and results.
