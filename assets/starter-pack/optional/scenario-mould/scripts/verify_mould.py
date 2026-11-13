#!/usr/bin/env python3
"""Validate a Scenario Mould's exported results and optional report.

Usage:
  python3 verify_mould.py RENDERED_DOM.html
  python3 verify_mould.py RENDERED_DOM.html --report REPORT.md

Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SEVERITY_LABELS = {
    "0": "Not a problem",
    "1": "Cosmetic",
    "2": "Minor",
    "3": "Major",
    "4": "Catastrophe",
}
VALID_STATUSES = {"PASS", "WARN", "BREAK"}
VALID_CALIBRATION_RESULTS = {"matched", "differs", "not checked"}

REQUIRED_REPORT_SECTIONS = [
    "Test Summary", "Recommendations", "Full Results",
    "Scorecard", "Assumptions", "Calibration", "Breakpoints",
]
CALIBRATION_LITERALS = [
    "Calibration: matched",
    "Calibration: differs",
    "Calibration: not checked",
]
FINDINGS_HEADER = "Scenario | Width | Code | Severity | Message"
BREAKPOINTS_HEADER = "Scenario | Metric | Width"
SCORECARD_HEADER = "Scenario | Widths tested | PASS | WARN | BREAK | Highest Severity"


class ResultsJSONExtractor(HTMLParser):
    """Extract the content of <script type="application/json" id="results-json">."""

    def __init__(self):
        super().__init__()
        self._inside = False
        self._chunks = []
        self.result = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if (tag == "script"
                and attr_dict.get("type") == "application/json"
                and attr_dict.get("id") == "results-json"):
            self._inside = True
            self._chunks = []

    def handle_data(self, data):
        if self._inside:
            self._chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._inside:
            self._inside = False
            self.result = "".join(self._chunks)


def extract_results_json(html_text):
    parser = ResultsJSONExtractor()
    parser.feed(html_text)
    return parser.result


def severity_to_status(sev):
    if sev <= 1:
        return "PASS"
    if sev == 2:
        return "WARN"
    return "BREAK"


def validate_dom(data, errors):
    required_top = ["title", "scenarios", "widths", "options", "severityScale",
                     "calibration", "results", "breakpoints", "tally"]
    for field in required_top:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    if not isinstance(data.get("title", ""), str) or not data.get("title", "").strip():
        errors.append("'title' must be a nonempty string")

    # Severity scale
    ss = data.get("severityScale", {})
    if isinstance(ss, dict):
        for k, v in SEVERITY_LABELS.items():
            if k not in ss:
                errors.append(f"severityScale missing key '{k}'")
            elif ss[k] != v:
                errors.append(f"severityScale['{k}'] is '{ss[k]}', expected '{v}'")
    else:
        errors.append("'severityScale' must be an object")

    # Scenarios
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("'scenarios' must be a nonempty array")
        return
    sc_ids = set()
    sc_titles = {}
    for sc in scenarios:
        sid = sc.get("id", "")
        sc_ids.add(sid)
        sc_titles[sid] = sc.get("title", "")

    # Widths
    widths = data.get("widths", [])
    if not isinstance(widths, list) or not widths:
        errors.append("'widths' must be a nonempty array")
        return
    width_set = set(widths)

    # Calibration
    cal = data.get("calibration", {})
    if isinstance(cal, dict):
        cal_result = cal.get("result")
        if cal_result not in VALID_CALIBRATION_RESULTS:
            errors.append(f"calibration.result '{cal_result}' not in {VALID_CALIBRATION_RESULTS}")
        cal_sc = cal.get("scenario")
        if cal_sc and cal_sc not in sc_ids:
            errors.append(f"calibration.scenario '{cal_sc}' not in declared scenarios")
        cal_w = cal.get("width")
        if cal_w and cal_w not in width_set:
            errors.append(f"calibration.width {cal_w} not in declared widths")
    else:
        errors.append("'calibration' must be an object")

    # Results — check every scenario × width cell
    results = data.get("results", [])
    if not isinstance(results, list):
        errors.append("'results' must be an array")
        return

    expected_cells = {(sid, w) for sid in sc_ids for w in widths}
    found_cells = set()
    tally_counts = {"PASS": 0, "WARN": 0, "BREAK": 0}
    row_peaks = {}  # scenario -> max severity

    for i, res in enumerate(results):
        if not isinstance(res, dict):
            errors.append(f"Result at index {i} is not an object")
            continue

        sc = res.get("scenario", "")
        title = res.get("title", "")
        w = res.get("width")
        status = res.get("status")
        highest = res.get("highestSeverity")
        flags = res.get("flags", [])

        if sc not in sc_ids:
            errors.append(f"Result {i}: scenario '{sc}' not in declared scenarios")
        if sc in sc_titles and title != sc_titles[sc]:
            errors.append(f"Result {i}: title '{title}' doesn't match declaration '{sc_titles[sc]}'")
        if w not in width_set:
            errors.append(f"Result {i}: width {w} not in declared widths")
        if status not in VALID_STATUSES:
            errors.append(f"Result {i}: invalid status '{status}'")

        cell = (sc, w)
        if cell in found_cells:
            errors.append(f"Result {i}: duplicate cell ({sc}, {w})")
        found_cells.add(cell)

        if status in tally_counts:
            tally_counts[status] += 1

        # Validate flags
        if not isinstance(flags, list):
            errors.append(f"Result {i}: 'flags' must be an array")
            flags = []

        max_flag_sev = 0
        for j, flag in enumerate(flags):
            if not isinstance(flag, dict):
                errors.append(f"Result {i}, flag {j}: not an object")
                continue
            for ff in ("code", "name", "severity", "message"):
                if ff not in flag:
                    errors.append(f"Result {i}, flag {j}: missing '{ff}'")
            fsev = flag.get("severity")
            if not isinstance(fsev, int) or fsev < 0 or fsev > 4:
                errors.append(f"Result {i}, flag {j}: severity must be int 0-4, got {fsev}")
            else:
                max_flag_sev = max(max_flag_sev, fsev)

        # highestSeverity must match
        if isinstance(highest, int):
            if highest != max_flag_sev:
                errors.append(f"Result {i} ({sc}@{w}): highestSeverity is {highest} but max flag severity is {max_flag_sev}")
            expected_status = severity_to_status(highest)
            if status != expected_status:
                errors.append(f"Result {i} ({sc}@{w}): status '{status}' doesn't match severity {highest} (expected '{expected_status}')")
        elif highest is not None:
            errors.append(f"Result {i}: highestSeverity must be an integer 0-4")

        # Track row peaks
        if isinstance(highest, int):
            row_peaks[sc] = max(row_peaks.get(sc, 0), highest)

    missing_cells = expected_cells - found_cells
    if missing_cells:
        for sc, w in sorted(missing_cells):
            errors.append(f"Missing result cell: ({sc}, {w})")

    extra_cells = found_cells - expected_cells
    if extra_cells:
        for sc, w in sorted(extra_cells):
            errors.append(f"Extra result cell: ({sc}, {w})")

    # Tally check
    tally = data.get("tally", {})
    if isinstance(tally, dict):
        for k in ("PASS", "WARN", "BREAK"):
            expected = tally_counts.get(k, 0)
            actual = tally.get(k, 0)
            if actual != expected:
                errors.append(f"Tally '{k}' is {actual}, expected {expected}")
    else:
        errors.append("'tally' must be an object")

    # Breakpoints
    bps = data.get("breakpoints", [])
    if isinstance(bps, list):
        for i, bp in enumerate(bps):
            if not isinstance(bp, dict):
                errors.append(f"Breakpoint {i}: not an object")
                continue
            bp_sc = bp.get("scenario")
            if bp_sc and bp_sc not in sc_ids:
                errors.append(f"Breakpoint {i}: scenario '{bp_sc}' not in declared scenarios")
            for key, val in bp.items():
                if key == "scenario":
                    continue
                if val is not None and (not isinstance(val, (int, float)) or val <= 0):
                    errors.append(f"Breakpoint {i}: '{key}' must be null or a positive number, got {val}")
    else:
        errors.append("'breakpoints' must be an array")


def validate_report(report_path, data, errors):
    text = Path(report_path).read_text(encoding="utf-8")

    # Required sections
    for section in REQUIRED_REPORT_SECTIONS:
        pattern = re.compile(r"^#+\s+" + re.escape(section), re.MULTILINE | re.IGNORECASE)
        if not pattern.search(text):
            errors.append(f"Report missing section: '{section}'")

    # Calibration literal
    has_cal = False
    for lit in CALIBRATION_LITERALS:
        if lit in text:
            has_cal = True
            break
    if not has_cal:
        errors.append("Report missing literal calibration line (one of: " + ", ".join(f"'{c}'" for c in CALIBRATION_LITERALS) + ")")

    # Fenced results appendix
    appendix_pattern = re.compile(r"```scenario-mould-results\s*\n(.*?)\n```", re.DOTALL)
    match = appendix_pattern.search(text)
    if not match:
        errors.append("Report missing fenced 'scenario-mould-results' appendix")
    else:
        try:
            appendix_data = json.loads(match.group(1))
            if isinstance(data, dict) and isinstance(appendix_data, dict):
                if data.get("tally") != appendix_data.get("tally"):
                    errors.append("Report appendix tally doesn't match DOM export tally")
                dom_sc_ids = {s["id"] for s in data.get("scenarios", [])}
                app_sc_ids = {s["id"] for s in appendix_data.get("scenarios", [])}
                if dom_sc_ids != app_sc_ids:
                    errors.append("Report appendix scenarios don't match DOM export scenarios")
        except json.JSONDecodeError:
            errors.append("Report appendix contains invalid JSON")

    # Table headers
    if FINDINGS_HEADER not in text:
        errors.append(f"Report missing findings table header: '{FINDINGS_HEADER}'")
    if BREAKPOINTS_HEADER not in text:
        errors.append(f"Report missing breakpoints table header: '{BREAKPOINTS_HEADER}'")
    if SCORECARD_HEADER not in text:
        errors.append(f"Report missing scorecard table header: '{SCORECARD_HEADER}'")

    # Matrix table — check first row starts with Scenario
    matrix_pattern = re.compile(r"^\|\s*Scenario\s*\|", re.MULTILINE)
    if not matrix_pattern.search(text):
        errors.append("Report missing matrix table (expected header starting with '| Scenario |')")

    # Scorecard totals cross-check
    scorecard_match = re.compile(
        r"^\|\s*Total\s*\|[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
        re.MULTILINE,
    ).search(text)
    if scorecard_match and isinstance(data, dict):
        tally = data.get("tally", {})
        sc_pass = int(scorecard_match.group(1))
        sc_warn = int(scorecard_match.group(2))
        sc_break = int(scorecard_match.group(3))
        if sc_pass != tally.get("PASS", 0):
            errors.append(f"Scorecard Total PASS ({sc_pass}) doesn't match tally ({tally.get('PASS', 0)})")
        if sc_warn != tally.get("WARN", 0):
            errors.append(f"Scorecard Total WARN ({sc_warn}) doesn't match tally ({tally.get('WARN', 0)})")
        if sc_break != tally.get("BREAK", 0):
            errors.append(f"Scorecard Total BREAK ({sc_break}) doesn't match tally ({tally.get('BREAK', 0)})")


def main():
    parser = argparse.ArgumentParser(description="Validate a Scenario Mould's exported results and report.")
    parser.add_argument("dom_html", help="Path to rendered DOM HTML")
    parser.add_argument("--report", help="Path to Markdown report for cross-validation")
    args = parser.parse_args()

    dom_path = Path(args.dom_html)
    if not dom_path.exists():
        print(f"FAIL: File not found: {dom_path}", file=sys.stderr)
        sys.exit(1)

    html_text = dom_path.read_text(encoding="utf-8")
    raw_json = extract_results_json(html_text)

    if not raw_json or not raw_json.strip():
        print("FAIL: No <script type=\"application/json\" id=\"results-json\"> found or it is empty", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(f"FAIL: results-json contains invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []
    validate_dom(data, errors)

    if args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            errors.append(f"Report file not found: {report_path}")
        else:
            validate_report(report_path, data, errors)

    notes = [e for e in errors if e.startswith("NOTE:")]
    failures = [e for e in errors if not e.startswith("NOTE:")]

    for note in notes:
        print(note)

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        mode = "DOM + report" if args.report else "DOM"
        print(f"\n--- {len(failures)} failure(s), {len(notes)} note(s) [{mode}] ---")
        sys.exit(1)
    else:
        mode = "DOM + report" if args.report else "DOM"
        print(f"PASS: Results valid ({len(notes)} note(s)) [{mode}]")
        sys.exit(0)


if __name__ == "__main__":
    main()
