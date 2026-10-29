# Plan 2: the horizon sweep

At which horizon does the Philadelphia Fed's Manufacturing Business Outlook Survey earn its place beside an AR(2)? A preregistered test on real-time US GDP, 1999–2019.

**Result.** At h = 1, the primary test, the survey did not improve the AR(2) credibly (ratio 0.930; 90% interval 0.869–1.038); reliable detection needed a ratio of about 0.85. The survey's ratios rose monotonically with the horizon, consistent with a fading relative advantage, but the rise was not established. The credit impulse did not improve the AR(2) at any horizon. Details and caveats: `RESULTS.md`.

| File | What it is |
| --- | --- |
| `PLAN.md` | The preregistered plan, frozen at tag `plan2` |
| `PLAN2_LOCK.json` | The lock: tag, file hashes, survey hashes, seeds |
| `RESULTS.md` | **The results**, in the plan's pre-written sentences, with one declared wording deviation |
| `results_attempt1/` | The official run (attempt 1, all gates passed): `results.json`, `forecasts.csv`, `run_log.txt` |
| `figures/` | The ratio curve and coefficient curve, and the script that draws them from `results.json` |
| `release_dates.csv` | The survey reading used at each of the 78 origins, its release time and the next release |
| `power_coverage.json` | The pre-freeze power and coverage check (Section 13) |
| `feasibility/` | The ALFRED revision check that made the plan possible |
| `../code_post_lock/plan2_*.py`, `run_plan2.py` | The scripts (MIT) |

**Survey data are not in this repository.** The Philadelphia Fed permits research use but not redistribution. `plan2_fetch.py` downloads the two unadjusted series from ALFRED (vintage 15 October 2026) with your own free FRED API key, set as the environment variable `FRED_API_KEY`, and prints their SHA-256. Gate 6 of the run checks them against the hashes in `PLAN.md`, Section 13.

**Running.** Assemble the working layout in `../REPLICATION.md`, put the scripts in `p2/post_lock/`, then run `plan2_fetch.py`, `plan2_selftest.py` and `python run_plan2.py pipeline-test OUTDIR`. The real run, `python run_plan2.py real`, refuses without `plan2/PLAN2_LOCK.json` and refuses once an attempt has passed the gate.
