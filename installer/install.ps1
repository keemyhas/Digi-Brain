# Digi Brain installer (Windows). POSIX twin: install.sh - same behavior, shared SPEC-installer.md contract.
# Usage: .\install.ps1 <target-repo> [--overwrite] [--git-init] [--verify-only] [--defaults] [--answers-file <path>]
# No network access. Nothing leaves the machine.

param(
    [string]$Target = "",
    [switch]$Overwrite = $false,
    [switch]$GitInit = $false,
    [switch]$VerifyOnly = $false,
    [switch]$Defaults = $false,
    [string]$AnswersFile = ""
)

$ErrorActionPreference = "Stop"
$script:AnswerMap = @{}

function Fail([string]$msg) { Write-Output "INSTALLER ABORT: $msg"; exit 1 }

function Read-Answer([string]$key, [string]$prompt, [string]$default) {
    if ($script:AnswerMap.ContainsKey($key)) { return $script:AnswerMap[$key] }
    if ($Defaults) { return $default }
    if ($default -ne "") { $suffix = " [$default]" } else { $suffix = "" }
    $ans = Read-Host "$prompt$suffix"
    if ([string]::IsNullOrWhiteSpace($ans)) { return $default }
    return $ans.Trim()
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "..\template"

if ([string]::IsNullOrWhiteSpace($Target)) { Fail "usage: .\install.ps1 <target-repo> [--overwrite] [--git-init]" }
if (-not (Test-Path -LiteralPath $TemplateDir)) { Fail "template/ not found next to installer." }

# Refuse to install into the Digi Brain source tree itself.
if ((Test-Path -LiteralPath (Join-Path $Target "SPEC-digi-brain.md")) -or (Test-Path -LiteralPath (Join-Path $Target "template"))) {
    Fail "target looks like the Digi Brain source tree. Install into a foreign repo."
}

$AgentsDir = Join-Path $Target ".agents"
if ((Test-Path -LiteralPath $AgentsDir) -and (-not $Overwrite) -and (-not $VerifyOnly)) {
    Fail "$AgentsDir exists. Re-run with --overwrite (a timestamped backup is written first)."
}

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $AgentsDir)) { Fail "nothing installed at $AgentsDir." }
    $leftover = Get-ChildItem -Path $AgentsDir -Recurse -Include "*.md" | Select-String -Pattern "\{\{[A-Z_]+\}\}"
    if ($leftover) { Fail "unresolved placeholders remain."; $leftover | Select-Object -First 10 }
    Write-Output "VERIFY OK: no unresolved placeholders under $AgentsDir."
    exit 0
}

