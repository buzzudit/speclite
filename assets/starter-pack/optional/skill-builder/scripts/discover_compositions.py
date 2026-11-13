#!/usr/bin/env python3
"""Discover composable skill pairs based on typed ports.

Scans all installed skills under .claude/skills/, reads their
skill-manifest.json, and finds pairs where one skill's output type matches
another's input type (with widening).

Usage: python3 discover_compositions.py [--skills-dir <path>] [--port-types <path>]
Exit 0 always. Prints discovered compositions.
"""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_WIDENING = {
    "severity-findings": ["artifact-json"],
    "scorecard": ["artifact-json"],
    "theme-codes": ["artifact-json"],
    "recommendations": ["artifact-json"],
    "checklist": ["artifact-json"],
    "decision-log": ["artifact-json"],
    "lifecycle-gate": ["artifact-json"],
    "artifact-markdown": ["text-block"],
    "artifact-json": ["text-block"],
}


def load_widening(port_types_path):
    if port_types_path and Path(port_types_path).exists():
        try:
            data = json.loads(Path(port_types_path).read_text())
            types = data.get("types", {})
            widening = {}
            for type_name, type_def in types.items():
                widens = type_def.get("widens_to", [])
                if widens:
                    widening[type_name] = widens
            return widening
        except (json.JSONDecodeError, KeyError):
            pass
    return DEFAULT_WIDENING


def types_compatible(output_type, input_type, widening):
    if output_type == input_type:
        return True
    return input_type in widening.get(output_type, [])


def discover(skills_dir, widening):
    skills = {}
    for manifest_path in skills_dir.glob("*/skill-manifest.json"):
        try:
            data = json.loads(manifest_path.read_text())
            name = data.get("name", manifest_path.parent.name)
            skills[name] = data
        except (json.JSONDecodeError, KeyError):
            continue

    if len(skills) < 2:
        return []

    compositions = []

    for out_name, out_data in skills.items():
        out_ports = out_data.get("ports", {}).get("outputs", [])
        for out_port in out_ports:
            out_type = out_port.get("type", "")

            for in_name, in_data in skills.items():
                if in_name == out_name:
                    continue
                in_ports = in_data.get("ports", {}).get("inputs", [])
                for in_port in in_ports:
                    in_type = in_port.get("type", "")
                    if types_compatible(out_type, in_type, widening):
                        compositions.append({
                            "from_skill": out_name,
                            "from_port": out_port.get("name", ""),
                            "from_type": out_type,
                            "to_skill": in_name,
                            "to_port": in_port.get("name", ""),
                            "to_type": in_type,
                            "required": in_port.get("required", True),
                            "widened": out_type != in_type,
                        })

    compositions.sort(key=lambda c: (not c["required"], c["widened"],
                                      c["from_skill"], c["to_skill"]))
    return compositions


def main():
    parser = argparse.ArgumentParser(description="Discover skill compositions.")
    parser.add_argument("--skills-dir", default=".claude/skills",
                        help="Path to skills directory")
    parser.add_argument("--port-types", default=None,
                        help="Path to port-types.json")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of human-readable")
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.is_dir():
        print(f"No skills directory at {skills_dir}", file=sys.stderr)
        sys.exit(0)

    widening = load_widening(args.port_types)
    compositions = discover(skills_dir, widening)

    if args.json:
        print(json.dumps(compositions, indent=2))
    elif not compositions:
        print("No compositions discovered.")
    else:
        print(f"Discovered {len(compositions)} composition(s):\n")
        for c in compositions:
            widened = " (widened)" if c["widened"] else ""
            required = " [required]" if c["required"] else " [optional]"
            print(f"  {c['from_skill']}.{c['from_port']} ({c['from_type']})")
            print(f"    → {c['to_skill']}.{c['to_port']} ({c['to_type']})"
                  f"{widened}{required}")
            print()


if __name__ == "__main__":
    main()
