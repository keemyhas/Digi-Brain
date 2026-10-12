#!/bin/sh
# Digi Brain installer (POSIX). Windows twin: install.ps1 - same behavior, shared SPEC-installer.md contract.
# Usage: ./install.sh <target-repo> [--overwrite] [--git-init] [--verify-only] [--defaults] [--answers-file=<path>]
# No network access. Nothing leaves the machine.
set -eu

fail() { printf "INSTALLER ABORT: %s\n" "$1" >&2; exit 1; }

TARGET=""
OVERWRITE=0
DO_GIT=0
VERIFY_ONLY=0
ASK_DEFAULTS=0
ANSWERS_FILE=""

# Parse arguments safely
while [ $# -gt 0 ]; do
  case "$1" in
    --overwrite) OVERWRITE=1; shift ;;
    --git-init) DO_GIT=1; shift ;;
    --verify-only) VERIFY_ONLY=1; shift ;;
    --defaults) ASK_DEFAULTS=1; shift ;;
    --answers-file=*) ANSWERS_FILE="${1#--answers-file=}"; shift ;;
    --answers-file)
      shift
      [ $# -gt 0 ] || fail "missing argument for --answers-file"
      ANSWERS_FILE="$1"
      shift
      ;;
    -*) fail "unknown option: $1" ;;
    *)
      if [ -z "$TARGET" ]; then
        TARGET="$1"
      else
        fail "unexpected argument: $1"
      fi
      shift
      ;;
  esac
done

[ -n "$TARGET" ] || fail "usage: ./install.sh <target-repo> [--overwrite] [--git-init] [--verify-only] [--defaults] [--answers-file=<path>]"

# Resolve absolute target path safely
if [ ! -d "$TARGET" ]; then
  mkdir -p "$TARGET" || fail "cannot create target directory: $TARGET"
fi
TARGET_CANONICAL="$(cd "$TARGET" 2>/dev/null && pwd)" || fail "cannot resolve target path: $TARGET"
TARGET="$TARGET_CANONICAL"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../template"
BOOT_TEMPLATE="$SCRIPT_DIR/BOOT-CHECKLIST.template.md"

[ -d "$TEMPLATE_DIR" ] || fail "template/ directory not found at $TEMPLATE_DIR"

if [ -e "$TARGET/SPEC-digi-brain.md" ] && [ -d "$TARGET/template" ]; then
  fail "target looks like the Digi Brain source tree ($TARGET). Install into a foreign repo."
fi

AGENTS_DIR="$TARGET/.agents"

# Unified verification function
run_verify() {
  check_dir="$1"
  v_pass=1

  printf "=== DIGI-BRAIN VERIFICATION ===\n"

  # 1. Structure check
  struct_ok=1
  for req_d in memory rules agents workflows; do
    if [ ! -d "$check_dir/$req_d" ]; then
      printf "  MISSING DIR: %s\n" "$req_d"
      struct_ok=0
    fi
  done
  if [ "$struct_ok" -eq 1 ]; then
    printf "STRUCTURE CHECK: PASS\n"
  else
    printf "STRUCTURE CHECK: FAIL\n"
    v_pass=0
  fi

  # 2. Bootstrap check
  boot_ok=1
  for req_f in memory/brain.md BOOT-CHECKLIST.md rules/session-bootstrap.md skills-map.md SKILLS-MANIFEST.md; do
    if [ ! -f "$check_dir/$req_f" ]; then
      printf "  MISSING BOOTSTRAP FILE: %s\n" "$req_f"
      boot_ok=0
    fi
  done
  if [ "$boot_ok" -eq 1 ]; then
    printf "BOOTSTRAP CHECK: PASS\n"
  else
    printf "BOOTSTRAP CHECK: FAIL\n"
    v_pass=0
  fi

  # 3. Safety check
  safe_ok=1
  for req_f in rules/engineering-standards.md rules/memory-intake.md rules/project-logging.md rules/code-documentation-and-onboarding.md; do
    if [ ! -f "$check_dir/$req_f" ]; then
      printf "  MISSING SAFETY FILE: %s\n" "$req_f"
      safe_ok=0
    fi
  done
  if [ "$safe_ok" -eq 1 ]; then
    printf "SAFETY CHECK: PASS\n"
  else
    printf "SAFETY CHECK: FAIL\n"
    v_pass=0
  fi

  # 4. Placeholder check
  unresolved="$(find "$check_dir" -type f -name "*.md" -exec grep -HnE "\{\{[A-Z0-9_*]+\}\}" {} + 2>/dev/null || true)"
  if [ -z "$unresolved" ]; then
    printf "PLACEHOLDER CHECK: PASS\n"
  else
    printf "PLACEHOLDER CHECK: FAIL\n"
    printf "%s\n" "$unresolved" | head -n 5
    v_pass=0
  fi

  # 5. Fingerprint scan
  fp_hits="$(find "$check_dir" -type f -name "*.md" -exec grep -HniE "abdul|hassan|archon|falx|vellora|synapseems" {} + 2>/dev/null | grep -v "grep -rn" | grep -v "fingerprint" || true)"
  if [ -z "$fp_hits" ]; then
    printf "FINGERPRINT SCAN: PASS\n"
  else
    printf "FINGERPRINT SCAN: FAIL\n"
    printf "%s\n" "$fp_hits" | head -n 5
    v_pass=0
  fi

  # 6. Secret-pattern scan
  secret_regex='ghp_[A-Za-z0-9_]{36,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|bearer[[:space:]]+[A-Za-z0-9_\-\.]{20,}|password[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']+["'"'"']'
  sec_hits="$(find "$check_dir" -type f -name "*.md" -exec grep -HnE "$secret_regex" {} + 2>/dev/null || true)"
  if [ -z "$sec_hits" ]; then
    printf "SECRET-PATTERN SCAN: PASS\n"
  else
    printf "SECRET-PATTERN SCAN: FAIL\n"
    printf "%s\n" "$sec_hits" | head -n 5
    v_pass=0
  fi

  if [ "$v_pass" -eq 1 ]; then
    printf "OVERALL: PASS\n"
    return 0
  else
    printf "OVERALL: FAIL\n"
    return 1
  fi
}

