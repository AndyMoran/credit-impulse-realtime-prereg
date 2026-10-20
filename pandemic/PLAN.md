# Pandemic-period illustration, 2020–21: analysis plan

19 October 2026 · Andy Moran (Heaviside Analytics)

> **Status.** This plan was written on 19 October 2026, before any Z.1 release from 2020 was downloaded and before any forecast for a 2020–21 target was computed. It will be committed to the public repository and tagged before the download. That tag's timestamp, not this document, is the evidence of timing. Whatever this exercise finds, it is a **non-preregistered illustration**: it is not part of the confirmatory family, it cannot change the study's headline, and it is reported in full whatever it shows.
>
> **What is and is not already known.** GDP and unemployment outcomes for 2020–21 are public, and the author knows them. The protocol's rule of excluding forecasts with targets from 2020Q1 onwards was written with the pandemic known. What has not been seen is the real-time credit data published in 2020, and any forecast the locked models would have made for 2020–21 targets. This plan fixes every choice about those before they are seen.

## 1. Why this exists, and what it can show

The protocol (v2.3, checklist F) says that 2020–21 is "excluded from confirmatory sample; reported separately". The working paper has not yet reported it, and an external reviewer pointed out the gap. This plan meets that commitment.

The question is narrow: **what would the locked models, unchanged, have forecast for 2020–21 targets, using only the credit data published at the time, and how did those forecasts compare with the benchmark?**

What it can show:

- how a credit-augmented forecast behaves through a shock that did not originate in credit;
- whether the 2020 real-time credit data, which include government-guaranteed loans and drawn credit lines, sent a misleading signal.

What it cannot show:

- **Anything confirmatory.** There are only eight targets, all dominated by one shock. No p-values and no intervals will be reported.
- **Anything about credit's causal role in 2020.** The pandemic was not a credit shock, and government lending changed what the credit series measures.
- **A revised answer to the paper's question.** The headline stays as pre-committed.

No outcome of this exercise is described in advance as "supporting" or "undermining" the study. Section 4 fixes the wording for each possible result.

## 2. Sample and data

**Targets.** Eight target quarters, 2020Q1–2021Q4, at the locked horizon h = 4. The origins are therefore 2019Q1–2020Q4. These are exactly the forecasts that the locked rule "exclude any forecast whose target falls in 2020Q1 or later" removed. No other horizon, period or extension is added.

**Credit data.** As in the locked design, each origin uses the latest Z.1 release dated before its origin date (the 15th of the middle month).

| Origins | Z.1 release used | Status |
| --- | --- | --- |
| 2019Q1–2020Q1 | Dec 2018 – Dec 2019 | Already in the locked dataset |
| 2020Q2 | 12 March 2020 | **To download** |
| 2020Q3 | June 2020 release | **To download** |
| 2020Q4 | September 2020 release | **To download** |

The exact June and September 2020 release dates will be read from the Federal Reserve's release-dates page and recorded before parsing. If either release turns out to post-date its origin, the locked rule picks the previous release, and whatever the rule gives is used.

**Other data.** These are already in hand, in the frozen files whose hashes are recorded in the locked manifest:

- Real-time GDP, deflator and unemployment vintages (RTDSM).
- Revised targets from the same 2026Q3 vintage as the main study.
- SPF median forecasts.

The SPF survey deadlines for 2020 are not in the locked deadline map, which ends at 2019Q4. They will be taken from the Philadelphia Fed's release-dates file and recorded with its hash.

**Nothing else is downloaded.** In particular, no release after September 2020 is used, and the revised credit series remains the September 2026 release already in the dataset.

## 3. Models and code

**Models: exactly the locked specification.** These are P1a (GDP growth), P1b (unemployment) and P2a (the SPF median GDP forecast, corrected with credit), each against its locked benchmark: a direct AR(2) with four published lags of the real-time credit impulse, entering at their release lags, against the same AR(2) without them; and for P2a, the credit-corrected against the bias-corrected SPF forecast. Each model is re-estimated at every origin on an expanding window from 1965Q1, using only pairs whose target had been published by the origin. As a consequence, origins in late 2020 are trained on data that already include the 2020Q2 collapse. That follows from the locked rule and is not adjusted. P3 (GDP revisions) is not extended: eight quarters cannot support a regression with controls, and revisions to 2021 are still recent.

**Code: the locked `phase2.py`, unedited.** A new script, `post_lock/pandemic.py`, will:

