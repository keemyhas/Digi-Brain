# Persona exporter (Windows PowerShell 5.1). POSIX port deferred per SPEC-persona-trainer.md.
# Usage: .\export-persona.ps1 -InputPath <personalities.md> [-Out <pairs.jsonl>]
# Local only. Never transmits. Shared SPEC-persona-trainer.md contract.
param(
    [string]$InputPath = "",
    [string]$Out = ""
)

$ErrorActionPreference = "Stop"
function Fail([string]$msg) { Write-Output "EXPORT ABORT: $msg"; exit 1 }

if ([string]::IsNullOrWhiteSpace($InputPath)) { Fail "usage: .\export-persona.ps1 -InputPath <personalities.md> [-Out <pairs.jsonl>]" }
if (-not (Test-Path -LiteralPath $InputPath)) { Fail "input not found: $InputPath" }
if ([string]::IsNullOrWhiteSpace($Out)) { $Out = Join-Path (Split-Path -Parent $InputPath) "persona-pairs.jsonl" }

function Json-Escape([string]$s) {
    $s = $s.Replace("\", "\\").Replace('"', '\"').Replace("`r", "").Replace("`n", "\n").Replace("`t", "\t")
    return $s
}

$lines = [System.IO.File]::ReadAllLines($InputPath)
$inTwin = $false
$rows = @()
foreach ($line in $lines) {
    if ($line -match "(?i)twin|divergence") { $inTwin = $true }
    if ($inTwin -and ($line -match "^\s*\|")) {
        $cells = $line.Split("|")
        if ($cells.Count -ge 6) {
            $date = $cells[1].Trim(); $pick = $cells[2].Trim(); $corr = $cells[3].Trim(); $lesson = $cells[4].Trim()
            if ($date -match "^(Date|[-:]+)$") { continue }
            if ($pick -match "^[: -]+$") { continue }
            $rows += [pscustomobject]@{ Date = $date; Pick = $pick; Correction = $corr; Lesson = $lesson }
        }
    }
}

$secretRe = "password|passwd|admin123|api[_-]?key|bearer [A-Za-z0-9]|mongodb://|postgres://|ghp_|sk-|AKIA"
$written = 0; $skipped = 0; $quarantined = 0; $n = 0
$outLines = @()
foreach ($r in $rows) {
    $n++
    if ([string]::IsNullOrWhiteSpace($r.Pick) -or [string]::IsNullOrWhiteSpace($r.Correction)) { $skipped++; continue }
    if (($r.Pick.Contains("{") -and $r.Pick.Contains("}")) -or ($r.Correction.Contains("{") -and $r.Correction.Contains("}"))) { $skipped++; continue }
    $blob = $r.Date + " " + $r.Pick + " " + $r.Correction + " " + $r.Lesson
    if ($blob -match $secretRe) { $quarantined++; continue }
    $d = $r.Date
    if ($d -notmatch "^\d{4}-\d{2}-\d{2}$") { $d = "unknown" }
    $dd = $d.Replace("-", "")
    $obj = '{"pair_id":"div-' + $dd + '-' + $n.ToString("00") + '","schema":"digi-brain-divergence-pair-v1","date":"' + (Json-Escape $d) + '","twin_pick":"' + (Json-Escape $r.Pick) + '","owner_correction":"' + (Json-Escape $r.Correction) + '"'
    if (-not [string]::IsNullOrWhiteSpace($r.Lesson)) { $obj += ',"lesson":"' + (Json-Escape $r.Lesson) + '"' }
    $obj += '}'
    $outLines += $obj
    $written++
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($Out, $outLines, $utf8)

# Self-validate: every line parses as JSON with all required fields.
$bad = 0
foreach ($ol in ([System.IO.File]::ReadAllLines($Out))) {
    if ([string]::IsNullOrWhiteSpace($ol)) { continue }
    try {
        $o = $ol | ConvertFrom-Json
        foreach ($f in @("pair_id", "schema", "date", "twin_pick", "owner_correction")) {
            if ($null -eq $o.$f) { $bad++ }
        }
        if ($o.schema -ne "digi-brain-divergence-pair-v1") { $bad++ }
    } catch { $bad++ }
}
if ($bad -gt 0) { Fail ("self-validation failed on " + $bad + " line(s).") }

Write-Output ("EXPORT OK: $Out (rows=$($rows.Count) written=$written skipped=$skipped quarantined=$quarantined)")
