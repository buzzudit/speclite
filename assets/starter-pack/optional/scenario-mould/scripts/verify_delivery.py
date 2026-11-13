#!/usr/bin/env python3
"""Final delivery gate for a Scenario Mould.

Usage: python3 verify_delivery.py MOULD.html SESSION.json EVIDENCE_DIR REPORT.md

Presents three separate verdicts:
  - Contract checks: PASS/FAIL
  - Browser checks: PASS/FAIL
  - Calibration: matched/differs/not checked

Exit 0 only if contract and browser both pass. Calibration is informational.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

REQUIRED_REVIEWS = [
    "source-fidelity", "synthetic-data", "coverage", "visual", "recommendations",
]
VALID_REVIEW_STATUSES = {"reviewed", "provisional"}


def sha256_file(fpath):
    return hashlib.sha256(Path(fpath).read_bytes()).hexdigest()


def check_contract(session_path, errors):
    """Check session JSON has reviews with valid structure."""
    try:
        data = json.loads(Path(session_path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        errors.append(f"Cannot read session JSON: {e}")
        return None

    reviews = data.get("reviews")
    if not isinstance(reviews, dict):
        errors.append("Session JSON missing 'reviews' object")
        return data

    for key in REQUIRED_REVIEWS:
        if key not in reviews:
            errors.append(f"Missing review record: '{key}'")
            continue
        rec = reviews[key]
        if not isinstance(rec, dict):
            errors.append(f"Review '{key}' is not an object")
            continue

        status = rec.get("status")
        if status not in VALID_REVIEW_STATUSES:
            errors.append(f"Review '{key}' has invalid status '{status}' (expected reviewed|provisional)")

        if not rec.get("evidence"):
            errors.append(f"Review '{key}' missing 'evidence' field")

        if status == "provisional" and not rec.get("limitation"):
            errors.append(f"Provisional review '{key}' missing 'limitation' field")

    return data


def check_browser(evidence_dir, session_path, errors):
    """Check browser-checks.json exists and all checks passed."""
    bc_path = Path(evidence_dir) / "browser-checks.json"
    if not bc_path.exists():
        errors.append(f"browser-checks.json not found in {evidence_dir}")
        return None

    try:
        bc = json.loads(bc_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"browser-checks.json contains invalid JSON: {e}")
        return None

    if bc.get("error"):
        errors.append(f"Browser checks had an error: {bc['error']}")

    checks = bc.get("checks", [])
    if not checks:
        errors.append("browser-checks.json has no check records")
        return bc

    failed = [c for c in checks if c.get("status") == "FAIL"]
    if failed:
        for f in failed:
            errors.append(f"Browser check failed: {f.get('check', '?')} — {f.get('details', '')}")

    # Hash verification
    if session_path and Path(session_path).exists():
        current_hash = sha256_file(session_path)
        recorded_hash = bc.get("sessionHash")
        if recorded_hash and current_hash != recorded_hash:
            errors.append(
                f"Session JSON has changed since browser checks ran "
                f"(current: {current_hash[:12]}…, recorded: {recorded_hash[:12]}…). "
                f"Finalize reviews and rerun browser checks."
            )

    return bc


def check_calibration(mould_path, report_path):
    """Extract calibration status from the report."""
    if not Path(report_path).exists():
        return "not checked", "Report file not found"

    text = Path(report_path).read_text(encoding="utf-8")

    for literal in ("Calibration: matched", "Calibration: differs", "Calibration: not checked"):
        if literal in text:
            status = literal.replace("Calibration: ", "")
            return status, literal

    return "not checked", "No calibration literal found in report"


def check_evidence_files(evidence_dir, errors):
    """Check required evidence files exist."""
    required = ["rendered.html", "results.json", "browser-checks.json", "workspace.png"]
    for fname in required:
        fpath = Path(evidence_dir) / fname
        if not fpath.exists():
            errors.append(f"Missing evidence file: {fname}")


def main():
    parser = argparse.ArgumentParser(description="Scenario Mould delivery gate.")
    parser.add_argument("mould_html", help="Path to the mould HTML file")
    parser.add_argument("session_json", help="Path to SESSION.json")
    parser.add_argument("evidence_dir", help="Path to evidence directory")
    parser.add_argument("report_md", help="Path to the Markdown report")
    args = parser.parse_args()

    for fpath, label in [
        (args.mould_html, "Mould HTML"),
        (args.session_json, "Session JSON"),
        (args.report_md, "Report"),
    ]:
        if not Path(fpath).exists():
            print(f"FAIL: {label} not found: {fpath}", file=sys.stderr)
            sys.exit(1)

    if not Path(args.evidence_dir).is_dir():
        print(f"FAIL: Evidence directory not found: {args.evidence_dir}", file=sys.stderr)
        sys.exit(1)

    # --- Contract checks ---
    contract_errors = []
    check_contract(args.session_json, contract_errors)
    check_evidence_files(args.evidence_dir, contract_errors)
    contract_pass = len(contract_errors) == 0

    # --- Browser checks ---
    browser_errors = []
    check_browser(args.evidence_dir, args.session_json, browser_errors)
    browser_pass = len(browser_errors) == 0

    # --- Calibration ---
    cal_status, cal_detail = check_calibration(args.mould_html, args.report_md)

    # --- Report ---
    print("=" * 60)
    print("SCENARIO MOULD DELIVERY GATE")
    print("=" * 60)

    print(f"\n  Contract checks:  {'PASS' if contract_pass else 'FAIL'}")
    if contract_errors:
        for e in contract_errors:
            print(f"    - {e}")

    print(f"\n  Browser checks:   {'PASS' if browser_pass else 'FAIL'}")
    if browser_errors:
        for e in browser_errors:
            print(f"    - {e}")

    print(f"\n  Calibration:      {cal_status}")
    print(f"    {cal_detail}")

    if cal_status == "differs":
        print("    NOTE: Results may be shared with an explicit limitation; do not relabel as matched.")
    elif cal_status == "not checked":
        print("    NOTE: Results are provisional until calibrated against the real product.")

    print("\n" + "=" * 60)

    overall = contract_pass and browser_pass
    if overall:
        print(f"DELIVERY: READY (calibration: {cal_status})")
    else:
        print("DELIVERY: BLOCKED")

    print("=" * 60)

    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
