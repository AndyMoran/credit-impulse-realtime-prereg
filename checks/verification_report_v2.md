# Verification report v2: "Did the Credit Impulse Help Forecasters in Real Time?" (draft 19 Oct 2026)

Checker: an independent agent that did not see the drafting. Manuscript checked: `/home/claude/v2/md/manuscript_draft_2026-10-19.md`.
Ground truth: `p2/results_real/*` (results.json SHA-256 recomputed as 9e4239dd…a99c, which matches the paper), `p2/phase2.py`, `p2/post_lock/out/*`, `protocol_v2.3.md`, `bundle/.../data_derived/*`, the Gaussian power CSVs (`/mnt/attach/outputs/power2_results_R2000.csv`), `LOCK.json` and `v2/credit-impulse-v2.0-results/DEVIATIONS.md`.
Method: every number was recomputed in Python from the forecast CSVs, the coverage and calibration CSVs, the coefficient-path CSV, the revised impulse (`phase2.load('synthetic')`, `measures(Z['current'], NO[LATEST], P[LATEST]).CI`), and the revision and D2 files. The scratch scripts are in `/tmp/claude-0/-home-claude/e9f4fe62-515e-5367-a51c-8093aa4971b5/scratchpad/`.

## Summary count

| Verdict | Count |
| --- | --- |
| OK | 157 |
| Wrong (factual, internal inconsistency or unsupported) | 8 |
| Rounding / minor wording | 2 |
| Unverifiable from the files | 4 |
| **Total claims checked** (numbered items below; grouped rows count each number) | **171** |

Every confirmatory, grid, exploratory, Table 4, Table 5 and Table 3b number matches the locked or post-lock outputs. The errors are in a lead–lag statement, the labelling of P2b, the audit-log bookkeeping, one interpretive phrase about the pre-2008Q4 gain, and one sentence about raising the nominal level.

## Most important issues (ranked)

1. **§6.1, wrong forecast lead.** The text says: "a credit contraction predicted faster growth **four to six quarters later**". The credit lags are X at q\*−j with q\* = o − 2, j = 0..3, and the target is o + 4. The lead from impulse to target is therefore **6 to 9 quarters**: 6 for the latest lag, 9 for the oldest. The protocol's own power DGP describes it as "CI at lag 6". Correct the text to "six to nine quarters later".
2. **§5.4, P2b mislabelled.** The text says: "The SPF unemployment counterfactual (P2b, **a pre-registered secondary test**)". The protocol (§3 table, line 301) lists P2b as **Exploratory**, and the paper itself counts P2b among the 27 exploratory tests. It should be called "a pre-registered exploratory test".
3. **Intro item 2 (and, more softly, §6.1), interpretation not supported.** The text says: "a gain spread across 1999–2008 **rather than concentrated in the collapse**". Of the pre-2008Q4 gain of 30.2, 12.1 (40%) comes from 7 origins in 2007Q1–2008Q3. Two of those origins forecast the collapse quarters: 2007Q3 (target 2008Q3, outcome −2.1, gain +9.1) and 2008Q1 (target 2009Q1, outcome −4.5, gain +9.3). Together they give +18.4, partly offset by 2007Q4 (−7.1) and 2008Q3 (−4.5). The 1999–2006 origins contribute 18.2 over 30 origins. "Partly spread over the expansion, with 40% from seven origins around the collapse" is accurate. "Rather than concentrated in the collapse" overstates the point.
4. **§5.1, "Raising the nominal level does not cure this", overstated for GDP.** In `coverage_by_level.csv`, P1a coverage reaches 0.903 at the 97% level and 0.900 at the 97% level with an effect, and 0.94–0.96 at 99%. For GDP, raising the level does restore 90% coverage. It fails only for P1b (0.87 at 99%) and P2a (0.857). The script's own comment says this applies to P1b and P2a. Suggested wording: "does not cure this for unemployment or the SPF".
5. **Appendix A, log numbering inconsistent.** The text says "The full log (**Entries 1–29**)" but the post-lock checks cite "Entry 29" in the heading and "**Entries 29–30**" in the first row. The code agrees with the second: `calibrate.py` and `calibrated_intervals.py` are marked Entry 30, and `diagnostics.py` is Entry 29. The released `DEVIATIONS.md` (v2.0) contains Entries 21–26 only. Change the range to "Entries 1–30" and make the heading say "Entries 29–30".
6. **§5.3, coefficient range.** The text says: "between **−0.17** and −0.28 up to 2010". The recomputed range over origins up to 2010Q4 is **−0.165 (2000Q1) to −0.276**. That rounds to −0.16, not −0.17.
7. **Data availability, incomplete file list.** The text says the post-lock checks are "coverage.py, diagnostics.py and the Figure 7 script". Table 3b and the calibration also depend on `calibrate.py` and `calibrated_intervals.py`, so these should be listed too.
8. **Appendix C, wrong count for the file.** The text says: "The dated list of **all 83** Z.1 releases … is in `tables/z1_release_dates.csv`". That file has **95** rows (1996-09-12 to 2020-03-12), and 83 of them fall in the June 1999 to December 2019 range. Say that the file covers the 83 releases plus earlier and later ones.
9. **Figures: numbering, citation and labels.**
   - Figure 7 is first cited in §5.3, before Figures 5 and 6.
   - Figures 1, 2, 3 and 5 are never cited in the body text; they appear only as images.
   - Figure 5's printed title, "signals were **late** in both recessions", conflicts with §5.5, which calls the 2007Q4 episode "better described as coincident than late". §6 item 2 also says "late".
   - Image paths `../figures/fig1…fig6` do not resolve from `v2/md/`: only fig7 is in `v2/figures/`, and figs 1–6 are in `v2/credit-impulse-v2.0-results/figures/`.

