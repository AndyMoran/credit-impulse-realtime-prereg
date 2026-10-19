# Real-time credit impulse and US macro forecasting, 1999–2019: preregistration lock

**Question.** Did US private credit flows, measured from Federal Reserve Z.1 data **as published at the time**, carry information about later real GDP growth and unemployment that a forecaster could have used? How much of the predictive content reported on revised data depends on later revisions to the credit data?

**Status.** Locked before any forecast was scored against a real target and before any real SPF forecast error was examined. Phase 2, which runs every test once, starts only after this release is public.

Author: Andy Moran (Heaviside Analytics). Analysis code written with Claude (Anthropic).

## What is locked

| Folder | Contents |
|---|---|
| `protocol/` | Protocol v2.3 with the full Phase 0–1 audit log (Entries 1–19), as Markdown and PDF |
| `code/phase0`, `code/phase1` | Data audit, Z.1 download and parsing, credit-measure construction, revision study, power simulations |
| `code/phase2` | `phase2.py`: the complete analysis that Phase 2 will run; `test_phase2.py`: the synthetic-data test harness; `power_realpath.py`, `ci_check.py`, `p3_size_check.py`: the design checks behind the final decision rules |
| `tables/` | Z.1 release dates (verified), SPF deadline–Z.1 map, origin–release table |
| `data_derived/` | Real-time credit vintages (84 Z.1 releases, $ billions), credit measures by vintage, revision statistics, gap decomposition |
| `phase1_results/` | Phase 1 charts and all power-simulation outputs |
| `synthetic_tests/` | Results of the synthetic tests (credit real; all targets and SPF simulated) |
| `MANIFEST.txt` | SHA-256 of every file here, plus hashes of the raw public inputs that are not redistributed |

## Confirmatory core (Holm across four)

- **P1a.** Real-time credit impulse vs direct AR(2), real GDP growth, h = 4.
- **P1b.** As P1a, for the unemployment rate.
- **P2a.** Credit-corrected vs bias-corrected SPF median GDP forecast.
- **P3.** Real-time credit impulse vs later revisions to advance GDP.

All four fall in the protocol's "estimate only" power band (audit Entries 18–19). The credit impulse's variation is concentrated in 2008–09, so only very large gains (roughly 40% or more) can be detected reliably. Results will be reported as estimates with 90% intervals. "Credible improvement" will be claimed only if the whole interval excludes no-gain, and no significance language will be used.

## Reproducing

Python 3.11+ with numpy, pandas, scipy, statsmodels and openpyxl. Raw inputs are public: Fed Z.1 archive, Philadelphia Fed RTDSM and SPF, FRED GS2. Their exact versions are identified by the hashes in `MANIFEST.txt` and `data_derived/download_log.csv`. Scripts assume the working layout `phase0/`, `p1/` (with raw inputs in `p1/data/`) and `p2/`; path constants are at the top of each script. `phase2.py` runs on real data only when `LOCK.json`, giving this release's URL, tag commit and DOI, is present.

## After lock

Any change is recorded in a dated deviation log, stating whether any results had been seen. All pre-registered outputs are published, including nulls.
