#!/usr/bin/env python3
"""Validate a complete speclite skill package.

Checks that the skill directory has the required files for its declared shape,
the manifest is valid, verification scripts exist, and provenance is populated.

Usage: python3 validate_skill_package.py <skill-directory>
Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import sys
from pathlib import Path

SHAPE_REQUIRED_FILES = {
    "session-flow": [
        "SKILL.md",
        "skill-manifest.json",
        "references/session-guide.md",
        "references/enforcement.md",
        "references/report-format.md",
    ],
    "reference": [
        "SKILL.md",
        "skill-manifest.json",
    ],
    "one-shot": [
        "SKILL.md",
        "skill-manifest.json",
    ],
    "recurring-check": [
        "SKILL.md",
        "skill-manifest.json",
        "references/check-criteria.md",
    ],
}


def check_files_exist(skill_dir, shape, errors):
    required = SHAPE_REQUIRED_FILES.get(shape, ["SKILL.md", "skill-manifest.json"])
    for rel_path in required:
        full = skill_dir / rel_path
        if not full.exists():
            errors.append(f"Missing required file: {rel_path}")


def check_manifest_valid(skill_dir, errors):
    manifest_path = skill_dir / "skill-manifest.json"
    if not manifest_path.exists():
        errors.append("skill-manifest.json not found")
        return None
    try:
        data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"skill-manifest.json is invalid JSON: {e}")
        return None
    return data


def check_name_matches_dir(skill_dir, data, errors):
    if data is None:
        return
    manifest_name = data.get("name", "")
    dir_name = skill_dir.name
    if manifest_name != dir_name:
        errors.append(
            f"Manifest name '{manifest_name}' does not match "
            f"directory name '{dir_name}'"
        )


def check_skill_md_frontmatter(skill_dir, errors):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return
    text = skill_md.read_text()
    if not text.startswith("---"):
        errors.append("SKILL.md missing YAML frontmatter")
        return
    end = text.find("---", 3)
    if end == -1:
        errors.append("SKILL.md frontmatter not closed")
        return
    frontmatter = text[3:end]
    if "name:" not in frontmatter:
        errors.append("SKILL.md frontmatter missing 'name'")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter missing 'description'")


def check_verification_scripts_exist(skill_dir, data, errors):
    if data is None:
        return
    ver = data.get("verification", {})
    scripts = ver.get("scripts", [])
    for script in scripts:
        script_path = script.get("path", "")
        if script_path and not (skill_dir / script_path).exists():
            errors.append(f"Verification script not found: {script_path}")


def check_provenance_populated(data, errors):
    if data is None:
        return
    prov = data.get("provenance", {})
    academic = prov.get("academic", [])
    industry = prov.get("industry", [])
    if not academic:
        errors.append("Provenance has no academic citations")
    if not industry:
        errors.append("Provenance has no industry citations")


def check_ports_populated(data, errors):
    if data is None:
        return
    ports = data.get("ports", {})
    outputs = ports.get("outputs", [])
    if not outputs:
        errors.append("No output ports declared")


def main():
    parser = argparse.ArgumentParser(description="Validate a skill package.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.is_dir():
        print(f"FAIL: Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    errors = []

    data = check_manifest_valid(skill_dir, errors)

    shape = data.get("shape", "session-flow") if data else "session-flow"
    check_files_exist(skill_dir, shape, errors)
    check_name_matches_dir(skill_dir, data, errors)
    check_skill_md_frontmatter(skill_dir, errors)
    check_verification_scripts_exist(skill_dir, data, errors)
    check_provenance_populated(data, errors)
    check_ports_populated(data, errors)

    if errors:
        print(f"FAIL: {len(errors)} error(s) in {skill_dir.name}:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: {skill_dir.name} is a valid skill package.")
    sys.exit(0)


if __name__ == "__main__":
    main()
