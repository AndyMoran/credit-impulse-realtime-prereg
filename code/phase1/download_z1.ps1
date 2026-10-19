# Phase 1: download every Z.1 vintage needed for the real-time credit dataset.
# Run in a folder containing z1_release_dates.csv. Creates raw\<folder>\ and download_log.csv.
# Releases up to Jun 2016 publish Disk/gtabs.zip (D.1-D.3 as .prn); later releases publish one CSV zip.
$ErrorActionPreference = 'Stop'
$base = 'https://www.federalreserve.gov/releases/z1'
$rows = Import-Csv .\z1_release_dates.csv | Where-Object { $_.release_date -ge '1999-06-11' -and $_.release_date -le '2019-12-31' }
$targets = foreach ($r in $rows) { [pscustomobject]@{ release_date=$r.release_date; folder=$r.archive_folder } }
# Latest vintage, used as the 'revised' series
$targets += [pscustomobject]@{ release_date='current'; folder='current' }
New-Item -ItemType Directory -Force raw | Out-Null
$log = foreach ($t in $targets) {
  $dir = "raw\$($t.folder)"; New-Item -ItemType Directory -Force $dir | Out-Null
  $tries = @("$base/$($t.folder)/Disk/gtabs.zip", "$base/$($t.folder)/z1_csv_files.zip")
  if ($t.folder -eq '20160609') { $tries += "$base/z1-csv-20160617.zip" }
  $got = $null
  foreach ($u in $tries) {
    $out = Join-Path $dir (Split-Path $u -Leaf)
    try { Invoke-WebRequest -UseBasicParsing $u -OutFile $out; $got = $u; break } catch { if (Test-Path $out) { Remove-Item $out } }
  }
  $hash = if ($got) { (Get-FileHash (Join-Path $dir (Split-Path $got -Leaf))).Hash } else { '' }
  if ($got) { Expand-Archive -Force (Join-Path $dir (Split-Path $got -Leaf)) $dir }
  Write-Host "$($t.release_date)  $(if ($got) {'OK  ' + (Split-Path $got -Leaf)} else {'MISSING'})"
  [pscustomobject]@{ release_date=$t.release_date; folder=$t.folder; url=$got; sha256=$hash; downloaded=(Get-Date -Format s) }
  Start-Sleep -Milliseconds 700
}
$log | Export-Csv .\download_log.csv -NoTypeInformation
Write-Host "`nMissing:"; $log | Where-Object { -not $_.url } | Format-Table release_date, folder
