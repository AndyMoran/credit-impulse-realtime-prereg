# Plan 2: the horizon sweep

At which horizon does the Philadelphia Fed's Manufacturing Business Outlook Survey earn its place beside an AR(2)? A preregistered test on real-time US GDP, 1999–2019.

| File | What it is |
| --- | --- |
| `PLAN.md` | The preregistered plan, frozen at tag `plan2` |
| `release_dates.csv` | The survey reading used at each of the 78 origins, its release time and the next release |
| `power_coverage.json` | The pre-freeze power and coverage check (Section 13) |
| `feasibility/` | The ALFRED revision check that made the plan possible |
| `../code_post_lock/plan2_*.py`, `run_plan2.py` | The scripts (MIT) |

**Survey data are not in this repository.** The Philadelphia Fed permits research use but not redistribution. `plan2_fetch.py` downloads the two unadjusted series from ALFRED (vintage 15 October 2026) with your own free FRED API key, set as the environment variable `FRED_API_KEY`, and prints their SHA-256. Gate 6 of the run checks them against the hashes in `PLAN.md`, Section 13.

**Running.** Assemble the working layout in `../REPLICATION.md`, put the scripts in `p2/post_lock/`, then run `plan2_fetch.py`, `plan2_selftest.py` and `python run_plan2.py pipeline-test OUTDIR`. The real run, `python run_plan2.py real`, refuses without `plan2/PLAN2_LOCK.json` and refuses once an attempt has passed the gate.
