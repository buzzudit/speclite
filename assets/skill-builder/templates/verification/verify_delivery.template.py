#!/usr/bin/env python3
"""Delivery gate for {{skill_name}}.

Runs all verification scripts and checks that all deliverables exist.

Usage: python3 verify_delivery.py <session.json> <output-dir>
Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


VERIFICATION_SCRIPTS = {{verification_script_paths}}


def run_script(script_path, *args):
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + list(args),
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0, result.stdout + result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return False, str(e)


def check_deliverables_exist(session_data, output_dir, errors):
    deliverables = session_data.get("deliverables", {})
    for key, rel_path in deliverables.items():
        full_path = output_dir / rel_path
        if not full_path.exists():
            errors.append(f"Deliverable '{key}' not found at {rel_path}")
        elif full_path.stat().st_size == 0:
            errors.append(f"Deliverable '{key}' is empty at {rel_path}")


def check_provenance(session_data, errors):
    prov = session_data.get("provenance", {})
    if not prov.get("academic"):
        errors.append("No academic provenance citations in session")
    if not prov.get("industry"):
        errors.append("No industry provenance citations in session")


def main():
    parser = argparse.ArgumentParser(description="Delivery gate.")
    parser.add_argument("session", help="Path to SESSION.json")
    parser.add_argument("output_dir", help="Path to output directory")
    args = parser.parse_args()

    session_path = Path(args.session)
    output_dir = Path(args.output_dir)

    if not session_path.exists():
        print(f"FAIL: Session file not found: {session_path}", file=sys.stderr)
        sys.exit(1)

    try:
        session_data = json.loads(session_path.read_text())
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid session JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []
    verdicts = {}

    scripts_dir = Path(__file__).parent
    for script_name in VERIFICATION_SCRIPTS:
        script_path = scripts_dir / script_name
        if not script_path.exists():
            errors.append(f"Verification script not found: {script_name}")
            verdicts[script_name] = "MISSING"
            continue
        passed, output = run_script(script_path, str(session_path))
        verdicts[script_name] = "PASS" if passed else "FAIL"
        if not passed:
            errors.append(f"Verification script failed: {script_name}\n    {output.strip()}")

    check_deliverables_exist(session_data, output_dir, errors)
    check_provenance(session_data, errors)

    print("Delivery gate results:")
    for script, verdict in verdicts.items():
        print(f"  {script}: {verdict}")

    if errors:
        print(f"\nFAIL: {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("\nPASS: All checks passed. Ready for delivery.")
    sys.exit(0)


if __name__ == "__main__":
    main()