if [ "$VERIFY_ONLY" -eq 1 ]; then
  [ -d "$AGENTS_DIR" ] || fail "nothing installed at $AGENTS_DIR"
  if run_verify "$AGENTS_DIR"; then
    exit 0
  else
    exit 1
  fi
fi

if [ -e "$AGENTS_DIR" ] && [ "$OVERWRITE" -eq 0 ]; then
  fail "$AGENTS_DIR exists. Re-run with --overwrite (timestamped backup first)."
fi

CONFIG_FILE="$(mktemp "${TMPDIR:-/tmp}/digi_cfg.XXXXXX")"
trap 'rm -f "$CONFIG_FILE"' EXIT

set_config() {
  _k="$1"
  _v="$2"
  case "$_k" in
    OWNER_NAME|OWNER_ROLE|PROJECT_NAME|ACTIVATION_PHRASE|TWIN_NAME|SAFETY_INVARIANTS|\
    SAFETY_INVARIANTS_FILE|BACKEND_DIRS|BACKEND_SCOPE|FRONTEND_DIRS|FRONTEND_SCOPE|\
    TEST_COMMAND|TYPE_CHECK|TEST_FRAMEWORK|TESTS_DIR|TEST_SCOPE|DATABASE|MIGRATIONS_DIR|\
    MIGRATION_NAMING|DOCS_DIR|API_DOCS|ADR_DIR|FUTURE_PLANS_DIR|QA_DIR|FIXTURE_PREFIX|\
    OWNER_PERSONAS|DEV_URL|AUTH_MIDDLEWARE|SAFETY_MIDDLEWARE|QUERY_PLACEHOLDER_STYLE|\
    DATA_PROTECTION_STANDARD|SENSITIVE_RESOURCES|KEY_COLUMNS|PROTECTED_COLUMNS_POLICY|\
    DOMAIN_REVIEWER|WORKFLOWS_DIR|DOMAIN_DOCS|SYNC_RULE|OWNER_DOMAIN|COMPLIANCE_STANDARD|\
    OFFLINE_STRATEGY|LARGE_CLIENT_FILES|CODE_GRAPH|CODE_GRAPH_*)
      printf "%s\t%s\n" "$_k" "$_v" >> "$CONFIG_FILE"
      ;;
    *)
      fail "unrecognized configuration key: $_k"
      ;;
  esac
}

get_config() {
  _k="$1"
  _def="$2"
  _hit="$(grep -E "^$_k	" "$CONFIG_FILE" 2>/dev/null | tail -n 1 | cut -f2- || true)"
  if [ -n "$_hit" ]; then
    printf '%s' "$_hit"
  else
    printf '%s' "$_def"
  fi
}

if [ -n "$ANSWERS_FILE" ]; then
  [ -f "$ANSWERS_FILE" ] || fail "answers file not found: $ANSWERS_FILE"
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ""|\#*) continue ;;
    esac
    case "$line" in
      *=*)
        k="${line%%=*}"
        v="${line#*=}"
        k="$(printf '%s' "$k" | tr -d ' \t\r\n')"
        v="$(printf '%s' "$v" | tr -d '\r')"
        set_config "$k" "$v"
        ;;
      *)
        fail "malformed line in answers file: $line"
        ;;
    esac
  done < "$ANSWERS_FILE"
