#!/usr/bin/env python3
"""Plan/doc coherence checks for the codebase-audit skill.

Mechanical checks that keep the planning corpus trustworthy:
  1. planning/tech-stack.md declared versions vs real dependency manifests
  2. stories/index.md links vs real file paths, folder, and Status: header
  3. planning/bookkeeping.md root-file rules vs what is at the root
  4. planning/stubs.md file references vs what exists on disk

Adapts to the project's structure — skips checks for docs that do not exist.

Exit code is always 0 — drift is a finding for a human, not a script failure.
Run from the repo root:
    python3 .claude/skills/codebase-audit/scripts/check_doc_coherence.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".next", ".git", "out", "dist", "__pycache__", ".turbo",
    "venv", ".venv", "env", "build", "target",
}

ALLOWED_ROOT_FILES = {
    "agents.md", "AGENTS.md", "progress.md", "README.md", "readme.md",
    "LICENSE", "LICENSE.md", ".gitignore", "package.json", "package-lock.json",
    ".env", ".DS_Store", "CLAUDE.md", "claude.md",
}
ALLOWED_ROOT_PREFIXES = (".",)


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def norm_version(v: str) -> str:
    return re.sub(r"^[\^~>=<\s]+", "", (v or "").strip())


def check_tech_stack(repo: Path) -> list[str]:
    out = []
    ts = repo / "planning" / "tech-stack.md"
    if not ts.is_file():
        return []
    text = ts.read_text(encoding="utf-8", errors="replace")

    # Collect installed packages from all package.json files
    installed: dict[str, str] = {}
    for p in repo.rglob("package.json"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        pkg = load_json(p)
        for section in ("dependencies", "devDependencies"):
            for name, ver in (pkg.get(section) or {}).items():
                installed.setdefault(name, norm_version(ver))

    # Look for version declarations in table rows:
    # | Something | Package Name | 1.2.3 | notes |
    for m in re.finditer(
        r"\|\s*[^|]+\|\s*([^|]+?)\s*\|\s*([0-9][0-9.x]*)\s*\|", text
    ):
        name_col = m.group(1).strip()
        declared = m.group(2).strip()
        # Try to match the name column against known packages
        for pkg_name in installed:
            if pkg_name.lower() in name_col.lower() or name_col.lower() in pkg_name:
                actual = installed[pkg_name]
                if (not actual.startswith(declared.rstrip(".x"))
                        and not declared.startswith(actual)):
                    out.append(
                        f"tech-stack.md declares {name_col} {declared}, "
                        f"installed {pkg_name} is {actual}")

    # Check for libraries named in backticks that are not installed
    lib_section = re.search(r"\n## Libraries\n(.*?)(?=\n## |\Z)", text, re.S)
    if lib_section:
        for lib in re.findall(r"`(@?[a-z0-9][a-z0-9\-/.]+)`", lib_section.group(1)):
            if lib.endswith(".md") or lib in installed:
                continue
            if any(part.strip() in installed for part in lib.split("+")):
                continue
            out.append(
                f"tech-stack.md Libraries table names `{lib}` "
                f"but it is not in any package.json")
    return out


def check_story_index(repo: Path) -> list[str]:
    out = []
    idx = repo / "stories" / "index.md"
    if not idx.is_file():
        return []
    text = idx.read_text(encoding="utf-8", errors="replace")

    section = None
    for line in text.splitlines():
        h = re.match(r"^##\s+(.*)$", line)
        if h:
            section = h.group(1).strip()
            continue
        m = re.match(r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)", line)
        if not m:
            continue
        label, relpath = m.group(1), m.group(2)
        target = repo / "stories" / relpath
        if not target.is_file():
            out.append(f"index {label}: link does not resolve -> stories/{relpath}")
            continue
        body = target.read_text(encoding="utf-8", errors="replace")
        sm = re.search(r"^Status:\s*(\w+)", body, re.M)
        status = sm.group(1) if sm else None
        parts = Path(relpath).parts
        folder_status = parts[1] if len(parts) > 2 else None
        if status and folder_status and status != folder_status:
            out.append(f"index {label}: Status: {status} but file sits in "
                       f"{folder_status}/ ({relpath})")
        if section and status:
            sec = section.lower()
            expected = {
                "doing": "doing", "review": "review", "blocked": "blocked",
                "ready": "ready", "backlog": "backlog",
            }
            for key, want in expected.items():
                if sec.startswith(key) and status != want:
                    out.append(f"index {label}: listed under '{section}' "
                               f"but Status: {status}")
            if sec.startswith("recently done") and status != "done":
                out.append(f"index {label}: listed under '{section}' "
                           f"but Status: {status}")

    # Story files on disk that the index never links
    linked = set(re.findall(
        r"^\s*-\s*\[[^\]]+\]\(([^)]+)\)", text, re.M))
    stories_dir = repo / "stories"
    for p in sorted(stories_dir.rglob("*.md")):
        rel_str = str(p.relative_to(stories_dir))
        if rel_str in {"index.md", "story-template.md"}:
            continue
        if rel_str not in linked:
            out.append(f"story file not linked from index: stories/{rel_str}")
    return out


def check_root(repo: Path) -> list[str]:
    bookkeeping = repo / "planning" / "bookkeeping.md"
    if not bookkeeping.is_file():
        return []
    out = []
    for p in sorted(repo.iterdir()):
        if p.is_dir():
            continue
        name = p.name
        if name in ALLOWED_ROOT_FILES or name.startswith(ALLOWED_ROOT_PREFIXES):
            continue
        out.append(f"root file not allowed by bookkeeping.md root rules: {name}")
    return out


def check_stubs(repo: Path) -> list[str]:
    stubs = repo / "planning" / "stubs.md"
    if not stubs.is_file():
        return []
    out = []
    text = stubs.read_text(encoding="utf-8", errors="replace")
    live_lines = [
        ln for ln in text.splitlines()
        if not re.search(r"~~|REMOVED|REPLACED", ln, re.I)
    ]
    referenced = set(re.findall(
        r"`([a-zA-Z0-9_\-./]+\.(?:ts|tsx|js|jsx|py|rb|sql|json))`",
        "\n".join(live_lines)))
    for f in sorted(referenced):
        hits = list(repo.rglob(Path(f).name))
        hits = [h for h in hits
                if not any(skip in h.parts for skip in SKIP_DIRS)]
        if not hits:
            out.append(f"stubs.md references `{f}` but no such file exists")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    groups = [
        ("tech-stack.md vs dependencies", check_tech_stack(repo)),
        ("stories/index.md vs story files", check_story_index(repo)),
        ("bookkeeping.md root rules", check_root(repo)),
        ("stubs.md file references", check_stubs(repo)),
    ]
    total = 0
    for title, findings in groups:
        if not findings and title.startswith(("tech-stack", "stories", "stubs")):
            # Only print sections that had something to check
            ts_exists = (repo / "planning" / "tech-stack.md").is_file()
            idx_exists = (repo / "stories" / "index.md").is_file()
            stubs_exists = (repo / "planning" / "stubs.md").is_file()
            bk_exists = (repo / "planning" / "bookkeeping.md").is_file()
            if title.startswith("tech-stack") and not ts_exists:
                continue
            if title.startswith("stories") and not idx_exists:
                continue
            if title.startswith("stubs") and not stubs_exists:
                continue
            if title.startswith("bookkeeping") and not bk_exists:
                continue
        print(f"\n=== {title} ===")
        if not findings:
            print("  no drift detected")
        for f in findings:
            print(f"  - {f}")
            total += 1
    print(f"\n[doc-coherence] {total} drift item(s). Verify each before reporting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
