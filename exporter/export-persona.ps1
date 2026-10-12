# Persona exporter (Windows PowerShell 5.1). Twin with tools/export_persona.py.
# Usage: .\export-persona.ps1 -InputPath <personalities.md> [-Out <pairs.jsonl>]
# Local only. Never transmits. Shared SPEC-persona-trainer.md contract.
param(
    [string]$InputPath = "",
    [string]$Out = "",
    [string]$Schema = "v1"
)

$ErrorActionPreference = "Stop"
function Fail([string]$msg) { Write-Error "EXPORT ABORT: $msg"; exit 1 }

if ([string]::IsNullOrWhiteSpace($InputPath)) { Fail "usage: .\export-persona.ps1 -InputPath <personalities.md> [-Out <pairs.jsonl>]" }
if (-not (Test-Path -LiteralPath $InputPath)) { Fail "input not found: $InputPath" }
if ([string]::IsNullOrWhiteSpace($Out)) { $Out = Join-Path (Split-Path -Parent $InputPath) "persona-pairs.jsonl" }
$QuarantineFile = [System.IO.Path]::ChangeExtension($Out, ".quarantine.jsonl")

$lines = [System.IO.File]::ReadAllLines($InputPath)
$inTwin = $false
$rows = @()
foreach ($line in $lines) {
    if ($line -match "(?i)twin|divergence") { $inTwin = $true }
    if ($inTwin -and ($line -match "^\s*\|")) {
        $cells = $line.Split("|")
        if ($cells.Count -ge 5) {
            $date = $cells[1].Trim(); $pick = $cells[2].Trim(); $corr = $cells[3].Trim()
            $lesson = if ($cells.Count -ge 6) { $cells[4].Trim() } else { "" }
            if ($date -match "^(Date|[-:]+)$" -or $date -eq "") { continue }
            if ($pick -match "^[: -]+$" -or $pick -eq "Pick") { continue }
            $rows += [pscustomobject]@{ Date = $date; Pick = $pick; Correction = $corr; Lesson = $lesson }
        }
    }
}

$secretRe = "password|passwd|ghp_[A-Za-z0-9_]{36,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|bearer|mongodb://|postgres://|api[_-]?key"
$written = 0; $skipped = 0; $quarantined = 0; $n = 0
$outLines = @()
$quarantineLines = @()
foreach ($r in $rows) {
    $n++
    if ([string]::IsNullOrWhiteSpace($r.Pick) -or [string]::IsNullOrWhiteSpace($r.Correction)) { $skipped++; continue }
    if (($r.Pick.Contains("{") -and $r.Pick.Contains("}")) -or ($r.Correction.Contains("{") -and $r.Correction.Contains("}"))) { $skipped++; continue }
    $blob = $r.Date + " " + $r.Pick + " " + $r.Correction + " " + $r.Lesson
    if ($blob -match $secretRe) {
        $quarantined++
        $qObj = [pscustomobject]@{ row = $n; date = $r.Date; reason = "secret_pattern_matched"; preview = $blob.Substring(0, [Math]::Min(80, $blob.Length)) }
        $quarantineLines += ($qObj | ConvertTo-Json -Compress)
        continue
    }
    $d = $r.Date
    if ($d -notmatch "^\d{4}-\d{2}-\d{2}$") { $d = "unknown" }
    $dd = $d.Replace("-", "")
    $pairId = "div-" + $dd + "-" + $n.ToString("00")
    if ($Schema -eq "v2") {
        $rec = [ordered]@{
            pair_id = $pairId
            schema = "digi-brain-divergence-pair-v2"
            date = $d
            twin_pick = $r.Pick
            owner_correction = $r.Correction
            scope = "project"
            decision_category = "workflow"
            review_status = "verified"
        }
    } else {
        $rec = [ordered]@{
            pair_id = $pairId
            schema = "digi-brain-divergence-pair-v1"
            date = $d
            twin_pick = $r.Pick
            owner_correction = $r.Correction
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($r.Lesson)) { $rec.lesson = $r.Lesson }
    $outLines += ($rec | ConvertTo-Json -Compress)
    $written++
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($Out, $outLines, $utf8)
if ($quarantineLines.Count -gt 0) {
    [System.IO.File]::WriteAllLines($QuarantineFile, $quarantineLines, $utf8)
}

# Self-validate JSON validity
$bad = 0
foreach ($ol in ([System.IO.File]::ReadAllLines($Out))) {
    if ([string]::IsNullOrWhiteSpace($ol)) { continue }
    try {
        $o = $ol | ConvertFrom-Json
        foreach ($f in @("pair_id", "schema", "date", "twin_pick", "owner_correction")) {
            if ($null -eq $o.$f) { $bad++ }
        }
    } catch { $bad++ }
}
if ($bad -gt 0) { Fail ("self-validation failed on " + $bad + " line(s).") }

Write-Output ("EXPORT OK: $Out (written=$written skipped=$skipped quarantined=$quarantined)")
