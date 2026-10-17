# Digi Brain installer (Windows PowerShell 5.1). POSIX twin: install.sh - same behavior, shared SPEC-installer.md contract.
# Usage: .\install.ps1 -Target <repo> [-Overwrite] [-GitInit] [-VerifyOnly] [-Defaults] [-AnswersFile <path>]
# No network access. Nothing leaves the machine.
param(
    [string]$Target = "",
    [switch]$Overwrite,
    [switch]$GitInit,
    [switch]$VerifyOnly,
    [switch]$Defaults,
    [string]$AnswersFile = ""
)

$ErrorActionPreference = "Stop"

function Fail([string]$msg) {
    Write-Error "INSTALLER ABORT: $msg"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($Target)) {
    Fail "usage: .\install.ps1 -Target <repo> [-Overwrite] [-GitInit] [-VerifyOnly] [-Defaults] [-AnswersFile <path>]"
}

if (-not (Test-Path -LiteralPath $Target)) {
    try {
        New-Item -ItemType Directory -Path $Target -Force | Out-Null
    } catch {
        Fail "cannot create target directory: $Target"
    }
}
$Target = (Resolve-Path -LiteralPath $Target).ProviderPath

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path (Split-Path -Parent $ScriptDir) "template"
$BootTemplate = Join-Path $ScriptDir "BOOT-CHECKLIST.template.md"

if (-not (Test-Path -LiteralPath $TemplateDir)) {
    Fail "template/ directory not found at $TemplateDir"
}

if ((Test-Path -LiteralPath (Join-Path $Target "SPEC-digi-brain.md")) -and (Test-Path -LiteralPath (Join-Path $Target "template"))) {
    Fail "target looks like the Digi Brain source tree ($Target). Install into a foreign repo."
}

$AgentsDir = Join-Path $Target ".agents"

