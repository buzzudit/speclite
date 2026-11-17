#!/usr/bin/env python3
"""Surface inventory for the codebase-audit skill.

Deterministic map of what exists, so the lens passes never have to re-explore
the tree. Writes JSON to stdout (and to --out if given).

Detects the project shape automatically: Next.js, Express, Django, Rails,
generic Node, generic Python, etc. Add detection for new frameworks as needed.

Run from the repo root:
    python3 .claude/skills/codebase-audit/scripts/collect_inventory.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".next", ".git", "out", "dist", "__pycache__", ".turbo",
    "venv", ".venv", "env", ".tox", "build", "target", ".cache", "coverage",
    ".mypy_cache", ".pytest_cache",
}


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            yield Path(dirpath) / f


def rel(p: Path, repo: Path) -> str:
    try:
        return str(p.relative_to(repo))
    except ValueError:
        return str(p)


def detect_framework(repo: Path) -> dict:
    """Detect the project's framework and language from files on disk."""
    signals = {
        "has_package_json": (repo / "package.json").is_file(),
        "has_requirements_txt": (repo / "requirements.txt").is_file(),
        "has_pyproject_toml": (repo / "pyproject.toml").is_file(),
        "has_gemfile": (repo / "Gemfile").is_file(),
        "has_cargo_toml": (repo / "Cargo.toml").is_file(),
        "has_go_mod": (repo / "go.mod").is_file(),
    }

    frameworks = []
    pkg_json_dirs = []

    for p in repo.rglob("package.json"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        pkg_json_dirs.append(p.parent)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "next" in deps:
            frameworks.append({"type": "nextjs", "root": rel(p.parent, repo)})
        elif "express" in deps:
            frameworks.append({"type": "express", "root": rel(p.parent, repo)})
        elif "fastify" in deps:
            frameworks.append({"type": "fastify", "root": rel(p.parent, repo)})
        elif "nuxt" in deps:
            frameworks.append({"type": "nuxt", "root": rel(p.parent, repo)})
        elif "react" in deps:
            frameworks.append({"type": "react", "root": rel(p.parent, repo)})
        elif "vue" in deps:
            frameworks.append({"type": "vue", "root": rel(p.parent, repo)})

    if any((repo / d / "manage.py").is_file() for d in [".", *os.listdir(repo)]
           if (repo / d).is_dir()):
        frameworks.append({"type": "django", "root": "."})
    if (repo / "config" / "routes.rb").is_file():
        frameworks.append({"type": "rails", "root": "."})

    return {"signals": signals, "frameworks": frameworks}


def find_source_dirs(repo: Path) -> list[Path]:
    """Find directories likely containing application source code."""
    candidates = [
        "src", "app/src", "lib", "app", "server", "api", "backend", "frontend",
        "web", "marketing/src", "extension", "packages",
    ]
    dirs = []
    for c in candidates:
        p = repo / c
        if p.is_dir():
            dirs.append(p)
    if not dirs:
        dirs.append(repo)
    return dirs


def collect_routes_nextjs(root: Path, repo: Path) -> dict:
    """Collect routes from a Next.js App Router project."""
    app_dir = root / "src" / "app"
    if not app_dir.is_dir():
        app_dir = root / "app"
    if not app_dir.is_dir():
        return {}

    pages, api_routes, server_action_files, client_components = [], [], [], []
    for p in walk(app_dir):
        if p.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        r = rel(p, repo)
        name = p.name
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        if name in {"page.tsx", "page.ts", "page.jsx", "page.js"}:
            pages.append(r)
        if name in {"route.ts", "route.tsx", "route.js", "route.jsx"}:
            methods = sorted(set(re.findall(
                r"export\s+(?:async\s+)?function\s+(GET|POST|PUT|PATCH|DELETE)", text)))
            api_routes.append({"file": r, "methods": methods})
        if '"use server"' in text or "'use server'" in text:
            actions = sorted(set(re.findall(
                r"export\s+(?:async\s+)?function\s+(\w+)", text)))
            server_action_files.append({"file": r, "exports": actions})
        if '"use client"' in text or "'use client'" in text:
            client_components.append(r)
    return {
        "pages": sorted(pages),
        "api_routes": sorted(api_routes, key=lambda d: d["file"]),
        "server_action_files": sorted(server_action_files, key=lambda d: d["file"]),
        "client_components": sorted(client_components),
    }


def collect_routes_express(root: Path, repo: Path) -> dict:
    """Collect route definitions from an Express-like project."""
    routes = []
    for p in walk(root):
        if p.suffix not in {".ts", ".js"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(
            r"(?:app|router)\.(get|post|put|patch|delete|all)\s*\(\s*['\"`]([^'\"`]+)",
            text, re.I,
        ):
            routes.append({
                "file": rel(p, repo),
                "method": m.group(1).upper(),
                "path": m.group(2),
            })
    return {"routes": routes}


def collect_packages(repo: Path) -> dict:
    """Collect dependency info from all package.json files."""
    out = {}
    for p in repo.rglob("package.json"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        r = rel(p, repo)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            out[r] = {"_parse_error": str(e)}
            continue
        out[r] = {
            "dependencies": data.get("dependencies", {}),
            "devDependencies": data.get("devDependencies", {}),
            "scripts": sorted(data.get("scripts", {}).keys()),
        }
    return out


def collect_python_packages(repo: Path) -> dict:
    """Collect dependency info from Python project files."""
    out = {}
    for name in ("requirements.txt", "requirements-dev.txt", "pyproject.toml",
                  "setup.py", "setup.cfg", "Pipfile"):
        p = repo / name
        if p.is_file():
            out[name] = {"exists": True, "lines": p.read_text(
                encoding="utf-8", errors="replace").count("\n") + 1}
    return out


def collect_migrations(repo: Path) -> list[dict]:
    """Collect database migration info from common migration directories."""
    out = []
    migration_dirs = []

    for pattern in [
        "*/supabase/migrations", "supabase/migrations", "migrations",
        "*/migrations", "db/migrate", "alembic/versions", "prisma/migrations",
    ]:
        migration_dirs.extend(repo.glob(pattern))

    for mig_dir in migration_dirs:
        if not mig_dir.is_dir():
            continue
        for p in sorted(mig_dir.glob("*.sql")):
            text = p.read_text(encoding="utf-8", errors="replace")
            out.append({
                "file": rel(p, repo),
                "lines": text.count("\n") + 1,
                "creates_tables": sorted(set(re.findall(
                    r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?:public\.)?\"?(\w+)\"?",
                    text, re.I))),
            })
        for p in sorted(mig_dir.rglob("*.py")):
            out.append({"file": rel(p, repo), "type": "python_migration"})
        for p in sorted(mig_dir.rglob("*.rb")):
            out.append({"file": rel(p, repo), "type": "ruby_migration"})

    # Prisma schema
    for p in repo.rglob("schema.prisma"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        out.append({"file": rel(p, repo), "type": "prisma_schema"})

    return out


def collect_env_surface(repo: Path) -> dict:
    """Collect environment variable references from source code."""
    public_vars, all_vars = set(), set()

    public_prefixes = ("NEXT_PUBLIC_", "VITE_", "REACT_APP_", "NUXT_PUBLIC_")

    for src_dir in find_source_dirs(repo):
        for p in walk(src_dir):
            if p.suffix not in {".ts", ".tsx", ".js", ".jsx", ".py", ".rb"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in re.finditer(r"process\.env\.([A-Z0-9_]+)", text):
                v = m.group(1)
                all_vars.add(v)
                if any(v.startswith(pfx) for pfx in public_prefixes):
                    public_vars.add(v)
            for m in re.finditer(r"import\.meta\.env\.([A-Z0-9_]+)", text):
                v = m.group(1)
                all_vars.add(v)
                if any(v.startswith(pfx) for pfx in public_prefixes):
                    public_vars.add(v)
            for m in re.finditer(r"os\.environ(?:\.get)?\s*\(\s*['\"]([A-Z0-9_]+)", text):
                all_vars.add(m.group(1))

    return {"public": sorted(public_vars), "all": sorted(all_vars)}


def git_tracked(repo: Path, patterns: list[str]) -> dict:
    """Check whether sensitive file patterns are tracked in git."""
    out = {}
    for pat in patterns:
        try:
            r = subprocess.run(
                ["git", "ls-files", "--error-unmatch", pat],
                cwd=repo, capture_output=True, text=True, timeout=20,
            )
            out[pat] = {
                "tracked": r.returncode == 0,
                "files": [ln for ln in r.stdout.splitlines() if ln],
            }
        except (OSError, subprocess.SubprocessError) as e:
            out[pat] = {"error": str(e)}
    return out


def find_sensitive_patterns(repo: Path) -> list[str]:
    """Build a list of sensitive file patterns to check based on what exists."""
    patterns = [".env"]
    for p in repo.rglob(".env*"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        patterns.append(rel(p, repo))
    for name in ("keys", "secrets", "credentials"):
        for p in repo.rglob(name):
            if p.is_dir() and not any(skip in p.parts for skip in SKIP_DIRS):
                patterns.append(rel(p, repo))
    return sorted(set(patterns))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    try:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=repo,
            capture_output=True, text=True, timeout=20,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        sha = "unknown"

    framework_info = detect_framework(repo)

    # Collect routes based on detected framework
    app_routes = {}
    for fw in framework_info["frameworks"]:
        fw_root = repo / fw["root"]
        if fw["type"] == "nextjs":
            app_routes[fw["root"]] = collect_routes_nextjs(fw_root, repo)
        elif fw["type"] in ("express", "fastify"):
            app_routes[fw["root"]] = collect_routes_express(fw_root, repo)

    report = {
        "repo": str(repo),
        "commit": sha,
        "project_shape": framework_info,
        "routes": app_routes,
        "migrations": collect_migrations(repo),
        "packages": collect_packages(repo),
        "python_packages": collect_python_packages(repo),
        "env": collect_env_surface(repo),
        "sensitive_paths": git_tracked(repo, find_sensitive_patterns(repo)),
    }

    text = json.dumps(report, indent=2, sort_keys=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(text)

    # Summary
    route_count = sum(
        len(v.get("pages", v.get("routes", [])))
        for v in app_routes.values()
    )
    print(
        f"\n[inventory] commit={sha} frameworks={len(framework_info['frameworks'])} "
        f"routes={route_count} "
        f"migrations={len(report['migrations'])} "
        f"public_env={len(report['env']['public'])}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
