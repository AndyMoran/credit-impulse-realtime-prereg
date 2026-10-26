# Deviation and disclosure log (post-lock)

Locked: GitHub release `v1.0-lock`, commit 4eb084fb2c462fffec72574f108043ea9d796cc9, 19 Oct 2026 14:55 UTC, DOI 10.5281/zenodo.23477871.
Nothing in the locked release has been edited. Every entry below was added afterwards and says whether results had been seen.
The full audit log (Entries 1–58) is in `protocol_post_lock/protocol_v2.3_audit_log_to_entry58.pdf` (release v2.2); the version to Entry 37 is in release v2.1.

| Entry | Date (2026) | What | Results seen? |
|---|---|---|---|
| 21 | 19 Oct | Lock recorded. The tag-commit files (`MANIFEST.txt`, `phase2.py`, protocol) were re-downloaded and their SHA-256 hashes match the bundle. The bundle zip named in the v1.0 release notes was not attached, but its 42 files are committed individually and hashed in `MANIFEST.txt`. | No |
| 22 | 19 Oct | Phase 2 run once in real mode with the locked `phase2.py` (SHA-256 da697030…), 15:00:47–15:01:25 UTC, exit code 0, no deviations. `results/results.json` SHA-256 9e4239dd116eaea7c9f65df83f85d349f338aeb4adb6ff16904a6793ed6fa99c. | Yes (this is the run) |
| 23 | 19 Oct | S5 recorded as "not supported". The protocol did not define support for S5 and the results were mixed. This is the conservative reading, chosen after results were seen. | Yes |
| 24 | 19 Oct | The §13 figures were drawn from the locked outputs by `code_post_lock/figures.py` (no new estimation). The fitted line in Fig. 6 is for display only. The k_o lag is constant at 2, so it is stated in the text rather than drawn. | Yes |
| 25 | 19 Oct | An independent agent, which had not seen the drafting, checked 77 claims in the manuscript: 63 OK, 9 wrong, 2 rounding, 3 unverifiable. Every estimate matched the locked outputs. The errors were descriptive (mainly about the 2008 episode) and have been corrected. See `checks/verification_report.md`. | Yes |
| 26 | 19 Oct | External feedback on the manuscript was adopted with corrections. Discussion of Keen's theory was moved to §6.1, "Discussion beyond the pre-registered map", and worded in terms of intervals. The extensions are flagged as each needing its own preregistration. References were verified against publisher or RePEc records. | Yes |
| 27 | 19 Oct | Results release v2.0-results published (DOI 10.5281/zenodo.23479717). | Yes |
| 28 | 19 Oct | Red-team review adopted: new title, narrower claims, definitions, Appendices B–C, two references. Two review claims rebutted (the §5.3 arithmetic was correct; GS2 is in both BVAR variants). | Yes |
| 29 | 19 Oct | Second review. Post-lock checks: interval coverage simulation; P1a coefficient paths and largest losses (which **corrected** the draft's mechanism: the model forecast a rebound, not weakness); P2a training-start sensitivity. | Yes |
| 30 | 19 Oct | Coverage-calibrated intervals reported alongside the locked ones (Table 3b). The interval method was not switched; the locked rule still governs. | Yes |
| 31 | 19 Oct | Author-run cross-platform re-run on Windows with `verify_lock.py`: PASS (estimates match; hash differs by floating-point rounding). Not the independent check. | Yes |
| 32 | 19 Oct | Second independent agent check of 171 claims: 8 wording errors corrected; every estimate matched. | Yes |
| 33 | 20 Oct | Pandemic-period plan and script committed and tagged `pandemic-plan` (commit b9a7fc0) before any 2020 data were downloaded. | No |
| 34 | 20 Oct | March, June and September 2020 Z.1 releases downloaded, hashed, parsed with the locked parser; continuity checks passed. | No |
| 35 | 20 Oct | Pandemic-period run, once. All three tests "about as accurate" as the benchmark over eight targets. | Yes |
| 36 | 20 Oct | §5.6 written with the plan's pre-written sentences. **Declared deviation:** an explanatory note on one dominant unemployment forecast and on the mechanical pull of the extended ratios towards 1. | Yes |
| 37 | 20 Oct | Third review adopted: headline language ("no convincing average gain"; modest gains not ruled out), Table 3b relabelled a sensitivity analysis, training-vintage statement and timing example, narrower dataset label, Appendix D on inference and simulation. | Yes |
| 38 | 20 Oct | Release v2.1 published (DOI 10.5281/zenodo.23497087): revised paper, post-lock analyses, pandemic-period illustration and verification kit. | Yes |
| 39 | 20 Oct | Style rewrite of the paper (Strunk and White, Zinsser): first person, restructured §5–§6, shorter sentences. Locked passages, tables and numbers checked unchanged by script; an independent agent check found 11 meaning changes, all corrected. | Yes |
| 40 | 20 Oct | Box 1, "Terms used in this paper", added at the end of §1. | Yes |
| 41 | 20 Oct | Abstract and introduction revised after reader feedback; "about 50%" corrected to "52%" (S6 ratio 1.522). | Yes |
| 42 | 20 Oct | Style-sheet pass: positive form, estimates in place of hedging words, active voice. Uncertainty statements kept. | Yes |
| 43 | 20 Oct | The 10.6% GDP result given more prominence, with the caveat beside it; "gain" defined as a fall in forecast error. | Yes |
| 44 | 20 Oct | Claims bounded: "a sharp rebound that did not materialise"; the caveat placed beside every statement of the headline; the methods lesson scoped to one predictor path and one simulated process. | Yes |
| 45 | 20 Oct | Working paper v2.2 prepared for posting: 183-word abstract, title-page DOIs, PDF exported. | Yes |
| 46 | 20 Oct | Concrete-language pass: the abstract and §1 now open with the benchmark named and the answer "On the 1999–2019 evidence, no", with the 6% caveat in the same sentence; abstract phrasing replaced throughout. An independent agent check found 15 meaning changes, all corrected or reverted. | Yes |
| 47 | 20 Oct | Abstract power sentence reworded at the author's request (80% power only at a true RMSE ratio of about 0.6); Appendix A no longer states an entry count. | Yes |
| 48 | 20 Oct | Abstract rewritten as a plain-language summary: the RMSE ratio, interval and power jargon left to the body; the 6% caveat kept in the opening sentence. | Yes |
| 49 | 22 Oct | Opening answer clarified in the abstract and §1 (verdict, then best estimate with the 6% caveat); abstract split into three paragraphs. | Yes |
| 50 | 22 Oct | Motivation sentence added to the abstract (revised data, which no forecaster had); version date changed to 22 October 2026. | Yes |
| 51 | 22 Oct | The 6% caveat in the abstract and §1 now says a small benefit "lies at the edge of what the data allow"; "unlikely" not used, since the intervals do not support a probability statement. | Yes |
| 52 | 22 Oct | The abstract and §1 now give the GDP result as a best estimate plus a range (about 6% better to 44% worse); §1 adds a three-row table with the locked and widened intervals. | Yes |
| 53 | 22 Oct | The credit-to-GDP gap defined in plain words in §1, where Edge and Meisenzahl (2011) is cited. | Yes |
| 54 | 22 Oct | Edge and Meisenzahl sentence in §1 reworded: the gap defined in its own sentence, and the effect of revisions stated plainly ("on trend" can become "well above trend", or the reverse). | Yes |
| 55 | 22 Oct | Abstract reorganised: all results in the first paragraph; what was built and why in the second, with the long sentence split. | Yes |
| 56 | 22 Oct | Reader feedback: power and the 6% range reconciled in the abstract, §6 and §7; horizon convention stated in Box 1; gap described as a guide for countercyclical buffers; Barnichon–Nekarda reference completed. DOIs not added (could not be verified). | Yes |
| 57 | 22 Oct | Framing feedback: the methods lesson named as a case study of the methods actually tested; power and interval claims each qualified; the episode described precisely (variation in the crisis, losses in the recovery forecasts); the turning-point lesson recast as a hypothesis for future testing. | Yes |
| 58 | 22 Oct | Precision edits: the 6%–44% range labelled a post-lock sensitivity interval; horizon stated as quarter o + 4 in §1 and Box 1; SPF result named as the credit-corrected median SPF forecast (2.5% worse); methods scoped in the §1 contributions. | Yes |
| 59 | 22 Oct | Release v2.2 published (tag `v2.2-publish`, commit f2a5f39), archived at DOI 10.5281/zenodo.23560860. | Yes |

### TimesFM extension (plan `timesfm/PLAN.md`, tag `timesfm-plan`)

| Entry | Date (2026) | What | Results seen? |
|---|---|---|---|
| 62–65 | 26 Oct | Plan written and revised before freezing: checkpoints and package versions recorded; training-data check (TimesFM 2.5 High, TimesFM 3.0 Uncertain); credit alignment rules with a value-by-value self-test; numerical L1 flag (0.10 / 0.20, OR). The AR(2)'s own L1 values (0.995, 0.984) were computed by the pipeline test before freezing and are disclosed in the plan. | No |
| 66 | 26 Oct | Plan frozen: tag `timesfm-plan` on commit 7406c2c, 17:26:15 UTC; `PLAN_LOCK.json` committed (58fd7e2). | No |
| 67 | 26 Oct | First attempt (started 17:49:20 UTC) stopped while loading data (`openpyxl` missing), before any model was called; results folder empty. `openpyxl` 3.1.5 installed; other packages unchanged. | No |
| 68 | 26 Oct | Run 1 completed (18:05:43 UTC). **Defect:** with `return_backcast=True`, TimesFM 2.5's `forecast()` returns the backcast before the forecast, and the wrapper took the first five rows, so the GDP-only TimesFM 2.5 "forecasts" were backcast values. Invalid: F1, F4, the TimesFM 2.5 premium, its tail measures and its L1/L2. Valid: F2, F3, the TimesFM 3.0 premium and checks, and the TimesFM 2.5 forecasts with credit. Run 1 outputs kept (`results.json` 9960e6f8…). | Yes |
| 69 | 26 Oct | **Declared deviation.** The author chose to fix the defect and run once more (run 2), reporting both runs. Fix: `_pack` takes the last five rows; `forecast()` checks the output length; two new self-test checks (the forecast must respond to the end of the series; the 10th percentile must lie below the median). The fix is committed before run 2. Run 2's TimesFM 3.0 results must equal run 1's. | Yes |
| 70 | 26 Oct | Run 2 completed (18:35:41 UTC). Every column except the two GDP-only TimesFM 2.5 columns is bit-for-bit identical to run 1. No comparison shows a credible improvement (F1 1.015, F2 1.004, F3 1.018, F4 1.047); both premiums small; no L1 or L2 flag. Both models ran on the CPU (the torch build is CUDA 2.14.1+cu130, but `torch.cuda.is_available()` was False). Outputs in `timesfm/results/`; run 1 kept in `timesfm/results_run1_backcast_bug/`. | Yes |

No confirmatory analysis code, specification, sample or decision rule was changed after lock. Post-lock analyses (Entries 29–30, 33–36) use the locked code unchanged and are labelled as post-lock wherever they are reported.
