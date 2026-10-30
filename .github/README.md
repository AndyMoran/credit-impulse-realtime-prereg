# Real-time US macro forecasting, 1999–2019: credit, a survey and foundation models

A series of preregistered tests of one question: **what, beyond GDP's own recent history, helps forecast US GDP growth in real time?** Each test was planned, frozen and tagged before any result was seen, using only the data a forecaster had on each date.

Andy Moran (Heaviside Analytics) · MIT licence

## The answer so far

Nothing tested beat a direct AR(2), GDP growth predicted from its own last two quarters, at 78 quarterly origins, 1999Q3–2018Q4.

| Study | Question | Result | Archive |
| --- | --- | --- | --- |
| **Credit impulse** (the main study) | Did the real-time credit impulse improve forecasts of GDP growth and unemployment four quarters ahead? | No. GDP: RMSE ratio 1.106 (90% interval 0.984–1.356); unemployment 1.011; SPF correction 1.025. Revisions to the credit data change nothing. | Working paper v2.2, [10.5281/zenodo.23560860](https://doi.org/10.5281/zenodo.23560860) |
| **TimesFM** | Does Google's TimesFM 2.5 or 3.0, used as published, beat the AR(2)? Does credit help it? | No. Ratios 1.015 and 1.004; credit did not help. | [10.5281/zenodo.23675487](https://doi.org/10.5281/zenodo.23675487) |
| **Survey horizon sweep** (Plan 2) | At which horizon does the Philadelphia Fed's Manufacturing Business Outlook Survey help? | Not credibly at any. At one quarter ahead, 0.930 (0.869–1.038); the point gains fade from 9% now to 1% a year out, and the quarter-ahead gain vanishes without 2008–09. | [10.5281/zenodo.23777951](https://doi.org/10.5281/zenodo.23777951) |
| **Timestral** | Does Mistral's Timestral-209M beat the AR(2)? Does credit help it? | No. Ratio 1.018 (0.960–1.093); credit did not help; about as accurate as both TimesFM models. | [10.5281/zenodo.23812724](https://doi.org/10.5281/zenodo.23812724) |

Ratios are RMSE ratios, model ÷ benchmark; below 1 means the model forecast better. A "credible improvement" requires the whole 90% interval to lie below 1. The tests are underpowered for small gains, and each write-up states its detection limit: read every null as "no gain detected", not "no effect".

**The reading.** When a two-lag model, three foundation models and a timely survey all stall at the same point, the limit is the information in the data, not the model. Foundation models were tested here on a short, quarterly, heavily revised series, the case least favourable to them; an energy-data test is next.

## Where to start

| To read | Go to |
| --- | --- |
| The main study | [`paper/manuscript_v2.2_2026-10-22.pdf`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/blob/main/paper/manuscript_v2.2_2026-10-22.pdf) |
| The TimesFM note | [`timesfm/`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/tree/main/timesfm) |
| The survey results | [`plan2/RESULTS.md`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/blob/main/plan2/RESULTS.md) |
| The Timestral results | [`timestral/RESULTS.md`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/blob/main/timestral/RESULTS.md) |
| Every deviation from a plan | [`DEVIATIONS.md`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/blob/main/DEVIATIONS.md) and each study's results file |
| How to reproduce | [`REPLICATION.md`](https://github.com/AndyMoran/credit-impulse-realtime-prereg/blob/main/REPLICATION.md) |

## How each test was run

1. **Plan first.** Every choice, including the wording of each possible result, was written down before any forecast was scored.
2. **Freeze in public.** The plan and scripts were committed and tagged; the tag's timestamp is the evidence of timing.
3. **Run under a gate.** The official run is the first that passes pre-specified validity checks (from Plan 2 onwards; earlier studies ran once).
4. **Report everything,** in the pre-written sentences, with every deviation dated and marked as made before or after results were seen.

## Timeline

| Date (2026) | Tag | What it fixed or released |
| --- | --- | --- |
| 19 Oct | `v1.0-lock` | Main study frozen ([10.5281/zenodo.23477871](https://doi.org/10.5281/zenodo.23477871)) |
| 19 Oct | `v2.0-results` | Main study results ([10.5281/zenodo.23479717](https://doi.org/10.5281/zenodo.23479717)) |
| 20 Oct | `pandemic-plan`, `v2.1-verification` | Pandemic-period illustration (2020–21, not preregistered as a test: all forecasts about as accurate as the benchmark) and verification kit ([10.5281/zenodo.23497087](https://doi.org/10.5281/zenodo.23497087)) |
| 22 Oct | `v2.2-publish` | Working paper v2.2 ([10.5281/zenodo.23560860](https://doi.org/10.5281/zenodo.23560860)) |
| 26 Oct | `timesfm-plan`, `timesfm-note` | TimesFM extension frozen, then released |
| 29 Oct | `plan2`, `plan-2-results` | Survey horizon sweep frozen, then released |
| 29 Oct | `timestral-plan`, `timestral-results` | Timestral extension frozen, then released |

## Data and licences

Raw inputs are public: the Federal Reserve's Z.1 archive, the Philadelphia Fed's Real-Time Data Set and Survey of Professional Forecasters, and FRED/ALFRED. The Philadelphia Fed survey data are not redistributed; `code_post_lock/plan2_fetch.py` downloads them with your own FRED API key. Foundation-model weights are not included; the scripts download them at pinned revisions. TimesFM 3.0 is used under Google's non-commercial licence, and its back-end script is not published.

## Related work

Carriero, Pettenuzzo and Shekhar (2026), arXiv:[2606.28670](https://arxiv.org/abs/2606.28670), find that off-the-shelf foundation models barely beat a simple autoregression on real-time US macro data beyond the short term. It was found after these plans were frozen and played no part in their design.

## The original lock

The root `README.md` is the preregistration lock's README, kept byte for byte because the lock's `MANIFEST.txt` and `verification/verify_lock.py` check its hash. This page is the current overview.

## Use of AI

The author is responsible for all design decisions, modelling runs, interpretation, and final content. AI tools (including Claude, ChatGPT, Microsoft Copilot, DeepSeek, Kimi, and Z.ai) were used for drafting text, writing and testing scripts, checking outputs, and performing sanity-checks on reasoning and code. All modelling was executed by the author, who retains full responsibility for the analysis and results.
