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
