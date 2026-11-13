#!/usr/bin/env python3
"""Validate a Scenario Mould session record (SESSION.json).

Usage: python3 verify_session.py SESSION.json
Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import sys
from pathlib import Path

REQUIRED_DECISIONS = ["scope", "layout", "variables", "calibration", "broken", "output"]
VALID_STATUSES = {"confirmed", "delegated"}
VALID_PROBE_ACTIONS = {"fill", "select", "check", "uncheck"}
REQUIRED_COVERAGE = [
    "everyday", "empty", "missing", "long-labels", "near-duplicates",
    "stress", "error-state", "loading-state", "partial-data",
]
NON_WAIVABLE = {"everyday", "stress"}


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
            errors.append(f"Decision '{key}' has invalid status '{status}' (expected confirmed|delegated)")
        if status == "delegated":
            assumptions = rec.get("assumptions", "")
            if not isinstance(assumptions, str) or not assumptions.strip():
                errors.append(f"Delegated decision '{key}' must have nonempty 'assumptions' string")


def check_scenarios(data, errors):
    if "scenarios" not in data or not isinstance(data["scenarios"], list):
        errors.append("Missing or invalid 'scenarios' array")
        return []
    scenarios = data["scenarios"]
    ids = []
    for i, sc in enumerate(scenarios):
        if not isinstance(sc, dict):
            errors.append(f"Scenario at index {i} is not an object")
            continue
        for field in ("id", "title"):
            if field not in sc:
                errors.append(f"Scenario at index {i} missing field '{field}'")
        sid = sc.get("id", "")
        expected_id = f"S{i + 1}"
        if sid != expected_id:
            errors.append(f"Scenario at index {i} has id '{sid}', expected '{expected_id}'")
        ids.append(sid)
    if not scenarios:
        errors.append("Scenarios array is empty")
    return ids


def check_widths(data, errors):
    if "widths" not in data or not isinstance(data["widths"], list):
        errors.append("Missing or invalid 'widths' array")
        return []
    widths = data["widths"]
    if not widths:
        errors.append("Widths array is empty")
        return []
    for w in widths:
        if not isinstance(w, (int, float)) or w <= 0 or w != int(w):
            errors.append(f"Width '{w}' is not a finite positive integer")
    has_zoom = any(w <= 800 for w in widths)
    if not has_zoom:
        errors.append("NOTE: No zoom-equivalent width found (expected a width <= 800px, e.g. 720 for 200% zoom of 1440)")
    return widths


def check_calibration(data, errors, scenario_ids, widths):
    if "calibration" not in data or not isinstance(data["calibration"], dict):
        errors.append("Missing or invalid 'calibration' object")
        return
    cal = data["calibration"]
    for field in ("scenario", "width"):
        if field not in cal:
            errors.append(f"Calibration missing field '{field}'")
    sc = cal.get("scenario")
    if sc and sc not in scenario_ids:
        errors.append(f"Calibration scenario '{sc}' not in declared scenarios")
    w = cal.get("width")
    if w and w not in widths:
        errors.append(f"Calibration width {w} not in declared widths")


def check_coverage(data, errors, scenario_ids):
    if "coverage" not in data or not isinstance(data["coverage"], dict):
        errors.append("Missing or invalid 'coverage' object")
        return
    coverage = data["coverage"]
    for key in REQUIRED_COVERAGE:
        if key not in coverage:
            errors.append(f"Missing coverage key: '{key}'")
            continue
        val = coverage[key]
        if isinstance(val, dict):
            if val.get("not_applicable"):
                if key in NON_WAIVABLE:
                    errors.append(f"Coverage key '{key}' cannot be waived (not_applicable)")
                if not val.get("reason"):
                    errors.append(f"Coverage '{key}' marked not_applicable but missing 'reason'")
                if not val.get("source"):
                    errors.append(f"Coverage '{key}' marked not_applicable but missing 'source'")
            else:
                errors.append(f"Coverage '{key}' is an object but not marked not_applicable")
        elif isinstance(val, list):
            for sid in val:
                if sid not in scenario_ids:
                    errors.append(f"Coverage '{key}' references unknown scenario '{sid}'")
            if key == "stress" and len(set(val)) < 2:
                errors.append(f"Coverage 'stress' must have at least 2 distinct scenario IDs, got {len(set(val))}")
        else:
            errors.append(f"Coverage '{key}' must be an array of scenario IDs or a not_applicable object")


def check_variables(data, errors):
    if "variables" not in data or not isinstance(data["variables"], list):
        errors.append("Missing or invalid 'variables' array")
        return
    selectors = []
    for i, var in enumerate(data["variables"]):
        if not isinstance(var, dict):
            errors.append(f"Variable at index {i} is not an object")
            continue
        for field in ("id", "label", "bounds", "default", "evidence", "probe"):
            if field not in var:
                errors.append(f"Variable '{var.get('id', f'index {i}')}' missing field '{field}'")
        probe = var.get("probe")
        if isinstance(probe, dict):
            action = probe.get("action")
            if action not in VALID_PROBE_ACTIONS:
                errors.append(f"Variable '{var.get('id', f'index {i}')}' probe has invalid action '{action}'")
            for pfield in ("value", "selector"):
                if pfield not in probe:
                    errors.append(f"Variable '{var.get('id', f'index {i}')}' probe missing '{pfield}'")
            sel = probe.get("selector")
            if sel:
                selectors.append((var.get("id", f"index {i}"), sel))
        elif probe is not None:
            errors.append(f"Variable '{var.get('id', f'index {i}')}' probe is not an object")
    seen = {}
    for vid, sel in selectors:
        if sel in seen:
            errors.append(f"Duplicate selector '{sel}' in variables '{seen[sel]}' and '{vid}'")
        seen[sel] = vid


def main():
    parser = argparse.ArgumentParser(description="Validate a Scenario Mould session record.")
    parser.add_argument("session_json", help="Path to SESSION.json")
    args = parser.parse_args()

    path = Path(args.session_json)
    if not path.exists():
        print(f"FAIL: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print("FAIL: Top-level value must be an object", file=sys.stderr)
        sys.exit(1)

    errors = []

    check_decisions(data, errors)
    scenario_ids = check_scenarios(data, errors)
    widths = check_widths(data, errors)
    check_calibration(data, errors, scenario_ids, widths)
    check_coverage(data, errors, scenario_ids)
    check_variables(data, errors)

    notes = [e for e in errors if e.startswith("NOTE:")]
    failures = [e for e in errors if not e.startswith("NOTE:")]

    for note in notes:
        print(note)

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        print(f"\n--- {len(failures)} failure(s), {len(notes)} note(s) ---")
        sys.exit(1)
    else:
        print(f"PASS: Session record is valid ({len(notes)} note(s))")
        sys.exit(0)


if __name__ == "__main__":
    main()
