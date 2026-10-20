#!/usr/bin/env python3
"""
Independent re-run of the locked credit-impulse study (release v1.0-lock).

Checks, in order:
  1. every file in the locked release matches MANIFEST.txt (SHA-256);
  2. phase2.py is the locked file;
  3. the ten public raw inputs match the hashes recorded in MANIFEST.txt;
  4. LOCK.json names the locked release;
  5. runs the locked analysis once, in a fresh working folder;
  6. compares the new results.json with the published one (hash, then the confirmatory estimates).
It never edits the release, the raw inputs or the published results. A report is written next to this script.

Usage:
  python verify_lock.py --release <unpacked v1.0-lock folder>
                        --results <v2.0-results 'results' folder>
                        --raw <raw_inputs_v1.0-lock.zip or a folder of the ten files>
Needs Python 3.11+ with numpy, pandas, scipy, statsmodels and openpyxl.
"""
import argparse, hashlib, json, os, platform, shutil, subprocess, sys, tempfile, zipfile, datetime

LOCKED_PHASE2 = 'da697030f2349feae24dc79a3dfcbb786552b62186ffbf624a027c591814766e'
PUBLISHED_RESULTS = '9e4239dd116eaea7c9f65df83f85d349f338aeb4adb6ff16904a6793ed6fa99c'
LOCK_COMMIT = '4eb084fb2c462fffec72574f108043ea9d796cc9'
LOCK_DOI = '10.5281/zenodo.23477871'
RAW_DEST = {  # raw file name -> place in the working layout
    'ROUTPUTQvQd.xlsx': 'p1/data', 'NOUTPUTQvQd.xlsx': 'p1/data', 'PQvQd.xlsx': 'p1/data', 'rucQvMd.xlsx': 'p1/data',
    'routput_fst.xlsx': 'p1/data', 'GS2.csv': 'p1/data', 'medianGrowth.xlsx': 'p1/data/spf',
    'medianLevel.xlsx': 'p1/data/spf', 'SPFmicrodata.xlsx': 'p1/data/spf'}
FROM_RELEASE = {  # release path -> place in the working layout
    'tables/spf_deadlines_z1_map.csv': 'phase0', 'code/phase1/build.py': 'p1', 'code/phase1/fixedb.py': 'p1',
    'data_derived/credit_vintages_long.csv': 'p1/data', 'data_derived/download_log.csv': 'p1/data',
    'code/phase2/phase2.py': 'p2'}

log = []
def say(msg): print(msg, flush=True); log.append(msg)
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

def find_release_root(path):
    for root, _, files in os.walk(path):
        if 'MANIFEST.txt' in files and os.path.isdir(os.path.join(root, 'code')): return root
    sys.exit(f'No MANIFEST.txt with a code/ folder found under {path}')