1. import the locked `phase2.py` without editing it (its SHA-256 is checked at start-up: `da697030…`);
2. add the three 2020 vintages, parsed by the locked parser (`parse_z1.py`, v4) into a separate file, `credit_vintages_2020.csv`. The locked dataset is not modified;
3. add the 2020 SPF deadlines to the deadline map in memory;
4. move the target cut-off from 2019Q4 to 2021Q4, the only parameter changed;
5. call the locked functions `run_p1` and `run_p2` for the eight origins, and once for the extended sample described in Section 4.

Before any real 2020 data are used, the script will be shown to reproduce the locked 1999Q3–2018Q4 forecasts exactly, with the cut-off at 2019Q4.

## 4. What will be reported, and how it will be worded

All of the following will be reported, whatever they show:

1. **A forecast table** for each of P1a, P1b and P2a, with one row per target quarter (eight rows). Each row gives the real-time impulse at q\*, the credit term (for P1a and P1b, the summed credit coefficients times the impulse lags), the benchmark forecast, the credit-model forecast, the outcome (from the 2026Q3 vintage, as in the main study) and the squared-error difference.
2. **The RMSE ratio over the eight targets** for each test, and the mean forecast error of each model.
3. **The extended-sample ratio**: the locked comparison re-computed over origins 1999Q3–2020Q4 (86 origins), shown next to the locked ratio for 1999Q3–2018Q4. It is labelled descriptive.
4. **The real-time impulse in 2019–20**, as published in the March, June and September 2020 releases, against the revised series.

No p-values, intervals or bootstrap results will be computed for this exercise.

**Pre-written wording.** For each test, the sentence is chosen by the eight-target RMSE ratio *r*:

| Ratio over the eight targets | Sentence |
| --- | --- |
| *r* < 0.90 | "Over the eight pandemic-period targets, the credit model's forecasts were more accurate than the benchmark's (ratio *r*)." |
| 0.90 ≤ *r* ≤ 1.10 | "Over the eight pandemic-period targets, the credit model's forecasts were about as accurate as the benchmark's (ratio *r*)." |
| *r* > 1.10 | "Over the eight pandemic-period targets, the credit model's forecasts were less accurate than the benchmark's (ratio *r*)." |

Each is followed by the same two sentences: "With eight targets dominated by one shock that did not originate in credit, this is an illustration, not evidence about predictive content. It does not alter the pre-registered conclusion." Then come two factual sentences: one on the direction of the credit model's errors (whether it over- or under-forecast on average), and "Adding these targets changes the full-sample ratio from \[locked value\] to \[extended value\]."

**Placement.** The results will go in a new subsection, 5.6, "The pandemic period, 2020–21 (not preregistered)", with one sentence in Section 6. The abstract, the headline and the pre-committed interpretive map will not change.

## 5. Procedure, in order

1. **Agree this plan.** The author reads it and settles any change before step 3. After that, the plan is frozen.
2. **Write and test the script.** `post_lock/pandemic.py` is written and shown to reproduce the locked 1999Q3–2018Q4 forecasts exactly. It may be tested only on data already in the locked release.
3. **Freeze the plan and the script publicly.** Commit this plan (as Markdown) and `pandemic.py` to the repository, tag the commit `pandemic-plan`, and record the commit hash, the tag time and both files' SHA-256 in the audit log.
4. **Download, then hash.** Download the March, June and September 2020 Z.1 release archives, the Federal Reserve's release-dates page and the Philadelphia Fed's SPF release-dates file. Record each file's SHA-256 before opening it.
5. **Parse and check.** Parse the three releases with the locked parser. Run the locked continuity check against the December 2019 vintage: no consecutive pair may differ by more than a factor of 2 in median level. Confirm the household and business series codes used in December 2019. Record the parse report.
6. **Run once.** Run `pandemic.py` once and save its outputs and log with their hashes.
7. **Report.** Write Section 5.6 using only the wording in Section 4, and log the run as an audit entry stating that results were seen.

If a step fails for a mechanical reason, such as a renamed file or a changed column header, only the mapping is fixed, as the Phase 1 rules allow, and the fix is logged before the run. No model, sample or wording choice is reopened.

## 6. What counts as a deviation

Any of the following after step 3 is a deviation. It must be logged with its date and a statement of whether results had been seen, and reported in Section 5.6:

- a change to the targets, origins, horizon or releases used;
- any change to `phase2.py` or `pandemic.py` beyond a logged mapping fix;
- running the analysis more than once on real 2020 data;
- a fourth test, another credit measure, another horizon, or any statistic not listed in Section 4;
- wording other than the pre-written sentences, or moving the results out of Section 5.6;
- leaving any listed output unreported.

The main study's locked results are not re-estimated or replaced. If the pandemic-period exercise raises a question worth testing, for example how government-guaranteed lending distorts the credit impulse, it goes into a new plan, written before the data are examined.