Write-Output "--- Digi Brain install: single interview (Enter = default, 'none' where allowed) ---"
if ($AnswersFile -ne "") {
    if (-not (Test-Path -LiteralPath $AnswersFile)) { Fail "answers file not found: $AnswersFile" }
    foreach ($line in (Get-Content -LiteralPath $AnswersFile)) {
        if ($line -match "^\s*(#|$)") { continue }
        $i = $line.IndexOf("=")
        if ($i -gt 0) { $script:AnswerMap[$line.Substring(0, $i).Trim()] = $line.Substring($i + 1).Trim() }
    }
}
$A = @{}
$A["OWNER_NAME"] = Read-Answer "OWNER_NAME" "Owner name" "Ada Example"
$A["OWNER_ROLE"] = Read-Answer "OWNER_ROLE" "Owner role" "Solo Developer"
$A["PROJECT_NAME"] = Read-Answer "PROJECT_NAME" "Project name" "Acme Project"
$A["ACTIVATION_PHRASE"] = Read-Answer "ACTIVATION_PHRASE" "Autonomous-mode activation phrase" "take the wheel"
$A["TWIN_NAME"] = Read-Answer "TWIN_NAME" "Twin name ('none' disables autonomous mode)" "Deuter"
$A["SAFETY_INVARIANTS"] = Read-Answer "SAFETY_INVARIANTS" "Safety invariants (free text, or 'none yet')" "None defined."
$A["SAFETY_INVARIANTS_FILE"] = Read-Answer "SAFETY_INVARIANTS_FILE" "Safety invariants file" "none - same file, section 5"
$A["BACKEND_DIRS"] = Read-Answer "BACKEND_DIRS" "Backend dirs (comma list)" "src/"
$A["BACKEND_SCOPE"] = Read-Answer "BACKEND_SCOPE" "Backend scope" "server-side services"
$A["FRONTEND_DIRS"] = Read-Answer "FRONTEND_DIRS" "Frontend dirs (comma list)" "public/"
$A["FRONTEND_SCOPE"] = Read-Answer "FRONTEND_SCOPE" "Frontend scope" "user interfaces"
$A["TEST_COMMAND"] = Read-Answer "TEST_COMMAND" "Test command" "npm test"
$A["TYPE_CHECK"] = Read-Answer "TYPE_CHECK" "Type-check command" "npm run type-check"
$A["TEST_FRAMEWORK"] = Read-Answer "TEST_FRAMEWORK" "Test framework" "Jest"
$A["TESTS_DIR"] = Read-Answer "TESTS_DIR" "Tests dir" "tests/"
$A["TEST_SCOPE"] = Read-Answer "TEST_SCOPE" "Test scope" "the full suite"
$A["DATABASE"] = Read-Answer "DATABASE" "Database engine" "PostgreSQL"
$A["MIGRATIONS_DIR"] = Read-Answer "MIGRATIONS_DIR" "Migrations dir" "migrations/"
$A["MIGRATION_NAMING"] = Read-Answer "MIGRATION_NAMING" "Migration naming" "YYYYMMDD_feature_name.sql"
$A["DOCS_DIR"] = Read-Answer "DOCS_DIR" "Docs dir" "docs/"
$A["API_DOCS"] = Read-Answer "API_DOCS" "API docs file" "docs/api.md"
$A["ADR_DIR"] = Read-Answer "ADR_DIR" "ADR dir" "docs/adr/"
$A["FUTURE_PLANS_DIR"] = Read-Answer "FUTURE_PLANS_DIR" "Future-plans dir" "docs/future-plans/"
$A["QA_DIR"] = Read-Answer "QA_DIR" "QA workspace dir" ".qa/"
$A["FIXTURE_PREFIX"] = Read-Answer "FIXTURE_PREFIX" "Test fixture prefix" "QA-"
$A["OWNER_PERSONAS"] = Read-Answer "OWNER_PERSONAS" "User personas (comma list)" "Admin, End User"
$A["DEV_URL"] = Read-Answer "DEV_URL" "Dev URL" "http://localhost:<port>"
$A["AUTH_MIDDLEWARE"] = Read-Answer "AUTH_MIDDLEWARE" "Auth middleware names" "requireAuth, requirePermission"
$A["SAFETY_MIDDLEWARE"] = Read-Answer "SAFETY_MIDDLEWARE" "Safety middleware ('none' if any)" "none"
$A["QUERY_PLACEHOLDER_STYLE"] = Read-Answer "QUERY_PLACEHOLDER_STYLE" "Query placeholder style" '$1, $2, ...'
$A["DATA_PROTECTION_STANDARD"] = Read-Answer "DATA_PROTECTION_STANDARD" "Data-protection standard" "AES-256 at rest, TLS in transit"
$A["SENSITIVE_RESOURCES"] = Read-Answer "SENSITIVE_RESOURCES" "Sensitive resources" "user-owned records, credentials, tokens"
$A["KEY_COLUMNS"] = Read-Answer "KEY_COLUMNS" "High-traffic key columns" "id, created_at, status"
$A["PROTECTED_COLUMNS_POLICY"] = Read-Answer "PROTECTED_COLUMNS_POLICY" "Protected-column policy" "no storage-layer computation on protected columns"
$A["DOMAIN_REVIEWER"] = Read-Answer "DOMAIN_REVIEWER" "Domain safety reviewer" "Owner (default; type a name to override)"
$A["WORKFLOWS_DIR"] = (Read-Answer "WORKFLOWS_DIR" "Workflows dir" "workflows").TrimEnd("/")
$A["DOMAIN_DOCS"] = Read-Answer "DOMAIN_DOCS" "Extra domain docs" "memory/architecture.md only"
$A["SYNC_RULE"] = Read-Answer "SYNC_RULE" "Multi-mirror sync rule ('single' = one tree)" "single"
$A["OWNER_DOMAIN"] = Read-Answer "OWNER_DOMAIN" "Business domain (one line)" "general web operations"
$A["COMPLIANCE_STANDARD"] = Read-Answer "COMPLIANCE_STANDARD" "Compliance standard ('none' if any)" "none"
$A["OFFLINE_STRATEGY"] = Read-Answer "OFFLINE_STRATEGY" "Offline strategy ('none' if any)" "none"
$A["LARGE_CLIENT_FILES"] = Read-Answer "LARGE_CLIENT_FILES" "Large client files ('none' if any)" "none"
$A["CODE_GRAPH"] = Read-Answer "CODE_GRAPH" "Code-graph tool ('none' if any)" "none"

