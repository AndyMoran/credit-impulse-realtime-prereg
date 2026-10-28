# alfred_check.py: does the Philly Fed NSA index ever change between vintages?
# Usage: FRED_API_KEY=yourkey python alfred_check.py
import os, requests, pandas as pd
KEY = os.environ["FRED_API_KEY"]
URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES = ["GACDFNA066MNFRBPHI", "GACDFSA066MSFRBPHI", "NOCDFNA066MNFRBPHI"]
EARLY, LATE = "2015-06-18", "2026-10-15"     # first archived vintage; latest release date

def vintage(sid, date):
    r = requests.get(URL, params=dict(series_id=sid, api_key=KEY, file_type="json",
                     realtime_start=date, realtime_end=date,
                     observation_start="1968-05-01", observation_end="2015-05-01"))
    r.raise_for_status()
    s = pd.Series({o["date"]: o["value"] for o in r.json()["observations"]})
    return pd.to_numeric(s, errors="coerce")

for sid in SERIES:
    try:
        a, b = vintage(sid, EARLY), vintage(sid, LATE)
    except Exception as e:
        print(f"{sid}: could not fetch ({e})"); continue
    both = a.index.intersection(b.index)
    diff = (a[both] - b[both]).abs()
    print(f"{sid}: {len(both)} months compared, {int((diff > 0).sum())} differ, max |diff| = {diff.max():.3f}")
    a.to_csv(f"{sid}_{EARLY}.csv"); b.to_csv(f"{sid}_{LATE}.csv")