# Unified verification function
function Test-DigiBrainInstallation([string]$checkDir) {
    $vPass = $true
    Write-Output "=== DIGI-BRAIN VERIFICATION ==="

    # 1. Structure check
    $structOk = $true
    foreach ($d in @("memory", "rules", "agents", "workflows")) {
        $p = Join-Path $checkDir $d
        if (-not (Test-Path -LiteralPath $p)) {
            Write-Output "  MISSING DIR: $d"
            $structOk = $false
        }
    }
    if ($structOk) {
        Write-Output "STRUCTURE CHECK: PASS"
    } else {
        Write-Output "STRUCTURE CHECK: FAIL"
        $vPass = $false
    }

    # 2. Bootstrap check
    $bootOk = $true
    foreach ($f in @("memory\brain.md", "BOOT-CHECKLIST.md", "rules\session-bootstrap.md", "skills-map.md", "SKILLS-MANIFEST.md")) {
        $p = Join-Path $checkDir $f
        if (-not (Test-Path -LiteralPath $p)) {
            Write-Output "  MISSING BOOTSTRAP FILE: $f"
            $bootOk = $false
        }
    }
    if ($bootOk) {
        Write-Output "BOOTSTRAP CHECK: PASS"
    } else {
        Write-Output "BOOTSTRAP CHECK: FAIL"
        $vPass = $false
    }

    # 3. Safety check
    $safeOk = $true
    foreach ($f in @("rules\engineering-standards.md", "rules\memory-intake.md", "rules\project-logging.md", "rules\code-documentation-and-onboarding.md")) {
        $p = Join-Path $checkDir $f
        if (-not (Test-Path -LiteralPath $p)) {
            Write-Output "  MISSING SAFETY FILE: $f"
            $safeOk = $false
        }
    }
    if ($safeOk) {
        Write-Output "SAFETY CHECK: PASS"
    } else {
        Write-Output "SAFETY CHECK: FAIL"
        $vPass = $false
    }

    # 4. Placeholder check
    $unresolved = Get-ChildItem -Path $checkDir -Recurse -Include "*.md" -File | Select-String -Pattern "\{\{[A-Z0-9_*]+\}\}"
    if (-not $unresolved) {
        Write-Output "PLACEHOLDER CHECK: PASS"
    } else {
        Write-Output "PLACEHOLDER CHECK: FAIL"
        $unresolved | Select-Object -First 5 | ForEach-Object { Write-Output "  $($_.Filename):$($_.LineNumber): $($_.Line.Trim())" }
        $vPass = $false
    }

    # 5. Fingerprint scan
    $fp = Get-ChildItem -Path $checkDir -Recurse -Include "*.md" -File | Select-String -Pattern "abdul|hassan|archon|falx|vellora|synapseems" | Where-Object { $_.Line -notmatch "grep -rn" -and $_.Line -notmatch "fingerprint" }
    if (-not $fp) {
        Write-Output "FINGERPRINT SCAN: PASS"
    } else {
        Write-Output "FINGERPRINT SCAN: FAIL"
        $fp | Select-Object -First 5 | ForEach-Object { Write-Output "  $($_.Filename):$($_.LineNumber): $($_.Line.Trim())" }
        $vPass = $false
    }

    # 6. Secret-pattern scan
    $secretPattern = "ghp_[A-Za-z0-9_]{36,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|bearer\s+[A-Za-z0-9_\-\.]{20,}|password\s*[:=]\s*['`"][^'`"]+['`"]"
    $secHits = Get-ChildItem -Path $checkDir -Recurse -Include "*.md" -File | Select-String -Pattern $secretPattern
    if (-not $secHits) {
        Write-Output "SECRET-PATTERN SCAN: PASS"
    } else {
        Write-Output "SECRET-PATTERN SCAN: FAIL"
        $secHits | Select-Object -First 5 | ForEach-Object { Write-Output "  $($_.Filename):$($_.LineNumber): $($_.Line.Trim())" }
        $vPass = $false
    }

    if ($vPass) {
        Write-Output "OVERALL: PASS"
    } else {
        Write-Output "OVERALL: FAIL"
    }
    $script:LastVerificationPassed = $vPass
}

if ($VerifyOnly) {
    if (-not (Test-Path -LiteralPath $AgentsDir)) {
        Fail "nothing installed at $AgentsDir"
    }
    Test-DigiBrainInstallation $AgentsDir
    if ($script:LastVerificationPassed) { exit 0 } else { exit 1 }
}

if ((Test-Path -LiteralPath $AgentsDir) -and (-not $Overwrite)) {
    Fail "$AgentsDir exists. Re-run with -Overwrite (timestamped backup first)."
}

# Approved configuration whitelist
$ValidKeys = @(
    "OWNER_NAME", "OWNER_ROLE", "PROJECT_NAME", "ACTIVATION_PHRASE", "TWIN_NAME", "SAFETY_INVARIANTS",
    "SAFETY_INVARIANTS_FILE", "BACKEND_DIRS", "BACKEND_SCOPE", "FRONTEND_DIRS", "FRONTEND_SCOPE",
    "TEST_COMMAND", "TYPE_CHECK", "TEST_FRAMEWORK", "TESTS_DIR", "TEST_SCOPE", "DATABASE", "MIGRATIONS_DIR",
    "MIGRATION_NAMING", "DOCS_DIR", "API_DOCS", "ADR_DIR", "FUTURE_PLANS_DIR", "QA_DIR", "FIXTURE_PREFIX",
    "OWNER_PERSONAS", "DEV_URL", "AUTH_MIDDLEWARE", "SAFETY_MIDDLEWARE", "QUERY_PLACEHOLDER_STYLE",
    "DATA_PROTECTION_STANDARD", "SENSITIVE_RESOURCES", "KEY_COLUMNS", "PROTECTED_COLUMNS_POLICY",
    "DOMAIN_REVIEWER", "WORKFLOWS_DIR", "DOMAIN_DOCS", "SYNC_RULE", "OWNER_DOMAIN", "COMPLIANCE_STANDARD",
    "OFFLINE_STRATEGY", "LARGE_CLIENT_FILES", "CODE_GRAPH", "CODE_GRAPH_*"
)

$AnswerMap = @{}

if ($AnswersFile -ne "") {
    if (-not (Test-Path -LiteralPath $AnswersFile)) {
        Fail "answers file not found: $AnswersFile"
    }
    foreach ($rawLine in (Get-Content -LiteralPath $AnswersFile)) {
        $line = $rawLine.Trim()
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) { continue }
        $idx = $line.IndexOf("=")
        if ($idx -le 0) {
            Fail "malformed line in answers file: $line"
        }
        $k = $line.Substring(0, $idx).Trim()
        $v = $line.Substring($idx + 1).Trim()
        if (-not ($ValidKeys -contains $k)) {
            Fail "unrecognized configuration key in answers file: $k"
        }
        $AnswerMap[$k] = $v
    }
}

function Read-Answer([string]$key, [string]$prompt, [string]$defaultVal) {
    if (-not ($ValidKeys -contains $key)) {
        Fail "internal error: unapproved prompt key $key"
    }
    if ($AnswerMap.ContainsKey($key)) {
        return [string]$AnswerMap[$key]
    }
    if ($Defaults) {
        return $defaultVal
    }
    $ans = Read-Host "$prompt [$defaultVal]"
    if ([string]::IsNullOrWhiteSpace($ans)) {
        return $defaultVal
    }
    return $ans.Trim()
}

Write-Output "--- Digi Brain install: single interview (Enter = default, 'none' where allowed) ---"

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
$A["CODE_GRAPH_*"] = $A["CODE_GRAPH"]

# Staging directory for atomic install and rollback
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$stagingDir = Join-Path $Target (".agents.staging." + $stamp + "." + $PID)
if (Test-Path -LiteralPath $stagingDir) { Remove-Item -LiteralPath $stagingDir -Recurse -Force }
New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

Copy-Item -Path (Join-Path $TemplateDir "*") -Destination $stagingDir -Recurse -Force

if ($A["CODE_GRAPH"] -eq "none") {
    $cg = Join-Path $stagingDir "rules\code-graph.md"
    if (Test-Path -LiteralPath $cg) { Remove-Item -LiteralPath $cg -Force }
}

# Skills map
$map = "# Skills map (generated - all rows start as prose fallbacks; replace with harness skill names)`n`n| Gate | Harness skill |`n|---|---|`n"
$map += "| spec-before-code | none - prose fallback |`n| multi-file build | none - prose fallback |`n| bug-fix | none - prose fallback |`n| security | none - prose fallback |`n| shipping | none - prose fallback |`n"
$map += "`nSource: SKILLS-MANIFEST.md next to this map. Fallback exercise (mandatory on first session): run one gate entirely in prose and log it.`n"
Set-Content -LiteralPath (Join-Path $stagingDir "skills-map.md") -Value $map

# Boot checklist
if (Test-Path -LiteralPath $BootTemplate) {
    Copy-Item -LiteralPath $BootTemplate -Destination (Join-Path $stagingDir "BOOT-CHECKLIST.md") -Force
}

# Perform literal substitutions in staging
$stagedFiles = Get-ChildItem -Path $stagingDir -Recurse -File
foreach ($f in $stagedFiles) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    foreach ($k in $A.Keys) {
        $text = $text.Replace("{{" + $k + "}}", [string]$A[$k])
    }
    # Strip setup banner lines
    $filteredLines = $text -split "`r?`n" | Where-Object { $_ -notmatch "^> Setup:" }
    $text = [string]::Join("`n", $filteredLines) + "`n"
    [System.IO.File]::WriteAllText($f.FullName, $text)

    if ($f.Name -like "*.template.md") {
        $destName = $f.FullName -replace "\.template\.md$", ".md"
        Move-Item -LiteralPath $f.FullName -Destination $destName -Force
    }
}

