# TimesFM extension: real-time GDP forecasts with a time-series foundation model

A preregistered extension to the working paper *Did the Credit Impulse Help Forecasters in Real Time? A Preregistered Test, 1999–2019* (v2.2, DOI [10.5281/zenodo.23560860](https://doi.org/10.5281/zenodo.23560860)). It does not change the paper's headline.

**Result.** Given only real-time data, neither TimesFM 2.5 nor TimesFM 3.0 forecast US GDP growth four quarters ahead credibly better than a direct AR(2) over 78 origins, 1999Q3–2018Q4. Adding the real-time credit impulse did not credibly improve either model, and the revised-credit premium was small for both. The credit comparisons are underpowered: read them as "no credible improvement detected", not "no effect".

**Archived:** release `timesfm-note`, DOI [10.5281/zenodo.23675487](https://doi.org/10.5281/zenodo.23675487).

**Read the note:** [`note/timesfm_note_2026-10-26.pdf`](note/timesfm_note_2026-10-26.pdf) (also as [Markdown](note/timesfm_note_2026-10-26.md)).

## Timeline

| Step | Where |
|---|---|
| Plan frozen before any TimesFM forecast of real data | tag `timesfm-plan` (commit 7406c2c, 26 Oct 2026 17:26 UTC); `PLAN.md`, `PLAN_LOCK.json` |
| Run 1 completed with a defect in the TimesFM 2.5 wrapper | `results_run1_backcast_bug/` (kept unchanged) |
| Fix committed in public before re-running | commit d2d7acd |
| Run 2, the reported run | `results/` |
| Deviations, declared | `../DEVIATIONS.md`, Entries 62–70; note Section 6 |

## Files

| Path | Contents |
|---|---|
| `PLAN.md` | The preregistered analysis plan |
| `PLAN_LOCK.json` | Tag, file hashes, checkpoints, package versions, L0 ratings, L1 thresholds |
| `results/` | Run 2: `forecasts.csv`, `table_2010_12.csv`, `results.json`, `run_log.txt` |
| `results_run1_backcast_bug/` | Run 1, defective, kept for the record |
| `note/` | The note (PDF, Markdown) and its one figure |
| `../code_post_lock/tfm_*.py`, `run_timesfm.py` | Public scripts (MIT) |

## Licences and what is not here

- TimesFM 2.5 weights: Apache-2.0. TimesFM 3.0 weights: TimesFM Non-Commercial License v1.0.
- The TimesFM 3.0 back-end script is not published: the licence forbids distributing works that use the model. Its settings are described in `PLAN.md` and its SHA-256 is in `PLAN_LOCK.json`. TimesFM 3.0 forecasts (outputs, which the licence says are not Derivatives) are published, for non-commercial research use only.
- No model weights are in this repository.

## Reproducing

Download the checkpoints at the revisions in `PLAN_LOCK.json` (the run script checks their hashes), assemble the working layout described in `../REPLICATION.md`, and run `python run_timesfm.py real` from `p2/post_lock/`. The script refuses to run if `timesfm/results/` exists. Use `python run_timesfm.py pipeline-test OUTDIR` to test the pipeline with a stand-in model.

## AI use

AI tools (including Claude, ChatGPT, Microsoft Copilot, DeepSeek, Kimi and Z.ai) helped draft text, write and test scripts and check outputs. The defect described in the note's Section 6 was in code written with Claude's help. The author made all design decisions, ran the models and is responsible for the content.

## Related work

Carriero, Pettenuzzo and Shekhar (2026), "MACROCAST: A Vintage-Consistent Time Series Foundation Model for Real-Time Macroeconomic Forecasting", arXiv:2606.28670 (30 June 2026), evaluate off-the-shelf foundation models (Chronos-2 and Moirai2-Small) on 123 monthly FRED-MD series with real-time vintages, August 1999 to December 2024. Against an AR(1), the median error ratios are close to 1 beyond the short term (about 0.99–1.00 at 6 and 12 months); their own small model, trained on vintage-consistent data, beats the AR(1) on most series by small margins. They do not test TimesFM or Timestral, GDP or credit covariates, and their evaluation is not preregistered. Their findings and these are consistent. This work was found after the TimesFM and Timestral plans were frozen and played no part in their design.