fi

ask() {
  _k="$1"
  _prompt="$2"
  _default="$3"

  _existing="$(grep -E "^$_k	" "$CONFIG_FILE" 2>/dev/null | tail -n 1 | cut -f2- || true)"
  if [ -n "$_existing" ]; then
    return 0
  fi

  if [ "$ASK_DEFAULTS" -eq 1 ]; then
    set_config "$_k" "$_default"
    return 0
  fi

  printf "%s [%s]: " "$_prompt" "$_default"
  IFS= read -r ans || ans=""
  if [ -z "$ans" ]; then
    ans="$_default"
  fi
  set_config "$_k" "$ans"
}

printf -- "--- Digi Brain install: single interview (Enter = default, 'none' where allowed) ---\n"
ask OWNER_NAME "Owner name" "Ada Example"
ask OWNER_ROLE "Owner role" "Solo Developer"
ask PROJECT_NAME "Project name" "Acme Project"
ask ACTIVATION_PHRASE "Autonomous-mode activation phrase" "take the wheel"
ask TWIN_NAME "Twin name ('none' disables autonomous mode)" "Deuter"
ask SAFETY_INVARIANTS "Safety invariants (free text, or 'none yet')" "None defined."
ask SAFETY_INVARIANTS_FILE "Safety invariants file" "none - same file, section 5"
ask BACKEND_DIRS "Backend dirs (comma list)" "src/"
ask BACKEND_SCOPE "Backend scope" "server-side services"
ask FRONTEND_DIRS "Frontend dirs (comma list)" "public/"
ask FRONTEND_SCOPE "Frontend scope" "user interfaces"
ask TEST_COMMAND "Test command" "npm test"
ask TYPE_CHECK "Type-check command" "npm run type-check"
ask TEST_FRAMEWORK "Test framework" "Jest"
ask TESTS_DIR "Tests dir" "tests/"
ask TEST_SCOPE "Test scope" "the full suite"
ask DATABASE "Database" "PostgreSQL"
ask MIGRATIONS_DIR "Migrations dir" "migrations/"
ask MIGRATION_NAMING "Migration naming" "YYYYMMDD_feature_name.sql"
ask DOCS_DIR "Docs dir" "docs/"
ask API_DOCS "API docs file" "docs/api.md"
ask ADR_DIR "ADR dir" "docs/adr/"
ask FUTURE_PLANS_DIR "Future-plans dir" "docs/future-plans/"
ask QA_DIR "QA workspace dir" ".qa/"
ask FIXTURE_PREFIX "Test fixture prefix" "QA-"
ask OWNER_PERSONAS "User personas (comma list)" "Admin, End User"
ask DEV_URL "Dev URL" "http://localhost:<port>"
ask AUTH_MIDDLEWARE "Auth middleware names" "requireAuth, requirePermission"
ask SAFETY_MIDDLEWARE "Safety middleware ('none' if any)" "none"
ask QUERY_PLACEHOLDER_STYLE "Query placeholder style" '$1, $2, ...'
ask DATA_PROTECTION_STANDARD "Data-protection standard" "AES-256 at rest, TLS in transit"
ask SENSITIVE_RESOURCES "Sensitive resources" "user-owned records, credentials, tokens"
ask KEY_COLUMNS "High-traffic key columns" "id, created_at, status"
ask PROTECTED_COLUMNS_POLICY "Protected-column policy" "no storage-layer computation on protected columns"
ask DOMAIN_REVIEWER "Domain safety reviewer" "Owner (default; type a name to override)"
ask WORKFLOWS_DIR "Workflows dir" "workflows"
ask DOMAIN_DOCS "Extra domain docs" "memory/architecture.md only"
ask SYNC_RULE "Multi-mirror sync rule ('single' = one tree)" "single"
ask OWNER_DOMAIN "Business domain (one line)" "general web operations"
ask COMPLIANCE_STANDARD "Compliance standard ('none' if any)" "none"
ask OFFLINE_STRATEGY "Offline strategy ('none' if any)" "none"
ask LARGE_CLIENT_FILES "Large client files ('none' if any)" "none"
ask CODE_GRAPH "Code-graph tool ('none' if any)" "none"

twin_val="$(get_config TWIN_NAME "Deuter")"
if [ "$twin_val" = "none" ]; then
  set_config TWIN_NAME "Autonomous mode disabled - activation phrase inert until a twin name is set."
