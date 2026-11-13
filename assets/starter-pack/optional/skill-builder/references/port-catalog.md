# Port Type Catalog

Load this file during Step 7 (port definition) to help the author declare typed
inputs and outputs for their skill.

---

## What ports are

Ports are typed declarations of what a skill consumes (inputs) and produces
(outputs). They enable composition: when one skill's output type matches
another skill's input type, the two can chain together.

## Core port types

### severity-findings

Rated findings using the NNG 0-4 severity scale. Each finding has an ID,
summary, severity rating, evidence, and recommendation.

Used by: scenario-mould (output), heuristic-evaluation (output).
Feeds into: any skill that accepts evaluation findings.

### scorecard

Numeric scores organized by category. Each entry has a category name, score,
maximum possible score, and optional notes.

Used by: heuristic-evaluation (output), recurring-check skills (output).

### theme-codes

Qualitative analysis output: thematic codes with definitions, example quotes,
and frequency counts.

Used by: qualitative analysis skills (output).

### recommendations

Prioritized action items with title, priority, rationale, and effort estimate.

Used by: evaluation skills (output), audit skills (output).
Feeds into: project management and planning tools.

### checklist

Ordered pass/fail/NA criteria list.

Used by: recurring-check skills (output), audit skills (output).

### decision-log

Decision records with status (confirmed/delegated), value, evidence, and
assumptions.

Used by: session-flow skills (output).

### lifecycle-gate

Stage-gate result: pass, fail, revisit, or accept-risk with evidence and
optional sign-off.

Used by: lifecycle-aware skills (output).
Feeds into: lifecycle tracking and dashboard tools.

### component-ref

Reference to a UI component: file path, screenshot, or prose description.

Used by: scenario-mould (input), UI evaluation skills (input).

### artifact-html

A standalone single-file HTML artifact with no external dependencies.

Used by: scenario-mould (output), interactive tools (output).

### artifact-markdown

A markdown document.

Used by: most skills (output for reports).

### artifact-json

Structured JSON data.

Used by: most skills (output for session records, findings data).

### artifact-diagram

SVG diagram or Mermaid source.

Used by: architecture review skills (output), flow mapping skills (output).

### text-block

Freeform text. Catch-all for unstructured data.

---

## Widening rules

Some port types can substitute for broader types:

| Type | Widens to |
|------|-----------|
| severity-findings | artifact-json |
| scorecard | artifact-json |
| theme-codes | artifact-json |
| recommendations | artifact-json |
| checklist | artifact-json |
| decision-log | artifact-json |
| lifecycle-gate | artifact-json |
| artifact-markdown | text-block |
| artifact-json | text-block |

Widening means: if a skill's output is `severity-findings` and another skill's
input is `artifact-json`, the composition is valid because severity-findings
widens to artifact-json.

---

## Declaring ports

In the SKILL.md:
```yaml
ports:
  inputs:
    - name: component-source
      type: component-ref
      required: true
      description: The UI component to evaluate
  outputs:
    - name: findings
      type: severity-findings
      description: Rated findings with recommendations
    - name: report
      type: artifact-markdown
      description: Full evaluation report
```

In skill-manifest.json:
```json
{
  "ports": {
    "inputs": [
      { "name": "component-source", "type": "component-ref",
        "required": true, "description": "The UI component to evaluate" }
    ],
    "outputs": [
      { "name": "findings", "type": "severity-findings",
        "description": "Rated findings with recommendations" }
    ]
  }
}
```

---

## Composition discovery

After defining ports, the builder checks installed skills for compatible
connections:

1. For each output type, find skills with matching input types.
2. For each input type, find skills with matching output types.
3. Apply widening rules.
4. Report pairings to the author.
5. Add a `## Composition` section to the generated SKILL.md.
