# Verification report: "Did Credit Help Forecasters in Real Time? A Preregistered Test, 1999–2019"

Manuscript: Claude Docs export rev 11, saved as /home/claude/check/manuscript.md (the references section is left out of the local copy because it is out of scope).
Sources: results.json (SHA-256 9e4239dd…, which matches the manuscript), the forecast CSVs, the Phase 1 outputs, the power files, protocol_v2.3.md (Entries 1–19), and the live protocol headings for Entries 20–24.
Recomputed: cumulative squared-error gains, the 2007Q1–2010Q4 share, the S6 split, k at every origin, sample lengths, D2 shares, real-path power by effect scale, the count of exploratory tests, and the concentration of impulse variance.

## 1. Claim table

| # | Location | Claim as written | Source value (file/key) | Status | Note |
|---|---|---|---|---|---|
| 1 | Abstract, §1, §3 | 83 dated Z.1 releases, June 1999 – Dec 2019 | download_log.csv: 83 dated rows (1999-06-11 … 2019-12-12) plus "current" | OK | |
| 2 | Abstract, §4.1 | 78 forecast origins, 1999Q3–2018Q4 | results.json core.P1a.n = 78; origin_table 7998–8075 | OK | |
| 3 | Abstract, §1, §5.1 | P1a ratio 1.106; 90% CI 0.984–1.356; "+10.6%" | 1.10647; [0.98367, 1.35579] | OK | |
| 4 | Abstract, §5.1 | P1b ratio 1.011 (0.994–1.043); "+1.1%" | 1.01086; [0.99392, 1.04322] | OK | |
| 5 | Abstract, §5.1 | P2a ratio 1.025 (0.988–1.076); "+2.5%" | 1.02456; [0.98833, 1.07561] | OK | |
| 6 | Abstract, §5.1 | P3 coefficient 0.111; 90% CI −0.047 to 0.269 | beta_CI 0.11104; ci90 [−0.04717, 0.26926] | OK | |
| 7 | §5.1 note | Unadjusted p = 0.555, 0.618, 0.665, 0.221 | 0.5554, 0.6176, 0.66525, 0.22122 | OK | |
| 8 | §5.1 note | P3 fixed-b HAC p = 0.036 | p_fixedb_hac 0.0357 | OK | |
| 9 | §5.1 table | Credible improvement No ×4; Holm reject No ×4 | credible_* false; holm_reject false | OK | |
| 10 | §1 | "None of the four 90% intervals clears no-gain" | all ratio CIs contain 1; the P3 CI contains 0 | OK | |
| 11 | §5.1 | "at most about 2% (GDP), 1% (SPF), 0.6% (unemployment)" | 1−0.9837 = 1.6%; 1−0.9883 = 1.2%; 1−0.9939 = 0.6% | OK | |
| 12 | §5.2 | Revised-credit GDP ratio "unchanged at 1.106"; unemployment 1.011 → 1.003 | grid.g.totrev_revised 1.10597; grid.u.totrev_revised 1.00334 | OK | The 1.003 is the total-revision cell. The +0.008 premium uses the credit-only cell (1.0027), which also rounds to 1.003. |
| 13 | Abstract, §1, §5.2 | Premium +0.0005 (−0.066 to 0.037) for GDP; +0.008 (−0.018 to 0.024) for unemployment; both "small" | 0.000487 [−0.0658, 0.0374]; 0.00814 [−0.0176, 0.0236]; premium_size "small" | OK | |
| 14 | §5.2 | Early-estimate ratios 1.129 (GDP), 1.011 (unemployment) | rt_early 1.12915; 1.01086 | OK | |
| 15 | §5.3 | Total cumulative loss 108.9; 2007Q1–2010Q4 origins contribute 74.1 (68%) | Recomputed: −108.937; −74.060; 0.6798 (matches crisis_share) | OK | |
| 16 | Abstract, §1, §5.3 | Pre-2008Q4 split 0.959 (0.896–0.982), "about 4%"; post 1.522 (1.148–1.863), "about 50%" | S6_pre_g 0.9594 [0.8960, 0.9824]; S6_post_g 1.5223 [1.1481, 1.8626]; recomputed with 37 and 41 origins | OK | |
| 17 | §1 (finding 2), Abstract, §5.3 | Pre-2008Q4 gain came "largely by anticipating the collapse" / "catching the collapse" / "Credit anticipated the collapse" | Pre-2008Q4 gain = 30.24. Origins 1999Q3–2006Q4 give 18.16 (60%) at ratio 0.917. Origins 2007Q1–2008Q3 give 12.08 (40%) at ratio 0.977. The worst collapse quarter (target 2008Q4, y = −8.5) was a loss of −7.07. | WRONG | Most of the pre-split gain is a steady small gain over 1999–2006, not the collapse. |
| 18 | Abstract, §1, §5.3 | "the impulse stayed negative through the recovery" / "credit stayed deeply negative while output recovered" | P3_forecasts CI (real-time): data quarters 2008Q3–2010Q3 negative (min −11.8 in 2009Q2), 2010Q4 +0.6, 2011 +3 to +5. Losses fall at origins 2010Q1–2011Q4, where the model's four lags still held negative values. | WRONG (overstated) | The impulse turned positive from data quarter 2010Q4. The loss comes from lagged negative values held in the model. |
| 19 | §5.3 | "edges ahead from 2000 until forecasts made in late 2009, then loses heavily on forecasts of the 2010–12 recovery" | Cumulative gain rises from 1999Q3 and peaks at the 2008Q2 origin (34.8). It is flat at about 30–31 to 2009Q4, then falls: 2010Q1 −26.1, 2010Q3 −37.6, and through 2011Q4. Targets of the losing forecasts are 2011Q1–2012Q4. | WRONG (dating) | The gains end at 2008Q2 origins, not late 2009, and the losses fall on 2011–12 targets. 2010 targets show net ≈ 0. |
| 20 | §5.3 | SPF correction "loses from the start (total −26.5, of which −1.3 from 2007–10)" | First origin −4.8; total −26.515; window −1.333 | OK | |
| 21 | §5.3 | Unemployment "Neither shows a sustained gain at any point" | P1b cumulative is positive 2008Q1 and 2009Q1–2010Q3 (≤ +0.5); 2007–10 window gain +0.52 | OK | Marginal: the unemployment window gain is positive but negligible. |
| 22 | §1, §3.2, §4.1 | k = 2 at every origin; no targets beyond 2019Q4 | origin_table k = 2.0 ×78; max s = 8079 (2019Q4) | OK | |
| 23 | §4.2 | 32 training pairs at the first origin; SPF training from 1990Q3 | P2a_forecasts n_train = 32 at o = 7998; protocol §8 | OK | |
| 24 | §4.2 | P3: 83 quarters, 1999Q2–2019Q4 | P3_forecasts 83 rows, s 7997–8079; core.P3.n = 83 | OK | |
| 25 | §4.2 | Expanding window from 1965Q1 | protocol §8 | OK | |
| 26 | §4.3 | P3 fixed-b over-rejects 14–18%; bootstrap 3.5% | Entry 18 | OK | |
| 27 | §4.3 | Block bootstrap, block 4, 2,000 draws | phase2.py BOOT_B, BOOT_BLOCK = 2000, 4 | OK | |
| 28 | §4.3 | Large premium: at least 0.05 and the CI excludes 0 | protocol §4a | OK | |
| 29 | §4.4 Table 2 | Gaussian-path unadjusted power 0.86 / 0.70 / 0.77 | power2_results_R2000.csv, row 0.90: 0.857 / 0.699 / 0.767 | OK | The P2a cell is at P2a's own ratio of 0.92 (spf_ratio_at_kg 0.920), not 0.90; at its own 0.90 it is about 0.85. Footnote this. |
| 30 | §4.4 Table 2 | Actual-path power 0.45 / 0.31 / 0.51 at ratios 0.91 / 0.93 / 0.93 | power_realpath.csv kg = 0.35: share p < 0.05 = 0.445 / 0.305 / 0.510; median ratios 0.907 / 0.934 / 0.929 | OK | |
| 31 | §4.4, §6 | 80% power needs a ratio of about 0.6 (gain of roughly 40%) | Entry 19 (0.57 at 0.82, 0.87 at 0.52) | OK | This is extrapolated beyond power_realpath.csv, whose grid ends at 0.82. |
| 32 | §4.4 | False improvement 0–2%; a true 7% gain detected 30–40% of the time | Entry 19: 0 / 2 / 2%; 32 / 29 / 40% at true ratios 0.92–0.94 | ROUNDING | The range is 29–40%. The ci_check output is not among the locked files. |
| 33 | Abstract, §1, §4.4 | "almost all of the impulse's variation comes from one episode" | Revised CI 1999Q1–2019Q3: 2008–09 holds 72% of squared deviations (8 of 83 quarters); 2008–10 holds 75% | WRONG (overstated) | "About three-quarters" is accurate. The protocol uses the same phrase, but the data do not support "almost all". |
| 34 | §3.3 Table 1 | CI +0.03 / 0.95 / 0.28 / 0.96 / 86% | revision_stats CI total: 0.0292 / 0.9456 / 0.2829 / 0.9595 / 0.8554 | OK | |
| 35 | Table 1 | CG −0.19 / 0.69 / 0.18 / 0.99 / 98% | −0.1874 / 0.6940 / 0.1826 / 0.9877 / 0.9759 | OK | |
| 36 | Table 1 | RCG −0.30 / 0.70 / 0.21 / 0.98 / 95% | −0.2951 / 0.7035 / 0.2109 / 0.9796 / 0.9518 | OK | |
| 37 | Table 1 | Gap (data only) −1.13 / 1.32 / 0.14 / 0.99 / 100% | GAP total: −1.1264 / 1.3230 / 0.1356 / 0.9926 / 1.0 | OK | |
| 38 | Table 1 | 83 quarters, 1999Q1–2019Q3 | first_release_vs_revised.csv 83 rows | OK | |
| 39 | Table 1 note | Credit-only noise/signal 0.28 = total | 0.2801 vs 0.2829 | OK | |
| 40 | §3.3 | 2008Q3 first −7.5 vs −5.2 today; 2006Q4 −0.27 vs +2.25 | CI_rt −7.487 / CI_rev −5.185; −0.2653 / +2.2481 | OK | |
| 41 | §3.3 | Largest revisions at turning points | Top absolute revisions: 2009Q3, 2006Q4, 2008Q3, 2001Q1 | OK | |
| 42 | §3.3 | D2 shares: data 3%, filter 108%, covariance −11% | Recomputed: 3.3%, 107.7%, −11.0% | OK | |
| 43 | §3.3 | Mean absolute revision 1.4 pp (data) vs 7.0 pp (filter) | 1.399; 6.982 | OK | |
| 44 | §3.3 | Real-time vs final gap corr 0.65; same sign in 76% of quarters | GAP_final: 0.650; 75.9% | OK | The 2026-end filter gives 0.60 / 74.7%; the manuscript uses the 2019 final, which is fine. |
| 45 | §3.3 | Gap rose during the 2001 recession | GAP_rt 4.50 (2001Q1) → 8.31 (2001Q4) | OK | |
| 46 | §3.1 | Household code 154102005 → 154104005 in the Sep 2010 release | Entry 4 | OK | |
| 47 | §3.1 | Units switch in the Mar 2011 release; median ratio exactly 1000.000 | Entry 10 | OK | |
| 48 | §3.1 | CSV replaced fixed-width files in Sep 2016; current release renames the tables | Entry 10 | OK | |
| 49 | §3.1 | "Three documented breaks" vs "An undocumented units switch" | — | WRONG (wording) | Self-contradictory. Suggest "three breaks, documented here". |
| 50 | §3.1 | Levels track flows, corr 0.98 (Dec 2019 vintage) | Entry 11 | OK | |
| 51 | §3.1 | Current release 11 September 2026, data to 2026Q2 | download_log has only "current"; Entry 10 says "Current (Sep 2026)" | UNVERIFIABLE | The day and the end quarter are not in the files. |
| 52 | §3.1 | Earlier releases print only the last four to five years | Entry 1 table (~4.5 to ~5 years) | OK | |
| 53 | §3.1 | Flows are SAAR "divided by 4" | Not found in protocol entries | UNVERIFIABLE | Check build.py. |
| 54 | §3.1 | Every release date verified against the archive | Entries 8–9 (one date corrected) | OK | |
| 55 | §3.2 | 15th of middle month; revised targets 2026Q3 vintage; early estimate s+2; drgdp6 / UNEMP6; GS2 only in BVAR | protocol §5, §8, Entries 13, 15, 17 | OK | |
| 56 | §5.4 | "about 30 comparisons" | 27 exploratory tests with p-values (32 entries including S6 and direction) | OK | |
| 57 | §5.4 Table 4 | All 22 exploratory ratios (S2 ×8, S5 ×4, S4 ×2, E1, R1 ×4, rolling ×2, h1/h2 ×4) | results.json exploratory (e.g. GAP_u 0.92247, rolling60_g 1.24255, R1_Z_u 0.99974) | OK | Every value rounds correctly. |
| 58 | Table 4 note | p-values: gap 0.002, RCG 0.025, contraction 0.002, E1 0.026 | 0.0016, 0.02455, 0.0021, 0.0262 | OK | |
| 59 | Table 4 note | BVAR bootstrap p = 0.077 | S4_u p_boot 0.0775 | ROUNDING | Half-up rounding gives 0.078. |
| 60 | Table 4 note | p < 0.05 "only for unemployment" | All GDP exploratory p ≥ 0.18 (S4_g p_boot 0.447) | OK | |
| 61 | §1, §5.4, §6 | Unemployment gains 2–8% "across five specifications" | gap 7.8%, RCG 2.2%, contraction 4.3%, E1 3.2%, BVAR 4.6% | OK | §6 item 3 lists only four of the five (omits the contraction model). |
| 62 | §1, §5.4, §6 | Attributed to "slower-moving credit measures" / "slower-moving stock measures", BVAR included | phase2.py run_s4: the BVAR's credit variable is CI_{t−2}, the impulse | WRONG | The BVAR uses the fast-moving impulse, not a stock measure. |
| 63 | §1 | "a contraction-asymmetric model" | Table 4: "S5 real-credit contraction model" (0.957); the S5 asymmetric impulse worsens unemployment (1.249) | WRONG (label) | The label could be read as the asymmetric-impulse model. Use "the real-credit contraction model". |
| 64 | §1 | "None of these appears for GDP" | GDP: gap 1.102, RCG 1.030, contraction 1.055, BVAR 0.989 (1.1% gain, p = 0.45) | OK | Literally true for 2–8% gains. Mention the BVAR's 0.989. |
| 65 | §5.4 | P2b 1.115; P2a micro 1.026; direction 66.2% → 64.9% | 1.11493; 1.02597; 0.66234 / 0.64935 (n = 77) | OK | |
| 66 | §5.5 | Impulse rule late at the 2001 and 2007 peaks in real-time and revised data; on 29% of quarters | D1 rt_sig_ci episodes 8007 (2001Q4) and 8031 (2007Q4), both "late"; totrev 8006 and 8036 "late"; share 0.2949 | OK | The impulse rule also had false alarms (rt 2005Q1, 2017Q3–2018Q1; revised 2003Q1–Q3, 2017Q2–2018Q1), which are not mentioned. |
| 67 | §5.5 | Credit-growth rule: only false alarms, all from 2010 on | rt starts 8041, 8057, 8074; revised starts 8040 | OK | |
| 68 | §5.5 | 2009 P3 quarters: impulse −10 to −12; revisions in both directions | s 2009Q1–Q4: CI −10.65, −11.79, −11.25, −10.36; R +1.68, +0.30, −2.12, −1.34 | OK | |
| 69 | §6 | Headline sentence and S5 reading; values 0.957 / 1.249; both worsen GDP (1.053, 1.055) | protocol §4a cell; live Entry 23 | OK | |
| 70 | §5 | results.json SHA-256 9e4239dd… | sha256sum 9e4239dd116e… | OK | |
| 71 | App. A, Data | v1.0-lock, commit 4eb084f, DOI 10.5281/zenodo.23477871, 19 Oct | LOCK.json | OK | |
| 72 | App. A | Rows 1–5 and 8 (power-spec errors, fixed-b, conditional-path power, sign, D1 seen, S5) | Entries 12–13, 16, 17, 18–19, 23 | OK | |
| 73 | App. A | "Phase 2 run once; no deviations"; full log is Entries 1–24 | Live protocol Entries 21–24 headings | OK | |
| 74 | §1, App. A | "Appendix A lists all deviations" / every change logged | Entry 7 (17 Oct): S3 dropped after G3 failed. Not in the appendix, which lists only 19 Oct rows. | WRONG (omission) | Add a 17 Oct row for S3. |
| 75 | §1 | Locked "the wording of every possible conclusion" | §6: "The protocol did not define 'supported' for S5" | WRONG (internal) | Soften to "the wording of the headline conclusions". |
| 76 | §6 | "The 2001 recession was not a credit recession" | — | UNVERIFIABLE | Interpretive. |
| 77 | §4.4 | Impulse "quiet for most of 1999–2019, swings violently in 2008–09" | Consistent with row 33 | OK | |