fi

rev_val="$(get_config DOMAIN_REVIEWER "Owner")"
if [ "$rev_val" = "none" ]; then
  set_config DOMAIN_REVIEWER "Owner (default; type a name to override)"
fi

wf_val="$(get_config WORKFLOWS_DIR "workflows")"
wf_clean="$(printf '%s' "$wf_val" | sed 's|/*$||')"
set_config WORKFLOWS_DIR "$wf_clean"

cg_val="$(get_config CODE_GRAPH "none")"
set_config "CODE_GRAPH_*" "$cg_val"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
STAGING_DIR="$TARGET/.agents.staging.$TIMESTAMP.$$"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

cp -R "$TEMPLATE_DIR/." "$STAGING_DIR/"

if [ "$cg_val" = "none" ] && [ -f "$STAGING_DIR/rules/code-graph.md" ]; then
  rm -f "$STAGING_DIR/rules/code-graph.md"
fi

cat << 'EOF' > "$STAGING_DIR/skills-map.md"
# Skills map (generated - all rows start as prose fallbacks; replace with harness skill names)

| Gate | Harness skill |
|---|---|
| spec-before-code | none - prose fallback |
| multi-file build | none - prose fallback |
| bug-fix | none - prose fallback |
| security | none - prose fallback |
| shipping | none - prose fallback |

Source: SKILLS-MANIFEST.md next to this map. Fallback exercise (mandatory on first session): run one gate entirely in prose and log it.
EOF

if [ -f "$BOOT_TEMPLATE" ]; then
  cp "$BOOT_TEMPLATE" "$STAGING_DIR/BOOT-CHECKLIST.md"
fi

SUBST_AWK='
NR==FNR {
  split($0, arr, "\t");
  if (arr[1] != "") {
    tokens[arr[1]] = arr[2];
  }
  next;
}
{
  line = $0;
  for (t in tokens) {
    target = "{{" t "}}";
    idx = index(line, target);
    while (idx > 0) {
      line = substr(line, 1, idx - 1) tokens[t] substr(line, idx + length(target));
      idx = index(line, target);
    }
  }
  print line;
}
'

find "$STAGING_DIR" -type f | while IFS= read -r f; do
  awk -F'\t' "$SUBST_AWK" "$CONFIG_FILE" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  grep -v "^> Setup:" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  case "$f" in
    *.template.md)
      dest="${f%.template.md}.md"
      mv "$f" "$dest"
      ;;
  esac
done

if ! run_verify "$STAGING_DIR"; then
  rm -rf "$STAGING_DIR"
  fail "verification failed on staged output. Target was not modified."
fi

BACKUP_DIR=""
if [ -e "$AGENTS_DIR" ]; then
  BACKUP_DIR="$TARGET/.agents.backup-$TIMESTAMP"
  mv "$AGENTS_DIR" "$BACKUP_DIR" || fail "cannot backup existing $AGENTS_DIR"
  printf "Backup written: %s\n" "$BACKUP_DIR"
fi

if ! mv "$STAGING_DIR" "$AGENTS_DIR"; then
  if [ -n "$BACKUP_DIR" ] && [ -d "$BACKUP_DIR" ]; then
    mv "$BACKUP_DIR" "$AGENTS_DIR" || true
    printf "ROLLBACK: restored previous installation from %s\n" "$BACKUP_DIR" >&2
  fi
  fail "activation failed: cannot move staging to $AGENTS_DIR"
fi

if [ "$DO_GIT" -eq 1 ] && [ ! -e "$TARGET/.git" ]; then
  git -C "$TARGET" init >/dev/null 2>&1 || true
fi

# Ensure root bootstrap pointer exists for harnesses (Antigravity, OpenCode, Claude Code)
if [ ! -e "$TARGET/AGENTS.md" ]; then
  cat << 'EOF' > "$TARGET/AGENTS.md"
# Digi-Brain Operating Memory

This repository uses Digi-Brain persistent operating memory.
- **Session Bootstrap:** Follow [.agents/rules/session-bootstrap.md](.agents/rules/session-bootstrap.md) on turn 1.
- **Brain Router:** [.agents/memory/brain.md](.agents/memory/brain.md)
- **Engineering Standards:** [.agents/rules/engineering-standards.md](.agents/rules/engineering-standards.md)
- **Policy Enforcement:** [.agents/rules/policy-enforcement.md](.agents/rules/policy-enforcement.md)
EOF
fi

printf -- "---\n"
printf "INSTALL OK: %s\n" "$AGENTS_DIR"
printf "Next: open a fresh agent session in the target repo and follow .agents/BOOT-CHECKLIST.md\n"
