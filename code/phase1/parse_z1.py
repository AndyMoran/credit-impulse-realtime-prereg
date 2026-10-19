"""Phase 1: extract household and business credit (flows and levels) from every downloaded Z.1 vintage.

Usage:  python parse_z1.py raw  ->  writes credit_vintages_long.csv and parse_report.csv
Reads every .prn / .csv file under raw/<folder>/ and keeps columns whose series code matches the
mapping below. Columns are matched by CODE, never by position (protocol mapping rule).
"""
import csv, re, sys
from pathlib import Path

# concept -> codes across vintages (household code changed Sep 2010: 154102005 -> 154104005)
MAP = {
    "hh_flow_saar":  ["FA154102005.Q", "FA154104005.Q"],
    "nfb_flow_saar": ["FA144104005.Q"],
    "hh_level_sa":   ["LA154102005.Q", "LA154104005.Q"],
    "nfb_level_sa":  ["LA144104005.Q"],
}
CODE2CONCEPT = {c: k for k, v in MAP.items() for c in v}

def norm_date(s):
    s = s.strip().strip('"')
    for pat in (r"^(\d{4})0?([1-4])$", r"^(\d{4}):?Q([1-4])$", r"^(\d{4})-?Q([1-4])$"):
        m = re.match(pat, s)
        if m: return f"{m.group(1)}Q{m.group(2)}"
    m = re.match(r"^(\d{4})-(\d{2})-\d{2}$", s)  # 1999-01-01 style
    if m: return f"{m.group(1)}Q{(int(m.group(2))-1)//3+1}"
    return None

def tokens(line):
    line = line.strip()
    if "," in line: return [t.strip().strip('"') for t in next(csv.reader([line]))]
    return [t.strip('"') for t in re.findall(r'"[^"]*"|\S+', line)]

# Units: D-table files are in $ billions up to the Dec 2010 release and in $ millions from the
# Mar 10, 2011 release onward (.prn and .csv alike). Verified: median level ratio exactly 1000.000
# between the 20101209 and 20110310 vintages (audit log, Phase 1 entry). Output is always $ billions.
def units_divisor(vintage_folder):
    return 1000.0 if vintage_folder == "current" or vintage_folder >= "20110310" else 1.0

def parse_file(path, divisor=1.0):
    """Yield (code, quarter, value). Handles two-part .prn files: a new header row resets columns."""
    header = None
    for line in path.read_text(errors="replace").splitlines():
        tk = tokens(line)
        if not tk: continue
        if any(re.fullmatch(r"F[AGLU]\d{9}\.Q|LA\d{9}\.Q", t) for t in tk[1:]):
            header = tk; continue
        if header is None: continue
        q = norm_date(tk[0])
        if not q: continue
        for code, val in zip(header[1:], tk[1:]):
            if code in CODE2CONCEPT:
                try: yield code, q, float(val) / divisor
                except ValueError: pass  # ND / blanks

def main(root):
    out, report = [], []
    for vdir in sorted(Path(root).iterdir()):
        if not vdir.is_dir(): continue
        found = {}
        allf = sorted(list(vdir.rglob("*.prn")) + list(vdir.rglob("*.csv")))
        # D.2/D.3 files only (gtab2d.prn, gtab3d.prn, d2.csv, d3.csv): other tables carry the same
        # codes in different units (millions), so they are used only as a fallback, and flagged.
        dfiles = [f for f in allf if re.search(r"(gtab[23]d?\.prn|(^|[^a-z0-9])d[23]\.csv|(^|[^a-z0-9])d3_[st]\.csv)$", f.name.lower())]
        if not dfiles: report.append([vdir.name, "FALLBACK_ALL_FILES", "", "", ""])
        for f in (dfiles or allf):
            for code, q, v in parse_file(f, units_divisor(vdir.name)):
                key = (CODE2CONCEPT[code], q)
                if key in found and abs(found[key][1] - v) > 0.01:
                    report.append([vdir.name, "CONFLICT", CODE2CONCEPT[code], q, f.name])
                found.setdefault(key, (code, v, f.name))
        for (concept, q), (code, v, fname) in sorted(found.items()):
            out.append([vdir.name, concept, code, q, v, fname])
        concepts = sorted({k[0] for k in found})
        last = max((k[1] for k in found), default="")
        report.append([vdir.name, "OK" if len(concepts) == 4 else "INCOMPLETE", ";".join(concepts), last, ""])
    # Continuity check: a units error shifts EVERY quarter of a vintage by the same factor (~1000x).
    # Compare consecutive vintages on the MEDIAN ratio over common quarters, levels only
    # (flows are small and cross zero, so quarter-by-quarter ratios are meaningless for them).
    import statistics
    byv = {}
    for v, concept, code, q, val, fn in out: byv.setdefault(v, {})[(concept, q)] = val
    dated = sorted(k for k in byv if k != "current") + (["current"] if "current" in byv else [])
    for a, b in zip(dated, dated[1:]):
        for concept in ("hh_level_sa", "nfb_level_sa"):
            ratios = [byv[b][k] / byv[a][k] for k in byv[a]
                      if k[0] == concept and k in byv[b] and byv[a][k] > 1 and byv[b][k] > 1]
            if ratios:
                m = statistics.median(ratios)
                if not (0.5 < m < 2):
                    report.append([b, "UNITS_JUMP", concept, f"median ratio {m:.3f}", f"vs {a}"])
    with open("credit_vintages_long.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["vintage_folder", "concept", "code", "quarter", "value_bn", "source_file"]); w.writerows(out)
    with open("parse_report.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["vintage_folder", "status", "concepts_or_concept", "last_quarter_or_quarter", "file"]); w.writerows(report)
    bad = [r for r in report if r[1] != "OK"]
    print(f"{len(report)-len(bad)} vintages OK; {len(bad)} need a look (see parse_report.csv)")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "raw")