## 2. WRONG and ROUNDING items: suggested corrections

1. **Row 17 (finding 2, abstract, §5.3).** Replace "largely by anticipating the collapse" / "catching the collapse" with: "The gain is spread across the period. About 60% accrued over 1999–2006, and forecasts made in 2007Q1–2008Q3 added the rest with mixed results (a large miss on 2008Q4)."
2. **Row 18.** Replace "the impulse stayed negative through the recovery" with: "the impulse was deeply negative through 2010Q3, and the model's lags carried those readings into forecasts of 2011–12."
3. **Row 19.** Replace with: "The credit model edges ahead from the first origins until mid-2008, holds that lead through forecasts made in 2009, then loses heavily on forecasts made in 2010–11 for the 2011–12 recovery."
4. **Row 33.** Replace "almost all" with "about three-quarters (2008–09 accounts for 72% of the impulse's squared deviations in 8 of 83 quarters)". The same fix applies in the abstract, §1 and §4.4.
5. **Row 62.** Drop the BVAR from "slower-moving credit measures", or say "slower-moving credit measures and the BVAR". Also fix §6 item 3.
6. **Row 63.** Change "a contraction-asymmetric model" to "the real-credit contraction model".
7. **Row 49.** Change "Three documented breaks" to "Three breaks, documented below,".
8. **Row 74.** Add an Appendix A row: "17 Oct | S3 (GDI revisions) dropped: G3 failed, no real-time GDI before 2012 (Entry 7) | No".
9. **Row 75.** Change "the wording of every possible conclusion" to "the wording of the headline conclusions".
10. **Row 32 (ROUNDING).** Change "30–40%" to "29–40%" (or "about 30–40%").
11. **Row 59 (ROUNDING).** Change 0.077 to 0.078.
12. **Row 29 (footnote only).** Add to the Table 2 note: "Gaussian P2a cell at P2a's own ratio of 0.92."

