#!/usr/bin/env python3
"""Validate a {{skill_name}} session record (SESSION.json).

Usage: python3 verify_session.py SESSION.json
Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_DECISIONS = {{required_decision_keys}}
VALID_STATUSES = {"confirmed", "delegated"}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return False


def check_decisions(data, errors):
    if "decisions" not in data or not isinstance(data["decisions"], dict):
        errors.append("Missing or invalid 'decisions' object")
        return
    decisions = data["decisions"]
    for key in REQUIRED_DECISIONS:
        if key not in decisions:
            errors.append(f"Missing decision record: '{key}'")
            continue
        rec = decisions[key]
        if not isinstance(rec, dict):
            errors.append(f"Decision '{key}' is not an object")
            continue
        for field in ("status", "value", "evidence"):
            if field not in rec:
                errors.append(f"Decision '{key}' missing field '{field}'")
        status = rec.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"Decision '{key}' has invalid status '{status}'")
        if status == "delegated":
            assumptions = rec.get("assumptions", "")
            if not isinstance(assumptions, str) or not assumptions.strip():
                errors.append(f"Delegated decision '{key}' must have nonempty 'assumptions'")


def check_deliverables(data, errors):
    if "deliverables" not in data or not isinstance(data["deliverables"], dict):
        errors.append("Missing or invalid 'deliverables' object")
        return
    deliverables = data["deliverables"]
    for key, path in deliverables.items():
        if not isinstance(path, str) or not path.strip():
            errors.append(f"Deliverable '{key}' has empty path")


{{#custom_checks}}
def check_{{check_id}}(data, errors):
    """{{check_description}}"""
    {{check_body}}


{{/custom_checks}}

def main():
    parser = argparse.ArgumentParser(description="Validate a session record.")
    parser.add_argument("session", help="Path to SESSION.json")
    args = parser.parse_args()

    path = Path(args.session)
    if not path.exists():
        print(f"FAIL: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []
    check_decisions(data, errors)
    check_deliverables(data, errors)
    {{#custom_checks}}
    check_{{check_id}}(data, errors)
    {{/custom_checks}}

    if errors:
        print(f"FAIL: {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: Session record is valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
