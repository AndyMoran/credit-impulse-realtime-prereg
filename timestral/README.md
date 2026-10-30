# Timestral extension: real-time GDP forecasts with Mistral's time-series foundation model

A preregistered extension to the TimesFM note (DOI [10.5281/zenodo.23675487](https://doi.org/10.5281/zenodo.23675487)) and the working paper (DOI [10.5281/zenodo.23560860](https://doi.org/10.5281/zenodo.23560860)).

**Result.** Given only real-time data, Timestral-209M did not forecast US GDP growth four quarters ahead credibly better than a direct AR(2) over 78 origins, 1999Q3–2018Q4 (ratio 1.018; 90% interval 0.960–1.093). Adding the real-time credit impulse did not help, and the revised-credit premium was small. Its forecasts were about as accurate as both TimesFM models'.

**Archived:** release `timestral-results`, DOI [10.5281/zenodo.23812724](https://doi.org/10.5281/zenodo.23812724).

| File | What it is |
| --- | --- |
| `PLAN.md` | The preregistered plan, frozen at tag `timestral-plan` |
| `PLAN_LOCK.json` | The lock: tag, file and checkpoint hashes, settings |
| `RESULTS.md` | **The results note**, in the plan's pre-written sentences |
| `results_attempt1/` | The official run (attempt 1, all gates passed) |
| `../code_post_lock/tsl_*.py`, `run_timestral.py` | The scripts (MIT); they reuse the frozen TimesFM scripts |

The model weights are not in this repository. They are downloaded from Hugging Face (`mistralai/Timestral-209M`, revision in `PLAN_LOCK.json`) under Mistral's Modified MIT licence.

## Related work

Carriero, Pettenuzzo and Shekhar (2026), "MACROCAST: A Vintage-Consistent Time Series Foundation Model for Real-Time Macroeconomic Forecasting", arXiv:2606.28670 (30 June 2026), evaluate off-the-shelf foundation models (Chronos-2 and Moirai2-Small) on 123 monthly FRED-MD series with real-time vintages, August 1999 to December 2024. Against an AR(1), the median error ratios are close to 1 beyond the short term (about 0.99–1.00 at 6 and 12 months); their own small model, trained on vintage-consistent data, beats the AR(1) on most series by small margins. They do not test TimesFM or Timestral, GDP or credit covariates, and their evaluation is not preregistered. Their findings and these are consistent. This work was found after the TimesFM and Timestral plans were frozen and played no part in their design.
