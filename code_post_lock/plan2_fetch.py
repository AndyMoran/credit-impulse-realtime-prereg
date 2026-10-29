"""
Plan 2: fetch the Philadelphia Fed survey indexes (not seasonally adjusted) from ALFRED at a fixed vintage.

The unadjusted indexes are unrevised (plan2/PLAN.md, Section 2), so any vintage gives the same values; a fixed vintage
makes the download reproducible byte for byte. The data are not redistributed (Philadelphia Fed terms): this script
and the SHA-256 hashes it prints are published instead.

Usage (needs a free FRED API key):  FRED_API_KEY=... python plan2_fetch.py
Writes ../../plan2/data/<series>.csv and prints their SHA-256.
"""
import os, sys, hashlib, requests

VINTAGE = "2026-10-15"                                     # fixed ALFRED vintage
SERIES = {"GACDFNA066MNFRBPHI": "General Activity, NSA", "NOCDFNA066MNFRBPHI": "New Orders, NSA"}
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "plan2", "data")


def fetch(sid, key):
    r = requests.get("https://api.stlouisfed.org/fred/series/observations",
                     params=dict(series_id=sid, api_key=key, file_type="json",
                                 realtime_start=VINTAGE, realtime_end=VINTAGE,
                                 observation_start="1968-05-01", observation_end="2019-12-01"))
    r.raise_for_status()
    rows = [(o["date"], o["value"]) for o in r.json()["observations"]]
    if any(v == "." for _, v in rows): sys.exit(f"{sid}: missing values in the download")
    return "date,value\n" + "".join(f"{d},{v}\n" for d, v in rows)


if __name__ == "__main__":
    key = os.environ.get("FRED_API_KEY") or sys.exit("Set FRED_API_KEY.")
    os.makedirs(OUT, exist_ok=True)
    for sid, name in SERIES.items():
        text = fetch(sid, key)
        path = os.path.join(OUT, f"{sid}.csv")
        open(path, "w", encoding="utf-8", newline="").write(text)
        n = text.count("\n") - 1
        print(f"{sid} ({name}): {n} months, vintage {VINTAGE}, sha256 {hashlib.sha256(text.encode()).hexdigest()}")
