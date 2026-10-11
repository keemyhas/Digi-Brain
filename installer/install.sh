#!/bin/sh
# Digi Brain installer (POSIX). Windows twin: install.ps1 - same behavior, shared SPEC-installer.md contract.
# Usage: ./install.sh <target-repo> [--overwrite] [--git-init] [--verify-only]
# No network access. Nothing leaves the machine.
set -eu

TARGET="${1:-}"
OVERWRITE=0; DO_GIT=0; VERIFY_ONLY=0; ASK_DEFAULTS=0; ANSWERS_FILE=""
for a in "$@"; do
  case "$a" in
    --overwrite) OVERWRITE=1 ;;
    --git-init) DO_GIT=1 ;;
    --verify-only) VERIFY_ONLY=1 ;;
    --defaults) ASK_DEFAULTS=1 ;;
    --answers-file=*) ANSWERS_FILE="${a#--answers-file=}" ;;
  esac
done

fail() { echo "INSTALLER ABORT: $1"; exit 1; }
ask() { # ask <VAR> <prompt> <default>
  if [ "$ASK_DEFAULTS" -eq 1 ]; then eval "$1=\"$3\""; return; fi
  if [ -n "$ANSWERS_FILE" ]; then
    hit="$(grep -E "^$1=" "$ANSWERS_FILE" 2>/dev/null | tail -n 1 | cut -d= -f2-)"
    if [ -n "$hit" ]; then eval "$1=\"$hit\""; return; fi
  fi
  printf "%s [%s]: " "$2" "$3"
  IFS= read -r ans || ans=""
  if [ -z "$ans" ]; then ans="$3"; fi
  eval "$1=\"$ans\""
}

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../template"

[ -n "$TARGET" ] || fail "usage: ./install.sh <target-repo> [--overwrite] [--git-init]"
[ -d "$TEMPLATE_DIR" ] || fail "template/ not found next to installer."

if [ -e "$TARGET/SPEC-digi-brain.md" ] || [ -e "$TARGET/template" ]; then
  fail "target looks like the Digi Brain source tree. Install into a foreign repo."
fi

AGENTS_DIR="$TARGET/.agents"
if [ -e "$AGENTS_DIR" ] && [ "$OVERWRITE" -eq 0 ] && [ "$VERIFY_ONLY" -eq 0 ]; then
  fail "$AGENTS_DIR exists. Re-run with --overwrite (timestamped backup first)."
fi

if [ "$VERIFY_ONLY" -eq 1 ]; then
  [ -d "$AGENTS_DIR" ] || fail "nothing installed at $AGENTS_DIR."
  if grep -rEn "\{\{[A-Z_]+\}\}" "$AGENTS_DIR" --include="*.md" | head -5 | grep -q .; then
    fail "unresolved placeholders remain."
  fi
  echo "VERIFY OK: no unresolved placeholders under $AGENTS_DIR."
  exit 0
fi

echo "--- Digi Brain install: single interview (Enter = default, 'none' where allowed) ---"
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
ask QUERY_PLACEHOLDER_STYLE "Query placeholder style" "$1, $2, ..."
ask DATA_PROTECTION_STANDARD "Data-protection standard" "AES-256 at rest, TLS in transit"
ask SENSITIVE_RESOURCES "Sensitive resources" "user-owned records, credentials, tokens"
ask KEY_COLUMNS "High-traffic key columns" "id, created_at, status"
ask PROTECTED_COLUMNS_POLICY "Protected-column policy" "no storage-layer computation on protected columns"
ask DOMAIN_REVIEWER "Domain safety reviewer" "Owner (default; type a name to override)"
ask WORKFLOWS_DIR "Workflows dir" "workflows"
WORKFLOWS_DIR="$(printf '%s' "$WORKFLOWS_DIR" | sed 's|/$||')"
ask DOMAIN_DOCS "Extra domain docs" "memory/architecture.md only"
ask SYNC_RULE "Multi-mirror sync rule ('single' = one tree)" "single"
ask OWNER_DOMAIN "Business domain (one line)" "general web operations"
ask COMPLIANCE_STANDARD "Compliance standard ('none' if any)" "none"
ask OFFLINE_STRATEGY "Offline strategy ('none' if any)" "none"
ask LARGE_CLIENT_FILES "Large client files ('none' if any)" "none"
ask CODE_GRAPH "Code-graph tool ('none' if any)" "none"

[ "$TWIN_NAME" = "none" ] && TWIN_NAME="Autonomous mode disabled."
[ "$DOMAIN_REVIEWER" = "none" ] && DOMAIN_REVIEWER="Owner (default; type a name to override)"

