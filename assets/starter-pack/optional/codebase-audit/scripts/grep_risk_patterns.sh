#!/usr/bin/env bash
# Curated risk greps for the codebase-audit skill.
#
# Every hit is a CANDIDATE, not a finding. The point is to narrow where model
# judgment gets spent. Verify each hit by reading the surrounding code before it
# reaches the report.
#
# Adapts to the project's structure — searches whatever source directories exist.
#
# Always exits 0 — hits are expected. Run from the repo root:
#   bash .claude/skills/codebase-audit/scripts/grep_risk_patterns.sh

set -uo pipefail

REPO="${1:-.}"
cd "$REPO" || exit 0

EXCL=(--exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git
      --exclude-dir=out --exclude-dir=dist --exclude-dir=__pycache__
      --exclude-dir=.turbo --exclude-dir=venv --exclude-dir=.venv
      --exclude-dir=env --exclude-dir=build --exclude-dir=target
      --exclude-dir=coverage --exclude-dir=.mypy_cache
      --exclude=package-lock.json --exclude=yarn.lock --exclude=pnpm-lock.yaml)

# Discover source directories
SRC=()
for d in src app/src lib app server api backend frontend web marketing/src extension packages; do
  [ -d "$d" ] && SRC+=("$d")
done
# Also check for migration directories
for d in supabase/migrations app/supabase/migrations migrations db/migrate prisma/migrations; do
  [ -d "$d" ] && SRC+=("$d")
done
[ ${#SRC[@]} -eq 0 ] && SRC=(".")

section() {
  echo
  echo "=== $1 ==="
  echo "--- why: $2"
}

hits() {
  local pat="$1"; shift
  grep -rnE "${EXCL[@]}" "$@" -- "$pat" "${SRC[@]}" 2>/dev/null || echo "  (none)"
}

# === Language-agnostic patterns ===

section "Secrets in client-visible env vars" \
  "NEXT_PUBLIC_, VITE_, REACT_APP_ vars ship in the client bundle"
hits 'NEXT_PUBLIC_[A-Z0-9_]*(KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)|VITE_[A-Z0-9_]*(KEY|SECRET|TOKEN|PASSWORD)|REACT_APP_[A-Z0-9_]*(KEY|SECRET|TOKEN|PASSWORD)'

section "Empty or swallowing catch blocks" \
  "a silent catch turns a failure into a wrong answer the user trusts"
grep -rnE "${EXCL[@]}" -A2 -- 'catch\s*(\([^)]*\))?\s*\{' "${SRC[@]}" 2>/dev/null \
  | grep -E 'catch.*\{\s*\}|\{\s*$' -A1 \
  | grep -B1 -E '^\S+-[0-9]+-\s*\}\s*$' | head -60 || echo "  (none obvious)"
# Python bare except
hits 'except:\s*$|except\s+Exception\s*:\s*$' || true
echo "  [also run: grep -rn 'catch' / 'except' and read each by hand]"

section "Console/print statements in application code" \
  "may leak sensitive data; bypasses structured logging"
hits 'console\.(log|info|warn|error|debug)|print\(|puts\s|logger\.(info|debug|warn)\('

section "Type assertion escape hatches" \
  "an 'as' cast or type ignore at a boundary asserts a shape nobody validated"
hits 'as any|as unknown as|@ts-ignore|@ts-expect-error|eslint-disable|# type:\s*ignore|# noqa'

section "HTML injection sinks" \
  "XSS risk"
hits 'dangerouslySetInnerHTML|innerHTML\s*=|v-html|safe\s*\||mark_safe|raw\s*%>'

section "Client-supplied identifiers in mutations" \
  "an org/user/tenant id read from input instead of the session is an authz hole"
hits 'formData\.get\(.(org|organization|tenant|practice|user|account)' -i
hits 'request\.(body|query|params)\.\s*(org|organization|tenant|practice|user|account)' -i

section "External calls without an obvious timeout" \
  "a hung external call strands the request"
hits 'fetch\(|axios\.|requests\.(get|post|put|patch|delete)|httpx\.|Net::HTTP|anthropic\.|openai\.'

section "Raw SQL / direct database calls" \
  "string-built SQL bypasses the ORM/typed query layer"
hits '\.rpc\(|execute_sql|sql`|query\(`|\.raw\(|\.execute\(|cursor\.(execute|fetchall)|ActiveRecord.*find_by_sql'

section "Auth check patterns (inventory — absence is the finding)" \
  "which endpoints assert a session at all"
hits 'getUser\(\)|getSession\(\)|requireAuth|isAuthenticated|authenticate|authorize|@login_required|@permission_required|before_action.*authenticate|jwt\.verify|verifyToken|auth\(\)|protect\('

section "Cron and webhook endpoint auth" \
  "an unauthenticated cron/webhook endpoint is a public mutation surface"
hits 'CRON_SECRET|authorization.*bearer|x-cron|vercel-cron|webhook.*secret|WEBHOOK_SECRET' -i

section "Sensitive data fields near logging or errors" \
  "read each hit: is a sensitive field interpolated into a message?"
hits '(first_name|last_name|email|password|ssn|social_security|dob|date_of_birth|credit_card|card_number|account_number|api_key|secret_key|access_token)'

section "TODO / FIXME / HACK / STUB markers" \
  "cross-check against planning/stubs.md if it exists"
hits 'TODO|FIXME|HACK|XXX|STUB|stub|not implemented|placeholder' -i

section "Hardcoded URLs and IPs" \
  "may point to dev/staging in production, or leak internal infrastructure"
hits 'http://localhost|127\.0\.0\.1|0\.0\.0\.0|hardcoded|\.internal\.' -i

echo
echo "=== summary ==="
echo "Every section above is candidates only. Phase 3 verification is mandatory:"
echo "open each cited line, confirm the failure scenario is reachable, drop what is not."
exit 0