## 3. Overall verdict

The quantitative core is accurate. Every confirmatory estimate, interval, p-value, grid cell, premium, exploratory ratio, revision statistic, D2 share, power figure, count (83 / 78 / 83 / 32, k = 2) and cumulative total (108.9, 74.1, 68%, −26.5, −1.3) matches the locked files and rounds correctly, with two minor exceptions (0.077 → 0.078; 30–40% → 29–40%). The problems are in the narrative about the crisis.

- **The pre-2008Q4 gain:** it did not come "largely" from anticipating the collapse. Most of it accrued steadily over 1999–2006, and the model missed the 2008Q4 collapse quarter.
- **The impulse during the recovery:** it did not stay negative "through the recovery". It turned positive from data quarter 2010Q4.
- **Timing in §5.3:** the GDP lead peaks in mid-2008, not late 2009, and the losses fall on 2011–12 targets.
- **Variance concentration:** "almost all" overstates it; the share is about three-quarters.

There are also smaller labelling and consistency faults: the BVAR is described as a slower-moving measure, the "contraction-asymmetric" label is ambiguous, "three documented breaks" contradicts "undocumented", the S3 deviation is missing from Appendix A, and the "every possible conclusion" claim conflicts with §6. None of these changes the null headline or the preregistered reading, but the abstract and finding 2 should be reworded before circulation.