if [ -e "$AGENTS_DIR" ]; then
  STAMP="$(date +%Y%m%d-%H%M%S)"
  cp -r "$AGENTS_DIR" "$TARGET/.agents.backup-$STAMP"
  echo "Backup written: $TARGET/.agents.backup-$STAMP"
  rm -rf "$AGENTS_DIR"
fi
mkdir -p "$AGENTS_DIR"
cp -r "$TEMPLATE_DIR/." "$AGENTS_DIR/"

[ "$CODE_GRAPH" = "none" ] && rm -f "$AGENTS_DIR/rules/code-graph.md"

# Substitute every token from the interview.
VARS="OWNER_NAME OWNER_ROLE PROJECT_NAME ACTIVATION_PHRASE TWIN_NAME SAFETY_INVARIANTS
SAFETY_INVARIANTS_FILE BACKEND_DIRS BACKEND_SCOPE FRONTEND_DIRS FRONTEND_SCOPE
TEST_COMMAND TYPE_CHECK TEST_FRAMEWORK TESTS_DIR TEST_SCOPE DATABASE MIGRATIONS_DIR
MIGRATION_NAMING DOCS_DIR API_DOCS ADR_DIR FUTURE_PLANS_DIR QA_DIR FIXTURE_PREFIX
OWNER_PERSONAS DEV_URL AUTH_MIDDLEWARE SAFETY_MIDDLEWARE QUERY_PLACEHOLDER_STYLE
DATA_PROTECTION_STANDARD SENSITIVE_RESOURCES KEY_COLUMNS PROTECTED_COLUMNS_POLICY
DOMAIN_REVIEWER WORKFLOWS_DIR DOMAIN_DOCS SYNC_RULE OWNER_DOMAIN COMPLIANCE_STANDARD
OFFLINE_STRATEGY LARGE_CLIENT_FILES CODE_GRAPH"
for f in $(find "$AGENTS_DIR" -type f); do
  for v in $VARS; do
    val="$(eval "echo \"\$$v\"")"
    # perl-free: python-free single-token replace via sed with | delimiter
    esc_val="$(printf '%s' "$val" | sed 's/[&|\\]/\\&/g')"
    sed -i "s|{{$v}}|$esc_val|g" "$f"
  done
  case "$f" in
    *.template.md) mv "$f" "${f%.template.md}.md" ;;
  esac
done

printf '# Skills map (generated - all rows start as prose fallbacks; replace with harness skill names)\n\n| Gate | Harness skill |\n|---|---|\n| spec-before-code | none - prose fallback |\n| multi-file build | none - prose fallback |\n| bug-fix | none - prose fallback |\n| security | none - prose fallback |\n| shipping | none - prose fallback |\n\nSource: SKILLS-MANIFEST.md next to this map. Fallback exercise (mandatory on first session): run one gate entirely in prose and log it.\n' > "$AGENTS_DIR/skills-map.md"

if [ -f "$SCRIPT_DIR/BOOT-CHECKLIST.template.md" ]; then
  cp "$SCRIPT_DIR/BOOT-CHECKLIST.template.md" "$AGENTS_DIR/BOOT-CHECKLIST.md"
  for v in $VARS; do
    val="$(eval "echo \"\$$v\"")"
    esc_val="$(printf '%s' "$val" | sed 's/[&|\\]/\\&/g')"
    sed -i "s|{{$v}}|$esc_val|g" "$AGENTS_DIR/BOOT-CHECKLIST.md"
  done
fi

if [ "$DO_GIT" -eq 1 ] && [ ! -e "$TARGET/.git" ]; then git -C "$TARGET" init >/dev/null 2>&1; fi

# Setup banners served their purpose pre-substitution; installed files must not lecture about install.
for f in $(find "$AGENTS_DIR" -type f -name "*.md"); do
  grep -v "^> Setup:" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done

if grep -rEn "\{\{[A-Z_]+\}\}" "$AGENTS_DIR" --include="*.md" | head -5 | grep -q .; then
  echo "VERIFY FAILED: unresolved placeholders."; exit 1
fi
if grep -rEin "abdul|hassan|archon|falx|vellora|synapseems" "$AGENTS_DIR" --include="*.md" | grep -v "grep -rniE" | grep -q .; then
  echo "VERIFY FAILED: fingerprint terms in output."; exit 1
fi

echo "---"
echo "INSTALL OK: $AGENTS_DIR"
echo "Next: open a fresh agent session in the target repo and follow .agents/BOOT-CHECKLIST.md"
