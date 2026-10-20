# v2.1: revised paper, post-lock analyses, pandemic-period illustration and verification kit

This release adds folders to the repository. Nothing from `v1.0-lock` (DOI 10.5281/zenodo.23477871) or `v2.0-results` (DOI 10.5281/zenodo.23479717) is changed. The locked results are unchanged.

| Folder | Contents |
| --- | --- |
| `paper/` | Working paper v2.1, 20 October 2026 (PDF and Markdown). Revised after three external reviews and a second independent claim check |
| `figures/` | Figure 7 (post-lock): P1a credit coefficients and forecasts |
| `code_post_lock/` | Post-lock scripts. All import the locked `phase2.py` unchanged. The coverage and calibration simulations, diagnostics, Table 4 and Figure 7 scripts, and `pandemic.py` (identical to the file tagged `pandemic-plan`) |
| `results_post_lock/` | Outputs of those scripts |
| `pandemic/` | Pandemic-period illustration: the frozen plan, `PLAN_LOCK.json`, the three 2020 Z.1 archives and release-date files (hashed), the parsed vintages, the single run's outputs and log |
| `verification/` | `verify_lock.py` (one-command re-run of the locked analysis), `VERIFY.md` (instructions), and the author's own cross-platform re-run (not an independent check) |
| `checks/` | Second independent agent check of the manuscript (171 claims) |
| `protocol_post_lock/` | The protocol with its full audit log, Entries 1–37 |
| `.github/ISSUE_TEMPLATE/` | Template for reporting a verification re-run |
| `DEVIATIONS.md` | Every post-lock step through Entry 37, with whether results had been seen |
| `REPLICATION.md` | Journal-style replication README: data provenance, requirements, instructions, and a map from each table and figure to its program |
| `MANIFEST_v2.1.txt` | SHA-256 of every file in this release |

**What changed in the paper since v2.0.**

- The headline now reads "no convincing average gain", and the uncertainty still allows modest gains.
- Coverage-calibrated intervals are reported as a sensitivity analysis.
- The 2011–12 mechanism was corrected: the model forecast a rebound, not weakness.
- The paper states that training uses the data vintage available at each forecast origin.
- New §5.6 reports the 2020–21 period under a plan frozen before the 2020 data were downloaded.
- Appendix D covers inference and simulation details.

**Independent re-runs are invited**: see `verification/VERIFY.md`.
