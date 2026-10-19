# Verify each Z.1 release date against the release's own page. Run from the folder holding z1_release_dates.csv.
$rows = Import-Csv .\z1_release_dates.csv | Where-Object { $_.release_date -ge '1999-06-11' -and $_.release_date -le '2019-12-31' }
$out = foreach ($r in $rows) {
  $f = $r.archive_folder; $found = $null; $src = $null
  foreach ($p in @("default.htm","accessible/default.htm","html/default.htm","DEFAULT.HTM")) {
    try {
      $html = (Invoke-WebRequest -UseBasicParsing "https://www.federalreserve.gov/releases/z1/$f/$p").Content
      if ($html -match 'Release Date:\s*\**\s*([A-Z][a-z]+ \d{1,2}, \d{4})') { $found = $Matches[1]; $src = "$p (Release Date)"; break }
      if ($html -match 'Last [Uu]pdate:?\s*\**\s*([A-Z][a-z]+ \d{1,2}, \d{4})') { $found = $Matches[1]; $src = "$p (Last update)"; break }
    } catch {}
  }
  $d = if ($found) { ([datetime]::Parse($found)).ToString('yyyy-MM-dd') } else { '' }
  [pscustomobject]@{ release_date=$r.release_date; page_date=$d; source=$src; match=($d -eq $r.release_date) }
  Start-Sleep -Milliseconds 500
}
$out | Export-Csv .\z1_dates_verified.csv -NoTypeInformation
$out | Where-Object { -not $_.match } | Format-Table
