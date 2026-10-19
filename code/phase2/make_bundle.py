"""Assemble the preregistration lock bundle and its MANIFEST (SHA-256 of every file, plus raw-input hashes)."""
import os, shutil, hashlib, json, zipfile, pandas as pd
B = '/home/claude/bundle/credit-impulse-realtime-prereg'; shutil.rmtree(B, ignore_errors=True)
P1, P2, P0 = '/home/claude/p1', '/home/claude/p2', '/home/claude/phase0'
layout = {
  'code/phase0': [f'{P0}/build.py', f'{P0}/verify_z1_dates.ps1'],
  'code/phase1': [f'{P1}/{f}' for f in ('build.py', 'build2.py', 'study.py', 'charts.py', 'calib.py', 'fixedb.py', 'power.py', 'power2.py')]
                 + ['/home/claude/phase1/download_z1.ps1', '/home/claude/phase1/parse_z1.py'],
  'code/phase2': [f'{P2}/{f}' for f in ('phase2.py', 'test_phase2.py', 'power_realpath.py', 'ci_check.py', 'p3_size_check.py', 'make_bundle.py')],
  'tables': [f'{P0}/z1_release_dates.csv', f'{P0}/spf_deadlines_z1_map.csv', f'{P1}/out/origin_release_table.csv'],
  'data_derived': [f'{P1}/data/credit_vintages_long.csv', f'{P1}/data/parse_report.csv', f'{P1}/data/download_log.csv',
                   f'{P1}/out/credit_measures_by_vintage.csv', f'{P1}/out/credit_measures_revised.csv',
                   f'{P1}/out/first_release_vs_revised.csv', f'{P1}/out/revision_stats.csv', f'{P1}/out/gap_decomposition_D2.csv'],
  'phase1_results': [f'{P1}/out/fig1_first_release_vs_revised.png', f'{P1}/out/fig2_gap_decomposition_D2.png',
                     f'{P1}/out/calib.npz', f'{P1}/out/power_results_R2000.csv', f'{P1}/out/power_results_fixedb_R2000.csv',
                     f'{P1}/out/power2_results_R2000.csv', f'{P2}/power_realpath.csv'],
  'synthetic_tests': [f'{P2}/synthetic_test_results.csv', f'{P2}/synthetic_test_log.txt'],
  '.': ['/home/claude/bundle/README.md'],
  'protocol': ['/home/claude/bundle/protocol_v2.3.md', '/home/claude/bundle/protocol_v2.3.pdf'],
}
for d, fs in layout.items():
    os.makedirs(f'{B}/{d}', exist_ok=True)
    for f in fs:
        if os.path.exists(f): shutil.copy2(f, f'{B}/{d}/')
        else: print('MISSING (not copied):', f)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
raw = {  # raw inputs not redistributed; hashes prove the versions used
  'RTDSM ROUTPUTQvQd.xlsx': sha(f'{P1}/data/ROUTPUTQvQd.xlsx'), 'RTDSM NOUTPUTQvQd.xlsx': sha(f'{P1}/data/NOUTPUTQvQd.xlsx'),
  'RTDSM PQvQd.xlsx': sha(f'{P1}/data/PQvQd.xlsx'), 'RTDSM rucQvMd.xlsx': sha(f'{P1}/data/rucQvMd.xlsx'),
  'RTDSM routput_fst.xlsx': sha(f'{P1}/data/routput_fst.xlsx'),
  'SPF medianGrowth.xlsx': sha(f'{P1}/data/spf/medianGrowth.xlsx'), 'SPF medianLevel.xlsx': sha(f'{P1}/data/spf/medianLevel.xlsx'),
  'SPF SPFmicrodata.xlsx': sha(f'{P1}/data/spf/SPFmicrodata.xlsx'), 'SPF spf-caveats.pdf': sha(f'{P1}/data/spf/spf-caveats.pdf')}
if os.path.exists(f'{P1}/data/GS2.csv'): raw['FRED GS2.csv'] = sha(f'{P1}/data/GS2.csv')
with open(f'{B}/MANIFEST.txt', 'w') as m:
    m.write('# SHA-256 of every file in this bundle\n')
    for root, _, fs in sorted(os.walk(B)):
        for f in sorted(fs):
            if f == 'MANIFEST.txt': continue
            p = os.path.join(root, f); m.write(f'{sha(p)}  {os.path.relpath(p, B)}\n')
    m.write('\n# Raw inputs used but not redistributed (public; re-downloadable)\n')
    for k, v in raw.items(): m.write(f'{v}  {k}\n')
    m.write('# Z.1 release archives: SHA-256 per file in data_derived/download_log.csv\n')
z = '/home/claude/bundle/credit-impulse-realtime-prereg-v1.0-lock.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, fs in os.walk(B):
        for f in fs: p = os.path.join(root, f); zf.write(p, os.path.relpath(p, os.path.dirname(B)))
print('bundle zip sha256', sha(z), os.path.getsize(z))
