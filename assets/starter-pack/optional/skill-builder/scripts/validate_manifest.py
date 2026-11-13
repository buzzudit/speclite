#!/usr/bin/env python3
"""Validate a skill-manifest.json against the speclite skill schema.

Usage: python3 validate_manifest.py <manifest.json> [--schema <schema.json>]
Exit 0 on PASS, 1 on FAIL.
"""

import argparse
import json
import re
import sys
from pathlib import Path

KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
COMMAND_RE = re.compile(r"^/[a-z][a-z0-9-]*$")

VALID_SHAPES = {"session-flow", "reference", "one-shot", "recurring-check"}
VALID_LIFECYCLE_STAGES = {"discover", "model", "build", "measure", None}
VALID_PROVENANCE_TYPES = {"standard", "vendor", "regulatory", "practice"}
VALID_DELIVERABLE_FORMATS = {"markdown", "html", "json", "diagram", "scorecard", "pdf", "csv"}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return False


def check_required_fields(data, errors):
    required = ["name", "version", "shape", "description", "invocable",
                 "provenance", "ports", "deliverables", "verification"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")


def check_name(data, errors):
    name = data.get("name", "")
    if not isinstance(name, str) or not KEBAB_RE.match(name):
        errors.append(f"'name' must be kebab-case, got: '{name}'")


def check_version(data, errors):
    version = data.get("version", "")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        errors.append(f"'version' must be semver, got: '{version}'")


def check_shape(data, errors):
    shape = data.get("shape")
    if shape not in VALID_SHAPES:
        errors.append(f"'shape' must be one of {VALID_SHAPES}, got: '{shape}'")


def check_description(data, errors):
    desc = data.get("description", "")
    if not isinstance(desc, str) or len(desc) < 10:
        errors.append("'description' must be a string of at least 10 characters")


def check_command(data, errors):
    if data.get("invocable") and "command" in data:
        cmd = data["command"]
        if cmd is not None and not COMMAND_RE.match(cmd):
            errors.append(f"'command' must match /name pattern, got: '{cmd}'")


def check_provenance(data, errors):
    prov = data.get("provenance")
    if not isinstance(prov, dict):
        errors.append("'provenance' must be an object")
        return

    for layer in ("academic", "industry"):
        entries = prov.get(layer)
        if not isinstance(entries, list) or len(entries) == 0:
            errors.append(f"'provenance.{layer}' must have at least one entry")
            continue
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"provenance.{layer}[{i}] is not an object")
                continue
            for field in ("claim", "source"):
                if field not in entry or not entry[field].strip():
                    errors.append(f"provenance.{layer}[{i}] missing '{field}'")

    if layer == "industry":
        for i, entry in enumerate(prov.get("industry", [])):
            ptype = entry.get("type")
            if ptype is not None and ptype not in VALID_PROVENANCE_TYPES:
                errors.append(f"provenance.industry[{i}] invalid type '{ptype}'")

    org = prov.get("organizational")
    if org is not None and not isinstance(org, list):
        errors.append("'provenance.organizational' must be an array or null")


def check_ports(data, errors):
    ports = data.get("ports")
    if not isinstance(ports, dict):
        errors.append("'ports' must be an object")
        return

    for direction in ("inputs", "outputs"):
        entries = ports.get(direction)
        if not isinstance(entries, list):
            errors.append(f"'ports.{direction}' must be an array")
            continue
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"ports.{direction}[{i}] is not an object")
                continue
            for field in ("name", "type", "description"):
                if field not in entry or not str(entry[field]).strip():
                    errors.append(f"ports.{direction}[{i}] missing '{field}'")

    outputs = ports.get("outputs", [])
    if isinstance(outputs, list) and len(outputs) == 0:
        errors.append("'ports.outputs' must have at least one entry")


def check_deliverables(data, errors):
    deliverables = data.get("deliverables")
    if not isinstance(deliverables, list) or len(deliverables) == 0:
        errors.append("'deliverables' must have at least one entry")
        return
    for i, d in enumerate(deliverables):
        if not isinstance(d, dict):
            errors.append(f"deliverables[{i}] is not an object")
            continue
        for field in ("id", "format", "description"):
            if field not in d:
                errors.append(f"deliverables[{i}] missing '{field}'")
        fmt = d.get("format")
        if fmt not in VALID_DELIVERABLE_FORMATS:
            errors.append(f"deliverables[{i}] invalid format '{fmt}'")


def check_verification(data, errors):
    ver = data.get("verification")
    if not isinstance(ver, dict):
        errors.append("'verification' must be an object")
        return

    criteria = ver.get("criteria")
    if not isinstance(criteria, list) or len(criteria) == 0:
        errors.append("'verification.criteria' must have at least one entry")
    else:
        for i, c in enumerate(criteria):
            if not isinstance(c, dict):
                errors.append(f"verification.criteria[{i}] is not an object")
                continue
            for field in ("id", "description", "automated"):
                if field not in c:
                    errors.append(f"verification.criteria[{i}] missing '{field}'")

    scripts = ver.get("scripts")
    if not isinstance(scripts, list):
        errors.append("'verification.scripts' must be an array")


def check_lifecycle(data, errors):
    lc = data.get("lifecycle")
    if lc is None:
        return
    if not isinstance(lc, dict):
        errors.append("'lifecycle' must be an object or omitted")
        return
    stage = lc.get("stage")
    if stage is not None and stage not in VALID_LIFECYCLE_STAGES:
        errors.append(f"lifecycle.stage must be one of {VALID_LIFECYCLE_STAGES}")


def main():
    parser = argparse.ArgumentParser(description="Validate a skill manifest.")
    parser.add_argument("manifest", help="Path to skill-manifest.json")
    args = parser.parse_args()

    path = Path(args.manifest)
    if not path.exists():
        print(f"FAIL: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"FAIL: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []
    check_required_fields(data, errors)
    check_name(data, errors)
    check_version(data, errors)
    check_shape(data, errors)
    check_description(data, errors)
    check_command(data, errors)
    check_provenance(data, errors)
    check_ports(data, errors)
    check_deliverables(data, errors)
    check_verification(data, errors)
    check_lifecycle(data, errors)

    if errors:
        print(f"FAIL: {len(errors)} validation error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"PASS: {path.name} is valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