# Run verification on staged directory
Test-DigiBrainInstallation $stagingDir
if (-not $script:LastVerificationPassed) {
    Remove-Item -LiteralPath $stagingDir -Recurse -Force
    Fail "verification failed on staged output. Target was not modified."
}

# Activation: backup existing .agents if present
$backupPath = $null
if (Test-Path -LiteralPath $AgentsDir) {
    $backupPath = Join-Path $Target (".agents.backup-" + $stamp)
    Move-Item -LiteralPath $AgentsDir -Destination $backupPath -Force
    Write-Output "Backup written: $backupPath"
}

try {
    Move-Item -LiteralPath $stagingDir -Destination $AgentsDir -Force
} catch {
    if ($null -ne $backupPath -and (Test-Path -LiteralPath $backupPath)) {
        Move-Item -LiteralPath $backupPath -Destination $AgentsDir -Force
        Write-Error "ROLLBACK: restored previous installation from $backupPath"
    }
    Fail "activation failed: cannot move staging to $AgentsDir. Error: $_"
}

if ($GitInit -and (-not (Test-Path -LiteralPath (Join-Path $Target ".git")))) {
    try { git -C $Target init 2>&1 | Out-Null } catch {}
}

# Ensure root bootstrap pointer exists for harnesses (Antigravity, OpenCode, Claude Code)
$rootAgentsMd = Join-Path $Target "AGENTS.md"
if (-not (Test-Path -LiteralPath $rootAgentsMd)) {
    $rootAgentsContent = @"
# Digi-Brain Operating Memory

This repository uses Digi-Brain persistent operating memory.
- **Session Bootstrap:** Follow [.agents/rules/session-bootstrap.md](.agents/rules/session-bootstrap.md) on turn 1.
- **Brain Router:** [.agents/memory/brain.md](.agents/memory/brain.md)
- **Engineering Standards:** [.agents/rules/engineering-standards.md](.agents/rules/engineering-standards.md)
- **Policy Enforcement:** [.agents/rules/policy-enforcement.md](.agents/rules/policy-enforcement.md)
"@
    [System.IO.File]::WriteAllText($rootAgentsMd, $rootAgentsContent.Trim() + "`n")
}

$rootClaudeMd = Join-Path $Target "CLAUDE.md"
if (-not (Test-Path -LiteralPath $rootClaudeMd)) {
    $rootClaudeContent = @"
# Digi-Brain Operating Memory

This repository uses Digi-Brain persistent operating memory.
- **Session Bootstrap:** Follow [.agents/rules/session-bootstrap.md](.agents/rules/session-bootstrap.md) on turn 1.
- **Brain Router:** [.agents/memory/brain.md](.agents/memory/brain.md)
- **Engineering Standards:** [.agents/rules/engineering-standards.md](.agents/rules/engineering-standards.md)
- **Policy Enforcement:** [.agents/rules/policy-enforcement.md](.agents/rules/policy-enforcement.md)
"@
    [System.IO.File]::WriteAllText($rootClaudeMd, $rootClaudeContent.Trim() + "`n")
}


Write-Output "---"
Write-Output "INSTALL OK: $AgentsDir"
Write-Output "Next: open a fresh agent session in the target repo and follow .agents/BOOT-CHECKLIST.md"
