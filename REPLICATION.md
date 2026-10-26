# Replication package: "Did the Credit Impulse Help Forecasters in Real Time? A Preregistered Test, 1999–2019"

Andy Moran (Heaviside Analytics). Package version 2.2, 22 October 2026.

The package is split across four GitHub releases of `AndyMoran/credit-impulse-realtime-prereg`. Each release adds folders and none changes an earlier one:

| Release | DOI | Contents |
| --- | --- | --- |
| `v1.0-lock` | 10.5281/zenodo.23477871 | Locked protocol, all analysis code, real-time credit vintages, `MANIFEST.txt` |
| `v2.0-results` | 10.5281/zenodo.23479717 | The single locked run (`results/`), Figures 1–6, `figures.py` |
| `v2.1-verification` | 10.5281/zenodo.23497087 | Revised paper, post-lock analyses, pandemic-period illustration, verification kit |
| `v2.2-publish` | 10.5281/zenodo.23560860 | Working paper v2.2 (style revision; no result changed), audit log to Entry 58 |

The tag `pandemic-plan` (commit b9a7fc0) freezes the pandemic-period plan and script before any 2020 data were downloaded.

## 1. Data availability and provenance

All inputs are public. The author had legitimate access to every one of them, and no data are confidential.

| Source | What is used | Where | Files and hashes |
| --- | --- | --- | --- |
| Board of Governors of the Federal Reserve System, *Financial Accounts of the United States* (Z.1) | 83 quarterly releases, June 1999–December 2019, plus the release of 11 September 2026 (tables D.2/D.3: household and nonfinancial business debt, flows and levels) | federalreserve.gov/releases/z1/ (dated archive folders) | Parsed vintages in `data_derived/credit_vintages_long.csv` (v1.0-lock). The SHA-256 of each downloaded archive is in `data_derived/download_log.csv` |
| Same, pandemic-period illustration | Releases of 12 March, 11 June and 21 September 2020 | Same | Archives in `pandemic/raw/`. Hashes in `pandemic/download_log_2020.csv` and audit log Entry 34 |
| Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists | ROUTPUT, NOUTPUT, P (quarterly vintages), RUC (monthly), first-release ROUTPUT | philadelphiafed.org, Real-Time Data Research | Not redistributed in v1.0-lock; SHA-256 in `MANIFEST.txt`. The site states that the data set "may be used by macroeconomic researchers to verify empirical results". Preferred citation: Croushore and Stark (2001) |
| Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters | Median RGDP growth and UNEMP levels; individual RGDP responses; release-dates file | Same | Hashes in `MANIFEST.txt` and, for the 2020 release-dates file, `pandemic/raw/` |
| FRED, Federal Reserve Bank of St. Louis | GS2, the two-year Treasury yield, monthly | fred.stlouisfed.org/series/GS2 | Hash in `MANIFEST.txt` |

**Raw-input files for verification.** The ten Philadelphia Fed and FRED files used in the locked run are collected in `raw_inputs_v1.0-lock.zip` (SHA-256 `56ec8466dd5ba9986a82020323327af1c497f91e573c2b5c3ae327c95c87a6f3`). It is attached to the `v2.1-verification` GitHub release. The Philadelphia Fed files grow every quarter, so a fresh download will not match the recorded hashes once a newer vintage has been added. Use the archived copies.

## 2. Computational requirements

- **Software:** Python 3.11 or later with numpy, pandas, scipy, statsmodels and openpyxl. Two environments have run the locked analysis:
  - Linux, Python 3.13.16, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0, openpyxl 3.1.5 (the published run; byte-identical `results.json`);
  - Windows 11, Python 3.13.14, numpy 2.3.3, pandas 2.3.3 (same estimates; `results.json` differs only in floating-point rounding).
- **Hardware:** any laptop. Memory use is under 2 GB.
- **Run times (two-core cloud machine):**

| Script | Time |
| --- | --- |
| Locked analysis (`phase2.py real`) | about 40 seconds |
| `verify_lock.py` | about 1 minute |
| Figures and tables | seconds each |
| Coverage simulation (`coverage.py`) | about 20 minutes as two parallel processes of 150 replications |
| Calibration simulation (`calibrate.py`) | about 10 minutes as two parallel processes of 150 replications |
| Pandemic-period run | about 5 seconds |

- **Randomness:** every random draw is seeded. The locked seed is 20261019. The simulation seeds are given in Appendix D of the paper.

## 3. Directory layout for running

The scripts expect the working layout of the original project. Assemble it from the releases as follows:

```text
work/phase0/spf_deadlines_z1_map.csv         <- v1.0-lock tables/
work/p1/build.py, fixedb.py                  <- v1.0-lock code/phase1/
work/p1/data/credit_vintages_long.csv,
             download_log.csv                <- v1.0-lock data_derived/
work/p1/data/*.xlsx, GS2.csv; spf/*.xlsx     <- raw inputs (Section 1)
work/p2/phase2.py, test_phase2.py            <- v1.0-lock code/phase2/
work/p2/LOCK.json, results_real/             <- v2.0-results results/
work/p2/figures.py                           <- v2.0-results code_post_lock/
work/p2/post_lock/*.py                       <- v2.1 code_post_lock/
work/p2/post_lock/out/                       <- v2.1 results_post_lock/ (to reuse the simulation outputs)
work/pandemic/                               <- v2.1 pandemic/
work/p2/post_lock/tfm_*.py, run_timesfm.py   <- timesfm-plan code_post_lock/ (TimesFM extension)
work/timesfm/PLAN.md                         <- timesfm-plan timesfm/
```

## 4. Instructions

1. **Verify the locked run:** `python verification/verify_lock.py --release <v1.0-lock folder> --results <v2.0-results folder> --raw raw_inputs_v1.0-lock.zip`. The script checks every hash, runs the locked analysis once in a temporary folder and compares the results. See `verification/VERIFY.md`.
2. **Reproduce the locked results by hand:** in `work/p2`, run `python phase2.py real`. It writes `results_real/`, which should match `v2.0-results/results/`.
3. **Reproduce the figures:** run `python figures.py` in `work/p2` for Figures 3–6, and `python post_lock/fig7.py` after `post_lock/diagnostics.py` for Figure 7. Figures 1–2 come from the Phase 1 scripts (`code/phase1/charts.py` in v1.0-lock).
4. **Reproduce the post-lock analyses:** run these in `work/p2/post_lock`:
   - `python diagnostics.py`
   - `python table4_contributions.py`
   - `python coverage.py 150 0` and `python coverage.py 150 150`
   - `python calibrate.py 150 0` and `python calibrate.py 150 150`
   - `python calibrated_intervals.py`
5. **Pandemic-period illustration:** `python post_lock/pandemic.py check` reproduces all 234 locked forecasts without using 2020 data. The real mode runs only once; it refuses if `pandemic/results/` already exists. To re-run it, copy the package elsewhere and delete that folder. The script must match the tagged hash `759dbf4f…`.

## 5. Tables and figures

| Exhibit | Program | Output |
| --- | --- | --- |
| Table 1 | v1.0-lock `code/phase1/study.py` | `data_derived/revision_stats.csv` |
| Table 2 | v1.0-lock `code/phase1/power2.py` (Gaussian path), `code/phase2/power_realpath.py` (actual path) | `phase1_results/power2_results_R2000.csv`, `power_realpath.csv` |
| Table 3 | `phase2.py` | `results_real/results.json` (`core`) |
| Table 3b | `calibrate.py`, `calibrated_intervals.py` | `results_post_lock/calibrated_intervals.json`, `coverage_by_level.csv` |
| Table 4 | `table4_contributions.py` | `results_post_lock/table4_contributions.csv` |
| Table 5 | `diagnostics.py` | `results_post_lock/p1a_top_loss_origins.csv` |
| Table 6 | `phase2.py` | `results.json` (`exploratory`) |
| Table 7 | `pandemic.py` | `pandemic/results/pandemic_results.json` |
| Figures 1–2 | v1.0-lock `code/phase1/charts.py` | `phase1_results/` |
| Figures 3–6 | v2.0-results `figures.py` | `figures/` |
| Figure 7 | `diagnostics.py`, `fig7.py` | `figures/fig7_p1a_coefficients_forecasts.*` |
| §5.1 coverage rates | `coverage.py`, `calibrate.py` | `results_post_lock/coverage_*.csv`, `calib_*.csv` |
| §5.3 SPF training start | `diagnostics.py` | `results_post_lock/p2a_training_start.csv` |

## 6. Records

- `DEVIATIONS.md` lists every post-lock step, with whether results had been seen.
- The full audit log (Entries 1–58) is in `protocol_post_lock/`.
- `checks/` holds the independent agent check of the manuscript.
- `verification/` holds the verification kit and the author's own cross-platform re-run (not an independent check).

**Independent re-runs are invited.** Please report them using the "Verification re-run" issue template. None has been reported yet.

## References

Croushore, D. and Stark, T. (2001). A real-time data set for macroeconomists. *Journal of Econometrics* 105(1): 111–130.
