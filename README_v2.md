# v2.0-results: results, figures and working paper

This release adds the outputs of the preregistered study locked in `v1.0-lock` (DOI 10.5281/zenodo.23477871). Every file from the lock is unchanged; this release only adds new folders.

**Headline (pre-committed wording): "null, small premium."** The US credit impulse, as published at the time, did not improve four-quarter-ahead forecasts of real GDP growth or unemployment over 1999–2019, and revisions to the credit data do not change that.

| Test | Estimate | 90% interval |
|---|---|---|
| P1a GDP, RMSE ratio vs direct AR(2) | 1.106 | 0.984–1.356 |
| P1b unemployment, RMSE ratio | 1.011 | 0.994–1.043 |
| P2a SPF median GDP, RMSE ratio | 1.025 | 0.988–1.076 |
| P3 GDP revision on impulse (pp per point) | 0.111 | −0.047 to 0.269 |

Ratios below 1 mean credit helps. No test shows a credible improvement. The credit-revision premium is +0.0005 for GDP and +0.008 for unemployment.

| Folder | Contents |
|---|---|
| `results/` | `results.json` and the forecast tables from the single locked run, the run log, and `LOCK.json` |
| `figures/` | Figs 1–2 (Phase 1, already in the lock) and Figs 3–6 (§13), as PNG and PDF |
| `paper/` | Working-paper draft, 19 Oct 2026 |
| `protocol_post_lock/` | The protocol with its audit log through Entry 26 |
| `checks/` | Independent verification report on the manuscript |
| `code_post_lock/` | `figures.py`, the only script written after lock (it draws figures, with no estimation) |
| `DEVIATIONS.md` | Every post-lock entry, with whether results had been seen |
| `MANIFEST_v2.txt` | SHA-256 of every file in this release |

To reproduce: run `code/phase2/phase2.py real` from the v1.0-lock layout with `LOCK.json` in place, then run `code_post_lock/figures.py`.
