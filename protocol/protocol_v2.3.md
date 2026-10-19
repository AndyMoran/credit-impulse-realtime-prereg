# Real-Time Credit Impulse Project: Red-Team Review & Preregistration Protocol

Oct 17, 2026 · @Andy

**Decision, 17 Oct 2026:** scope narrowed to one question: *did US private credit flows carry information about output and unemployment that a forecaster could have used at the time, 1990–2019?* The DSGE horse race is dropped because it has already been run on real-time data (Edge–Gürkaynak; Del Negro–Schorfheide; Wieland–Wolters). Protocol v2.3 below replaces all earlier versions. The red-team findings stay as the rationale.

## Summary verdict

The plan is sound in spirit but not yet lockable: five design flaws would let the results say more than the data can support. The factual premises check out; the framing of what is being tested does not.

**What holds**

- The 2026 prize to Robert E. Hall and Michael Woodford "for microeconomic foundations of macroeconomic stabilisation" is confirmed (announced 12 October 2026).
- NBER WP 35875 (Freeman, Xie, Zhang & Zhou) exists and says what the plan says it says.
- Real-time US data for GDP, inflation, unemployment and the policy rate exist and are well documented.
- The "simplest model first" ladder is good practice and matches the forecasting literature's own benchmarks.

**What breaks (must fix before lock)**

1. **Construct validity.** The prize claims better *policy design*, not better *forecasts*. Forecast accuracy is a fair but partial test. H1 must be restated as a forecasting claim, not a verdict on the prize.
2. **The 2007–09 window is the discovery sample for H2.** The "credit impulse" was coined in November 2008 and Keen's "credit accelerator" was named around 2010–11. Testing them on the crisis that inspired them is in-sample, however careful the vintages.
3. **Credit data were not available in this form in real time.** The BIS total-credit series launched in March 2013 and is break-adjusted ex post. A real-time credit series must be rebuilt from archived Z.1 releases.
4. **The decision gate makes H1 untestable.** DSGE (Level 3) is reached only if credit-augmented models win. If they lose, H1 is never tested. Use published real-time DSGE forecasts as an unconditional comparator instead.
5. **No statistical power on the primary window.** About 12–16 forecast origins and 3–4 recessions cannot support significance claims. Turning-point results must be pre-declared as descriptive.

**Biggest single change:** make the full 1990–2019 real-time evaluation the confirmatory test, treat named crisis windows as pre-specified subsets, and treat 2007–09 as exploratory for H2.

## Premise verification

All three factual premises are confirmed, but premise 1 needs re-wording so the project tests what the prize actually claims.