Minor rounding notes:
- §5.3 says the model "edges ahead from 2000", but the cumulative gain is already positive at the first origin, 1999Q3 (+2.2).
- Appendix A says "full-sample GDP interval falls wholly below 1 in 1% of replications". The value is 0.7% in `coverage_*.csv` and 1.7% in `calib_*.csv`, so it is acceptable as "about 1–2%".

**Mechanism check (task item 4):** the credit model **over-forecast** GDP growth at every origin from 2010Q1 to 2011Q4. The forecast error fa − y ranges from +2.95 to +6.86 pp, with credit forecasts of 4.3–7.5% against outcomes of −0.9% to 4.6%. The paper's "forecast a strong rebound in 2011–12 that did not come" is therefore correct, and the old "kept forecasting weakness" wording has been removed everywhere except the Appendix A note that discloses the correction.

## Claim table

| # | Location | Claim | Recomputed | Verdict | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | Abstract | 83 dated releases June 1999–Dec 2019 | download_log: 83 + current; z1_release_dates 83 in range | OK | |
| 2 | Abstract | 78 forecast origins | 78 (1999Q3–2018Q4) | OK | |
| 3 | Abstract | DOI 10.5281/zenodo.23477871 | LOCK.json | OK | |
| 4 | Abstract | GDP RMSE +10.6%, ratio 1.106 (0.984–1.356) | 1.10647 (0.98367–1.35579) | OK | |
| 5 | Abstract | Unemployment 1.011 (0.994–1.043) | 1.01086 (0.99392–1.04322) | OK | |
| 6 | Abstract | SPF 1.025 (0.988–1.076) | 1.02456 (0.98833–1.07561) | OK | |
| 7 | Abstract | P3 0.111 (−0.047 to 0.269) | 0.11104 (−0.04717, 0.26926) | OK | |
| 8 | Abstract | Premium close to zero for both | +0.0005, +0.0081 | OK | |
| 9 | Abstract | ~4% better up to 2008Q3, ~50% worse from 2008Q4 | 0.959, 1.522 | OK | |
| 10 | Abstract | Losses: model forecast strong rebound 2011–12 | fa 5.4–7.5 vs y −0.9–4.6 at origins 2010–11; fa > y at all 8 | OK | direction confirmed |
| 11 | Abstract | ~three-quarters of variation from 2008–09 | 71.8% | OK | |
| 12 | Abstract | 80% power needs ~40% gain | Entry 19: ratio ≈0.6 | OK | |
| 13 | Abstract | Gaussian sim overstated power | 0.86/0.70/0.77 vs 0.45/0.31/0.51 | OK | |
| 14 | Abstract | Nominal 90% intervals cover 69–81% | calib: P1a .81/.807, P1b .75/.737, P2a .693/.77 | OK | |
| 15 | Abstract | Widened intervals allow gains up to ~6% | P1a 5.9% | OK | |
| 16 | §1 | Revised data also no gain | credrev ratio 1.1060 / 1.0027 | OK | |
| 17 | §1 item 1 | +10.6%, +1.1%, +2.5% | 1.1065, 1.0109, 1.0246 | OK | |
| 18 | §1 item 1 | None of four 90% intervals clears no-gain | all hi > 1; P3 lo < 0 | OK | |
| 19 | §1 item 2 | Pre-2008Q3 beats benchmark ~4% | 0.9594 | OK | |
| 20 | §1 item 2 | Gain "spread across 1999–2008 rather than concentrated in the collapse" | 18.2 of 30.2 from 1999–2006; 12.1 from 7 origins 2007Q1–08Q3, incl. +9.1 (2007Q3→2008Q3) and +9.3 (2008Q1→2009Q1) | Wrong (overstated) | Issue 3 |
| 21 | §1 item 2 | Such intervals arise ~5% of the time with no effect | 4.7% (kg=0, pre) | OK | |
| 22 | §1 item 2 | Post ~50% worse, almost entirely 2011–12 rebound forecasts | origins 2010Q1–11Q4: −135.6 of −139.2 post | OK | |
| 23 | §1 item 2 | Origins 2007Q1–2010Q4 = 68% of loss | 74.06/108.94 = 68.0% | OK | |
| 24 | §1 item 3 | Unemployment gains 2–8% in four specs | gap 7.8, RCG 2.2, contraction 4.3, E1 3.2 | OK | |
| 25 | §1 item 3 | BVAR 4.6% gain | 0.9539 | OK | |
| 26 | §1 item 3 | Nothing comparable for GDP | best GDP: BVAR 0.989 | OK | |
| 27 | §1 item 3 | ~30 comparisons | 27 tests / 32 comparisons | OK | approximate |
| 28 | §1 contribs | 83 Z.1 vintages 1999–2019 | 83 | OK | |
| 29 | §2 | E&M: revisions as large as the gap, mainly filter | protocol §1 | OK | literature |
| 30 | §2 | E1 overlapping 2000–2019 window | E1 origins from 2000Q1, n=76 | OK | |
| 31 | §3.1 | 83 releases 11 Jun 1999–12 Dec 2019 + current | download_log | OK | |
| 32 | §3.1 | Current release 11 Sep 2026, data to 2026Q2 | Entry 10 "Current (Sep 2026)" | OK | day not independently checked |
| 33 | §3.1 | June 1999 checked by hand vs printed tables | – | Unverifiable | Entries 2–3 not fully read |
| 34 | §3.1 | Earlier releases print last 4–5 years | protocol 278 | OK | |
| 35 | §3.1 | Code 154102005→154104005 in Sep 2010 | credit_vintages_long: old to 20100610, new from 20100917 | OK | |
| 36 | §3.1 | Units switch Mar 2011, ratio 1000.000; ≤ factor 2 after fix | Entry 10, parse_z1.py | OK | |
| 37 | §3.1 | CSV from Sep 2016; current renames tables | Entry 10 | OK | |
| 38 | §3.1 | corr(ΔL, F) 0.98 in Dec 2019 vintage | 0.982 | OK | |
| 39 | §3.1 | HP λ=400,000, ≥40 quarters | Entry 11 | OK | |
| 40 | §3.2 | Revised targets 2026Q3 vintage | protocol 358 | OK | |
| 41 | §3.2 | k = 2 at all 78 origins | origin_table all k=2 | OK | |
| 42 | §3.3 | 83 quarters 1999Q1–2019Q3 | n=83 | OK | |
| 43–47 | Table 1 CI row | +0.03, 0.95, 0.28, 0.96, 86% | 0.029, 0.946, 0.283, 0.960, 85.5% | OK | |
| 48 | Table 1 CG row | −0.19, 0.69, 0.18, 0.99, 98% | −0.187, 0.694, 0.183, 0.988, 97.6% | OK | |
| 49 | Table 1 RCG row | −0.30, 0.70, 0.21, 0.98, 95% | −0.295, 0.703, 0.211, 0.980, 95.2% | OK | total revision |
| 50 | Table 1 GAP row | −1.13, 1.32, 0.14, 0.99, 100% | −1.126, 1.323, 0.136, 0.993, 100% | OK | |
| 51 | Table 1 note | Credit-only noise/signal 0.28 ≈ total | 0.280 vs 0.283 | OK | |
| 52 | §3.3 | 2008Q3 first −7.5, today −5.2 | −7.487, −5.185 | OK | |
| 53 | §3.3 | 2006Q4 −0.27 vs +2.25 | −0.265, +2.248 | OK | |
| 54 | §3.3 D2 | Data 3%, filter 108%, cov −11% | 3.3%, 107.7%, −11.0% | OK | |
| 55 | §3.3 D2 | MAR 1.4 vs 7.0 pp | 1.40, 6.98 | OK | |
| 56 | §3.3 D2 | RT vs final corr 0.65, sign 76% | 0.650, 75.9% | OK | |
| 57 | §3.3 | Gap rose during 2001 recession | GAP_rt 4.5 (2001Q1) → 8.3 (2001Q4) | OK | |
| 58 | §4 | v2.3 protocol, v1.0-lock tag | LOCK.json | OK | |
| 59 | §4.1 | 78 origins 1999Q3–2018Q4, h=4; s ≥ 2020Q1 excluded | phase2.py | OK | |
| 60 | §4.1 | 2019Q4 endpoint in first draft; checklist "reported separately" | protocol lines 189, 191 | OK | |
| 61 | §4.1 | Premium sign: positive = revised better | phase2 prem = rt − credrev | OK | |
| 62 | §4.2 | Expanding window from 1965Q1 | phase2 start | OK | |
| 63 | §4.2 | P2a trained from 1990Q3; 32 pairs at first origin | min_pairs 32 | OK | |
| 64 | §4.2 | P3 83 quarters 1999Q2–2019Q4 | P3_forecasts s 7997–8079 | OK | |
| 65 | §4.3 | Fixed-b adopted because normal CVs over-rejected | Entries 12–13 | OK | |
| 66 | §4.3 | P3 fixed-b 14–18%, bootstrap 3.5% | Entry 18 | OK | |
| 67 | §4.3 | Block 4, 2,000 draws | BOOT_B, BOOT_BLOCK | OK | |
| 68 | §4.3 | Large premium rule ≥0.05 & CI excludes 0 | phase2 | OK | |
| 69 | §4.4 | 8 of 83 quarters hold 72% of squared deviations | 71.8% (revised CI 1999Q1–2019Q3) | OK | |
| 70 | Table 2 | Gaussian 0.86 / 0.70 / 0.77 | power2 unadj at 0.90: 0.857, 0.699, 0.767 (P2a own ratio 0.920) | OK | |
| 71 | Table 2 | Actual path 0.45 / 0.31 / 0.51 at 0.91/0.93/0.93 | Entry 18 | OK | |
| 72 | §4.4 | 80% power at ratio ~0.6 | Entry 19 | OK | |
| 73 | §4.4 | False improvement 0–2%; true 7% gain detected 29–40% | Entry 19: 0/2/2%; 32/29/40% at 0.92–0.94 | OK | |
| 74 | §5 | results.json SHA-256 | sha256sum match | OK | |
| 75–78 | Table 3 | All estimates/intervals; no credible improvement; no Holm rejection | results.json | OK | |
| 79 | Table 3 note | p 0.555, 0.618, 0.665, 0.221; fixed-b 0.036 | 0.5554, 0.6176, 0.66525, 0.2212, 0.0357 | OK | |
| 80 | §5.1 | Favourable ends = 1.6%, 1.2%, 0.6% gains | 1.63, 1.17, 0.61 | OK | |
| 81 | §5.1 | 300 replications | 300 per kg×test | OK | |
| 82 | §5.1 | Coverage 80–81% GDP, 74–75% U, 69–77% SPF | calib .807–.81, .737–.75, .693–.77 | OK | coverage.py full: .797–.803 |
| 83 | §5.1 | S6 halves 74–83% | pre .787–.827, post .743–.800 | OK | |
| 84 | §5.1 | Misses one-sided: below truth with no effect, above with effect | kg=0: hi<true 17–30% vs lo>true 1–3%; kg=.25: lo>true 14–16% vs hi<true 6–10% | OK | |
| 85 | §5.1 | "Raising the nominal level does not cure this" | P1a reaches 0.90 at 97%, 0.94–0.96 at 99% | Wrong (overstated) | Issue 4 |
| 86 | §5.1 | 99% intervals reach only 86–96% | 0.857–0.957 | OK | |
| 87 | §5.1 | Factors 1.35, 1.75, 2.1 | recomputed: P1a 1.35, P1b 1.75, P2a 2.1 | OK | |
| 88–90 | Table 3b | Calibrated 0.941–1.443, 0.981–1.067, 0.948–1.132 | 0.9407–1.4431, 0.9812–1.0675, 0.9485–1.1318 | OK | |
| 91 | Table 3b | Largest gains 5.9, 1.9, 5.2% | 5.93, 1.88, 5.15 | OK | |
| 92 | §5.1 | Gains up to ~6% GDP, 5% SPF, 2% U | as above | OK | |
| 93 | §5.2 | GDP 1.1065 → 1.1060 | 1.10647 → 1.10598 | OK | |
| 94 | §5.2 | U 1.011 → 1.003 | 1.0109 → 1.0027 | OK | |
| 95 | §5.2 | Total premiums +0.0005, +0.0075 | 0.00050, 0.00752 | OK | |
| 96 | §5.2 | Premium +0.0005 (−0.066, 0.037); +0.008 (−0.018, 0.024) | matches | OK | |
| 97 | §5.2 | Early-estimate 1.129, 1.011 | 1.1292, 1.0109 | OK | |
| 98–113 | Table 4 | All 15 cells + totals | recomputed from forecast CSVs, all match to 0.1 | OK | |
| 114 | §5.3 | Model edges ahead from 2000 | cumulative already +2.2 at 1999Q3 | Rounding | wording |
| 115 | §5.3 | Peak at 2008Q2 origin; held through 2009 | peak 34.8 at 2008Q2; 29.8–31.3 in 2009 | OK | |
| 116 | §5.3 | −135.6 over 2010Q1–2011Q4 | −135.64 | OK | |
| 117 | §5.3 | 74.1 of 108.9 (68%) | ✓ | OK | |
| 118 | §5.3 | S6 0.959 (0.896–0.982), 1.522 (1.148–1.863) | ✓ | OK | |
| 119 | §5.3 | S6 split reflects impulse definition (late 2008) | protocol S6 row | OK | |
| 120 | §5.3 | Pre-2008Q4 interval below 1 in 5% with no effect | 4.7% | OK | |
| 121 | §5.3 | Quarters to 2008Q1: 45% of sample, ~14% of squared deviations | 44.6%, 14.1% | OK | |
| 122 | §5.3 | Factor for the pre half is 1.35 | required factor 1.35 at kg 0, .15, .25 | OK | |
| 123 | §5.3 | Widened pre interval 0.874–0.990 | 0.8738–0.9905 | OK | |
| 124 | §5.3 | Widened pre interval wholly below 1 ~3% with no effect | 2.7% | OK | |
| 125 | §5.3 | 18.2 of 30.2; 2007Q1–2008Q3 add 12.1 | 18.16, 30.24, 12.08 | OK | |
| 126 | §5.3 | Coefficient sum negative throughout | max −0.075 | OK | |
| 127 | §5.3 | "between −0.17 and −0.28 up to 2010" | −0.165 to −0.276 | Rounding | Issue 6 (should read −0.16) |
| 128 | §5.3 | ~−0.10 by 2018 | −0.098 to −0.101 | OK | |
| 129 | §5.3 | 2010 origins: lag impulses −3 to −12; credit term 2.4–4.3; forecasts 5.4–7.5; outcomes −0.9 to 4.6 | −2.76 to −12.00; 2.37–4.25; 5.41–7.52; −0.95 to 4.57 | OK | |
| 130 | §5.3 | 2011 origins credit term 1.2–3.4; impulse turned positive | 1.18–3.35; lag0 +0.58 at 2011Q1 | OK | |
| 131 | §5.3 | Coefficients not reshaped; "bounce-back learned from earlier cycles" | sum −0.23 → −0.28 (mild); learning source not shown | Unverifiable | interpretation |
| 132 | §5.3 | U 2007–10 contribution +0.5 | +0.522 | OK | |
| 133 | §5.3 | SPF −23.2 of −26.5 from 1999–2006; +5.0 in 2010–11; 32–61 surveys | −23.24; +5.02; 32→61 | OK | |
| 134 | §5.3 | SPF training start: 68 common origins; 1.019, 1.130, 1.095 | p2a_training_start.csv | OK | |
| 135 | Table 5 | All six rows (impulse, sum, term, AR, credit, outcome, loss) | p1a_top_loss_origins.csv: all match | OK | 2011Q1 sum −0.2549 → −0.25 |
| 136 | Table 5 note | Six origins = 121 of 139 lost after 2008Q4 | 121.08 of 139.18 | OK | |
| 137 | §5.4 | 27 tests / 32 comparisons; four p < 0.05, all U | counted from results.json | OK | |
| 138 | §5.4 | P(≥4 of 27 at 0.05) = 0.044 | 0.0437 | OK | |
| 139 | Table 6 | All 22 entries | results.json all match to 3 dp | OK | |
| 140 | Table 6 note | p 0.002, 0.025, 0.002, 0.026; BVAR boot 0.078 | 0.0016, 0.0245, 0.0021, 0.0262, 0.0775 | OK | |
| 141 | §5.4 | Rolling 1.243 / 1.097 | ✓ | OK | |
| 142 | §5.4 | P2b 1.115 (p 0.147) | 1.1149, 0.1465 | OK | |
| 143 | §5.4 | P2b "a pre-registered secondary test" | protocol: Exploratory | Wrong | Issue 2 |
| 144 | §5.4 | Micro P2a 1.026; direction 66.2% → 64.9% | 1.0260; 0.6623 → 0.6494 | OK | |
| 145 | §5.5 | §10 written 17 Oct | protocol v2.3 header dated 17 Oct | Unverifiable | section-level date not separately logged |
| 146 | §5.5 | RT CI episodes start 2001Q4 (3 qtrs after peak) and 2007Q4 | D1 starts 8007 = 2001Q4, 8031 = 2007Q4 | OK | |
| 147 | §5.5 | Revised starts 2001Q3, 2009Q1 | 8006, 8036 | OK | |
| 148 | §5.5 | Two false alarms each; on 29% of RT quarters | 2 and 2; 0.295 | OK | |
| 149 | §5.5 | CG rule only false alarms, all from 2010 | RT 2010Q2, 2014Q2, 2018Q3; revised 2010Q1 | OK | |
| 150 | §5.5 / Fig 6 | 2009 quarters impulses −10 to −12; revisions both ways | CI −10.4 to −11.8; R +1.68, +0.30, −2.12, −1.34 | OK | |
| 151 | §6 | S5: contraction 0.957 U; asym 1.249 U; both worse GDP | 0.957, 1.249; 1.053, 1.055 | OK | |
| 152 | §6 item 4 | Gap 0.922; impulse U 1.011 | ✓ | OK | |
| 153 | §6 item 5 | R1 1.054, 1.056 | ✓ | OK | |
| 154 | §6.1 | Credit contraction predicted faster growth "four to six quarters later" | Lead is 6–9 quarters (q\*−j, q\* = o−2, target o+4) | Wrong | Issue 1 |
| 155 | §6.1 | 12.1 of 30.2 from 2007Q1–2008Q3 | ✓ | OK | |
| 156 | §7 | Modest pre-crisis gain wiped out by 2011–12 rebound forecast | ✓ | OK | |
| 157 | App A | S3 dropped 17 Oct (G3) | Entry 7 | OK | |
| 158 | App A | Power fixes (one lag, 1955, SPF, P3 controls) 19 Oct | Entry 16 | OK | |
| 159 | App A | Fixed-b; real-path power; wild bootstrap; crisis share; premium sign; E1; D1 seen | Entries 13, 17–19 | OK | |
| 160 | App A | Lock 14:55 UTC, commit 4eb084f, DOI | LOCK.json | OK | |
| 161 | App A | Run 15:00:47–15:01:25 UTC | DEVIATIONS Entry 22 | OK | |
| 162 | App A | "Full log (Entries 1–29)" vs "Entries 29–30" | scripts cite Entry 30; released log ends at 26 | Wrong (inconsistent) | Issue 5 |
| 163 | App A | Post-lock coverage row figures (80–81, 74–75, 69–77, 74–83; 1%, 5%; factors) | as rows 82–87, 120 | OK | 1%: 0.7% (coverage) / 1.7% (calib) |
| 164 | App A | Training-start row | ✓ | OK | |
| 165 | App A | Entries 27–30 part of the protocol record | not in released DEVIATIONS.md (to 26) | Unverifiable | |
| 166 | App B | E1 from 2000Q1; BVAR from 1976Q3 | E1 n=76 from 8000; Entry 17 | OK | |
| 167 | App C | "all 83 Z.1 releases" in z1_release_dates.csv | file has 95 rows (83 in range) | Wrong (minor) | Issue 8 |
| 168 | Data avail. | Post-lock scripts listed | omits calibrate.py, calibrated_intervals.py | Wrong (minor) | Issue 7 |
| 169 | Figures | Order of citation; captions; paths | Fig 7 cited before 5–6; Figs 1, 2, 3, 5 uncited; Fig 5 title "late" vs text "coincident"; ../figures has only fig7 | Wrong (consistency) | Issue 9 |
| 170 | Fig 7 | Annotation 2010Q3: 6.8% vs −0.1%; negative sum throughout | 6.77, −0.09 | OK | |
| 171 | Fig 4 | Totals −108.9/−1.9/−26.5; window −74.1/+0.5/−1.3; S6 values | ✓ | OK | |

Grouped rows (43–47, 75–78, 88–90, 98–113) cover several numbered claims each, all OK. Two minor rounding notes, the Appendix A "1%" and the 2011Q1 coefficient, are recorded inside OK rows.
