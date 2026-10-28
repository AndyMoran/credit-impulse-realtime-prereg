# Plan 2 feasibility: are the Philly Fed survey's unadjusted indexes ever revised?

Run on 28 October 2026, before any Plan 2 design or analysis.

**Check.** Compare the earliest ALFRED vintage (18 June 2015) with the latest (15 October 2026), month by month, for May 1968 to May 2015.

| Series | Months | Differ | Max change |
|---|---|---|---|
| GACDFNA066MNFRBPHI (General Activity, not seasonally adjusted) | 565 | 0 | 0.000 |
| NOCDFNA066MNFRBPHI (New Orders, not seasonally adjusted) | 565 | 0 | 0.000 |
| GACDFSA066MSFRBPHI (General Activity, seasonally adjusted; control) | 565 | 405 | 7.1 |

**Reading.** The unadjusted indexes did not change in any month across all vintages from June 2015 to October 2026. The seasonally adjusted control did, so the check can detect revisions. Stability before 2015 is inferred, not observed: ALFRED's archive for this survey starts in June 2015.

**Files.** `alfred_check.py` (run with a FRED API key in `FRED_API_KEY`), `alfred_check_output.txt`, and `csv_sha256.txt`. The downloaded CSVs are not included: the Federal Reserve Bank of Philadelphia permits research use but does not grant redistribution. Rerun the script to fetch them, and compare their hashes with `csv_sha256.txt`.

Data: Federal Reserve Bank of Philadelphia, Manufacturing Business Outlook Survey, via ALFRED (Federal Reserve Bank of St. Louis). Conclusions are the author's, not the Bank's.