| Premise in draft | Status | What the record shows | Change needed |
| --- | --- | --- | --- |
| 2026 Nobel to Hall and Woodford for "microeconomic foundations of macroeconomic stabilisation" | Confirmed | Announced 12 Oct 2026 by the Royal Swedish Academy ([press release](https://nobelprize.org/prizes/economic-sciences/2026/press-release)). Committee says their models improved our ability to implement stabilisation policy and underpin models used by central banks. | Quote the citation exactly. Read the Academy's scientific background PDF before lock and list which specific papers it credits. |
| Prize ratifies "the NK/DSGE paradigm" | Partly | The prize credits two people's work, not the Smets–Wouters model. Hall's record is broad: his 1978 consumption paper implies a random-walk benchmark; he chaired the NBER Business Cycle Dating Committee for 30+ years ([NBER](https://www.nber.org/news/robert-hall-and-michael-woodford-awarded-2026-nobel-prize)). Woodford's *Interest and Prices* (2003) is the NK core ([PUP](https://press.princeton.edu/node/71367)). | Call it "the NK/DSGE model class descended from this work". Do not attribute Smets–Wouters results to the laureates personally. |
| NBER WP 35875 documents high and rising concentration | Confirmed | Economics is the only one of 18 fields where prizewinner concentration is rising ([NBER w35875](https://www.nber.org/papers/w35875)). | Keep as motivation only. It is evidence about sociology of prizes, not about model accuracy; say so. |
| Keen as source of testable debt hypotheses | Confirmed, with caveat | Keen defines the credit accelerator as the change in the change in debt over a year, divided by GDP, and credits Biggs et al. for the idea ([Keen 2011](https://nakedcapitalism.com/2011/06/steve-keen-dude-where’s-my-recovery.html)). | Cite Biggs, Mayer & Pick (2010) as the operational source; Keen as the theoretical motivation. |

**Construct-validity note.** Forecast accuracy is not the prize's stated contribution. Edge and Gürkaynak argue that, under good monetary policy, a correct NK model itself predicts that inflation deviations are hard to forecast ([FEDS 2011-11](https://www.federalreserve.gov/econres/feds/how-useful-are-estimated-dsge-model-forecasts.htm)). So a DSGE that forecasts no better than a random walk is not, by itself, a refutation. The protocol should say this up front, then test anyway: forecasting at turning points is still a necessary condition for policy usefulness in real time.

**Conflict-of-definition note.** Recession dates come from the NBER committee Hall chaired. This is not bias, but turning-point scoring must use dates *as announced*, and announcement lags (about a year) mean those dates were never available to a real-time forecaster.

## Red-team findings

Each finding names the flaw, why it matters, and the fix written into the protocol below. Severity: **Critical** = would invalidate a headline claim; **Major** = would bias a comparison; **Minor** = reporting hygiene.

### 1. Forecast target definitions (Major)

- **Undefined growth concept.** "Real GDP growth at h=4" can mean the single quarter four steps ahead (q/q annualised) or cumulative growth over four quarters. They have very different error variances and different winners. *Fix:* primary = q/q annualised at h = 1, 2, 4; secondary = cumulative 4-quarter growth.
- **Undefined "truth".** GDP is revised for years; the 2009 and 2013 comprehensive revisions moved history materially. *Fix:* primary actual = the estimate in the vintage published two quarters after the target quarter ("second-ish release"); robustness = first release and latest vintage. Never mix.
- **Unemployment level vs change.** A random walk in levels is nearly unbeatable at h=1. *Fix:* forecast the quarterly-average level; score RMSE on the level and directional accuracy on the change.
- **Inflation measure unstated.** *Fix:* GDP deflator (matches the DSGE literature's observable), q/q annualised.
- **Turning-point metric undefined.** *Fix:* a pre-written rule, e.g. a model "calls" a recession when its forecast path has two consecutive negative q/q growth quarters or a +0.5 pp rise in unemployment within 4 quarters. Score hits, misses, false alarms and lead time.

### 2. Real-time vintages (Critical)

- **Credit is the weak link.** The BIS total-credit database was introduced in March 2013 ([BIS QR](https://bis.org/publ/qtrpdf/r_qt1303h.htm)) and its US series is break-adjusted with BIS's own statistical techniques ([FRED notes](https://fred.stlouisfed.org/graph/?g=BwH3)). Neither existed in 2007. *Fix:* build real-time credit from archived Z.1 releases (Fed release archive and FRASER); use BIS only as a final-vintage robustness check.
- **ALFRED coverage of Z.1 looks thin before 2013.** ALFRED vintages for at least some Z.1 series begin in June 2013 ([ALFRED Z.1 search](https://alfred.stlouisfed.org/search?st=z1)). *Fix:* a data-audit step before lock confirms, series by series, the earliest usable vintage; anything missing is reconstructed or the variable is dropped.
- **Release timing.** Z.1 lags quarter-end by about 10 weeks, longer than the GDP advance estimate. *Fix:* the information set at each origin is defined by publication date, not by reference quarter. A ragged edge is allowed and documented.
- **Policy rate at the zero lower bound.** From December 2008 the fed funds rate stops carrying information, which breaks linear VARs. Shadow rates (e.g. Wu–Xia) are estimated ex post and leak. *Fix:* replace fed funds with the 2-year Treasury yield, available unrevised in real time.

### 3. Crisis-window leakage (Critical)

Leakage here is anything known after a forecast origin that shapes the forecast. Six channels exist:

1. **Hypothesis leakage.** The credit impulse was introduced in a Deutsche Bank note of 19 Nov 2008 ([CASE](https://case-research.eu/en/case-starts-to-publish-a-quarterly-update-on-credit-impulse-100774)); Keen renamed it in 2011. Both were shaped by watching 2008.
2. **Model-choice leakage.** DSGEs with financial frictions were adopted *because* of the crisis; Del Negro, Hasegawa and Schorfheide note macroeconomists paid little attention to them beforehand ([NY Fed SR 695](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr695.pdf)).
3. **Data-construction leakage.** Break adjustment, HP-filtered credit gaps and seasonal factors are computed using later data.
4. **Hyperparameter leakage.** BVAR prior tightness, lag length or rolling-window length tuned on the full sample.
5. **Date leakage.** NBER peak/trough dates used to define windows or to time a forecast.
6. **Researcher leakage.** The analyst knows the outcome. Every specification choice is a potential forking path.

*Fix:* all specifications frozen before any forecast is computed; hashes recorded; 2007–09 labelled exploratory for H2; confirmatory H2 evidence must come from 1990–91, 2001, and the non-recession years; one-sided filters only; window boundaries set by calendar, not NBER dates.

### 4. Model comparability (Major)

- **Unequal information sets.** Smets–Wouters uses seven observables; Level 1A uses four. A DSGE "win" may just be more data. *Fix:* report a BVAR on the same seven observables as the DSGE's fair benchmark.
- **Nested models.** 1B nests 1A. The Diebold–Mariano test is invalid for nested comparisons. *Fix:* Clark–West test for 1A vs 1B.
- **Estimation scheme.** *Fix:* expanding window from 1965Q1 for all models, re-estimated at every origin, with a fixed-length rolling window (60 quarters) as robustness.
- **Multi-step method.** *Fix:* iterated forecasts for VAR/AR; direct forecasts as robustness.
- **Trailing mean unspecified ("8 or 12").** *Fix:* lock 8 quarters; 12 as robustness.
- **Do not build your own DSGE first.** Real-time SW and SW-with-financial-frictions forecasts already exist ([Del Negro & Schorfheide 2013](https://econpapers.repec.org/RePEc:fip:fednsr:554); [Cai et al.](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr844.pdf)) and Wieland–Wolters published real-time model forecasts around five NBER recessions using the Macroeconomic Model Data Base ([Wieland & Wolters](https://publikationen.ub.uni-frankfurt.de/opus4/frontdoor/index/index/year/2010/docId/7902)). Use these as the Level 3 comparator; replicate one only if the archive allows exact alignment.
- **Missing professional benchmarks.** SPF and Greenbook forecasts are the natural human comparators and are already used in this literature. *Fix:* add both as reference rows (not competitors to be beaten).

### 5. Credit impulse construction (Major)

The draft names "credit impulse" but not its formula. Small definitional choices change the series sign around turning points.

- **Canonical definition.** Biggs, Mayer & Pick: the change in the *flow* of credit relative to GDP ([VoxEU](https://cepr.org/voxeu/columns/myth-phoenix-miracle)). Lock it as:

```latex
CI_t = \frac{(D_t - D_{t-4}) - (D_{t-4} - D_{t-8})}{\sum_{j=0}^{3} Y_{t-j}} \times 100
```

where D is end-quarter private non-financial credit and Y is nominal GDP (quarterly, not annualised), both from the same vintage.

- **Levels vs flows.** Z.1 level differences include reclassifications and valuation breaks; Z.1 flow tables exclude them. *Fix:* primary = sum of Z.1 seasonally adjusted flows; robustness = level differences.
- **Revision amplification.** A double difference amplifies revision noise. *Fix:* report the revision variance of CI (first vs latest vintage) before any forecasting.
- **Credit-to-GDP gap.** If used, one-sided HP filter only (BIS uses λ = 400,000). Two-sided filtering is leakage.
- **Quarterly vs annual impulse.** *Fix:* lock the 4-quarter version above; the quarterly double difference is robustness only.
- **Sector scope.** *Fix:* households + non-financial business (Z.1 domestic non-financial excluding government).

### 6. Sample size and power (Critical)

- **Primary window too small.** 2007Q1–2010Q4 gives 16 origins; at h=4 the overlapping errors leave roughly 4 independent observations. No test has useful power at that size.
- **Turning points are rare.** 1990–2019 holds three US recessions. Hit-rate comparisons on n=3 are anecdotes.
- **Multiple comparisons.** Roughly 10 models × 3 horizons × 3 targets × 4 metrics × 3 windows = 1,080 cells.
- *Fix:* (a) confirmatory sample = all origins 1990Q1–2019Q4 (120 origins); (b) two pre-named primary contrasts only; (c) small-sample corrections (Harvey–Leybourne–Newbold) and fixed-b HAC; (d) Giacomini–Rossi fluctuation test for time-varying performance; (e) Holm correction across primary contrasts; (f) crisis windows and turning points reported descriptively with bootstrap intervals; (g) a pre-lock power simulation stating the minimum detectable RMSE ratio.

### 7. Decision gate (Critical)

The gate tests H2 and then uses the result to decide whether H1 is tested at all. If 1B fails, DSGE is never evaluated, and H1 silently drops out. It also invites "keep adding complexity until something wins". *Fix:* the gate governs only whether *you build* new models. Evaluation of existing real-time DSGE forecasts is unconditional. Level 2 is dropped from the confirmatory plan.

### 8. Euro-area extension (Minor)

The ECB's real-time database exists, but the euro-area 2008–13 episode includes a sovereign crisis no US-trained specification anticipates. *Fix:* keep it exploratory and say so; specify it in a separate, later preregistration.

## Data availability audit

Every macro series is available in true real time except private credit, which must be reconstructed. Rows marked *verify* are checks to complete and record before lock.

| Series | Primary source | Real-time vintages? | Revision risk | Action before lock |
| --- | --- | --- | --- | --- |
| Real GDP (ROUTPUT) | [Philadelphia Fed RTDSM](https://philadelphiafed.org/research-and-data/real-time-center/real-time-data) | Yes, mid-quarter vintages back to 1965 | High; benchmark revisions 2009, 2013 | Lock vintage-timing rule and "truth" vintage |
| GDP deflator (P) | RTDSM | Yes | Moderate | Lock as inflation measure |
| Unemployment rate (RUC) | RTDSM (monthly) | Yes | Low; seasonal factors only | Lock quarterly-average rule |
| Nominal GDP (NOUTPUT) | RTDSM | Yes | High | Needed as credit-impulse denominator, same vintage |
| 2-year Treasury yield | Fed H.15 / FRED | Not revised | None | Replaces fed funds after ZLB |
| Fed funds rate | FRED | Not revised | None | Keep pre-2008 only, or drop |
| Private non-financial credit | [Fed Z.1 archive](https://www.federalreserve.gov/releases/z1/20130606/) + [FRASER](https://fraser.stlouisfed.org/title/93/item/579649) | Partial; must be reconstructed. ALFRED Z.1 vintages appear to start mid-2013 | High; reclassifications | *Verify* earliest machine-readable vintage per series; document gaps |
| BIS total credit, US | [BIS / FRED](https://fred.stlouisfed.org/graph/?g=BwH3) | No; database launched March 2013, break-adjusted | Not applicable | Final-vintage robustness only |
| Baa–10y spread | FRED | Not revised | None | Optional observable; needed if comparing to SW-FF |
| SPF forecasts | Philadelphia Fed SPF | Yes, by construction | None | Reference benchmark |
| Greenbook forecasts | Philadelphia Fed (released with a lag) | Yes | None | *Verify* coverage through 2019 |
| Real-time DSGE forecasts | Del Negro & Schorfheide (2013); Cai et al.; Wieland–Wolters / MMB | Published, real-time or pseudo-real-time | Mixed | *Verify* which are "real real-time" vs reconstructed; label each |
| NBER cycle dates + announcement dates | NBER | Announcement dates known | None | Use for scoring only, never as model input |

Two caveats apply to the published DSGE forecasts. Edge et al. note their own "real-time" forecasts were produced retrospectively ([FEDS 2009-10](https://www.federalreserve.gov/pubs/feds/2009/200910/)), and model choice may still embed hindsight. Label every comparator as *real real-time* (made at the time) or *pseudo real-time* (made later on old vintages).

## Preregistration checklist

Tick every box before computing a single forecast error. Anything unticked at lock is either resolved or explicitly listed as a deviation.

**A. Claims and framing**

- [ ] Nobel framing reduced to one sentence of motivation; no claim about the prize or DSGE models
- [ ] Construct-validity caveat (forecasting ≠ policy design) written into the protocol
- [ ] Exact Nobel citation quoted; Academy scientific background read and credited papers listed
- [ ] Primary contrasts named (max two) and all others labelled secondary or exploratory
- [ ] 2007–09 labelled exploratory for H2, with reason (hypothesis formed on that episode)

**B. Targets and truth**

- [ ] Growth concept locked (q/q annualised primary; 4Q cumulative secondary)
- [ ] Inflation measure locked (GDP deflator)
- [ ] Unemployment target locked (quarterly-average level; direction scored on change)
- [ ] "Truth" vintage rule locked (published two quarters after target; first release and latest as robustness)
- [ ] Turning-point call rule written down, with lead-time scoring

**C. Data and vintages**

- [ ] Series IDs, sources and transformations listed in a data dictionary
- [ ] Forecast-origin timing rule locked (mid-quarter, matching RTDSM)
- [ ] Information set defined by publication date, ragged edge documented
- [ ] Z.1 vintage audit complete: earliest usable vintage per credit series recorded
- [ ] Policy-rate variable locked (2-year yield)
- [ ] Raw vintage files archived with SHA-256 hashes

**D. Credit variables**

- [ ] Credit-impulse formula locked (4-quarter version, flows-based, same-vintage nominal GDP)
- [ ] Sector scope locked (households + non-financial business)
- [ ] Any gap measure uses a one-sided filter only
- [ ] Revision-variance diagnostic of CI scheduled before forecasting

**E. Models**

- [ ] Level 0 locked: random walk, 8-quarter trailing mean, AR(1), AR(2)
- [ ] Level 1A/1B locked: variables, lag length (fixed at 2), BVAR prior and hyperparameters fixed in advance
- [ ] Estimation scheme locked (expanding from 1965Q1; 60-quarter rolling as robustness)
- [ ] Iterated multi-step for VAR/AR locked
- [ ] ADL model (AR(2) + credit impulse) locked as the simplest credit test
- [ ] Latest-vintage credit series built for the hindsight comparison (H-C)
- [ ] SPF and Greenbook added as reference rows
- [ ] Phase 0 go/no-go rule and sample fallback recorded

**F. Evaluation and inference**

- [ ] Confirmatory sample locked: origins 1990Q1–2019Q4
- [ ] Crisis windows fixed by calendar quarters, not NBER dates
- [ ] COVID (2020–21) excluded from confirmatory sample; reported separately
- [ ] Tests locked: Clark–West for nested, DM with HLN correction for non-nested, Giacomini–Rossi fluctuation test
- [ ] Multiple-comparison rule locked (Holm across primary contrasts)
- [ ] Power simulation run; minimum detectable RMSE ratio stated
- [ ] Inference language rule: no significance claims on crisis windows or turning points

**G. Process**

- [ ] Protocol committed to a public timestamped repository (e.g. OSF or tagged GitHub release) before analysis
- [ ] Code for all models written and run on synthetic data only before lock
- [ ] Deviation log created; every post-lock change dated and justified
- [ ] All results reported, including failures and null findings

**H. v2.1 additions**

- [ ] "Revised" target vintage frozen (download date recorded)
- [ ] SPF survey deadlines and Z.1 release dates tabulated for every quarter
- [ ] SPF test uses only Z.1 releases published before each survey deadline
- [ ] Three credit measures pre-registered as one family, Holm-corrected within it
- [ ] Credit gap uses a one-sided HP filter (λ = 400,000), recomputed at every vintage
- [ ] Threshold rules have no free parameters; false alarms counted across all quarters
- [ ] GDI vintage coverage checked in ALFRED
- [ ] Nowcasting parked; not run under this protocol

**I. v2.2 additions**

- [ ] Claim worded as predictive content under real-time vintages; no causal language anywhere
- [ ] Vintage-by-vintage series mapping table complete (table, line, series code per Z.1 vintage)
- [ ] PDF extraction protocol followed for any pre-digital Z.1 vintage; reconciliation log archived
- [ ] Z.1 and GDI release-date tables complete; origins without a known date dropped
- [ ] Realistic power simulation published (actual origins, overlap, Holm across four); conditional rules in §11 applied
- [ ] COVID exclusion applied by target quarter

**J. v2.3 additions**

- [ ] Interpretive map locked; unlisted patterns to be reported as "unanticipated"
- [ ] Advance-estimate release dates tabulated for P3 anchors
- [ ] Real-time GDP deflator mapped for real credit growth
- [ ] Data vintage of López-Buenache et al. (2025) confirmed with the authors, or stated as an inference
- [ ] CBO natural-rate vintages checked in ALFRED (E1 only)
- [ ] Power simulation extended to P3 and S5

## Preregistration protocol v2.3

This is the text to lock; it replaces v2.2. Fields in \[brackets\] are filled in Phases 0–1, before any forecast is computed. Notation: o = origin quarter; s = target quarter; v = Z.1 vintage; w = GDP vintage.

### 1. Claim and its limits

**Question.** Under the data vintages available at each date, did standard credit transformations have predictive content for subsequently revised US real GDP growth and unemployment, 1990–2019? How much of the predictive content measured on revised data depends on revisions to the credit data?

**What this does not claim.**

- **No causal claim.** The project measures predictive content, not whether credit drives demand.
- **Real-time data is not real-time knowledge.** The credit impulse was first defined in November 2008, and Keen's credit accelerator in 2011. Results before 2008 show what this transformation *would have delivered* applied to contemporaneous data, not what forecasters knew or could reasonably have chosen. Credit growth and credit-to-GDP were standard before 2008, so the horse race in S2 is a partial check on this concept hindsight.
- **P2 is counterfactual.** "Would have improved the SPF" means the information was in published data. It does not mean forecasters erred by ignoring it.
- No claim about DSGE models or the 2026 Economics prize.

**Related evidence.** [López-Buenache, Borsi and Rosa-García (2025)](https://www.recercat.cat/handle/20.500.14342/5700) find that credit contractions improve the identification and recursive forecasting of labour-market slack in a Markov-switching framework (US, 1955–2023). Their out-of-sample exercise is recursive from 2000, but the data do not appear to be vintage-based, and slack is defined against an estimated natural rate that is itself revised. The present project tests whether that signal survives a real-time information set and revised-outcome scoring, over an overlapping 2000–2019 window. *Open item:* confirm the data vintage with the corresponding author before citing this as fact.

**Closest precedent.** [Edge and Meisenzahl (2011)](https://www.federalreserve.gov/econres/feds/the-unreliability-of-credit-to-gdp-ratio-gaps-in-real-time-implications-for-countercyclical-capital-buffers.htm) show that real-time revisions to the US credit-to-GDP gap are about as large as the gap itself, and come mainly from the filter's unreliable end-of-sample trend rather than from revisions to the underlying data. Their question is **reliability**: does the measure move after the fact? This project asks about **usefulness for macro forecasting**: did the measure, as published, carry information about later output, unemployment, professional forecast errors and GDP revisions? Real-time usefulness tests already exist in the early-warning literature (e.g. Alessi and Detken, 2011), but for crisis prediction, not for macro forecasts or forecaster counterfactuals; the novelty claimed here is scoped to the latter.

**What is new relative to them.**

- **Window.** The sample runs to 2019 and includes the post-2008 period, when the impulse concept was public (S6). That is the more informative half of the freshness claim.
- **Channel.** The impulse uses no filter, so it isolates the channel they found secondary: data revisions. Two forces pull in opposite directions. Double differencing amplifies revision noise. But S\_t is a four-quarter sum of flows, which averages away part of the noise hitting individual quarters, while Z.1 flows are themselves subject to large periodic benchmark revisions. The size of the impulse's revision premium is therefore genuinely open.
- **No pre-commitment to either story.** A measure can be revised heavily and still predict well, if revisions hit parts that do not matter. It can equally lose its predictive content precisely because revisions hit the parts that did. The grid (§2) and interpretive map (§4a) distinguish these cases; neither is assumed.

### 2. The organising grid

|  | Early-estimate target | Revised target |
| --- | --- | --- |
| **Real-time credit vintage** | Real-time vintage, early target (reference) | **Primary cell** |
| **Revised credit vintage** | Not reported | Revised-data benchmark (as in most published work) |

**Credit-revision premium** = RMSE ratio (credit model ÷ benchmark) using real-time credit and denominator, minus the same ratio using revised credit with the real-time GDP denominator, so that a positive premium means revised credit data forecast better (sign fixed 19 Oct 2026, audit Entry 17). Both are scored against the revised target. It isolates revisions to the credit data, holding the transformation fixed. The **total predictor-revision premium** (revised credit *and* revised denominator) is reported as a secondary decomposition. Neither premium measures concept hindsight; §1 covers that.

### 3. Phases and go/no-go

**Phase 0 — data audit.** Each gate is recorded as pass or fail before Phase 1 begins.

| Gate | Criterion | If it fails |
| --- | --- | --- |
| G1 Credit vintages | A complete vintage-by-vintage mapping table (Z.1 table, line, series code, units, SA status) for every vintage used, and at least 60 consecutive origins with all components present | Project stops at a dataset note |
| G2 Z.1 release dates | Exact publication date verified for every vintage used | Undated vintage dropped; the origin uses the latest earlier dated vintage |
| G3 GDI vintages | First-release and anchor-date GDI values for at least 60 target quarters | S3 dropped; P3 runs on GDP alone |
| G4 SPF deadlines | Documented deadline for every survey in the P2 sample (Philadelphia Fed release-dates file; surveys from 1990Q3 only), and at least 40 evaluation surveys after the training period | P2 demoted to secondary |

**Sample-start decision (17 Oct 2026, before any forecast).** The confirmatory sample starts at origin **1999Q3**, the first origin after the June 11, 1999 Z.1 release, which is the earliest vintage with machine-readable full quarterly history. It runs to 2018Q4 at h = 4: 78 origins, which passes G1. Earlier vintages print only the last 4–5 years of quarterly data, so they cannot supply a full real-time estimation history. An **exploratory extension to 1990Q1** uses a hybrid vintage: real-time values for the quarters printed in each PDF release, spliced onto older history from the June 1999 vintage. It is labelled as carrying a partial hindsight leak, and it never enters the confirmatory tests. As a consequence, the 1990–91 recession is exploratory only, and the 2001 and 2007–09 recessions remain in the confirmatory sample.

**Mapping table.** Z.1 series names and codes changed over time (e.g. "credit market instruments" became "debt securities and loans"). The table links each vintage's series to one consistent concept. Any break in definition is logged with its date, never smoothed.

**PDF extraction protocol** (any vintage without machine-readable files):

1. Record source URL, file SHA-256 and page numbers for every table used.
2. Extract twice, independently: (a) automated, from the PDF text layer, or OCR (Tesseract) if none; (b) manual keying, blind to (a).
3. Resolve every cell where (a) and (b) differ by inspecting the page image; log each resolution.
4. Check that components sum to printed totals within ±1 in the last printed digit. Flag, but do not force, mismatches between flows and level changes.
5. Record units and seasonal-adjustment status from each table header.
6. Extract only series listed in the mapping table.

**Phase 1** builds all credit measures in real-time and revised form, runs the revision study and the power simulation (§11), and draws the raw-series graphs. No forecasts are computed. **Lock** follows, then **Phase 2** runs every test once.

### 4. Hypotheses and decision rules

| ID | Hypothesis | Status | Test |
| --- | --- | --- | --- |
| P1a | Real-time credit impulse adds predictive content for revised real GDP growth at h = 4 over AR(2) | **Confirmatory** | Direct ADL vs direct AR(2), Clark–West, one-sided |
| P1b | Same, for the unemployment rate | **Confirmatory** | As above |
| P2a | Real-time credit impulse, published before each survey deadline, would have improved bias-corrected SPF median GDP growth forecasts at h = 4 | **Confirmatory** | Corrected vs bias-corrected SPF, Clark–West |
| P3 | Real-time credit impulse predicts later revisions to first-release GDP growth | **Confirmatory** | §9; two-sided HAC t-test |
| P2b | Same as P2a, for SPF unemployment forecasts | Exploratory | As P2a |
| S1 | Credit-revision premium is positive | Exploratory | §2; block bootstrap interval |
| S2 | Ranking of credit impulse, credit growth, credit-to-GDP gap and real credit growth | Exploratory | Each in the P1 model |
| S3 | Real-time credit predicts GDI revisions, and GDP revisions controlling for GDI | Exploratory | Dropped: G3 failed (audit Entry 7) |
| S4 | P1 using the BVAR (1A vs 1B) | Exploratory | §8 |
| S5 | Predictive content is concentrated in credit contractions | Exploratory | Asymmetric and contraction ADLs (§8) |
| S6 | Stability before and after the impulse was defined: P1 on origins up to 2008Q3 vs from 2008Q4 | Exploratory | Separate RMSE ratios with intervals |
| R1 | Ragged-edge variants Y and Z (§6) | Robustness | Reported in full; never used to select the headline |
| E1 | Replication of the López-Buenache et al. credit-contraction signal under real-time vintages, 2000–2019 | Exploratory | Markov-switching model, filtered probabilities only (§8) |
| E2 | The credit-revision premium comes from late-arriving source data (routine releases) rather than from redefinitions (benchmark releases). Run only if S1 shows a premium. | Exploratory | Trace each quarter's credit impulse through all 83 releases (1999–2019) and assign each revision step to the release that made it. A release is a benchmark release if its median absolute revision to the credit impulse, for quarters at least 12 quarters before its q\*, exceeds 0.25 × the SD of the revised impulse; every other release is routine. The threshold is fixed before the revision paths are examined (agreed by Andy, 19 Oct 2026). Revisions from Dec 2019 to the current release cannot be split and are reported as one block. Descriptive revision shares only. |
| D1 | Credit threshold signals preceded recessions | Descriptive | §10 |

**The confirmatory core is P1a, P1b, P2a and P3, under Holm, and nothing else.** Every other entry is exploratory or robustness, and the paper labels it that way in its own language, not as a second tier of tests. Exploratory results get no multiplicity correction and support no confirmatory claim. All are published, including nulls. P3 is in the core because it has one observation per quarter and no forecast overlap, making it likely the best-powered test.

**Expectation statement (not a hypothesis).** We expect the credit-revision premium for the impulse to be small, because data revisions were the secondary channel for credit gaps (Edge and Meisenzahl, 2011). If it is large, that is itself a finding. Given the benchmark-revision exposure noted in §1, this is a genuine gamble, not a safe prior. It adds **no test** to the confirmatory core: S1 remains exploratory and uncorrected for multiplicity, and the expectation is reported as confirmed or contradicted, nothing more.

**D2 — Edge–Meisenzahl replication (descriptive, dataset validation).** On this project's own Z.1 vintages, 1999–2019, decompose each quarter's credit-to-GDP gap revision (real-time minus latest) into two parts:

1. **Data-revision component:** the gap recomputed on latest-vintage data, but with the filter run only up to the origin quarter.
2. **End-point (filter) component:** everything else.

Report each part's share of revision variance. Reproducing their "mostly filter" result validates the vintage dataset and links this paper to theirs. A different result is reported as a finding.

**D2 and S1 measure different objects.** D2 is a variance decomposition of the *gap's revisions*, and it validates the dataset and confirms whether the filter was the gap's dominant problem. S1 is a difference of *forecast RMSE ratios*, and it asks a separate question: whether the residual data-revision channel, alone and unfiltered, changes the impulse's predictive content. Results from one are not read as evidence about the other.

### 4a. Interpretive map (pre-registered)

Results are interpreted only through this table. Any pattern not listed is reported as "unanticipated", with no post hoc explanation. Wording follows the power rule in §11. Exploratory results (E1) cannot move a reading between rows.

**Headline map, written before lock.** P1 is "positive" if it meets the support rule in §11. The credit-revision premium is **large** if it is at least 0.05 in RMSE-ratio units and its 90% bootstrap interval excludes zero, and **small** otherwise.

| Headline outcome | Pre-committed sentence for the paper |
| --- | --- |
| Honest cell positive | "Credit carried predictive content that a forecaster could have used from data as published at the time." |
| Null, large premium | "The predictive content of credit reported in revised data depends on later revisions to the credit data; it was not available in real time." |
| Null, small premium | "Credit shows no detectable predictive content in either real-time or revised data at this sample size; the published evidence does not rest on revisions, and given that the available credit variation is concentrated in 2008–09, the design could reliably detect only very large gains, of roughly 40% or more (RMSE ratio about 0.6; audit Entries 18–19)." |

The detailed table below refines these readings; it never overrides them.

| Pattern of results | Reading |
| --- | --- |
| P1 supported; credit-revision premium small | Predictive content was available in real time, and revised-data evidence holds up |
| P1 supported; premium large | Content exists in real time, but revised-data estimates overstate it |
| P1 null; revised-data cell positive; premium large | **Measurement story:** apparent content depends on revisions to the credit data |
| P1 null; premium small; S5 supported | **Specification story:** the signal is concentrated in contractions and averaged away by a linear model |
| P1 null; premium small; S5 null | **No evidence** of predictive content under real-time data at this sample size; only very large gains (roughly 40% or more) ruled out, because the credit variation is concentrated in 2008–09 |
| P1b supported; P1a null | Content is specific to the labour market; consistent with, but not proof of, a financing-constraint channel |
| P3 supported | First-release GDP did not fully reflect information in published credit data; this stands whatever P1 shows |
| P2a supported | The information was in published data before the SPF deadline but not reflected in the median forecast |

No row is a causal claim. The map interprets prediction patterns, not mechanisms.

### 5. Targets

- **Real GDP growth:** g\_s = 100 × \[(Y\_s / Y\_{s−1})^4 − 1\], discretely compounded, where Y is real GDP, chained dollars, seasonally adjusted. This matches the annualisation used by BEA and the SPF, so model and SPF errors are on the same scale.
- **Unemployment:** u\_s = mean of the three monthly civilian unemployment rates (SA) in quarter s. The target is the **level**. Because the base is known at the origin, RMSE on the level equals RMSE on the change from that base. Directional accuracy uses the sign of u\_s − u\_{o−1}, with u\_{o−1} from the origin vintage; changes under 0.05 pp are dropped from the direction metric.
- **Horizon:** at origin o, the target is s = o + h, for h ∈ {1, 2, 4}; h = 4 is primary. This matches the SPF's four-quarter-ahead convention.
- **Revised target:** values from the RTDSM vintage dated 2026Q3 (ROUTPUT26Q3, RUC26Q3), downloaded 19 Oct 2026, frozen and hashed (SHA-256: ROUTPUTQvQd.xlsx 25433da0…, rucQvMd.xlsx d971e59d…; full hashes in audit Entry 13).
- **Early-estimate target:** the value for s in the RTDSM vintage dated quarter s + 2.
- **COVID exclusion by target quarter:** any forecast with s ≥ 2020Q1 is excluded. The last included origin is 2018Q4 at h = 4, 2019Q2 at h = 2 and 2019Q3 at h = 1.

### 6. Information set, ragged edge and credit timing

- **Origin.** The origin date is the RTDSM vintage date for quarter o (middle month). GDP, unemployment, inflation and the 2-year yield are observed through o − 1 in that vintage, so non-credit variables have no ragged edge.
- **Credit availability.** At each origin, credit is taken from the latest Z.1 release dated before the origin date. Its last quarter is q\*\_o, and the gap k\_o = o − q\*\_o is recorded as data, not chosen (typically 2). If a release is late, the latest earlier release is used and the larger k\_o recorded.
- **Origin–release table.** In Phase 1, a table of (origin, Z.1 release date, q\*\_o, k\_o) is built from release dates alone. It is dated and hashed before any forecast is computed.
- **Primary treatment: release-time lags.** Credit enters every model only at the lags actually published, X\_{q\**o}, X*{q\*\_o−1}, and so on. Nothing fills the gap between q\*\_o and o − 1, and no auxiliary model is used. This method was chosen on transparency grounds alone, before any forecast was computed; Phase 1 is descriptive only.
- **Robustness Y: AR imputation.** The 4-quarter credit flow S\_t for quarters q\*\_o + 1 … o − 1 is forecast from an AR(4) on S\_t alone, estimated on that Z.1 vintage up to q\*\_o. CI for those quarters is then computed, and models use calendar lags ending at o − 1.
- **Robustness Z: credit-only state-space model.** A VAR(2) on household and non-financial business flows, in state-space form, fills q\*\_o + 1 … o − 1 by Kalman forecast.
- **Gap-filler rule.** No gap-filler uses GDP, unemployment, inflation, interest rates or any other non-credit series to predict credit. Nominal GDP enters only as the published CI denominator, never as a predictor.
- **Reporting rule.** Primary is release-time lags, tested under Holm. AR imputation and the credit-only state-space model are reported in full as robustness, with RMSE ratios and intervals. Disagreement between them and the primary is reported, not adjudicated by selecting the favourable result.
- **Lock.** The rule text, the gap-filler code and the origin–release table are committed and SHA-256 hashed at lock.
- **Estimation history.** Estimation at each origin uses the full history as it appears in the origin's vintages (end-of-sample vintage convention).

### 7. Credit definitions

**Stocks and flows are kept separate.** Let L\_t^(v) be the outstanding stock at the end of quarter t, and F\_t^(v) the seasonally adjusted transactions flow during quarter t. Both cover households plus non-financial business, debt securities and loans, from Z.1 vintage v. Flows published at annual rates are divided by 4. Let N\_t^(w) be the sum of quarterly nominal GDP (SAAR ÷ 4) over t − 3 … t, from GDP vintage w.

```latex
S_t^{(v)} = \sum_{j=0}^{3} F_{t-j}^{(v)} \qquad CI_t^{(v,w)} = 100 \times \frac{S_t^{(v)} - S_{t-4}^{(v)}}{N_t^{(w)}}
```

| Measure | Built from | Definition | Role |
| --- | --- | --- | --- |
| Credit impulse | Flows | CI\_t above; split into CI⁺ = max(CI, 0) and CI⁻ = min(CI, 0) for S5 | Primary |
| Credit growth | Stocks | 100 × (L\_t / L\_{t−4} − 1) | S2 |
| Credit-to-GDP gap | Stocks | R\_t = 100 × L\_t / N\_t, minus a one-sided HP trend (λ = 400,000) estimated on R up to t within that vintage | S2 |
| Real credit growth | Stocks | 100 × \[(L\_t / L\_{t−4}) ÷ (P\_t / P\_{t−4}) − 1\], P = GDP deflator from the origin's RTDSM vintage; contraction indicator = 1 if negative | S2, S5, E1 |

**Robustness:** CI from stock differences, replacing S\_t with L\_t − L\_{t−4}. The difference between the two is reclassifications and breaks, reported in the revision study.

**Denominator vintage:** real-time w = the RTDSM vintage at the origin, which always covers q\*\_o because GDP is published before Z.1. Revised w = the frozen latest vintage.

### 8. Models

All models are estimated on an expanding window from 1965Q1 (or the earliest quarter the vintage supports) and re-estimated at every origin. Robustness: a 60-quarter rolling window.

| Model | Specification | Used in |
| --- | --- | --- |
| Benchmarks | Random walk; 8-quarter mean; AR(1); AR(2) | Reference |
| Direct AR(2) | y\_{o+h} = α + φ₁y\_{o−1} + φ₂y\_{o−2} + ε | P1 benchmark |
| Direct ADL | Direct AR(2) + Σ\_{j=0}^{3} β\_j X\_{q\*−j}, where X is the credit measure | P1, S1, S2 |
| Asymmetric ADL | Direct AR(2) + Σ β⁺*j CI⁺*{q\*−j} + Σ β⁻*j CI⁻*{q\*−j}, j = 0…3; split fixed at zero, nothing estimated | S5 |
| Contraction ADL | Direct AR(2) + real credit growth and its interaction with the contraction indicator, lags 0–3 | S5 |
| BVAR 1A | GDP growth, GDP deflator inflation, unemployment, 2-year yield; lag 2; data through o − 1 | S4 |
| BVAR 1B | 1A + CI shifted by its release lag (CI\_{t−2}), so credit enters only as published; when k\_o > 2, the missing value is filled by the credit-only AR imputation (robustness Y). No conditioning on non-credit data | S4 |
| SPF corrected | SPF\_{o+4\|o} + α̂\_o + β̂\_o × CI\_{q\*} | P2 |
| SPF bias-corrected | SPF\_{o+4\|o} + α̂\_o | P2 benchmark |
| Markov-switching (E1) | Two-regime Markov-switching regression of Δu\_t on a switching intercept and switching variance, with real credit growth at its release lag (RCG\_{t−k}) as a non-switching regressor, estimated from 1965Q1 on data through o − 1 at each origin from 2000Q1. The filtered (never smoothed) probability of the rising-unemployment regime at o − 1 is added to the direct AR(2) for u\_{o+4}, and scored by Clark–West against the AR(2) (specification agreed 19 Oct 2026, audit Entry 17) | E1 |

**E1 targets:** the unemployment level (as in P1b), and real-time slack only if CBO natural-rate vintages exist in ALFRED. Using today's natural rate would bring hindsight into the target.

**Why direct.** The ADL is direct, so it needs no forecast of credit, nests the direct AR(2) exactly, and keeps Clark–West valid.

**BVAR prior (S4).** Minnesota prior, identical hyperparameters in 1A and 1B: overall tightness 0.2, cross-variable 0.5, lag decay 2. Prior mean on the first own lag is 1 for unemployment and the 2-year yield, and 0 for GDP growth, inflation and CI. Scale parameters come from AR(4) residual variances on each estimation sample. Shrinkage makes Clark–West asymptotics non-standard, so S4 uses the HLN-corrected Diebold–Mariano test with a bootstrap and is read as supporting evidence only.

**SPF alignment (P2), checked against the [SPF documentation](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/spf-documentation.pdf) (July 2026):**

- **Horizon.** In survey o, forecasters know GDP through o − 1 (the advance estimate) plus the employment report released in month 2 of o. Column suffix 6 is quarter o + 4, matching h = 4.
- **GDP target series.** The official median growth series (MedianGrowth.xlsx, dRGDP6) is the growth rate of the median *level* forecasts, not the median of individual growth rates. It is discretely compounded and annualised. **Primary:** dRGDP6 as published, because that is what a contemporary saw. **Robustness:** the median of each forecaster's own implied growth rate, from SPFmicrodata.xlsx. This avoids mixing different forecasters' levels across adjacent quarters.
- **Unemployment target series.** UNEMP6, the median forecast of the quarterly-average rate. It is a level, so no growth construction is needed.
- **Base years.** Level files use the base year in force at each survey and are never rescaled. Only growth rates enter P2a, so this does not matter.
- **Deadlines and sample.** Deadlines come from the Philadelphia Fed release-dates file. Only surveys from 1990Q3 onward are used: 1990Q2 was collected after the fact, and the timing of pre-1990 ASA/NBER surveys is not documented.
- **Credit.** CI\_{q\*} comes from the latest Z.1 release dated before the deadline d\_o; typically q\* = o − 2.
- **Correction.** α̂ and β̂ are estimated by OLS on past surveys whose target quarter had been published by d\_o. Errors are computed from values as published at d\_o. At least 20 training pairs are required before the first evaluation, and evaluation is against the revised target. The bias-only benchmark stops a pure bias correction being credited to credit.
- **Information edge.** The SPF's extra month of labour-market data is left in place. It makes P2 harder to pass, not easier.
- **Implied sample.** A training pair from survey s becomes usable only once quarter s + 4 is published, so the first evaluation survey is about 1996Q3. That leaves at most about 90 evaluation surveys to 2018Q4, and fewer if Z.1 vintages start later.

### 9. P3 and S3 — revision tests

**P3 (primary, GDP only).**

- **Anchor date a\_s:** the release date of the advance GDP estimate for quarter s (end of month 1 of s + 1).
- **Outcome:** R\_s = g\_s(revised) − g\_s(advance).
- **Predictor:** CI from the latest Z.1 release before a\_s (typically covering s − 1).
- **Controls (as published at a\_s):** advance g\_s and g\_{s−1}.
- **Test:** OLS with HAC standard errors (4 lags); two-sided test of the CI coefficient, with p-value and 90% interval from a restricted wild (Rademacher) block bootstrap of the HAC t-statistic (block 4, 999 draws), because fixed-b HAC over-rejects (14–18%) when a few extreme CI values dominate (amended 19 Oct 2026, audit Entry 18). One observation per quarter.
- **Robustness:** revision measured to the last vintage before the next comprehensive revision, which removes definitional changes from R\_s.

**S3 (dropped, 17 Oct 2026: G3 failed, see audit Entry 7; text kept for the record).**

- **Anchor:** the date GDI for s is first published.
- **Outcomes:** the GDP revision from that date, and the GDI revision.
- **Controls add:** GDI growth and the GDP–GDI growth gap at the anchor.

**Reading.** A non-zero coefficient means early estimates did not fully reflect information already in published Z.1 data ("noise" rather than "news" in the revision). It is not a claim that the statistical agency erred.

### 10. D1 — threshold signals

**Rules (no free parameters), evaluated at each origin with data as then available:**

1. CI negative for two consecutive available quarters.
2. 4-quarter credit growth below 4-quarter nominal GDP growth.

**Episode definition.**

- A signal belongs to its origin quarter.
- An **episode** is a run of consecutive signal quarters; runs separated by a single non-signal quarter are merged.
- **Hit:** the episode starts 1–6 quarters before an NBER peak (1990Q3, 2001Q1, 2007Q4).
- **Late:** the episode starts between the peak and the trough.
- **False alarm:** any other episode.
- **Miss:** a peak with no episode starting in the 6 quarters before it.
- Lead time = peak quarter − episode start.
- The share of all quarters spent in signal is also reported.

The revised version applies the same rules to revised data for the same data quarters. Published BIS thresholds are not used, because they were calibrated after 2008.

### 11. Power and power-dependent rules

**Simulation, run in Phase 1 and published before lock:**

- **DGP for P1 and P2:** the direct ADL, with CI following its own fitted AR process and measurement noise matching the Phase 1 credit revision variances.
- **DGP for P3:** the revision regression, with a CI effect calibrated to partial R² of 0.02, 0.05 and 0.10.
- **DGP for S5:** the asymmetric ADL, with an effect only in CI⁻.
- **Design:** actual sample sizes (P1 origins from Phase 0; P2a at most about 90 surveys; P3 one observation per quarter), h = 4 overlap where relevant, HAC tests, and Holm across P1a, P1b, P2a and P3.
- **Effect sizes for forecast tests:** true RMSE ratios of 0.85, 0.90 and 0.95.
- **Replications:** 2,000.
- **Reported:** per-test and family-wise power, and the minimum detectable effect at 80% power. Result (specification-matched simulation, fixed-b, Holm, audit Entry 16): RMSE ratio 0.88 for P1a, 0.85 for P1b and 0.89 for P2a; partial R² just above 0.10 for P3. Holm-adjusted power at a true ratio of 0.90: P1a 0.71, P1b 0.58, P2a 0.75; P3 0.45 at partial R² 0.05.

**Pre-declared rules, selected by power at a true ratio of 0.90:**

| Power at 0.90 | Primary tests | Support rule | Language for a null |
| --- | --- | --- | --- |
| ≥ 0.80 | All four | Holm p < 0.05 and ratio ≤ 0.95 | "Not supported" if ratio ≥ 1.00, else "inconclusive" |
| 0.50–0.80 | All four | Same | "Not detected; gains larger than \[upper 90% bound\] ruled out" |
| < 0.50 | P1a and P3 only; P1b and P2a move to exploratory | Estimation only: "credible improvement" if the 90% bootstrap interval for the RMSE ratio lies wholly below 1.00 | No significance language; ratios and intervals reported |

**The rule is applied test by test** (decision, 19 Oct 2026, before any forecast). Each confirmatory test's band is set by its own Holm-adjusted power at a true RMSE ratio of 0.90 (for P3, a partial R² of 0.05). **Inference uses fixed-b critical values** (Kiefer–Vogelsang, Bartlett kernel, b = (h − 1 + 1)/n), simulated once and frozen, because standard normal critical values with NW HAC over-rejected at these sample sizes (audit Entry 12).

**Bands as applied (decision 19 Oct 2026, audit Entries 18–19; supersedes Entries 14 and 16):** power is assessed conditional on the actual credit path, because the real credit impulse is dominated by one episode and a Gaussian simulation overstates power. On that basis all four confirmatory tests fall in the < 0.50 band. Each is therefore reported as an estimate with its 90% interval (block bootstrap for RMSE ratios; wild block bootstrap for P3), with "credible improvement" only if the whole interval lies below 1.00 (for P3, excludes zero). No significance language is used; Holm-adjusted p-values are reported for completeness only. Checked on synthetic data with the real credit path: the rule's false "credible improvement" rate is 0–2%, and it detects a true 7% gain 30–40% of the time.

The rule is chosen from simulation alone and written into the locked protocol.

**Expectation statement.** If the simulated minimum detectable RMSE ratio is below 0.95, meaning only gains larger than 5% can be detected, the protocol and the paper both state: *"Before seeing any results, we expected this design to detect only large improvements, because almost all the variation in the credit impulse comes from 2008–09; at the actual credit path, even a 10% gain would be detected less than half the time, and only gains of roughly 40% or more reliably. Smaller real effects may exist and go undetected."*

### 12. Inference details

- HAC standard errors with h − 1 lags.
- Giacomini–Rossi fluctuation test (20-origin window) to show *when* any gain occurs.
- Block bootstrap (block length 4) for premia and ratio intervals.
- Descriptive windows (calendar-fixed): 2000Q1–2002Q4 and 2007Q1–2010Q4 within the confirmatory sample; 1989Q3–1992Q2 in the exploratory hybrid-vintage extension only. The 2007–09 window is exploratory for all credit claims.

### 13. Graphs

- The grid as one chart of RMSE ratios with intervals (headline exhibit).
- Real-time vs revised CI, with recession shading added after the series are drawn.
- The k\_o lag at each origin.
- Threshold timeline: real-time and revised rows, with episodes classified.
- Cumulative squared-error differences for P1 and P2, with the share of the total gain coming from origins 2007Q1–2010Q4 reported beside each, together with the signed total (added 19 Oct 2026, audit Entry 19).
- GDP and GDI revisions against real-time CI.

### 14. Out of scope and process

- Nowcasting is parked: quarterly Z.1 arrives after the first GDP estimate. DSGE comparisons and the euro area are also out of scope.
- Lock = tagged public commit (OSF or GitHub release) with this protocol, the mapping table, extraction logs, power results, code tested on synthetic data, and SHA-256 hashes of every raw file.
- A dated deviation log, each entry stating whether any results had been seen. All pre-registered outputs published, including nulls.

## Phase 0 audit log

Entries are dated and are never edited after the fact; corrections are added as new entries.

### Entry 1 — 17 Oct 2026: Z.1 vintage availability and series codes

**Result: G1 passes from 1999Q3. Sample-start decision recorded in protocol §3.**

| Period of Z.1 releases | Source | Format | Quarterly history per vintage | Usable for |
| --- | --- | --- | --- | --- |
| Jun 11, 1999 → present | [Fed release archive](https://www.federalreserve.gov/releases/z1/release-dates.htm), per-release "Historical data" page | Zip files from 1952Q1, incl. debt file for tables D.1–D.3 ([example](https://www.federalreserve.gov/releases/z1/19990611/data.htm)) | Full | Confirmatory sample |
| Sep 12, 1996 → Mar 12, 1999 | Fed release archive | Text PDF only ([Mar 1999 page](https://www.federalreserve.gov/releases/z1/19990312/) has no data link) | Last \~4.5 years | Exploratory extension |
| Mar 1988 → Jun 1996 | [FRASER](https://fraser.stlouisfed.org/title/z1-financial-accounts-united-states-93?browse=1990s) | Scanned PDF with OCR text; OCR errors confirmed (e.g. "A" for "4") in the [Mar 6, 1991 release](https://fraser.stlouisfed.org/title/z1-financial-accounts-united-states-93/march-6-1991-69042) | \~5 years | Exploratory extension; double extraction required |

**Series codes, June 11, 1999 vintage** (read from the release's [coded tables](https://www.federalreserve.gov/releases/z1/19990611/Coded/); zip download was blocked from the workspace, so confirm against the zip when downloaded):

| Concept | Flow, SA annual rate (D.2 / F.100, F.101) | Level, SA (D.3) | Current-vintage code |
| --- | --- | --- | --- |
| Households, credit market instruments | FA154102005 | LA154102005 | FL154104005 (households, debt securities and loans) |
| Nonfinancial business, credit market instruments | FA144104005 | LA144104005 | FL144104005 (unchanged) |
| of which nonfinancial corporate | FA104104005 | LA104104005 | — |

**Mapping finding:** the household code changed between vintages (154102005 → 154104005), alongside the renaming of "credit market instruments" to "debt securities and loans". The business code is unchanged. Both must be linked in the mapping table, with the date of the change identified.

**FRASER coverage, 1989–1996.** All quarterly releases are present except two:

- **Dec 1991:** no December release; the Jan 31, 1992 "Annual Revisions" release appears to carry 1991Q3 data in its place.
- **Q3 1995:** no release between Sep 13, 1995 and Mar 8, 1996 (possibly the government shutdown).

Under the existing late-release rule (§6), affected origins use the latest earlier vintage and record a larger k\_o. Year-end special editions ("Financial Assets and Liabilities", "Annual Total Flows") are not quarterly vintages and are excluded.

**Open items from this entry:**

- [ ] Download the June 1999 zip on a machine with access and confirm the codes above against the .prn headers
- [ ] Confirm what quarter the Jan 31, 1992 release covers, and search for a 1995Q3 release outside FRASER (Fed library or Board publications)
- [ ] Verify the series codes for at least one vintage per year 1999–2015, to date the household code change

### Entry 2 — 17 Oct 2026: June 11, 1999 zip files downloaded and checked

**Result: household codes confirmed in the raw files for flow, level and growth; business flow and growth confirmed. Business level, the D.2/D.3 files, the last-row check and the value spot check are still open.**

| File (table) | Codes found in header | Confirms |
| --- | --- | --- |
| ltabs.zip (L.1, sector summary of levels) | FL154102005.Q; business as components FL104104005.Q, FL114102005.Q, FL134102005.Q | Household level code in this vintage is **FL154102005**; the current vintage uses FL154104005, so the code change is confirmed from the raw file |
| gtabs.zip (D.1, debt growth rates) | FG154102005.Q, FG144104005.Q | Household and business codes exist in the D-table set |
| atabs.zip (F.1, borrowing summary) | FA154102005.Q; business as components FA104104005.Q, FA114102005.Q, FA134102005.Q | Household flow code. FA894104005.Q appears twice: the second half of a two-part file |
| atabs.zip, atab100d.prn / atab101d.prn (F.100, F.101) | FA154102005.Q / FA144104005.Q | Household and business flow codes (as reported by Andy) |

**File hashes (SHA-256):**

| File | SHA-256 |
| --- | --- |
| gtabs.zip | F55C45BEC616807F2BF1E3FF83005606C668562E24FBD990B0B325794350A55E |
| atabs.zip | D0269B923838D45873CDC901486675AF56AB4D4AC15D3EC1597C031385A80F89 |
| ltabs.zip | 423F13B585CC04FADE3D0BB0A8F78D905B610F0AF96CB386E29A107E35E5E779 |

**Open items from this entry:**

- [ ] ltab101d.prn: confirm FL144104005.Q (business total, level)
- [ ] gtabs.zip D.2 and D.3 files: confirm FA154102005.Q, FA144104005.Q, LA154102005.Q, LA144104005.Q
- [ ] Confirm the last row of each file is 1999Q1
- [ ] Spot-check household borrowing, 1999Q1, in the gtabs D.2 file against table D.2 of the [June 1999 PDF](https://www.federalreserve.gov/releases/z1/19990611/z1.pdf)

The first open item of Entry 1 (confirm codes against the zip) is partly closed by this entry.

### Entry 3 — 17 Oct 2026: Entry 2 checks 1–3 closed

**Result: all four series codes are confirmed in the raw June 1999 files, and every file ends at 1999Q1. Only the value spot check remains.**

- ltab101d.prn contains **FL144104005.Q** (business total, level).
- gtab2d.prn (D.2, borrowing) contains **FA154102005.Q** and **FA144104005.Q**.
- gtab3d.prn (D.3, debt outstanding) contains **LA154102005.Q** and **LA144104005.Q**.
- gtab1d.prn (D.1) has none of these codes, as expected: it holds growth rates under FG codes.
- Last row is 1999Q1 in all files checked.

**Spot-check values from the printed release** (table D.2 and D.3, [June 1999 PDF](https://www.federalreserve.gov/releases/z1/19990611/z1.pdf), 1999Q1, $ billions):

| Series | Printed value | Value in file |
| --- | --- | --- |
| FA154102005.Q households, borrowing (SAAR) | 556.3 | 556.25 (match) |
| FA144104005.Q business, borrowing (SAAR) | 498.1 | 498.14 (match) |
| LA154102005.Q households, outstanding (SA) | 6041.4 | 6041.37 (match) |
| LA144104005.Q business, outstanding (SA) | 5337.5 | 5337.51 (match) |

- [ ] Fill the file values and confirm they round to the printed values

**Format note (from gtab2d.prn):** dates are written "199901" (year + two-digit quarter); D.2 values are $ billions at seasonally adjusted annual rates, two decimals.

**Spot check passed (17 Oct 2026):** all four file values round to the printed release values. The June 11, 1999 vintage is confirmed for codes, units, last quarter and values. G1 data-source check for this vintage: **pass**.

### Entry 4 — 17 Oct 2026: code-change date, release dates, SPF deadlines, GDI coverage

**Result: the household code change is dated to Sep 2010. Both date tables are built. G4 passes. G3 is provisionally failing, so S3 is likely dropped while P3 runs on GDP alone.**

**1. Household code change.** Checked in the Fed's coded tables (table D.2/D.3) release by release:

| Release | Household code | Business code |
| --- | --- | --- |
| Jun 11, 1999 → Jun 10, 2010 (checked: 1999, 2003, 2007, Mar 2009, Dec 2009, Mar 2010, Jun 2010) | 154102005 | 144104005 |
| Sep 17, 2010 → present (checked: Sep 2010, Dec 2010) | 154104005 | 144104005 |

The Sep 2010 coded tables also reorder the D-table columns (federal government moves position). **Rule added to the mapping table: parse columns by series code, never by position.** The Sep 2010 release separately announced further identifier changes from Dec 9, 2010, and those are covered by the same rule. Still to do: confirm the switch in the Sep 2010 gtabs.zip headers ([data page](https://www.federalreserve.gov/releases/z1/20100917/data.htm)).

**2. Z.1 release-date table.** 95 releases, Sep 1996 → Mar 2020, transcribed from the [Fed release-dates page](https://www.federalreserve.gov/releases/z1/release-dates.htm), with format and household code per release (file: z1\_release\_dates.csv). Points to note:

- The 2003Q3 data came out on **Jan 15, 2004**; there was no December 2003 release.
- Dates are taken from the archive folder names. One looks wrong ("20170305" is a Sunday), so G2 requires checking each date against the release's own cover page before lock.

**3. SPF deadlines.** All 118 surveys from 1990Q3 to 2019Q4, from the [Philadelphia Fed release-dates file](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/spf-release-dates.txt), are linked to the latest Z.1 release before each deadline (file: spf\_deadlines\_z1\_map.csv).

- From 1999Q3 to 2019Q4, **k = 2 in 81 of 82 surveys**. The exception is 2019Q1, whose deadline the shutdown pushed to Mar 12, 2019, after the Mar 7 Z.1 release, so k = 1. The protocol's "typically 2" is confirmed.
- Shutdown-delayed surveys: 1996Q1, 2013Q4 and 2019Q1.
- **G4: pass.** All deadlines are documented; the evaluation sample is well above 40 surveys.

**4. GDI vintages in ALFRED (provisional).** ALFRED's record for [GDI](https://alfred.stlouisfed.org/series?seid=GDI) appears to begin on **Dec 20, 2012**. That would give about 29 target quarters before 2020, against the 60 that G3 requires, so **G3 provisionally fails**. Before deciding, check whether:

- [ ] ALFRED's "all vintages" download confirms the Dec 2012 start
- [ ] BEA's archive of past NIPA releases supplies first-release GDI for 1999–2012, which would mean PDF extraction

If neither source closes the gap, S3 is dropped as the protocol specifies, and P3 runs on GDP alone.

### Entry 5 — 17 Oct 2026: GDI vintage start confirmed

**Result: ALFRED's earliest GDI vintage is 2012-12-20, read from the vintage selector on the [ALFRED GDI page](https://alfred.stlouisfed.org/series?seid=GDI) (Edit Graph → select a vintage). First-release GDI is therefore available for target quarters from about 2012Q3 only, roughly 30 quarters before 2020, against the 60 that G3 requires.**

- A first download (alfredgraph.xlsx, created 2026-10-17) contained only the two most recent vintages (2026-08-26, 2026-09-30), the ALFRED default, so it was not used for this check.
- G3 stays **provisionally failing**. Two routes remain before a final decision:
  - [ ] Check the earliest vintage of [A261RC1Q027SBEA](https://alfred.stlouisfed.org/series?seid=A261RC1Q027SBEA), nominal GDI under BEA's own code
  - [ ] Decide whether to extract first-release GDI for 1999–2012 (about 54 quarters) from BEA's Survey of Current Business PDF archive
- If both routes fail, or the extraction is judged not worth the cost for an exploratory test: **G3 fails, S3 is dropped as pre-registered, and P3 runs on GDP alone.** This does not affect the confirmatory core.

### Entry 6 — 17 Oct 2026: second GDI series checked

**Result: real GDI ([A261RX1Q020SBEA](https://alfred.stlouisfed.org/series?seid=A261RX1Q020SBEA)) has its earliest ALFRED vintage on 2013-02-28, later than nominal GDI (2012-12-20). The series ID A261RC1Q027SBEA suggested in Entry 5 does not exist (404) and is withdrawn.** No ALFRED GDI series covers 1999–2012.

**Decision pending (Andy):** extract about 54 quarters of first-release GDI from BEA's Survey of Current Business PDFs, or record **G3: fail → S3 dropped; P3 runs on GDP alone**. Recommended: record the fail. S3 is exploratory, and the extraction cost is high relative to its value.

### Entry 7 — 17 Oct 2026: G3 decision

**Decision (Andy): G3 is recorded as failed.** No ALFRED GDI series has vintages before Dec 2012 (Entries 5–6), and extracting first-release GDI from BEA PDFs was judged not worth the cost for an exploratory test.

**Consequences, applied to the protocol before lock:**

- **S3 is dropped.** Its row in §4 and its text in §9 are marked as dropped, not deleted.
- **P3 is unchanged.** It is anchored to the advance GDP estimate and never depended on GDI.
- **The confirmatory core is unchanged:** P1a, P1b, P2a and P3, under Holm.

**Gate status after Phase 0 so far:** G1 pass (from 1999Q3) · G2 pending (release dates to verify against cover pages) · G3 fail · G4 pass.

### Entry 8 — 17 Oct 2026: G2 spot check of Z.1 release dates

**Result: 8 of 83 in-scope release dates checked against the releases' own pages. Seven match; one is corrected. G2 stays pending until all 83 are verified.**

| Folder date | Printed date | Source | Status |
| --- | --- | --- | --- |
| 1999-06-11 | June 11, 1999 | data page | Match |
| 2001-09-18 | Tuesday September 18, 2001 | cover PDF | Match (delayed after 9/11) |
| 2003-06-05 | June 5, 2003 | release page | Match |
| 2004-01-15 | January 15, 2004 | cover PDF | Match (2003Q3 data; no Dec 2003 release) |
| 2008-12-11 | December 11, 2008 | release page | Match |
| 2013-09-25 | September 25, 2013 | release page | Match |
| **2017-03-05** | **March 9, 2017** | cover PDF | **Corrected**: the archive folder name is not the release date |
| 2019-09-20 | September 20, 2019 | release page (last update) | Match |

- Only one in-scope folder date fell on a weekend (2017-03-05), and that was the error.
- The correction does not change the SPF mapping: the 2017Q2 deadline (May 9) falls after either date.
- **Lesson for the mapping table:** archive folder names are identifiers, not dates. Every date must come from the release itself.

* [ ] Verify the remaining 75 dates by running verify\_z1\_dates.ps1 (reads each release page and flags mismatches); record the result as a new entry

### Entry 9 — 17 Oct 2026: G2 complete

**Result: all 83 in-scope Z.1 release dates (Jun 1999 → Dec 2019) are verified against the releases' own pages. G2: pass.**

- verify\_z1\_dates.ps1, run by Andy on 17 Oct 2026, read every release page and flagged one mismatch: folder 20160609, whose page shows "Last update" 2016-09-09.
- That release's [cover PDF](https://www.federalreserve.gov/releases/z1/20160609/z1.pdf) prints **June 9, 2016** (First Quarter 2016), so the table date is correct. The page's "last update" reflects a later re-posting, not the release.
- Including the 2017 correction in Entry 8, the release-date table has **one corrected date and no other errors**.

**Phase 0 gate summary:** G1 pass (confirmatory sample from 1999Q3) · G2 pass · G3 fail (S3 dropped) · G4 pass. **Phase 0 go decision: GO.**

### Entry 10 — 19 Oct 2026: Phase 1, credit vintages downloaded and parsed

**Result: all 83 releases (Jun 11, 1999 → Dec 12, 2019) plus the current release downloaded with none missing. Household and business borrowing (flow, SAAR) and debt outstanding (level, SA) extracted from every vintage and expressed in $ billions. Parser: 84 vintages OK, 0 flags.**

**File formats:**

| Releases | File | Debt tables | Units |
| --- | --- | --- | --- |
| Jun 1999 → Dec 2010 | Disk/gtabs.zip (.prn) | gtab2d.prn (D.2), gtab3d.prn (D.3) | **$ billions** |
| Mar 2011 → Jun 2016 | Disk/gtabs.zip (.prn) | gtab2d.prn, gtab3d.prn | **$ millions** |
| Sep 2016 → Dec 2019 | z1\_csv\_files.zip | d2.csv, d3.csv | $ millions |
| Current (Sep 2026) | z1\_csv\_files.zip | **D3\_t.csv** (transactions), **D3\_s.csv** (levels); D.2/D.3 merged and renamed "D3" | $ millions |

**Findings:**

1. **Undocumented units switch at the Mar 10, 2011 release.** The .prn debt files moved from billions to millions with no change in file names. It was detected by the parser's continuity check as a median level ratio of **exactly 1000.000** between the Dec 2010 and Mar 2011 vintages, then a ratio of 0.001 at the Sep 2016 format change under an earlier rule. **Rule adopted:** divide by 1,000 for every vintage from Mar 10, 2011 onward. After the fix, no consecutive pair of vintages differs by more than a factor of 2 in median level.
2. **Table renaming in the current release:** D.2 and D.3 are now D3\_t and D3\_s. Added to the mapping table.
3. **Plausible large revisions to spot-check later:** 2019Q3 levels in the Dec 2019 vintage vs today: households $15,985bn → $15,759bn; business $15,987bn → $17,047bn (+$1,060bn).

**Process notes:** the continuity check was first run quarter by quarter on flows as well as levels, which gave thousands of false flags (flows cross zero). It was replaced by a median ratio on levels only, before any results were examined. Files: download\_z1.ps1, parse\_z1.py (v4), download\_log.csv (SHA-256 per file), credit\_vintages\_long.csv, parse\_report.csv.

### Entry 11 — 19 Oct 2026: Phase 1, real-time credit dataset, revision study and D2

**Result: credit flows are revised modestly; the credit-to-GDP gap is revised heavily, and almost entirely because of the filter's end point, not the data.** This is descriptive only. No forecasts were computed.

**Build decisions (fixed before any results were examined):**

- Common start 1953Q1. Quarterly flow = SAAR/4. Credit = households + nonfinancial business.
- RTDSM vintages dated to the 15th of the middle month. Each Z.1 vintage is paired with the latest RTDSM vintage published before its release date, which supplies the GDP denominator and the deflator.
- Origin–release table: 82 origins (1999Q3–2019Q4). The latest Z.1 release before each origin gives q\* and k. **k = 2 at every origin.**
- Three versions per quarter: *real time* (first release); *credit-revised* (current Z.1 credit, real-time GDP, which isolates credit-data revisions for S1); and *revised* (current Z.1 with the latest GDP vintage).
- Gap: one-sided HP filter, λ = 400,000, at least 40 quarters of history, recomputed in every vintage. The final gap for D2 is a two-sided HP filter on revised data through 2019Q4. Ending the filter in 2026 instead moves the 1999–2019 final gap by up to 3.3 pp, so it is reported as a sensitivity check.

**Validation:** every Z.1 release has a GDP vintage covering q\*. corr(ΔL, F) = 0.98 in the Dec 2019 vintage. Hand check: CI for 2008Q3 in the Dec 2008 vintage = (1,036 − 2,101) / ≈14,200 = −7.49, which matches the pipeline.

**Revision statistics, first release vs revised, 83 quarters (1999Q1–2019Q3):**

| Measure | Mean revision | SD revision | Noise/signal | Corr | Sign agreement |
| --- | --- | --- | --- | --- | --- |
| Credit impulse (CI) | +0.03 | 0.95 | 0.28 | 0.96 | 86% |
| Credit growth (CG) | −0.19 | 0.69 | 0.18 | 0.99 | 98% |
| Real credit growth (RCG) | −0.30 | 0.70 | 0.21 | 0.98 | 95% |
| Gap, data part only | −1.13 | 1.32 | 0.14 | 0.99 | 100% |

**Findings:**

1. **GDP revisions barely matter for CI.** Credit-only revisions (noise/signal 0.28) are as large as total revisions (0.28), so the S1 credit-revision premium is the relevant object. CG involves no GDP, so its credit-only and total revisions are identical by construction.
2. **CI is noisier in expansions than in recessions** (noise/signal 0.38 vs 0.21). The largest revisions came at the 2008 turning point: 2008Q3 first release −7.5 vs revised −5.2.
3. **D2: the filter accounts for essentially all of the gap's unreliability.** Variance shares of the total gap revision: data 3%, end-point filter 108%, covariance −11%. Mean absolute revision: data 1.4 pp vs filter 7.0 pp. Corr(real-time, final) = 0.65; the sign agrees in 76% of quarters. This replicates Edge–Meisenzahl in a new sample. It also supports keeping the gap exploratory and putting the flow measures at the centre.

**Caption note, Fig. 2 (gap):** the real-time gap moves for reasons that have nothing to do with credit.

- **It rose during the 2001 recession** (4.5 → 11 by 2003Q2). Credit kept growing at 7–9% while GDP slowed, so debt/GDP jumped from 137% to 152%. This is a denominator effect, a known flaw of the credit gap (Repullo and Saurina, 2011).
- **It fell in 2003–05** (11 → 8) while credit was accelerating (7.5% → 9.3%). Debt/GDP had flattened and the one-sided trend was still catching up with the earlier jump. It was not a warning signal.
- **It stayed near 10 through 2005–08.** Debt/GDP rose 21 points, but the trend absorbed 18 of them. In 2009Q2 the gap still read +5.8.

The final two-sided gap, rising steadily to +19 in 2008, relies on hindsight about the 2010s deleveraging. The real-time warning before 2008 appears in the impulse, which fell from about +4 in early 2006 to about −1 by mid-2007 (Fig. 1), not in the gap. Whether that warning had forecasting value is left to P1/P2a.

**Files:** build.py, build2.py, study.py, charts.py; origin\_release\_table.csv, credit\_measures\_by\_vintage.csv, credit\_measures\_revised.csv, first\_release\_vs\_revised.csv, revision\_stats.csv, gap\_decomposition\_D2.csv; fig1\_first\_release\_vs\_revised.png, fig2\_gap\_decomposition\_D2.png.

**Still to do in Phase 1:** power simulation (§11); placeholders; lock.

### Entry 12 — 19 Oct 2026: Phase 1, power simulation (§11)

**Result: at a true RMSE ratio of 0.90, Holm-adjusted power is 0.82 for P1a, 0.75 for P1b, 0.82 for P2a, and 0.53 for P3 (partial R² 0.05). The minimum detectable effect at 80% power is a ratio of about 0.90 (a 10% gain). Gains of 5% are detected about half the time.** No forecasts on actual data were computed.

**Design (written before the run):**

- **Data-generating process.** AR(2) processes fitted to revised CI, GDP growth and the unemployment level, 1955Q1–2019Q4. The shocks are jointly normal, using the residual covariance from those fits. Credit's effect is *imposed*: κ × CI at lag 6 (q\* = o − 2 → target o + 4), with κ chosen by bisection on a 300,000-quarter population run so that the true RMSE ratio of the direct ADL against AR(2) equals the stated value. The credit–target relationship was never estimated on real data.
- **Real-time noise.** The value at the edge (o − 2) carries N(0, 0.946²), the total revision SD of CI from Entry 11. Training rows use settled values.
- **Tests.**
  - P1a and P1b: 78 origins (1999Q3–2018Q4); expanding OLS from 1955Q3; the training sample ends at target ≤ o − 1; Clark–West with NW HAC (h − 1 = 3 lags), one-sided.
  - P2a: an SPF proxy = the population AR-information forecast plus N(0, 0.5²) idiosyncratic noise; bias-corrected benchmark; correction trained from 1969Q1.
  - P3: 82 quarters, partial R² of 0.02, 0.05 and 0.10, two-sided NW t-test (3 lags).
  - Holm across all four tests. 2,000 replications per cell.

| True ratio (P3 R²) | P1a | P1b | P2a | P3 | Any rejection | All four |
| --- | --- | --- | --- | --- | --- | --- |
| 1.00 (0) — size | 0.024 | 0.034 | 0.023 | 0.032 | 0.083 | 0.000 |
| 0.95 (0.02) | 0.51 | 0.41 | 0.52 | 0.20 | 0.66 | 0.10 |
| 0.925 (0.02) | 0.69 | 0.58 | 0.69 | 0.25 | 0.81 | 0.17 |
| **0.90 (0.05)** | **0.82** | **0.75** | **0.82** | **0.53** | 0.91 | 0.43 |
| 0.875 (0.05) | 0.90 | 0.87 | 0.90 | 0.56 | 0.96 | 0.50 |
| 0.85 (0.10) | 0.94 | 0.93 | 0.94 | 0.85 | 0.98 | 0.80 |

Holm-adjusted power; unadjusted power is in power\_results\_R2000.csv.

**Findings needing a decision before lock:**

1. **Size distortion.** Under the null, unadjusted rejection rates are 5.9% (P1a), 7.8% (P1b), 5.8% (P2a) and 8.8% (P3), against a nominal 5%. The family-wise false-positive rate is 8.3% against a nominal 5%. NW HAC with a small n over-rejects. *Proposed:* use fixed-b critical values (Kiefer–Vogelsang), as listed in the red-team fix (§6c), and re-run the size row only.
2. **Which wording rule applies.** Read test by test at a ratio of 0.90: P1a and P2a fall in the ≥ 0.80 band; P1b and P3 fall in the 0.50–0.80 band. No test falls below 0.50, so none moves to exploratory. *Proposed:* apply the rule test by test, which needs one clarifying sentence in §11.
3. **The expectation statement in §11 is worded backwards.** "Minimum detectable ratio above 0.95, meaning only gains larger than 5% can be detected" should read "below 0.95". Read as intended, the statement is triggered: the minimum detectable ratio is about 0.90.

**Caveats:** credit acts through a single lag; edge noise is i.i.d.; the SPF is a stylised proxy; P3 errors are i.i.d. Each caveat is a simplification and is reported as such.

**Files:** calib.py, power.py, calib.npz, power\_results\_R2000.csv.

### Entry 13 — 19 Oct 2026: power re-run with fixed-b inference; placeholders filled

**Decisions applied (Andy, 19 Oct 2026, before any forecast):** fixed-b critical values; the §11 rule applied test by test; the §11 expectation-statement wording corrected ("above" → "below" 0.95).

**Fixed-b critical values** for the Bartlett-kernel NW t-statistic with 3 lags (b ≈ 0.05), simulated with 20,000 draws at T = 2,000: one-sided 5% = 1.781 (n = 78); two-sided 5% = 2.091 (n = 82). These agree with the Kiefer–Vogelsang (2005) polynomial approximation (1.757 and 2.105) to within simulation error. The full simulated null distributions are used for p-values, which then enter Holm.

| True ratio (P3 R²) | P1a | P1b | P2a | P3 | Any rejection | All four |
| --- | --- | --- | --- | --- | --- | --- |
| 1.00 (0) — size, unadjusted | 0.050 | 0.066 | 0.044 | 0.074 | — | — |
| 1.00 (0) — size, Holm | 0.020 | 0.026 | 0.017 | 0.021 | 0.064 | 0.000 |
| 0.95 (0.02) | 0.45 | 0.36 | 0.46 | 0.17 | 0.61 | 0.08 |
| 0.925 (0.02) | 0.64 | 0.53 | 0.64 | 0.21 | 0.76 | 0.14 |
| **0.90 (0.05)** | **0.77** | **0.70** | **0.77** | **0.48** | 0.89 | 0.37 |
| 0.875 (0.05) | 0.87 | 0.82 | 0.87 | 0.51 | 0.94 | 0.44 |
| 0.85 (0.10) | 0.91 | 0.90 | 0.91 | 0.82 | 0.98 | 0.75 |

**Findings:**

1. **Size is mostly fixed.** The family-wise false-positive rate falls from 8.3% to 6.4%. A residual excess remains for P1b (6.6%) and P3 (7.4%), against a Monte Carlo SE of about 0.5 pp; it is reported, not corrected further.
2. **Minimum detectable effect at 80% (Holm):** RMSE ratio 0.89 for P1a and P2a, 0.88 for P1b; partial R² of about 0.095 for P3. The expectation statement is triggered.
3. **Bands, test by test:** P1a, P1b and P2a fall in the 0.50–0.80 band ("not detected; gains larger than \[upper 90% bound\] ruled out"). **P3 = 0.48, just below 0.50:** decision pending (see below).

**Revised-target vintage frozen:** RTDSM 2026Q3, downloaded 19 Oct 2026. SHA-256:

- ROUTPUTQvQd.xlsx 25433da00f46764a167590efe5c3e1c20a3e91e98ba0f49e6f92f058bc42c9e3
- rucQvMd.xlsx d971e59d3ed5f1322a46631743508fb1ad5eee39bfbe12425a641a277fdd9b9a
- NOUTPUTQvQd.xlsx c8202c095afbb8a3bd4470c8b61a6413a3d66922657395ef3efcc13cce7429ee
- PQvQd.xlsx c9f7336fab2e8559c2730a69c86fb36a5324d2651a81d767491220f637dbedd1
- routput\_fst.xlsx 2bffa7a68ad43a950a04cb378a368b5e59192b1febcfe22d2a0e110132bfc9c5

**Placeholders filled:** the revised-target date (§5), the minimum detectable ratio (interpretation map, two cells), the §11 result, and the expectation-statement value. Placeholders that remain by design: "\[upper 90% bound\]", which is filled from results; the E2 benchmark threshold, awaiting sign-off.

**Files:** fixedb.py, power.py (fixed-b version), power\_results\_fixedb\_R2000.csv. The earlier normal-critical-value run (Entry 12) is kept for the record.

### Entry 14 — 19 Oct 2026: decisions on P3 and E2

- **P3 (decided by Andy):** the §11 rule is applied as written. Power of 0.48 at partial R² 0.05 is below 0.50, so P3 is reported as an estimate only, with no significance language. The effect-size pairing was not revisited after the power results were seen. P3 stays in the confirmatory core and the Holm family.
- **E2 (decided by Andy):** the benchmark-release threshold of 0.25 × SD of the revised impulse is agreed.
- **Still required before lock (§14):** Phase 2 analysis code written and tested on synthetic data only; the SPF input files (MedianGrowth.xlsx, SPFmicrodata.xlsx and the median unemployment file) downloaded and hashed; the lock bundle assembled and published as a tagged public commit.

### Entry 15 — 19 Oct 2026: SPF input files downloaded, hashed and checked

**Result: all four files were downloaded from the Philadelphia Fed (all versions dated 14 Aug 2026), and the hashes computed on Andy's machine match those recomputed after upload. The layouts are as the protocol assumes.**

| File | Bytes | SHA-256 |
| --- | --- | --- |
| medianGrowth.xlsx | 144,611 | FDCF9CA0299DE022C58F8FC35FD20761D8E52B45E038781AE3C4826D1A3CBB5C |
| medianLevel.xlsx | 554,444 | D296E737331C406F7680414504A0D005472743709387F8FDA6D969A1D2200977 |
| SPFmicrodata.xlsx | 24,612,638 | D45AF2EAEBE11E8C7A0635D3F868D5D85897E5BC5CC3D8CB477C243B31FAA076 |
| spf-caveats.pdf | 15,843 | D29674D2E6816C14A86755C7BA8D0922993A1ECBBEE7CA4321E1993B863F126F |

**Layout checks:**

1. **GDP.** The growth file's RGDP sheet holds columns drgdp2–drgdp6 (lower case in the file; "dRGDP6" in the protocol refers to drgdp6). Hand check, 2008Q1 survey: (RGDP6 / RGDP5)^4 − 1 = (11,989.93 / 11,898.11)^4 − 1 = 3.12%, which matches drgdp6 = 3.1227. This confirms that drgdp6 is the discretely compounded, annualised growth of the median levels, for quarter o + 4.
2. **Unemployment.** UNEMP6 is in the level file's UNEMP sheet, for quarter o + 4.
3. **Coverage.** Both series start with the 1968Q4 survey; 5 surveys between 1969 and 1974 are missing. Correction training therefore has far more than the 20 pairs required before 1999Q3.
4. **Microdata.** The RGDP sheet has one row per forecaster per survey (YEAR, QUARTER, ID, INDUSTRY, RGDP1–RGDP6). In 1999–2019 there are 29–53 forecasters per survey (median 40.5).
5. **ID caveats** (spf-caveats.pdf). IDs may be reused in the NBER/ASA era, and may follow either the firm or the person after a job change. **Not material here:** the robustness series needs IDs only *within* a single survey, to pair one forecaster's RGDP5 and RGDP6. It never tracks IDs across surveys.
6. **Note.** Before 1992 the SPF's output variable is real GNP. This is consistent with the RTDSM, whose early vintages also measure GNP, provided targets are always taken from the vintage rule in §5. It affects correction training only, not the evaluation sample.

No forecast was computed, and no SPF error was examined.

### Entry 16 — 19 Oct 2026: power simulation corrected to match the protocol's model specification

**Error found (by Claude, while reading §6–§10 to write the Phase 2 code; no forecasts had been computed).** The simulations in Entries 12–13 departed from the locked-text specification in four ways:

1. The ADL used one credit lag, where §8 specifies X\_{q\*−j} for j = 0–3.
2. Estimation started in 1955, where §8 specifies 1965Q1.
3. The SPF correction trained from 1969 with a free coefficient on the SPF, where §8 specifies SPF + α̂ + β̂·CI\_{q\*}, with the SPF coefficient fixed at 1, trained on surveys from 1990Q3 only.
4. P3 omitted the §9 controls (advance g\_s and g\_{s−1}) and used 3 HAC lags instead of 4, with n = 82 instead of 83 (s = 1999Q2–2019Q4).

Entries 12–13 are superseded for the rule selection but kept for the record.

**Corrected run** (power2.py; fixed-b nulls for n = 78 with 3 lags and n = 83 with 4 lags; 2,000 replications). P2a's power is read against its own true ratio: under the restricted correction, a given credit effect yields a smaller SPF gain.

| True ratio (P3 R²) | P1a | P1b | P2a (own ratio) | P3 | Any rejection | All four |
| --- | --- | --- | --- | --- | --- | --- |
| 1.00 (0), size, unadjusted | 0.047 | 0.067 | 0.040 | 0.070 | — | — |
| 1.00 (0), size, Holm | 0.012 | 0.024 | 0.014 | 0.021 | 0.063 | 0.000 |
| 0.95 (0.02) | 0.35 | 0.28 | 0.28 (0.96) | 0.18 | 0.54 | 0.06 |
| 0.925 (0.02) | 0.55 | 0.39 | 0.46 (0.94) | 0.17 | 0.68 | 0.08 |
| **0.90 (0.05)** | **0.71** | **0.58** | 0.63 (0.92) | **0.45** | 0.85 | 0.27 |
| 0.875 (0.05) | 0.81 | 0.69 | 0.74 (0.90) | 0.48 | 0.91 | 0.35 |
| 0.85 (0.10) | 0.88 | 0.79 | 0.83 (0.88) | 0.79 | 0.96 | 0.62 |

**Holm-adjusted power at a true ratio of 0.90:** P1a 0.71, P1b 0.58, P2a 0.75 (interpolated at its own ratio of 0.90), P3 0.45. **Minimum detectable effect at 80%:** ratio 0.88 for P1a, 0.85 for P1b and 0.89 for P2a; partial R² just above 0.10 for P3.

**Consequences.** The band assignments are unchanged: P1a, P1b and P2a are in 0.50–0.80, and P3 is below 0.50, so it is reported as an estimate only (Entry 14 decision stands). The minimum-detectable-effect values in §4a, §11 and the expectation statement are corrected from "about 11%" to about 12% (GDP) and 15% (unemployment). The size excess remains: 6.3% family-wise; P1b 6.7%; P3 7.0%.

**Lesson for Phase 2:** the analysis code is written directly from §6–§10, and each specification element is listed against the protocol section that defines it.

### Entry 17 — 19 Oct 2026: Phase 2 code written and tested on synthetic data; protocol fixes

**Code.** phase2.py implements §5–§10 in full: information sets, models, the core tests with Holm, the grid and S1, S2, S4 (Minnesota BVAR), S5, S6, R1 (Y and Z), E1, E2, D1, the rolling-window and h = 1, 2 robustness checks, and the unemployment direction metric. Real mode refuses to run without LOCK.json (release URL, tag commit, DOI).

**Synthetic tests** (test\_phase2.py). Credit is real; all targets, GDP and unemployment vintages, SPF series and yields are simulated, so no real outcome was read.

- Sample sizes match the protocol: P1a, P1b and P2a 78 each; P3 83; 32 SPF training pairs at the first origin.
- A planted P3 effect of 0.80 is recovered as 0.77–0.80.
- Over 30 seeds, the false-positive rate for the forecast tests is 3%. The full run takes 24 s.
- Two coding bugs were found and fixed: E1 parameter indexing, and a date/lag misalignment in E1.

**Disclosure: D1 seen before lock.** D1 uses only credit data and NBER dates, so the synthetic smoke test computed the real D1 result. In 2001 and 2007–08, both real-time signals switched on at or after the peak ("late"). D1 is descriptive, uses no forecast target and has no decision attached. It is recorded here as seen before lock.

**Protocol fixes (agreed by Andy):**

1. The §2 premium sign is corrected (real-time ratio minus revised-credit ratio; positive means revised credit forecasts better).
2. The E1 specification is written into §8.

**New input.** FRED GS2 (2-year Treasury, monthly, 1976-06 to 2026-09), 9,742 bytes, SHA-256 57607a5c6474c1ea02f7f3aac5600f63a3157ef357c2afc05e63f9c69f56bab5. Quarterly averages over complete quarters; the BVAR sample starts in 1976Q3.

### Entry 18 — 19 Oct 2026: power conditional on the actual credit path; P3 size

**Finding.** In synthetic runs using the real credit path, almost all of credit's forecasting gain comes from the 2008–09 collapse. The Clark–West loss differential is then highly skewed, and the test has little power even for large average gains. The earlier simulations (Entries 12, 13 and 16) drew CI from a Gaussian AR(2) and did not capture this. A simulation conditional on the actual revised credit path (power\_realpath.py; targets, vintages and SPF simulated; 200 replications per cell) gives:

| Median true ratio (P1a / P1b / P2a) | Unadjusted power P1a | P1b | P2a | Holm P1a | Holm P1b | Holm P2a |
| --- | --- | --- | --- | --- | --- | --- |
| \~1.02–1.04 (null) | 0.055 | 0.045 | 0.035 | 0.015 | 0.005 | 0.010 |
| 0.96 / 0.97 / 0.97 | 0.33 | 0.26 | 0.34 | 0.07 | 0.12 | 0.07 |
| **0.91 / 0.93 / 0.93** | **0.45** | **0.31** | **0.51** | 0.09 | 0.12 | 0.11 |
| 0.82 / 0.85 / 0.86 | 0.57 | 0.43 | 0.71 | 0.10 | 0.13 | 0.11 |

The Holm figures are further depressed in this harness because a P3 effect was planted alongside, so P3 is rejected first and the remaining tests face thresholds of 0.05/3 and below.

**P3 size.** Conditional on the real credit path, the fixed-b HAC test of P3 over-rejects: 14–18% at a nominal 5%, because a few extreme CI values dominate. A restricted wild (Rademacher) block bootstrap-t (block 4, 999 draws) gives 3.5% size, and power of 0.43 at a modest planted effect.

**Decisions pending before lock (Andy):**

- (a) whether the §11 bands are set from the conditional-on-path power. Under that power every confirmatory test falls in the < 0.50 band (estimate only).
- (b) whether P3 inference moves to the wild block bootstrap.

No real target or SPF error has been examined.

### Entry 19 — 19 Oct 2026: decisions on conditional-path power, P3 inference and the crisis share

**Decisions (Andy, 19 Oct 2026; no real target or SPF error examined):**

1. The §11 bands are set from power conditional on the actual credit path. All four confirmatory tests fall in the < 0.50 band and are reported as estimates with 90% intervals; "credible improvement" applies only if the interval lies wholly below 1.00 (for P3, excludes zero). This supersedes the band assignments of Entries 14 and 16.
2. P3 uses a restricted wild (Rademacher) block bootstrap of the HAC t-statistic (block 4, 999 draws) for its p-value and 90% interval (§9 amended). The fixed-b HAC p-value is retained in the output for comparison only.
3. A descriptive statistic is added to §13: the share of the total squared-error gain from origins 2007Q1–2010Q4, reported with the signed total.

**Checks of the new rule** (ci\_check.py; real credit path, simulated targets; 100 seeds; 500 bootstrap draws). False "credible improvement" rate with no true effect: P1a 0%, P1b 2%, P2a 2%. With true ratios of 0.92–0.94: detected 32%, 29% and 40% of the time.

**Reliable detection threshold.** From the conditional-path runs (Entry 18 and test\_phase2.py), unadjusted P1a power is 0.57 at a ratio of 0.82 and 0.87 at 0.52. 80% power therefore needs a ratio of about 0.6, a gain of roughly 40%. The §4a null sentence, the interpretive-map cell and the expectation statement now say this, replacing the earlier 11–15% figures.

**Code updated:** phase2.py (wild\_block\_t, crisis\_share, estimate-only bands and the credible-improvement flags). Synthetic smoke test passes (40 s).

## Sources

**Sources used by protocol v2.3** (data, methods, definitions)

- [Philadelphia Fed Real-Time Data Set for Macroeconomists](https://philadelphiafed.org/research-and-data/real-time-center/real-time-data)
- [SPF documentation (Philadelphia Fed, July 2026)](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/spf-documentation.pdf)
- [Fed Z.1 release archive (example, June 2013)](https://www.federalreserve.gov/releases/z1/20130606/)
- [FRASER Z.1 archive](https://fraser.stlouisfed.org/title/93/item/579649)
- [ALFRED search: Z.1 series vintages](https://alfred.stlouisfed.org/search?st=z1)
- [Biggs, Mayer & Pick, credit impulse definition (VoxEU)](https://cepr.org/voxeu/columns/myth-phoenix-miracle)
- [CASE: origin and date of the credit impulse (Biggs 2008)](https://case-research.eu/en/case-starts-to-publish-a-quarterly-update-on-credit-impulse-100774)
- [Keen, credit accelerator definition (2011)](https://nakedcapitalism.com/2011/06/steve-keen-dude-where’s-my-recovery.html)
- [López-Buenache, Borsi & Rosa-García (2025), *Economic Analysis and Policy* 88](https://www.recercat.cat/handle/20.500.14342/5700) · [2020 working paper (MPRA)](https://mpra.ub.uni-muenchen.de/100523)

* [Edge & Meisenzahl (2011), The unreliability of credit-to-GDP ratio gaps in real time, FEDS 2011-37 / *IJCB* 7(4)](https://www.federalreserve.gov/econres/feds/the-unreliability-of-credit-to-gdp-ratio-gaps-in-real-time-implications-for-countercyclical-capital-buffers.htm)

Sources behind the earlier red-team sections are linked inline there and are not inputs to the protocol.