def find_results_dir(path):
    for root, _, files in os.walk(path):
        if 'LOCK.json' in files and 'results.json' in files: return root
    sys.exit(f'No folder containing both LOCK.json and results.json found under {path}')

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--release', required=True); ap.add_argument('--results', required=True); ap.add_argument('--raw', required=True)
    a = ap.parse_args(); ok_all = True
    for p in (a.release, a.results, a.raw):
        if not os.path.exists(p): sys.exit(f'Not found: {p}  (give the real path of the unzipped folder or zip file)')
    a.results = find_results_dir(a.results)
    say(f'Verification run {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M UTC}')
    say(f'Python {platform.python_version()} on {platform.platform()}')
    try:
        import numpy, pandas, scipy, statsmodels, openpyxl
        say(f'numpy {numpy.__version__}, pandas {pandas.__version__}, scipy {scipy.__version__}, '
            f'statsmodels {statsmodels.__version__}, openpyxl {openpyxl.__version__}')
    except ImportError as e: sys.exit(f'Missing package: {e}. Install numpy pandas scipy statsmodels openpyxl.')

    # 1. release against its manifest
    rel = find_release_root(a.release); files, raw_hash, bad = {}, {}, []
    for line in open(os.path.join(rel, 'MANIFEST.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#'): continue
        h, name = line.split('  ', 1)
        if name.split(' ')[0] in ('RTDSM', 'SPF', 'FRED'): raw_hash[name.split(' ', 1)[1]] = h
        else: files[name] = h
    for name, h in files.items():
        p = os.path.join(rel, name)
        if not os.path.exists(p) or sha(p) != h: bad.append(name)
    say(f'\n1. Release files against MANIFEST.txt: {len(files) - len(bad)} of {len(files)} match' + (f'; MISMATCH: {bad}' if bad else ''))
    ok_all &= not bad

    # 2. locked analysis code
    h2 = sha(os.path.join(rel, 'code/phase2/phase2.py')); ok = h2 == LOCKED_PHASE2; ok_all &= ok
    say(f'2. phase2.py is the locked file: {"yes" if ok else "NO"} ({h2})')

    # 3. raw inputs
    tmp = tempfile.mkdtemp(prefix='verify_lock_'); rawdir = os.path.join(tmp, 'raw')
    if zipfile.is_zipfile(a.raw):
        with zipfile.ZipFile(a.raw) as z:
            for m in z.namelist():
                if os.path.basename(m) in raw_hash:
                    with z.open(m) as src, open(os.path.join(os.makedirs(rawdir, exist_ok=True) or rawdir, os.path.basename(m)), 'wb') as dst:
                        shutil.copyfileobj(src, dst)
    else:
        os.makedirs(rawdir, exist_ok=True)
        for root, _, fs in os.walk(a.raw):
            for f in fs:
                if f in raw_hash: shutil.copy2(os.path.join(root, f), os.path.join(rawdir, f))
    say('3. Raw inputs against the hashes in MANIFEST.txt:')
    for name, h in raw_hash.items():
        p = os.path.join(rawdir, name); got = sha(p) if os.path.exists(p) else None
        status = 'match' if got == h else ('MISSING' if got is None else 'MISMATCH')
        if name in RAW_DEST: ok_all &= status == 'match'
        say(f'   {name:22} {status}')

    # 4. LOCK.json
    L = json.load(open(os.path.join(a.results, 'LOCK.json')))
    ok = L.get('tag_commit') == LOCK_COMMIT and L.get('doi') == LOCK_DOI; ok_all &= ok
    say(f'4. LOCK.json names commit {L.get("tag_commit", "?")[:7]} and DOI {L.get("doi")}: {"as expected" if ok else "UNEXPECTED"}')

    # 5. assemble a fresh working layout and run once
    work = os.path.join(tmp, 'work')
    for src, dst in FROM_RELEASE.items():
        os.makedirs(os.path.join(work, dst), exist_ok=True); shutil.copy2(os.path.join(rel, src), os.path.join(work, dst))
    for name, dst in RAW_DEST.items():
        os.makedirs(os.path.join(work, dst), exist_ok=True); shutil.copy2(os.path.join(rawdir, name), os.path.join(work, dst))
    shutil.copy2(os.path.join(a.results, 'LOCK.json'), os.path.join(work, 'p2'))
    say('\n5. Running the locked analysis once (about a minute) ...')
    t0 = datetime.datetime.now()
    # -E -P: ignore PYTHON* environment overrides and do not import from the script folder,
    # but keep user-installed packages (isolated mode -I would hide them on Windows).
    r = subprocess.run([sys.executable, '-E', '-P', 'phase2.py', 'real'], cwd=os.path.join(work, 'p2'),
                       capture_output=True, text=True)
    secs = (datetime.datetime.now() - t0).total_seconds()
    if r.returncode != 0:
        say(f'   FAILED after {secs:.0f} s, exit code {r.returncode}:\n{r.stderr[-2000:]}'); ok_all = False
    else:
        say(f'   finished in {secs:.0f} s')
        new = os.path.join(work, 'p2', 'results_real', 'results.json'); hn = sha(new)
        say(f'\n6. New results.json SHA-256: {hn}')
        if hn == PUBLISHED_RESULTS:
            say('   Identical to the published file: exact reproduction.')
        else:
            say('   Hash differs from the published file; comparing the confirmatory estimates (tolerance 0.0005):')
            pub = json.load(open(os.path.join(a.results, 'results.json')))['core']; mine = json.load(open(new))['core']
            if sha(os.path.join(a.results, 'results.json')) != PUBLISHED_RESULTS:
                say('   NOTE: the published results.json supplied is not the expected file.')
            for t in ('P1a', 'P1b', 'P2a', 'P3'):
                for k in ('ratio', 'beta_CI', 'ratio_ci90', 'ci90', 'p', 'holm_reject'):
                    if k in pub[t]:
                        x, y = pub[t][k], mine[t][k]
                        pairs = zip(x, y) if isinstance(x, list) else [(x, y)]
                        same = x == y if isinstance(x, bool) else all(abs(u - v) < 5e-4 for u, v in pairs)
                        ok_all &= same; say(f'   {t:4} {k:11} published {x}  re-run {y}  {"OK" if same else "DIFFERENT"}')
    verdict = 'PASS' if ok_all else 'FAIL'
    say(f'\nOVERALL: {verdict}')
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'verification_report_{verdict}.txt')
    open(out, 'w', encoding='utf-8').write('\n'.join(log) + '\n'); print(f'Report written to {out}')
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    main()