if ($A["TWIN_NAME"] -eq "none") {
    $A["TWIN_NAME"] = "Autonomous mode disabled - activation phrase inert until a twin name is set."
}
if ($A["DOMAIN_REVIEWER"] -eq "none") {
    $A["DOMAIN_REVIEWER"] = "Owner (default; type a name to override)"
}

# Backup + render.
if (Test-Path -LiteralPath $AgentsDir) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = Join-Path $Target ".agents.backup-$stamp"
    Copy-Item -LiteralPath $AgentsDir -Destination $backup -Recurse -Force
    Write-Output "Backup written: $backup"
    Remove-Item -LiteralPath $AgentsDir -Recurse -Force
}
New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null
Copy-Item -Path (Join-Path $TemplateDir "*") -Destination $AgentsDir -Recurse -Force

if ($A["CODE_GRAPH"] -eq "none") {
    $cg = Join-Path $AgentsDir "rules\code-graph.md"
    if (Test-Path -LiteralPath $cg) { Remove-Item -LiteralPath $cg -Force }
}
$A["CODE_GRAPH_*"] = $A["CODE_GRAPH"]

$files = Get-ChildItem -Path $AgentsDir -Recurse -File
foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    foreach ($k in $A.Keys) {
        $text = $text.Replace("{{" + $k + "}}", $A[$k])
    }
    [System.IO.File]::WriteAllText($f.FullName, $text)
    if ($f.Name -like "*.template.md") {
        $new = $f.FullName -replace "\.template\.md$", ".md"
        Move-Item -LiteralPath $f.FullName -Destination $new -Force
    }
}

# Skills map.
$map = "# Skills map (generated - all rows start as prose fallbacks; replace with harness skill names)`n`n| Gate | Harness skill |`n|---|---|`n"
$map += "| spec-before-code | none - prose fallback |`n| multi-file build | none - prose fallback |`n| bug-fix | none - prose fallback |`n| security | none - prose fallback |`n| shipping | none - prose fallback |`n"
$map += "`nSource: SKILLS-MANIFEST.md next to this map. Fallback exercise (mandatory on first session): run one gate entirely in prose (no skill invocation) and log which gate + what the skill would have added.`n"
Set-Content -LiteralPath (Join-Path $AgentsDir "skills-map.md") -Value $map

# Boot checklist.
$bootSrc = Join-Path $ScriptDir "BOOT-CHECKLIST.template.md"
if (Test-Path -LiteralPath $bootSrc) {
    $boot = [System.IO.File]::ReadAllText($bootSrc)
    foreach ($k in $A.Keys) { $boot = $boot.Replace("{{" + $k + "}}", $A[$k]) }
    Set-Content -LiteralPath (Join-Path $AgentsDir "BOOT-CHECKLIST.md") -Value $boot
}

if ($GitInit -and (-not (Test-Path -LiteralPath (Join-Path $Target ".git")))) {
    git -C $Target init 2>&1 | Out-Null
}

# Self-verify: banners removed, zero tokens, clean scans.
foreach ($f in (Get-ChildItem -Path $AgentsDir -Recurse -File)) {
    $lines = [System.IO.File]::ReadAllLines($f.FullName) | Where-Object { $_ -notmatch "^> Setup:" }
    [System.IO.File]::WriteAllLines($f.FullName, $lines)
}
$leftover = Get-ChildItem -Path $AgentsDir -Recurse -Include "*.md" | Select-String -Pattern "\{\{[A-Z_*]+\}\}"
if ($leftover) { Write-Output "VERIFY FAILED: unresolved placeholders:"; $leftover | Select-Object -First 10; exit 1 }
$fp = Get-ChildItem -Path $AgentsDir -Recurse -Include "*.md" | Select-String -Pattern "abdul|hassan|archon|falx|vellora|synapseems" | Where-Object { $_.Line -notmatch "grep -rniE" }
if ($fp) { Write-Output "VERIFY FAILED: fingerprint terms in output."; exit 1 }

Write-Output "---"
Write-Output "INSTALL OK: $AgentsDir"
Write-Output "Next: open a fresh agent session in the target repo and follow .agents/BOOT-CHECKLIST.md"
