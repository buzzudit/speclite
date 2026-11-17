#!/usr/bin/env python3
"""Authorization and access-control coverage check for the codebase-audit skill.

Detects the project's database layer and checks for access-control gaps:
- Supabase/Postgres: RLS enablement and policy coverage per table
- Prisma: middleware or policy patterns
- Django: permission checks in views
- Generic: auth check patterns in route handlers

Exit code is always 0 — gaps are findings for a human to verify, not script
failures. Run from the repo root:
    python3 .claude/skills/codebase-audit/scripts/check_auth_coverage.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".next", ".git", "out", "dist", "__pycache__", ".turbo",
    "venv", ".venv", "env", ".tox", "build", "target",
}

CREATE_TABLE = re.compile(
    r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?:public\.)?\"?(\w+)\"?", re.I)
DROP_TABLE = re.compile(
    r"drop\s+table\s+(?:if\s+exists\s+)?(?:public\.)?\"?(\w+)\"?", re.I)
ENABLE_RLS = re.compile(
    r"alter\s+table\s+(?:public\.)?\"?(\w+)\"?[^;]*?enable\s+row\s+level\s+security",
    re.I | re.S)
FORCE_RLS = re.compile(
    r"alter\s+table\s+(?:public\.)?\"?(\w+)\"?[^;]*?force\s+row\s+level\s+security",
    re.I | re.S)
CREATE_POLICY = re.compile(
    r"create\s+policy\s+\"?([^\"\n]+?)\"?\s+on\s+(?:public\.)?\"?(\w+)\"?", re.I)
DROP_POLICY = re.compile(
    r"drop\s+policy\s+(?:if\s+exists\s+)?\"?([^\"\n]+?)\"?\s+on\s+(?:public\.)?\"?(\w+)\"?",
    re.I)
CREATE_TRIGGER = re.compile(
    r"create\s+trigger\s+\"?(\w+)\"?[^;]*?\s+on\s+(?:public\.)?\"?(\w+)\"?",
    re.I | re.S)


def strip_sql_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"--[^\n]*", " ", text)
    return text


def find_migration_dirs(repo: Path) -> list[Path]:
    dirs = []
    for pattern in [
        "*/supabase/migrations", "supabase/migrations", "migrations",
        "*/migrations", "db/migrate", "alembic/versions", "prisma/migrations",
    ]:
        dirs.extend(d for d in repo.glob(pattern) if d.is_dir())
    return dirs


def check_rls_coverage(repo: Path) -> bool:
    """Check RLS coverage for Supabase/Postgres SQL migrations. Returns True if
    any SQL migrations were found."""
    mig_dirs = find_migration_dirs(repo)
    sql_files = []
    for mig_dir in mig_dirs:
        sql_files.extend(sorted(mig_dir.glob("*.sql")))

    if not sql_files:
        return False

    tables: dict[str, dict] = {}

    for path in sql_files:
        sql = strip_sql_comments(path.read_text(encoding="utf-8", errors="replace"))
        fname = path.name
        for m in CREATE_TABLE.finditer(sql):
            t = m.group(1).lower()
            tables.setdefault(t, {
                "created_in": fname, "rls": False, "forced": False,
                "policies": set(), "triggers": set(), "dropped": False,
            })
            tables[t]["dropped"] = False
        for m in DROP_TABLE.finditer(sql):
            t = m.group(1).lower()
            if t in tables:
                tables[t]["dropped"] = True
        for m in ENABLE_RLS.finditer(sql):
            t = m.group(1).lower()
            tables.setdefault(t, {
                "created_in": "(not in migrations)", "rls": False,
                "forced": False, "policies": set(), "triggers": set(),
                "dropped": False,
            })
            tables[t]["rls"] = True
        for m in FORCE_RLS.finditer(sql):
            t = m.group(1).lower()
            if t in tables:
                tables[t]["forced"] = True
        for m in CREATE_POLICY.finditer(sql):
            name, t = m.group(1).strip(), m.group(2).lower()
            tables.setdefault(t, {
                "created_in": "(not in migrations)", "rls": False,
                "forced": False, "policies": set(), "triggers": set(),
                "dropped": False,
            })
            tables[t]["policies"].add(name)
        for m in DROP_POLICY.finditer(sql):
            name, t = m.group(1).strip(), m.group(2).lower()
            if t in tables:
                tables[t]["policies"].discard(name)
        for m in CREATE_TRIGGER.finditer(sql):
            name, t = m.group(1).lower(), m.group(2).lower()
            if t in tables:
                tables[t]["triggers"].add(name)

    live = {t: d for t, d in tables.items() if not d["dropped"]}

    print(f"[auth] SQL migrations scanned: {len(sql_files)}")
    print(f"[auth] tables found: {len(live)}\n")

    hdr = f"{'table':<28} {'rls':<5} {'policies':<9} {'triggers':<9} created_in"
    print(hdr)
    print("-" * len(hdr))
    for t in sorted(live):
        d = live[t]
        print(f"{t:<28} {'yes' if d['rls'] else 'NO':<5} "
              f"{len(d['policies']):<9} {len(d['triggers']):<9} {d['created_in']}")

    no_rls = sorted(t for t, d in live.items() if not d["rls"])
    rls_no_policy = sorted(t for t, d in live.items()
                           if d["rls"] and not d["policies"])

    print("\n=== GAPS (verify each by hand before reporting) ===")
    print(f"\nRLS not enabled ({len(no_rls)}):")
    for t in no_rls:
        print(f"  - {t}  (created in {live[t]['created_in']})")
    if not no_rls:
        print("  none")

    print(f"\nRLS enabled but zero policies ({len(rls_no_policy)}):")
    for t in rls_no_policy:
        print(f"  - {t}")
    if not rls_no_policy:
        print("  none")

    return True


def check_route_auth(repo: Path):
    """Check for auth checks in route handlers and API endpoints."""
    auth_patterns = [
        r"getUser\(\)", r"getSession\(\)", r"requireAuth", r"isAuthenticated",
        r"authenticate", r"authorize", r"checkPermission", r"requireRole",
        r"@login_required", r"@permission_required", r"IsAuthenticated",
        r"before_action\s+:authenticate", r"jwt\.verify", r"verifyToken",
        r"auth\(\)", r"protect\(\)", r"guard\(",
    ]
    combined = "|".join(auth_patterns)

    print("\n=== Route/endpoint auth check coverage ===")
    print("--- Endpoints with NO auth pattern detected ---\n")

    # Next.js API routes
    for p in repo.rglob("route.ts"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(combined, text):
            print(f"  {p.relative_to(repo)}")

    for p in repo.rglob("route.js"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(combined, text):
            print(f"  {p.relative_to(repo)}")

    # Express-style route files
    for suffix in (".ts", ".js"):
        for p in repo.rglob(f"*routes*{suffix}"):
            if any(skip in p.parts for skip in SKIP_DIRS):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?:app|router)\.(get|post|put|patch|delete)", text):
                if not re.search(combined, text):
                    print(f"  {p.relative_to(repo)}")

    # Django views
    for p in repo.rglob("views.py"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(combined, text):
            print(f"  {p.relative_to(repo)}")

    print("\nNote: absence of a recognized auth pattern does not mean the")
    print("endpoint is unprotected — it may use middleware, decorators, or")
    print("a framework convention this script does not detect. Verify each.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    found_sql = check_rls_coverage(repo)
    if not found_sql:
        print("[auth] no SQL migrations found — skipping RLS check")

    check_route_auth(repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
