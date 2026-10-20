# Independent re-run: how to verify the locked results

20 October 2026 · Andy Moran (Heaviside Analytics)

## 1. What you are checking

*Did the Credit Impulse Help Forecasters in Real Time? A Preregistered Test, 1999–2019* is a preregistered study by Andy Moran (Heaviside Analytics). Its analysis code and decision rules were frozen in a public release before any result was computed, and the results come from a single run of that frozen code. The study's defence against "they tuned it after seeing the answer" rests on two claims you can check without trusting the author:

1. **The code that produced the results is the code that was locked.** The release `v1.0-lock` (GitHub, archived at DOI [10.5281/zenodo.23477871](https://doi.org/10.5281/zenodo.23477871)) predates the results, and its `phase2.py` has SHA-256 `da697030f2349feae24dc79a3dfcbb786552b62186ffbf624a027c591814766e`.
2. **Running that code on the public inputs reproduces the published numbers.** The published `results.json` (in release `v2.0-results`, DOI [10.5281/zenodo.23479717](https://doi.org/10.5281/zenodo.23479717)) has SHA-256 `9e4239dd116eaea7c9f65df83f85d349f338aeb4adb6ff16904a6793ed6fa99c`.

**A pass** means: (a) the release and Zenodo timestamps put the lock before the run (19 October 2026, lock 14:55 UTC, run 15:00 UTC); (b) every file hash below matches; and (c) your re-run gives the same `results.json`, byte for byte or, if your library versions differ, the same four confirmatory estimates to three decimals. You are not asked to judge the economics or the design, only whether the published numbers come from the locked code.

## 2. What you need

- **Time:** about an hour. The analysis itself runs in about 40 seconds.
- **Software:** Python 3.11 or later with numpy, pandas, scipy, statsmodels and openpyxl. The published run used Python 3.13, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0 and openpyxl 3.1.5. Matching these versions should give a byte-identical `results.json`; other versions may differ in the last digits.
- **The locked release** `v1.0-lock`: download it from Zenodo (DOI above) or as the source archive of the GitHub tag. It contains the code, the real-time credit vintages and `MANIFEST.txt`, the SHA-256 list for every file.
- **`LOCK.json`**: from the `results/` folder of release `v2.0-results`. The code refuses to run on real data without it. It names the release URL, tag commit and DOI.
- **Ten public input files** that the release does not redistribute. They must match the hashes below exactly. The simplest route is to take them from the author and check the hashes yourself. You can also download them from the [Philadelphia Fed Real-Time Data Set](https://philadelphiafed.org/research-and-data/real-time-center/real-time-data), the Philadelphia Fed's Survey of Professional Forecasters pages and [FRED](https://fred.stlouisfed.org/series/GS2). These files grow each quarter, so a fresh download made after the next update will not match, and the revised GDP targets would then move. If that happens, use the author's copies.

| File | SHA-256 |
| --- | --- |
| ROUTPUTQvQd.xlsx | `25433da00f46764a167590efe5c3e1c20a3e91e98ba0f49e6f92f058bc42c9e3` |
| NOUTPUTQvQd.xlsx | `c8202c095afbb8a3bd4470c8b61a6413a3d66922657395ef3efcc13cce7429ee` |
| PQvQd.xlsx | `c9f7336fab2e8559c2730a69c86fb36a5324d2651a81d767491220f637dbedd1` |
| rucQvMd.xlsx | `d971e59d3ed5f1322a46631743508fb1ad5eee39bfbe12425a641a277fdd9b9a` |
| routput\_fst.xlsx | `2bffa7a68ad43a950a04cb378a368b5e59192b1febcfe22d2a0e110132bfc9c5` |
| medianGrowth.xlsx (SPF) | `fdcf9ca0299de022c58f8fc35fd20761d8e52b45e038781ae3c4826d1a3cbb5c` |
| medianLevel.xlsx (SPF) | `d296e737331c406f7680414504a0d005472743709387f8fda6d969a1d2200977` |
| SPFmicrodata.xlsx (SPF) | `d45af2eaebe11e8c7a0635d3f868d5d85897e5bc5cc3d8cb477c243b31faa076` |
| GS2.csv (FRED) | `57607a5c6474c1ea02f7f3aac5600f63a3157ef357c2afc05e63f9c69f56bab5` |
| spf-caveats.pdf (SPF; documentation only) | `d29674d2e6816c14a86755c7ba8d0922993a1ecbbee7ca4321e1993b863f126f` |

## 3. Steps

**Step 1. Check the timeline.** On GitHub, open the `v1.0-lock` tag and note the date of commit `4eb084fb2c462fffec72574f108043ea9d796cc9`. On Zenodo, note the publication date of record 10.5281/zenodo.23477871. Both should be on or before 19 October 2026 at 14:55 UTC. The run log in `v2.0-results` (`results/run_real_log.txt`) gives the run as 15:00:47–15:01:25 UTC the same day.

**Step 2. Run the verification script.** `verify_lock.py` is in the `verification/` folder of release v2.1; the raw-input zip is attached to the same release or available from the author. It is a short, readable Python file that only checks and runs; it never edits the release or your inputs. It does every remaining check in one go: release files against the manifest, the locked `phase2.py`, the raw-input hashes and `LOCK.json`. It then runs the locked analysis once in a fresh temporary folder and compares the new `results.json` with the published one. Unzip the v1.0-lock archive into a folder `v1` and the v2.0-results archive into a folder `v2`, put the raw-input zip beside them, and run (the script finds the right subfolders itself):

```bash
python verify_lock.py --release .\v1 --results .\v2 --raw .\raw_inputs_v1.0-lock.zip
```

It prints each check, ends with `OVERALL: PASS` or `OVERALL: FAIL`, and writes `verification_report_PASS.txt` (or `_FAIL.txt`) beside itself. The author tested it both ways: on the untouched release it reproduced the published hash exactly in 39 seconds; with one character of `phase2.py` changed, it reported the code mismatch, the changed estimates and `FAIL`.

**Checking by hand (optional).** The steps below do the same checks one at a time, for anyone who would rather not rely on the script. They are numbered A to D.

**A. Check the release.** Unpack `v1.0-lock` and check every file against its manifest. The manifest also lists the raw inputs, which are not in the release; the command below leaves them out. Run it in the unpacked release folder:

```bash
cd credit-impulse-realtime-prereg
grep -v '^#' MANIFEST.txt | grep -v -E '  (RTDSM|SPF|FRED) ' | sha256sum -c
```

Every line should say `OK`. Then confirm that `code/phase2/phase2.py` has the hash given in Section 1.

**B. Assemble the working layout.** The scripts expect three folders side by side:

```text
work/phase0/spf_deadlines_z1_map.csv      <- tables/
work/p1/build.py, fixedb.py               <- code/phase1/
work/p1/data/credit_vintages_long.csv     <- data_derived/
work/p1/data/download_log.csv             <- data_derived/
work/p1/data/ROUTPUTQvQd.xlsx, NOUTPUTQvQd.xlsx, PQvQd.xlsx,
             rucQvMd.xlsx, routput_fst.xlsx, GS2.csv      <- raw inputs
work/p1/data/spf/medianGrowth.xlsx, medianLevel.xlsx,
                 SPFmicrodata.xlsx                       <- raw inputs
work/p2/phase2.py                         <- code/phase2/
work/p2/LOCK.json                         <- v2.0-results, results/
```

Check the raw inputs against the table in Section 2 (`sha256sum work/p1/data/*.* work/p1/data/spf/*`).

**C. Run the locked analysis once.**

```bash
cd work/p2
python3 -I phase2.py real
sha256sum results_real/results.json
```

It takes about 40 seconds and writes `results_real/`. A few pandas `FutureWarning` lines are expected.

**D. Compare.** If the hash equals the one in Section 1, the re-run is exact and you are done. If not, compare the confirmatory estimates with the published file, using this short script (save it as `compare.py`):

```python
import json, sys
a, b = (json.load(open(f))['core'] for f in sys.argv[1:3])
for t in ('P1a', 'P1b', 'P2a', 'P3'):
    for k in ('ratio', 'beta_CI', 'ratio_ci90', 'ci90', 'p', 'holm_reject'):
        if k in a[t]:
            x, y = a[t][k], b[t][k]
            pair = zip(x, y) if isinstance(x, list) else [(x, y)]
            ok = x == y if isinstance(x, bool) else all(abs(u - v) < 5e-4 for u, v in pair)
            print(t, k, x, y, 'OK' if ok else 'DIFFERENT')
```

```bash
python3 compare.py path/to/published/results.json results_real/results.json
```

Every line should say `OK`. The author rehearsed these steps from the release files in a clean folder, and they reproduced the published hash exactly.

## 4. What to report back

Please send the author a short note with:

1. the dates you found for the tag commit and the Zenodo record (Step 1);
2. the report file written by verify\_lock.py (or, if you checked by hand, whether every manifest line and raw-input hash matched);
3. your Python and library versions;
4. the SHA-256 of your `results.json`, and the estimate comparison if the hash differed (the report includes both).

If anything fails, report it as it is. A failed check is useful, and it will be published as it stands.

**Sign-off statement.** If all checks pass, please add this to your note, with your name and affiliation. It will appear, with your permission, in the paper's appendix and the next release:

> *On \[date\] I downloaded release v1.0-lock (DOI 10.5281/zenodo.23477871) and confirmed that its files match MANIFEST.txt and that its lock precedes the published run. Using public input files that match the published hashes, I ran `phase2.py real` once. It produced results.json with SHA-256 \[hash\] \[or: the same four confirmatory estimates to three decimals\]. I was not involved in the study's design or analysis.*

Questions go to Andy Moran (Heaviside Analytics). Thank you; this takes an hour and is worth more to the paper's credibility than anything its author can say.
